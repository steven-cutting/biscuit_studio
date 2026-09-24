---
id: S03
title: "Showcase routes: the model page around the embedded viewer, and the gallery"
status: done
depends_on: [S01, S02]
parallel_with: [S04, S05, S06]
branch: ticket/s03-showcase-routes
estimated_size: M
---

# S03: Showcase routes: the model page around the embedded viewer, and the gallery

## Context

After S01 the site has a front door that links to `/model/` and `/gallery/`, and after
S02 the approved model and the cel set are in the tree: the viewer, the GLB and the pose
overview under `static/pose-studio/` (served by Pages byte for byte), the sources under
`assets/models/biscuit/`, and the eleven cel PNG files under `assets/illustrations/good/`, all
listed in `assets/manifest.json`. This ticket writes the two pages those links point at.

The viewer is embedded as-is (CONVENTIONS.md §1 decision 3) and it is **linked, not
framed**. It is a 27,561,425-byte page with its geometry and thirty-six textures inlined,
so an `<iframe>` inside the shell would load it on top of the shell rather than instead of
it; and it carries its own `<meta name="color-scheme" content="light">`, a cream ground
(`#ede7de`) and a vermilion rule (D `models/biscuit/viewer.html`, the `<style>` block in
its first kilobyte), which would sit inside the platform's dark room as a second break —
the one the design direction's operating rule forbids (H `docs/design/direction.md`
lines 43-60). The model page therefore shows the preview image, says what the model is,
and hands the reader to the viewer as a whole page of its own. Ticket C03 is where a
viewer that wears the platform's tokens gets built.

Read first, at the commits CONVENTIONS.md §0 pins (read-only):

- CONVENTIONS.md §1 decision 3 and 8, §2 (the rows marked S03), §3 (the
  `static/pose-studio/` layout and the three rewritten hrefs), §5 (the cel set is
  generated and not yet cleared to leave), §10, §11.
- D `/Users/scutting/.supacode/repos/biscuit_pics/very_nice_three_deeez/models/biscuit/README.md`
  lines 1-9 (what the model is: Soft Charm face, Full Soft ears, Longer Drape tail, fitted
  cream sweater, the poseable rig), line 44 (the GLB "uses standard PBR materials, so
  lighting and outlines can look different in other viewers"), lines 55-59 (33 deform
  bones, four presets, still posing only).
- H `/Users/scutting/projects/biscuit_games/src/lib/index.ts` lines 26-48: `CardLabel`
  is exported, and H `src/lib/components/CardLabel.svelte` renders an `<h2>` — the one
  heading level below the lockup a page here can reach without writing its own.
- H `src/routes/+page.svelte` lines 68-100 and this repository's `src/routes/+page.svelte`
  (S01) for the `.page` shell and the tokens; `src/lib/components/Lockup.svelte` (S01).
- H `docs/design/character.md` lines 52-66 ("Voice") for the register of every sentence.
- `assets/manifest.json` (S02) for the paths and the eleven filenames.

## Goal

At the end of this ticket, on branch `ticket/s03-showcase-routes`:

- `/model/` shows the pose overview, says what the model is and what it is not, links to
  the pose studio as a full page, offers the GLB for download with the sentence about its
  materials, and links to the `.blend` on GitHub.
- `/gallery/` shows the eleven cel illustrations as captioned figures with real alt text,
  and says how they were made and that they have not left the studio.
- Both pages wear the shell S01 built, and `tests/pages.test.ts` proves their headings,
  links and images.
- A build with `BASE_PATH=/biscuit_studio` carries the viewer and the GLB into `build/`
  unchanged and links to them under the base path.
- `just check` is green.

## Non-goals

- A three.js viewer, or any change to the embedded one: C03.
- Any file under `static/pose-studio/` or `assets/`, or `assets/manifest.json`: S02's,
  and this ticket reads them only.
