---
title: "Develop locally"
kind: "how-to"
audience: [contributor, maintainer, agent]
canonical_for: [local_development]
requires: []
---

# Develop locally

## Prerequisites

| Tool | Why |
| --- | --- |
| Node 26 | Runs the site, Vite and Vitest. |
| npm 11 | The package manager. Nothing else is supported. |
| `uv` | Provides the pinned Python tooling the hook gate and the asset checker run on. |
| `just` | The task runner, and the only supported interface to the checks. |
| `git-lfs` | Installed once per machine; `git lfs install` must then have run in the clone, and `scripts/initialize.sh` runs it. A clone made without it holds pointer text where `assets/models/biscuit/model/biscuit-poseable.blend` should be. |
| A GitHub token with `read:packages` | The design system is installed from GitHub Packages, which authenticates every request. |

`package.json` states the supported ranges in `engines` and the exact Node and npm in
`volta`, so a Volta user gets the right Node automatically. `.python-version` names the
Python that `uv` runs the tooling on. Blender is not a prerequisite: it is needed only to
rebuild the model, which [Rebuild the model](rebuild-the-model.md) covers.

## First run

This repository takes its design system from `@steven-cutting/biscuit-games`, published to
GitHub Packages. That registry authenticates every request, including a read of a public
package, so the token comes before anything else. Put one line in `~/.npmrc` — the user
configuration, never this repository's `.npmrc`, which names the registry for the scope and
holds no credential:

```text
//npm.pkg.github.com/:_authToken=<your token>
```

Replace the placeholder, angle brackets and all. It is bracketed rather than spelled
`YOUR_TOKEN` because `ripsecrets` reads this repository as part of the gate and takes a
bare word after `_authToken=` for a token whether or not it is one — so a plainer
placeholder here would fail the commit that documented it. The token is a personal access
token carrying `read:packages`, and it lives in `~/.npmrc` and nowhere in this repository.

Without the line npm answers `401 Unauthorized` and says the authentication token was not
provided — the registry refusing the request, rather than a broken install.

```console
just initialize
```

This creates or checks `uv.lock` and `package-lock.json`, installs both toolchains from
them, runs `git lfs install --local` so the LFS filter and hooks are configured for this
clone, normalises formatting, and installs the pre-commit hook. Run it once per clone. It
never stages, commits, tags or pushes.

Three things about that first run are worth knowing before it surprises you:

- **It needs the network.** `npm ci` reads the registry with your token, and the first
  `just lint` clones every hook repository into prek's cache. An offline first run fails
  at the install or at the first lint, for no reason of the studio's; once the caches are
  full, the checks run offline.
- **The hook is installed only from the primary checkout.** Every worktree of a
  repository shares one `.git/hooks`, and a hook installed from a secondary worktree would
  run that worktree's tools for commits made anywhere. In a secondary worktree
  `just initialize` says so and skips it; run `just install-hooks` once from the primary
  checkout. For the same reason `git lfs install --local` writes to the `.git/config`
  every worktree shares, which is what you want.
- **The gate reads the index, not the worktree.** `prek run --all-files` lints the files
  `git ls-files` reports, so a new file is invisible to `just lint` and `just check`
  until you stage it.

## Every day

```console
just dev
```

Vite serves the site with hot module replacement. There is no backend to start, no
database to bring up and no proxy to configure; the browser talks to Vite and to nothing
else. The site has three routes: `/`, `/model/` and `/gallery/`. The pose studio is a
static file rather than a route, served at `/pose-studio/viewer.html`.

To see what a deployment would actually serve, build first and then preview:

```console
just frontend-build
just preview
```

Both read the base path from `BASE_PATH`, which is empty unless you set it, so the two
commands above serve the build at the root. To reproduce the published site exactly, set
the base path the project site is served under — the repository's name, which `pages.yml`
reads from the event — on both commands, for the reason
[Configuration](../reference/configuration.md) gives:

```console
BASE_PATH=/biscuit_studio just frontend-build
BASE_PATH=/biscuit_studio just preview
```

## Before handing work back

```console
just fix       # formats and applies the safe automatic repairs
just check     # the whole gate, read-only
```

Of the two, only `just fix` modifies files. Every check is read-only, and `just check`
proves it by comparing the worktree before and after each recipe. If the change touched
anything under `assets/` or `static/pose-studio/`, `just check-assets` is the narrow
recipe to run first.

## Keeping the workspace current

After pulling, re-sync so the installed dependencies match the lockfiles:

```console
just sync
```

If a pull brought a new version of the model and the `.blend` reads as a short text file,
the LFS objects were not fetched: `git lfs pull` fetches them, and `git lfs install
--local` is the missing step if it happens again.

## Related pages

- [Commands](../reference/commands.md)
- [Test and debug](test-and-debug.md)
- [Large files](../explanation/large-files.md)
- [Troubleshooting](../operations/troubleshooting.md)
