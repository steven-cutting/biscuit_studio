---
title: "Decision 0001: A static site with no backend"
kind: "decision"
audience: [maintainer, agent]
canonical_for: [decision_no_backend]
requires: []
---

# Decision 0001: A static site with no backend

*Carried from the Biscuit Games template's decision 0001 at `2283589`, and restated for a repository that is not a game.*

## Context

The studio is a repository of assets and a site that shows them: the approved model, the
illustrations, and a few pages that present them on the platform's design system. The site
has no accounts, no visitors' data and no shared state, and nothing it shows changes
between one visitor and the next. The conventions it inherits arrive by way of the
template and Poodl, and Poodl's came from a full-stack template with a Python backend, a
PostgreSQL database and a generated API client.

## Decision

Build a static site. SvelteKit with `@sveltejs/adapter-static`, every route prerendered,
published to GitHub Pages. No server, no database, no API, no generated client, and no
`frontend/` subdirectory to be a sibling of something that does not exist. The pose studio
is a static file served beside the site, not a route, and it too talks to nothing.

## Consequences

Deployment is a directory of files. There is nothing to operate, nothing to scale,
nothing to patch between releases, and no secret to rotate. Hosting is free.

The site stores nothing. It keeps no setting, no history and no pose in the browser; the
pose studio saves a pose only by downloading a file the reader keeps.

Prerendering has teeth. Module-scope work runs once, at build time, in Node — so anything
per-visitor must happen in the browser after hydration, and a route that cannot be
rendered at build time fails the build rather than shipping. The one per-visitor thing the
site does, following the device's motion and contrast preferences, happens in the layout
after hydration for exactly that reason.

The base path becomes configuration. A project site is served from a subdirectory,
so `BASE_PATH` is read at build time into `paths.base`. Where the value comes from,
and why no domain sits in front of it, is [Decision 0004](0004-a-project-pages-site.md).

Everything the site serves is a file in the build, which is why a large served file has to
be an ordinary Git blob rather than an LFS object; see
[Decision 0006](0006-sources-in-lfs-served-files-as-blobs.md).

## What would reopen this

Anything requiring shared state or a server: uploads from visitors, comments, a
collection of poses shared between readers, or assets served to the games from an API
rather than copied. None is in scope — see
[Purpose and scope](../project/purpose-and-scope.md).

## Related pages

- [Architecture](../explanation/architecture.md)
- [Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md)
- [Decision 0004: A project Pages site](0004-a-project-pages-site.md)