- Thumbnails or a resized copy of any illustration (an open point below).
- Promoting anything to the hub or a game (C01, C02).
- The home page, the layout, `app.html`, the lockup and S01's tests.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `src/routes/model/+page.svelte` | S03 | Step 1 (embedded) | new |
| `src/routes/gallery/+page.svelte` | S03 | Step 2 (embedded) | new |
| `tests/pages.test.ts` | S03 | Step 3 (embedded) | new |
| `svelte.config.js` | S03 | this repository (S01) | remove the `NOT_YET_BUILT` set and the `prerender` block, which let the crawler past a 404 on the two routes this ticket adds |

The table is the whole scope. Nothing outside it is edited except the `status:` line of
this ticket.

## Steps

Work from the repository root on branch `ticket/s03-showcase-routes`, created from
`main` after S01 and S02 have both merged. `just sync` first.

### Step 1: `src/routes/model/+page.svelte`

```svelte
<script lang="ts">
  import { CardLabel, HeaderBar } from '@steven-cutting/biscuit-games';
  import { base } from '$app/paths';

  import Lockup from '$lib/components/Lockup.svelte';

  /*
   * The model, and the three ways to have it. The viewer is a whole page of its
   * own rather than a frame here: it is 26 MB with its textures inlined, and it
   * carries its own light palette, which would sit inside the platform's dark
   * ground as a second break. The .blend is not served — it is an LFS object,
   * and Pages would serve its pointer as text — so that link goes to GitHub.
   *
   * `base` is /biscuit_studio where Pages serves the site and empty locally.
   */
  const BLEND_URL =
    'https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/model/biscuit-poseable.blend';
</script>

<svelte:head>
  <title>Biscuit Studio: the model</title>
  <meta
    name="description"
    content="The approved poseable model of Biscuit: the pose studio, the portable GLB and the Blender scene."
  />
</svelte:head>

<div class="page">
  <HeaderBar>
    {#snippet brand()}
      <Lockup />
    {/snippet}
  </HeaderBar>

  <main>
    <CardLabel>The model</CardLabel>

    <img
      src="{base}/pose-studio/previews/pose-overview.jpg"
      alt="Biscuit in the four preset poses: standing, sitting, lying down and with a paw raised, each shown dressed in the cream sweater and undressed."
      width="930"
      height="900"
    />

    <p>
      The approved model: the Soft Charm face, the Full Soft ears, the Longer Drape tail and
      the fitted cream sweater, on a rig of thirty-three deform bones with four preset poses.
      It is a rig for still posing. There is no facial rig, no cloth simulation and no
      animation.
    </p>

    <ul role="list">
      <li>
        <a href="{base}/pose-studio/viewer.html" rel="external" data-sveltekit-reload>
          Open the pose studio
        </a>
        — poses, views and a PNG or pose file to save, in a page of its own. It needs
        WebGL 2 and works offline.
      </li>
      <li>
        <a
          href="{base}/pose-studio/model/biscuit-poseable.glb"
          rel="external"
          data-sveltekit-reload
          download>Download the GLB</a
        >
        — the skinned standing rig with its textures and the sweater's corrective shapes.
        It carries standard PBR materials rather than the approved cel shading, so it looks
        different from the studio in another viewer.
      </li>
      <li>
        <a href={BLEND_URL}>The Blender scene on GitHub</a> — the editable native source,
        with the pose panel embedded.
      </li>
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

  img {
    display: block;
    inline-size: 100%;
    block-size: auto;
    margin-block: var(--s-5) var(--s-8);
    border: var(--rule-w) solid var(--rule);
    border-radius: var(--radius-card);
  }

  p {
    margin-block: 0 var(--s-8);
    color: var(--text-2);
    line-height: 1.5;
  }

  ul {
    display: grid;
    gap: var(--s-5);
    margin: 0;
    padding: 0;
    list-style: none;
    color: var(--text-2);
    line-height: 1.5;
  }

  a {
    color: var(--text);
  }
</style>
```

`width` and `height` on the image are the overview's pixel size, read from the file with
`python3 -c 'from PIL import Image; print(Image.open("static/pose-studio/previews/pose-overview.jpg").size)'`;
if that prints something other than `(930, 900)`, use what it prints. Every token named
exists in H `src/app.css` (`--rule`, `--rule-w`, `--radius-card` beside those S01 used).
The `download` attribute on the GLB link is what makes a browser save a 16 MB binary
rather than navigate to it.

