---
title: "Maintain dependencies"
kind: "how-to"
audience: [maintainer, agent]
canonical_for: [dependency_maintenance]
requires: []
---

# Maintain dependencies

Every dependency is pinned to an exact version, in `package.json` and in
`pyproject.toml`. No `^`, no `~`. Both lockfiles are committed and marked
`linguist-generated`. Nothing updates them for you.

One of them comes from a second registry: `@steven-cutting/biscuit-games` is read from
GitHub Packages through the committed `.npmrc`, which scopes `@steven-cutting` there and
holds no token. Moving it is its own section below, because what it carries is not only
code.

## Check that the lockfiles still match

```console
just lock-check
```

This runs `uv lock --check` and an npm install dry run. It is part of `just check`, so a
manifest edited without relocking fails the gate rather than drifting.

## Update deliberately

```console
just lock            # relock at the versions the manifests already state
just lock-upgrade    # move to newer versions within the manifests' constraints
```

Because the manifests pin exact versions, `just lock-upgrade` on its own changes very
little. Moving a dependency forward means editing the version in the manifest and then
relocking.

## Upgrading a package

1. Check what it is compatible with before choosing a version. This bites: the current
   TypeScript major is ahead of what `typescript-eslint` supports, so the repository
   pins the 6.x line deliberately, not by neglect.

   ```console
   npm view typescript-eslint peerDependencies
   ```

2. Edit the exact version in `package.json` or `pyproject.toml`.
3. Run `just lock`, then read the lockfile diff before accepting it.
4. Run `just sync`. `just lock` rewrites the lockfiles and installs nothing, and no check
   installs `node_modules` for itself, so without this the gate runs the old versions.
5. Run `just check`. A type-checker or linter upgrade usually surfaces new findings; fix
   them rather than pinning back, unless the finding is wrong for this project.

## Moving the design system package

`@steven-cutting/biscuit-games` carries the stylesheet the studio wears and the components
it renders, so a bump is read before it is taken.

1. See what is published, which needs the token
   [Develop locally](develop-locally.md) describes:

   ```console
   npm view @steven-cutting/biscuit-games versions
   ```

2. Read what moved. The package ships its own changelog, so after installing it is at
   `node_modules/@steven-cutting/biscuit-games/CHANGELOG.md`; before installing, the
   platform's repository has both that and a handover page naming every consumer-visible
   change — [The platform upstream](../project/platform.md) links them.
3. Edit the exact version, run `just lock`, and read the lockfile diff: one dependency line
   and one entry, and anything else is a stop-and-read. Then run `just sync`, because
   `just lock` installs nothing and every step below reads the installed package.
4. The studio restates nothing, so a bump is read in the package's `CHANGELOG.md` and
   proved by `just check`. No test here holds a platform figure or clause to the package's
   text; what changed arrives as the stylesheet and the components themselves.
5. Add a `CHANGELOG.md` entry naming what a reader would see; `package.json` is the one
   place the installed version is stated.
6. Run `just check`, then look at the three routes under `just dev`, in dark and light and
   with high contrast, because nothing here reviews the rendered site automatically.

Nothing proposes this bump for you. There is no Dependabot here, and one would need the
registry credential as a stored secret of its own.

## Moving the tooling package

The documentation and agent gates and the runner behind `just check` are console scripts
of `biscuit-games-tooling`, which the `dev` group in `pyproject.toml` pins to the release
tag `@v0.3.0` of `steven-cutting/biscuit_games_tooling`. `uv.lock` records the commit
behind the tag, and `just lock-check` fails when the tag moves without a relock.

1. Read the package's `CHANGELOG.md` in that repository for the release you are taking, and
   the level its README gives the change. A Major release can fail a tree that passed.
2. Edit the tag in the `biscuit-games-tooling` line of `pyproject.toml`, then relock that
   one package and read the lockfile diff:

   ```console
   uv lock --upgrade-package biscuit-games-tooling
   ```

3. Run `just sync`, because the lock installs nothing.
4. On a Major release, run `just check` before committing. Otherwise the hooks that read
   `pyproject.toml` re-run the contracts on the commit.

A tag the package has released is never moved, so relocking without editing the tag
changes nothing. The same release is pinned a second time, by commit, in the workflows;
see the last section.

## Moving Pillow

`pillow` is a dev dependency for one reason: `scripts/check_assets.py` opens every raster
image under `assets/` and `static/pose-studio/` to read its EXIF. It is pinned exactly in
`pyproject.toml` like every other Python pin, and it moves the same way: edit the version,
relock with `uv lock --upgrade-package pillow`, read the diff, and `just sync`.

The proof is `just check-assets`. Its `check` subcommand runs the checker's own self-test
first, which opens the committed EXIF fixture `tests/fixtures/exif-gps.jpg` and a handful of
images it generates, and fails unless each is refused or passed as it should be. A Pillow
release that changed how EXIF is read, or dropped a format its wheels bundle, fails there
rather than silently letting metadata through.

## Actions in the workflows

The two workflows pin three things, each to a commit SHA with its release tag as a
comment, never to the tag:

- `actions/checkout`, in each of the three jobs in `ci.yml`;
- the tooling repository's composite action `actions/setup-toolchain`, which installs
  Node, npm, `uv`, Python and `just` in each of those jobs;
- the tooling repository's reusable workflow `game-pages.yml`, which `pages.yml` calls.

The actions those shared pieces run, and the toolchain versions they install, are pinned
inside the tooling repository and move there. Moving the tooling release is a two-file
change: `ci.yml` and `pages.yml` carry the same SHA, and both change in one commit, together
with the `pyproject.toml` tag above if the Python package moves with it.

Resolve the release's commit and replace both the SHA and the comment. Its tags are
annotated, so ask for the commit: the SHA a tag reference answers with names the tag
object, which no `uses:` line accepts.

```console
gh api repos/steven-cutting/biscuit_games_tooling/commits/v0.3.0 --jq .sha
```

`actionlint` runs inside `just lint`, so a malformed workflow fails locally.

## Related pages

- [Configuration](../reference/configuration.md)
- [Quality gates](../reference/quality-gates.md)
- [Maintenance](../operations/maintenance.md)
- [The platform upstream](../project/platform.md)
