---
title: "Decision 0008: The viewer is embedded as-is"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_viewer_embedded]
requires: []
---

# Decision 0008: The viewer is embedded as-is

## Context

The approved model came with its own viewer: a single HTML page, 26 MB, a hand-written
WebGL 2 renderer with no dependency and no network request, every texture and all the
geometry inlined. It carries the approved cel look — the illustrated shading and the
outlines the maintainer approved — and lets a reader pose her with sliders, save a pose and
save a PNG, offline.

The model also exports a 16 MB GLB, which any glTF viewer can open. The GLB carries
standard PBR materials, not the cel shading, so in any other viewer she looks different.

The site had to ship with the model on it. Rewriting the viewer as a Svelte component on a
maintained 3D library, with the cel look reproduced, is a project of its own.

## Decision

Serve the viewer unchanged, as a static file, and port it later.

- `static/pose-studio/viewer.html` is the page `viewer.py` builds, byte for byte except for
  three links. Beside it are the two files it links by relative path,
  `model/biscuit-poseable.glb` and `previews/pose-overview.jpg`, so those links work where
  Pages serves it.
- The three links it makes to files the site does not serve — the `.blend` twice and the
  model's README once — are rewritten to their pages on GitHub, and nothing else is
  changed. The manifest records the viewer's original sha256 as `source_sha256` and lists
  the three rewrites under `patched`.
- The model page links to the viewer rather than framing it inside the site's shell. The
  viewer is its own page.
- A later port to a maintained three.js component, reproducing the cel look, is the
  intended replacement.

## Consequences

**The viewer ignores the platform.** It is its own page, with a cream ground, its own
type and its own controls; it does not wear the platform's tokens or follow its theme or
high contrast. It follows the device's reduced-motion preference on its own terms, by
reading the media query itself rather than the platform's attribute.

**Every rebuild rewrites 26 MB.** The viewer is served, so it is an ordinary blob, and
history keeps every version; see
[Decision 0006](0006-sources-in-lfs-served-files-as-blobs.md).

**Two looks ship.** The viewer shows the approved cel shading and the GLB does not. The
model page says so beside the download, so nobody takes the GLB for the approved look.

**Three links point at `main`.** A branch rename, or a move of the `.blend` or the README,
breaks them inside a file no linter reads. The manifest's `patched` field is where they are
written down.

## What would reopen this

The three.js port landing, which replaces the file. The viewer growing past what Pages
serves comfortably. The hub's rule refusing the cel look the viewer exists to show.

## Related pages

- [Rebuild the model](../how-to/rebuild-the-model.md)
- [Large files](../explanation/large-files.md)
- [Accessibility](../explanation/accessibility.md)
- [Decision 0009: No component workshop yet](0009-no-component-workshop-yet.md)
