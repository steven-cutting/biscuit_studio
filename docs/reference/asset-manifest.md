---
title: "Asset manifest"
kind: "reference"
audience: [contributor, maintainer, agent]
canonical_for: [asset_manifest_format]
requires: []
---

# Asset manifest

`assets/manifest.json` records every asset the studio holds: its size, its sha256, which
storage Git keeps it in, where it came from and under what licence. `scripts/check_assets.py`
is the one program that reads and writes it. This page is the format, the checker's
subcommands and every refusal it prints, and the limit of what it proves.

## The file

`assets/manifest.json` is strict JSON: an object with `schema_version`, which is `1`, and
`assets`, a list of entries. Each entry is written on one line, the list is sorted by `path`,
and the file ends in exactly one newline. Prettier ignores it and the `check-json` hook
parses it, so a hand edit that breaks the JSON fails the hook gate before the checker reads
it.

Every file under `assets/` and `static/pose-studio/` has an entry, except
`assets/manifest.json` itself. Nothing else is listed: `tests/fixtures/exif-gps.jpg` is a test
input, not an asset. Today the manifest lists 105 files.

## An entry

```json
{"path": "static/pose-studio/model/biscuit-poseable.glb", "bytes": 16112380, "sha256": "51d16c1826b2c3ad6ad85fcb176a73e0d1c7a0ac3665ad10f1b6700e9e9be716", "storage": "blob", "source": "biscuit_pics@1d9d358:models/biscuit/model/biscuit-poseable.glb", "licence": "unsettled"}
```

Six fields are required, in this order:

| Field | Type | Meaning |
| --- | --- | --- |
| `path` | string | Repository-relative, forward slashes. |
| `bytes` | integer | The size of the committed file; for an LFS file, the object's size as its pointer states it. |
| `sha256` | string | 64 lowercase hex digits: the digest of the committed bytes; for an LFS file, the object's, read from the pointer's oid. |
| `storage` | string | `blob` or `lfs`, and it must agree with what `.gitattributes` says for the path. |
| `source` | string | Where the file came from, in one of three forms below. |
| `licence` | string | `unsettled` until the licence question is answered. |

`source` is written in one of three forms. The checker requires the field to be present and
not empty and reads nothing else in it, so the form is a convention that review holds, not
one the gate enforces; `"source": "unknown"` would pass `just check-assets`:

- `<repository>@<commit>:<path>` — imported, from that path in that repository at that
  commit. Every entry today reads `biscuit_pics@1d9d358:` followed by its path there.
- `rebuilt:<date>` — regenerated here by a rebuild on that date.
- `studio` — made here. It is what `write` gives a new file, and a person replaces it when
  the file came from elsewhere.

`licence` is `unsettled` on every entry, because the licence of the studio's assets is not
decided; the field exists so that the answer, when it comes, is a diff a person can review.
[Content policy](../explanation/content-policy.md) owns the question.

Two optional fields are present only where true, and always together:

| Field | Type | Present when |
| --- | --- | --- |
| `source_sha256` | string | The committed bytes differ from the source's. 64 lowercase hex digits, never equal to `sha256`. For a `rebuilt:` entry the source is the build output, so it is the digest of the file before any patch the rebuild applies. |
| `patched` | list of strings | The same condition. A non-empty list of non-empty strings, each saying what changed. |

Two entries carry them today. The viewer's `patched` lists its three rewritten links and that
nothing else differs, and its `source_sha256` is the unpatched page's digest, which the build
also records as `sha256` in `assets/models/biscuit/qa/viewer-package.json`; the checker reads
that record and refuses a mismatch. The model's README carries them because its links and a
provenance section were adapted to this repository.

## The checker

`scripts/check_assets.py` takes one subcommand. Run it from anywhere inside the worktree; run
outside one, it prints `check_assets: run this from inside a Git worktree` and exits 2.

**`check`** is what `just check-assets` runs. It runs `self-test` first, then walks
`assets/` and `static/pose-studio/` and compares them with the manifest. Each finding is one
line on standard error, `<path>: <reason>`; after the last it prints
`check_assets check: <n> finding(s)` and exits 1. With no finding it prints
`check_assets check: ok` and exits 0. The reasons, word for word:

| Reason | Refused because |
| --- | --- |
| `present but not listed; run just assets-manifest` | A file under either root has no entry. |
| `listed in the manifest but absent from the worktree` | An entry names a file that is gone. |
| `sha256 differs from the manifest; run just assets-manifest and read the diff` | A byte changed. |
| `size differs from the manifest` | The size changed; a changed size always changes the digest too, so this arrives with the line above. |
| `storage must be blob or lfs` | `storage` holds anything else. |
| `storage 'lfs' but .gitattributes says 'blob'` | The entry and `.gitattributes` disagree, either way round. |
| `manifest entry lacks <field>` | A required field is missing. |
| `unknown manifest field(s) [...]` | A field outside the eight is present. |
| `carries EXIF (<tags>); strip every metadata field before committing` | An image carries a tag beyond its resolution; every tag found is named, `GPSInfo` included. |
| `a TIFF, whose structure is stored as EXIF tags and cannot be told from metadata; export it as PNG` | A `.tif` or `.tiff`, whatever it holds. |
| `not a readable image (...)` | A raster suffix Pillow cannot open. |
| `source_sha256 and patched go together` | One optional field without the other. |
| `source_sha256 must be 64 lowercase hex digits` | A malformed digest. |
| `source_sha256 equals sha256, so nothing was patched; remove both fields` | The two digests agree. |
| `patched must be a non-empty list of non-empty strings` | An empty list or an empty item. |
| `source_sha256 must equal the sha256 in assets/models/biscuit/qa/viewer-package.json; run just assets-manifest` | The viewer's digest disagrees with its build record. |

