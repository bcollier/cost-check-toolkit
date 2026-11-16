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

### 5. 2026-11-16
> tell me more about this I searched your Ignatius and Faculty Twin prompt logs (432 entries) for things you kept repeating. Here’s what came up, with quotes you could use as evidence.

Redid the search properly. The first pass had counted every line of the logs, including the agent's summaries, and had missed the HW3 and HW6 logs. The new pass counts only my own quoted prompts (478 across HW3, HW4, HW6 and Project 2) by theme. The script is `notes/log_themes.py` and the table and quotes are in `notes/build-notes.md`. Cost came out as 48 prompts, not about 125. Screenshots of the live site were the most common theme at 63.

### 6. 2026-11-16
> the logs for HW5 and HW7 should be on the prompt logs of their repos/

Found the logs. The course has no HW5: Project 2 sits in that slot. HW7 has two logs: `mime-over-matter` (phase 1, prompts in code blocks) and the second half of `monday-855/prompt_log.md` (phase 2, from line 94; the first half is the original author's). Also added a second HW3 log (`nhl-player-compare`). Cloned these repos locally, taught `notes/log_themes.py` the three log formats, and reran it: 527 prompts across seven logs. HW7 adds no cost prompts, but "log my prompts" turns out to be the broadest theme, appearing in five projects plus HW8.
