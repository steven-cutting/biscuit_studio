# Biscuit — the approved model

**This directory is the canonical home of the approved Biscuit model in this repository.**
Start all new posing, renders, exports and model work from this version: Soft Charm face,
Full Soft ears, Longer Drape tail and fitted cream sweater, with the poseable rig, improved
hind-leg proportions, original broad cream cuffs and softly sculpted charcoal toe beans on
all four paws.

[Open the pose studio](../../../static/pose-studio/viewer.html) ·
[Toe bean close-ups](previews/toe-beans-review.jpg) ·
[Preview the poses](../../../static/pose-studio/previews/pose-overview.jpg) ·
[Blender scene](model/biscuit-poseable.blend) ·
[Skinned GLB](../../../static/pose-studio/model/biscuit-poseable.glb)

`model/biscuit-poseable.blend` is the editable native scene, stored in Git LFS. The GLB and
the offline studio are companion outputs of the same model and are served by the site, so
they live under `static/pose-studio/` rather than here. `model/rig.json`, `poses/`,
`textures/`, `src/` and `qa/` keep the rig, presets, assets, build tools and verification
records together.

Keep this path stable. Nothing under it is edited by hand: an import follows
`docs/how-to/import-an-asset.md`, a rebuild follows `docs/how-to/rebuild-the-model.md`, and
`assets/manifest.json` records every file's digest and source. Replace the contents here
only when the maintainer approves a new version.

## Provenance

Imported on 2026-09-26 from the `biscuit_pics` repository, worktree branch
`very_nice_three_deeez`, commit `891c44c7919d95e66cb10c0b4d2599c0a5e697d2`, path
`models/biscuit/`, replacing the import of 2026-09-23 from `1d9d358`. Every file is
byte-identical to that commit except this README and the viewer. Four of the viewer's
links were changed: its three links to files this repository does not serve were
rewritten to GitHub URLs, and its link to the toe bean comparison sheet was removed.
`assets/manifest.json` records the original digest as `source_sha256` and lists the four
changes under `patched`. The matched before / after comparison renders, `previews/comparison/`
and `previews/comparison.jpg`, were not imported.

In `biscuit_pics` this version was approved on 2026-09-26 and promoted from the toe bean
study, `biscuit_pics/generated/3d/miami-cinematic-toe-beans/`, at commit `80d1871`. The
native model, GLB, rig, textures and four presets are byte-identical to that approved
version.

Each paw has four rounded toe pads and a larger, gently lobed central pad: **20 pads
total**, in matte warm charcoal `#493F3C`. A shallow recess in each sole keeps the pads
within the original foot envelope. The original paw vertices, exterior faces, claws and
cream cuffs are preserved, along with all 144 other existing parts.

**This model uses rig version 2.** Rig-version-2 poses from the hindquarters study remain
compatible. Saved poses from the previous rig-version-1 standard, the one this repository
imported first, are rejected because its rear joints had different rest positions; the
archived rig-version-1 package is
`biscuit_pics/generated/3d/miami-cinematic-poseable-rig-v1/`. The pose JSON schema remains
version 1.

The build reads the previous hindquarters standard,
`biscuit_pics/generated/3d/miami-cinematic-hindquarters-refined/`, as an immutable input,
and the `miami-cinematic-eyes-refined` helpers it was made from. Those, and the chain of
earlier studies the helpers read without writing —
`miami-cinematic-eyes-refined` → `miami-cinematic-sweater-foreleg-refined` →
`miami-cinematic-tail-drape-studies` (variant D3) → `ear-profile-studies` → `ear-studies`
→ `cinematic-studies` → `miami-angular-base`, plus the studio camera frames `src/viewer.py`
reads from `miami-cinematic-sweater-foreleg-refined/qa/viewer-package.json` — stay in
`biscuit_pics` under `biscuit_pics/generated/3d/` and are not in this repository. The
finished `.blend`, `.glb` and offline viewer work on their own; rebuilding needs that
checkout, and `scripts/rebuild_model.sh` says how it is reached.

## Pose her in the browser

1. Open `static/pose-studio/viewer.html` in a browser with WebGL 2 — on the published site
   it is the pose studio the model page links to. It works offline, without a server or
   installation.
2. Choose **Standing**, **Sitting**, **Lying down** or **Paw raised**.
3. Expand a control group to adjust her body, head, legs, paws, ears or tail. L/R refer to
   Biscuit's left and right. Each slider has its own reset button.
4. Drag the model to orbit and scroll to zoom. **View & appearance** includes front, side
   and overhead views, close-ups, and dressed / Biscuit only / sweater only displays.
5. **Save pose** downloads a JSON file. **Open pose** restores it, including the view.
   **Save PNG** downloads the current canvas view with a cream background. Save before
   closing the page; poses are not stored automatically.

Keyboard: Tab selects controls; arrow keys adjust a focused slider. On the canvas, arrow
keys orbit, +/− zoom, Home restores the view, and Space toggles rotation. On a phone, the
controls appear below the model.

To see all four soles, choose **Below** in **View & appearance**. For a presented paw,
choose **Paw raised**, set **Left front leg → Paw angle** to **−25°**, then select
**Front**. You can also open the supplied
[toe bean review pose](qa/toe-bean-review-pose.json), which adds a slight head tilt.

## Pose her in Blender

Open `model/biscuit-poseable.blend` (a clone made without git-lfs sees a pointer file
here instead; `docs/how-to/develop-locally.md` says how to fetch it). The scene starts in
the approved standing pose with `Biscuit.Rig` selected and all textures packed.

