---
name: cut-release
description: Prepare a versioned release, roll CHANGELOG.md, and generate bilingual Release Notes.
disable-model-invocation: true
---

# Cut Release

Prepare a clean, verified release with aligned version manifests, an updated `CHANGELOG.md`, synchronized bilingual READMEs, and bilingual GitHub Release Notes.

## Workflow

1. **Inspect Release Readiness & Real Diff**:
   - Run the readiness helper first (pass `--target-version X.Y.Z` if the target version is already chosen):
     ```bash
     python3 ~/.agents/skills/cut-release/scripts/check_release_ready.py <repo-root> [--target-version X.Y.Z]
     ```
   - Inspect `git log <last-tag>..HEAD --oneline` and `git diff <last-tag>..HEAD --stat` (plus key file diffs) to verify actual shipped behavior—never rely solely on commit titles.

2. **Align Version Manifests**:
   - Ensure every version file present in the repository (`Cargo.toml`, `package.json`, `pyproject.toml`, `VERSION`, `Info.plist` / `macos/Resources/Info.plist`, `.claude-plugin/plugin.json`) reflects the exact target version `X.Y.Z`.
   - Re-run any lockfile/manifest consistency checks required by the repository (e.g. `cargo check`, `npm test`, or plugin consistency scripts).

3. **Synchronize Bilingual READMEs**:
   - Call the Skill tool with `"docs-sync"` and verify `README.md` and `README.zh-CN.md` accurately reflect all user-facing CLI flags, ports, configuration keys, and installation changes introduced since `<last-tag>`.

4. **Roll `CHANGELOG.md`**:
   - Promote items from `## [Unreleased]` into `## [X.Y.Z] - YYYY-MM-DD` (Keep a Changelog format), keeping an empty `## [Unreleased]` heading at the top.
   - Group entries under `Added`, `Changed`, `Fixed`, `Removed`, and `Security`, prefixing incompatible changes with `**Breaking**:` and concrete migration steps.
   - Re-run:
     ```bash
     python3 ~/.agents/skills/docs-sync/scripts/verify_docs.py <repo-root>
     python3 ~/.agents/skills/cut-release/scripts/check_release_ready.py <repo-root> --target-version X.Y.Z
     ```

5. **Draft Bilingual GitHub Release Notes**:
   - Produce a ready-to-publish Release Notes body containing both English and Simplified Chinese:

     ```markdown
     ## Highlights
     - ...

     ## Breaking Changes & Migration
     - ... (omit section if none)

     ## Improvements & Fixes
     - ...

     ## Install & Verification
     - Download or build instructions + SHA-256 verification if applicable

     ---

     ## 核心亮点
     - ...

     ## 破坏性变更与迁移
     - ...（无则省略）

     ## 改进与修复
     - ...

     ## 安装与校验
     - 安装方式与校验命令
     ```

6. **Publish Only After Explicit Confirmation**:
   - Ask the user to confirm before creating tags (`git tag -a vX.Y.Z -m "vX.Y.Z"`), pushing tags, or creating a GitHub Release (`gh release create vX.Y.Z --draft --notes-file ...`).
   - If the repository automates releases via GitHub Actions (`.github/workflows/release.yml`), extract the release body directly from the `## [X.Y.Z]` section of `CHANGELOG.md` so repository history and GitHub Releases share a single source of truth.
