---
id: S02
title: "Asset import: the approved model and the cel set from biscuit_pics, LFS, the manifest"
status: done
depends_on: [S00]
parallel_with: [S01, S03, S04, S05, S06]
branch: ticket/s02-asset-import
estimated_size: L
---

# S02: Asset import: the approved model and the cel set from biscuit_pics, LFS, the manifest

## Context

The approved Biscuit model and the eleven cel illustrations live today in D, the
`biscuit_pics` worktree at `/Users/scutting/.supacode/repos/biscuit_pics/very_nice_three_deeez`,
commit `1d9d358` (full hash `1d9d3580f2037826feb6e05f39f5a777b52db86c`). CONVENTIONS.md §1
decision 8 says exactly what comes across: `models/biscuit/` whole (94 files, 92 MB) and
`good/` (11 PNG files, 14 MB), and nothing else. Decision 4 says how it is stored — fresh
history, three files in LFS, everything the site serves as an ordinary blob — and §3 is
the policy in full. Decision 9 is the rule this ticket restates and never tests: **no
ticket copies a photograph of the real dog. If one is ever copied, the maintainer approves
it first, one photograph at a time, and it is committed only after every metadata field
has been stripped from it; `just check-assets` refuses any image carrying a GPS or
camera-identifying EXIF field regardless of approval.** D `biscuit_pics/raw/` holds 163
such photographs and none of them is in scope.

S00 has already landed the machinery this ticket fills: `.gitattributes` with the LFS and
binary patterns (§3), the one exclusion set in six files (§2.1), `scripts/check_assets.py`
with its `check`, `write` and `self-test` subcommands (§4), the `check-assets`,
`assets-manifest` and `model-rebuild` recipes (§2.2), an empty `assets/manifest.json`, and
a two-line stub `scripts/rebuild_model.sh` that exits 2. This ticket puts the files in,
fills the manifest, replaces the stub, and proves the gate stays green with a 26 MB file in
the tree.

Three facts from CONVENTIONS.md §1 decide the layout:

- **Fact 10.** The viewer links `model/biscuit-poseable.blend` (twice),
  `model/biscuit-poseable.glb` (once), `previews/pose-overview.jpg` (three times) and
  `README.md` (once), all relative to itself, and fetches nothing else. The GLB and the
  overview image are therefore placed beside the viewer under `static/pose-studio/` so
  the served page's links resolve; the `.blend` and the README are not served (LFS; under
  `assets/`), so those three `href` values are rewritten to GitHub blob URLs. §3 gives the
  values. Consequence: `pose-overview.jpg` lives **only** at
  `static/pose-studio/previews/pose-overview.jpg`, not under
  `assets/models/biscuit/previews/`, because one copy is enough and the viewer's link is
  what fixes where it goes.
- **Fact 8.** The three large files are byte-identified by sha256 at `1d9d358`; this
  ticket asserts them before the copy, after the copy, and (for the two unpatched ones)
  after `git add`.
- **Fact 9.** No image in scope carries EXIF. The sweep in step 6 confirms it on the
  copied files, so the GPS refusal in `check_assets.py` has nothing to refuse today and is
  proved live only by its `self-test`.

The rebuild is out of scope, but the script that would run it is not. D
`models/biscuit/README.md` lines 61-78 give the five-command sequence and say the build
"reads the historical eyes-refined model under `biscuit_pics/generated/3d/`". Read D
`models/biscuit/src/common.py` (32 lines) and `src/viewer.py` (23 lines) before writing
the script: both compute `ROOT = Path(__file__).resolve().parents[1]` (the package
directory) and `REPO_ROOT = ROOT.parents[1]`, then reach
`REPO_ROOT / 'biscuit_pics/generated/3d/…'`. In D, `REPO_ROOT` is the worktree root. In
this repository the package sits at `assets/models/biscuit/`, so `REPO_ROOT` resolves to
`assets/`, and the studies would be looked for at `assets/biscuit_pics/generated/3d/…`.
The scripts are copied verbatim and never edited (§2: excluded from every linter, D's
own build tooling), so the script this ticket writes bridges the path from outside
(step 8). `viewer.py` also writes `ROOT/viewer.html` and `ROOT/qa/viewer-package.json`;
`build.py` writes `ROOT/model/biscuit-poseable.blend` and `ROOT/model/biscuit-poseable.glb`;
`render.py` writes `ROOT/previews/native/`; `proof_sheet.py` writes
`ROOT/previews/pose-overview.jpg`. Three of those outputs belong under
`static/pose-studio/` here, so the script moves them and re-applies the three `href`
rewrites after every rebuild.

Read first: CONVENTIONS.md §0, §1 (decisions 4, 8, 9; facts 4, 5, 8, 9, 10), §2 (the rows
owned by S02, and §2.1), §3, §4, §5, §9 ("D is read-only"), §10 (the two claims assigned
to S02), §11. In D: `README.md` (root, 18 lines), `models/biscuit/README.md` (78 lines),
`models/biscuit/src/common.py`, `models/biscuit/src/viewer.py`,
`models/biscuit/qa/viewer-package.json` (which records the viewer's own sha256 and byte
count: `8838e723…` and 27,561,425). In this repository: `.gitattributes`,
`scripts/check_assets.py`, the `assets` and `model` sections of `Justfile`,
`docs/reference/asset-manifest.md` if S06 has landed (it is a stub otherwise; §4 is the
contract either way).

## Goal

At the end of this ticket, on branch `ticket/s02-asset-import`:

- Every file in the copy list below exists at its destination, byte-identical to D at
  `1d9d358` except `static/pose-studio/viewer.html`, which differs from D in exactly three
  attribute values.
- `git lfs ls-files` lists exactly three files: the `.blend`, `qa/geometry/rigged.json`
  and `qa/native-samples.json`; every other asset is an ordinary blob.
- `assets/manifest.json` holds one entry per file under `assets/` and
  `static/pose-studio/` (105 entries), every `source` names `biscuit_pics@1d9d358:<D path>`,
  every `licence` is `unsettled`, and the viewer's entry carries `source_sha256` and the
  three-item `patched` list.
- `just check-assets` is green; `just lint` is green with the real files in the tree,
  which settles the §10 claim that the prek `exclude` alone keeps the hooks off them.
- `scripts/rebuild_model.sh` is the real script, shellcheck-clean, committed `100755`,
  and exits 2 with a usage line when run without its argument.
- `assets/models/biscuit/README.md` is D's README adapted, with a Provenance section, and
  lychee resolves every relative link in it offline.
- `just check` is green.

## Non-goals

- **Any photograph of the real dog.** Decision 9 above. Nothing under D
  `biscuit_pics/raw/` is read by this ticket, and the EXIF sweep in step 6 runs over the
  copied files only.
- Anything under D `inspiration/`, `model_sheets/`, `biscuit_pics/generated/` or
  `ai_tmp/` (decision 8, §5).
- Running the rebuild. `scripts/rebuild_model.sh` is written and checked for shape; the
  rebuild it describes needs Blender, a `biscuit_pics` checkout and about a minute of
  headless rendering, and it is `docs/how-to/rebuild-the-model.md`'s (S05) to document
  and a later change's to run.
