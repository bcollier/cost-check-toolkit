# Build notes (facts for the write-up; not graded prose)

## Evidence from earlier prompt logs (cost / free fallback was the most repeated theme)
Ignatius at Home (HW4), PROMPT_LOG.md:
- "can we do a free version with free microsoft tts or a low cost version as well?"
- "I want to be able to choose the model, and I want to show estimated costs for both the elevenlabs production and the model calls"
- "can we have a free mode where we use a model I have academic access to on Jetstream so add one more key"
- "can I give you a key to tavily so we can enable web search in free mode?"
- "costs should not be on the iphone version, they should be displayed when building the retreat but not when playing through them"
About 125 prompts across the Ignatius and Faculty Twin logs mention cost, money or free.

## What happened while building (2026-11-11)
1. **The course's MCP example no longer runs.** `pip install mcp` installed 2.3.0, where `from mcp.server.fastmcp import FastMCP` raises an error: FastMCP was renamed `MCPServer` (`from mcp.server.mcpserver import MCPServer`). The server is written for 2.x and pins `mcp>=2.3,<3`.
2. **Claude Code called the tool on the first try.** A fresh `claude -p "How much does Claude Haiku cost per million input tokens right now?"` called `mcp__model-prices__model_prices` with `{'query': 'claude haiku'}` and answered $0.10/1M input.
3. **Codex saw the skill but ignored the tool.** Asked to "use any tool you have" for a GPT-5 mini price, Codex loaded its built-in `openai-docs` skill and used web search instead of `model_prices`.
4. **Codex then blocked the tool.** Asked to call `model_prices` by name, `codex exec` failed with "MCP tool call requires approval, but approval policy is never". Fix: mark the tool read-only, `@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))`. Rerun: "mcp: model-prices/model_prices (completed)", with real output.
5. **Open issue (candidate for ITERATION):** results sort cheapest first, so `:batch` variants (async, half price) come first. "openai/gpt-5-mini:batch $0.12" is listed above the normal $0.25 price, which a checker could quote as the price of an interactive call. Not fixed yet.

## Where things are installed on this machine
- Skill: symlinked to `~/.claude/skills/cost-check` and `~/.codex/skills/cost-check`.
- Claude Code: `claude mcp add --scope user model-prices -- <repo>/.venv/bin/python <repo>/mcp-server/model_prices_server.py`
- Codex: `~/.codex/config.toml`
  ```toml
  [mcp_servers.model-prices]
  command = "<repo>/.venv/bin/python"
  args = ["<repo>/mcp-server/model_prices_server.py"]
  ```
- Python 3.14 venv in `.venv` (`python3.14 -m venv .venv && .venv/bin/pip install -r mcp-server/requirements.txt`).
