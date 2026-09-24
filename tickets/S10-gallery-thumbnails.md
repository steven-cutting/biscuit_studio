---
id: S10
title: "Gallery thumbnails: WebP copies of the cel set, made by a recipe and listed in the manifest"
status: open
depends_on: [S08]
parallel_with: [S11]
branch: ticket/s10-gallery-thumbnails
estimated_size: M
---

# S10: Gallery thumbnails: WebP copies of the cel set, made by a recipe and listed in the manifest

## Context

`/gallery/` imports the eleven cel drawings under `assets/illustrations/good/` at full
size: nine heads at 1374×1145 and two bodies at 958×1642, as PNG files. The grid draws
each in a cell at least `9rem` wide. S03 measured the page scrolled to the end at 11 PNG
files and 15,141,024 bytes transferred, with the drawings painting for several seconds
after they arrived (S03 hand-back, "Browser check"). Its open point, "Thumbnails", said
that a resized copy of each drawing would cut that by an order of magnitude. It also said
that a derived image is an asset: it needs a manifest entry and a recipe that makes it
deterministically, so it belongs to an `asset-change` of its own. CONVENTIONS.md §11
accepts the heavy page for the first release, so this ticket runs after S08.

This is that `asset-change`. It follows the `asset-change` skill,
`docs/how-to/import-an-asset.md` for the manifest and review steps, and
`docs/reference/asset-manifest.md` for the entry's fields (CONVENTIONS.md §4:
`source` is `rebuilt:<date>` for a regenerated file).

Read first: CONVENTIONS.md §2.1, §4, §9 and §11; S03's ticket and hand-back notes;
`src/routes/gallery/+page.svelte`; `tests/pages.test.ts`; `scripts/check_assets.py`
(the metadata rule a new image must pass); the `asset-change` and `accessibility-review`
skills.

## Goal

- `just thumbnails` writes one WebP per drawing under `assets/illustrations/thumbnails/`,
  byte-identical on every run at the pinned Pillow.
- Each thumbnail has a manifest entry with `source: "rebuilt:<date>"`, and
  `just check-assets` is green.
- The gallery shows the thumbnails. Each figure offers the full drawing through a link
  whose accessible name says which drawing it opens.
- The scrolled gallery transfers a small fraction of the 15,141,024 bytes S03 measured,
  as measured again here.

## Non-goals

- Changing, re-encoding or removing the eleven PNG files: they stay the source, byte for
  byte.
- A `srcset` ladder of several widths. One width is enough for a grid of cells this
  small; add more only if the measurement says so.
- Thumbnails for anything outside `assets/illustrations/good/`.
- Promoting a thumbnail out of the studio (C01 has not landed).

## Files touched

| Path | Class | Change |
| --- | --- | --- |
| `scripts/make_thumbnails.py` | script | new: reads the eleven PNG files, writes the WebP copies |
| `Justfile` | repo | a `thumbnails` recipe in the `assets` section |
| `assets/illustrations/thumbnails/*.webp` | asset | eleven new files, written by the recipe, never by hand |
| `assets/manifest.json` | asset | eleven entries, written by `just assets-manifest`, then `source` set by hand as §4 allows for a new file |
| `src/routes/gallery/+page.svelte` | route | thumbnails shown, full drawings linked |
| `tests/pages.test.ts` | test | the gallery cases |
| `docs/reference/commands.md` | page | the recipe |
| `docs/how-to/import-an-asset.md` | page | a sentence: after changing a drawing under `good/`, run `just thumbnails` |
| `docs/how-to/maintain-dependencies.md` | page | a sentence: after a Pillow bump, run `just thumbnails-check` |
| `tickets/CONVENTIONS.md` | tickets | §11 "The gallery page is heavy" updated with the new measurement; S11, which may run alongside, edits only a different §11 bullet |
| `tickets/S10-gallery-thumbnails.md` | tickets | `status:` line, hand-back notes |

`assets/illustrations/` is already inside the §2.1 exclusion set, so the new directory
needs no linter change.

## Steps

1. **Choose the width.** Serve the gallery (`just preview`, with the base path as S03
   ran it). At the widest layout `--shell-max` allows, measure the widest rendered cell
   in CSS pixels. The thumbnail width is twice that, rounded up to a multiple of 40, and
   at least 480. Heights follow each drawing's aspect ratio. Record the measurement and
   the width.

2. **Write `scripts/make_thumbnails.py`** in the style of `scripts/check_assets.py`:
   standard library plus Pillow, a `main()` whose only argument is `--check`, and ruff
   clean under the `scripts/**` rules. For each `*.png` under
   `assets/illustrations/good/`, in sorted order, it:
   - opens the image and converts it to `RGB`, or to `RGBA` if it has an alpha channel;
   - resizes it to the chosen width with `Image.Resampling.LANCZOS`;
   - saves `assets/illustrations/thumbnails/<stem>.webp` with a fixed `quality`, a fixed
     `method=6`, and no `exif`, `icc_profile` or `xmp`;
   - removes any `.webp` in `thumbnails/` whose drawing no longer exists.

   With `--check`, the script writes nothing: it renders each thumbnail in memory and
   exits 1 naming every file whose bytes differ from the committed one. Pick the `quality`
   that keeps the drawings' line work clean at 1× and 2×, and say which values you looked
   at.

