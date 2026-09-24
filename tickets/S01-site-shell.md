---
id: S01
title: "Site shell: the platform package, the lockup, and appearance on the document element"
status: open
depends_on: [S00]
parallel_with: [S02, S03, S04, S05, S06]
branch: ticket/s01-site-shell
estimated_size: L
---

# S01: Site shell: the platform package, the lockup, and appearance on the document element

## Context

S00 left this repository with `just check` green over an empty site: `package.json`
already installs `@steven-cutting/biscuit-games` at `1.1.0` (CONVENTIONS.md §2.3),
`src/lib/brand.ts` already names the studio (§2.6), and `src/routes/+page.svelte` is a
placeholder with one `<main>` and a sentence. This ticket makes the site wear the platform:
the stylesheet imported once at the root layout, the platform's `HeaderBar` carrying this
repository's lockup as the page's only `h1`, and the two device-dependent appearance
attributes written on `<html>` through the port the package exports — which is what a game
is told to do (H `docs/how-to/consume-the-hub.md` sections 3 to 5) and what the hub's own
route does not yet do (H `src/app.html` lines 2-28 say so and why).

Read first, at the commits CONVENTIONS.md §0 pins (read-only):

- CONVENTIONS.md §1 decision 3, §2 (the rows marked S01), §2.6, §2.7, §9, §10.
- H `/Users/scutting/projects/biscuit_games/src/lib/components/HeaderBar.svelte` lines
  34-42: the props — `brand?: Snippet`, `chip`, `actions` — and lines 44-50, where the
  `brand` snippet is rendered inside `<h1 class="brand">`.
- H `src/lib/components/Wordmark.svelte` line 23 (`product?: string`) and line 31 (the
  words are `biscuit games / <product>`), line 36 (the `words` class the header's collapse
  reaches into).
- H `src/lib/index.ts` lines 26-65: what the root import exports. `HeaderBar`, `Wordmark`,
  `animationsActive`, `highContrastActive`, `createMediaPreferences`,
  `createFakePreferences` and the type `PreferencesPort` are all there; the icon map and
  the stylesheet are deliberately not.
- H `src/lib/domain/appearance.ts`: the three derivations, one line each, and the
  comment on why they are functions a game consumes.
- H `src/lib/ports/preferences.ts` lines 16-26 (`PreferencesPort`: `prefersDark`,
  `prefersReducedMotion`, `prefersMoreContrast`, `subscribe` returning the unsubscribe) and
  lines 72-104 (`createMediaPreferences(host = globalThis)`, which answers "no preference"
  when `matchMedia` is absent, as it is under jsdom and in Node at prerender).
- H `tests/appearance.test.ts`: the register a test here is written in — one `describe`
  per derivation, each `it` naming the guarantee it holds.
- H `src/routes/+page.svelte` lines 68-100: the `.page` shell, `main`, `p` and `ul` styles,
  every value a token.
- T `/Users/scutting/projects/biscuit_games_template/template/src/app.html`,
  `template/src/routes/+layout.svelte`, `template/tests/lockup.test.ts` and
  `template/tests/route.test.ts`: the shapes this ticket adapts.
- H `docs/design/character.md` "Voice" (lines 52-66): functional copy is plain, warm
  interface copy; never first person; no meme language.

## Goal

At the end of this ticket, on branch `ticket/s01-site-shell`:

- Every route renders inside the platform's stylesheet and chrome: `HeaderBar` draws the
  page's only `h1`, which reads `biscuit games / studio`.
- After hydration, `<html>` carries `data-animations="on"` unless the device asks for
  reduced motion, and `data-high-contrast="true"` only when the device asks for more
  contrast; both follow the device as it changes; `data-theme="dark"` is stated in the
  markup and never written by script.
- `src/lib/appearance.ts` and `src/lib/components/Lockup.svelte` are fully covered by
  `tests/appearance.test.ts` and `tests/lockup.test.ts`; `tests/route.test.ts` proves the
  home page's heading, title, landmark and two links.
- `just check` is green.

## Non-goals

- The model and gallery routes, and their tests: S03. The home page links to them by
  path, and the links resolve only after S03 merges; that is fine, because nothing here
  follows them.
- Any file under `assets/` or `static/pose-studio/`: S02.
- A settings control. The studio ships none, so `theme` stays the platform default and
  `data-theme="dark"` is markup, not state (CONVENTIONS.md §2.7).
- Stories or Storybook (CONVENTIONS.md §1 decision 10).
- Touching `src/lib/brand.ts`, `tests/brand.test.ts`, `src/routes/+layout.ts`,
  `src/app.d.ts`, `vite.config.ts` or any file CONVENTIONS.md §9 lists as touched by no
  lane.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `src/app.html` | S01 | T `template/src/app.html` (19 lines) | replaces S00's stub; `data-animations="on"` added on the `<html>` element as H `src/app.html` line 29 has it; comment rewritten (Step 1) |
