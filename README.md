# lstack

Personal agent skills stack for engineering and productivity, modeled after [mattpocock/skills](https://github.com/mattpocock/skills).

Small, composable, Markdown-first skills that work across Antigravity, Claude Code, Codex, Gemini CLI, Cursor, and any Agent Skills-compatible harness.

## Installation

### Local Development (Symlink Hot-Reload)

Clone this repository and link active skills directly into `~/.gemini/config/skills`, `~/.claude/skills`, and `~/.agents/skills`:

```bash
git clone https://github.com/xdlkc/lstack.git
cd lstack
./scripts/link-skills.sh
```

Whenever you edit a `SKILL.md` or pull new commits (`git pull`), updates take effect immediately. Re-run `./scripts/link-skills.sh` after adding, renaming, or removing a skill.

### Install Across Harnesses

<details>
<summary><strong>Any Agent via skills.sh</strong> (Cursor, Windsurf, OpenCode, Claude Code, etc.)</summary>

```bash
npx skills@latest add xdlkc/lstack
```

To update later, run `npx skills@latest update`.

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

## Skills Reference

Skills split on who can invoke them:

- **User-invoked**: triggered explicitly by you (e.g. `/grill-me`), orchestrating top-level workflows.
- **Model-invoked**: triggered autonomously by the agent when appropriate or explicitly by you, holding reusable discipline.

### Engineering

| Skill | Invocation | Description |
| --- | --- | --- |
| **[code-review](./skills/engineering/code-review/SKILL.md)** | Model-invoked | Two-axis diff review checking coding standards and requirement/spec fidelity. |
| **[tdd](./skills/engineering/tdd/SKILL.md)** | Model-invoked | Red-green-refactor test-driven development loop, one vertical slice at a time. |

#### User-invoked

*(None yet)*

#### Model-invoked

- **[code-review](./skills/engineering/code-review/SKILL.md)**: Two-axis diff review checking coding standards and requirement/spec fidelity.
- **[tdd](./skills/engineering/tdd/SKILL.md)**: Red-green-refactor test-driven development loop, one vertical slice at a time.

### Productivity

| Skill | Invocation | Description |
| --- | --- | --- |
| **[grill-me](./skills/productivity/grill-me/SKILL.md)** | User-invoked | Get relentlessly interviewed about a plan or design until every branch of the design tree is resolved. |
| **[grilling](./skills/productivity/grilling/SKILL.md)** | Model-invoked | Reusable interview primitive to stress-test plans, designs, and requirements one branch at a time. |

#### User-invoked

- **[grill-me](./skills/productivity/grill-me/SKILL.md)**: Get relentlessly interviewed about a plan or design until every branch of the design tree is resolved.

#### Model-invoked

- **[grilling](./skills/productivity/grilling/SKILL.md)**: Reusable interview primitive to stress-test plans, designs, and requirements one branch at a time.

## Repository Structure

- `skills/engineering/`: Promoted engineering skills (shipped in plugin).
- `skills/productivity/`: Promoted productivity skills (shipped in plugin).
- `skills/in-progress/`: Experimental skills under iteration (linked locally, excluded from plugin).
- `skills/deprecated/`: Retired skills.
- `.claude-plugin/`: Plugin and marketplace manifests (`plugin.json`, `marketplace.json`).
- `scripts/link-skills.sh`: Local symlink installer for Antigravity, Claude Code, and Codex.
