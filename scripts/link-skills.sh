#!/usr/bin/env bash
set -euo pipefail

# Links all active skills and documentation governance rules/hooks in this repository
# into local agent harness directories:
#   - ~/.gemini/config/skills & ~/.gemini/config/plugins/lstack-docs-governance: Antigravity
#   - ~/.claude/skills & ~/.claude/rules/docs-discipline.md: Claude Code
#   - ~/.agents/skills: Codex and other Agent Skills-compatible harnesses
#   - ~/.codex/AGENTS.md & ~/.kl/agent/AGENTS.md: managed governance rule block

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=(
  "$HOME/.gemini/config/skills"
  "$HOME/.claude/skills"
  "$HOME/.agents/skills"
)

names=()
srcs=()
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  names+=("$(basename "$src")")
  srcs+=("$src")
done < <(find "$REPO/skills" -name SKILL.md -not -path '*/node_modules/*' -not -path '*/deprecated/*' -not -path '*/misc/*' -print0)

for DEST in "${DESTS[@]}"; do
  # If $DEST is a symlink that resolves into this repo, we would end up writing
  # per-skill symlinks back into the repo's own skills/ tree. Detect and bail
  # out instead of polluting the working copy.
  if [ -L "$DEST" ]; then
    resolved="$(readlink -f "$DEST")"
    case "$resolved" in
      "$REPO"|"$REPO"/*)
        echo "error: $DEST is a symlink into this repo ($resolved)." >&2
        echo "Remove it (rm \"$DEST\") and re-run; the script will recreate it as a real dir." >&2
        exit 1
        ;;
    esac
  fi

  mkdir -p "$DEST"

  for i in "${!names[@]}"; do
    name="${names[$i]}"
    src="${srcs[$i]}"
    target="$DEST/$name"

    if [ -e "$target" ] && [ ! -L "$target" ]; then
      rm -rf "$target"
    fi

    ln -sfn "$src" "$target"
    echo "linked $name -> $src ($DEST)"
  done
done

# Link Antigravity governance plugin (global rule + Stop hook)
AGY_PLUGIN_DIR="$HOME/.gemini/config/plugins"
mkdir -p "$AGY_PLUGIN_DIR"
ln -sfn "$REPO/governance" "$AGY_PLUGIN_DIR/lstack-docs-governance"
echo "linked lstack-docs-governance -> $REPO/governance ($AGY_PLUGIN_DIR)"

# Link Claude Code global rule
CLAUDE_RULES_DIR="$HOME/.claude/rules"
mkdir -p "$CLAUDE_RULES_DIR"
ln -sfn "$REPO/governance/rules/AGENTS.md" "$CLAUDE_RULES_DIR/docs-discipline.md"
echo "linked docs-discipline.md -> $REPO/governance/rules/AGENTS.md ($CLAUDE_RULES_DIR)"

# Upsert managed rule block into Codex and kl global AGENTS.md when installed
if [ -d "$HOME/.codex" ]; then
  "$REPO/scripts/inject-repo-rule.sh" --file "$HOME/.codex/AGENTS.md"
fi

if [ -d "$HOME/.kl" ]; then
  "$REPO/scripts/inject-repo-rule.sh" --file "$HOME/.kl/agent/AGENTS.md"
fi
