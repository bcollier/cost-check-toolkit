---
name: cost-check
description: Reviews a project or a diff for every call that costs money (LLM and model APIs, text-to-speech, paid search or data APIs, paid hosting tiers) and reports whether each one has a free fallback and whether its cost is shown to the user. Reports only, never edits. Use before pushing a feature that calls an AI model or a paid API, or when asked what a project costs to run.
---
# Cost Check

## What to do
1. List the paid services the project calls. Start from the API keys the code reads (`os.environ`, `process.env`, config files), then find each place in the code that uses those keys or calls those services.
2. For each call, decide:
   - **Fallback:** is there a free path for the same feature (a free model, a free TTS voice, a local option), and does the code actually switch to it?
   - **Shown:** does the user see an estimated cost before spending, or is it silent?
3. If the `model_prices` tool is available, look up the current price of every LLM the code names. Do not quote prices from memory.
4. Do not fix anything. Report only.

## Output format
One line per paid call:

`[FREE FALLBACK | NO FALLBACK] [COST SHOWN | COST HIDDEN] file:line — service, model — price per 1M input/output tokens or "not an LLM"`

Then a short list: the three calls most likely to cost real money, cheapest fix first.

## Rules
- Cite a file and line for every call. No citation, no line in the report.
- A key that is defined but never used by the code is not a call. Leave it out.
- Judge what the code does, not what the README or comments say it does.
- Do not create, edit or delete any file.
