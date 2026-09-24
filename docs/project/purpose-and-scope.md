---
title: "Purpose and scope"
kind: "project"
audience: [user, contributor, maintainer, agent]
canonical_for: [project_purpose, project_non_goals]
requires: []
---

# Purpose and scope

Biscuit Games is a platform for small, exacting games that run in the browser. This
repository is its studio: the place where the platform's graphical assets are developed
and kept, and a static site that shows them. It is not a game, and it is not the hub.
The hub decides what Biscuit looks like and publishes the design system. The studio
makes the pictures of her that the hub and the games may one day use.

The site runs entirely in the browser. There is no server, no account and no database;
see [Decision 0001](../decisions/0001-static-site-no-backend.md).

## What it does

- **Keeps the approved model.** `assets/models/biscuit/` holds the poseable 3D model of
  Biscuit that the maintainer approved: the native `.blend`, the rig, the four saved poses,
  the packed textures, the QA record and the previews rendered from it. It also holds the
  Blender scripts that build it. The GLB exported from it is served beside the viewer.
- **Keeps the renders and exports made from the model**, and whatever is derived from them
  later, each listed with its source.
- **Keeps the 2D illustrations.** `assets/illustrations/good/` holds the cel set, eleven
  images generated and then vetted by the maintainer, and labelled as generated wherever
  they are shown.
- **Proves every file is what it claims to be.** `assets/manifest.json` records the size,
  the sha256, the storage and the source of every file under `assets/` and
  `static/pose-studio/`, and `just check-assets` refuses anything that disagrees with it.
- **Shows them.** A static site on GitHub Pages at `steven-cutting.github.io/biscuit_studio/`
  presents the model and the gallery, wearing the platform's header, wordmark and
  stylesheet so it reads as the same product as every game. The model page links out to
  the pose studio, the viewer that lets a reader turn and pose her in the browser.
- **Consumes the platform exactly as a game does.** `@steven-cutting/biscuit-games` is
  installed at an exact version, and its tokens, components and preference port are used
  as published. Nothing is copied from it and nothing overrides it.

## What it deliberately does not do

- **It does not decide the character, the aesthetic or a token.** The hub's character and
  design direction pages decide how Biscuit looks and what the platform may show. The
  hub's direction page lists 3D rendering and generated artefacts under Avoid today, and
  the studio's first obligation is a hub decision that permits cel-shaded renders from the
  approved model. Until that decision lands, nothing made here is promoted into the hub or
  a game. A change to the look is made in the hub first; see
  [The platform upstream](platform.md).
- **It does not hold the rebuild chain, the raw photographs or the reference art.** The
  model's earlier studies stay in `biscuit_pics`, cited by path and commit. So do the
  photographs of the real dog and the third-party reference art. See
  [Repository map](repository-map.md) for what was left behind and why.
- **It ships no game, no shared component and no package.** Nothing installs the studio.
  A finished asset leaves by copy, by the procedure on
  [Promote an asset](../how-to/promote-an-asset.md).
- **It runs Blender nowhere in CI.** A rebuild of the model is a documented local recipe
  that the maintainer approves. CI checks the site, the handbook and the asset manifest.
- **It holds no photograph of the real dog** unless the maintainer has approved that
  photograph and every metadata field has been stripped from it. None is held today. See
  [Content policy](../explanation/content-policy.md).

## Who it is for

Three readers. First, the maintainer, who approves the model and decides what leaves.
Second, an agent working here, which needs to know what the studio may change on its own
and what belongs to the hub. Third, the hub or a game that wants an asset: it takes one by
copy, following [Promote an asset](../how-to/promote-an-asset.md), and records where the
copy came from.

## Related pages

- [The platform upstream](platform.md), which is also where to find what the hub owns
- [Repository map](repository-map.md)
- [Content policy](../explanation/content-policy.md)
- [Architecture decisions](../decisions/README.md)