- Any page under `docs/` (S05, S06), any route or component (S01, S03), the workflows
  (S04).
- `Justfile`, `pyproject.toml`, `.gitattributes`, `scripts/check_assets.py`: §9 lists
  them as files no lane touches. A defect found in `check_assets.py` while running it is
  handed back as an S00 follow-up with the failing command quoted, not fixed here.
- Editing anything in D. `cp`, `shasum` and `git -C <D> rev-parse` are the only commands
  that touch it.
- Deciding the licence of the assets (§5, open). Every `licence` field is written as
  `unsettled`.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `assets/manifest.json` | S02 | `just assets-manifest`, then hand-edited `source`, `licence`, `source_sha256`, `patched` | S00's empty manifest replaced by 105 entries |
| `assets/models/biscuit/README.md` | S02 | D `models/biscuit/README.md`, adapted (step 7) | new |
| `assets/models/biscuit/model/biscuit-poseable.blend` | S02 | D, LFS | new |
| `assets/models/biscuit/model/rig.json` | S02 | D | new |
| `assets/models/biscuit/poses/{lying,paw-raised,sitting,standing}.json` | S02 | D | new, 4 files |
| `assets/models/biscuit/previews/*.png` and `previews/native/*.png` | S02 | D | new, 21 files (every preview except `pose-overview.jpg`) |
| `assets/models/biscuit/qa/**` | S02 | D; `geometry/rigged.json` and `native-samples.json` LFS | new, 10 files |
| `assets/models/biscuit/src/**` | S02 | D verbatim, never edited | new, 15 files |
| `assets/models/biscuit/textures/*.png` | S02 | D | new, 36 files |
| `assets/illustrations/good/*.png` | S02 | D `good/` | new, 11 files |
| `static/pose-studio/viewer.html` | S02 | D `models/biscuit/viewer.html`, three hrefs rewritten (step 5) | new |
| `static/pose-studio/model/biscuit-poseable.glb` | S02 | D, byte-identical | new |
| `static/pose-studio/previews/pose-overview.jpg` | S02 | D, byte-identical | new |
| `scripts/rebuild_model.sh` | S02 | step 8 (embedded) | S00's stub replaced; mode `100755` |
| `tickets/S02-asset-import.md` | ticket | this file | `status:` line, hand-back notes |

The table is the whole scope. Nothing outside it is edited.

### The copy list

Every path is relative to D on the left and to this repository on the right; bytes are
D's at `1d9d358`, read with `stat -f %z`. Storage is `lfs` where §3's `.gitattributes`
patterns match and `blob` otherwise.

`models/biscuit/` root and `model/`:

| D path | Bytes | Destination | Storage |
| --- | --- | --- | --- |
| `models/biscuit/README.md` | 7,740 | `assets/models/biscuit/README.md` (adapted, step 7) | blob |
| `models/biscuit/viewer.html` | 27,561,425 | `static/pose-studio/viewer.html` (patched, step 5) | blob |
| `models/biscuit/model/biscuit-poseable.blend` | 12,004,899 | `assets/models/biscuit/model/biscuit-poseable.blend` | lfs |
| `models/biscuit/model/biscuit-poseable.glb` | 16,112,380 | `static/pose-studio/model/biscuit-poseable.glb` | blob |
| `models/biscuit/model/rig.json` | 68,951 | `assets/models/biscuit/model/rig.json` | blob |

`models/biscuit/poses/` → `assets/models/biscuit/poses/`, all blob: `lying.json` 9,610;
`paw-raised.json` 8,900; `sitting.json` 9,881; `standing.json` 8,603.

`models/biscuit/previews/` → `assets/models/biscuit/previews/`, all blob, except the one
starred file, which goes to `static/pose-studio/previews/pose-overview.jpg`:
`lying-front.png` 353,608; `lying-hero.png` 387,246; `lying-left.png` 373,219;
`lying-undressed.png` 354,167; `native/lying.png` 641,350; `native/paw-raised.png` 621,618;
`native/sitting.png` 562,809; `native/standing.png` 592,344; `paw-raised-front.png`
404,152; `paw-raised-hero.png` 420,137; `paw-raised-left.png` 416,354;
`paw-raised-undressed.png` 403,725; **`pose-overview.jpg` 398,799 (starred)**;
`sitting-front.png` 406,885; `sitting-hero.png` 428,395; `sitting-left.png` 399,479;
`sitting-undressed.png` 408,173; `standing-front.png` 396,501; `standing-hero.png`
434,773; `standing-left.png` 405,842; `standing-undressed.png` 396,272;
`studio-desktop.png` 523,412; `studio-mobile.png` 424,485.

`models/biscuit/qa/` → `assets/models/biscuit/qa/`: `blender-ik-pose.json` 12,252 blob;
`browser-saved-pose.json` 9,830 blob; `browser-verification.json` 821 blob;
`geometry/rigged.json` 17,750,241 **lfs**; `interchange-verification.json` 1,136 blob;
`invalid-poses.json` 88,953 blob; `native-samples.json` 2,525,893 **lfs**;
`native-verification.json` 479 blob; `source-state.json` 51,552 blob;
`viewer-package.json` 341 blob.

`models/biscuit/src/` → `assets/models/biscuit/src/`, all blob, verbatim:
`blender_pose_tools.py` 5,737; `browser_test_utils.mjs` 3,235; `build.py` 7,898;
`common.py` 1,118; `export_pose_glb.py` 4,654; `pose_io.py` 7,307; `pose_math.js` 5,411;
`pose_viewer.js` 8,395; `proof_sheet.py` 2,182; `render.py` 2,592; `rig.py` 16,437;
`verify_browser.mjs` 6,353; `verify_interchange.py` 6,886; `verify.py` 8,601;
`viewer.py` 1,720; `viewer.template.html` 23,987.

`models/biscuit/textures/` → `assets/models/biscuit/textures/`, all blob, 36 files:
`coat-color.png` 741,177; `coat-normal.png` 723,594; `coat-occlusion.png` 27,994;
`coat-roughness.png` 86,095; `cream-color.png` 2,288,330; `cream-normal.png` 1,393,074;
`cream-occlusion.png` 56,501; `cream-roughness.png` 85,395; `ear-wave-color.png` 422,470;
`ear-wave-normal.png` 639,890; `ear-wave-occlusion.png` 28,441; `ear-wave-roughness.png`
45,512; `eye-color.png` 366,870; `eye-normal.png` 4,544; `eye-occlusion.png` 2,385;
`eye-roughness.png` 2,386; `face-B-color.png` 815,430; `face-B-normal.png` 774,311;
`face-B-occlusion.png` 25,640; `face-B-roughness.png` 7,806; `nose-color.png` 125,107;
`nose-normal.png` 813,587; `nose-occlusion.png` 2,385; `nose-roughness.png` 23,758;
`sweater-knit-color.png` 18,941; `sweater-knit-normal.png` 191,061;
`sweater-knit-occlusion.png` 15,961; `sweater-knit-roughness.png` 23,604;
`sweater-label-color.png` 9,415; `sweater-label-normal.png` 84,598;
`sweater-label-occlusion.png` 3,458; `sweater-label-roughness.png` 6,852;
`sweater-rib-color.png` 9,829; `sweater-rib-normal.png` 166,531;
`sweater-rib-occlusion.png` 2,385; `sweater-rib-roughness.png` 5,466.

