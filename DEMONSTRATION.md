# Demonstration

> ✍️ **WRITE THIS YOURSELF.** Including whether you agree with what the checker caught.

## The real task

Reviewing my previously built app to determine if there are API calls that I could replace with cheaper or free calls.

## Run 1
Details here: https://github.com/bcollier/cost-check-toolkit/blob/main/notes/excerpts/run1.md and https://github.com/bcollier/cost-check-toolkit/blob/main/notes/build-notes.md

### Doer session (shows the model_prices call)

Claude Code Opus 5.5

### Checker session (fresh, different model)

Codex (GPT-5.6)

## Run 2

Details here: https://github.com/bcollier/cost-check-toolkit/blob/main/notes/excerpts/run2.md and https://github.com/bcollier/cost-check-toolkit/blob/main/notes/build-notes.md

Ignatius's model menu in app/pricing.py is out of date. Bring MODELS and FALLBACK_PRICES up to today's Anthropic models and prices: add any current Claude models that are missing, fix labels like "fastest, cheapest" if they are no longer true, and update the fallback prices. Work on a new branch named demo/model-prices-run1, commit there, and do not push. Run the tests with .venv/bin/python -m pytest -q.

CALL  Skill  {"skill": "claude-api", "args": "Current Claude model IDs and per-million-token pricing, to update a model menu and fallback price table"}
  ->  Execute skill: claude-api
