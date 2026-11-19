# cost-check-toolkit

A checker skill (`cost-check`) and a one-tool MCP server (`model_prices`) for keeping track of what paid API calls cost.

## What the skill does and when it triggers

The skill finds every place in a project that calls a paid API: LLM calls to Anthropic, OpenRouter or OpenAI, and other paid services like ElevenLabs voices, xAI (Grok) and paid search. For each call it reports:

- whether the request is logged when it is sent
- whether the response is logged when it comes back, including failures
- whether the call's cost is recorded somewhere I can analyze later
- whether there is a free fallback (for example a free voice instead of ElevenLabs)
- the current price of the model, looked up with `model_prices`

It only reports. It never edits files, and it doesn't give advice on which model to use. Every line has to cite a file and line number, and anything it can't cite counts as not logged.

The agent loads it from the description in `skills/cost-check/SKILL.md`, which ends with: "Use before pushing a feature that calls an AI model or a paid API, or when asked whether API usage and spend are being tracked." In my runs I never named the skill. I just said "Check it for API costs before I push" and Codex picked it up. You can also call it directly with `/cost-check` in Claude Code or `$cost-check` in Codex.

## What the MCP tool does

`model_prices` looks up today's price for AI language models from OpenRouter's public model list (`https://openrouter.ai/api/v1/models`). You give it a few words like "claude haiku" or "gpt-6" and it returns the matching models, cheapest first, with input and output prices per million tokens and the context length. It only covers LLMs, not text-to-speech or search.

The agent decides to call it from the tool's docstring, which says to use it "whenever a cost matters" and "Do not answer prices from memory; they change often and your training data is stale." In both demo runs, Claude Code called it without being told to.

## Why: the friction, with quotes from my prompt logs

I dug through old prompts from prior assignments and did some clustering. The thing I asked about most was screenshots, and cost was second. I picked cost because it seemed simpler to implement.

My Ignatius at Home app (HW4) is a good example. I had premium voices from ElevenLabs, but it was much more affordable to use the free Microsoft text-to-speech for the free version. I kept asking for free versions, cost estimates and cost tracking, and the estimates were sometimes far off.

Details on the search through my old logs are in [notes/build-notes.md](notes/build-notes.md). Here are quotes from my past prompts.

HW4, Ignatius at Home, PROMPT_LOG.md:

- "can we do a free version with free microsoft tts or a low cost version as well?"
- "I want to be able to choose the model, and I want to show estimated costs for both the elevenlabs production and the model calls"
- "can we have a free mode where we use a model I have academic access to on Jetstream"
- "these should all have wrapping aroud them that safely drops them from the proces if we hit the c[redit limit]"
- "why only one research site, for the free version I assumed you would still use all four free search engines"
- "why does it say this retreat would cost 4.24 but it actually costed $21.13" (the estimate was five times too low)
- "default new retreats to opus 5.5, show estimated rates / cost when choosing the models"
- "How many minutes of content? Voices seem really expensive"

Project 2 (Faculty Twin):

- "I want it to run for free, would it fit in the free cloudflare budget?"
- "track tokens spent in / out etc. to estimate spend"

## Install

You need Python 3.10 or newer. The easiest way is the install script, which sets up both the skill and the MCP server for Claude Code and Codex:

```bash
git clone https://github.com/bcollier/cost-check-toolkit.git
cd cost-check-toolkit
bash install.sh
```

It's safe to run again, for example after a `git pull`. Then start a new Claude Code or Codex session and ask "What does Claude Haiku cost right now?" It should call `model_prices` instead of answering from memory.

If you'd rather do it by hand, the steps are below.

### The skill

Copy or symlink the `skills/cost-check` folder into the folder your agent reads skills from:

| Tool | Skill folder |
|---|---|
| Claude Code | `~/.claude/skills/cost-check/` |
| Codex | `~/.agents/skills/cost-check/` (Codex 0.157 also reads `~/.codex/skills/`) |

```bash
mkdir -p ~/.claude/skills ~/.agents/skills
ln -s "$PWD/skills/cost-check" ~/.claude/skills/cost-check
ln -s "$PWD/skills/cost-check" ~/.agents/skills/cost-check
```

Start a new session afterwards so the agent sees it.

### The MCP server (exact config; mark machine-specific paths)

**Machine-specific:** `/Users/bcollier/Code/cost-check-toolkit` below is where I cloned the repo. Replace it with the full path to your own clone. Use full paths, not `~` or relative paths.

