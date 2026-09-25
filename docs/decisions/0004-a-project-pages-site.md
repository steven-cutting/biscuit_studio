---
title: "Decision 0004: A project Pages site"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_project_pages_site]
requires: []
---

# Decision 0004: A project Pages site

*Carried from the Biscuit Games template's decision 0010 at `2283589`, and restated for a repository that is not a game.*

## Context

GitHub Pages serves a project site at `<owner>.github.io/<repository>/`, with the account
lowercased in the host. Only a user site, or a site with a custom domain, is served from
the root of a domain.

Poodl's record on its address chose a domain of its own, with a landing page in front of
the game and a step that assembled the domain around the build. That domain, `pnut.fans`,
stays with Poodl, and the hub's own decision 0012 is where the platform deferred any
domain of its own.

The studio has to publish with no domain, no DNS records and nothing to stage, and it
serves three files larger than anything a game serves.

## Decision

The studio is a project Pages site at `stevencutting.com/biscuit_studio/`.

`.github/workflows/pages.yml` calls the tooling repository's `game-pages.yml` with
`base_path` set to a slash and the repository name, read from the workflow event as
`github.event.repository.name`, so the build runs with `BASE_PATH=/biscuit_studio` and
uploads `build/`. The file never carries the name. `svelte.config.js` reads `BASE_PATH`
into `paths.base`, and it is empty locally. `static/.nojekyll` rides along so that Pages
serves `_app/`.

There is no custom domain on this repository. The host is the account's: a project site is
served beneath the user site's domain, which is `stevencutting.com`, so the first deploy
landed there and `steven-cutting.github.io/biscuit_studio/` redirects to it. Adding a
domain of this repository's own later is a change to the repository settings and to
`base_path` in the workflow, and to nothing else. Moving the whole platform to `pnut.fans`
is the hub's move, deferred by its decision 0012, and the studio follows it when it comes.

## Consequences

**One setting comes before the first push.** The Pages source is set to GitHub Actions in
the repository settings; until it is, the build job succeeds and uploads its artefact but
the deploy job fails with `Failed to create deployment (status: 404)`. No package grant is
needed, unlike the template's first record: the hub package is public, so the build job's
own token installs it.

**The address in this handbook is prose.** It is written by hand, so a mismatch with the
repository's real name is invisible to every gate, while `pages.yml` stays correct
because it reads the event.

**Every path the app builds goes through `paths.base`.** A link or an asset written from
the root works locally, where the base is empty, and breaks only once it is published
beneath the repository's name. The pose studio links its own GLB and overview image by
relative path, which is why those files sit beside it.

**Nothing outside `build/` is published.** There is no landing page, no second copy of a
stylesheet and no staging script to keep true.

**The build checks out without LFS objects, so nothing served may ever be LFS-tracked.**
The checkout fetches pointers, not objects; a served file under an LFS pattern would be
published as pointer text, and the build would not notice. See
[Decision 0006](0006-sources-in-lfs-served-files-as-blobs.md).

**The deploy runs after CI, not beside it.** `pages.yml` runs on `workflow_run` when `CI`
completes, and publishes only a push to `main` that CI passed and that was the head of
`main` when CI finished. This is a deliberate deviation from the template, whose workflow
deploys on every push: branch protection does not bind administrators, so a direct push
would otherwise publish a commit nothing had checked. It costs a manual deploy — a redeploy
is a rerun of a gated run — and renaming the workflow `CI` stops every deploy without an
error.

## What would reopen this

A custom domain for the studio. The platform serving the studio, with its games, beneath
a domain of its own; the hub's decision 0012 is where that is deferred.

## Related pages

- [Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md)
- [Configuration](../reference/configuration.md)
- [Decision 0001: A static site with no backend](0001-static-site-no-backend.md)