`good/` → `assets/illustrations/good/`, all blob, 11 files: `cool-body.png` 869,681;
`cool-head.png` 1,361,047; `warm-body.png` 979,044;
`warm-head-bashful-blush-exaggerated.png` 1,527,884; `warm-head-bashful.png` 1,525,989;
`warm-head-chin-lifted.png` 1,462,047; `warm-head-eye-slant.png` 1,481,154;
`warm-head-looking-up.png` 1,424,974; `warm-head-sad.png` 1,478,921;
`warm-head-side-eye.png` 1,496,671; `warm-head.png` 1,530,312.

That is 94 files from `models/biscuit/` and 11 from `good/`: 105 destinations, 3 of them
LFS, 3 under `static/pose-studio/`, 102 under `assets/`. (The count includes the adapted
README; the D README is the source of it, not copied as-is.)

## Steps

Work from the repository root on branch `ticket/s02-asset-import`. `D` below is
`/Users/scutting/.supacode/repos/biscuit_pics/very_nice_three_deeez`; set it as a shell
variable rather than typing it. Nothing writes into `$D`.

### Step 1: Pin the source and assert the three digests

```sh
D=/Users/scutting/.supacode/repos/biscuit_pics/very_nice_three_deeez
git -C "$D" rev-parse HEAD
git -C "$D" status --short | wc -l
shasum -a 256 "$D/models/biscuit/viewer.html" "$D/models/biscuit/model/biscuit-poseable.glb" "$D/models/biscuit/model/biscuit-poseable.blend"
```

Expected: `1d9d3580f2037826feb6e05f39f5a777b52db86c`; `0` (a clean worktree); the three
digests of CONVENTIONS.md §1 fact 8 —
`8838e723399ee4e1eba5e9926da4503fe639459f1b809bc3bf9575856e55170a`,
`51d16c1826b2c3ad6ad85fcb176a73e0d1c7a0ac3665ad10f1b6700e9e9be716`,
`95d164730e9354ab3d9bd561a73180690bbb055fffa9bf230c735f735234b4c3`. If any differs, D
has moved since this ticket was written: stop, record the new HEAD and digests in the
hand-back notes, and ask the maintainer whether the newer state is the one to import.
Every later `source` field names the commit `rev-parse` printed.

Also confirm the attributes S00 landed, before anything is copied, because git decides
LFS at `git add` time from the patterns that exist then:

```sh
git check-attr filter assets/models/biscuit/model/biscuit-poseable.blend assets/models/biscuit/qa/geometry/rigged.json assets/models/biscuit/qa/native-samples.json static/pose-studio/model/biscuit-poseable.glb
git lfs env | head -3
```

Expected: the first three print `filter: lfs`, the fourth `filter: unspecified`; `git lfs
env` prints a version. A `filter: unspecified` on the `.blend` means `.gitattributes` is
not S00's or git-lfs is not installed; stop and hand back. **The order matters:** a file
added before its pattern exists is committed as a blob, and moving it into LFS afterwards
rewrites history. Nothing is `git add`ed until step 9.

### Step 2: Copy the model package into `assets/`

```sh
mkdir -p assets/models/biscuit assets/illustrations static/pose-studio/model static/pose-studio/previews
cp -R "$D/models/biscuit/model" "$D/models/biscuit/poses" "$D/models/biscuit/previews" "$D/models/biscuit/qa" "$D/models/biscuit/src" "$D/models/biscuit/textures" assets/models/biscuit/
```

Then move the two served files out of `assets/` and put the viewer beside them:

```sh
mv assets/models/biscuit/model/biscuit-poseable.glb static/pose-studio/model/biscuit-poseable.glb
mv assets/models/biscuit/previews/pose-overview.jpg static/pose-studio/previews/pose-overview.jpg
cp "$D/models/biscuit/viewer.html" static/pose-studio/viewer.html
```

`cp -R` on macOS preserves nothing that matters here (no symlinks exist in the package;
confirm with `find "$D/models/biscuit" -type l | wc -l`, expected `0`). The D README is
not copied; step 7 writes the adapted one.

### Step 3: Copy the cel set

```sh
cp -R "$D/good" assets/illustrations/good
find assets static/pose-studio -type f | wc -l
```

Expected: `105`: the 104 copied files plus `assets/manifest.json`, which S00 tracks; the
README step 7 writes is not there yet.

### Step 4: Assert the copy is byte-identical

```sh
shasum -a 256 static/pose-studio/viewer.html static/pose-studio/model/biscuit-poseable.glb assets/models/biscuit/model/biscuit-poseable.blend
cd "$D" && find models/biscuit good -type f ! -name README.md ! -name viewer.html ! -path '*/model/biscuit-poseable.glb' ! -name pose-overview.jpg -exec shasum -a 256 {} + | sed 's#  models/biscuit/#  assets/models/biscuit/#; s#  good/#  assets/illustrations/good/#' > /tmp/s02-expected.txt; cd -
shasum -a 256 -c /tmp/s02-expected.txt | grep -vc ': OK$'
```

Expected: the three fact-8 digests, unchanged; then `0` lines that are not `OK` (100
files checked). The viewer's digest changes in step 5, which is why it is asserted here
first. Use `ai_tmp/` rather than `/tmp` if the shell has `noclobber` set and the file
exists; nothing under `ai_tmp/` is committed.

### Step 5: Rewrite the three hrefs in the viewer

Before:

```sh
grep -o 'href="[^"]*"' static/pose-studio/viewer.html | sort | uniq -c
```

Expected, exactly: `2 href="model/biscuit-poseable.blend"`, `1 href="model/biscuit-poseable.glb"`,
`3 href="previews/pose-overview.jpg"`, `1 href="README.md"` (CONVENTIONS.md §1 fact 10).

The rewrite, byte-exact and touching nothing else (the file is 27 MB on one long line of
JSON; `sed -i` would work but a Python replace is easier to assert on):

```sh
uv run --frozen python - <<'EOF'
from pathlib import Path
p = Path("static/pose-studio/viewer.html")
s = p.read_bytes()
pairs = [
    (b'href="model/biscuit-poseable.blend"', b'href="https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/model/biscuit-poseable.blend"', 2),
    (b'href="README.md"', b'href="https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/README.md"', 1),
]
for old, new, n in pairs:
    assert s.count(old) == n, (old, s.count(old))
    s = s.replace(old, new)
p.write_bytes(s)
EOF
```

After:

```sh
grep -o 'href="[^"]*"' static/pose-studio/viewer.html | sort | uniq -c
shasum -a 256 static/pose-studio/viewer.html
```

Expected: `2 href="https://github.com/…/biscuit-poseable.blend"`, `1
href="model/biscuit-poseable.glb"`, `3 href="previews/pose-overview.jpg"`, `1
href="https://github.com/…/README.md"`, and no `href="model/biscuit-poseable.blend"` or
`href="README.md"` line; a new digest, which step 10 records as the manifest's `sha256`
while `source_sha256` keeps `8838e723…`. Record the new digest in the hand-back notes.

