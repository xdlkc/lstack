# lstack

English | [简体中文](./README.zh-CN.md)

Personal agent skills stack for engineering and productivity, modeled after [mattpocock/skills](https://github.com/mattpocock/skills).

Small, composable, Markdown-first skills designed to work across Antigravity, Claude Code, Codex, Gemini CLI, Cursor, and other Agent Skills-compatible harnesses.

## Installation

### Local Development (Symlink Hot-Reload)

Clone this repository and link active skills directly into `~/.gemini/config/skills`, `~/.claude/skills`, and `~/.agents/skills`:

```bash
git clone https://github.com/xdlkc/lstack.git
cd lstack
./scripts/link-skills.sh
```

[`scripts/link-skills.sh`](./scripts/link-skills.sh) scans `skills/` for `SKILL.md` files (excluding `deprecated/`, `misc/`, and `node_modules/`), validates that none of the destination directories are symlinks pointing back into the repository, and creates per-skill symlinks. Edits to any `SKILL.md` or `git pull` take effect immediately; re-run `./scripts/link-skills.sh` after adding, renaming, moving, or retiring a skill.

### Install Across Harnesses

<details>
<summary><strong>Any Agent via skills.sh</strong> (Cursor, Windsurf, OpenCode, Claude Code, etc.)</summary>

```bash
npx skills@latest add xdlkc/lstack
```

To update later:

```bash
npx skills@latest update
```

</details>

<details>
<summary><strong>Claude Code</strong> (plugin marketplace)</summary>

```bash
claude plugin marketplace add xdlkc/lstack
claude plugin install lstack@xdlkc
```

</details>

<details>
<summary><strong>Codex</strong> (plugin marketplace)</summary>

```bash
codex plugin marketplace add xdlkc/lstack
codex plugin add lstack@xdlkc
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

```bash
gemini skills install https://github.com/xdlkc/lstack.git --path skills/engineering
gemini skills install https://github.com/xdlkc/lstack.git --path skills/productivity
```

</details>

<details>
<summary><strong>Antigravity</strong></summary>

Run `./scripts/link-skills.sh` from a local clone to symlink active skills into `~/.gemini/config/skills`.

</details>

## Skills Reference

Skills split by how they are invoked:

- **User-invoked**: Triggered explicitly by the user (e.g. `/grill-me`), orchestrating top-level workflows. Marked with `disable-model-invocation: true` in `SKILL.md` and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. User-invoked skills may call model-invoked skills, never another user-invoked skill.
- **Model-invoked**: Triggered autonomously by the agent via `Use when...` description conditions, or explicitly by the user, holding reusable discipline.

### Engineering

| Skill | Invocation | Description |
| --- | --- | --- |
| **[code-review](./skills/engineering/code-review/SKILL.md)** | `Model-invoked` | Two-axis diff review checking coding standards (`AGENTS.md`, `CLAUDE.md`, structure) and spec/correctness fidelity, ordered by severity. |
| **[tdd](./skills/engineering/tdd/SKILL.md)** | `Model-invoked` | Red-green-refactor test-driven development loop, building one vertical slice through public seams at a time. |

### Productivity

| Skill | Invocation | Description |
| --- | --- | --- |
| **[grill-me](./skills/productivity/grill-me/SKILL.md)** | `User-invoked` | Top-level interview workflow that calls `grilling` and blocks code edits until every branch of the plan or design is resolved and confirmed. |
| **[grilling](./skills/productivity/grilling/SKILL.md)** | `Model-invoked` | Reusable interview primitive to stress-test plans, designs, and requirements one dependency-ordered branch at a time. |

## Promotion Lifecycle

Skills progress through buckets under `skills/`:

1. **`skills/in-progress/`** ([notes](./skills/in-progress/README.md)) — Experimental beta skills under active iteration. Symlinked locally by `./scripts/link-skills.sh` for daily testing, but excluded from top-level `README.md` and `.claude-plugin/plugin.json`.
2. **`skills/engineering/` & `skills/productivity/`** — Promoted daily skills shipped in [`.claude-plugin/plugin.json`](./.claude-plugin/plugin.json). Each promoted skill stays synchronized across top-level `README.md`, its bucket README ([`skills/engineering/README.md`](./skills/engineering/README.md) or [`skills/productivity/README.md`](./skills/productivity/README.md)), and `.claude-plugin/plugin.json`.
3. **`skills/deprecated/`** — Retired skills (created when needed). Never symlinked locally and excluded from top-level documentation and plugin manifests.

## Repository Structure

```text
.
├── .claude-plugin/
│   ├── marketplace.json        # Marketplace catalog entry (xdlkc)
│   └── plugin.json             # Plugin manifest & promoted skills list
├── scripts/
│   └── link-skills.sh          # Local symlink installer (Antigravity, Claude Code, Codex)
├── skills/
│   ├── engineering/            # Promoted engineering skills (code-review, tdd)
│   ├── productivity/           # Promoted productivity skills (grill-me, grilling)
│   └── in-progress/            # Experimental skills (excluded from plugin manifest)
├── AGENTS.md                   # Repository conventions
├── CLAUDE.md                   # Canonical authoring & sync rules
├── README.md
└── README.zh-CN.md
```

## License

MIT (as declared in [`.claude-plugin/plugin.json`](./.claude-plugin/plugin.json)).
