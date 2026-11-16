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

### 7. 2026-11-16
> ok I'm ready to test it out

Reminded me of the demo requirements (notes/ASSIGNMENT_CHECKLIST.md). Picked a real task: Ignatius's model menu (`app/pricing.py`) still called Haiku 4.5 "fastest, cheapest" and lacked the 5.5 models. Run 1 doer: a fresh `claude -p` session (Opus 5.5) in the Ignatius API repo, told to update the menu and fallback prices on a local branch without pushing. The prompt does not name `model_prices`; web search was also allowed. Transcript: notes/runs/run1-doer.jsonl.

### 8. 2026-11-16
> remove the HW8 and CS name in teh description of this repo HW8 (CMU 15-114): a cost-check skill and a model_prices MCP server. be specific that this is for API costs correct?

Changed the GitHub description to "An agent skill that flags paid API calls (LLM, text-to-speech, search) and whether each has a free fallback, plus an MCP server that looks up live LLM API prices".

### 9. 2026-11-16
> explain DEMONSTRATION.md, also where is documentation around the two skill runs? is this all up on github, I watn to run on laptop

Explained what DEMONSTRATION.md must contain. Run 1's facts were already pushed in `notes/build-notes.md`, but the raw transcripts were not (`notes/runs/` is git-ignored). Added `notes/excerpts/run1.md`, verbatim and trimmed, so the runs can be read on GitHub. Gave laptop install steps. Only Run 1 had been done.

### 10. 2026-11-16
> do this Switching those is real work that would make them about 10 times cheaper. Want me to run it, or would you rather pick the task?

Run 2. Doer: a fresh `claude -p` session (Opus 5.5) in the Ignatius API repo, told to switch the fast model in `app/preview.py` and `app/talk_turns.py` from Haiku 4.5 to Haiku 5.5. It worked on a new local branch built on Run 1's, with no push. The prompt does not name `model_prices`. Then a fresh Codex checker session. Transcripts: notes/runs/run2-*.

### 11. 2026-11-16
> is the skill and mcp up on github so I can try it on my lapotp

Checked GitHub. `skills/cost-check/SKILL.md`, `mcp-server/model_prices_server.py` (with the read-only fix for Codex) and `requirements.txt` were all there and current. Pushed the prompt log.

(Run 2 finished: notes/excerpts/run2.md, and the "Run 2" section of notes/build-notes.md. The branch `demo/haiku-5-5-run2` is pushed to ignatius-at-home-api, not merged.)

### 12. 2026-11-16
> explain this The same format drift both times. Each report opened with a verdict line (“Push verdict: hold…”, “Cost review: pass…”) and added prose outside the fixed format. Since it happened twice, it’s a pattern rather than luck, and a stricter rule in SKILL.md is easy to fix and rerun
>
> also,  I drop the parts of the server that say to show the costs to the user. remind me what the cost check output goes? I want it to check whether all API calls are properly logged on both send and receive, and that all associated costs for the API calls should be logged for analytics.

Explained the format drift and where the report goes. Revised the skill to v2. Removed: the "is the cost shown to the user" check and the COST SHOWN/HIDDEN tags (now explicitly out of scope). Added: checks that each paid call is logged when sent and when the response comes back (including failures), and that its cost is computed from actual usage and stored for analytics. Kept: the free-fallback check. The output format now forbids anything before or after the lines and gaps (no verdict, summary, headings or model advice). v1 is saved at notes/skill-versions/SKILL.v1.md. Reran the checker with v2 on both demo branches.

(v2 reruns finished: notes/excerpts/iteration-v2.md, and the "Skill v2 rerun" section of notes/build-notes.md.)
