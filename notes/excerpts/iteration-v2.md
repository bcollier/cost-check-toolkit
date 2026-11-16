# Skill v2 reruns (verbatim, trimmed)

Same branches and the same checker prompts as Runs 1 and 2, in a fresh Codex (GPT-5.6) read-only session with `skills/cost-check/SKILL.md` v2. The v1 skill is at `notes/skill-versions/SKILL.v1.md`; the v1 reports are at the end of `run1.md` and `run2.md`.

## Run 1 branch, skill v2

**Prompt:**
```
I'm about to push the branch demo/model-prices-run1 (compare it to main with git diff main...demo/model-prices-run1). Check it for API costs before I push.
```

**Skill loaded:**
```
I’m using the cost-check skill because this is a pre-push review of paid API usage. I’ll inspect the branch diff and report findings only; I won’t modify anything.
```

**MCP calls:** 14 completed

**Report:**
```
[SENT: NOT LOGGED] [RECEIVED: LOGGED] [COST: LOGGED] [FREE FALLBACK] app/llm.py:87 — OpenRouter/Anthropic, claude-opus-5.5 — $4/$20 per 1M input/output tokens; response/cost recorded at app/llm.py:75, app/pricing.py:129, app/llm_log.py:100
[SENT: NOT LOGGED] [RECEIVED: LOGGED] [COST: LOGGED] [FREE FALLBACK] app/llm.py:87 — OpenRouter/Anthropic, claude-fable-5.2 — $8/$40 per 1M input/output tokens; response/cost recorded at app/llm.py:75, app/pricing.py:129, app/llm_log.py:100
[SENT: NOT LOGGED] [RECEIVED: LOGGED] [COST: LOGGED] [FREE FALLBACK] app/llm.py:87 — OpenRouter/Anthropic, claude-fable-5.1 — $10/$50 per 1M input/output tokens; response/cost recorded at app/llm.py:75, app/pricing.py:129, app/llm_log.py:100
[SENT: NOT LOGGED] [RECEIVED: LOGGED] [COST: LOGGED] [FREE FALLBACK] app/llm.py:87 — OpenRouter/Anthropic, claude-opus-5 — $5/$25 per 1M input/output tokens; response/cost recorded at app/llm.py:75, app/pricing.py:129, app/llm_log.py:100
[SENT: NOT LOGGED] [RECEIVED: LOGGED] [COST: LOGGED] [FREE FALLBACK] app/llm.py:87 — OpenRouter/Anthropic, claude-sonnet-5.5 — $2/$10 per 1M input/output tokens; response/cost recorded at app/llm.py:75, app/pricing.py:129, app/llm_log.py:100
[SENT: NOT LOGGED] [RECEIVED: LOGGED] [COST: LOGGED] [FREE FALLBACK] app/llm.py:87 — OpenRouter/Anthropic, claude-sonnet-5 — $2/$10 per 1M input/output tokens; response/cost recorded at app/llm.py:75, app/pricing.py:129, app/llm_log.py:100
[SENT: NOT LOGGED] [RECEIVED: LOGGED] [COST: LOGGED] [FREE FALLBACK] app/llm.py:87 — OpenRouter/Anthropic, claude-haiku-5.5 — $0.10/$0.50 per 1M input/output tokens; response/cost recorded at app/llm.py:75, app/pricing.py:129, app/llm_log.py:100
[SENT: NOT LOGGED] [RECEIVED: LOGGED] [COST: LOGGED] [FREE FALLBACK] app/llm.py:87 — OpenRouter/Anthropic, claude-haiku-4.5 — $1/$5 per 1M input/output tokens; response/cost recorded at app/llm.py:75, app/pricing.py:129, app/llm_log.py:100
GAP: Haiku 5.5 prompts over 100k tokens are charged at 5× the listed input rate, but app/pricing.py:141 always applies the base rate despite the warning at app/pricing.py:51.
GAP: Paid Claude requests have no send-time record; app/llm.py:75 writes the first record only after the response or failure.
```

## Run 2 branch, skill v2

**Prompt:**
```
I'm about to push the branch demo/haiku-5-5-run2. Its new work is git diff demo/model-prices-run1...demo/haiku-5-5-run2. Check it for API costs before I push.
```

**Skill loaded:**
```
I’m using the cost-check skill because this is a pre-push audit of paid API usage. I’ll inspect exactly the diff you named and report findings only—no edits.
```

**MCP calls:** 1 completed

**Report:**
```
[SENT: NOT LOGGED] [RECEIVED: LOGGED] [COST: LOGGED] [FREE FALLBACK] app/preview.py:53 — OpenRouter/Anthropic, anthropic/claude-haiku-5.5 — $0.10/$0.50 per 1M input/output tokens; response/failure log: app/llm.py:75, app/llm_log.py:98, app/storage.py:340; actual-usage cost: app/llm.py:99, app/pricing.py:129, app/llm_log.py:103; free path: app/preview.py:25,49
[SENT: NOT LOGGED] [RECEIVED: LOGGED] [COST: LOGGED] [FREE FALLBACK] app/talk_turns.py:177 — OpenRouter/Anthropic, anthropic/claude-haiku-5.5 — $0.10/$0.50 per 1M input/output tokens; response/failure log: app/llm.py:75, app/llm_log.py:98, app/storage.py:340; actual-usage cost: app/llm.py:99, app/pricing.py:129, app/llm_log.py:103; free path: app/talk_turns.py:165
[SENT: NOT LOGGED] [RECEIVED: LOGGED] [COST: LOGGED] [FREE FALLBACK] app/talk_turns.py:161 — OpenRouter/Anthropic summary, anthropic/claude-haiku-5.5 — $0.10/$0.50 per 1M input/output tokens; response/failure log: app/llm.py:75, app/llm_log.py:98, app/storage.py:340; actual-usage cost: app/llm.py:99, app/pricing.py:129, app/llm_log.py:103; free path: app/talk_turns.py:154
Gap: app/llm.py:87 sends requests, but the durable log is written only afterward from the finally block at app/llm.py:75; a process interruption can leave no sent record.
Gap: app/pricing.py:160 rounds each call to $0.0001 before app/llm_log.py:103 stores it; at Haiku 5.5 prices, charges below $0.00005 are recorded as zero.
```
