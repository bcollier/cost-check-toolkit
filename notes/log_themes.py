# Counts recurring themes in my own quoted prompts (lines starting with ">") across earlier course prompt logs.
# Paths are machine-specific: point LOGS at your own copies. Usage: python3 notes/log_themes.py ["theme name" to list matches]
import re, sys, collections
# (path, format, first line to read). Formats: "quote" = prompts in > blocks; "fence" = prompts in ``` blocks;
# "italic" = prompts written *"like this"* in a README. Phase 2 of HW7 starts at line 94; lines above it are the original author's.
LOGS = {
 "HW3 NHL Player Compare": ("/Users/jarvis/Code/nhl-player-compare/README.md", "italic", 1),
 "HW3 gAIm API Explorer": ("/Users/jarvis/Code/gaim-api-explorer/PROMPTS.md", "quote", 1),
 "HW4 Ignatius at Home": ("/Users/jarvis/Code/ignatius-at-home-api/PROMPT_LOG.md", "quote", 1),
 "HW6 Slide Finder": ("/Users/jarvis/Code/slide-finder/prompt_log.md", "quote", 1),
 "HW7 Mime Over Matter (phase 1)": ("/Users/jarvis/Code/mime-over-matter/prompt_log.md", "fence", 1),
 "HW7 Monday 8:55 (phase 2)": ("/Users/jarvis/Code/monday-855/prompt_log.md", "quote", 94),
 "Project 2 Faculty Twin": ("/Users/jarvis/Code/faculty-twin/prompt_log.md", "quote", 1),
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
 "log my prompts": r"(prompt[ _]?log|log (all|every|these|the)\b.*prompts?|log all)",
 "live link / play it on the web": r"(link to play|play it from web|on the web|in chrome|github pages|turn on pages|live site)",
 "stop and check with me": r"(check (back )?with me|stop for me|check it with me|ask me|before you (start|build))",
 "deploy / push": r"\b(deploy|push|commit|merge|render|vercel|github pages)\b",
}
def prompts(path, fmt, first):
    lines = open(path, encoding="utf-8").read().splitlines()[first - 1:]
    blocks, cur, in_fence = [], [], False
    if fmt == "italic":
        blocks = re.findall(r'\*"(.+?)"\*', "\n".join(lines), re.S)
    for line in lines if fmt != "italic" else []:
        if fmt == "fence":
            if line.startswith("```"):
                if in_fence:
                    blocks.append(" ".join(cur).strip()); cur = []
                in_fence = not in_fence
            elif in_fence:
                cur.append(line.strip())
        elif line.startswith(">"):
            cur.append(line[1:].strip())
        elif cur:
            blocks.append(" ".join(cur).strip()); cur = []
    if cur: blocks.append(" ".join(cur).strip())
    seen, out = set(), []
    for b in blocks:
        b = " ".join(b.split())
        if b and b not in seen: seen.add(b); out.append(b)
    return out
allp = {k: prompts(*v) for k, v in LOGS.items()}
print("prompts (unique, quoted lines only):", {k: len(v) for k, v in allp.items()}, "total", sum(map(len, allp.values())))
print()
short = {k: (k.split()[0] + ("p2" if "phase 2" in k else "p1" if "phase 1" in k else "b" if "gAIm" in k else "")) for k in LOGS}
print(f"{'theme':28}" + "".join(f"{short[k]:>9}" for k in LOGS) + f"{'total':>8}")
for t, rx in THEMES.items():
    r = re.compile(rx, re.I)
    counts = [sum(1 for p in allp[k] if r.search(p)) for k in LOGS]
    print(f"{t:28}" + "".join(f"{c:>9}" for c in counts) + f"{sum(counts):>8}")
if len(sys.argv) > 1:
    r = re.compile(THEMES[sys.argv[1]], re.I)
    for k in LOGS:
        for p in allp[k]:
            if r.search(p): print(f"[{short[k]}] {p[:230]}")