### Step 2: `src/routes/gallery/+page.svelte`

The eleven files under `assets/illustrations/good/`, imported by Vite so the build hashes
and copies them, with the sizes S02 recorded (bytes): `cool-body` 869,681; `cool-head`
1,361,047; `warm-body` 979,044; `warm-head` 1,530,312; `warm-head-bashful` 1,525,989;
`warm-head-bashful-blush-exaggerated` 1,527,884; `warm-head-chin-lifted` 1,462,047;
`warm-head-eye-slant` 1,481,154; `warm-head-looking-up` 1,424,974; `warm-head-sad`
1,478,921; `warm-head-side-eye` 1,496,671. Heads are 1374×1145, bodies 958×1642, all
RGBA.

```svelte
<script lang="ts">
  import { CardLabel, HeaderBar } from '@steven-cutting/biscuit-games';

  import Lockup from '$lib/components/Lockup.svelte';

  import coolBody from '../../../assets/illustrations/good/cool-body.png';
  import coolHead from '../../../assets/illustrations/good/cool-head.png';
  import warmBody from '../../../assets/illustrations/good/warm-body.png';
  import warmHead from '../../../assets/illustrations/good/warm-head.png';
  import warmHeadBashful from '../../../assets/illustrations/good/warm-head-bashful.png';
  import warmHeadBashfulBlush from '../../../assets/illustrations/good/warm-head-bashful-blush-exaggerated.png';
  import warmHeadChinLifted from '../../../assets/illustrations/good/warm-head-chin-lifted.png';
  import warmHeadEyeSlant from '../../../assets/illustrations/good/warm-head-eye-slant.png';
  import warmHeadLookingUp from '../../../assets/illustrations/good/warm-head-looking-up.png';
  import warmHeadSad from '../../../assets/illustrations/good/warm-head-sad.png';
  import warmHeadSideEye from '../../../assets/illustrations/good/warm-head-side-eye.png';

  /*
   * The cel set: two bodies and nine heads, two colour grades, made to be mixed
   * and matched. Imported rather than read from static/ so the build fingerprints
   * each file and a stale cache cannot show an old drawing under a new name.
   *
   * Every figure carries its own caption and its own alt text, because the
   * caption says what the drawing is for and the alt says what is in it, and a
   * reader who hears only one of them should not lose the other.
   */
  const FIGURES = [
    { src: warmHead, caption: 'Warm head, resting', alt: 'Biscuit’s head in the warm grade, facing forward with a level gaze.' },
    { src: warmBody, caption: 'Warm body', alt: 'Biscuit’s body in the warm grade, standing in the cream sweater, drawn without a head so a head can be placed on it.' },
    { src: coolHead, caption: 'Cool head, resting', alt: 'Biscuit’s head in the cool grade, facing forward with a level gaze.' },
    { src: coolBody, caption: 'Cool body', alt: 'Biscuit’s body in the cool grade, standing in the cream sweater, drawn without a head.' },
    { src: warmHeadBashful, caption: 'Warm head, bashful', alt: 'Biscuit’s head turned slightly away with lowered eyes.' },
    { src: warmHeadBashfulBlush, caption: 'Warm head, bashful with blush', alt: 'Biscuit’s head turned slightly away with lowered eyes and an exaggerated blush across the muzzle.' },
    { src: warmHeadChinLifted, caption: 'Warm head, chin lifted', alt: 'Biscuit’s head with the chin raised and the eyes half closed.' },
    { src: warmHeadEyeSlant, caption: 'Warm head, eye slant', alt: 'Biscuit’s head with the eyes narrowed into a slant.' },
    { src: warmHeadLookingUp, caption: 'Warm head, looking up', alt: 'Biscuit’s head tilted back, eyes raised to something above.' },
    { src: warmHeadSad, caption: 'Warm head, sad', alt: 'Biscuit’s head with the ears low and the eyes turned down.' },
    { src: warmHeadSideEye, caption: 'Warm head, side eye', alt: 'Biscuit’s head facing forward with the eyes slid to one side.' }
  ] as const;
</script>

<svelte:head>
  <title>Biscuit Studio: the gallery</title>
  <meta
    name="description"
    content="The cel illustrations of Biscuit: two bodies and nine heads in two colour grades."
  />
</svelte:head>

<div class="page">
  <HeaderBar>
    {#snippet brand()}
      <Lockup />
    {/snippet}
  </HeaderBar>

  <main>
    <CardLabel>The gallery</CardLabel>

    <p>
      Eleven cel drawings made before the model: two bodies and nine heads, in a warm and a
      cool grade, cut to be mixed and matched. They were generated with ChatGPT from
      photographs of the real dog and picked by hand. They are studio material: nothing here
      has been cleared to leave the studio, and the platform's design direction decides
      whether any of it can.
    </p>

    <ul role="list">
      {#each FIGURES as figure, index (figure.caption)}
        <li>
          <figure>
            <img
              src={figure.src}
              alt={figure.alt}
              loading={index === 0 ? 'eager' : 'lazy'}
              decoding="async"
            />
            <figcaption>{figure.caption}</figcaption>
          </figure>
        </li>
      {/each}
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
    grid-template-columns: repeat(auto-fill, minmax(9rem, 1fr));
    gap: var(--s-5);
    margin: 0;
    padding: 0;
    list-style: none;
  }

  figure {
    margin: 0;
  }

  img {
    display: block;
    inline-size: 100%;
    block-size: auto;
    background: var(--surface);
    border: var(--rule-w) solid var(--rule);
    border-radius: var(--radius-card);
  }

  figcaption {
    margin-block-start: var(--s-2);
    color: var(--text-3);
    font-size: var(--fs-small);
  }
</style>
```

