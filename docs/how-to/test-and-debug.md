---
title: "Test and debug"
kind: "how-to"
audience: [contributor, maintainer, agent]
canonical_for: [test_workflow]
requires: []
---

# Test and debug

## Run the suites

```console
just frontend-unit        # Vitest, once
just frontend-coverage    # Vitest with the coverage floor enforced
just frontend-static      # ESLint, Prettier check, svelte-check
just check-assets         # the asset manifest, after the checker's own self-test
```

To iterate on one file, watch it:

```console
just frontend-watch tests/appearance.test.ts
```

`just frontend-watch` with no argument watches every suite. It never exits, which is why it
is not part of `just check`.

Framework configuration and conventions are described in
[Testing](../reference/testing.md); this page is about narrowing down a failure.

## Narrow down a failing test

1. Run the single file first. A failure that only appears in the whole suite is usually
   shared state, and there is very little of it here — every test builds its own fake
   preferences port and its own element.
2. If a component assertion fails, read the DOM that Testing Library prints. It shows the
   accessible names, which is what the queries match on.
3. If the expectation is about how a surface should look or behave, the hub's page that
   owns the behaviour is the arbiter; see [The platform upstream](../project/platform.md).
   The studio adds no rule of its own, so the current code is never the arbiter.
4. Do not weaken an assertion to make it pass. If the platform's rule is wrong, it is
   changed in the hub first and arrives here as a version of the package.

## Debug a coverage failure

`just frontend-coverage` prints the totals and fails below 90% on any of the four figures.
Vitest's text reporter prints the per-file table empty; the per-file figures are in
`coverage/coverage-summary.json`, which the same run writes.

The measured surface is small: `src/lib/brand.ts`, `src/lib/appearance.ts` and
`src/lib/components/Lockup.svelte` are the whole of it. Everything under `src/routes/` is
outside the glob, which is why route-only code lives there and nothing else does. Two
cases look alike and are not:

- **Untested behaviour.** Add the test. This is the common case.
- **Unreachable code.** A defensive branch no input can reach, or a Svelte-compiled
  update branch for a value that never changes. Remove the branch rather than inventing
  a test that reaches it artificially.

Never lower the threshold in `vite.config.ts`.

## Debug an asset failure

`just check-assets` prints one line per finding, as `<path>: <reason>`, and a count. A
file that is present but not listed, or whose sha256 differs, means something under
`assets/` or `static/pose-studio/` changed without `just assets-manifest`; decide whether
the change was meant before running it, and read the manifest diff after. A refusal naming
an EXIF tag means an image carries metadata beyond its resolution, which is stripped at
the source, never waved through. Never edit the manifest by hand to make it agree. See
[Import an asset](import-an-asset.md).

## Debug a browser problem

There is no server, so the browser and the build output are the whole system.

```console
BASE_PATH=/biscuit_studio just frontend-build
BASE_PATH=/biscuit_studio just preview
```

The base path goes on both commands, so the preview sits where Pages serves. See
[Configuration](../reference/configuration.md).

If something works under `just dev` but not under `just preview`, suspect prerendering:
module-scope work runs once at build time, and anything per-visitor must happen in the
browser.

The pose studio is different. It is a static file, not part of the SvelteKit app:
`just dev` serves it at `/pose-studio/viewer.html`, exactly as the build copies it. It
needs WebGL 2, and says so on the page when the browser cannot start it. It reads the
reduced-motion preference itself, not through the platform's attribute. A problem inside
it is debugged against the model's own sources under `assets/models/biscuit/src/` —
`viewer.template.html`, `pose_viewer.js` and `pose_math.js`, which `viewer.py` assembles
into the page — and fixed by a rebuild, as [Rebuild the model](rebuild-the-model.md)
describes, never by editing the served file and never against anything under `src/`.

## Related pages

- [Testing](../reference/testing.md)
- [Quality gates](../reference/quality-gates.md)
- [Rebuild the model](rebuild-the-model.md)
- [Troubleshooting](../operations/troubleshooting.md)
