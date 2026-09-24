---
title: "Asset manifest"
kind: "reference"
audience: [contributor, maintainer, agent]
canonical_for: [asset_manifest_format]
requires: []
---

# Asset manifest

This page will own the format of `assets/manifest.json`: strict JSON, one entry per line
sorted by path, the six required fields (path, bytes, sha256, storage, source and licence)
and the two optional ones (source sha256 and patched), how an LFS entry is verified from
its pointer, which images the checker refuses for their EXIF, and the one recipe that is
allowed to write the file.
