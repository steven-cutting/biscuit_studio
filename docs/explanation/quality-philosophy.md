---
title: "Quality philosophy"
kind: "explanation"
audience: [contributor, maintainer, agent]
canonical_for: [quality_philosophy]
requires: []
---

# Quality philosophy

Gates encode decisions, not taste. Each one exists because someone decided something, and
the gate is what stops the decision quietly reverting. If a gate cannot be traced back to a
decision, it should be deleted rather than tolerated.

## Checks are read-only

Every recipe under `just check` reports and never repairs. `bg-project-check`, the runner
behind `just check`, enforces this by snapshotting the worktree and comparing it after every
recipe, so a check that rewrites a file fails the run rather than hiding drift. Repair is
`just fix`, which is the aggregate rather than the only writer — `just format`, the two lock
recipes and `just assets-manifest` write as well; [Commands](../reference/commands.md) is
the list.

This is why the pre-commit configuration is split in two. `.pre-commit-config.yaml` is the
gate and is what gets installed; `.pre-commit-fix.yaml` holds the mutating hooks and runs
only from `just fix`.

## Fix the cause, not the report

A suppression is a last resort: one rule, one line, with a stated reason. Lowering the
coverage threshold, disabling a lint rule at a call site, or loosening an assertion until it
passes are all ways of deleting the signal while keeping the machinery.

Where a rule is genuinely wrong for a body of files, the fix is to configure it once, in the
config file, with a comment saying why. The studio's one standing example is the exclusion
set: the imported assets and the served viewer are skipped by every linter through one
pattern set, written in each tool's own configuration with the reason beside it, because
Blender's build scripts, a 26 MB page of inlined textures and a folder of PNG files were
never written to this repository's rules and are not edited by hand. That is a scope drawn
once, not a rule disabled where it fired. `eslint.config.js` turns no rule off or down, and
no file under `src/`, `tests/` or `scripts/` carries a suppression comment.

## Unreachable is not untested

Coverage distinguishes two things that look alike. A branch no input can reach is not a gap
in the tests; it is code that should not exist. `Lockup.svelte` holds no if block and takes
no prop for the same reason: a branch nothing renders is a branch the floor counts against
the whole tree. `applyAppearance` takes its element as an argument rather than reading
`document`, so the only arm that touches the real page sits in `src/routes/`, outside the
measured glob, and every arm inside it is reached by a test that hands it an element.

The corollary: do not chase the last few percent. The floor is 90, and the suite reports 100
over the three measured files today. That is what a small `src/lib/` produces; the floor is
90 rather than 100 so that the first branch the compiler emits and no input reaches is
removed or recorded, not covered by a contrived test.

## Tests inject, they do not stub

A fake is not a mock. It behaves — the fake preferences port answers what it was told and
reports a change when `set()` is called. Tests that assert a function was called are not
evidence that anything works.

Stubbing a global is banned outright. A side effect sits behind a port, and the test hands in
the fake: the appearance test passes the package's fake preferences port and an element it
created itself, and asserts on that element. Nothing is patched onto `window`, and no test
reaches `document.documentElement`. The rule is affordable because `applyAppearance` was
written to take both as arguments; code that reached for the global would need a stub, and
the stub is what the rule forbids.

## The hub is the arbiter

When a look or a rule is in question, the platform's specification and the hub's pages say
which answer stands, and neither the studio's code nor its tests are adjusted until they
agree with it. When the studio disagrees with the hub, the hub changes first, and nothing
here relies on the change until it has landed there.

The first worked example is the brand rule. The hub's design direction lists 3D rendering
and generated art under what to avoid, and the studio's model and drawings are both. The
studio does not argue the point in its own pages or ship around it; it waits on a hub
decision permitting renders from the approved model and vetted generated art, and records
the wait in [Hub handover](../operations/hub-handover.md).

## An asset is evidence too

A model file or a drawing is checked the way code is. Every file under `assets/` and
`static/pose-studio/` is listed in `assets/manifest.json` with its sha256 and its source,
and `just check-assets` proves the worktree agrees with it on every run. Before it checks
anything it runs its own self-test against a tree it builds, so a checker that had stopped
refusing a tampered byte or a GPS tag would fail the gate rather than pass everything.

Nothing under those two directories is edited by hand. An import or a rebuild goes through
its procedure, `just assets-manifest` is the one thing that writes the manifest, and the
manifest's diff is read before it is committed, because a rewritten manifest agrees with
whatever is in the worktree.

## Related pages

- [Quality gates](../reference/quality-gates.md)
- [Testing](../reference/testing.md)
- [Asset manifest](../reference/asset-manifest.md)
