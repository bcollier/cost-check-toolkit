"""MCP server with one tool: current model prices from OpenRouter's public model list."""
import json
import sys
import time
import urllib.request

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

MODELS_URL = "https://openrouter.ai/api/v1/models"
CACHE_SECONDS = 600

mcp = MCPServer("model-prices")
_cache = {"at": 0.0, "models": []}


def log(msg):
    # stdout carries the MCP protocol, so anything for humans goes to stderr
    print(f"[model-prices] {msg}", file=sys.stderr)


def load_models():
    if time.time() - _cache["at"] < CACHE_SECONDS and _cache["models"]:
        return _cache["models"]
    req = urllib.request.Request(MODELS_URL, headers={"User-Agent": "cost-check-toolkit"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        models = json.load(resp)["data"]
    _cache.update(at=time.time(), models=models)
    log(f"fetched {len(models)} models")
    return models


def per_million(price):
    # OpenRouter quotes dollars per token as a string; negative means the price varies
    value = float(price or 0)
    if value < 0:
        return None
    return value * 1_000_000


def describe(model):
    pricing = model.get("pricing", {})
    p_in, p_out = per_million(pricing.get("prompt")), per_million(pricing.get("completion"))
    if p_in is None or p_out is None:
        cost = "price varies by routed model"
    elif p_in == 0 and p_out == 0:
        cost = "FREE"
    else:
        cost = f"${p_in:,.2f} per 1M input tokens, ${p_out:,.2f} per 1M output tokens"
    return f"{model['id']}: {cost}; context {model.get('context_length', '?'):,} tokens"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
def model_prices(query: str, limit: int = 10) -> str:
    """Look up today's price for AI language models, from OpenRouter's live model list.

    Use this whenever a cost matters: estimating what an LLM feature will cost,
    checking whether a model has a free version, or comparing models on price.
    Do not answer prices from memory; they change often and your training data is stale.

    query: words that must all appear in the model id or name, e.g. "claude sonnet",
      "gpt-5 mini", "llama", "deepseek", or "free" for zero-cost models.
    limit: how many matches to return, cheapest first (default 10).

    Returns one line per model with its OpenRouter id, input and output price in
    US dollars per million tokens, and context length. Prices are OpenRouter's;
    calling a provider directly can cost slightly less. Covers text and multimodal
    LLMs only, not text-to-speech, image generation or search APIs.
    """
    try:
        models = load_models()
    except Exception as exc:
        return f"Could not reach OpenRouter ({exc}). No prices available right now."

    words = query.lower().split()
    matches = [m for m in models if all(w in f"{m['id']} {m.get('name', '')}".lower() for w in words)]
    if not matches:
        return f"No models match '{query}'. Try fewer or shorter words, such as a provider name."

    def sort_key(m):
        p = per_million(m.get("pricing", {}).get("prompt"))
        return float("inf") if p is None else p

    matches.sort(key=sort_key)
    shown = matches[: max(1, limit)]
    lines = [describe(m) for m in shown]
    header = f"{len(matches)} models match '{query}'; showing {len(shown)}, cheapest first (prices as of {time.strftime('%Y-%m-%d')}):"
    return "\n".join([header, *lines])


if __name__ == "__main__":
    mcp.run()
