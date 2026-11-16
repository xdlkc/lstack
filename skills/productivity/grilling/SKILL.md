---
name: grilling
description: >-
  Interview the user relentlessly about a plan, design, or idea until every
  branch of the decision tree is resolved. Use when requirements are ambiguous,
  when starting a complex feature, or when another skill needs structured
  clarification before implementation.
---

# Grilling

Walk down every branch of the design or decision tree with the user before jumping to execution.

## Rules

1. **Ask one focused question at a time** (or a tight, small batch of closely related choices when using a structured question tool). Never dump a wall of 10 unrelated questions.
2. **Offer a recommended default** whenever a question has clear engineering trade-offs, explaining why in one short sentence.
3. **Explore the codebase first** for questions that code or config can already answer. Never ask the user about facts you can inspect directly.
4. **Follow dependencies**: resolve upstream architectural or product decisions before drilling into downstream implementation details.
5. **Track open branches** internally and confirm when every branch is resolved, then summarize the agreed decisions concisely before proceeding.
