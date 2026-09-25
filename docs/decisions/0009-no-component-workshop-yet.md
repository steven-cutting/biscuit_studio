---
title: "Decision 0009: No component workshop yet"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_no_workshop]
requires: []
---

# Decision 0009: No component workshop yet

## Context

Every other Biscuit Games repository carries a component workshop. The hub's decision 0008
installed Storybook so that each shared component is seen in every state, and its decision
0009 publishes the workshop to Chromatic for visual review; the template renders both into
every game. Both are cited through [The platform upstream](../project/platform.md).

The workshop earns its cost where components are authored. The studio authors no shared
component: it mounts the platform's `HeaderBar` and `Wordmark`, wraps the wordmark in a
one-line `Lockup`, and composes pages from them. Its one interactive surface, the pose
studio, is a static file that no workshop would render.

## Decision

No component workshop in the first release. No Storybook, no Chromatic, no `stories/`
directory, no `.storybook/` configuration and no `CHROMATIC_PROJECT_TOKEN` secret. The gate
has three CI jobs — `frontend`, `documents` and `assets` — not the four a game has.

## Consequences

**No visual review of the site.** A change to how a page looks is seen by whoever runs
`just dev`, and by nothing automatic. The platform's components are reviewed in the hub's
workshop, so what is unreviewed is only how the studio arranges them.

**`tests/` is the whole evidence.** Testing Library suites under jsdom, querying by role
and name, are what prove a page renders what it should. They prove structure and
accessible names, not appearance.

**The hub's story-level accessibility checks do not run here.** The hub renders each story
in a real browser with axe over it. The studio's pages get no such pass, so accessibility
here rests on the platform's components, the tests and review; see
[Accessibility](../explanation/accessibility.md).

**A dependency set smaller than a game's.** No Playwright, no browser download on the
first run, and nothing that needs a secret.

## What would reopen this

The first component authored here. The three.js port of the viewer is the likely one: a
component with states worth seeing, which would bring the workshop and its review with it.
A page whose look needs review across the four combinations of theme and high contrast,
which the tests cannot give.

## Related pages

- [The platform upstream](../project/platform.md)
- [Testing](../reference/testing.md)
- [Quality gates](../reference/quality-gates.md)
- [Decision 0008: The viewer is embedded as-is](0008-the-viewer-is-embedded-as-is.md)