| `src/lib/appearance.ts` | S01 | CONVENTIONS.md §2.7 | new; byte for byte |
| `src/lib/components/Lockup.svelte` | S01 | T `tickets/CONVENTIONS.md` §7 `Lockup.svelte`, adapted | new (Step 3) |
| `src/routes/+layout.svelte` | S01 | T `template/src/routes/+layout.svelte`, extended | replaces S00's stub (Step 4) |
| `src/routes/+page.svelte` | S01 | Step 5 (embedded) | replaces S00's placeholder |
| `tests/lockup.test.ts` | S01 | T `template/tests/lockup.test.ts`, adapted | new |
| `tests/appearance.test.ts` | S01 | Step 6 (embedded) | new |
| `tests/route.test.ts` | S01 | T `template/tests/route.test.ts`, extended | new |

The table is the whole scope. Nothing outside it is edited except the `status:` line of
this ticket.

## Steps

Work from the repository root on branch `ticket/s01-site-shell`. `just sync` first; the
registry token in `~/.npmrc` is what lets `npm ci` read the platform package.

### Step 1: `src/app.html`

T's file with one attribute added and the comment rewritten to say what is true here:

```html
<!doctype html>
<!--
  data-theme="dark" and data-animations="on" are `default AppearanceSettings
  appearance_settings` from the platform's appearance.allium, which
  @steven-cutting/biscuit-games ships, stated in the markup so the prerendered
  page paints the platform default before anything hydrates. Dark is home.

  The theme never changes: this site ships no settings control, so `theme` is
  the default and dark_active is true. The other two attributes are re-derived
  after hydration from the device, through the preferences port the package
  exports — src/routes/+layout.svelte does it, and src/lib/appearance.ts says
  how. data-high-contrast is absent here because app.css matches the literal
  string "true" and the setting's default is false; the layout adds it when the
  device asks for more contrast, and removes data-animations when the device asks
  for less motion.
-->
<html lang="en" data-theme="dark" data-animations="on">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="icon" href="data:," />
    %sveltekit.head%
  </head>
  <body data-sveltekit-preload-data="hover">
    <div style="display: contents">%sveltekit.body%</div>
  </body>
</html>
```

The favicon stays the empty data URL H and T carry: the reduced icon-mark does not exist
yet (H `docs/design/character.md` lines 25-32), and drawing one here would be deciding a
platform fact in the wrong repository.

### Step 2: `src/lib/appearance.ts`

Write CONVENTIONS.md §2.7's module byte for byte, including its comments. It imports
`animationsActive`, `highContrastActive` and the type `PreferencesPort` from the package
root, exports `documentAttributes(port)` and `applyAppearance(root, port)`, and touches no
global: `root` is an argument, which is what lets the test hand it an element it made.

### Step 3: `src/lib/components/Lockup.svelte`

```svelte
<script lang="ts">
  import { Wordmark } from '@steven-cutting/biscuit-games';

  import { STUDIO_NAME } from '$lib/brand';

  /**
   * This site's lockup: the platform's words, and then its own.
   *
   * The platform's `Wordmark` draws it, given a `product`, so the display face,
   * the weight, the tracking and the `words` class `HeaderBar` reaches into
   * to collapse the words below about 26rem are all the platform's. Every route
   * hands this to `HeaderBar` as its `brand` snippet, and the page's only `h1`
   * reads "biscuit games / studio".
   *
   * No markup of its own and no conditional block: a component with a branch
   * nothing renders is a branch the coverage floor counts against the whole tree.
   */
</script>

<Wordmark product={STUDIO_NAME} />
```

No `<style>`, so nothing for `svelte-check --fail-on-warnings` to call unused.

### Step 4: `src/routes/+layout.svelte`

```svelte
<script lang="ts">
  import '@steven-cutting/biscuit-games/app.css';

  import { createMediaPreferences } from '@steven-cutting/biscuit-games';
  import { onMount } from 'svelte';

  import { applyAppearance } from '$lib/appearance';

  /*
   * The design system's stylesheet, imported once and nowhere below it: the
   * token vocabulary, the four palettes, the two faces and the global element
   * rules together. This site's own styles name tokens from it and restate no
   * value.
   *
   * The one place `document` is reached. Everything under src/lib/ takes its
   * element and its port as arguments; this layout is where the real ones are
   * handed over, after hydration, because at prerender there is no document
   * and no device to ask. `createMediaPreferences()` reads `globalThis.matchMedia`
   * and answers "no preference" where it is absent, so the call is safe under
   * jsdom too. The unsubscribe is returned so the listeners go when the layout
   * does.
   */
  let { children }: { children?: import('svelte').Snippet } = $props();

  onMount(() => applyAppearance(document.documentElement, createMediaPreferences()));
</script>

{@render children?.()}
```

