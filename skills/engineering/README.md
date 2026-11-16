# Engineering

Daily skills for writing, testing, and reviewing code.

## User-invoked

Reachable only when explicitly invoked by the user (`disable-model-invocation: true` in `SKILL.md`; `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[cut-release](./cut-release/SKILL.md)**: Prepare a versioned release, roll `CHANGELOG.md`, and draft bilingual Release Notes.

## Model-invoked

Reachable by the model autonomously or by the user explicitly.

- **[code-review](./code-review/SKILL.md)**: Two-axis diff review checking coding standards, documentation/changelog parity, and requirement/spec fidelity.
- **[docs-sync](./docs-sync/SKILL.md)**: Keep bilingual `README.md`, `README.zh-CN.md`, and `CHANGELOG.md` synchronized with code, CLI, and config changes.
- **[tdd](./tdd/SKILL.md)**: Red-green-refactor test-driven development loop, one vertical slice at a time.