The three rewrites are the only difference between the served viewer and D's, and
`patched` in the manifest says so in words (step 10). The blob URLs name `main` and the
`assets/models/biscuit/` path; CONVENTIONS.md §11 records that a branch rename or a path
move breaks them inside a file no linter reads.

### Step 6: The EXIF sweep

Every copied image, through the same library `check_assets.py` uses:

```sh
uv run --frozen python - <<'EOF'
from pathlib import Path
from PIL import Image
paths = sorted(p for root in ("assets", "static/pose-studio") for p in Path(root).rglob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg"})
flagged = []
for p in paths:
    exif = Image.open(p).getexif()
    gps = exif.get_ifd(0x8825)
    if len(exif) or gps:
        flagged.append((str(p), dict(exif), dict(gps)))
print(len(paths), "images;", len(flagged), "with EXIF")
for f in flagged: print(f)
EOF
```

Expected: `69 images; 0 with EXIF` (36 under `assets/models/biscuit/textures`, 21 under
`assets/models/biscuit/previews`, 11 under `assets/illustrations/good`, 1 under
`static/pose-studio/previews`).
CONVENTIONS.md §1 fact 9 says this was already true in D on 2026-09-23; the sweep proves
it of the copies. A flagged file is not stripped here: stop and hand back, because
stripping is a change to a source and the maintainer decides. No `sips`, no `exiftool`:
Pillow is the one image library the toolchain pins, and the gate's checker reads EXIF the
same way.

### Step 7: `assets/models/biscuit/README.md`

Write the file below. It is D `models/biscuit/README.md` (78 lines) with every relative
link corrected to this repository's layout, the two links into
`biscuit_pics/generated/3d/…` turned into code spans naming the D path and commit, the
Blender command paths kept as D wrote them, and a Provenance section at the top. lychee
resolves the relative links offline in `just lint`; the README is outside `docs/`, so the
documentation contract does not register it and it carries no frontmatter.

````markdown
# Biscuit — the approved model

**This directory is the canonical home of the approved Biscuit model in this repository.**
Start all new posing, renders, exports and model work from this version: Soft Charm face,
Full Soft ears, Longer Drape tail and fitted cream sweater, with the poseable rig.

[Open the pose studio](../../../static/pose-studio/viewer.html) ·
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

Imported on 2026-09-23 from the `biscuit_pics` repository, worktree branch
`very_nice_three_deeez`, commit `1d9d3580f2037826feb6e05f39f5a777b52db86c`, path
`models/biscuit/`. Every file is byte-identical to that commit except the viewer, whose
three links to files this repository does not serve were rewritten to GitHub URLs;
`assets/manifest.json` records the original digest as `source_sha256` and lists the three
rewrites under `patched`.

In `biscuit_pics` the package had been moved intact from
`biscuit_pics/generated/3d/miami-cinematic-poseable/`, and its rig was built from the
`miami-cinematic-eyes-refined` model. That model, and the chain of earlier studies the
build reads without writing —
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

## Pose her in Blender

Open `model/biscuit-poseable.blend` (a clone made without git-lfs sees a pointer file
here instead; `docs/how-to/develop-locally.md` says how to fetch it). The scene starts in
the approved standing pose with `Biscuit.Rig` selected and all textures packed.

The embedded textures work independently of their stored source paths, which still name
the earlier study. If you unpack or relink textures for editing, use this package's
`textures/` directory. The approved scene has been preserved byte for byte.

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
assigned bones. The sweater uses the same skeleton and five driven corrections for the
shoulders, hips and belly. The collar follows the lower neck and chest.

This is a rig for still posing. The four supplied poses are checked from multiple views,
dressed and undressed. Arbitrary extreme combinations can still need manual joint or
garment adjustments. There is no cloth simulation, facial-expression rig, automatic ground
contact or walk-cycle animation.

## Rebuild and verification

The build reads the historical eyes-refined model from a `biscuit_pics` checkout and never
writes to it. `src/common.py` and `src/viewer.py` resolve that checkout two directories
above this package, so `scripts/rebuild_model.sh` places a gitignored link at
`assets/biscuit_pics` pointing at the checkout you give it. Rebuilding requires Blender
(verified with 5.2.1), Python 3 and Pillow, and replaces the generated files in this
package and under `static/pose-studio/`; keep design experiments elsewhere and promote a
replacement here only after the maintainer approves it.

```sh
just model-rebuild /path/to/biscuit_pics
```

That runs, from this directory, the five commands the package's own tooling expects —
`src/build.py` and `src/verify.py` and `src/render.py` under Blender, `src/viewer.py` and
`src/proof_sheet.py` under Python — then moves the viewer, the GLB and the overview image
to `static/pose-studio/`, re-applies the viewer's three link rewrites, and rewrites
`assets/manifest.json`. Read the manifest diff before committing.

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
````

The `docs/how-to/…` mentions are code spans, not links: those pages are S05's and may be
stubs when this ticket runs, and a link into `docs/` from outside it is not one the
contract checks.

### Step 8: `scripts/rebuild_model.sh`

Replace S00's stub with the script below, `chmod 755`, and confirm `git ls-files -s`
will show `100755` once added. It is written so that `docs/how-to/rebuild-the-model.md`
has a real procedure to document; it is not run beyond its argument check here.

**The path decision.** `common.py` line 10 and `viewer.py` line 6 compute `REPO_ROOT` as
the second parent of the package directory, which here is `assets/`. Three ways to bridge
it: edit the two scripts (refused: they are D's, verbatim, and excluded from the gate
precisely because they are not this repository's code), set an environment variable (the
scripts read none), or place a link at `assets/biscuit_pics` pointing at the checkout's
`biscuit_pics` directory so `assets/biscuit_pics/generated/3d/…` resolves. The link is the
one that changes no source, so the script makes it, gitignore covers it, and the script
removes it on exit. Read both scripts before accepting this; if either reaches a path this
reasoning misses, record the difference in the hand-back notes and adjust the link, not the
scripts.

