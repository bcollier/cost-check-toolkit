---
name: cost-check
description: Reviews a project or a diff for every call to a paid API (LLM and model APIs, text-to-speech, paid search or data APIs) and reports whether each call is logged when it is sent and when the response comes back, whether its cost is recorded for analytics, and whether it has a free fallback. Reports only, never edits. Use before pushing a feature that calls an AI model or a paid API, or when asked whether API usage and spend are being tracked.
---
# Cost Check

## What to do
1. List the paid services the project calls. Start from the API keys the code reads (`os.environ`, `process.env`, config files), then find each place in the code that uses those keys or calls those services.
2. For each call, decide:
   - **Sent:** is a log record written when the request goes out (service, model or endpoint, time, what it is for)?
   - **Received:** is the response logged, including failures and timeouts (status, duration, tokens or characters used)? Logging only successful responses is PARTIAL.
   - **Cost:** is this call's cost computed from the response's actual usage and stored where analytics can read it (a database table, a log file, a metrics service)? A price estimated before the call and never checked against usage is ESTIMATE ONLY.
   - **Fallback:** is there a free path for the same feature (a free model, a free TTS voice, a local option), and does the code actually switch to it?
3. If the `model_prices` tool is available, look up the current price of every LLM the code names, and compare it with the price the code uses to compute cost. Do not quote prices from memory.
4. Do not fix anything. Report only.

## Output format
One line per paid call, and nothing else before it:

`[SENT: LOGGED | NOT LOGGED] [RECEIVED: LOGGED | PARTIAL | NOT LOGGED] [COST: LOGGED | ESTIMATE ONLY | NOT LOGGED] [FREE FALLBACK | NO FALLBACK] file:line — service, model — price per 1M input/output tokens or "not an LLM"`

Then up to three gaps, most money at risk first, one line each. End there: no verdict, no summary, no headings, no advice on which model to use.

## Rules
- Cite a file and line for the call and for every log write or cost record you count. No citation means NOT LOGGED.
- When one wrapper logs every call that goes through it, cite the wrapper once and name it on each line.
- A key that is defined but never used by the code is not a call. Leave it out.
- Whether the user sees the cost is out of scope. Do not report it.
- Judge what the code does, not what the README or comments say it does.
- Do not create, edit or delete any file.
