#!/usr/bin/env python3
"""Check version alignment across manifests, CHANGELOG state, and docs verification."""

from __future__ import annotations

import argparse
import importlib.util
import json
import plistlib
import re
import subprocess
import sys
from pathlib import Path


def load_verify_docs():
    verify_script = Path(__file__).resolve().parents[2] / "docs-sync" / "scripts" / "verify_docs.py"
    spec = importlib.util.spec_from_file_location("lstack_verify_docs", verify_script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load verify_docs.py from {verify_script}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def normalize_version(ver: str) -> str:
    return ver.strip().lstrip("vV")


def extract_toml_package_version(path: Path, sections: tuple[str, ...]) -> str | None:
    current_section = ""
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip()
            continue
        if current_section in sections:
            m = re.match(r'^version\s*=\s*["\']([^"\']+)["\']', line)
            if m:
                return m.group(1).strip()
    return None


def discover_versions(repo_dir: Path) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []

    cargo = repo_dir / "Cargo.toml"
    if cargo.is_file():
        ver = extract_toml_package_version(cargo, ("package", "workspace.package"))
        if ver:
            found.append(("Cargo.toml", ver))

    pkg = repo_dir / "package.json"
    if pkg.is_file():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            if isinstance(data.get("version"), str) and data["version"].strip():
                found.append(("package.json", data["version"].strip()))
        except Exception:
            pass

    pyproject = repo_dir / "pyproject.toml"
    if pyproject.is_file():
        ver = extract_toml_package_version(pyproject, ("project", "tool.poetry"))
        if ver:
            found.append(("pyproject.toml", ver))

    version_file = repo_dir / "VERSION"
    if version_file.is_file():
        lines = [ln.strip() for ln in version_file.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if lines:
            found.append(("VERSION", lines[0]))

    for plist_rel in ("Info.plist", "macos/Resources/Info.plist"):
        plist_path = repo_dir / plist_rel
        if plist_path.is_file():
            try:
                with plist_path.open("rb") as f:
                    plist = plistlib.load(f)
                ver = plist.get("CFBundleShortVersionString")
                if isinstance(ver, str) and ver.strip():
                    found.append((plist_rel, ver.strip()))
            except Exception:
                pass

    plugin_json = repo_dir / ".claude-plugin" / "plugin.json"
    if plugin_json.is_file():
        try:
            data = json.loads(plugin_json.read_text(encoding="utf-8"))
            if isinstance(data.get("version"), str) and data["version"].strip():
                found.append((".claude-plugin/plugin.json", data["version"].strip()))
        except Exception:
            pass

    return found


def inspect_git_tags(repo_dir: Path) -> tuple[str | None, int]:
    tag_proc = subprocess.run(
        ["git", "-C", str(repo_dir), "describe", "--tags", "--abbrev=0"],
        capture_output=True,
        text=True,
    )
    if tag_proc.returncode == 0 and tag_proc.stdout.strip():
        tag = tag_proc.stdout.strip()
        cnt_proc = subprocess.run(
            ["git", "-C", str(repo_dir), "rev-list", "--count", f"{tag}..HEAD"],
            capture_output=True,
            text=True,
        )
        cnt = int(cnt_proc.stdout.strip()) if cnt_proc.returncode == 0 and cnt_proc.stdout.strip().isdigit() else 0
        return tag, cnt

    all_cnt = subprocess.run(
        ["git", "-C", str(repo_dir), "rev-list", "--count", "HEAD"],
        capture_output=True,
        text=True,
    )
    cnt = int(all_cnt.stdout.strip()) if all_cnt.returncode == 0 and all_cnt.stdout.strip().isdigit() else 0
    return None, cnt


def inspect_changelog(repo_dir: Path, target_version: str | None) -> dict[str, object]:
    cl_path = repo_dir / "CHANGELOG.md"
    if not cl_path.is_file():
        return {"exists": False, "has_unreleased": False, "unreleased_items": 0, "has_target": False}

    text = cl_path.read_text(encoding="utf-8")
    has_unreleased = bool(re.search(r"(?m)^##\s+\[Unreleased\]", text, re.IGNORECASE))
    unreleased_items = 0
    unreleased_match = re.search(
        r"(?ms)^##\s+\[Unreleased\]\s*\n(.*?)(?=^##\s+\[|\Z)", text, re.IGNORECASE
    )
    if unreleased_match:
        unreleased_items = sum(
            1 for ln in unreleased_match.group(1).splitlines() if ln.strip().startswith(("-", "*"))
        )

    has_target = False
    if target_version:
        norm = re.escape(normalize_version(target_version))
        has_target = bool(re.search(rf"(?m)^##\s+\[v?{norm}\]", text))

    return {
        "exists": True,
        "has_unreleased": has_unreleased,
        "unreleased_items": unreleased_items,
        "has_target": has_target,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check repository release readiness.")
    parser.add_argument("repo_dir", nargs="?", default=".", help="Path to repository root")
    parser.add_argument("--target-version", help="Expected target version (e.g. 0.2.0 or v0.2.0)")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = parser.parse_args()

    repo_dir = Path(args.repo_dir).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    last_tag, commits_since = inspect_git_tags(repo_dir)
    versions = discover_versions(repo_dir)
    norm_versions = {normalize_version(v) for _, v in versions}

    if len(norm_versions) > 1:
        details = ", ".join(f"{src}={ver}" for src, ver in versions)
        errors.append(f"Version mismatch across manifests: {details}")

    target_norm = normalize_version(args.target_version) if args.target_version else None
    if target_norm:
        if versions and target_norm not in norm_versions:
            details = ", ".join(f"{src}={ver}" for src, ver in versions)
            errors.append(f"Target version {target_norm} does not match manifests ({details})")
        elif not versions:
            warnings.append("No version manifest found (Cargo.toml, package.json, VERSION, etc.)")

    cl_info = inspect_changelog(repo_dir, target_norm)
    if not cl_info["exists"]:
        warnings.append("CHANGELOG.md is missing (create one before or during release)")
    elif target_norm and not cl_info["has_target"] and cl_info["unreleased_items"] == 0:
        warnings.append(
            f"CHANGELOG.md has neither ## [{target_norm}] nor entries under ## [Unreleased]"
        )

    verify_mod = load_verify_docs()
    doc_errors = verify_mod.verify_repo(repo_dir)
    errors.extend(doc_errors)

    summary = {
        "repo": str(repo_dir),
        "last_tag": last_tag,
        "commits_since_tag": commits_since,
        "versions": [{"file": f, "version": v} for f, v in versions],
        "target_version": target_norm,
        "changelog": cl_info,
        "warnings": warnings,
        "errors": errors,
        "ready": not errors,
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"Repository : {repo_dir.name} ({repo_dir})")
        print(f"Last tag   : {last_tag or '(none)'} (+{commits_since} commits)")
        if versions:
            print("Manifests  : " + ", ".join(f"{f}={v}" for f, v in versions))
        else:
            print("Manifests  : (none detected)")
        if cl_info["exists"]:
            print(
                f"CHANGELOG  : present (unreleased bullets={cl_info['unreleased_items']}, "
                f"target section={'yes' if cl_info['has_target'] else 'no'})"
            )
        else:
            print("CHANGELOG  : missing")
        for w in warnings:
            print(f"WARN: {w}")
        for e in errors:
            print(f"ERR : {e}")
        print("Status     : " + ("READY" if not errors else "NOT READY"))

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
