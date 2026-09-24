---
id: C03
title: "A three.js viewer inside the shell, retiring the embedded 26 MB file"
status: open
depends_on: [S03, C01]
parallel_with: []
branch: ticket/c03-threejs-viewer
estimated_size: L
---

# C03: A three.js viewer inside the shell, retiring the embedded 26 MB file

## Context

S03 serves the pose studio as D's `viewer.html` byte for byte (three hrefs aside) under
`static/pose-studio/` (CONVENTIONS.md §1 decision 3, §3): 27,561,425 bytes, a
hand-written WebGL2 renderer with 146 character parts and 2 garment parts (74,880 and
11,948 triangles, D `models/biscuit/qa/viewer-package.json`), every texture and the
geometry inlined as base64 and JSON, no dependency, no fetch. It works, it is offline, and
it costs 26 MB of history on every rebuild (CONVENTIONS.md §11, first risk) and a 26 MB
download on every visit. It also wears its own palette — `#ede7de` ground, `#aa353b`
rule, a skewed `h1` (D `src/viewer.template.html` line 7) — which is a cream page inside
a dark platform, and reads no `data-theme`, no `data-animations` and no token.

Decision 0008 in the studio's record ("The viewer is embedded as-is", S05) says what would
reopen it: a maintained viewer that loads the GLB. This ticket is that. It also needs C01,
because a viewer that draws Biscuit inside the platform's chrome is her fuller register
on a Biscuit Games page, and until the hub permits renders from the model that page is
showing something the hub's rule refuses.

The reference implementation, all under D
`/Users/scutting/.supacode/repos/biscuit_pics/very_nice_three_deeez/models/biscuit/` at
`1d9d358` (read-only; the studio's copies live under `assets/models/biscuit/src/` after
S02, byte-identical):

| File | Bytes | What it holds |
| --- | --- | --- |
| `src/pose_math.js` | 5,411 | dependency-free pose math: quaternions `w,x,y,z`, column-major matrices, `fromControls(spec, values, name, base)`, `validate(spec, doc)`, `corrections(spec, bones)`, `matrices(rig, doc)` |
| `src/pose_viewer.js` | 8,395 | the UI: slider groups from `rig.controls`, presets, CPU skinning in `deformBuffer` (4 joints per vertex, 5 morph deltas), `reframe`, `importPose` / `exportPose`, spin, view buttons |
| `src/viewer.template.html` | 23,987 | the shell and the two GLSL ES 3.00 shaders (lines 55-63): passes `0` colour, `1` inverted-hull contour (`gl.cullFace(gl.FRONT)`, line 118), `2` clay, `3` wireframe; uniforms `colorMap`, `normalMap`, `roughMap`, `aoMap`, `tint`, `solid`, `dark`, `middle`, `light` (a three-band toon ramp per batch), `normalStrength` (`.18` on the face, `.32` elsewhere, line 114) |
| `src/pose_io.py` | 7,307 | the same format and validation on the Blender side; `MODEL_ID = "biscuit-miami-soft-charm-poseable"`, `RIG_VERSION = 1` |
| `model/rig.json` | 68,951 | `modelId`, `rigVersion`, `coordinateSystem` ("right-handed Z-up, -Y forward, +X Biscuit left"), `bones` (33: `name`, `head`, `tail`, `parent`, `restWorld`, `inverseBind`, `restLocal`, `restRotation`), `controls` (id, label, group, min, max, step, unit, targets with bone, axis, factor), `correctives` (5: name, bone, threshold, range) |
| `poses/*.json` | 4 × ~9 KB | `format: "biscuit-pose"`, `version: 1`, `modelId`, `rigVersion`, `name`, `bones` (33 transforms of `location`, `rotation`, `scale`), `controls`, `correctives`, `viewer` (yaw, pitch, zoom, frame, display, surface, contours) |
| `model/biscuit-poseable.glb` | 16,112,380 | the skinned standing rig with weights, PBR textures and the five sweater morph targets; served at `static/pose-studio/model/biscuit-poseable.glb` |
| `README.md` line 44 | | "the portable GLB uses standard PBR materials, so lighting and outlines can look different in other viewers" — the cel look is in the shaders, not in the file |

