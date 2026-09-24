---
name: code-review
description: Review a change in this repository against its invariants, specifications, tests, and documentation contract.
---

# Review a change

1. Read `AGENTS.md` and the specification module the change touches. Review the whole diff, not the summary of it.
2. Check the invariants in `AGENTS.md` one at a time. The hub decides shared behaviour and changes first, runes only, side effects behind a port with `document` reached only in `onMount` under `src/routes/`, exact version pins, no assumed server, colour never alone, the coverage floor intact, and every asset listed in `assets/manifest.json` with nothing under `assets/` or `static/pose-studio/` edited by hand.
3. Check the change against the platform's specifications, which arrive with the package under `node_modules/@steven-cutting/biscuit-games/specs/`. A rule, guard or threshold decided in code here that the platform states differently is a finding even when the behaviour looks right.
4. Check the test evidence. A test that only asserts a function was called is not evidence; a component test that queries by class or test id rather than by accessible role is not evidence either.
5. Check the boundaries. Nothing under `src/lib/` may touch a browser global, and no test may stub one; `+layout.svelte`'s `onMount` is the recorded exception, and it hands `document.documentElement` to a function that takes it as an argument.
6. Check documentation ownership. A durable fact belongs on the page that owns its topic in `docs/manifest.yml`, added there rather than restated.
7. Check scope. Unrelated refactors, new dependencies and speculative abstractions are findings in themselves.
8. Check the boundary. A fact about the platform belongs in the hub, not here; a change that moves an asset out of this repository runs the `hub-handover` skill; a change under `assets/` or `static/pose-studio/` arrives with a manifest diff whose `source` fields say where the bytes came from.
9. Report findings by severity with `file:line`, what breaks, and the smallest fix. Run `just check` before concluding.
