# Changelog

All notable changes to `lstack` are documented in this file.

## [Unreleased]

## [0.2.0] - 2026-11-17

### Added
- `docs-sync` engineering skill (`skills/engineering/docs-sync/`) and `verify_docs.py` checker to enforce bilingual `README.md` / `README.zh-CN.md` parity, relative link validity, Mermaid/math safety, and license-claim accuracy.
- `cut-release` user-invoked engineering skill (`/cut-release`) and `check_release_ready.py` to align version manifests, roll `CHANGELOG.md`, and draft bilingual GitHub Release Notes.
- `governance/` Antigravity plugin bundle (`plugin.json`, `rules/AGENTS.md`, `hooks.json`, `hooks/stop-docs-check.py`) providing always-on global rules and a deterministic `Stop` hook against bilingual README drift.
- `scripts/inject-repo-rule.sh` helper to inject the managed governance rule block into isolated repository `AGENTS.md` files (such as headless Nexus workers).

### Changed
- Extended `code-review` (`skills/engineering/code-review/SKILL.md`) Axis 2 to check `README.md`, `README.zh-CN.md`, and `CHANGELOG.md` parity on user-visible diffs.
- Extended `scripts/link-skills.sh` to link `~/.gemini/config/plugins/lstack-docs-governance`, `~/.claude/rules/docs-discipline.md`, and managed `AGENTS.md` rule blocks in `~/.codex/` and `~/.kl/agent/`.

## [0.1.0] - 2026-11-16

### Added
- Initial `lstack` repository layout with `engineering/` (`code-review`, `tdd`) and `productivity/` (`grill-me`, `grilling`) skills.
- `.claude-plugin/` marketplace and plugin manifests plus `scripts/link-skills.sh` symlink installer.
