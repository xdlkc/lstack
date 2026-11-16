---
name: code-review
description: >-
  Two-axis review of a git diff or recent changes: Standards (code quality,
  clarity, repo conventions) and Spec (fidelity to requirements and edge cases).
  Use before committing, opening a PR, or when the user asks for a code review.
---

# Code Review

Review the target diff independently across two axes so style feedback does not obscure functional gaps.

If your harness supports fresh-context subagents, dispatch two parallel reviewers (one for Standards, one for Spec) with a fresh context window so neither biases the other, then synthesize their findings. Otherwise, perform the two passes explicitly in sequence.

## Axis 1: Standards Review

Inspect the diff against the repository's rules (`AGENTS.md`, `CLAUDE.md`, linters) and engineering fundamentals:
- Duplicated logic that should share a helper
- Deep nesting or oversized functions that should be split
- Special-case `if/else` chains where a table or uniform path fits better
- Misleading names, dead code, or unguarded boundary conditions
- Unnecessary edits outside the scope of the task

## Axis 2: Spec & Correctness Review

Inspect the diff against the originating task, spec, or issue:
- Are all requested requirements actually implemented end-to-end?
- Are edge cases, error paths, and failure modes handled?
- Are tests verifying real behavior rather than tautological mocks?
- Did the change introduce regressions or break existing contracts?
- If the diff changes CLI commands/flags, ports, configuration, environment variables, or user-visible behavior, are `README.md`, `README.zh-CN.md` (in bilingual repos), and `CHANGELOG.md` (when present) updated in lockstep?

## Output Format

Report findings ordered by severity (**Blocker** -> **Major** -> **Minor** -> **Nit**), citing exact file paths and line numbers, with concrete fix suggestions. Only approve when no Blockers remain and verification commands have passed.
