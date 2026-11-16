# Build notes (facts for the write-up; not graded prose)

## Evidence from earlier prompt logs
Method: `notes/log_themes.py` takes only my own prompts (quoted with `>`, in code blocks, or in italics, depending on the log), removes duplicates, and counts prompts per theme by keyword. Keyword matching overcounts a little (e.g. "free" in "feel free"); the quotes below were read by hand.

| Theme | HW3 NHL Compare | HW3 gAIm Explorer | HW4 Ignatius | HW6 Slide Finder | HW7 Mime (phase 1) | HW7 Monday 8:55 (phase 2) | Project 2 Faculty Twin | Total |
|---|---|---|---|---|---|---|---|---|
| prompts in the log | 5 | 4 | 286 | 48 | 18 | 26 | 140 | 527 |
| screenshots ("here's what I see") | 0 | 0 | 62 | 0 | 0 | 0 | 1 | 63 |
| cost / free mode | 0 | 0 | 41 | 0 | 0 | 0 | 7 | 48 |
| look / design | 0 | 0 | 25 | 4 | 6 | 3 | 7 | 45 |
| deploy / push | 0 | 0 | 17 | 0 | 1 | 2 | 13 | 33 |
| README / docs | 0 | 0 | 15 | 2 | 1 | 0 | 13 | 31 |
| test it / it's broken | 1 | 1 | 13 | 3 | 0 | 0 | 12 | 30 |
| keys / secrets | 1 | 0 | 20 | 0 | 0 | 0 | 8 | 29 |
| spec first / still in spec? | 0 | 0 | 7 | 2 | 3 | 6 | 5 | 23 |
| phone / iPhone | 0 | 0 | 19 | 0 | 0 | 0 | 0 | 19 |
| student privacy / names | 0 | 0 | 4 | 0 | 0 | 0 | 8 | 12 |
| log my prompts | 0 | 0 | 3 | 1 | 1 | 2 | 3 | 10 |
| live link / play it on the web | 0 | 0 | 5 | 0 | 0 | 3 | 1 | 9 |
| stop and check with me | 0 | 0 | 0 | 0 | 3 | 0 | 1 | 4 |

There is no HW5 in this course: the homework list goes HW4, Project 2, HW6. HW7's phase 2 log is the second half of `monday-855/prompt_log.md` (from line 94); the first half is the original author's phase 1 log.

**Depth vs. breadth.** Cost is the deepest theme (48 prompts) but nearly all from one project (HW4). "Log my prompts" is the broadest: it shows up in HW4, HW6, both halves of HW7 and Project 2, and again in HW8 ("log all of my prompts starting from…"). Spec questions also span HW4 through HW7: "have you changed the spec since handoff?", "would it still be up to spec if we changed the setting", "keep to the spec but we want this to be awesome".

Cost quotes (HW4, Ignatius at Home, PROMPT_LOG.md), in the order I typed them:
- "can we do a free version with free microsoft tts or a low cost version as well?"
- "I want to be able to choose the model, and I want to show estimated costs for both the elevenlabs production and the model calls"
- "can we have a free mode where we use a model I have academic access to on Jetstream"
- "these should all have wrapping aroud them that safely drops them from the proces if we hit the c[redit limit]"
- "why only one research site, for the free version I assumed you would still use all four free search engines"
- "why does it say this retreat would cost 4.24 but it actually costed $21.13" (the estimate was five times too low)
- "default new retreats to opus 5.5, show estimated rates / cost when choosing the models"
- "How many minutes of content? Voices seem really expensive"
Project 2 (Faculty Twin): "I want it to run for free, would it fit in the free cloudflare budget?"; "track tokens spent in / out etc. to estimate spend"

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
