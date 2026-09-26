---
id: S13
title: "Model update: the approved model re-imported from biscuit_pics at 891c44c"
status: done
depends_on: [S02, S08]
parallel_with: [S10, S11, S12]
branch: update-model
estimated_size: M
---

# S13: Model update: the approved model re-imported from biscuit_pics at 891c44c

## Context

S02 imported the approved model from D, the `biscuit_pics` worktree at
`/Users/scutting/.supacode/repos/biscuit_pics/very_nice_three_deeez`, at `1d9d358`. D has
since promoted two approved versions to `models/biscuit/`: `e54f7d5`, refined
hindquarters on rig version 2, and `891c44c`, twenty sculpted charcoal toe beans. At
`891c44c` the package tracks 133 files, up from 94. It renames the undressed previews,
adds rear and undressed front and left views, four `paw-pad-*` textures, six QA records
and three build scripts, and its build now starts from
`biscuit_pics/generated/3d/miami-cinematic-hindquarters-refined/` rather than from the
eyes-refined model directly. Its viewer adds a fourth relative link, to
`previews/comparison.jpg`.

This is an import in the sense of `docs/how-to/import-an-asset.md`, following S02's
procedure, not a rebuild: every model entry's `source` names `biscuit_pics@891c44c`.

The maintainer decided on 2026-09-26:

- The toe bean comparison, `previews/comparison.jpg` and the eight renders under
  `previews/comparison/`, is no longer relevant and does not come across.
- The work is tracked by this ticket. S11 is not edited.
- The model page describes the revision.

## Goal

- Every file D tracks under `models/biscuit/` at `891c44c`, except the nine comparison
  files, is in this repository, byte-identical, where S02 put its predecessor. The
  README is adapted, and the viewer differs in four places.
- The viewer's comparison link is removed rather than left dead.
- `assets/manifest.json` names `biscuit_pics@891c44c:` on every model entry and
  `biscuit_pics@1d9d358:` on the eleven drawings only.
- `scripts/rebuild_model.sh` follows the new build: the hindquarters study as a
  precondition, `src/verify_anatomy.py` as a sixth command, the comparison deleted after
  the run, and the fourth viewer change applied and asserted.
- The model page, its test and every handbook page that stated a figure of the old import
  are current.

## Non-goals

- Running a rebuild (S11).
- Editing D, or anything outside this repository.
- The drawings, the licence (still `unsettled`), push, pull request and tag.
- The decision records 0006 to 0008 and `AGENTS.md`'s provenance list. They record the
  state when they were written, and they are left as history.

## Files touched

| Path | Change |
| --- | --- |
| `assets/models/biscuit/**` | replaced by D's `models/biscuit/` at `891c44c`, less the comparison; `.gitignore` new; four `*-undressed.png` removed |
| `assets/models/biscuit/README.md` | re-adapted from D's README at `891c44c` |
| `static/pose-studio/viewer.html` | D's viewer, with four changes |
| `static/pose-studio/model/biscuit-poseable.glb`, `static/pose-studio/previews/pose-overview.jpg` | D's, byte-identical |
| `assets/manifest.json` | 130 entries; model sources to `891c44c`; README and viewer `patched` rewritten |
| `scripts/rebuild_model.sh` | the new build's precondition, sixth command, comparison purge and fourth change |
| `src/routes/model/+page.svelte` | description names the toe beans and hind legs; overview is 1800 × 1510; viewer size 29 MB |
| `tests/pages.test.ts` | a test that the description names the toe beans |
| `docs/how-to/rebuild-the-model.md`, `docs/reference/asset-manifest.md`, `docs/reference/testing.md`, `docs/reference/quality-gates.md`, `docs/explanation/large-files.md`, `docs/explanation/architecture.md`, `docs/explanation/quality-philosophy.md`, `docs/operations/maintenance.md`, `docs/project/repository-map.md` | figures and facts of the new import |
| `CHANGELOG.md` | an Unreleased entry |
| `tickets/README.md` | an index row |
| `tickets/S13-model-update.md` | this file |