The alt texts describe what the executing agent sees after opening each file; the ones
above are a starting point written from the filenames, and the agent corrects any that
misdescribe the drawing, recording the change. The first figure loads eagerly and the
rest lazily; the page is still 14 MB when scrolled to the end, which is the open point
below. `decoding="async"` keeps a 1.5 MB PNG from blocking paint. The ground behind a
transparent PNG is `--surface`, so the cut-outs read on the dark room rather than on
nothing.

If Vite refuses the `.png` imports under TypeScript (`svelte-check` reporting that the
module has no type), add nothing to `src/app.d.ts`: SvelteKit's generated ambient types
already declare `*.png`. Record what was seen.

### Step 3: `tests/pages.test.ts`

```ts
import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';

import { STUDIO_NAME } from '../src/lib/brand';
import Gallery from '../src/routes/gallery/+page.svelte';
import Model from '../src/routes/model/+page.svelte';

const LOCKUP = `biscuit games / ${STUDIO_NAME}`;

describe('the model page', () => {
  it('carries the lockup as its only level-one heading and names its section', () => {
    render(Model);

    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(LOCKUP);
    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('The model');
  });

  it('hands the reader to the pose studio as a whole page', () => {
    render(Model);

    expect(screen.getByRole('link', { name: 'Open the pose studio' })).toHaveAttribute(
      'href',
      '/pose-studio/viewer.html'
    );
  });

  it('offers the GLB for download and the Blender scene on GitHub', () => {
    render(Model);

    expect(screen.getByRole('link', { name: 'Download the GLB' })).toHaveAttribute(
      'href',
      '/pose-studio/model/biscuit-poseable.glb'
    );
    expect(screen.getByRole('link', { name: 'The Blender scene on GitHub' })).toHaveAttribute(
      'href',
      expect.stringContaining('/blob/main/assets/models/biscuit/model/biscuit-poseable.blend')
    );
  });

  it('describes its preview image', () => {
    render(Model);

    expect(screen.getByRole('img').getAttribute('alt')).toMatch(/four preset poses/);
  });
});

describe('the gallery page', () => {
  it('carries the lockup and names its section', () => {
    render(Gallery);

    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(LOCKUP);
    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('The gallery');
  });

  it('lists eleven captioned figures, every one with alt text', () => {
    render(Gallery);

    const figures = screen.getAllByRole('figure');

    expect(figures).toHaveLength(11);
    for (const image of screen.getAllByRole('img')) {
      expect(image.getAttribute('alt')?.trim()).not.toBe('');
    }
  });

  it('says the drawings were generated and have not left the studio', () => {
    render(Gallery);

    expect(screen.getByText(/generated with ChatGPT/)).toBeInTheDocument();
    expect(screen.getByText(/has been cleared to leave the studio/)).toBeInTheDocument();
  });
});
```