three.js: `three` and `@types/three` were both `0.186.0` on npm on 2026-09-23; the
executing agent re-reads `npm view three version` and pins exactly what it finds, with
`@types/three` at the same version.

The platform's obligations the new viewer must meet, which the old one does not: H
`docs/specs/operation.allium` — `EveryControlIsAComfortableTarget` (line 133; 44 px
across, from `config.minimum_touch_target`), `DeliberateZoomIsNeverTakenAway` (126; no
`touch-action: none` on the page, no `user-scalable=no`), `FullyKeyboardOperable` (220),
`FocusIsVisibleWhereverItLands` (227), `EveryPromiseHereHoldsAtTheNarrowestWidth` (247;
320 px) — and H `docs/specs/appearance.allium` — `ReducedMotionOverridesTheAnimationSetting`
(140; auto-rotate runs only while the document carries `data-animations="on"`, which
`src/lib/appearance.ts` derives from the port), `EveryCombinationMeetsTheLegibilityFloor`
(159; every control the viewer draws is a platform control or is measured), and
`AppearanceNeverCarriesMeaningAlone` (152). The studio's `accessibility-review` skill
(CONVENTIONS.md §7) already lists the three viewer checks.

Read first: CONVENTIONS.md §1 (decisions 3 and 10), §2.7, §3, §7, §11; the seven D files
above; the studio's `docs/decisions/0008-the-viewer-is-embedded-as-is.md`,
`0006-sources-in-lfs-served-files-as-blobs.md` and `0009-no-component-workshop-yet.md`;
`src/routes/model/+page.svelte` and `tests/pages.test.ts` as S03 left them; H
`docs/explanation/accessibility.md`; H `src/lib/components/Button.svelte` and
`SegmentedControl.svelte` (the controls the viewer's buttons and mode switches are built
from, through the package).

## Goal

- A pose viewer rendered by three.js inside the studio's shell on the model page, loading
  the GLB, driving the 33 bones and 5 morph targets from the same `biscuit-pose` JSON the
  Blender panel reads and writes, with the four presets, the slider groups, orbit, zoom,
  the framing and display modes, open and save pose, and save PNG.
- A cel look that a reviewer holding the old viewer beside it accepts as the same
  character: three-band toon ramp per material, inverted-hull contours in the ink colour,
  normal and occlusion maps applied, no specular gloss. The exact match is not the goal;
  the approved appearance is (`README.md` line 44).
- Every control a platform control or measured to the floor; auto-rotate honours
  `data-animations`; the canvas ground and ink follow the platform's tokens in all four
  theme and contrast combinations.
- `static/pose-studio/viewer.html` removed from the tree, its manifest entry gone, the
  two decision records marked, and the model page's link replaced by the component.
- The coverage floor intact: everything under `src/lib/` tested, and the WebGL surface
  kept where jsdom cannot reach it and the glob does not measure it.

## Non-goals

- Installing Storybook or Chromatic. Decision 0009's reopener is recorded in Open points,
  not acted on.
