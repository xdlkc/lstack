# Productivity

General workflow tools, not code-specific.

## User-invoked

Reachable only when explicitly invoked by the user (`disable-model-invocation: true` in `SKILL.md`; `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[grill-me](./grill-me/SKILL.md)**: Get relentlessly interviewed about a plan or design until every branch of the design tree is resolved.

## Model-invoked

Reachable by the model autonomously or by the user explicitly.

- **[grilling](./grilling/SKILL.md)**: Reusable interview primitive to stress-test plans, designs, and requirements one branch at a time.