```sh
#!/bin/sh
set -eu

# Rebuilds the approved model from its sources, then puts each output where this
# repository keeps it. Needs Blender and a checkout of biscuit_pics holding the
# study chain assets/models/biscuit/README.md names. Never part of `just check`.
#
#   scripts/rebuild_model.sh /path/to/biscuit_pics
#
# BLENDER names the executable; the default is the macOS application bundle.

usage() {
  printf '%s\n' 'usage: scripts/rebuild_model.sh <path to a biscuit_pics checkout>' >&2
  exit 2
}

[ "$#" -eq 1 ] || usage
checkout=$1
blender=${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}

project_root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd -P)
cd "$project_root"

package=assets/models/biscuit
served=static/pose-studio
studies=$checkout/biscuit_pics/generated/3d

[ -d "$studies/miami-cinematic-eyes-refined" ] || {
  printf '%s\n' "no study chain at $studies; see $package/README.md, Provenance" >&2
  exit 2
}
[ -x "$blender" ] || {
  printf '%s\n' "Blender not found at $blender; set BLENDER" >&2
  exit 2
}
git rev-parse --is-inside-work-tree >/dev/null

# src/common.py and src/viewer.py resolve the studies two directories above the
# package, which is assets/ here. A link there, removed on exit, is what makes
# assets/biscuit_pics/generated/3d/... resolve without editing either script.
link=assets/biscuit_pics
[ ! -e "$link" ] || { printf '%s\n' "$link already exists; remove it first" >&2; exit 2; }
ln -s "$checkout/biscuit_pics" "$link"
trap 'rm -f "$link"' EXIT

# The five commands the package's README gives, in its order, from inside it.
# build.py writes model/biscuit-poseable.blend and model/biscuit-poseable.glb;
# viewer.py writes viewer.html and qa/viewer-package.json; verify.py writes the
# qa records; render.py writes previews/native/; proof_sheet.py writes
# previews/pose-overview.jpg.
(
  cd "$package"
  "$blender" --background --python-exit-code 1 --python src/build.py
  uv run --frozen python src/viewer.py
  "$blender" --background --python-exit-code 1 --python src/verify.py
  "$blender" --background --python-exit-code 1 --python src/render.py
  uv run --frozen python src/proof_sheet.py
)

# The three outputs the site serves live beside the viewer, not in the package.
mv "$package/viewer.html" "$served/viewer.html"
mv "$package/model/biscuit-poseable.glb" "$served/model/biscuit-poseable.glb"
mv "$package/previews/pose-overview.jpg" "$served/previews/pose-overview.jpg"

# The viewer links two files the site does not serve; the same three rewrites
# the first import made, asserted the same way. assets/manifest.json records
# them under `patched`.
uv run --frozen python - <<'EOF'
from pathlib import Path
p = Path("static/pose-studio/viewer.html")
s = p.read_bytes()
pairs = [
    (b'href="model/biscuit-poseable.blend"', b'href="https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/model/biscuit-poseable.blend"', 2),
    (b'href="README.md"', b'href="https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/README.md"', 1),
]
for old, new, n in pairs:
    assert s.count(old) == n, (old, s.count(old))
    s = s.replace(old, new)
p.write_bytes(s)
EOF

just assets-manifest

printf '\n%s\n' 'Rebuilt. Read the assets/manifest.json diff, then set each changed entry'
printf '%s\n' 'source to rebuilt:<date> and its source_sha256 to the new viewer digest.'
printf '%s\n' 'Nothing has been staged, committed, tagged, or pushed.'
```

Two things the script relies on that this ticket checks rather than assumes: `uv run
--frozen python` provides Pillow for `viewer.py` and `proof_sheet.py` (§2.4 pins it), and
`assets/biscuit_pics` must be gitignored — S00's `.gitignore` names it (CONVENTIONS.md §2).
Confirm with `git check-ignore assets/biscuit_pics`, which prints the path; if it prints
nothing, the link would be a stray path `just check` refuses, and that is an S00 follow-up
of one `.gitignore` line to hand back. The `trap` keeps the worktree clean either way.

Check the script's shape without running a rebuild:

```sh
sh scripts/rebuild_model.sh; echo "rc=$?"
sh scripts/rebuild_model.sh /nonexistent; echo "rc=$?"
uv run --frozen prek run --all-files shellcheck
```

Expected: the usage line and `rc=2`; the "no study chain" line and `rc=2`; shellcheck
passes (the file must be staged or tracked for prek to see it; run after step 9 if it is
skipped). The script is run for real, against `$D`'s parent checkout, only if the
maintainer asks in the hand-back; the rebuild is a non-goal.

### Step 9: Add to the index and confirm LFS took the three

```sh
git add assets static/pose-studio scripts/rebuild_model.sh
git lfs ls-files --long
git ls-files -s assets/models/biscuit/model/biscuit-poseable.blend assets/models/biscuit/qa/geometry/rigged.json assets/models/biscuit/qa/native-samples.json
git show :assets/models/biscuit/model/biscuit-poseable.blend | head -3
git ls-files -s scripts/rebuild_model.sh
git ls-files assets static/pose-studio | wc -l
```

Expected: `git lfs ls-files` lists exactly three paths with their sizes (12 MB, 18 MB,
2.5 MB); the three index entries are pointers (the `show` prints
`version https://git-lfs.github.com/spec/v1`, then `oid sha256:95d16473…`, then
`size 12004899`); `100755` for the script; `106` files (104 copied, the README, and
`assets/manifest.json`).
Anything more in `git lfs ls-files` means a pattern in `.gitattributes` is wider than §3
says, and anything fewer means step 1's check was ignored; either way, `git reset` the
index, fix nothing here, and hand back.

### Step 10: The manifest

```sh
just assets-manifest
git diff --stat assets/manifest.json
uv run --frozen python -c "import json; m=json.load(open('assets/manifest.json')); print(len(m['assets']), sorted({e['storage'] for e in m['assets']}), sum(e['bytes'] for e in m['assets']))"
```

Expected: 105 entries; `['blob', 'lfs']`; a byte total of about 106.9 MB (the sum of the
copy list, less D's README, plus the adapted one; record the figure). `write` fills
`source` as `studio` and `licence` as `unsettled` for a new file (§4). Now set every
`source` to the D path it came from, with one command rather than 105 edits:

```sh
uv run --frozen python - <<'EOF'
import json
from pathlib import Path
p = Path("assets/manifest.json")
m = json.loads(p.read_text())
prefix = "biscuit_pics@1d9d358:"
for e in m["assets"]:
    path = e["path"]
    if path.startswith("assets/models/biscuit/"):
        src = "models/biscuit/" + path.removeprefix("assets/models/biscuit/")
    elif path.startswith("assets/illustrations/good/"):
        src = "good/" + path.removeprefix("assets/illustrations/good/")
    elif path == "static/pose-studio/viewer.html":
        src = "models/biscuit/viewer.html"
    elif path == "static/pose-studio/model/biscuit-poseable.glb":
        src = "models/biscuit/model/biscuit-poseable.glb"
    elif path == "static/pose-studio/previews/pose-overview.jpg":
        src = "models/biscuit/previews/pose-overview.jpg"
    else:
        raise SystemExit(f"unexpected path {path}")
    e["source"] = prefix + src
    e["licence"] = "unsettled"
    if path == "static/pose-studio/viewer.html":
        e["source_sha256"] = "8838e723399ee4e1eba5e9926da4503fe639459f1b809bc3bf9575856e55170a"
        e["patched"] = [
            'href="model/biscuit-poseable.blend" (x2) -> https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/model/biscuit-poseable.blend',
            'href="README.md" -> https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/README.md',
            "no other byte differs from biscuit_pics@1d9d358:models/biscuit/viewer.html",
        ]
lines = [json.dumps(e, separators=(", ", ": ")) for e in sorted(m["assets"], key=lambda e: e["path"])]
p.write_text('{\n  "schema_version": 1,\n  "assets": [\n    ' + ",\n    ".join(lines) + "\n  ]\n}\n")
EOF
just check-assets
```

The write above has to match the exact layout `check_assets.py write` produces, or the
next `just assets-manifest` (which keeps `source`, `licence`, `source_sha256` and
`patched`) will reformat it; so after the edit, run `just assets-manifest` once more and
confirm `git diff assets/manifest.json` after it is empty. If `write` reorders keys or
changes the separators, take its layout — the tool's output is canonical (§4) — and adjust
the script above to produce it, noting the difference. The README entry
(`assets/models/biscuit/README.md`) is adapted, not copied, so its `source` is
`biscuit_pics@1d9d358:models/biscuit/README.md` all the same and its `sha256` is the
adapted file's; add
`"source_sha256": "b267406bd34ef01291590e5b26c5b9812d7b54e0cf6d3c3871257eeff39d2ec4"` (D's
README at `1d9d358`, which step 1's `shasum` over `$D/models/biscuit/README.md` confirms)
and `"patched": ["links corrected to this repository's layout; Provenance section added"]`
to it by hand after the script, then re-run `just assets-manifest` and `just check-assets`.

Expected from `just check-assets`: the self-test line, then the summary line, exit 0.

### Step 11: The gate with the real files

```sh
just lint
just check
```

Expected: both green. This is the §10 claim assigned to S02: the prek `exclude` alone
keeps `check-added-large-files`, editorconfig-checker, typos and lychee off the assets.
If `lint` fails on a file under `assets/` or `static/pose-studio/`, the exclusion set is
wrong in one of its six places: do not widen it here — §9 lists those files as S00's —
hand back the failing hook's output and the path, and stop. `just check` also proves that
`bg-project-check`'s worktree snapshot copes with 107 MB of new files (record how long it
takes).

### Step 12: Commit, notes, status

Commit on the ticket branch (LFS objects are written to `.git/lfs/objects/` by the
commit; `git lfs ls-files` afterwards still shows three). Fill in the hand-back notes,
set `status: done` on this file. Pushing and opening the pull request are separately
authorised: the push is the first time the three LFS objects leave this machine, and
S07 is where the remote comes to exist.

## Acceptance criteria

- [ ] `git -C "$D" rev-parse HEAD` printed `1d9d3580f2037826feb6e05f39f5a777b52db86c`
      before the copy, and every `source` in the manifest names `biscuit_pics@1d9d358:`.
- [ ] `git ls-files assets static/pose-studio | wc -l` prints `106`; `git lfs ls-files`
      lists exactly `assets/models/biscuit/model/biscuit-poseable.blend`,
      `assets/models/biscuit/qa/geometry/rigged.json` and
      `assets/models/biscuit/qa/native-samples.json`.
- [ ] `shasum -a 256` of `static/pose-studio/model/biscuit-poseable.glb` is
      `51d16c1826b2c3ad6ad85fcb176a73e0d1c7a0ac3665ad10f1b6700e9e9be716`, of the checked-out
      `.blend` is `95d164730e9354ab3d9bd561a73180690bbb055fffa9bf230c735f735234b4c3`, and
      of every other copied file equals D's (step 4's `-c` run reports no line but `OK`).