- Exporting a posed GLB in the browser (Blender's `export_pose_glb.py` remains the route).
- Animation, cloth, a face rig: D `README.md` lines 57-59 say the rig is for still posing
  and this ticket does not extend it.
- Changing the pose format, `rig.json` or the GLB. A viewer that needs a rebuilt GLB is a
  rebuild ticket first.
- Removing `assets/models/biscuit/src/pose_viewer.js` or `viewer.template.html`: they
  are the model package's build sources and stay under the manifest.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `package.json`, `package-lock.json` | repo (no lane; this runs after every lane) | S00's | `three` and `@types/three` added at exact pins |
| `src/lib/pose/format.ts` | repo | new; port of `pose_math.js` `validate`, `fromControls`, `corrections`, and the JSON types | pure, tested to the floor |
| `src/lib/pose/state.ts` | repo | new | the viewer's state machine: current pose, slider values, custom base, view state, preset selection, the reducer the controls call; no DOM, no three |
| `src/lib/pose/skinning.ts` | repo | new; port of `matrices(rig, doc)` | bone matrices from a pose and `rig.json`, as `Float32Array`s three.js can take; tested against `poses/*.json` and `qa/native-samples.json` (a sample of expected vertex positions, LFS, read in the test through the pointer only if present — see Open points) |
| `src/lib/pose/rig.ts` | repo | new | `rig.json` imported as a typed module and the `RIG` constant |
| `src/routes/model/PoseStudio.svelte` | repo | new; outside the coverage glob by design | the canvas component: three.js scene, `GLTFLoader`, materials, orbit, resize, WebGL-lost fallback |
| `src/routes/model/PoseControls.svelte` | repo | new; outside the glob | the sliders, presets and mode switches, built from the package's `Button`, `SegmentedControl`, `Input` (range) and `Notice`, driving `state.ts` |
| `src/routes/model/+page.svelte` | repo | S03's page | mounts the two components; the "Open the pose studio" link goes |
| `tests/pose-format.test.ts`, `tests/pose-state.test.ts`, `tests/pose-skinning.test.ts` | repo | new | to the floor |
| `tests/pages.test.ts` | repo | S03's | the model page assertions updated: the controls render in jsdom, the canvas component renders its fallback when `WebGL2RenderingContext` is absent |
| `static/pose-studio/viewer.html` | repo | S02's | deleted |
| `static/pose-studio/README.md`-shaped hrefs | | | none: the three rewritten hrefs die with the file |
| `assets/manifest.json` | repo | S02's | the viewer's entry removed by `just assets-manifest`; every other entry unchanged |
| `docs/decisions/0008-the-viewer-is-embedded-as-is.md` | repo | S05's | a **carried out on** mark beside the paragraph that named this ticket |
| `docs/decisions/0006-sources-in-lfs-served-files-as-blobs.md` | repo | S05's | the viewer row in its table marked the same way |
| `docs/explanation/large-files.md` | repo | S06's | the "26 MB on every rebuild" paragraph rewritten to past tense |
| `docs/how-to/rebuild-the-model.md` | repo | S05's | the `viewer.py` step marked as no longer needed for the site (still part of the package) |
| `docs/reference/testing.md` | repo | S06's | the section on what jsdom cannot run, and where the canvas components sit |
| `.agents/skills/accessibility-review/SKILL.md` and its two bridges | repo | S00's | the viewer step gains the three.js specifics |
| `CHANGELOG.md` | repo | S08's | an Unreleased entry: MINOR (a page changed what it shows; a 26 MB file left) |
| `tickets/C03-threejs-viewer.md` | tickets | this file | `status: done` |

## Steps

1. **Read the reference twice**: `pose_math.js` for the maths and the validation rules
   (every `throw` message is a rule the port keeps word for word, so a pose file that the
   Blender panel refuses is refused here with the same sentence), and
   `viewer.template.html` lines 55-63 and 111-118 for the render passes and the uniforms.
   Write down, in the hand-back notes, the toon ramp's three bands per batch
   (`b.bands`), the tint and solid colours, and the two `normalStrength` values, because
   those are what the three.js materials reproduce.

2. **Pin three.js.** `npm view three version`; add `three` and `@types/three` at that
   exact version to `dependencies` and `devDependencies` respectively; `just lock`. Read
   the lockfile diff.

3. **Port the pure half first** (`src/lib/pose/`), test-first: `format.ts` from
   `validate` and `fromControls` (the quaternion convention is `w,x,y,z`; the axis
   rotation is `value * factor * π / 360`, `pose_math.js` line 22; `height` moves
   `root.location[1]`), `skinning.ts` from `matrices` (column-major; `restLocal`,
   `inverseBind`), and `state.ts` as a reducer over the actions the old UI performed
   (`selectPreset`, `setControl`, `resetControl`, `openPose`, `setView`, `setDisplay`,
   `setSurface`, `toggleContours`, `toggleSpin`). Every test reads `rig.json` and the four
   `poses/*.json` from `assets/models/biscuit/` by relative import; the three files carry
   the coverage floor for `src/lib/**` and reach it before any canvas exists.

4. **Prove the maths against Blender.** `qa/native-samples.json` (2,525,893 bytes, LFS)
   holds sampled vertex positions from the native build. Write
   `tests/pose-skinning.test.ts` so that, when the file is a real JSON (LFS fetched), it
   asserts a sample of positions within `0.002` (the tolerance `pose_io.py` uses), and
   when it is a pointer (CI, `lfs: false`) it asserts the pointer's `oid` matches the
   manifest and skips the numeric case with a named `it.skip` reason. The floor is
   unaffected either way. Record the exact sample size and tolerance used.

5. **Build the canvas component** (`src/routes/model/PoseStudio.svelte`): `GLTFLoader`
   from `three/addons`, load `${base}/pose-studio/model/biscuit-poseable.glb`, find the
   `SkinnedMesh`es and their `skeleton.bones` by name against `RIG`, replace each
   `MeshStandardMaterial` with a `MeshToonMaterial` carrying the band ramp as a
   `gradientMap` (three bands, `NearestFilter`), the colour, normal and AO maps carried
   over, `roughnessMap` dropped (no gloss); an inverted-hull outline as a second mesh per
   part with `BackSide` and a solid ink material, scaled by the contour width the old
   shader used; morph target influences set from `correctives`; bone quaternions and
   positions set from the pose's transforms each frame the state changes. Orbit by
   pointer drag and by the arrow keys with the canvas focusable (`tabindex="0"`, a visible
   focus ring in the platform's `--focus`), zoom by wheel and `+`/`-`, `Home` resets,
   `Space` toggles spin. The ground colour is `--background` and the ink `--text`, read
   through `getComputedStyle` on the element the page passes in (never `document`), and
   re-read on `data-theme` and `data-high-contrast` changes through a `MutationObserver`
   on that element. Spin runs only while the element carries `data-animations="on"`.
   `webglcontextlost` shows `pose-overview.jpg` with the pose name as alt text and a
   sentence; `WebGL2RenderingContext` absent at mount shows the same.

6. **Build the controls** (`PoseControls.svelte`) from the package's components so their
   targets, names and contrast are the platform's: presets as a `SegmentedControl`,
   sliders as labelled `Input` ranges with an `output` and a reset `Button`, display and
   surface as `SegmentedControl`s, contours and spin as `Switch`es, open and save pose and
   save PNG as `Button`s. Grouped in `<details>` as the old UI was, `Head` open by
   default. The page's layout keeps the controls beside the canvas above 60rem and below
   it under, and nothing scrolls sideways at 320 px.

7. **Mount on the model page**, delete `static/pose-studio/viewer.html`, run `just
   assets-manifest`, read the manifest diff (one entry removed and nothing else), run
   `just check-assets`.

8. **Review against the two specifications** with the `accessibility-review` skill:
   every button 44 px at 320 px; the canvas operable by keyboard; auto-rotate stopped
   with `data-animations` absent (set the fake port's `prefersReducedMotion` and assert
   the element loses the attribute; then assert the component's `spinning` state is
   false); the four combinations legible (the controls are platform components; the
   canvas ground is a token; the pose name and status line are `--text` on
   `--background`).

9. **Documents**: the two decision marks (the verb is **carried out on**, dated, beside
   the paragraph that stopped being true, H `docs/decisions/README.md` lines 65-69),
   `large-files.md`, `rebuild-the-model.md`, `testing.md`, the skill and its bridges,
   `CHANGELOG.md`. `just check-docs`, `just check-agents`, `just check`.

10. Set `status: done`. Commit. Pushing and the pull request are authorised separately.

## Acceptance criteria

- [ ] `three` and `@types/three` pinned exactly, at the same version, and `just
      lock-check` green.
- [ ] `tests/pose-format.test.ts` refuses every case `pose_math.js` `validate` refuses,
      with the same message text, and accepts all four presets.
- [ ] `tests/pose-skinning.test.ts` matches `native-samples.json` within `0.002` when the
      LFS object is present and skips by name when it is a pointer.
- [ ] `just frontend-coverage` is at or above 90 on all four figures with the three
      `src/lib/pose/` modules included.
- [ ] `static/pose-studio/viewer.html` is absent from the tree and from
      `assets/manifest.json`; `just check-assets` is green; `git ls-files static/` shows
      the GLB and the preview only.
- [ ] The model page renders the controls in jsdom and the fallback image when WebGL is
      absent (`tests/pages.test.ts`).
- [ ] With `data-animations` removed from the root, the component reports no spin.
- [ ] Every control on the model page is a platform component or measured at 44 px; the
      page does not scroll sideways at 320 px (measured in `just preview` at that width
      and recorded as a screenshot path in the hand-back notes).
- [ ] The two decision records carry a dated **carried out on** mark and nothing else
      changed in them.
- [ ] `just check` is green.

## Verification

```sh
just lock-check
just frontend-coverage
git ls-files static/pose-studio
just check-assets
grep -n 'carried out on' docs/decisions/0008-the-viewer-is-embedded-as-is.md docs/decisions/0006-sources-in-lfs-served-files-as-blobs.md
BASE_PATH=/biscuit_studio just frontend-build && ls -la build/pose-studio/
just check
```

Expected: green; all four figures at or above 90 with `src/lib/pose/*` listed; two
paths (`static/pose-studio/model/biscuit-poseable.glb`,
`static/pose-studio/previews/pose-overview.jpg`) and `.nojekyll`'s parent nothing else;
green; two lines; a `build/pose-studio/` holding `model/` and `previews/` and no
`viewer.html`; green.

## Hand-back notes

Filled in by the agent that executes this ticket.

- The three.js version pinned and the date it was read.
- The band colours, tints and contour width carried over, and how close the look is
  judged to be, with a side-by-side screenshot path under `ai_tmp/` (not committed).
- The sample size and tolerance in the skinning test, and whether the LFS case ran.
- The measured targets at 320 px and the screenshot path.
- Which open points below were settled.

## Open points

- **Split.** This ticket is L and its two halves are separable: C03a, the pure modules
  under `src/lib/pose/` with their tests and the reference maths proven against
  `native-samples.json`; C03b, the canvas and controls, the deletion and the documents.
  Recommend splitting on pickup, with C03a's branch merged first; the executing agent
  writes C03b as a ticket if it does.
- **A workshop.** The studio now authors two components of its own. Decision 0009's
  reopener is exactly this; whether Storybook and Chromatic come in (with the browser
  download, the `stories` job and the token that H, P and T carry) is the maintainer's
  call. Recommend: not with this ticket; a story for a WebGL component proves little that
  `just preview` does not, and the pure modules are the tested surface.
- **`native-samples.json` in the test run.** Reading an LFS object in a test means a
  contributor without the object gets a skipped case; whether the studio's CI should
  fetch that one object (`lfs: true` on the `frontend` job, 2.5 MB of bandwidth a run) to
  make the case a required one. Recommend: skip locally, fetch in CI, and say so in
  `testing.md`.
- **Save PNG.** The old viewer composited a cream background. With the ground now a
  token, the saved PNG is whatever theme the reader is in; whether the export should
  offer a fixed ground is a product question.
- **Thumbnails and previews.** The 22 preview renders under `assets/models/biscuit/previews/`
  were made by the old viewer and the native build; whether the studio regenerates them
  from the new viewer so the site and the package agree is a later rebuild ticket.