`base` is empty under Vitest, so the expected hrefs carry no prefix. A `<figure>` with a
`<figcaption>` has the `figure` role in jsdom's accessibility tree, which is what
`getAllByRole('figure')` counts; if Testing Library reports none, query
`getAllByRole('img')` for the count instead and say so.

### Step 4: the build under the base path

```sh
BASE_PATH=/biscuit_studio just frontend-build
grep -c '/biscuit_studio/pose-studio/viewer.html' build/model/index.html
grep -c '/biscuit_studio/pose-studio/model/biscuit-poseable.glb' build/model/index.html
shasum -a 256 build/pose-studio/viewer.html build/pose-studio/model/biscuit-poseable.glb
python3 -c 'import json; m = {a["path"]: a["sha256"] for a in json.load(open("assets/manifest.json"))["assets"]}; print(m["static/pose-studio/viewer.html"]); print(m["static/pose-studio/model/biscuit-poseable.glb"])'
ls build/_app/immutable/assets/ | grep -c '\.png$'
```

The two `shasum` lines must equal the two manifest lines: `adapter-static` copies
`static/` into `build/` unchanged, and this is the check that it did. The PNG count is 11.

### Step 5: run and hand back

`just frontend-static`, `just frontend-coverage`, `just frontend-build`, `just check`.
Commit on the ticket branch, fill in the hand-back notes, set `status: done`. Pushing and
opening the pull request are separately authorised.

## Acceptance criteria

- [ ] `tests/pages.test.ts` passes: both pages carry the lockup as the only `h1` and a
      level-two section heading; the viewer link's `href` is `/pose-studio/viewer.html`;
      the GLB link's `href` is `/pose-studio/model/biscuit-poseable.glb`; the `.blend`
      link goes to the GitHub blob URL; every image has non-empty alt text; the gallery
      lists eleven figures; the generated-and-not-cleared sentence is present.
- [ ] The model page states that the GLB carries standard PBR materials rather than the
      approved cel shading (CONVENTIONS.md §11).
- [ ] The model page frames nothing: `grep -c iframe src/routes/model/+page.svelte`
      prints 0.
- [ ] `BASE_PATH=/biscuit_studio just frontend-build` links the viewer and the GLB under
      `/biscuit_studio/pose-studio/`, and the copied viewer and GLB in `build/` hash to
      the manifest's `sha256` for each.
- [ ] The built gallery carries eleven fingerprinted PNG files under `build/_app/immutable/assets/`.
- [ ] `just frontend-coverage` still passes the 90 floor (these routes are outside the
      glob; the floor is unchanged by them).
- [ ] `just check` is green.
- [ ] Each open point below is answered in the hand-back notes.

## Verification

```sh
just frontend-static
just frontend-unit
grep -c iframe src/routes/model/+page.svelte
BASE_PATH=/biscuit_studio just frontend-build
grep -c '/biscuit_studio/pose-studio/viewer.html' build/model/index.html
shasum -a 256 build/pose-studio/viewer.html
python3 -c 'import json; print({a["path"]: a["sha256"] for a in json.load(open("assets/manifest.json"))["assets"]}["static/pose-studio/viewer.html"])'
ls build/_app/immutable/assets/ | grep -c '\.png$'
just check
```

Expected: static and unit exit 0; `0` iframes; the build succeeds; the viewer count is at
least 1; the two sha256 lines are identical; the PNG count is 11; `just check` ends green.

Then in a browser with `BASE_PATH=/biscuit_studio just preview`: open
`/biscuit_studio/model/`, follow "Open the pose studio", and confirm the viewer draws the
model and its "Preview the poses" link resolves. Record what was seen, and the load time
of `/biscuit_studio/gallery/` from the network panel.

## Hand-back notes

Filled in by the agent that executes this ticket.