1. Install the server's one dependency in its own virtual environment:

   ```bash
   cd /Users/bcollier/Code/cost-check-toolkit
   python3 -m venv .venv
   .venv/bin/pip install -r mcp-server/requirements.txt
   ```

2. Check that it works on its own. This should print three Haiku prices:

   ```bash
   .venv/bin/python -c "import sys; sys.path.insert(0,'mcp-server'); import model_prices_server as s; print(s.model_prices('claude haiku', 3))"
   ```

3. Register it with Claude Code:

   ```bash
   claude mcp add --scope user model-prices -- /Users/bcollier/Code/cost-check-toolkit/.venv/bin/python /Users/bcollier/Code/cost-check-toolkit/mcp-server/model_prices_server.py
   ```

4. Register it with Codex by adding this to `~/.codex/config.toml` (in the file, not the terminal):

   ```toml
   [mcp_servers.model-prices]
   command = "/Users/bcollier/Code/cost-check-toolkit/.venv/bin/python"
   args = ["/Users/bcollier/Code/cost-check-toolkit/mcp-server/model_prices_server.py"]
   ```

5. Check both: `claude mcp get model-prices` should say **✔ Connected**, and `codex mcp list` should show `model-prices` as **enabled**.

The tool is marked read-only (`readOnlyHint=True`). Without that, `codex exec` refused to call it, because it needs approval and can't ask for it.

## Tools confirmed

- **Codex CLI 0.157 (GPT-5.6):** loaded the skill from its description in all four checker runs and called `model_prices` (9 calls in Run 1). See [run1.md](notes/excerpts/run1.md), [run2.md](notes/excerpts/run2.md) and [iteration-v2.md](notes/excerpts/iteration-v2.md).
- **Codex Desktop:** loaded the skill from `~/.agents/skills` and called `model_prices` 17 times in a full review of Ignatius. See [run3.md](notes/excerpts/run3.md).
- **Claude Code (Opus 5.5):** called `model_prices` on its own in both doer runs. The skill is installed and listed there, but I used Codex as the checker.
- I installed it on a second computer with the steps above and `claude mcp get` showed it connected.

It does not work in the Claude app's chat, which searched the web instead because the server isn't in that app's own config, or in ChatGPT, which can't load local skills or a local MCP server.

## Borrowed or adapted

- **The skill** follows the structure of the `spec-check` example on the [HW8 assignment page](https://www.cs.cmu.edu/~113/hw8.html): a description that says what it does and when to use it, numbered steps, a fixed output format, and a Rules section. Two of my rules are adapted from it: "Cite a file and line… No citation means NOT LOGGED" (from "If you can't cite one, it isn't met") and "Judge what the code does, not what the README or comments say it does."
- **The MCP server** started from the MCP Python quickstart in the course and the MCP docs. The course example uses `FastMCP`, which was renamed `MCPServer` in mcp 2.x, so the server uses `from mcp.server.mcpserver import MCPServer` and pins `mcp>=2.3,<3`.
- **The Codex config block** follows the three-line example on the HW8 page.
- **The prices** come from OpenRouter's public model list.

What's mine: the idea of checking API costs, the send / receive / cost / fallback checks, the rules I learned the hard way building Ignatius, and the evidence from my own logs.

## How I used AI

I used Claude Code (Opus 5.5) to suggest project ideas, write all the code (the MCP server, the skill, `install.sh`, and the scripts in `notes/` that searched my old prompt logs), and run the doer sessions in the demonstration. Codex (GPT-5.6) ran the checker sessions, in a separate session on a different model. Codex Desktop ran Run 3 and wrote its excerpt and notes.

I picked cost as the topic, decided what the skill should check after the first runs (logging on send and receive, and costs recorded for analytics, not whether the user sees the cost), approved the demo tasks, and judged the checker's findings.

I wrote the first drafts of README.md, DEMONSTRATION.md and ITERATION.md. Claude Code checked them against the assignment and listed what was wrong or missing, and I told it to make those fixes. Much of the change was repairing markdown, such as putting my install script in a code block, or syncing text with design changes made after I wrote the drafts. For example, my skill description still described the first version's free-fallback check, which I dropped after the first runs. It also added the MCP server setup steps, the evidence under Tools confirmed, the borrowed sources and the run excerpts, and it rewrote this section. I wrote the answers on whether I agree with each checker finding in DEMONSTRATION.md.

Every prompt I gave is in [prompt_log.md](prompt_log.md), with what was done. The commits that Claude Code made carry a Co-Authored-By line. Build notes are in [notes/build-notes.md](notes/build-notes.md).
