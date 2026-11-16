# lstack Repository Guidelines

> Canonical source: [CLAUDE.md](./CLAUDE.md). Keep both files aligned if repo rules change.

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

- **User-invoked**: Set `disable-model-invocation: true` in `SKILL.md` frontmatter and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`.
- **Model-invoked**: Omit `disable-model-invocation` and `policy`, and include rich trigger conditions (`Use when...`) in `description`.

A user-invoked skill may invoke model-invoked skills (`Call the Skill tool with "<skill>"`), never another user-invoked skill.

## Local Symlink & Governance Sync

After adding, renaming, moving, or removing a skill or updating `governance/`, run `./scripts/link-skills.sh` to refresh:

- Skill symlinks in `~/.gemini/config/skills`, `~/.claude/skills`, and `~/.agents/skills`.
- Antigravity governance plugin at `~/.gemini/config/plugins/lstack-docs-governance` (`rules/AGENTS.md` + `hooks.json` `Stop` gate).
- Claude Code global rule at `~/.claude/rules/docs-discipline.md`.
- Managed rule blocks in `~/.codex/AGENTS.md` and `~/.kl/agent/AGENTS.md` (when installed).

For isolated headless workers running with separate `HOME` directories, run `./scripts/inject-repo-rule.sh /path/to/repo` to upsert the governance block into the repository's `AGENTS.md`.
