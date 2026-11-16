# Counts recurring themes in my own quoted prompts (lines starting with ">") across earlier course prompt logs.
# Paths are machine-specific: point LOGS at your own copies. Usage: python3 notes/log_themes.py ["theme name" to list matches]
import re, sys, collections
LOGS = {
 "HW3 gAIm API Explorer": "/Users/jarvis/Code/gaim-api-explorer/PROMPTS.md",
 "HW4 Ignatius at Home": "/Users/jarvis/Code/ignatius-at-home-api/PROMPT_LOG.md",
 "HW6 Slide Finder": "/Users/jarvis/Code/slide-finder/prompt_log.md",
 "Project 2 Faculty Twin": "/Users/jarvis/Code/faculty-twin/prompt_log.md",
}
THEMES = {
 "cost / free mode": r"\b(cost|costs|free|money|cheap|cheaper|price|pricing|pay|paid|budget|spend|expensive|credits?)\b",
 "phone / iPhone": r"\b(iphone|phone|mobile|ipad)\b",
 "student privacy / names": r"(student names?|de-?identif|anonym|privacy|private|\bfaces?\b|passcode|ferpa)",
 "keys / secrets": r"\b(api key|key|keys|secret|secrets|\.env|token)\b",
 "test it / it's broken": r"(\btest|verify|doesn'?t work|not working|broken|\berror|\bbug|fails?\b|failing)",
 "screenshots / show me": r"(screenshot|screen shot)",
 "README / docs": r"\b(readme|documentation|docs)\b",
 "spec first": r"\bspec\b",
 "look / design": r"\b(beautiful|design|ugly|looks?|font|layout|style)\b",
 "deploy / push": r"\b(deploy|push|commit|merge|render|vercel|github pages)\b",
}
def prompts(path):
    blocks, cur = [], []
    for line in open(path, encoding="utf-8"):
        if line.startswith(">"):
            cur.append(line[1:].strip())
        elif cur:
            blocks.append(" ".join(cur).strip()); cur = []
    if cur: blocks.append(" ".join(cur).strip())
    seen, out = set(), []
    for b in blocks:
        if b and b not in seen: seen.add(b); out.append(b)
    return out
allp = {k: prompts(v) for k, v in LOGS.items()}
print("prompts (unique, quoted lines only):", {k: len(v) for k, v in allp.items()}, "total", sum(map(len, allp.values())))
print()
print(f"{'theme':28}" + "".join(f"{k.split()[0]:>10}" for k in LOGS) + f"{'total':>8}")
for t, rx in THEMES.items():
    r = re.compile(rx, re.I)
    counts = [sum(1 for p in allp[k] if r.search(p)) for k in LOGS]
    print(f"{t:28}" + "".join(f"{c:>10}" for c in counts) + f"{sum(counts):>8}")
if len(sys.argv) > 1:
    r = re.compile(THEMES[sys.argv[1]], re.I)
    for k in LOGS:
        for p in allp[k]:
            if r.search(p): print(f"[{k.split()[0]}] {p[:230]}")
