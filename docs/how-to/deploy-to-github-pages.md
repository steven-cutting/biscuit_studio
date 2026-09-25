---
title: "Deploy to GitHub Pages"
kind: "how-to"
audience: [maintainer, operator, agent]
canonical_for: [deployment_procedure]
requires: []
---

# Deploy to GitHub Pages

This repository publishes to GitHub Pages from `.github/workflows/pages.yml`, after CI has
passed on a push to `main`. Its one job calls `game-pages.yml` in
`steven-cutting/biscuit_games_tooling`, at a pinned release, which builds the static site
and hands `build/` to the Pages deployment action; nothing is committed to a branch.

The site is a project site, served at `stevencutting.com/biscuit_studio/`: the repository
`steven-cutting/biscuit_studio`, beneath `/biscuit_studio/` on its owner's Pages host. That
host is `stevencutting.com` rather than `steven-cutting.github.io` because the account's
user site carries that custom domain, and GitHub serves every project site of the account
beneath the user site's domain; `steven-cutting.github.io/biscuit_studio/` answers with a
redirect to it. HTTPS is enforced in the repository's Pages settings, which the bootstrap
script does not apply.

## One-time setup

A new repository starts from nothing, so the Pages source is set once, before the first
push that should deploy: in the repository settings, under Pages, set the source to
**GitHub Actions**. The workflow cannot do this for itself.

No package grant is needed. The platform package is public, so the build job's own token
can install it without the repository being given access to the package.

The repository's own `scripts/bootstrap_repo.sh` applies that setting with `gh`, together
with the branch protection requiring the three CI checks and the vulnerability-reporting
setting the rest of this handbook assumes:

```console
scripts/bootstrap_repo.sh steven-cutting/biscuit_studio --checks frontend,documents,assets
```

Without `--apply` it prints what it would change and changes nothing. Each run with
`--apply` changes a repository setting, which is an action the maintainer authorises
each time rather than once. `--checks` is passed because the script's default names a
game's check contexts, and the studio's are the three bare job names.

The deploy job names a `github-pages` environment, which needs no setup: GitHub creates it
on the first run that reaches that job. Until the Pages source is set, the build job
succeeds and uploads its artefact but the deploy job fails with
`Failed to create deployment (status: 404)`, even though the workflow itself is correct.

## Where the site is served from

A project site lives beneath the repository's name on the owner's Pages host, so the app is
built to live under `/biscuit_studio`. The workflow reads that name from the event that
triggered it rather than carrying it in the file, which keeps the address out of
`pages.yml` and keeps `paths.base` in `svelte.config.js` from drifting away from the
address Pages serves. A custom domain is a later change to the repository settings and to nothing here;
[decision 0004](../decisions/0004-a-project-pages-site.md) records why the project site is
the starting point.

## What the site serves

Everything beneath `/biscuit_studio/`:

- the three routes: the home page, `model/` and `gallery/`;
- `pose-studio/viewer.html`, the pose studio;
- `pose-studio/model/biscuit-poseable.glb`, the portable model the viewer and the model
  page link;
- `pose-studio/previews/pose-overview.jpg`, the overview sheet the viewer links;
- and the illustrations the gallery imports, which the build fingerprints under `_app/`.

## What the workflow does

- Waits for CI. It runs on `workflow_run` when the workflow named `CI` completes on
  `main`, and its job runs only when that run succeeded, was triggered by a push, and
  tested the commit that was the head of `main` when CI finished. Branch protection does
  not bind administrators, so without this a direct push would publish a commit nothing
  checked.
- Passes a slash and the repository name, read from the event, to the shared workflow as
  its `base_path` input, and the shared workflow sets `BASE_PATH` from it, so the build
  cannot drift from where Pages serves it.
- Checks out without LFS objects, which is the checkout action's default. That is correct
  because nothing the site serves is LFS-tracked: the `.blend` and the two large QA
  records never leave `assets/`.
- Builds with `npm run build`, which is `just frontend-build`.
- Uploads `build/` as the Pages artefact. `static/.nojekyll` rides along so Pages serves
  the underscore-prefixed `_app/` directory rather than treating it as a Jekyll internal.
- Deploys it in a second job that holds the `pages: write` and `id-token: write` scopes.
  The job that builds holds `contents: read` and `packages: read` and neither publishing
  scope, so the credential that installs and the credential that deploys never meet.

Deployments are serialised by a concurrency group and are never cancelled mid-flight: a
half-published site is worse than a slightly stale one.

What the gate costs: there is no manual deploy, because a manual run would skip CI;
nothing deploys while CI is red; a push that CI passes after a newer push has landed is
skipped, and the newer one deploys itself; and renaming the `name: CI` line in `ci.yml`
stops every deploy silently, which a comment in `pages.yml` says beside the trigger.

One risk the checkout makes silent: the LFS patterns in `.gitattributes` name sources by
path, so a rename that moved a served file under a pattern — beneath
`assets/models/biscuit/qa/geometry/`, say, or any `.blend` — would deploy the pointer text
in its place, and the build would not fail. [Large files](../explanation/large-files.md)
is the policy that keeps served files out of LFS.

## Reproduce a deployment locally

```console
BASE_PATH=/biscuit_studio just frontend-build
BASE_PATH=/biscuit_studio just preview
```

The base path goes on both commands, so the preview sits where Pages serves. See
[Configuration](../reference/configuration.md).

## Rolling back

Re-run the last good deployment, from the Actions tab or with `gh run rerun` and the
run's id, or revert the commit and let CI and the deploy that follows it publish a fresh build. There is no state
to migrate and no cache to clear beyond the browser's.

## Related pages

- [Decision 0004: A project Pages site](../decisions/0004-a-project-pages-site.md)
- [Architecture](../explanation/architecture.md)
- [Configuration](../reference/configuration.md)
- [Maintenance](../operations/maintenance.md)
