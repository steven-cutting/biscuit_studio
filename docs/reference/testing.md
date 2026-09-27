---
title: "Testing"
kind: "reference"
audience: [contributor, maintainer, agent]
canonical_for: [testing_reference]
requires: []
---

# Testing

What the suite is, where it lives, the rules a test here follows, what the coverage floor
measures, and what each file proves. How to run and debug it is
[Test and debug](../how-to/test-and-debug.md).

## Framework

Vitest in one configuration. The unit suite runs in jsdom with Testing Library,
`globals: true` so Testing Library registers its automatic cleanup hook, and one setup line
in `tests/setup.ts`. `vite.config.ts` names the one suite and holds its coverage block, and
all three test recipes pass `--config vite.config.ts` so they read the same.

There is no story run and no contrast test. Both live in the hub, where the components are
rendered in a workshop and the palette is declared and measured; this repository authors no
shared component, so it has no workshop to run stories in and no palette of its own to
measure. See [Decision 0009](../decisions/0009-no-component-workshop-yet.md).

## Layout

Tests live in `tests/`, never colocated with `src/`.

| File | What it is |
| --- | --- |
| `setup.ts` | The single import that registers the jest-dom matchers, reached through `setupFiles`. Not a test. |
| `brand.test.ts` | The three constants in `src/lib/brand.ts`. |
| `lockup.test.ts` | `Lockup.svelte`, the words and the silent mark. |
| `appearance.test.ts` | `src/lib/appearance.ts`, through the package's fake preferences port. |
| `route.test.ts` | The home page, `src/routes/+page.svelte`. |
| `pages.test.ts` | The model page and the gallery. |
| `fixtures/exif-gps.jpg` | A 1×1 JPEG carrying a GPS block: the image the asset checker's self-test must refuse. Read by `scripts/check_assets.py`, never by Vitest. |

| Suffix | Runner |
| --- | --- |
| `*.test.ts` | Vitest in jsdom. The `include` glob is `tests/**/*.test.ts`. |
| `*.spec.ts` | Reserved for a browser suite. None exists and no browser is installed. |

There is no `stories/` directory. Files are named for what they cover rather than mirroring a
source path: `pages.test.ts` covers two routes.

## Conventions

**Query by accessible role and name.** Never by class, never by test id. A query that fails
because a name is missing has found a real defect: it is the same information a screen
reader uses. The home page's links are found as
`getByRole('link', { name: 'The model' })`, the gallery's drawings as `figure` roles.

Text that is not a control is the stated exception, and the lockup's test is it. A lockup has
no role, so it is found by its text, and it takes two assertions: one that the mark is
`aria-hidden`, and one that the words read exactly `biscuit games / studio`. A text query
matches an element's own text nodes, so the words are found whether or not the mark beside
them is hidden; the mark's silence is a separate claim and takes a separate assertion.

**Inject fakes, never stub a global.** A side effect is reached through a port, and a test
hands in the fake. The appearance test passes `createFakePreferences` from the platform
package, changes its answers with `set()`, and asserts on an element it created with
`document.createElement('div')` — an element the test owns, not the document's root, and
nothing patched onto `window`. `applyAppearance` takes both as arguments so that this is
possible; code that read `matchMedia` or `document.documentElement` itself would need a stub,
and the stub is what the rule forbids.

**One assertion per claim.** Where a test holds two claims, it asserts each on its own line,
so a failure names the claim that broke. A test that only asserts a function was called is
not evidence that anything works.

## Coverage

v8 provider, measured over `src/lib/**/*.{ts,svelte}`, with a 90% floor on branches,
functions, lines and statements. Below the floor the run fails. The glob matches three files
today — `brand.ts`, `appearance.ts` and `components/Lockup.svelte` — and all three are at
100%. A file landing under `src/lib/` without a test is reported at zero and drags the figure
down.

`src/routes/` is outside the glob on purpose. It is where the document is reached and where
the pages are assembled, and the route tests render it without being counted. Anything worth
measuring moves to `src/lib/` and takes its element and its port as arguments.

`Lockup.svelte` has no if block and takes no prop, because a branch nothing renders would be
a branch the floor counts against the whole tree. Distinguish an untested branch from an
unreachable one: defensive code no input can reach should be deleted rather than covered;
see [Quality philosophy](../explanation/quality-philosophy.md).

Vitest 4's text reporter prints the per-file table empty; the figures are in
`coverage/coverage-summary.json`, which the `json-summary` reporter writes.

## What the current suite proves

| Suite | Covers |
| --- | --- |
| `brand.test.ts` | That the lockup word is in the platform's own lowercase and not blank, and that the title and description are not blank and the description is a sentence. |
| `lockup.test.ts` | That the lockup's accessible text is exactly `biscuit games / studio`, with the mark `aria-hidden`. |
| `appearance.test.ts` | `documentAttributes` clause by clause — animations on unless the device asks for less motion, high contrast off unless it asks for more — and `applyAppearance` writing both attributes on the element it is given, following the fake port's changes, and stopping once unsubscribed. |
| `route.test.ts` | The home page: one level-one heading reading the lockup, the document title, a main landmark, and the two links by name with their unprefixed hrefs. |
| `pages.test.ts` | The model page: the lockup as its only level-one heading, its section name as the level-two heading, the pose studio and the GLB linked by name under `/pose-studio/`, the Blender scene linked on GitHub, alt text on the preview naming the four poses, and the description naming the toe beans. The gallery: its section name, eleven captioned figures each with alt text, and the sentence saying the drawings were generated and have not left the studio. |

## The asset checker's own test

The asset checker is Python and has no pytest; it carries its own test instead.
`uv run --frozen python scripts/check_assets.py self-test` builds a temporary Git
repository with a blob, a hand-written LFS pointer and a clean PNG, and asserts that the
checker passes it; that it refuses the pointer's path once the index holds the file itself
and passes it once the index holds the pointer; that `source` passes in each of its three
forms and `unknown` is refused; that it refuses `tests/fixtures/exif-gps.jpg` naming `GPS`;
that a JPEG carrying only a capture date and a WebP carrying only a software tag are refused
naming `EXIF`; that a PNG carrying only its resolution and a clean WebP pass; that a TIFF is
refused; that the viewer's `source_sha256` and `patched` are checked for shape and against
the build record; and that one changed byte is refused.

`just check-assets` runs `check`, and `just assets-manifest` runs `write`; both run the
self-test before they read the real tree, so a checker that had stopped refusing anything
fails the gate on every run rather than passing everything quietly. [Asset manifest](asset-manifest.md) lists what it refuses.

## Related pages

- [Quality gates](quality-gates.md)
- [Test and debug](../how-to/test-and-debug.md)
- [Asset manifest](asset-manifest.md)
