# lstack Repository Guidelines

This repository stores personal agent skills modeled after `mattpocock/skills`.

## Bucket Organization

Skills live in bucket folders under `skills/`:

- `engineering/`: Daily coding, testing, and review skills (promoted).
- `productivity/`: Daily non-code workflow and thinking skills (promoted).
- `in-progress/`: Experimental beta skills. Linked locally, but excluded from `README.md` and `.claude-plugin/plugin.json`.
- `deprecated/`: Retired skills. Never linked locally and excluded from `README.md` and `.claude-plugin/plugin.json`.

## Sync Rules for Promoted Skills

Every skill in `engineering/` or `productivity/` must stay in sync across:

1. Top-level `README.md` (linked to `./skills/<bucket>/<name>/SKILL.md`, grouped into **User-invoked** and **Model-invoked**).
2. Bucket `skills/<bucket>/README.md` (linked to `./<name>/SKILL.md`, grouped into **User-invoked** and **Model-invoked**).
3. `.claude-plugin/plugin.json` `skills` array (`"./skills/<bucket>/<name>"`).

Skills in `in-progress/` and `deprecated/` must not appear in top-level `README.md` or `.claude-plugin/plugin.json`.

## User-invoked vs Model-invoked Convention

Every `SKILL.md` falls into one of two invocation categories, and `agents/openai.yaml` beside `SKILL.md` must match:

- **User-invoked**: Reachable only when explicitly triggered by the user.
  - Set `disable-model-invocation: true` in `SKILL.md` frontmatter.
  - Set `policy:\n  allow_implicit_invocation: false` in `agents/openai.yaml`.
  - Keep `description` to a concise one-line human-facing summary.
- **Model-invoked**: Reachable autonomously by the model or explicitly by the user.
  - Omit `disable-model-invocation` and omit `policy` from `agents/openai.yaml`.
  - Write `description` with clear trigger phrasing (`Use when...`) so the model knows when to activate it.

A user-invoked skill may invoke model-invoked skills (e.g. `Call the Skill tool with "grilling"`), but no skill should invoke a user-invoked skill.

## Local Symlink Sync

After adding, renaming, moving, or removing a skill, run:

```bash
./scripts/link-skills.sh
```

This updates symlinks in `~/.gemini/config/skills`, `~/.claude/skills`, and `~/.agents/skills` for every skill outside `deprecated/` and `misc/`.

## Validation

After editing `.claude-plugin/plugin.json` or `.claude-plugin/marketplace.json`, verify valid JSON and check manifests (e.g. `claude plugin validate .` if Claude CLI is installed).