`src/routes/` is outside the coverage glob (`vite.config.ts` measures `src/lib/**`), which
is why the global is reached here and not in `appearance.ts`.

### Step 5: `src/routes/+page.svelte`

```svelte
<script lang="ts">
  import { HeaderBar } from '@steven-cutting/biscuit-games';
  import { base } from '$app/paths';

  import { STUDIO_DESCRIPTION, STUDIO_TITLE } from '$lib/brand';
  import Lockup from '$lib/components/Lockup.svelte';

  /*
   * The front door: the platform's chrome carrying this site's lockup, one
   * sentence, and the two places to go. `HeaderBar` carries the page's `h1`,
   * so there is no heading here.
   *
   * `base` is `/biscuit_studio` when pages.yml builds the site and empty
   * locally; every internal link carries it so a prerendered page works where
   * Pages serves it. Every selector below names an element, because
   * `svelte-check --fail-on-warnings` turns an unused selector into a failed
   * gate and an element selector cannot go stale.
   */
</script>

<svelte:head>
  <title>{STUDIO_TITLE}</title>
  <meta name="description" content={STUDIO_DESCRIPTION} />
</svelte:head>

<div class="page">
  <HeaderBar>
    {#snippet brand()}
      <Lockup />
    {/snippet}
  </HeaderBar>

  <main>
    <p>
      Where Biscuit is made. The poseable model she is drawn from, the renders taken from
      it, and the illustrations that came before it, kept here so every game draws the
      same dog.
    </p>

    <ul role="list">
      <li><a href="{base}/model/">The model</a></li>
      <li><a href="{base}/gallery/">The gallery</a></li>
    </ul>
  </main>
</div>

<style>
  .page {
    max-inline-size: var(--shell-max);
    margin-inline: auto;
    padding-inline: var(--shell-pad);
  }

  main {
    padding-block: var(--s-8) var(--s-11);
    color: var(--text);
    font-family: var(--font-ui);
  }

  p {
    margin-block: 0 var(--s-8);
    color: var(--text-2);
    line-height: 1.5;
  }

  ul {
    display: grid;
    gap: var(--s-5);
    margin-block: var(--s-5) 0;
    padding: 0;
    list-style: none;
  }

  a {
    color: var(--text);
  }
</style>
```

The `role="list"` on a `<ul>` whose markers are removed is H's own reasoning at H
`src/routes/+page.svelte` lines 45-51. Every token named exists in H `src/app.css`
(`--shell-max`, `--shell-pad`, `--s-5`, `--s-8`, `--s-11`, `--text`, `--text-2`,
`--font-ui`). The copy is plain interface copy in the platform's register: no first
person, no exclamation, and Biscuit is observed rather than speaking.

### Step 6: the three tests

`tests/lockup.test.ts` is T's file with `GAME_NAME` replaced by `STUDIO_NAME` and "this
game" by "this site". `tests/route.test.ts` is T's with `STUDIO_NAME`/`STUDIO_TITLE` and
one more case:

```ts
  it('offers the model and the gallery by name', () => {
    render(Page);

    expect(screen.getByRole('link', { name: 'The model' })).toHaveAttribute('href', '/model/');
    expect(screen.getByRole('link', { name: 'The gallery' })).toHaveAttribute('href', '/gallery/');
  });
```

`base` is empty under Vitest because nothing sets `BASE_PATH` there, so the expected
hrefs carry no prefix.

`tests/appearance.test.ts`:

