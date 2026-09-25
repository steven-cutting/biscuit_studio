---
name: asset-change
description: Import or rebuild an asset under assets/ and record it in the manifest with its source.
---

# Import or rebuild an asset

1. Read `AGENTS.md`, then `docs/how-to/import-an-asset.md` for a file arriving from outside, or `docs/how-to/rebuild-the-model.md` for a file the Blender pipeline regenerates. `docs/explanation/content-policy.md` says what may never arrive at all, and `docs/explanation/large-files.md` says which paths Git LFS holds.
2. If the file is a photograph of the real dog, stop. Each one needs the maintainer's approval, named, before it is copied, and every metadata field stripped before it is committed. Approval for one is not approval for the next.
3. Copy the bytes with `cp`, never by re-encoding. Check the sha256 against the source with `shasum -a 256` before and after; a source in another repository is cited as `<repository>@<commit>:<path>`.
4. Check `git check-attr filter <path>`: `lfs` for a native source, `unspecified` for anything the site serves. A served file that reports `lfs` is a defect in `.gitattributes`, not in the file, and it is handed back rather than worked around.
5. Run `just assets-manifest`, then read the manifest's diff. New entries carry `source: studio` and `licence: unsettled` until you set the source; set it now. A rebuilt file's `source` is `rebuilt:<date>`. Never change a `source` the tool preserved unless the bytes genuinely came from somewhere else. A file patched after import or build carries `source_sha256` and `patched` together; the viewer's `source_sha256` is read from `qa/viewer-package.json` by the tool and proved by the checker, never written by hand.
6. Run `just check-assets`. A refusal naming EXIF means a metadata field beyond the image's resolution is left in it, location and camera identity included: strip every field outside the repository and copy again, or do not commit it. A refusal naming TIFF means the format cannot be inspected: export it as PNG.
7. Say in the commit message what arrived, from where, and at what commit. Run `just check` before handing back.
