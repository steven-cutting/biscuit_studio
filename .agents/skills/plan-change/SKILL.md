---
name: plan-change
description: Plan a change when the scope, affected specifications, risks, or validation need evidence before any code is written.
---

# Plan a change

1. Read `AGENTS.md` and the specification modules the change touches. Separate what you read from what you are guessing.
2. Inspect the worktree before proposing anything, and preserve work you did not author.
3. Write down the observable outcome, and the explicit non-goals. A plan that does not say what it will not do cannot be reviewed for scope.
4. Identify whether the change moves a platform rule — the aesthetic, the character, a token, a guarantee. If it does, the hub changes first: plan the hub's page edit and decision record, and the entry in `docs/operations/hub-handover.md`, before any code here relies on the change. If the change moves an asset out of this repository, plan the `hub-handover` skill's entry alongside it.
5. Identify the boundaries crossed: a new side effect needs a port and a fake; a new surface needs its `@guarantee` clauses honoured; a new topic needs an owning documentation page.
6. Name the risks and the evidence that would settle them, and say which actions need authorization the agent does not already have.
7. Split into steps that can each be verified on their own, each pairing behaviour with its test and its documentation.
8. Present the plan with open questions marked as open. Confirm the plan runs green with `just check` before treating it as done.
