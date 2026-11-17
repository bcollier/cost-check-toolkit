#!/usr/bin/env bash
# Installs the cost-check skill and the model_prices MCP server for Claude Code and Codex.
# Run from a clone of this repo: bash install.sh. Safe to run again (e.g. after git pull).
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
SERVER="$REPO/mcp-server/model_prices_server.py"
VENV_PY="$REPO/.venv/bin/python"

PYTHON=""
for p in python3 python3.14 python3.13 python3.12 python3.11 python3.10; do
  if command -v "$p" >/dev/null && "$p" -c 'import sys; sys.exit(sys.version_info < (3, 10))'; then
    PYTHON="$p"; break
  fi
done
[ -n "$PYTHON" ] || { echo "Python 3.10 or newer is required (python3 is $(python3 --version 2>&1))." >&2; exit 1; }

# Skill: ~/.agents/skills is read by Codex, ~/.claude/skills by Claude Code.
# Symlinks to this clone, so a git pull updates the skill too.
mkdir -p ~/.agents/skills ~/.claude/skills
for dir in ~/.agents/skills ~/.claude/skills; do
  rm -rf "$dir/cost-check"
  ln -s "$REPO/skills/cost-check" "$dir/cost-check"
done
echo "Skill linked into ~/.agents/skills and ~/.claude/skills"

# MCP server: its own virtualenv, checked before it is registered.
[ -x "$VENV_PY" ] || "$PYTHON" -m venv "$REPO/.venv"
"$VENV_PY" -m pip install -q -r "$REPO/mcp-server/requirements.txt"
"$VENV_PY" -c "import sys; sys.path.insert(0, '$REPO/mcp-server'); import model_prices_server as s; print(s.model_prices('claude haiku', 1))"

if command -v claude >/dev/null; then
  claude mcp remove model-prices --scope user >/dev/null 2>&1 || true
  claude mcp add --scope user model-prices -- "$VENV_PY" "$SERVER"
else
  echo "Claude Code not found; skipped registering the server with it."
fi

if command -v codex >/dev/null; then
  codex mcp remove model-prices >/dev/null 2>&1 || true
  codex mcp add model-prices -- "$VENV_PY" "$SERVER"
else
  echo "Codex not found; skipped registering the server with it."
fi

echo "Done. Start a new Claude Code or Codex session and ask: What does Claude Haiku cost right now?"