```ts
import { createFakePreferences } from '@steven-cutting/biscuit-games';
import { describe, expect, it } from 'vitest';

import { applyAppearance, documentAttributes } from '../src/lib/appearance';

/*
 * appearance.allium — the `Appearance` surface, as this site honours it with
 * its settings fixed at the platform default: theme dark, high contrast off,
 * animations on. Only the device can move the two attributes below.
 */
describe('documentAttributes', () => {
  // ReducedMotionOverridesTheAnimationSetting: the device wins.
  it('keeps animations on while the device asks for no less motion', () => {
    expect(documentAttributes(createFakePreferences()).animations).toBe('on');
  });

  it('turns animations off when the device asks for less motion', () => {
    const port = createFakePreferences({ prefersReducedMotion: true });

    expect(documentAttributes(port).animations).toBeNull();
  });

  // MoreContrastFromTheDeviceTurnsHighContrastOn.
  it('leaves high contrast off while the device is silent', () => {
    expect(documentAttributes(createFakePreferences()).highContrast).toBeNull();
  });

  it('turns high contrast on when the device asks for more', () => {
    const port = createFakePreferences({ prefersMoreContrast: true });

    expect(documentAttributes(port).highContrast).toBe('true');
  });
});

describe('applyAppearance', () => {
  // SystemFollowsTheDeviceAsItChanges: written now, and again on every change.
  it('writes both attributes on the element it is given, and follows the device', () => {
    const root = document.createElement('div');
    const port = createFakePreferences();

    applyAppearance(root, port);

    expect(root).toHaveAttribute('data-animations', 'on');
    expect(root).not.toHaveAttribute('data-high-contrast');

    port.set({ prefersReducedMotion: true, prefersMoreContrast: true });

    expect(root).not.toHaveAttribute('data-animations');
    expect(root).toHaveAttribute('data-high-contrast', 'true');
  });

  it('stops following the device once unsubscribed', () => {
    const root = document.createElement('div');
    const port = createFakePreferences();
    const stop = applyAppearance(root, port);

    stop();
    port.set({ prefersReducedMotion: true });

    expect(root).toHaveAttribute('data-animations', 'on');
  });
});
```

The element is one the test creates and owns; no global is stubbed and `document` is used
only to make it, which is what the boundary rule permits a test (a test may use the
environment it runs in; it may not replace a global). Both branches of both attributes are
reached, in `documentAttributes` and through `applyAppearance`'s `write`, so the four
coverage figures over `src/lib/appearance.ts` are 100.

### Step 7: run and hand back

`just frontend-static`, `just frontend-coverage`, `just frontend-build`, then `just check`.
Commit on the ticket branch, fill in the hand-back notes, set `status: done`. Pushing and
opening the pull request are separately authorised.

## Acceptance criteria

- [ ] `src/lib/appearance.ts` is byte-identical to CONVENTIONS.md §2.7's block.
- [ ] `just frontend-coverage` reports 100 on all four figures for `src/lib/appearance.ts`
      and `src/lib/components/Lockup.svelte`, and the run passes the 90 floor.
- [ ] `tests/route.test.ts` proves: the level-one heading reads `biscuit games / studio`;
      `document.title` is `Biscuit Studio`; a `main` landmark exists; links named
      `The model` and `The gallery` carry `href` `/model/` and `/gallery/`.
- [ ] `tests/appearance.test.ts` proves both values of both attributes and that the
      unsubscribe stops updates.
- [ ] `src/routes/+layout.svelte` is the only file under `src/` that names `document`,
      and it does so inside `onMount`: `grep -rn 'document\.' src/` prints exactly one line.
- [ ] `BASE_PATH=/biscuit_studio just frontend-build` succeeds and `build/index.html`
      contains `href="/biscuit_studio/model/"` and `href="/biscuit_studio/gallery/"`.
- [ ] `just check` is green.
- [ ] Each open point below is answered in the hand-back notes.

## Verification

```sh
just frontend-static
just frontend-coverage
grep -rn 'document\.' src/
BASE_PATH=/biscuit_studio just frontend-build && grep -c 'href="/biscuit_studio/\(model\|gallery\)/"' build/index.html
just check
```

Expected: the first two exit 0, with the coverage table showing `appearance.ts` and
`Lockup.svelte` at 100 across; the grep prints one line, `src/routes/+layout.svelte`; the
build succeeds and the count is 2; `just check` ends green.

Then, once in a browser: `just dev`, open the page, and in the developer tools emulate
`prefers-reduced-motion: reduce` — `<html>` loses `data-animations` without a reload.
Record what was seen.

## Hand-back notes

Filled in by the agent that executes this ticket.

- The coverage table for `src/lib/**`, quoted.
- The output of every verification command, quoted.
- Whether `document.title` was reflected under jsdom (CONVENTIONS.md §10, assigned here);
  if the case was dropped, say so and why.
- Whether rendering `+page.svelte` under Vitest resolved `$app/paths` without further
  configuration (the open point below).
- Anything handed back to S00 (a needed change to a file no lane touches) or to S03.

## Open points

- **`$app/paths` under Vitest.** H's tests render components, never a route that imports
  `$app/paths`. The SvelteKit Vite plugin `vite.config.ts` loads should resolve the module
  under the jsdom project; if it does not, the smallest fix is to read `base` in the page
  through a one-line `src/lib/paths.ts` re-export and mock that module in the test — say
  which happened.
- **`document.title` under jsdom** (CONVENTIONS.md §10). T recorded the same claim for a
  game and its render passed; check here rather than assume.
- **The link copy.** `The model` and `The gallery` are the names S03's pages answer to;
  if S03 lands first with other headings, the names here follow S03's and this ticket says
  so in its notes rather than changing S03's files.