3. **Add the recipe** to the `Justfile`'s `assets` section, with a comment in the
   section's form:

   ```just
   # Rewrites assets/illustrations/thumbnails/ from the drawings beside it. Run it
   # after a drawing under good/ changes, then `just assets-manifest`.
   thumbnails:
       uv run --frozen python scripts/make_thumbnails.py
   ```

   Also add `thumbnails-check` running the script with `--check`. Whether it joins
   `just check` is an open point, so it does not join it here.

4. **Prove determinism.** Run `just thumbnails` twice and compare `shasum -a 256` of the
   eleven files between the runs. Run `just thumbnails-check` and expect exit 0. Then run
   `just check-assets` before the manifest is written, and expect it to refuse the eleven
   new files as unlisted, which proves the checker sees them.

5. **The manifest.** Run `just assets-manifest`. For each of the eleven new entries, set
   `source` to `rebuilt:<today>` and leave `licence` as `unsettled`, because a derived
   copy inherits its drawing's open question. Run `just assets-manifest` again and expect
   no diff. Read the whole manifest diff: it must add exactly eleven entries and change
   nothing else. Run `just check-assets`.

6. **The gallery.** Each figure's image comes from the thumbnail's import instead of the
   PNG's, with `width` and `height` attributes set from the thumbnail's pixel size so the
   grid does not shift as images load. Keep the first image eager and the rest lazy. The
   PNG files stay imported, so the build still fingerprints them. Each figure gains a
   link to its PNG, in the caption, whose accessible name includes the caption, such as
   "Warm head, resting, full size". Give the size in the visible text if you choose.
   Keep the alt texts as S03 corrected them. Run the `accessibility-review` skill over
   the change: the link must be a real anchor, reachable by keyboard, with a visible
   focus state from the platform's tokens.

7. **Tests.** In `tests/pages.test.ts`, the gallery still has eleven figures. Every `img`
   `src` ends `.webp` (hashed or not, as the build's import resolves under Vitest).
   Eleven links, each queried by role and a name matching its caption, point at a `.png`.
   Query by accessible role and name only.

8. **Measure.** `BASE_PATH=/biscuit_studio just preview`, then Chrome with the cache
   disabled. Record the bytes transferred for `/biscuit_studio/gallery/` before any
   scroll and scrolled to the end, in the form S03 used. Also record that following one
   full-size link serves the PNG with `200`.

9. **Docs and CONVENTIONS.** Add the recipes to `docs/reference/commands.md`, and one
   sentence to `docs/how-to/import-an-asset.md` (a changed drawing needs
   `just thumbnails`). Add one to `docs/how-to/maintain-dependencies.md`: the WebP encoder
   is the libwebp bundled with Pillow's wheels, so a Pillow bump can change every
   thumbnail's bytes. Run `just thumbnails-check` after one, and if it fails, run
   `just thumbnails` and `just assets-manifest` in the same change. In CONVENTIONS.md §11, update "The gallery page is heavy" to give
   the measured before and after. Run `just check-docs`.

10. Run the verification, fill in the hand-back notes, set `status: done`, and commit.
    Pushing and the pull request are authorised separately.

## Acceptance criteria

- [ ] `ls assets/illustrations/thumbnails/*.webp | wc -l` prints `11`.
- [ ] Two runs of `just thumbnails` give identical digests, and `just thumbnails-check`
      exits 0.
- [ ] `git diff main -- assets/manifest.json` adds eleven entries, each with a `source`
      beginning `rebuilt:`, and changes no existing entry.
- [ ] `git diff main --stat -- assets/illustrations/good/` is empty.
- [ ] `just check-assets` is green (every thumbnail passes the metadata rule).
- [ ] The gallery test finds eleven figures, eleven `.webp` images and eleven full-size
      links by name.
- [ ] The scrolled gallery's measured transfer is recorded beside S03's 15,141,024 bytes.
- [ ] `just check` is green.

## Verification

```sh
just thumbnails && shasum -a 256 assets/illustrations/thumbnails/*.webp >| ai_tmp/thumbs-1.txt
just thumbnails && shasum -a 256 assets/illustrations/thumbnails/*.webp | diff - ai_tmp/thumbs-1.txt && echo identical
just thumbnails-check; echo "rc=$?"
git diff main --stat -- assets/illustrations/good/
just check-assets
just frontend-unit
BASE_PATH=/biscuit_studio just frontend-build
ls build/_app/immutable/assets/ | grep -c '\.webp$'
just check
```

Expected: `identical`; `rc=0`; an empty stat; `check_assets check: ok`; the tests pass;
`11`; `just check` ends green with the worktree unchanged. The shell has `noclobber`, so
the first line writes with `>|`. Create `ai_tmp/` first if the worktree has none.

## Hand-back notes

Filled in by the agent that executes this ticket.

- The widest cell measured, the width chosen, and the `quality` chosen, with the values
  compared.
- The eleven thumbnails' byte sizes and their total.
- The gallery's transfer before any scroll and scrolled to the end, beside S03's figures.
- The manifest diff's summary, and the verification output, quoted.
- Anything this ticket finds that belongs to a done ticket, written as an item for a
  follow-up (CONVENTIONS.md §9).

## Open points

- **Whether `thumbnails-check` joins `just check`.** It would catch a drawing changed
  without its thumbnail. But it adds a Pillow render to every run, and the list of
  recipes `just check` runs is in `pyproject.toml` (`[tool.biscuit-games-tooling]`).
  Recommend adding it once the check's cost is measured, and asking the maintainer first.
