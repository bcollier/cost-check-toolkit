# Prompt log

The prompts given to AI tools while building this toolkit, in order and verbatim. The assignment does not require a log; it is kept for the README's "how I used AI" note.

Tool: Claude Code (model Claude Opus 5.5), working on a Mac with this repo checked out.

### 1. 2026-11-11
> give me ideas on what to do for this assignment https://www.cs.cmu.edu/~113/hw8.html

Read the HW8 page and searched the Ignatius at Home and Faculty Twin prompt logs (432 entries) for repeated instructions. Suggested pairs of a checker skill and an MCP tool, each with quotes from the logs, and recommended a `cost-check` skill paired with a `model_prices` tool. Noted that the posted due dates had passed.

### 2. 2026-11-11
> yes get it started . when it comes time for me to do a demo, remind me what the assignment requires. start a repo for this project

Created this repo with the `cost-check` skill, the `model_prices` MCP server (mcp 2.x, OpenRouter's public model list), stub README / DEMONSTRATION / ITERATION files to be written by hand, and `notes/ASSIGNMENT_CHECKLIST.md` for the demo. Registered the server in Claude Code and Codex, and installed the skill in both. Smoke tests: Claude Code called the tool on the first try. Codex first used web search instead, then was blocked by its approval policy; marking the tool read-only fixed that. Details are in `notes/build-notes.md`.

### 3. 2026-11-11
> log all of my prompts starting from give me ideas on what to do for this assignment https://www.cs.cmu.edu/~113/hw8.html

Started this file with prompts 1–3.

### 4. 2026-11-13
> push this yourself

Created the public GitHub repo bcollier/cost-check-toolkit and pushed. Ben had asked for it after the first attempt was blocked.