Executed on 2026-09-24 on the Supacode worktree branch `S03-showcase-routes`, not
`ticket/s03-showcase-routes` (the S00 decision: nothing reads the branch name), from
`main` at `e32d45a`. Acceptance-criteria boxes are left unticked; the evidence is here.

### Departures from the embedded code

- **`base` became `asset()`.** `base` from `$app/paths` is deprecated in the pinned
  SvelteKit 2.70.2 and the lint gate errors on it (S01 found this). The model page calls
  `asset('/pose-studio/…')` for the overview, the viewer and the GLB; `asset()` is typed
  against the files under `static/`, so a wrong path fails `svelte-check`. The comment was
  rewritten to say so. Both anchors keep `rel="external"` and `data-sveltekit-reload`.
- **The overview is 1920×2070**, not 930×900:
  `uv run --frozen python3 -c 'from PIL import Image; …'` printed `(1920, 2070)`, and those
  are the `width` and `height` attributes.
- **Gallery spacing.** The paragraph under the "The gallery" label had
  `margin-block: 0 …` and sat flush against the heading in the browser; it is now
  `margin-block: var(--s-5) var(--s-8)`, matching the gap the model page's image leaves.
- **`vite.config.ts` gained `server.fs.allow: ['assets']`**. This file is outside the table
  and the change was authorised by the maintainer during the ticket; see the fourth
  CONVENTIONS §10 claim below.
- Prettier reflowed the long `FIGURES` entries and two list items; the words are the
  ticket's except where the alt texts below say otherwise.

### Alt texts corrected after looking at the drawings

- Overview. Before: "… each shown dressed in the cream sweater and undressed." After:
  "Biscuit in the four preset poses, each in the cream sweater: standing, sitting, lying
  down and with a paw raised." All four cards in the sheet are dressed.
- Warm head. Before: "… facing forward with a level gaze." After: "… in three-quarter
  view: a cream topknot, long russet ears and brown eyes with a soft, open gaze."
- Warm body. Before: "… standing in the cream sweater …". After: "… sitting in the cream
  turtleneck sweater with her tail curled beside her, drawn without a head so a head can
  be placed on it." Both bodies sit, hind legs folded, with a neck stub where the head goes.
- Cool head. After: "The same resting head in the cool grade, the cream fur turned grey."
- Cool body. Before: "… standing in the cream sweater, drawn without a head." After: "The
  same sitting body in the cool grade, the sweater and fur turned grey, drawn without a
  head."
- Bashful. Before: "… turned slightly away with lowered eyes." After: "… with the eyes
  closed in a contented squint." The head faces the same way as the resting one.
- Bashful with blush. Before: "… an exaggerated blush across the muzzle." After: "… the
  eyes closed in a squint and a pink blush, hatched with short strokes, on both cheeks."
- Chin lifted. Before: "… the eyes half closed." After: "… looking down her nose through
  heavy lids."
- Eye slant. Before: "… narrowed into a slant." After: "… half closed under lowered lids,
  unimpressed."
- Looking up. After: "… tilted, the eyes raised to something above and to one side."
- Sad. Before: "… the ears low and the eyes turned down." After: "… the brows drawn
  together and the eyes cast down and away." The ears are the same as on every other head.
- Side eye. After: "… facing forward with the eyes slid up and to one side."

### Verification output

`just frontend-static`: exit 0; ESLint and Prettier clean, and `svelte-check` printed
`COMPLETED 426 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS`.

`just frontend-unit`: `Test Files  5 passed (5)`, `Tests  20 passed (20)`.

`just frontend-coverage`: exit 0; `coverage/coverage-summary.json` total is 100% on lines
(13/13), statements (16/16), functions (5/5) and branches (8/8). The new routes are outside
the `src/lib/**` glob, as the ticket said.

`grep -c iframe src/routes/model/+page.svelte`: `0`.

`BASE_PATH=/biscuit_studio just frontend-build`: exit 0, with no warning about the 26 MB
file and no collision warning. Then:

