# Biscuit Studio

The Biscuit Games studio: the repository where the platform's graphical assets are
developed — the poseable 3D model of Biscuit, the renders and exports made from it, and the
2D illustrations — and the static site on GitHub Pages that shows them.

It consumes `@steven-cutting/biscuit-games` exactly as a game does, and nothing depends on
it. Finished assets leave by copy, never by dependency: each copy is recorded in
`assets/manifest.json` with the sha256 it had here and, once ticket C02 has designed it, in
a ledger a consumer's gate can verify.

**Status: built, deployed, and holding the approved model.** The toolchain and the gate,
the three pages of the site, the approved model and the cel illustrations under a sha256
manifest, the handbook and the agent contract are all in place, and the site is served
from `main` by GitHub Pages. What is still open is listed in
[the work breakdown](tickets/README.md); nothing leaves for the hub until the hub's brand
rule allows it.

## The site

<https://stevencutting.com/biscuit_studio/>

The home page links to two others. The model page shows the approved model in its four
preset poses and offers it three ways: the pose studio (`pose-studio/viewer.html` under the
site, a single 27.6 MB page that needs WebGL 2 and works offline), the GLB to
download, and the Blender scene on GitHub. The gallery shows the cel set, two bodies and
nine heads.

It is a project Pages site built under `/biscuit_studio`, not a site of its own; see
[decision 0004](docs/decisions/0004-a-project-pages-site.md).

## Quick start

```console
just initialize
just check
```

`just initialize` is the whole first run: both lockfiles, both toolchains, Git LFS for
this repository and the hooks. Two things it needs are carried by no lockfile.

- **A token that reads the platform package.** `@steven-cutting/biscuit-games` comes from
  GitHub Packages, which authenticates every read. Put a GitHub token carrying
  `read:packages` in `~/.npmrc`, never in this repository, as the line
  `//npm.pkg.github.com/:_authToken=<your token>`.
- **Git LFS.** `scripts/initialize.sh` runs `git lfs install --local`. A clone made on a
  machine without git-lfs holds pointer text where the `.blend` should be; install git-lfs,
  run `git lfs install` and `git lfs pull` before opening it.

See [Develop locally](docs/how-to/develop-locally.md) for the rest. `just --list` prints
every recipe, and [Commands](docs/reference/commands.md) describes each one.

Do not run `just install-hooks` from a secondary git worktree: `.git/hooks` is shared across
every worktree of this repository, and the installed hook names an absolute path into the
worktree that installed it.

## Check your work

```console
just fix      # the aggregate repair command
just check    # every gate, read-only, proving the worktree is unchanged
```

## Layout

```text
assets/              The sources: the model, the illustrations, and manifest.json over them all
static/pose-studio/  What the site serves byte for byte: the viewer, the GLB, the previews
src/lib/             The brand, the appearance wiring, and the lockup component
src/routes/          The three prerendered pages: home, model, gallery
docs/                The handbook
tests/               Vitest suites, never colocated
scripts/             The asset checker, the rebuild script, the bootstrap script
tickets/             The work breakdown this repository was built from
```

## Documentation

Start at [the documentation map](docs/README.md).

- [Purpose and scope](docs/project/purpose-and-scope.md) — what this repository is, and is not
- [The platform upstream](docs/project/platform.md) — the boundary between here and the hub
- [Content policy](docs/explanation/content-policy.md) — what is committed, and what never is
- [Architecture decisions](docs/decisions/README.md) — what was chosen, and what it cost

Engineering conventions and the agent working agreement are in [AGENTS.md](AGENTS.md).

## Boundaries

The hub, `steven-cutting/biscuit_games`, owns every rule about Biscuit and about the design
system: how she looks, the tokens, the components, the specifications. The studio owns her
assets. Files travel one way as the package — the studio installs
`@steven-cutting/biscuit-games` at an exact version, as a game does — and the other way by
copy, when a finished asset is promoted to the hub or a game. See
[The platform upstream](docs/project/platform.md) and
[Promote an asset](docs/how-to/promote-an-asset.md).

## Bootstrap of this repository

CI (`.github/workflows/ci.yml`) runs three jobs on every pull request, on push to `main` and
on dispatch: `frontend` (the site), `documents` (the handbook and the agent contract) and
`assets` (the manifest). When CI succeeds on `main`, `.github/workflows/pages.yml` builds
the site and deploys it.

All three are required checks on `main`, applied in one round by
`scripts/bootstrap_repo.sh steven-cutting/biscuit_studio --checks frontend,documents,assets`,
because none of the three depends on a setting outside this repository. The same run set
the Pages source to GitHub Actions and switched private vulnerability reporting on, and a
run with `--hygiene` turned on deleting the branch on merge and turned the wiki and projects
off. HTTPS is enforced on the site, a setting the script does not make, applied by a
separate call. No CI job carries a `paths` filter or a `name:`, so no required
check can be skipped into blocking a merge and each check is named after its job.

Every `--apply` is an authorised action; see [AGENTS.md](AGENTS.md) and
[Deploy to GitHub Pages](docs/how-to/deploy-to-github-pages.md).
