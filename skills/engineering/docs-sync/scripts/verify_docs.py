#!/usr/bin/env python3
"""Verify bilingual README synchronization, relative links, Mermaid/math safety, and license backing."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ALLOWED_BRAND_CJK_RE = re.compile(
    r"(言辞|眉批|栈架|余痕|知了|毛选|奈克斯|简体中文|繁體中文|中文|毛泽东选集|实事求是|实践论|矛盾论)"
)
CJK_CHAR_RE = re.compile(r"[\u4e00-\u9fff]")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
MD_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_ATTR_RE = re.compile(r'(?:src|href)=["\']([^"\']+)["\']')
LICENSE_HEADING_RE = re.compile(r"^#{1,3}\s*(?:License|许可证|开源协议)\b", re.IGNORECASE | re.MULTILINE)
LICENSE_BADGE_RE = re.compile(r"img\.shields\.io/badge/license", re.IGNORECASE)


def check_relative_links(repo_dir: Path, filename: str, text: str) -> list[str]:
    errors: list[str] = []
    clean = INLINE_CODE_RE.sub("", FENCE_RE.sub("", text))

    candidates = [m.group(1) for m in MD_LINK_RE.finditer(clean)]
    candidates.extend(m.group(1) for m in HTML_ATTR_RE.finditer(clean))

    for target in candidates:
        if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
            continue
        rel = target.split("#", 1)[0].split("?", 1)[0]
        if not rel:
            continue
        if not (repo_dir / rel).exists():
            errors.append(f"{filename}: broken relative link -> {target}")
    return errors


def check_mermaid_and_dollars(filename: str, text: str) -> list[str]:
    errors: list[str] = []
    for m in re.finditer(r"```mermaid\r?\n(.*?)```", text, re.DOTALL):
        block = m.group(1)
        if re.search(r"<br\s*/?>|<[a-zA-Z][^>]*>", block):
            errors.append(f"{filename}: HTML tag inside mermaid block")

    no_code = INLINE_CODE_RE.sub("", FENCE_RE.sub("", text))
    for para in re.split(r"\r?\n\r?\n", no_code):
        cleaned = para.replace("\\$", "")
        if cleaned.count("$") >= 2:
            snippet = cleaned.strip().splitlines()[0][:60] if cleaned.strip() else ""
            errors.append(f"{filename}: >=2 unescaped '$' in paragraph ({snippet}...)")
    return errors


def cjk_ratio_in_english(text: str) -> tuple[int, int, float]:
    cleaned = INLINE_CODE_RE.sub("", FENCE_RE.sub("", text))
    cleaned = ALLOWED_BRAND_CJK_RE.sub("", cleaned)
    non_ws = re.sub(r"\s+", "", cleaned)
    total = len(non_ws)
    cjk_count = len(CJK_CHAR_RE.findall(non_ws))
    return cjk_count, total, (cjk_count / total if total else 0.0)


def has_license_backing(repo_dir: Path) -> bool:
    for item in repo_dir.iterdir():
        if item.is_file() and item.name.upper().startswith(("LICENSE", "COPYING")):
            return True

    pkg = repo_dir / "package.json"
    if pkg.is_file():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            if isinstance(data.get("license"), str) and data["license"].strip():
                return True
        except Exception:
            pass

    plugin_json = repo_dir / ".claude-plugin" / "plugin.json"
    if plugin_json.is_file():
        try:
            data = json.loads(plugin_json.read_text(encoding="utf-8"))
            if isinstance(data.get("license"), str) and data["license"].strip():
                return True
        except Exception:
            pass

    for manifest_name in ("Cargo.toml", "pyproject.toml"):
        manifest = repo_dir / manifest_name
        if manifest.is_file():
            content = manifest.read_text(encoding="utf-8", errors="ignore")
            if re.search(r'(?m)^\s*license(?:-file)?\s*=', content):
                return True

    return False


def check_bilingual_git_drift(repo_dir: Path) -> list[str]:
    if not (repo_dir / ".git").exists():
        check_git = subprocess.run(
            ["git", "-C", str(repo_dir), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
        )
        if check_git.returncode != 0:
            return []

    has_en_disk = (repo_dir / "README.md").exists()
    has_zh_disk = (repo_dir / "README.zh-CN.md").exists()

    tracked = subprocess.run(
        ["git", "-C", str(repo_dir), "ls-files", "--", "README.md", "README.zh-CN.md"],
        capture_output=True,
        text=True,
    )
    tracked_set = set(tracked.stdout.splitlines()) if tracked.returncode == 0 else set()

    both_exist = (has_en_disk or "README.md" in tracked_set) and (
        has_zh_disk or "README.zh-CN.md" in tracked_set
    )
    if not both_exist:
        return []

    status = subprocess.run(
        ["git", "-C", str(repo_dir), "status", "--porcelain", "--", "README.md", "README.zh-CN.md"],
        capture_output=True,
        text=True,
    )
    if status.returncode != 0:
        return []

    changed: set[str] = set()
    for line in status.stdout.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip().strip('"')
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip('"')
        if path in {"README.md", "README.zh-CN.md"}:
            changed.add(path)

    if len(changed) == 1:
        only_changed = next(iter(changed))
        other = "README.zh-CN.md" if only_changed == "README.md" else "README.md"
        return [f"Bilingual drift: {only_changed} has uncommitted changes while {other} was not updated"]
    return []


def verify_repo(
    repo_dir: Path,
    strict_bilingual: bool = False,
    allow_single_lang: bool = False,
) -> list[str]:
    errors: list[str] = []
    if not repo_dir.is_dir():
        return [f"Not a directory: {repo_dir}"]

    en_path = repo_dir / "README.md"
    zh_path = repo_dir / "README.zh-CN.md"
    changelog_path = repo_dir / "CHANGELOG.md"

    has_en = en_path.is_file()
    has_zh = zh_path.is_file()

    if strict_bilingual:
        if not has_en:
            errors.append("Missing README.md (--strict-bilingual)")
        if not has_zh:
            errors.append("Missing README.zh-CN.md (--strict-bilingual)")

    if not allow_single_lang:
        errors.extend(check_bilingual_git_drift(repo_dir))

    licensed = has_license_backing(repo_dir)

    if has_en:
        en_text = en_path.read_text(encoding="utf-8")
        errors.extend(check_relative_links(repo_dir, "README.md", en_text))
        errors.extend(check_mermaid_and_dollars("README.md", en_text))
        if has_zh:
            if "README.zh-CN.md" not in en_text:
                errors.append("README.md missing switcher link to README.zh-CN.md")
            cjk_cnt, total_cnt, ratio = cjk_ratio_in_english(en_text)
            if ratio >= 0.05:
                errors.append(
                    f"README.md CJK ratio too high ({cjk_cnt}/{total_cnt} = {ratio:.1%} >= 5%)"
                )
        if not licensed:
            stripped = FENCE_RE.sub("", en_text)
            if LICENSE_HEADING_RE.search(stripped) or LICENSE_BADGE_RE.search(stripped):
                errors.append("README.md claims a license without LICENSE file or manifest license field")

    if has_zh:
        zh_text = zh_path.read_text(encoding="utf-8")
        errors.extend(check_relative_links(repo_dir, "README.zh-CN.md", zh_text))
        errors.extend(check_mermaid_and_dollars("README.zh-CN.md", zh_text))
        if has_en and "README.md" not in zh_text:
            errors.append("README.zh-CN.md missing switcher link to README.md")
        zh_cjk = len(CJK_CHAR_RE.findall(zh_text))
        if zh_cjk < 50:
            errors.append(f"README.zh-CN.md has too few Chinese characters ({zh_cjk} < 50)")
        if not licensed:
            stripped = FENCE_RE.sub("", zh_text)
            if LICENSE_HEADING_RE.search(stripped) or LICENSE_BADGE_RE.search(stripped):
                errors.append("README.zh-CN.md claims a license without LICENSE file or manifest license field")

    if changelog_path.is_file():
        cl_text = changelog_path.read_text(encoding="utf-8")
        errors.extend(check_relative_links(repo_dir, "CHANGELOG.md", cl_text))
        errors.extend(check_mermaid_and_dollars("CHANGELOG.md", cl_text))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify bilingual README and CHANGELOG hygiene.")
    parser.add_argument("repo_dir", nargs="?", default=".", help="Path to repository root")
    parser.add_argument(
        "--strict-bilingual",
        action="store_true",
        help="Require both README.md and README.zh-CN.md to exist",
    )
    parser.add_argument(
        "--allow-single-lang",
        action="store_true",
        help="Skip bilingual git-drift check when intentionally editing only one language",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON result")
    args = parser.parse_args()

    repo_dir = Path(args.repo_dir).resolve()
    errors = verify_repo(
        repo_dir,
        strict_bilingual=args.strict_bilingual,
        allow_single_lang=args.allow_single_lang,
    )

    if args.json:
        print(json.dumps({"repo": str(repo_dir), "ok": not errors, "errors": errors}, ensure_ascii=False))
    elif errors:
        print(f"FAIL: {repo_dir.name} ({repo_dir})")
        for err in errors:
            print(f"  - {err}")
    else:
        print(f"OK: {repo_dir.name}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