```text
$ grep -c '/biscuit_studio/pose-studio/viewer.html' build/model/index.html
0
$ grep -c '/biscuit_studio/pose-studio/model/biscuit-poseable.glb' build/model/index.html
0
$ grep -oE '(src|href)="[^"]*pose-studio[^"]*"' build/model/index.html
src="../pose-studio/previews/pose-overview.jpg"
href="../pose-studio/viewer.html"
href="../pose-studio/model/biscuit-poseable.glb"
$ shasum -a 256 build/pose-studio/viewer.html build/pose-studio/model/biscuit-poseable.glb
ec1e9d32399191de2593e9737d5242c10ca8b6a41dc0029680f710065fe3c6e8  build/pose-studio/viewer.html
51d16c1826b2c3ad6ad85fcb176a73e0d1c7a0ac3665ad10f1b6700e9e9be716  build/pose-studio/model/biscuit-poseable.glb
$ python3 -c '…manifest sha256 for the two paths…'
ec1e9d32399191de2593e9737d5242c10ca8b6a41dc0029680f710065fe3c6e8
51d16c1826b2c3ad6ad85fcb176a73e0d1c7a0ac3665ad10f1b6700e9e9be716
$ ls build/_app/immutable/assets/ | grep -c '\.png$'
11
```

The two absolute-path greps print 0 rather than "at least 1" because `kit.paths.relative`
defaults to true, so prerendered markup links relatively (S01 recorded the same for the
home page). From `/biscuit_studio/model/`, `../pose-studio/viewer.html` resolves to
`/biscuit_studio/pose-studio/viewer.html`. After hydration the browser's accessibility tree
showed `href="/biscuit_studio/pose-studio/viewer.html"` and
`href="/biscuit_studio/pose-studio/model/biscuit-poseable.glb"`, so the links do sit under
the base path. The gallery's image `src` values are absolute, for example
`/biscuit_studio/_app/immutable/assets/warm-head.CyJ62iHX.png`. The overview JPEG's hash
matches the manifest too (`12d6a866…`).

`just check`: `All checks passed and the worktree is unchanged.`

### Browser check

Chrome, with `BASE_PATH=/biscuit_studio just preview` on `127.0.0.1:4173`:

- `/biscuit_studio/model/` rendered in the shell: the lockup, the "THE MODEL" label, the
  overview, the paragraph and the three links.
- "Open the pose studio" left the app for
  `/biscuit_studio/pose-studio/viewer.html` as a whole page. After "Getting Biscuit
  ready…" for a few seconds, it drew the dressed, standing model. There were no console
  errors, and WebGL 2 was available.
- In the viewer, "Pose overview" and "the preview sheet" both go to
  `/biscuit_studio/pose-studio/previews/pose-overview.jpg` (HEAD `200`), and "Skinned
  model · GLB" returns `200`.
- The viewer's "Posing guide" (README) and "Poseable Blender scene" links point at the
  expected GitHub blob URLs under `steven-cutting/biscuit_studio/blob/main/`. They were
  not followed: the repository is not on GitHub until S07, so they cannot resolve yet.
  The same goes for the model page's "The Blender scene on GitHub".
- `/biscuit_studio/gallery/` on first load, before any scroll: one PNG, 1,530,612 bytes,
  with `load` at 23 ms. Scrolled to the end: 11 PNG files, 15,141,024 bytes transferred,
  and the last response ended 4,468 ms after navigation (served from localhost, so this
  is decode and lazy-load time, not network). The drawings painted progressively for
  several seconds after arriving.

### The four CONVENTIONS §10 claims

- **The 26 MB file under `static/`.** Holds. `svelte-check --fail-on-warnings` and
  `vite build` printed nothing about it, and `adapter-static` copied the viewer and the
  GLB byte for byte (the sha256 values above).
- **`src/routes/model/` beside `static/pose-studio/`.** Holds. No collision warning in
  either build, and both `/model/` and `/pose-studio/viewer.html` are served.
- **The crawler and `static/` links.** Holds for the crawler. I removed
  `rel="external"` and `data-sveltekit-reload` from both anchors in a scratch edit and
  ran `just frontend-build`. It exited 0 with `build/model/index.html` written, so the
  crawler treats a target under `static/` as an asset, not a route. The attributes were
  put back and are in the commit, as the ticket requires. The click through the router
  was checked with the attributes in place: it left the app.