One finding names the build record rather than an asset:
`assets/models/biscuit/qa/viewer-package.json: carries no readable sha256 for
static/pose-studio/viewer.html`, when the record is present but holds no usable digest.

A manifest that cannot be read at all is one finding against `assets/manifest.json` itself,
naming the error — `schema_version must be 1`, a path listed twice, or the JSON parser's
message.

**How an LFS file is verified.** A file Git LFS tracks is checked out as a pointer unless the
object was fetched: three lines, the LFS specification's version line, `oid sha256:<hex>` and
`size <bytes>`. The checker reads those two values from the pointer and compares them with
the entry, so a checkout that never fetched an object passes exactly as one that did. When
the object is present instead, it hashes the bytes, which gives the same digest. That is why
every CI checkout is `lfs: false` and no job fetches an object.

**The EXIF rule.** Every file with a raster suffix — `.png`, `.apng`, `.jpg`, `.jpeg`, `.jpe`,
`.jfif`, `.mpo`, `.webp`, `.gif`, `.bmp`, `.avif`, `.heic`, `.heif` — is opened with Pillow and
its EXIF read. Three tags in the first image directory are allowed: `XResolution` (`0x011A`),
`YResolution` (`0x011B`) and `ResolutionUnit` (`0x0128`), because four of the model's native
renders carry exactly the first two. Any other tag there is refused, and so is anything at
all in the Exif directory (`0x8769`) — the camera, the date, the lens — or the GPS directory
(`0x8825`). A TIFF is refused outright, because a clean TIFF stores ten structural tags in the
same directory and metadata cannot be told from structure.

**`write`** is what `just assets-manifest` runs. It recomputes every entry from the worktree
and rewrites the file. It keeps `source`, `licence`, `source_sha256` and `patched` from the
existing entry where there is one, writes `source: "studio"` and `licence: "unsettled"` for a
new file, and reads the viewer's `source_sha256` from its build record whenever that record
is present. Then it compares the tree with the manifest it has just written, as `check` does,
and exits with that status, printing `check_assets write: ok` on success. It does not run
the self-test first, so a clean `write` is not proof that the checker is live; run
`just check-assets` for that. It never deletes a `source`.

**`self-test`** builds a temporary Git repository and proves the checker is live against it:
a blob, a hand-written LFS pointer and a clean PNG pass; `tests/fixtures/exif-gps.jpg` is
refused naming `GPS`; a JPEG with only a capture date and a WebP with only a software tag are
refused naming `EXIF`; a PNG with only its resolution and a clean WebP pass; a TIFF is refused;
the optional fields are checked for shape and against a build record; and one changed byte
is refused. [Testing](testing.md) says why this is the checker's test rather than a pytest
suite.

## What it does not prove

**A rewritten manifest passes.** `write` recomputes every hash from the worktree, so a
tampered asset followed by `just assets-manifest` produces a manifest that agrees with it.
`check-assets` is only as honest as the manifest, and the manifest is only as honest as its
review. The guard is a person reading the diff of `assets/manifest.json` on every import and
every rebuild — a changed `sha256` on a file nobody meant to change is the finding — and the
`source` field, which the tool never rewrites.

**It does not see how a file was stored.** It compares `storage` with what `.gitattributes`
says, not with what Git actually stored. A contributor on a machine without git-lfs who
commits a changed `.blend` stores the real file as an ordinary blob; `.gitattributes` still
names the path and the bytes still hash to the oid, so the check passes. git-lfs is installed
once per machine and `git lfs install --local` runs in each clone;
[Troubleshooting](../operations/troubleshooting.md) says how to spot the slip.

**It cannot tell a permitted image from a forbidden one.** A stripped photograph of the real
dog passes. [Content policy](../explanation/content-policy.md) is enforced by review.

## The recipes

- `just check-assets` — `check`, with the self-test first. Part of `just check` and the
  `assets` job in CI.
- `just assets-manifest` — `write`, then the same tree comparison, without the self-test. The
  one recipe that writes the manifest.
  Read its diff before committing.

## Related pages

- [Import an asset](../how-to/import-an-asset.md)
- [Large files](../explanation/large-files.md)
- [Content policy](../explanation/content-policy.md)
- [Commands](commands.md)