- [ ] `grep -c 'href="model/biscuit-poseable.blend"' static/pose-studio/viewer.html`
      and `grep -c 'href="README.md"'` both print `0`;
      `grep -o 'href="previews/pose-overview.jpg"' … | wc -l` prints `3` and
      `grep -o 'href="model/biscuit-poseable.glb"' … | wc -l` prints `1`; the manifest's
      viewer entry has `source_sha256` `8838e723…` and a three-item `patched`.
- [ ] The EXIF sweep prints `69 images; 0 with EXIF`.
- [ ] `assets/models/biscuit/README.md` exists, has a `## Provenance` section naming the
      commit and the seven-folder chain, and `just lint` (lychee offline) resolves every
      relative link in it.
- [ ] `scripts/rebuild_model.sh` is `100755`, `#!/bin/sh`, exits 2 with a usage line on
      no argument and on a path without the study chain, and shellcheck passes it.
- [ ] `just check-assets` exits 0 after `just assets-manifest` leaves `git diff
      assets/manifest.json` empty.
- [ ] `just lint` and `just check` are green with every file in the tree.
- [ ] No file under `Justfile`, `pyproject.toml`, `.gitattributes`, `.gitignore`,
      `scripts/check_assets.py` or `docs/` changed; `git status` after the commit shows a
      clean worktree and no `assets/biscuit_pics` link.
- [ ] Each open point below is answered in the hand-back notes.

## Verification

From the repository root, on the branch, after the commit:

```sh
git ls-files assets static/pose-studio | wc -l
git lfs ls-files --long
shasum -a 256 static/pose-studio/model/biscuit-poseable.glb assets/models/biscuit/model/biscuit-poseable.blend
grep -o 'href="[^"]*"' static/pose-studio/viewer.html | sort | uniq -c
just check-assets
just check
git ls-files -s scripts/rebuild_model.sh
sh scripts/rebuild_model.sh; echo "rc=$?"
```

Expected: `106`; three LFS lines; the two fact-8 digests; four href lines with counts
2, 1, 3, 1 and two of them GitHub URLs; the checker's self-test and summary lines, exit
0; `just check` green; `100755`; the usage line and `rc=2`.

## Hand-back notes

Filled in by the agent that executed this ticket, on branch `S02-asset-import` in a
Supacode worktree, 2026-09-23. Three commits on the branch, this one included; nothing
pushed. As agreed on S00, the work stays on the worktree's branch rather than
`ticket/s02-asset-import`; no check reads the branch name.

- **Step 1.** `git -C "$D" rev-parse HEAD` printed
  `1d9d3580f2037826feb6e05f39f5a777b52db86c`, `status --short | wc -l` printed `0`, and
  the four digests were the ticket's: viewer `8838e723399ee4e1eba5e9926da4503fe639459f1b809bc3bf9575856e55170a`,
  GLB `51d16c1826b2c3ad6ad85fcb176a73e0d1c7a0ac3665ad10f1b6700e9e9be716`, `.blend`
  `95d164730e9354ab3d9bd561a73180690bbb055fffa9bf230c735f735234b4c3`, D README
  `b267406bd34ef01291590e5b26c5b9812d7b54e0cf6d3c3871257eeff39d2ec4`. `git check-attr
  filter` printed `lfs` for the three LFS paths and `unspecified` for the GLB; `git lfs env`
  printed `git-lfs/3.8.0 (GitHub; darwin arm64; go 1.27.0)`; D holds no symlink; `git
  check-ignore assets/biscuit_pics` printed the path. No file's `check-attr` disagreed with
  §3.
