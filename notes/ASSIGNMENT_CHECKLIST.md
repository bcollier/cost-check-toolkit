# HW8 checklist: Build Your Own Agent Toolkit

Source: https://www.cs.cmu.edu/~113/hw8.html (CMU 15-114, Fall 2026). Due Mon 11/9, 8:00 PM; Google form by Sun 11/8, 8:00 PM.

## Grading (100)
| Part | Points | What they look for |
|---|---|---|
| Skill | 20 | A checker with a narrow job, specific steps, a fixed output format, and a description that makes the agent load it at the right time |
| MCP server | 25 | One working tool, registered, shown being called; install steps good enough for the TAs to run it |
| Grounding | 15 | Quotes from your own prompt logs (HW3–HW7) that justify the skill and the tool |
| Demonstration | 20 | The toolkit used on real work, the checker in a separate session, two runs; transcripts show the tool call |
| Iteration | 20 | One failure, your diagnosis, the change, the rerun. Weighted heavily |

## Before the demo: what it has to show
- [ ] A **real task**: a past assignment piece redone, Project 3 groundwork, another class or a personal project.
- [ ] **Session A (the doer)** does the task with `model_prices` available. Its transcript must show the tool call.
- [ ] **Session B (the checker)** is a **separate, fresh session**, ideally a **different model** (plan: Codex), and runs `cost-check` on Session A's work.
- [ ] Do it **twice** (Run 1 and Run 2) to show it is consistent, not lucky.
- [ ] **Save transcripts as you go** into `notes/runs/` (git-ignored); trim the excerpts later.
- [ ] Note what the checker caught and **whether you agree**. Only you can write that part.
- [ ] Find one place the skill or tool **misfired**, fix it, rerun, and keep the before and after.

## Files in the repo (public GitHub)
- [ ] `skills/cost-check/SKILL.md`: copyable skill folder
- [ ] `mcp-server/` source + `requirements.txt`
- [ ] `README.md`, **written by you**: what each piece does and when it triggers; the friction with log quotes; install (skill directory + exact server config, machine paths marked); tools confirmed (Claude Code, Codex); what was borrowed (the spec-check example's structure); how AI was used, with citations
- [ ] `DEMONSTRATION.md`, **written by you**: the task; both runs with trimmed transcripts; what the checker caught and whether you agree
- [ ] `ITERATION.md`, **written by you**: what went wrong; why; what changed; rerun result
- [ ] Keep README, DEMONSTRATION and ITERATION as separate files
- [ ] Submit the repo link on the Google form

No prompt log is required, though `prompt_log.md` is kept anyway. Heavily AI-written prose can lose points.
