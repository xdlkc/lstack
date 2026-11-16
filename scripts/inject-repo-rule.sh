#!/usr/bin/env bash
set -euo pipefail

# Upserts the lstack documentation & release governance block into AGENTS.md.
# Usage:
#   inject-repo-rule.sh <repo-dir> [<repo-dir> ...]
#   inject-repo-rule.sh --file <path/to/AGENTS.md>

REPO="$(cd "$(dirname "$0")/.." && pwd)"
RULE_SRC="$REPO/governance/rules/AGENTS.md"

if [ ! -f "$RULE_SRC" ]; then
  echo "error: missing rule source at $RULE_SRC" >&2
  exit 1
fi

if [ "$#" -eq 0 ]; then
  echo "Usage: $(basename "$0") <repo-dir> [...] | --file <AGENTS.md>" >&2
  exit 2
fi

upsert_file() {
  local target_file="$1"
  python3 - "$RULE_SRC" "$target_file" <<'PY'
import re
import sys
from pathlib import Path

rule_src = Path(sys.argv[1]).read_text(encoding="utf-8").strip()
target = Path(sys.argv[2])
target.parent.mkdir(parents=True, exist_ok=True)

begin = "<!-- BEGIN LSTACK DOCS GOVERNANCE -->"
end = "<!-- END LSTACK DOCS GOVERNANCE -->"
block = f"{begin}\n{rule_src}\n{end}"

existing = target.read_text(encoding="utf-8") if target.exists() else ""
pattern = re.compile(rf"{re.escape(begin)}.*?{re.escape(end)}", re.DOTALL)

if pattern.search(existing):
    updated = pattern.sub(lambda _: block, existing, count=1)
elif existing.strip():
    updated = existing.rstrip() + "\n\n" + block + "\n"
else:
    updated = block + "\n"

if not updated.endswith("\n"):
    updated += "\n"

target.write_text(updated, encoding="utf-8")
PY
  echo "updated governance block in $target_file"
}

if [ "$1" = "--file" ]; then
  if [ "$#" -ne 2 ]; then
    echo "error: --file requires exactly one path" >&2
    exit 2
  fi
  upsert_file "$2"
  exit 0
fi

for dir in "$@"; do
  if [ ! -d "$dir" ]; then
    echo "error: directory not found: $dir" >&2
    exit 1
  fi
  upsert_file "${dir%/}/AGENTS.md"
done
