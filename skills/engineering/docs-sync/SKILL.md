---
name: docs-sync
description: >-
  Keep bilingual README.md, README.zh-CN.md, and CHANGELOG.md synchronized with
  code, CLI, configuration, and architectural changes. Use when modifying CLI
  commands or flags, network ports, config schemas, environment variables,
  dependencies, directory layouts, or user-visible behavior, or when creating or
  editing README.md, README.zh-CN.md, or CHANGELOG.md.
---

# Documentation & Changelog Sync

Keep repository documentation accurate, reader-first, and synchronized across languages whenever code or interfaces change.

## 1. Bilingual README Standard (`README.md` + `README.zh-CN.md`)

In repositories that maintain both `README.md` and `README.zh-CN.md` (or when setting up bilingual docs for a repository):

- **Language & Switcher**:
  - `README.md` is written in **English** (`< 5%` CJK outside literal brand names such as `言辞` / `眉批` / `栈架` / `余痕`). Place `English | [简体中文](./README.zh-CN.md)` immediately below the H1/hero header.
  - `README.zh-CN.md` is written in **Simplified Chinese** with full technical parity and proper full-width Chinese punctuation (`，。：；（）`) outside code spans. Place `[English](./README.md) | 简体中文` immediately below the H1/hero header.
- **Reader-First Structure**:
  1. One-line positioning + explicit non-goals or architectural boundaries.
  2. End-user Quick Start / Installation (most common path first).
  3. Core usage: shortcuts, CLI commands, ports, API endpoints, and configuration tables.
  4. Architecture / directory layout (linking only existing files).
  5. Developer build, test, and advanced setup (wrap long low-frequency recipes such as self-signed certificates inside `<details>`).
- **Factual Rigor**:
  - Verify every CLI subcommand, flag, default port, environment variable, path, and dependency version directly against source files before writing.
  - **No invented licenses**: Only include a `License` section or badge if a `LICENSE*`/`COPYING*` file or manifest `license` field (`Cargo.toml`, `package.json`, `pyproject.toml`, `.claude-plugin/plugin.json`) exists in the repository.
  - **No patch-note bloat**: Never append chronological versioned patch notes (`v0.7.2 fixed...`) to `README.md`; keep chronological release history in `CHANGELOG.md`.
- **Markdown & Render Safety**:
  - Escape literal dollar signs (`\$`) when two or more could appear in the same prose paragraph outside code spans.
  - In Mermaid blocks (`flowchart TD` / `flowchart LR`), quote node labels containing parentheses or colons and avoid HTML tags (`<br>`).
- **GitHub Metadata Check**: If a change materially shifts project scope or headline capabilities, note whether the GitHub repository About `description` / `topics` also need updating.

## 2. `CHANGELOG.md` Standard (Keep a Changelog + SemVer)

When `CHANGELOG.md` exists in the repository (or when adding one):

- Keep `## [Unreleased]` at the top with relevant subsections (`### Added`, `### Changed`, `### Fixed`, `### Removed`, `### Security`).
- Record only **user- or caller-observable changes** — never dump raw git commit messages or internal refactors with zero external effect.
- Prefix incompatible changes with `**Breaking**:` and include a concrete one-line migration step.
- Omit empty subsections rather than leaving blank headings.

## 3. Mandatory Verification

After editing any documentation file, run the verification script from this skill directory against the target repository root:

```bash
python3 ~/.agents/skills/docs-sync/scripts/verify_docs.py <repo-root>
```

If creating or refactoring a bilingual pair from scratch, enforce both files with `--strict-bilingual`:

```bash
python3 ~/.agents/skills/docs-sync/scripts/verify_docs.py <repo-root> --strict-bilingual
```

Fix every reported error (bilingual drift, missing switcher, broken relative links, CJK leakage in `README.md`, Mermaid HTML tags, multi-`$` collisions, or unbacked license claims) before concluding.
