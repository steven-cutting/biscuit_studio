---
title: "Rebuild the model"
kind: "how-to"
audience: [contributor, maintainer, agent]
canonical_for: [model_rebuild_procedure]
requires: []
---

# Rebuild the model

A rebuild regenerates the approved model from its own scripts and the earlier studies it
was built from. It is rare, it is local, and it replaces the approved model only when the
maintainer approves the replacement. Most changes never need one: posing her, rendering a
still or exporting a posed GLB all work from the files already committed, as
`assets/models/biscuit/README.md` describes.

## What a rebuild is and is not

A rebuild rewrites the generated files in `assets/models/biscuit/` — the `.blend`, the rig,
the QA records and the previews — and the three served files under `static/pose-studio/`:
the viewer, the GLB and the overview image. It runs the model's own scripts under
`assets/models/biscuit/src/`, unchanged from where they were written.

It is never run in CI. CI checks that every file matches the manifest; it does not check
that the files could be made again, because that needs Blender and a 1.9 GB checkout no
runner has.

It is not a way to try things. The package's README says to keep design experiments
elsewhere, and that rule is kept: a rebuild that is not going to be approved does not
belong in this repository's history, where the viewer alone costs 29 MB each time.

## What it needs

- **Blender 5.2.1**, the version the model was verified with. The script uses
  `/Applications/Blender.app/Contents/MacOS/Blender`; on another system set `BLENDER` to
  the executable.
- **Python 3 with Pillow**, which this repository's own environment has: the two Python
  steps run through `uv run --frozen`.
- **A checkout of `biscuit_pics`** at the commit `assets/models/biscuit/README.md` names.
  The build reads the earlier studies under `biscuit_pics/generated/3d/` there and never
  writes to them. It starts from the previous standard,
  `miami-cinematic-hindquarters-refined`, and loads its helpers from the chain
  `miami-cinematic-eyes-refined` → `miami-cinematic-sweater-foreleg-refined`
  → `miami-cinematic-tail-drape-studies` (variant D3) → `ear-profile-studies` →
  `ear-studies` → `cinematic-studies` → `miami-angular-base`. `viewer.py` also reads the
  studio camera frames from
  `miami-cinematic-sweater-foreleg-refined/qa/viewer-package.json`. The chain is not in
  this repository and is not going to be; see
  [Repository map](../project/repository-map.md).
- **A clean tree.** `assets/` and `static/pose-studio/` must match `HEAD`, with nothing
  modified and nothing untracked. Commit or remove any change there first.

## The recipe

```console
just model-rebuild /path/to/biscuit_pics
```

That runs `scripts/rebuild_model.sh` with the one path, which is the checkout's root — the
directory that holds `biscuit_pics/generated/3d/`. A relative path is fine; the script
makes it absolute first. In order, it:

1. Refuses to start, with exit status 2, if the path is missing, the study chain is not
   under it, Blender is not where it looks, `assets/` or `static/pose-studio/` differs from
   `HEAD`, or `assets/biscuit_pics` already exists.
2. Places a gitignored symlink at `assets/biscuit_pics`, pointing into the checkout. The
   model's `common.py` and `viewer.py` look for the studies in the directories above the
   package, the first of which here is `assets/`; the link is what lets them run
   unchanged.
3. Runs the package's six commands from `assets/models/biscuit/`: `src/build.py`,
   `src/verify.py`, `src/verify_anatomy.py` and `src/render.py` under Blender with
   `--python-exit-code 1`, and `src/viewer.py` and `src/proof_sheet.py` under Python, in
   the order the package's README gives.
4. Removes the link, and the by-products a manifest walk would otherwise list: Python's
   `__pycache__` directories, and the `.blend1` backup Blender keeps when it saves over
   the `.blend`. It also deletes the toe bean comparison renders, `previews/comparison/`
   and `previews/comparison.jpg`, which the build writes and this repository does not
   keep.
5. Moves the viewer, the GLB and the overview image to `static/pose-studio/`, where the
   site serves them.
6. Hashes the viewer as `viewer.py` wrote it, then rewrites its three links to files the
   site does not serve — two to the `.blend` and one to the README — to their pages on
   GitHub, and removes the line holding its link to the comparison sheet, asserting that
   each occurs exactly as often as the import found it. The digest taken before the
   changes must equal the `sha256` that `viewer.py` recorded in `qa/viewer-package.json`,
   or the run fails.
7. Runs `just assets-manifest`, which rehashes every file, writes the viewer entry's
   `source_sha256` from `qa/viewer-package.json`, and runs the checker.

If any step fails, or the run is interrupted, a trap removes the link, restores
`assets/` and `static/pose-studio/` to `HEAD` and deletes what the run created, and says
so. A half-rebuilt model never outlives the run; the clean-tree precondition is what makes
that restore safe.

A successful run stages, commits and pushes nothing. What is left is yours:

1. Read the whole `assets/manifest.json` diff. Every regenerated file's hash moved;
   anything else that moved is a question.
2. Set `source` to `rebuilt:<date>` on every regenerated entry, by hand, because the tool
   never rewrites a source. The viewer entry's `source_sha256` is not yours to set: the
   tool reads it from `qa/viewer-package.json`, the digest of the page as `viewer.py`
   wrote it before the four changes, and `just check` refuses the manifest when the
   two differ or the field is malformed — so `patched` names a difference from bytes
   that can still be checked. Leave `patched` as it is unless the rewrites changed.
3. Open the viewer and look at her, in the four poses, before asking the maintainer to
   approve the result.
4. Run `just check`.

## The optional checks

Two further checks exist and are not part of the recipe. `src/verify_browser.mjs`
connects to an isolated Chrome remote-debugging profile, given as its argument, and checks
native and browser deformation agreement, offline operation, the desktop and mobile
controls, saved JSON and PNG downloads, and the rejection of invalid poses.
`src/verify_interchange.py` reopens browser poses in Blender and compares posed GLBs with
the native surfaces; run it after the browser check has written
`qa/browser-saved-pose.json`. Their reports land in `qa/browser-verification.json` and
`qa/interchange-verification.json`, beside the native report the recipe writes, and a
changed report is part of the diff to read.

## What every rebuild costs

- **29 MB of ordinary history.** The viewer is served, so it is an ordinary blob, and
  every rebuild commits all of it again. The `.blend` and the two large QA records add
  about 40 MB of LFS objects. That is why rebuilds are rare and approved, and why the
  port of the viewer to a maintained component is the way out; see
  [Decision 0006](../decisions/0006-sources-in-lfs-served-files-as-blobs.md).
- **Two looks.** The viewer and the `.blend` carry the approved cel shading. The GLB
  carries standard PBR materials, so in any other viewer its lighting and outlines look
  different. A rebuild does not change that, and the model page says so beside the
  download.
- **Three links that point at `main`.** The rewritten links in the viewer name the
  `.blend` and the README on the `main` branch. A branch rename, or a move of either file
  under `assets/models/biscuit/`, breaks them inside a file no linter reads. The viewer's
  manifest entry lists the three under `patched`, which is where to look.

## Related pages

- [Import an asset](import-an-asset.md)
- [Large files](../explanation/large-files.md)
- [Decision 0006: Sources in LFS, served files as blobs](../decisions/0006-sources-in-lfs-served-files-as-blobs.md)
- [Decision 0008: The viewer is embedded as-is](../decisions/0008-the-viewer-is-embedded-as-is.md)
