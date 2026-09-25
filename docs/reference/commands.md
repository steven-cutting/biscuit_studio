---
title: "Commands"
kind: "reference"
audience: [contributor, maintainer, operator, agent]
canonical_for: [command_reference]
requires: []
---

# Commands

`just` on its own prints the live set of recipes with their comments: `just default` is
that listing. This page says what each recipe is for, what it proves and whether it needs
the network. The `Justfile` is the only supported interface: if something is worth running
twice, it belongs there rather than in a shell history.

## Setup

| Recipe | Purpose |
| --- | --- |
| `just initialize` | One explicit first run. Creates both lockfiles, installs both toolchains, runs `git lfs install --local` for this clone, normalises formatting, and installs the hook when the checkout is the primary one. Needs the network and the registry token. Never stages, commits, tags or pushes. Safe in any worktree: it skips the hook rather than installing a shared one from the wrong place. |
| `just sync` | Install exactly what the lockfiles say: the Python environment, then `node_modules`. Run after pulling. Needs the network and the registry token. |
| `just install-hooks` | Install the read-only pre-commit gate. Primary checkout only — see the warning below. |

### Do not install the hook from a secondary worktree

Git keeps one `.git/hooks` directory and shares it across every worktree of the
repository. The installed hook records an absolute path into the virtual environment of
the worktree that installed it, and `just install-hooks` passes `--overwrite`, so
installing from a secondary worktree silently replaces the hook every other worktree also
commits through. Check first: this is a secondary worktree when
`git rev-parse --git-common-dir` and `git rev-parse --git-dir` differ, and then
`just install-hooks` is the wrong command here. Counting the rows of `git worktree list` is
not that test — it prints every worktree whatever it is run from. `just initialize` already
knows: it makes the same comparison and skips the hook, saying so, rather than installing one
from the wrong place. Run it freely; run `just install-hooks` by hand only from the primary
checkout. Nothing else warns you, and the breakage surfaces in another worktree, later.
The full account is in [Develop locally](../how-to/develop-locally.md).

## Dependencies

| Recipe | Purpose |
| --- | --- |
| `just lock` | Relock at the versions the manifests state. Writes both lockfiles; needs the network. |
| `just lock-upgrade` | Move within the manifests' constraints. Every pin is exact, so this moves only what a manifest already allows; needs the network. |
| `just lock-check` | Fail if a manifest and its lockfile disagree. Offline once the registry has been read. |

## Develop

| Recipe | Purpose |
| --- | --- |
| `just dev` | Vite development server with hot module replacement, on `127.0.0.1:5173`. Serves the gallery's drawings from `assets/` because `vite.config.ts` allows that one directory. |
| `just preview` | Serve the built output in `build/`. Build first, with the same `BASE_PATH` the build had; `BASE_PATH=/biscuit_studio just preview` after a build with that value reproduces the Pages address. |
| `just frontend-watch [path]` | Vitest in watch mode over one path, or over everything. The iteration loop; it never exits, so it is not a gate. |

## Format and repair

| Recipe | Purpose |
| --- | --- |
| `just format` | Ruff and Prettier, writing. |
| `just fix` | The mutating hook set, then ESLint autofix, then `just lint`. The aggregate repair command: reach for it rather than the individual writers. |

`just fix` is the repair command, not the only one that writes. `just format`, `just lock`,
`just lock-upgrade`, `just assets-manifest` and `just initialize` all modify tracked files
too — the first four by design, the last as part of a first run. What is read-only is the
**check** set: every recipe `just check` runs reports and never repairs, and
`bg-project-check` proves it per run by comparing the worktree before and after each one.
That is the guarantee worth relying on, and it is the one the other pages cite.

## Check

| Recipe | Purpose |
| --- | --- |
| `just lint` | The whole read-only hook gate over every tracked file. The first run clones every hook repository and needs the network; after that it is offline. |
| `just frontend-static` | ESLint, `prettier --check`, and `svelte-check --fail-on-warnings`. Offline. |
| `just frontend-unit` | Vitest, once. Offline. |
| `just frontend-coverage` | Vitest with the 90% floor over `src/lib/**` enforced. This is the one `just check` runs. Offline. |
| `just frontend-build` | Production build into `build/`. `svelte.config.js` reads `BASE_PATH` into `paths.base`, empty unless set — see [Configuration](configuration.md). Offline. |

## Documents and agents

| Recipe | Purpose |
| --- | --- |
| `just check-docs` | markdownlint, `typos`, the offline link check, then the documentation contract. Offline. |
| `just check-agents` | The agent contract: `AGENTS.md`, the adapters, and the skill bridges. Offline. |

## Assets

| Recipe | Purpose |
| --- | --- |
| `just check-assets` | Every file under `assets/` and `static/pose-studio/` against `assets/manifest.json`: listed, present, and byte-identical to its recorded sha256, an LFS pointer verified from the oid it carries. Refuses an image with EXIF beyond its resolution, and any TIFF. Runs the checker's own self-test first. Offline, and never fetches an LFS object. |
| `just assets-manifest` | Rewrite `assets/manifest.json` from the worktree, then check it. The one recipe that writes the manifest: it keeps every entry's `source`, `licence` and `patched`, reads the viewer's `source_sha256` from its build record, and recomputes the rest. Read its diff before committing. Offline. |
| `just model-rebuild <biscuit_pics>` | Rebuild the approved model from its sources, given a checkout of the source repository. Needs Blender and that checkout; never part of `just check` and never run in CI. See [Rebuild the model](../how-to/rebuild-the-model.md). |

[Asset manifest](asset-manifest.md) is the format and what the checker refuses, message by
message.

## Publish

None. No recipe publishes anything. The site is published by `.github/workflows/pages.yml`,
which runs after CI passes on a push to `main` and deploys only while that commit is still
`main`'s head; [Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md) is the
procedure. Nothing here builds a package, and nothing here pushes.

## Aggregate

| Recipe | Purpose |
| --- | --- |
| `just check` | Every gate in order — the list `pyproject.toml` names — proving the worktree is unchanged between each, then `just check-clean`. Offline once `just sync` and the first `just lint` have run. |
| `just check-clean` | Assert the worktree is clean, or matches a supplied baseline. |
| `just check-links-online` | Follow every external link, including the hub URLs on [The platform upstream](../project/platform.md). Manual and monthly; needs the network. Never part of `just check`. |

## Related pages

- [Quality gates](quality-gates.md)
- [Develop locally](../how-to/develop-locally.md)
- [Configuration](configuration.md)
- [Asset manifest](asset-manifest.md)