## The viewer's four changes

Applied by one byte-exact Python replace with each count asserted. The same snippet is in
`scripts/rebuild_model.sh`. Run against a fresh copy of D's viewer, it gave the same
digest as the committed file.

| Before | Count | After |
| --- | ---: | --- |
| `href="model/biscuit-poseable.blend"` | 2 | the GitHub blob URL, as S02 |
| `href="README.md"` | 1 | the GitHub blob URL, as S02 |
| `<a href="previews/comparison.jpg">Toe bean comparison <span>↗</span></a>` with its four-space indent and newline | 1 | nothing |

## Verification

```sh
git -C "$D" rev-parse HEAD; git -C "$D" status --short | wc -l
shasum -a 256 -c ai_tmp/s13-expected.txt | grep -vc ': OK$'
grep -c '@1d9d358' assets/manifest.json
git lfs ls-files
just check
```

## Hand-back notes

- **Source.** D at `891c44c7919d95e66cb10c0b4d2599c0a5e697d2`, `status --short` count
  `0`. D's viewer sha256 is `d21dca94644a1ec4155f575c91191ea4ed21b817b5915485901006022d56c0b0`,
  the value its `qa/viewer-package.json` records. D's README sha256 is
  `2f2bfe89e27ed05f0c712f89d8034fee92d26e540e5437e9bd7a8602f0155ad2`, which is the
  README entry's `source_sha256`.
- **The copy.** 118 files, the same set `git ls-tree -r 891c44c -- models/biscuit` lists
  less the comparison and the README, all `OK` under `shasum -a 256 -c` against D.
  `cp -R` also brought five `src/__pycache__/*.pyc` files. They are untracked and ignored
  in D, so they were deleted before the manifest was written; the tracked-set comparison
  is what caught them. A future import copies from `git ls-tree`, or checks against it,
  not from the directory.
- **The viewer.** It is 30,754,576 bytes, sha256
  `0585073bb8fac120fb2fac74eb0ecbb81e4c46b857f43cae95b7bb4fbfb39da7`. What remains:
  two GitHub `.blend` links, one GitHub README link, one GLB link and three overview
  links. No `comparison` string is left.
- **The manifest.** 130 entries, 127,705,162 bytes. Three are LFS: the `.blend`,
  `qa/geometry/rigged.json` and `qa/native-samples.json`, 40,462,615 bytes together.
  Four entries were removed (the `*-undressed.png` previews) and 29 added. 52 kept
  their bytes, the eleven drawings among them. `grep -c '@1d9d358'` gives `11`.
- **EXIF.** There are 85 images. Four native renders carry only `XResolution` and
  `YResolution`, which the checker allows, and `just check-assets` is green.
- **The gate.** `just check`: all checks passed and the worktree is unchanged
  (shellcheck, 5 test files / 21 tests, coverage, build, `check-assets`, `check-docs`,
  `check-agents`).
- **Served site.** Under `vite preview`, the viewer, the GLB and the overview are served
  at their new sizes. The prerendered `/model/` carries `width="1800" height="1510"` and
  the toe bean clause. The browser extension was not connected, so nobody has looked at
  the viewer in a browser; the maintainer should open it before pushing.
- **Setup side effects.** In a fresh worktree, `just initialize` modified
  `package-lock.json` (it dropped an extraneous `yaml` entry) and reformatted code inside
  `tickets/S00-foundation.md`. Both were restored to `HEAD`, and neither is part of
  this change. This belongs to S00 as a follow-up.
- **For S11.** S11 pins `1d9d358` and expects the five-command, three-rewrite script. Its
  run now needs D at `891c44c` or later, with `miami-cinematic-hindquarters-refined`
  present, and should expect six commands, the comparison purge and four viewer changes.
  S11 itself is not edited.
- **Kept, not served.** `previews/toe-beans-review.jpg`, the close-up sheet of the current
  model, not a before / after, is imported under `assets/` and linked from the README.
  If the maintainer counts it as part of the comparison, drop it and its
  `proof_sheet.py` output in the rebuild script together.
