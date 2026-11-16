# Engineering

Daily skills for writing, testing, and reviewing code.

## User-invoked

Reachable only when explicitly invoked by the user (`disable-model-invocation: true` in `SKILL.md`; `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

*(None yet. Add top-level orchestration skills here as your workflow grows.)*

## Model-invoked

Reachable by the model autonomously or by the user explicitly.

- **[code-review](./code-review/SKILL.md)**: Two-axis diff review checking coding standards and requirement/spec fidelity.
- **[tdd](./tdd/SKILL.md)**: Red-green-refactor test-driven development loop, one vertical slice at a time.
