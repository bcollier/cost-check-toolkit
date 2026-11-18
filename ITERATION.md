# Iteration

## What went wrong

In both demo runs the checker recommended showing prices to the user instead of checking whether the API calls were logged. In Run 2 its top fix was "Show the preview's estimated cost before automatically running it." That goes against a rule I set for Ignatius in HW4: "I don't want costs shown in the regular app, there should be a settings or log page tucked away somewhere."

There was a second, smaller problem in both runs: the reports didn't stick to the output format. Each one opened with a verdict line ("Push verdict: hold for one cost-accounting bug", "Cost review: pass with one disclosure caveat") and ended with paragraphs of advice, including which model to use.

## Why

The checker was doing what my first version of the skill told it to. v1's output format required a `[COST SHOWN | COST HIDDEN]` tag on every line (see [notes/skill-versions/SKILL.v1.md](notes/skill-versions/SKILL.v1.md)), so it treated a hidden cost as a problem to fix. I didn't catch that when I wrote it. What I actually care about is whether every call and its cost are recorded so I can analyze spending later, not whether the user sees a price.

The format drift was also partly my fault. v1 said to follow the lines with "a short list: the three calls most likely to cost real money, cheapest fix first." Asking for fixes invited advice, and nothing said where the report had to stop.

## What I changed

I rewrote the skill as v2 ([skills/cost-check/SKILL.md](skills/cost-check/SKILL.md)):

- Replaced the COST SHOWN / COST HIDDEN tag with three checks: `SENT` (is the request logged when it goes out), `RECEIVED` (is the response logged, including failures) and `COST` (is the cost from actual usage stored for analytics).
- Added a rule: "Whether the user sees the cost is out of scope. Do not report it."
- Tightened the format: one line per paid call and nothing before it, then up to three gaps, and "End there: no verdict, no summary, no headings, no advice on which model to use."

## Rerun result

I reran the checker with v2 on the same two branches with the same prompts, in a fresh Codex session. The full reports are in [notes/excerpts/iteration-v2.md](notes/excerpts/iteration-v2.md).

- It no longer mentions showing costs to the user.
- It found a real logging gap that v1 missed: paid requests aren't logged when they're sent, because "app/llm.py:75 writes the first record only after the response or failure."
- On the Run 2 branch it also found that costs are rounded to $0.0001 before they're stored, so at Haiku 5.5 prices "charges below $0.00005 are recorded as zero."
- The verdict lines and advice paragraphs are gone. The one thing left is small: one report labels its gaps `GAP:` and the other `Gap:`.

Before (v1, Run 2):
```
[FREE FALLBACK] [COST HIDDEN] app/preview.py:53 — OpenRouter/Anthropic, Claude Haiku 5.5 — $0.10/$0.50 per 1M input/output tokens
```

After (v2, same branch):
```
[SENT: NOT LOGGED] [RECEIVED: LOGGED] [COST: LOGGED] [FREE FALLBACK] app/preview.py:53 — OpenRouter/Anthropic, anthropic/claude-haiku-5.5 — $0.10/$0.50 per 1M input/output tokens; ...
Gap: app/pricing.py:160 rounds each call to $0.0001 before app/llm_log.py:103 stores it; at Haiku 5.5 prices, charges below $0.00005 are recorded as zero.
```
