#!/usr/bin/env python3
"""Antigravity Stop hook: prevent finishing a turn with bilingual README drift or broken doc links."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path


def allow() -> int:
    print(json.dumps({"decision": "allow"}))
    return 0


def load_verify_docs():
    candidates = [
        Path(__file__).resolve().parents[2]
        / "skills"
        / "engineering"
        / "docs-sync"
        / "scripts"
        / "verify_docs.py",
        Path.home() / ".agents" / "skills" / "docs-sync" / "scripts" / "verify_docs.py",
    ]
    for path in candidates:
        if path.is_file():
            spec = importlib.util.spec_from_file_location("lstack_verify_docs", path)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod
    return None


def find_candidate_repos(payload: dict) -> list[Path]:
    roots: list[Path] = []
    seen: set[Path] = set()

    raw_paths: list[str] = []
    if isinstance(payload.get("cwd"), str) and payload["cwd"]:
        raw_paths.append(payload["cwd"])
    if isinstance(payload.get("workspacePaths"), list):
        for p in payload["workspacePaths"]:
            if isinstance(p, str) and p:
                raw_paths.append(p)

    now = time.time()
    for raw in raw_paths:
        p = Path(raw).resolve()
        if not p.is_dir():
            continue

        top = subprocess.run(
            ["git", "-C", str(p), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
        )
        if top.returncode == 0 and top.stdout.strip():
            repo = Path(top.stdout.strip()).resolve()
            if repo not in seen:
                seen.add(repo)
                roots.append(repo)
            continue

        # Multi-repo workspace root (e.g. ~/Code): check only direct child repos
        # whose docs files were touched recently (within 15 minutes).
        for child in sorted(p.iterdir()):
            if not child.is_dir() or not (child / ".git").exists():
                continue
            recently_touched = False
            for doc_name in ("README.md", "README.zh-CN.md", "CHANGELOG.md"):
                doc = child / doc_name
                if doc.exists():
                    try:
                        if now - doc.stat().st_mtime <= 900:
                            recently_touched = True
                            break
                    except OSError:
                        pass
            if recently_touched:
                resolved = child.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    roots.append(resolved)

    return roots


def has_doc_changes(repo: Path) -> bool:
    status = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "status",
            "--porcelain",
            "--",
            "README.md",
            "README.zh-CN.md",
            "CHANGELOG.md",
        ],
        capture_output=True,
        text=True,
    )
    return status.returncode == 0 and bool(status.stdout.strip())


def run_check() -> int:
    raw = sys.stdin.read().strip()
    if not raw:
        return allow()

    payload = json.loads(raw)
    if not isinstance(payload, dict):
        return allow()

    if payload.get("terminationReason") != "NO_TOOL_CALL":
        return allow()
    if payload.get("continuationActive") is True:
        return allow()
    if payload.get("fullyIdle") is False:
        return allow()

    verify_mod = load_verify_docs()
    if verify_mod is None:
        return allow()

    all_errors: list[str] = []
    for repo in find_candidate_repos(payload):
        if not has_doc_changes(repo):
            continue
        errs = verify_mod.verify_repo(repo)
        for e in errs:
            all_errors.append(f"{repo.name}: {e}")

    if not all_errors:
        return allow()

    summary = "; ".join(all_errors[:6])
    if len(all_errors) > 6:
        summary += f" (+{len(all_errors) - 6} more)"

    print(
        json.dumps(
            {
                "decision": "continue",
                "reason": (
                    "[lstack-docs-governance] Documentation check failed on modified docs: "
                    f"{summary}. Fix these issues (update both README.md and README.zh-CN.md "
                    "and resolve link/format errors) before finishing."
                ),
            },
            ensure_ascii=False,
        )
    )
    return 0


def main() -> int:
    try:
        return run_check()
    except Exception:
        return allow()


if __name__ == "__main__":
    sys.exit(main())
