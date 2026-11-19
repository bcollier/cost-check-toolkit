# Demonstration

## The real task

My Ignatius at Home app (HW4) lets users pick which Claude model writes their retreat, and it keeps a price table for estimating cost. Both had fallen out of date. I gave Claude Code two real updates to make on separate branches, and before pushing each one I had Codex check the branch with the `cost-check` skill:

- **Run 1:** bring the model menu and fallback prices in `app/pricing.py` up to today's Anthropic models.
- **Run 2:** switch the app's fast model from Claude Haiku 4.5 to the newer and much cheaper Haiku 5.5.

The doer was Claude Code (Opus 5.5) with `model_prices` available. The checker was Codex (GPT-5.6) in a fresh, read-only session, so a different model checked the work. Full transcripts, trimmed but not reworded, are in [notes/excerpts/run1.md](notes/excerpts/run1.md) and [notes/excerpts/run2.md](notes/excerpts/run2.md).

## Run 1

### Doer session (shows the model_prices call)

Claude Code (Opus 5.5), fresh `claude -p` session in the Ignatius repo.

Prompt:
```
Ignatius's model menu in app/pricing.py is out of date. Bring MODELS and FALLBACK_PRICES up to today's Anthropic models and prices: add any current Claude models that are missing, fix labels like "fastest, cheapest" if they are no longer true, and update the fallback prices. Work on a new branch named demo/model-prices-run1, commit there, and do not push. Run the tests with .venv/bin/python -m pytest -q.
```

The prompt doesn't mention the tool, but the agent called it:
```
CALL  mcp__model-prices__model_prices  {"query": "claude", "limit": 40}
  ->  {"result":"36 models match 'claude'; showing 36, cheapest first (prices as of 2026-11-16):\nanthropic/claude-haiku-5.5:batch: $0.05 per 1M input tokens, $0.25 per 1M output tokens; ...
```

It added Fable 5.2, Sonnet 5.5 and Haiku 5.5 to the menu, updated the fallback prices, and committed `3f60323`. All 161 tests passed. It also noticed that Haiku 5.5 costs 5× more once a prompt goes over 100,000 tokens, which the app's price meter can't represent.

### Checker session (fresh, different model)

Codex (GPT-5.6), fresh `codex exec --sandbox read-only` session. I didn't name the skill.

Prompt:
```
I'm about to push the branch demo/model-prices-run1 (compare it to main with git diff main...demo/model-prices-run1). Check it for API costs before I push.
```

Codex loaded the skill on its own:
```
I'm using the cost-check skill because this branch is headed for push and may introduce model or paid-API calls. I'll inspect its rules, then review the exact `main...demo/model-prices-run1` diff without modifying anything.
```

It called `model_prices` 9 times. Part of its report (skill v1):
```
[FREE FALLBACK] [COST SHOWN] app/llm.py:87 — Anthropic/OpenRouter, Claude Sonnet 5.5 — $2/$10 per 1M input/output tokens
[FREE FALLBACK] [COST HIDDEN] app/llm.py:87 — Anthropic/OpenRouter, Claude Haiku 5.5 — $0.10/$0.50 through 100k prompt tokens; $0.50/$2.50 above 100k
```

## Run 2

### Doer session

Claude Code (Opus 5.5), fresh `claude -p` session.

Prompt:
```
Ignatius still uses Claude Haiku 4.5 as its fast model: FAST_CLAUDE in app/preview.py, and the brain choices in app/talk_turns.py. Switch them to Claude Haiku 5.5, which is newer and much cheaper, and make sure any speed or cost wording next to it is still true. Start from the branch demo/model-prices-run1: make a new branch demo/haiku-5-5-run2 from it, commit there, and do not push. Run the tests with .venv/bin/python -m pytest -q.
```

The tool call:
```
CALL  mcp__model-prices__model_prices  {"query": "claude haiku"}
  ->  {"result":"5 models match 'claude haiku'; showing 5, cheapest first (prices as of 2026-11-16):\nanthropic/claude-haiku-5.5:batch: $0.05 per 1M input tokens, $0.25 per 1M output tokens; ...
```

It switched the file preview and the "talk it over" brain to Haiku 5.5 and fixed the wording in 7 files, and committed `62c9271`. All 161 tests passed. It changed the cost label to "under a tenth of a cent a reply," since Haiku 5.5 is $0.10 / $0.50 per million tokens against $1 / $5 for Haiku 4.5. It also removed the speed claims, because it had no timing for the new model.

### Checker session

Codex (GPT-5.6), fresh read-only session.

Prompt:
```
I'm about to push the branch demo/haiku-5-5-run2. Its new work is git diff demo/model-prices-run1...demo/haiku-5-5-run2. Check it for API costs before I push.
```

Codex loaded the skill on its own again:
```
I'm using the cost-check skill because this diff is about to be pushed and may contain paid API calls. I'll inspect the full branch diff and report only—no edits.
```

It called `model_prices` twice. Its report (skill v1):
```
[FREE FALLBACK] [COST HIDDEN] app/preview.py:53 — OpenRouter/Anthropic, Claude Haiku 5.5 — $0.10/$0.50 per 1M input/output tokens
[FREE FALLBACK] [COST HIDDEN] app/talk_turns.py:161 — OpenRouter, Claude Haiku 5.5 conversation summary — $0.10/$0.50 per 1M input/output tokens
[FREE FALLBACK] [COST SHOWN] app/talk_turns.py:177 — OpenRouter, Claude Haiku 5.5 companion reply — $0.10/$0.50 per 1M input/output tokens
```

Its top suggestion was "Show the preview's estimated cost before automatically running it."

## What the checker caught, and whether I agree

**Run 1: Haiku 5.5's higher price over 100k tokens isn't counted.** The app stores only the lower rate and never applies the 5× rate above 100k tokens (`app/pricing.py:59` and `:140`). This is a real gap in the price meter. In practice the places that use Haiku don't get close: the companion's context is capped at 60,000 characters (about 15,000 tokens) and the preview reads 6,000 characters. 

I agreed with this finding, and asked for revisions.

**Run 2: show the user what the preview and summary cost.** I disagree. In HW4 I decided costs shouldn't be shown in the regular app: "I don't want costs shown in the regular app, there should be a settings or log page tucked away somewhere." The checker was only following my v1 skill, which had a COST SHOWN / COST HIDDEN tag. That became my iteration (see [ITERATION.md](ITERATION.md)).

**After the fix (skill v2), on the same two branches:**

- **Requests aren't logged when they're sent.** The log is written only after the response comes back (`app/llm.py:75`). If the process dies mid-call, there's no record that the request went out. 

I agreed this was a problem when we were designing it and didn't fix it then. This is correct that I should improve the logging of outbound API calls.

- **Very cheap calls are recorded as $0.** Each call's cost is rounded to $0.0001 before it's stored (`app/pricing.py:160`), so at Haiku 5.5 prices anything under $0.00005 shows up as zero. 

Both are true when I check the code. in pricying.py This needs to be fixed because we do have very small calles apparently as small as $0.0002 so it could be possible the log is missing some small charges that are being rounded. This would be a JIRA bug to fix.

"usd": round(self.usd, 4),     # line 160

**Run 3 (extra):** I also asked Codex Desktop to "look at the code for ignatius and run the cost check skill" on the whole app, not just a branch. It made 17 `model_prices` calls and found three gaps. The biggest one: "xAI can continue billing after the server's recorded limit" (`app/talk.py:430`). See [notes/excerpts/run3.md](notes/excerpts/run3.md).