- **The viewer after step 5.** sha256
  `ec1e9d32399191de2593e9737d5242c10ca8b6a41dc0029680f710065fe3c6e8`, 27,561,668 bytes
  (243 bytes longer than D's: the two URLs). `grep -o 'href=…' | sort | uniq -c` before:
  `2 model/biscuit-poseable.blend`, `1 model/biscuit-poseable.glb`,
  `3 previews/pose-overview.jpg`, `1 README.md`; after: the two GitHub blob URLs with
  counts 2 and 1, and the GLB and overview lines unchanged.
- **Step 3 and 4.** `find assets static/pose-studio -type f | wc -l` printed `105`. The
  three digests were unchanged after the copy. The expected-list run checked **101** files
  (the ticket says 100: the `.blend` is in the list, since only the README, the viewer,
  the GLB and the overview are excluded) and `grep -vc ': OK$'` printed `0`. Every text
  file in D is LF-only (checked with `grep -c $'\r'` over the non-binary files before the
  copy) and `git ls-files --eol assets static/pose-studio` after `git add` reports
  `i/-text w/-text` (71), `i/lf w/lf` (34) and one `i/lf w/-text` (the `.blend`, whose
  index entry is the pointer), so `* text=auto` altered nothing.
- **Step 6.** The sweep printed `70 images; 4 with EXIF`, not the ticket's `69 images; 0
  with EXIF`. CONVENTIONS.md §1 fact 9 already predicts both corrections: the four are
  `assets/models/biscuit/previews/native/{lying,paw-raised,sitting,standing}.png`, each
  carrying exactly `{282: 72.0, 283: 72.0}` (XResolution, YResolution) and an empty GPS
  IFD, which the checker allows; and there are 22 previews under `assets/`, not 21, so the
  count is 36 + 22 + 11 + 1. Nothing was stripped; `just check-assets` passes as copied.
- **Ticket arithmetic**, for the record and without effect on the totals: `previews/`
  under `assets/` holds 22 files (the table says 21), `src/` holds 16 (the table says 15),
  and step 4 checks 101 files (the text says 100). 94 files from `models/biscuit/`, 105
  destinations and 106 tracked paths are all as written.
- **Step 9.** After `git add`, `git lfs ls-files --long` listed exactly the three paths
  (`95d16473…` for the `.blend`, `927bf1ee…` for `qa/geometry/rigged.json`, `863cf74e…`
  for `qa/native-samples.json`, each starred as present); `git show
  :assets/models/biscuit/model/biscuit-poseable.blend | head -3` printed `version
  https://git-lfs.github.com/spec/v1`, `oid sha256:95d164730e9354ab3d9bd561a73180690bbb055fffa9bf230c735f735234b4c3`,
  `size 12004899`; `git ls-files -s scripts/rebuild_model.sh` printed `100755`; `git
  ls-files assets static/pose-studio | wc -l` printed `106`. Unchanged after the commit.
- **Step 10.** The first `just assets-manifest` wrote 105 entries, storages `['blob',
  'lfs']` (102 and 3), byte total **111,680,319**, which is the per-file copy list summed exactly,
  with the viewer 243 bytes longer and the adapted README at 9,164 (the ticket's
  "about 106.9 MB" is its own arithmetic). Two directory totals in CONVENTIONS.md §3
  are wrong while every per-file figure is right: `textures/` sums to 10,040,783 (§3
  says 12,209,289) and `illustrations/good/` to 15,137,724 (§3 says 14,092,724); S06
  should take the manifest's figures for `docs/explanation/large-files.md`. `check_assets.py write`'s layout
  matched the step-10 script exactly: after the script and the README's two hand-added
  fields, a second `just assets-manifest` left `git diff assets/manifest.json` empty, so no
  change to the script was needed. Every `source` starts `biscuit_pics@1d9d358:`, every
  `licence` is `unsettled`, and only the viewer (`source_sha256` `8838e723…`, three
  `patched` items) and the README (`source_sha256` `b267406b…`, one `patched` item) carry
  the optional fields. `just check-assets` printed `check_assets check: ok`, exit 0.
- **Step 11.** `just lint`: every hook passed (actionlint skipped, no workflow files yet)
  with the 26 MB viewer and the 16 MB GLB in the tree, so the prek `exclude` alone keeps
  `check-added-large-files`, editorconfig-checker, typos and lychee off the assets: the
  §10 claim holds and no hook was excluded beyond §2.1. `just check` exit 0 in **15
  seconds** wall clock (nine sha256 snapshots over the 112 MB, `bg-project-check` included);
  the snapshot is not slow enough to matter. Elided transcript:

  ```text
  ==> just lock-check
  ==> just lint            (21 hooks Passed, actionlint Skipped)
  ==> just frontend-static COMPLETED 376 FILES 0 ERRORS 0 WARNINGS
  ==> just frontend-coverage  Test Files 1 passed (1)  Tests 2 passed (2)
  ==> just frontend-build  Wrote site to "build"
  ==> just check-assets    check_assets check: ok
  ==> just check-docs      markdownlint, typos, lychee Passed; Validated 39 pages and 40 canonical topics.
  ==> just check-agents    Validated AGENTS.md, 2 adapters, and 8 skills.
  ==> just check-clean     The worktree matches the check baseline.
  All checks passed and the worktree is unchanged.
  ```

- **The README was invisible to the gate, now fixed (authorised).** `lychee.toml`
  `exclude_path` and `.markdownlint-cli2.jsonc` `ignores` both named `assets` whole, so
  neither hook read `assets/models/biscuit/README.md`, contradicting CONVENTIONS.md §2.1's
  sentence that the README is linted and its links resolved. Both are S00-owned files
  outside this ticket's table (not on §9's no-lane list); the maintainer authorised
  narrowing them here, as a CONVENTIONS correction, rather than a hand-back. Both now list the six package directories and `assets/illustrations`
  (the §2.1 set), and CONVENTIONS.md §2 (the two tree lines) and the §2.1 table say so.
  Proof, lychee 0.24.2 run directly on the README with `--offline --root-dir .`: under the
  old `lychee.toml` it prints `No files found for this input source` and `0 Total`;
  under the new one `4 Total, 4 Unique, 4 OK, 0 Errors` (the four relative links), and
  `prek run lychee --files assets/models/biscuit/README.md -v` reports the same four.
  markdownlint's verbose run now lists the README among its 85 files with 0 issues; its
  `ignores` work by the same negated globs that listing prints, so the old `!assets`
  hid it the same way. The typos exclusion in `pyproject.toml` still
  names `assets/` whole and so skips the README; left as the belt it is, since
  `pyproject.toml` was not in the authorisation and typos reads the README's prose nowhere
  else. Commit `c0c4a6b`.
- **`scripts/rebuild_model.sh` deviates from the embedded text in three places**,
  authorised by the maintainer and all about shape, not the build sequence: (1) the
  argument is made absolute before `cd "$project_root"` (`checkout=$(CDPATH='' cd --
  "$1" && pwd -P) || usage`), because the ticket's text resolved the symlink target from
  `assets/` and the study-chain test from the project root, so a relative path satisfied
  one and not the other; (2) `rm -f "$link"` runs after the five build commands and before
  `just assets-manifest`, so the manifest walk under `assets/` never meets the link
  (`rglob` on 3.14 would not have followed it, but the ordering now does not depend on
  that); the `trap` stays for an interrupted run. Consequences for the checks: a missing
  path now fails at the absolutising step and prints the usage line (`rc=2`), while a real
  directory without the chain prints the "no study chain" line (`rc=2`); both were run,
  with an absolute and a relative directory. (3) After a Codex adversarial review of the
  branch found that a failed build left `assets/` half-rewritten under the old manifest,
  the maintainer chose a guard and an automatic restore: the script refuses to start
  (`rc=2`) unless `git status --porcelain --untracked-files=all` is empty for `assets` and
  `static/pose-studio`, and an `EXIT` trap, with `INT` and `TERM` routed to it, restores
  both from `HEAD` and cleans what the run created unless the run reached the end of
  `just assets-manifest`. A staging directory was rejected because the build scripts write
  by relative path inside the package and are themselves assets. The same change purges
  `__pycache__` under the package after the build and on failure, and exports
  `PYTHONDONTWRITEBYTECODE=1`: `build.py` imports `common`, `rig` and `pose_io`, and the
  checker walks the filesystem, so ignored `.pyc` files would otherwise have entered the
  manifest and failed `check-assets` in a clean clone. Tested with a fake `BLENDER` that
  appends to `model/rig.json`, creates `previews/stray.png`, `src/__pycache__/x.pyc` and a
  stray file under `static/pose-studio/`, then exits 1:

  ```text
  $ touch assets/stray; BLENDER=<fake> sh scripts/rebuild_model.sh <fake checkout>
  assets/ or static/pose-studio/ differs from HEAD; commit or remove the changes first
  rc=2   (assets/stray left in place, then removed)
  $ BLENDER=<fake failing blender> sh scripts/rebuild_model.sh <fake checkout>
  rebuild failed; assets/ and static/pose-studio/ restored to HEAD
  rc=1
  $ just check-assets
  check_assets check: ok
  ```

  Afterwards neither `assets/biscuit_pics` nor `src/__pycache__` existed and the only
  change in the worktree was the script itself. The success path needs Blender and the
  real study chain and was not run. shellcheck passes it in `just lint`.
