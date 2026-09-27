---
title: "Maintenance"
kind: "operations"
audience: [maintainer, operator, agent]
canonical_for: [maintenance_routine]
requires: []
---

# Maintenance

There is no service to operate. Nothing runs, nothing accumulates, and there is no on-call:
the site is a directory of files GitHub Pages serves, and the viewer is one of those files.
What follows is upkeep of the repository, of the site's deploys, of the assets that leave
it, and of the links that cross between it and the hub.

## Routine

**Weekly.** Read any failing run of `ci.yml` or `pages.yml`. Nothing is scheduled — neither
workflow carries a `schedule:` trigger — so a failure means a push or a pull request met a
gate, or a deploy did not publish. A red `pages.yml` run leaves the previous deploy serving,
so the site is stale rather than broken; [Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md)
says how to rerun it.

**Monthly.** Run `just check-links-online`. It is the only check on the links into the hub,
and it has its own section below.

**Monthly.** Review dependency versions. Every pin is exact, so nothing moves on its own and
nothing is picked up by accident either. Nothing opens a bump for you: there is no Dependabot
or Renovate configuration here. Follow
[Maintain dependencies](../how-to/maintain-dependencies.md), and check compatibility before
choosing a version: `typescript-eslint` 8.66.0 declares support for TypeScript below 6.1, so
the pinned TypeScript 6.0.3 is inside its range and a TypeScript release at or past 6.1 waits
for a linter that accepts it.

**Per change.** An asset that has already left, or a rebuild of the model, is not a calendar
item but a step in the change itself. Both are below.

## Checking the links to the hub

```console
just check-links-online
```

This is the only thing in the repository that resolves a cross-repository link, and it is run
by hand. Three facts stack up behind that sentence:

- **The documentation contract skips external links entirely.** `bg-validate-docs` ignores
  any absolute URL, and any `mailto:`, so the exact-case, must-resolve rule that governs
  every internal link does not apply to a link that leaves the repository.
- **The offline link checker skips them too.** The lychee run inside `just check-docs`, and
  the identical one in the commit hook, pass `--offline`.
- **This recipe is the same lychee run with the network.** It is registered as a manual hook
  stage, so it is not part of `just check` — a check that can fail because a third party is
  down is not a gate. [Quality gates](../reference/quality-gates.md) says the same thing from
  the other direction.

The links it matters for are the hub pages on
[The platform upstream](../project/platform.md), the one page here allowed to carry them.
They are GitHub blob URLs to whole pages, because the hub's handbook is published nowhere.
A failure means a page moved or was renamed in the hub. Nothing on either side goes red when
that happens: the rot is silent, and it lasts until somebody runs this recipe — a month at
best. That is the standing price of one authoritative copy bought with links no machine
maintains.

When the recipe reports a failure, fix the link on the platform page if the hub's page simply
moved. If the failure means the hub changed something the studio relies on, write the item
into [Hub handover](hub-handover.md) and change nothing in the hub.

Three other links leave the site for this repository's own files on GitHub: two in the
viewer, to the Blender scene and the model's README, and one on the model page, to the
Blender scene. Not even this recipe follows them, because lychee reads Markdown and the three
sit in HTML and Svelte. They point at `main`, so a branch rename or a move under
`assets/models/biscuit/` breaks them silently; after either, open them by hand.

## Per change to an asset that has left

Once an asset has been promoted — copied into the hub or a game — a rebuild or a replacement
of it here is a change to something a consumer holds a copy of, even though no build anywhere
depends on this repository. The copy there does not update, and nothing there notices. Before
the change lands:

1. Run the `hub-handover` skill. It asks which consumer holds a copy, at which studio commit
   and sha256, and what the change means for it.
2. Write the item into [Hub handover](hub-handover.md), in that page's own register: what
   changed here, which copy it affects, and what the consumer would have to do to take it.
3. Change nothing in the other repository. Editing another repository needs explicit
   authorization for each action, and approval for one action is not approval for the next.
   This repository records; it does not act.

Nothing has been promoted yet, so today this section describes a step nobody has taken.

## Per rebuild of the model

A rebuild follows [Rebuild the model](../how-to/rebuild-the-model.md) and replaces the
approved model only when the maintainer approves the result. Weigh the cost before starting:
every rebuild adds the viewer's 29 MB and the GLB's 16 MB to ordinary history, and another
40 MB of LFS objects to storage, and none of it can be taken back without rewriting history.
After an approved rebuild, read the manifest's diff whole, check that every changed entry
says `rebuilt:` with the date, and, if anything rebuilt has already left, take the step above.

## Secrets

There are none. No workflow holds a stored secret, and there is no deployment credential to
rotate or create: `pages.yml` deploys with the run's own token under `pages: write` and
`id-token: write`, and CI installs the platform package with the run's own token under
`packages: read`. Each token is minted for its run and discarded with it.

The one credential in play lives outside the repository: the read token for GitHub Packages,
in `~/.npmrc` on each developer's machine. It is long-lived, so it belongs on the rotation
list beside `just check-links-online`; replace it when it expires or leaks, and never copy
it into a file here. See [Security model](../explanation/security-model.md).

## Related pages

- [Hub handover](hub-handover.md)
- [Troubleshooting](troubleshooting.md)
- [Maintain dependencies](../how-to/maintain-dependencies.md)
- [Security model](../explanation/security-model.md)
