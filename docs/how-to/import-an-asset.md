---
title: "Import an asset"
kind: "how-to"
audience: [contributor, maintainer, agent]
canonical_for: [asset_import_procedure]
requires: []
---

# Import an asset

An import brings a file into `assets/` or `static/pose-studio/` from outside the
repository, byte for byte, with a record of where it came from. It is the only way a file
enters either tree other than a rebuild of the model, which has
[its own page](rebuild-the-model.md). The procedure is short; most of it is deciding
whether the file may come in at all, and reading what the manifest says about it
afterwards.

## Before anything

Read [Content policy](../explanation/content-policy.md) first. It decides what may be
committed, and a file it refuses is refused however useful it would be:

- Nothing from `inspiration/` in `biscuit_pics`: it is third-party copyrighted reference
  art, kept as style reference only.
- No photograph of the real dog unless the maintainer has approved that photograph, one
  at a time, and every metadata field has been stripped from it. Copying one is a
  separately authorised action: stop and ask before the `cp`, not after.
- No commercial font, including the two under `biscuit_pics`'s dialogue work.
- Generated art is labelled as generated wherever it is shown.
- The licence of the studio's own assets is not yet decided. Every entry carries
  `"licence": "unsettled"` until the maintainer decides; an import does not decide it.

## Where it goes

A **source** — something the site never serves — goes under `assets/`: a model in
`assets/models/<name>/`, an illustration in `assets/illustrations/<set>/`. A **served
file** goes under `static/pose-studio/`, beside whatever links it, or under `assets/` if a
route imports it and the build fingerprints it.

[Large files](../explanation/large-files.md) decides whether a path goes through Git LFS. A
source over a few megabytes that a rebuild rewrites whole goes through LFS, by a pattern
in `.gitattributes`. Anything the site serves never does, because Pages serves an LFS
pointer as text. The patterns are already written; a new one is a change to the policy
page and to `.gitattributes` together, decided on its own, never slipped in with an
import.

## The procedure

1. **Copy the bytes, and only the bytes.** Use `cp` from a source you treat as read-only.
   Do not open and re-save the file, re-encode it or let an editor touch it: the manifest
   records the sha256 of exactly what is committed.
2. **Record the source commit.** For a file from another repository:

   ```console
   git -C <source checkout> rev-parse HEAD
   ```

   Check the copy against the original with `shasum -a 256` on both.
3. **See which storage applies.** `git lfs track` is never run by hand; the patterns are
   already in `.gitattributes`. Ask Git which one the path matches:

   ```console
   git check-attr filter <path>
   ```

   `filter: lfs` means LFS; `filter: unspecified` means an ordinary blob. Git LFS itself
   must be installed on the machine, and `git lfs install --local` run in this clone —
   `just initialize` does it. Without it a path LFS should hold is added as an ordinary
   blob, which the checker reports by reading the index: nothing is visible before
   `git add`, and after it `just check-assets` refuses the path.
4. **Watch the checker refuse it.**

   ```console
   just check-assets
   ```

   It names the new file and exits 1:

   ```text
   <path>: present but not listed; run just assets-manifest
   check_assets check: 1 finding(s)
   ```

5. **Write its entry.**

   ```console
   just assets-manifest
   ```

   This is the one recipe that writes `assets/manifest.json`. It recomputes every entry
   from the worktree and gives a new file `"source": "studio"` and
   `"licence": "unsettled"`.
6. **Set the source.** Edit the new entry's `source` to
   `<repository>@<commit>:<path>` — for example `biscuit_pics@1d9d358:good/warm-head.png`.
   `studio` is correct only for a file made here. This field, and only this one, is
   written by a person: the tool keeps it from then on and never rewrites it.
7. **Read the whole manifest diff.**

   ```console
   git diff assets/manifest.json
   ```

   Expect one added line per imported file and nothing else. A changed hash on a file you
   did not touch is a stop-and-read, not something to commit.
8. **Check, then run the gate.**

   ```console
   just check-assets
   just check
   ```

The manifest is only as honest as the review of its diff. `just assets-manifest` hashes
whatever is in the worktree, so a tampered file and a rewritten manifest pass the checker
together. And because the tool never rewrites `source`, a wrong source stays wrong until a
person fixes it. Step 7 is the guard for both.

## What the checker refuses

`just check-assets` prints every finding as `<path>: <reason>` and exits 1 if there is any.
It refuses:

- a file under `assets/` or `static/pose-studio/` with no entry, and an entry with no file;
- a blob whose size or sha256 differs from its entry;
- an LFS pointer whose `oid` or `size` disagrees with the entry — the pointer is read,
  so a checkout without the LFS objects is still verified, and the object is hashed
  instead when it is present;
- an entry whose `storage` disagrees with what `git check-attr` says for its path;
- an image carrying any EXIF beyond its resolution: GPS, camera, date, software, anything
  in the Exif or GPS directories, each tag named;
- a TIFF, outright, and an image with a raster suffix Pillow cannot open.

The details of each field are on [Asset manifest](../reference/asset-manifest.md).

## Images

Every raster image — `.png`, `.jpg` and `.jpeg` among a dozen suffixes — is opened with
Pillow and its EXIF read. Only `XResolution`, `YResolution` and `ResolutionUnit` are
allowed, because a few native renders carry them and nothing else.

An image the maintainer approved but that carries metadata is stripped before it is
copied in. Pillow does it: `Image.open(p).save(q)` with no `exif` argument writes none.
Check the result with `just check-assets` rather than trusting the save. exiftool is not a
dependency here, and no other tool is needed.

Stripping re-encodes the file, so the committed bytes differ from the source's: record the
original digest as the entry's `source_sha256`, and say what was done in `patched`.

## Related pages

- [Asset manifest](../reference/asset-manifest.md)
- [Large files](../explanation/large-files.md)
- [Content policy](../explanation/content-policy.md)
- [Rebuild the model](rebuild-the-model.md)
- [Promote an asset](promote-an-asset.md)
