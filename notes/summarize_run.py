"""Print the tool calls and final answer from a `claude -p --output-format stream-json` transcript.

Usage: python3 notes/summarize_run.py notes/runs/run1-doer.jsonl
"""
import json
import sys

for line in open(sys.argv[1], encoding="utf-8"):
    try:
        e = json.loads(line)
    except json.JSONDecodeError:
        continue
    if e.get("type") == "assistant":
        for c in e["message"]["content"]:
            if c["type"] == "tool_use":
                print(f"CALL  {c['name']}  {json.dumps(c['input'])[:220]}")
            elif c["type"] == "text" and c["text"].strip():
                print(f"SAYS  {c['text'].strip()[:220]}")
    elif e.get("type") == "user":
        for c in e["message"]["content"]:
            if isinstance(c, dict) and c.get("type") == "tool_result":
                body = c["content"] if isinstance(c["content"], str) else " ".join(x.get("text", "") for x in c["content"] if isinstance(x, dict))
                print(f"  ->  {body.strip()[:220]}")
    elif e.get("type") == "result":
        print(f"\nRESULT ({e.get('num_turns')} turns, ${e.get('total_cost_usd', 0):.2f} API-equivalent):\n{e.get('result', '')}")