CALL  Read  {"file_path": "/Users/jarvis/Code/ignatius-at-home-api/app/pricing.py"}
  ->  1	"""Models the user can choose, their prices, and what each call actually cost.
2	
3	Prices come from OpenRouter's public model list (refreshed every few hours), with
4	the table below as a fallback. Costs are computed 
CALL  ToolSearch  {"query": "select:mcp__model-prices__model_prices", "max_results": 1}
  ->  
CALL  mcp__model-prices__model_prices  {"query": "claude", "limit": 40}
  ->  {"result":"36 models match 'claude'; showing 36, cheapest first (prices as of 2026-11-16):\nanthropic/claude-haiku-5.5:batch: $0.05 per 1M input tokens, $0.25 per 1M output tokens; context 1,000,000 tokens\nanthropic/cla
CALL  Bash  {"command": "git checkout -b demo/model-prices-run1 && grep -rn \"haiku\\|sonnet-5\\|opus-5\\|fable\\|FALLBACK_PRICES\\|MODELS\" --include=*.py --include=*.js --include=*.html --include=*.md . | grep -v \"^./.venv\" | he
  ->  Switched to a new branch 'demo/model-prices-run1'
(eval):1: no matches found: --include=*.py
CALL  ToolSearch  {"query": "select:WebFetch,WebSearch", "max_results": 2}
  ->  
CALL  Bash  {"command": "grep -rnE \"haiku|sonnet-5|opus-5|fable|FALLBACK_PRICES|BASIC_SEARCH|fastest|cheapest|most capable\" --exclude-dir=.venv --exclude-dir=.git --exclude-dir=node_modules . | grep -v \"prompt-log\\|PROMPT\" | he
  ->  Binary file ./evals/__pycache__/fitness.cpython-312.pyc matches
Binary file ./evals/__pycache__/common.cpython-312.pyc matches
./evals/common.py:29:    "opus": ("openrouter", "anthropic/claude-opus-5.5", "Claude Opus 5.5
CALL  WebFetch  {"url": "https://platform.claude.com/docs/en/about-claude/pricing", "prompt": "List every current Claude model with its API model ID, base input price, 5-minute cache write, 1-hour cache write, cache hit/read, and output
  ->  <persisted-output>
Output too large (54.2KB). Full output saved to: /Users/jarvis/.claude/projects/-Users-jarvis-Code-ignatius-at-home-api/e9625d8d-4247-445c-b42c-51748a4a08bf/tool-results/toolu_01JLxFgfBDTFkCKU9aVmfKN2.
CALL  WebFetch  {"url": "https://platform.claude.com/docs/en/about-claude/models/overview", "prompt": "List all current (latest) Claude models with their API IDs, descriptions (e.g. fastest, most capable), and relative latency. List leg
  ->  ---
title: Models overview
url: https://platform.claude.com/docs/en/models/overview
description: Claude is a family of state-of-the-art large language models developed by Anthropic. This guide introduces the available mo
SAYS  Anthropic's docs list newer models than the app has (Fable 5.2, Sonnet 5.5, Haiku 5.5). Next I'm reading the full pricing table for cache rates and Haiku 5.5's "from" pricing.
CALL  Grep  {"pattern": "Haiku 5\\.5|Sonnet 5\\.5|Opus 5\\.5|Opus 5 |Sonnet 5 |Haiku 4\\.5|Fable 5\\.2|Fable 5\\.1|web search|Web search|\\$10 per 1,000|tier|Tier|From \\$", "path": "/Users/jarvis/.claude/projects/-Users-jarvis-Code
  ->  17:| Claude Fable 5.2                                                                                                                                                       | $8 / MTok             | $10 / MTok      | $16 
CALL  Bash  {"command": "F=/Users/jarvis/.claude/projects/-Users-jarvis-Code-ignatius-at-home-api/e9625d8d-4247-445c-b42c-51748a4a08bf/tool-results/toolu_01JLxFgfBDTFkCKU9aVmfKN2.txt; sed -n '40,50p;253p;360,376p' \"$F\" | cut -c1-9
  ->  A variable set in this command can't be checked before it runs
CALL  WebFetch  {"url": "https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool", "prompt": "Which models support web_search_20260209 (dynamic filtering) versus only web_search_20250305? Specifically: Claude Haiku
  ->  ---
title: Web search tool
url: https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool
description: Give Claude access to current web content with cited sources, optional dynamic filtering, and dom
CALL  Read  {"file_path": "/Users/jarvis/.claude/projects/-Users-jarvis-Code-ignatius-at-home-api/e9625d8d-4247-445c-b42c-51748a4a08bf/tool-results/toolu_01JLxFgfBDTFkCKU9aVmfKN2.txt", "offset": 40, "limit": 8}
  ->  40	*<sup>1 Cache hits and refreshes on Claude Fable 5.2, Claude Mythos 5.2, Claude Fable 5.1, and Claude Mythos 5.1 are priced at 0.025x the base input price.</sup>*
41	
42	*<sup>2 Cache hits and refreshes on Claude Opus
CALL  Grep  {"pattern": "100,000 tokens|Haiku 5.5", "path": "/Users/jarvis/.claude/projects/-Users-jarvis-Code-ignatius-at-home-api/e9625d8d-4247-445c-b42c-51748a4a08bf/tool-results/toolu_01JLxFgfBDTFkCKU9aVmfKN2.txt", "output_mode"
  ->  36:| Claude Haiku 5.5 (for prompts up to 100,000 tokens)                                                                                                                    | $0.10 / MTok          | $0.125 / MTok   | $0.2
SAYS  All the prices check out against Anthropic's pricing page. Now editing `app/pricing.py`.
CALL  Edit  {"replace_all": false, "file_path": "/Users/jarvis/Code/ignatius-at-home-api/app/pricing.py", "old_string": "    (\"anthropic/claude-opus-5.5\", \"claude-opus-5-5\", \"Claude Opus 5.5 (default)\"),\n    (\"anthropic/clau
  ->  The file /Users/jarvis/Code/ignatius-at-home-api/app/pricing.py has been updated successfully. (file state is current in your context — no need to Read it back)
CALL  Edit  {"replace_all": false, "file_path": "/Users/jarvis/Code/ignatius-at-home-api/app/pricing.py", "old_string": "# Dollars per token, and per web search. Used when OpenRouter can't be reached.\nFALLBACK_PRICES = {\n    \"ant
  ->  The file /Users/jarvis/Code/ignatius-at-home-api/app/pricing.py has been updated successfully. (file state is current in your context — no need to Read it back)
CALL  Bash  {"command": ".venv/bin/python -m pytest -q 2>&1 | tail -15", "description": "Run the test suite", "timeout": 600000}
  ->  =============================== warnings summary ===============================
<frozen importlib._bootstrap>:488
<frozen importlib._bootstrap>:488
  <frozen importlib._bootstrap>:488: DeprecationWarning: builtin type S
CALL  Bash  {"command": "git add app/pricing.py && git commit -q -F - <<'EOF'\nModel menu: add Fable 5.2, Sonnet 5.5, Haiku 5.5; refresh fallback prices\n\nPrices checked against Anthropic's pricing page on 2026-11-16. Fable 5.2 is\
  ->  3f60323 Model menu: add Fable 5.2, Sonnet 5.5, Haiku 5.5; refresh fallback prices
SAYS  I've updated `app/pricing.py` and committed it as `3f60323` on the new branch `demo/model-prices-run1` (not pushed). All 161 tests pass. I checked the prices against Anthropic's own pricing and models pages as of today, 


### Doer session

Claude Opus 5.5

### Checker session

Codex (GPT-5.6)

## What the checker caught, and whether I agree

I ran it first on the chat model being used in Ignatius App, it found savings from switching to Haiku from Sonnet

The second run updated models from 5.1 to 5.5 in all API calls.