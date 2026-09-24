---
title: "Terminology"
kind: "project"
audience: [contributor, maintainer, operator, agent]
canonical_for: [project_terminology]
requires: []
---

# Terminology

These words mean one thing here. Some come from the platform, some name the studio's own
files, and the rest name the arrangement between this repository and the hub and games it
serves. Using them loosely is how a review ends up arguing about vocabulary instead of
behaviour.

## The platform

| Term | Meaning |
| --- | --- |
| Platform | Biscuit Games: the games, the design system they share, and the decisions they hold in common. A family, not something you play. |
| Hub | The repository `steven-cutting/biscuit_games`, which decides the aesthetic, the character and the tokens, and publishes them. The studio's upstream; see [The platform upstream](platform.md). |
| The package | `@steven-cutting/biscuit-games`, what the hub publishes: the token stylesheet, the typefaces, the icons, the shared components, the ports and their fakes, and the platform's specifications. Installed here at an exact version. |
| Game | One playable thing on the platform, in a repository of its own. The studio is not one. |
| Design system | The tokens and components the package carries. The studio wears it and adds nothing to it. |
| Token | A named value in the package's stylesheet: a colour, a space, a type step, a duration, a font face. Components name tokens. They do not write the values. |
| The four combinations | Dark and light theme, each with and without high contrast. Every surface stays legible in all four. |
| Specifications | The platform's three Allium modules, installed with the package. They decide how a surface looks, how it is worked and what a surface played on owes. The studio restates none of them and adds none of its own. |
| Studio | This repository: where the platform's graphical assets are developed and kept, and the static site that shows them. |
| Approved model | What `assets/models/biscuit/` holds: the poseable 3D Biscuit the maintainer approved, with its rig, poses, textures, QA record and build scripts. Only the maintainer replaces it. |
| Viewer, or pose studio | `static/pose-studio/viewer.html`, a self-contained WebGL 2 page for turning and posing the model, served unchanged and linked from the model page. See [Decision 0008](../decisions/0008-the-viewer-is-embedded-as-is.md). |
| The manifest | `assets/manifest.json`: one entry per file under `assets/` and `static/pose-studio/`, carrying its size, sha256, storage, source and licence. Written only by `just assets-manifest`. |
| Source | An asset the site never serves, kept under `assets/`. A large one that a rebuild rewrites goes through Git LFS. Not to be confused with an entry's `source` field, which says where a file came from. |
| Served file | A file the site delivers as it is: the three under `static/pose-studio/`, and the illustrations the gallery imports. Always an ordinary Git blob, because Pages cannot serve an LFS object. |

## The repository

| Term | Meaning |
| --- | --- |
| Gate | A check that can fail the build. Listed in [Quality gates](../reference/quality-gates.md). |
| Recipe | A `Justfile` target. The only supported way to run anything. |
| Lane | One of the tickets the studio was first built in, each touching its own files so several could run side by side. The word survives in the hand-back notes under `tickets/`. |
| Port | The interface a side effect sits behind, with a real adapter and an in-memory fake beside it. The studio uses the preferences port the package exports, and any side effect it adds gets a port of its own. |
| Fake | The in-memory implementation of a port, used by tests. Not a mock: it behaves, rather than recording calls. |
| Import | Bringing a file into `assets/` or `static/pose-studio/` from outside, byte for byte, with its source recorded. See [Import an asset](../how-to/import-an-asset.md). |
| Rebuild | Regenerating the approved model and the viewer from the model's own scripts and the earlier studies, locally and only with the maintainer's approval. See [Rebuild the model](../how-to/rebuild-the-model.md). |
| Promotion | A finished asset leaving the studio for the hub or a game, by copy, recorded on both sides. See [Promote an asset](../how-to/promote-an-asset.md). |

## Related pages

- [The platform upstream](platform.md)
- [Repository map](repository-map.md)
- [Asset manifest](../reference/asset-manifest.md)