- **What `common.py` and `viewer.py` resolve.** Both compute `ROOT` as the package
  directory (`assets/models/biscuit`) and `REPO_ROOT = ROOT.parents[1]`, which is
  `assets/`, then reach `REPO_ROOT / 'biscuit_pics/generated/3d/…'`; the link at
  `assets/biscuit_pics` pointing at `<checkout>/biscuit_pics` is the right bridge for both.
  One thing the ticket's reasoning did not mention: `common.py` also `exec`s the
  eyes-refined study's own `src/common.py` (lines 13-15) and then sets `legacy.c.ROOT =
  ROOT`. That module resolves its own paths with `Path(__file__).resolve()`, which follows
  the symlink into the real checkout, so the study's helpers read their own chain where it
  lives; this is the intended behaviour and needs nothing from the script. Neither script
  reads an environment variable. The scripts are copied verbatim and untouched.
- **`assets/biscuit_pics` is gitignored**: `git check-ignore assets/biscuit_pics` prints
  the path. No S00 follow-up.
- **The LFS quota figure (open point).** Read on 2026-09-23 from GitHub Docs, "About
  storage and bandwidth usage" (Git LFS): a free account includes **10 GiB of storage and
  10 GiB of bandwidth a month**, and the pre-paid data packs have been replaced by metered
  billing beyond that (bandwidth per GiB downloaded, storage at an hourly rate); a
  download counts against the repository owner, and source archives containing LFS
  objects count too. CONVENTIONS.md §3 and §10 say 1 GB and 1 GB; the figure is ten times
  larger, so the three objects (32.3 MB) are 0.3% of a month's bandwidth per full fetch
  rather than 3%. Nothing changes in the design; S06 carries the figure onto
  `docs/explanation/large-files.md`.
- **Whether the packed textures are photo-derived (open point).** Asked; the maintainer
  does not know. Recorded as still open. Nothing here depends on it: the 36 maps carry no
  EXIF and pass the checker.
- **The licence (open point).** Not resolved. 105 entries carry `licence: "unsettled"`
  and wait on the answer in `docs/explanation/content-policy.md`.
- **Setup in this worktree.** `just sync` ran first (`uv sync`, then `npm ci` through the
  token in `~/.npmrc`; `.venv` and `node_modules` are gitignored), and the first `just
  lint` cloned the hook repositories into prek's cache. Neither `just install-hooks` nor
  `git lfs install --local` was run, since the worktree shares `.git` with
  `~/projects/biscuit_studio`. The three LFS objects are in that shared `.git/lfs/objects/`.
- **Authorisations asked**, all granted before the work: the three network reads above
  (`npm ci`, prek's hook clones, one fetch of the GitHub Docs page); the two rebuild-script
  fixes; the narrowing of the two lint configurations with the CONVENTIONS correction.
  Nothing left the machine; no push, no pull request.
- **Verification**, run after the commits, as the section above lists:

  ```text
  $ git ls-files assets static/pose-studio | wc -l
  106
  $ git lfs ls-files --long
  95d164730e9354ab3d9bd561a73180690bbb055fffa9bf230c735f735234b4c3 * assets/models/biscuit/model/biscuit-poseable.blend
  927bf1ee2c5b1756f8cb3a89d16eb5910ebe2523c7fdd7969601b4bd40d7b986 * assets/models/biscuit/qa/geometry/rigged.json
  863cf74e5431d94811a12fb0e686b163fad5e28bdf16610accc171fa370b7a00 * assets/models/biscuit/qa/native-samples.json
  $ shasum -a 256 static/pose-studio/model/biscuit-poseable.glb assets/models/biscuit/model/biscuit-poseable.blend
  51d16c1826b2c3ad6ad85fcb176a73e0d1c7a0ac3665ad10f1b6700e9e9be716  static/pose-studio/model/biscuit-poseable.glb
  95d164730e9354ab3d9bd561a73180690bbb055fffa9bf230c735f735234b4c3  assets/models/biscuit/model/biscuit-poseable.blend
  $ grep -o 'href="[^"]*"' static/pose-studio/viewer.html | sort | uniq -c
  2 href="https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/model/biscuit-poseable.blend"
  1 href="https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/README.md"
  1 href="model/biscuit-poseable.glb"
  3 href="previews/pose-overview.jpg"
  $ just check-assets
  check_assets check: ok
  $ just check
  All checks passed and the worktree is unchanged.   (15 s)
  $ git ls-files -s scripts/rebuild_model.sh
  100755 8109b897829a314e451b4aa0e3c427759dc1fcce 0 scripts/rebuild_model.sh
  $ sh scripts/rebuild_model.sh; echo "rc=$?"
  usage: scripts/rebuild_model.sh <path to a biscuit_pics checkout>
  rc=2
  ```

  `git status` is clean after the commits and no `assets/biscuit_pics` link exists.

## Open points

- **The LFS quota figure.** CONVENTIONS.md §3 and §10 state 1 GB storage and 1 GB
  bandwidth a month as the free tier and mark it unverified. Read GitHub's current
  documentation on Git LFS storage and bandwidth, record the figure and the date in the
  hand-back notes, and say whether three objects totalling 32.3 MB change anything; S06
  carries the figure onto `docs/explanation/large-files.md`.
- **Whether the packed textures in the `.blend` are photo-derived.** D's README says the
  scene's textures are packed and "still name the earlier study". The 36 PNG files under
  `textures/` are generated maps (colour, normal, occlusion, roughness per material) and
  carry no EXIF; whether any was painted from a photograph of the dog is a question for
  the maintainer, not a fact this ticket can read out of the file. Ask in the hand-back
  and record the answer; nothing here depends on it.
- **The licence.** Every `licence` field is `unsettled` (§5). This ticket does not
  resolve it; it records that 105 entries wait on the answer.
- **The rebuild link is ignored** (step 8): `git check-ignore assets/biscuit_pics` prints
  the path, or a one-line S00 follow-up is handed back.
- **Whether `just check` copes with the worktree snapshot** over 107 MB in acceptable
  time; if `bg-project-check` is slow enough to matter, say so and let the maintainer
  decide whether the snapshot should skip `assets/` (a change to G, out of scope).