- **PNG imports from `assets/` without `server.fs.allow`.** False for dev. Build and
  jsdom are fine (11 hashed PNG files; 20 tests pass). Under `vite dev`, `/gallery/`
  referenced `/assets/illustrations/good/warm-head.png`, which returned `403` with "The
  request id … is outside of Vite serving allow list". SvelteKit's own allow list does
  not include the repository root. With `server.fs.allow: ['assets']`, all 11 return
  `200`, and a request under `/@fs/` for a file outside the repository still returns
  `403`.

### The open points

- **Thumbnails.** Measured at 15,141,024 bytes for the scrolled gallery (above), about
  14.4 MiB, as the ticket estimated. The point carries forward to an `asset-change` of its
  own.
- **`getAllByRole('figure')` under jsdom.** It works: a `<figure>` with a `<figcaption>`
  has the `figure` role, the test counts 11, and the fallback was not needed.
- **The overview's dimensions.** 1920×2070 (above), not 930×900.
- **Links into `static/`.** Answered under the third §10 claim.
- **The viewer's README link.** It points at
  `https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/README.md`.
  It was not followed, because the repository is not published before S07.

### Handed back

- **To CONVENTIONS (maintainer).** The §10 claim that a PNG import from outside `src/`
  "resolves in build, dev and jsdom without `server.fs.allow`" is false for dev; the
  correction is `server.fs.allow: ['assets']` in `vite.config.ts`, now committed.
  CONVENTIONS.md itself was not edited. The Step 4 expectation of an absolute
  `/biscuit_studio/…` href in `build/model/index.html` should read as the relative href
  recorded above.
- **To S07.** Follow the three GitHub blob links (the model page's `.blend`, and the
  viewer's README and Blender links) once the repository is public.
- **To S02 and S01:** nothing. No manifest entry or path needed changing.

- The output of every verification command, quoted.
- The three CONVENTIONS.md §10 claims assigned here, each with the outcome: whether
  `svelte-check --fail-on-warnings` and `vite build` tolerated the 26 MB file under
  `static/` and copied it unchanged; whether `src/routes/model/` and
  `static/pose-studio/` coexisted without a collision warning; whether the PNG imports
  from `assets/` resolved in build, dev and jsdom without `server.fs.allow`.
- Every alt text corrected after looking at the drawing, before and after.
- The gallery's transfer size and load time as measured, for the open point below.
- Anything handed back to S02 (a manifest entry, a path) or to S01.

## Open points

- **Thumbnails.** The gallery transfers about 14 MB. A resized copy of each PNG (say
  480 px wide, WebP) would cut that by an order of magnitude, but a derived image is an
  asset, needs a manifest entry with `source: rebuilt:<date>` and a recipe that makes it
  deterministically, and belongs to an `asset-change` of its own rather than this ticket.
  Record the measured size and carry the point forward.
- **`getAllByRole('figure')` under jsdom.** Whether a `<figure>` with a `<figcaption>`
  reports the `figure` role there; the fallback is in Step 3.
- **The preview image's dimensions** (Step 1): confirm `930×900` from the file rather
  than from this ticket.
- **Links into `static/` from a prerendered page.** Two things SvelteKit does to an
  `<a href>` inside the app: the prerender crawler follows every same-origin link it
  renders and, with `strict: true` in `svelte.config.js`, fails the build on a target it
  cannot render; and the client router intercepts same-origin clicks. Both anchors above
  therefore carry `rel="external"` and `data-sveltekit-reload`, which take them out of
  both mechanisms. Whether the crawler treats a target that exists under `static/` as an
  asset rather than a route even without those attributes is a claim CONVENTIONS.md §10
  assigns to this ticket: build once without them and record what happens, then keep
  them regardless, because the router interception is the one that would otherwise turn
  a click on the viewer into a 404 inside the shell.
- **The viewer's "README" link.** After S02 it points at the GitHub blob URL of
  `assets/models/biscuit/README.md` (CONVENTIONS.md §3). It is checked by nothing on the
  site; note whether it resolved in the browser check.