Textures are packed and their relative paths point to this package's `textures/`
directory. The approved scene has been preserved byte for byte.

To enable the pose panel, open Blender's **Scripting** workspace, choose the embedded text
**blender_pose_tools.py**, and press **Run Script**. Return to the 3D viewport, press
**N**, and open the **Biscuit** tab. No add-on installation is needed; run the text again
when opening a new Blender session.

- The panel supplies the same four presets plus **Open pose** / **Save pose**.
- Select the rig and enter **Pose Mode**. Rotate bones for the back, neck, head,
  individual leg joints, three sections of each ear, and seven tail sections. Move `root`
  to place the whole character.
- Optional paw targets: click a **Front L/R** or **Hind L/R** button in the panel to match
  and enable that paw's IK. Move `CTRL.front.paw.L`, for example; its corresponding
  `CTRL.front.bend.L` controls the bend direction. Rotate the paw bone separately to
  orient the foot.
- Presets and opened pose files switch IK off and restore explicit joint transforms.
  **Save pose** captures the evaluated IK result, so a pose made with paw targets also
  opens correctly in the browser.

The browser sliders are relative adjustments when a Blender pose is opened. **Reset to
standing** returns to the original controls. Pose JSON files are shared between these
tools; they are not general Blender scenes or animation files.

## Portable model and saved poses

`static/pose-studio/model/biscuit-poseable.glb` contains the standing rig, mesh weights,
textures and sweater corrective shape keys. It can be imported into Blender or another
application supporting glTF skinning and morph targets. The native Blender materials and
browser preview use the approved illustrated shading; the portable GLB uses standard PBR
materials, so lighting and outlines can look different in other viewers.

To create a skinned GLB in a saved pose while preserving the matching sweater corrections,
run this command from this directory, replacing the two example file paths:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 \
  --python src/export_pose_glb.py -- /path/to/saved-pose.json /path/to/posed-biscuit.glb
```

On other systems, replace the Blender executable path. The exporter keeps the neutral GLB
intact and stores the pose in the new file. Applications that manipulate the raw GLB's
joints themselves should also update the five sweater morph weights according to
`model/rig.json`; glTF does not carry Blender's live corrective drivers.

## What the rig covers

There are 33 deform bones, with four optional paw targets and four bend controls in
Blender. Every character part, eye, fur detail, paw cuff and native contour follows its
assigned bones. All 20 pads follow their existing paw bones with full weight. The sweater
uses the same skeleton and five driven corrections for the shoulders, hips and belly. The
collar follows the lower neck and chest.

This is a rig for still posing. The four supplied poses are checked from multiple views,
dressed and undressed. Arbitrary extreme combinations can still need manual joint or
garment adjustments. There is no cloth simulation, facial-expression rig, automatic ground
contact or walk-cycle animation.

**Inherited floor-contact limitation:** the sitting preset places the front paws
approximately `0.0515` model units below the floor. The toe bean model preserves that
preset exactly and adds no further penetration. Standing pads meet the floor.

## Rebuild and verification

The build reads the archived rig-version-2 model in
`biscuit_pics/generated/3d/miami-cinematic-hindquarters-refined/` from a `biscuit_pics`
checkout and never writes to it; it adds the sole recesses and pads once, starting from
that immutable input. `src/common.py` and `src/viewer.py` find that checkout by searching
the directories above this package, so `scripts/rebuild_model.sh` places a gitignored link
at `assets/biscuit_pics` pointing at the checkout you give it. Rebuilding requires Blender
(verified with 5.2.1), Python 3 and Pillow, and replaces the generated files in this
package and under `static/pose-studio/`; keep design experiments elsewhere and promote a
replacement here only after the maintainer approves it.

```sh
just model-rebuild /path/to/biscuit_pics
```

That runs, from this directory, the six commands the package's own tooling expects —
`src/build.py`, `src/verify.py`, `src/verify_anatomy.py` and `src/render.py` under
Blender, `src/viewer.py` and `src/proof_sheet.py` under Python — then deletes the
comparison renders this repository does not keep, moves the viewer, the GLB and the
overview image to `static/pose-studio/`, re-applies the viewer's four link changes, and
rewrites `assets/manifest.json`. Read the manifest diff before committing.

`src/verify_browser.mjs` connects to an isolated Chrome remote-debugging profile supplied as
its argument. It checks native/browser deformation agreement, offline operation,
desktop/mobile controls, saved JSON and PNG downloads, and invalid pose rejection.
`src/verify_interchange.py` reopens browser poses in Blender and compares independently
evaluated and Blender-reimported posed GLBs with the native surfaces. Run it after the
browser checks have created `qa/browser-saved-pose.json`. Neither is part of
`just model-rebuild`.

Reports are in `qa/native-verification.json`, `qa/browser-verification.json` and
`qa/interchange-verification.json`. Native renders are in `previews/native/`; browser views
are in `previews/`, and the overview sheet is `static/pose-studio/previews/pose-overview.jpg`.

The [style report](qa/style-verification.json) checks all 144 protected parts, the
preserved paw exteriors and unchanged rig-version-2 specification, rest bones and
controls. The [pad report](qa/pad-verification.json) checks the 20 closed pad meshes, their
attachments, separation and floor contact relative to the source. The
[anatomy report](qa/anatomy-verification.json) covers the inherited rear-joint layout and
hind-paw contact. Browser checks cover the four presets, an articulated pose and eight
individual paw rotations. [Promotion details](qa/promotion.json) record the source commit
and hashes of all 47 copied model, pose and texture assets.
