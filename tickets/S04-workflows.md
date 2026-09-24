---
id: S04
title: "Workflows: ci.yml with three jobs, pages.yml through the shared workflow"
status: open
depends_on: [S00]
parallel_with: [S01, S02, S03, S05, S06]
branch: ticket/s04-workflows
estimated_size: M
---

# S04: Workflows: ci.yml with three jobs, pages.yml through the shared workflow

## Context

CONVENTIONS.md §8 fixes the studio's continuous integration: three required checks on
`main` named `frontend`, `documents` and `assets`, and a Pages deployment on every push
to `main`. §1 fact 6 says why the first is bespoke and the second is not. G's
`game-ci.yml` (`/Users/scutting/projects/biscuit_games_tooling/.github/workflows/game-ci.yml`)
hard-codes the `storybook-*`, `check-specs` and `analyse-specs` recipes in its three jobs
and offers no input to switch one off; the studio has none of those recipes (§2.2, §2.4),
so calling it would fail on the first missing recipe. H's own `ci.yml`
(`/Users/scutting/projects/biscuit_games/.github/workflows/ci.yml`, 118 lines) is the
inline shape to copy: one job per check, each with its own checkout and toolchain, `just`
recipes in the gate's order. G's composite action `actions/setup-toolchain/action.yml`
(64 lines) replaces H's five toolchain steps (H lines 26-38) with one `uses:`, at the
commit tag `v0.3.0` names, `6c5c07f6bec86e86b3930dfa41392e4b440e8c85`; it sets up Node with
the GitHub Packages registry for the `@steven-cutting` scope, uv with its cache, Python
3.14, `rust-just` 1.51.0 and npm 11.17.0, and installs nothing from the lockfiles — `just
sync` stays in the job, on the one step that carries `NODE_AUTH_TOKEN`
(G `game-ci.yml`, the `sync` step of each job, and G `README.md` "Calling it").

G's `game-pages.yml` (86 lines) is reused unchanged. T's rendered
`template/.github/workflows/pages.yml` (39 lines) already calls it at the `v0.3.0` commit
with `base_path: /${{ github.event.repository.name }}`, which for this repository is
`/biscuit_studio`; the file is taken verbatim. It builds with `npm ci` and `npm run build`,
uploads `build/` (the default `artifact_path`; no `stage`, because there is no domain root
to stage around, H decision 0012), and deploys in a second job holding `pages: write` and
`id-token: write`. Its checkout does not fetch LFS objects, which is correct: nothing
under `static/` is LFS (§3), and a Pages artefact built from a pointer would serve
pointer text (§1 fact 4).

The `assets` job is new. It runs `just check-assets`, which verifies every LFS-tracked
file from its pointer (§4), so the job checks out with `lfs: false` and never downloads
an object; the option is stated explicitly although it is `actions/checkout`'s default,
with a comment saying the pointer is what the checker reads. `check-assets` runs
`uv run --frozen python scripts/check_assets.py` (§2.2), so the job needs the Python
environment, which `just sync` provides along with `npm ci`; a recipe that syncs only
Python does not exist, and `AGENTS.md` says not to invent one, so `just sync` it is, with
the token, the same as the other two jobs.

Nothing runs in this ticket: the repository has no remote until S07, so actionlint
(in the hook gate, H `.pre-commit-config.yaml` lines 155-159) is the whole of the
evidence here, and S07 watches the first real run.

Read first: CONVENTIONS.md §0, §1 (decision 7, facts 3, 4, 6), §2 (the two S04 rows),
§8, §9, §10 (the `lfs: false` claim). H `.github/workflows/ci.yml` whole. G
`.github/workflows/game-ci.yml`, `.github/workflows/game-pages.yml`,
`actions/setup-toolchain/action.yml`, and G `README.md` lines 1-60 ("Calling it": pin by
the forty-character SHA with the tag in a comment; the calling job carries the union of
the called jobs' permissions). T `template/.github/workflows/pages.yml` whole. T
`tickets/C03-repository-bootstrap.md` lines 27-34 and 292-295 (the check's name is the
job id; no `paths` filter, no `name:`).

## Goal

- `.github/workflows/ci.yml` exists with three jobs whose ids are `frontend`, `documents`
  and `assets`, each running the steps §8 lists through `just`, on `pull_request`, push to
  `main` and `workflow_dispatch`.
- `.github/workflows/pages.yml` exists and is T's file byte for byte.
- `just lint` is green (actionlint accepts both files).
- `just check` is green.

## Non-goals

- A Chromatic workflow (§1 decision 10: no workshop in the first release).
- A release workflow (the studio publishes no package; `package.json` is `private`).
- Any repository setting: the Pages source, branch protection and the required-check
  names are S07's, applied with `scripts/bootstrap_repo.sh`.
- Running either workflow. No remote exists; S07 proves them.
- Caching Playwright, installing Chromium, installing the allium binary: none of the
  three is a studio dependency.
- A `paths` filter or a `name:` on any job (T C03: a skipped required check blocks the
  merge, and a `name:` changes the check's context).

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `.github/workflows/ci.yml` | S04 | H `.github/workflows/ci.yml` with the edits step 1 gives; exact content embedded | new |
| `.github/workflows/pages.yml` | S04 | T `template/.github/workflows/pages.yml` verbatim | new |
| `tickets/S04-workflows.md` | ticket | this file | `status:` line, hand-back notes |

The table is the whole scope. Nothing outside it is edited. S00 ships neither file, so
both are created here; if S00 left a stub at either path, it is replaced.

## Steps

Work from the repository root on branch `ticket/s04-workflows`.

### Step 1: `.github/workflows/ci.yml`

Write this file. It is H's `ci.yml` with: the `stories` job removed; H's five toolchain
steps (setup-node, setup-uv, `uv python install`, `uv tool install rust-just`, `npm
install --global npm`) replaced by the composite action; `packages: read` added to the
workflow permissions, because every job installs the platform package with the run's own
token; `NODE_AUTH_TOKEN` on the `just sync` step and nowhere else; the `documents` job
without `install-allium`, `check-specs` and `analyse-specs`; and the `assets` job added.
Action SHAs: `actions/checkout` is H line 23 (`3d3c42e5aac5ba805825da76410c181273ba90b1`,
v7.0.1); the composite action's commit is G `v0.3.0`. Confirm both before committing:
`git -C /Users/scutting/projects/biscuit_games_tooling rev-parse 'v0.3.0^{commit}'` and
`grep -n checkout@ /Users/scutting/projects/biscuit_games/.github/workflows/ci.yml`.

```yaml
name: CI

on:
  pull_request:
  push:
    # Quoted because a branch named `true`, `false`, `null`, `on`, or `1.0` is
    # valid to Git but is not a string to a YAML 1.1 parser.
    branches: ['main']
  workflow_dispatch:

permissions:
  contents: read
  # Every job installs @steven-cutting/biscuit-games from GitHub Packages with
  # the run's own token. A permission is not a secret: nothing is stored on
  # this repository for it.
  packages: read

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# Three jobs, and the job id is the check's name: `frontend`, `documents` and
# `assets` are what `main` requires. No job carries a `paths` filter or a
# `name:`, because a skipped required check blocks the merge and a name changes
# the context. The toolchain arrives through the shared composite action, at
# the commit its tag names; `just sync` stays here, on the one step that holds
# the registry token.
jobs:
  frontend:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: steven-cutting/biscuit_games_tooling/actions/setup-toolchain@6c5c07f6bec86e86b3930dfa41392e4b440e8c85 # v0.3.0
      - run: just sync
        env:
          # On the step that installs, never on the job: a step with no use for
          # the credential should not carry one. It is the run's own token,
          # minted and discarded with the run, so nothing is stored here.
          NODE_AUTH_TOKEN: ${{ github.token }}
      - run: just lock-check
      - run: just frontend-static
      - run: just frontend-coverage
      - run: just frontend-build

  documents:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: steven-cutting/biscuit_games_tooling/actions/setup-toolchain@6c5c07f6bec86e86b3930dfa41392e4b440e8c85 # v0.3.0
      # `just lint` runs the whole hook gate, which includes ESLint and the two
      # validators, so node_modules and the uv environment must both exist.
      - run: just sync
        env:
          NODE_AUTH_TOKEN: ${{ github.token }}
      - run: just lint
      # Already run by the hook gate above; repeated so a documentation or
      # agent-contract regression names itself in the step list rather than
      # inside `lint`.
      - run: just check-docs
      - run: just check-agents

  # The asset manifest against the tree. Every LFS-tracked file is verified
  # from the pointer it checks out as (the oid the pointer carries is the
  # object's sha256), so this job never fetches an object and the option below
  # says so where it can be read, although it is the action's default.
  assets:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
          lfs: false
      - uses: steven-cutting/biscuit_games_tooling/actions/setup-toolchain@6c5c07f6bec86e86b3930dfa41392e4b440e8c85 # v0.3.0
      # The checker runs under `uv run --frozen`, and `just sync` is the one
      # recipe that provides that environment; it installs node_modules too,
      # which this job never reads, at the cost of the same token the other
      # jobs carry.
      - run: just sync
        env:
          NODE_AUTH_TOKEN: ${{ github.token }}
      - run: just check-assets
```

The composite action takes seven inputs with defaults (G `action.yml` lines 8-31); none
is passed, because every default is the studio's pin (§0: node 26, npm 11.17.0, uv
0.11.18, Python 3.14, just 1.51.0, scope `@steven-cutting`, `npm-cache` on with
`package-lock.json` present).

### Step 2: `.github/workflows/pages.yml`

Copy T's file byte for byte:

```sh
cp /Users/scutting/projects/biscuit_games_template/template/.github/workflows/pages.yml .github/workflows/pages.yml
cmp /Users/scutting/projects/biscuit_games_template/template/.github/workflows/pages.yml .github/workflows/pages.yml && echo identical
```

For the record, the file (39 lines):

```yaml
name: Deploy to GitHub Pages

# Publishing needs write scopes that no other workflow here has, so the deploy
# lives in its own file rather than as a job on the end of CI.

on:
  push:
    branches: ['main']
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

# One deployment at a time, and never cancel one that is already running: a
# half-published site is worse than a slightly stale one.
concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  pages:
    # The union of what the called jobs hold: the build reads the platform
    # package, the deploy publishes.
    permissions:
      contents: read
      pages: write
      id-token: write
      packages: read
    uses: steven-cutting/biscuit_games_tooling/.github/workflows/game-pages.yml@6c5c07f6bec86e86b3930dfa41392e4b440e8c85 # v0.3.0
    with:
      # A project site: Pages serves the build at
      # <owner>.github.io/<repository>/, so the app is built to live under that
      # path. The name is read from the event rather than written here, which is
      # what keeps this file the same in every game and keeps `paths.base` in
      # svelte.config.js from drifting away from the address Pages actually
      # serves.
      base_path: /${{ github.event.repository.name }}
```

"Every game" in the comment is T's wording and is left as it is: the file is verbatim, and
the sentence is still true of why the name is read from the event. `svelte.config.js`
(§2.5) reads `BASE_PATH`, which the called workflow sets from `base_path` (G
`game-pages.yml` lines 19-22).

### Step 3: Lint

```sh
just lint
```

actionlint runs over `^\.github/workflows/.*\.ya?ml$` (H `.pre-commit-config.yaml` line
159, which S00 kept). Both files must pass. An actionlint finding about the composite
action's inputs, the `lfs` option or an expression is fixed in the file; a finding about
the shared workflow's inputs is a G defect, handed back rather than worked around. Then:

```sh
just check
```

### Step 4: Commit, notes, status

Commit on the ticket branch. Fill in the hand-back notes, set `status: done` on this
file. Pushing and opening the pull request are separately authorised.

## Acceptance criteria

- [ ] `.github/workflows/ci.yml` parses (`uv run --frozen prek run --all-files
      check-yaml actionlint` is clean) and its job ids, in order, are `frontend`,
      `documents`, `assets`: `grep -E '^  [a-z]+:$' .github/workflows/ci.yml` prints
      exactly those three lines.
- [ ] No job in `ci.yml` has a `name:` or a `paths:` key: `grep -cE '^\s+(name|paths):'
      .github/workflows/ci.yml` prints `0`.
- [ ] `grep -c 'NODE_AUTH_TOKEN' .github/workflows/ci.yml` prints `3`, one per job, and
      each sits under a `just sync` step.
- [ ] `grep -c 'lfs: false' .github/workflows/ci.yml` prints `1`, in the `assets` job.
- [ ] `grep -c '6c5c07f6bec86e86b3930dfa41392e4b440e8c85' .github/workflows/ci.yml` prints
      `3` and the same over `pages.yml` prints `1`; each occurrence is followed by
      `# v0.3.0`.
- [ ] `grep -c '3d3c42e5aac5ba805825da76410c181273ba90b1' .github/workflows/ci.yml`
      prints `3`, each followed by `# v7.0.1`.
- [ ] `cmp` reports `pages.yml` identical to T's.
- [ ] Workflow-level `permissions` in `ci.yml` are exactly `contents: read` and
      `packages: read`.
- [ ] `just lint` and `just check` are green.
- [ ] No file outside `.github/workflows/` changed.

## Verification

```sh
grep -E '^  [a-z]+:$' .github/workflows/ci.yml
grep -c 'NODE_AUTH_TOKEN' .github/workflows/ci.yml
grep -c 'lfs: false' .github/workflows/ci.yml
grep -c '6c5c07f6bec86e86b3930dfa41392e4b440e8c85' .github/workflows/ci.yml .github/workflows/pages.yml
cmp /Users/scutting/projects/biscuit_games_template/template/.github/workflows/pages.yml .github/workflows/pages.yml && echo identical
just lint
just check
```

Expected: `frontend:`, `documents:`, `assets:` (each indented two spaces); `3`; `1`; `ci.yml:3` and
`pages.yml:1`; `identical`; both gates green.

The end-to-end proof is S07's: after the first push, `gh run list` shows the `CI` run
with three jobs and the `Deploy to GitHub Pages` run, all `success`, and the required
checks on `main` read `frontend`, `documents`, `assets`.

## Hand-back notes

Filled in by the agent that executes this ticket.

- The `rev-parse` of G's `v0.3.0` and H's checkout SHA, quoted, confirming the pins.
- actionlint's output, quoted, and any finding it raised with what was changed.
- Whether the composite action was pinned with any input overridden (it should not be).
- Anything handed to S07: in particular, that the first `Deploy to GitHub Pages` run
  will fail at the deploy job with `Failed to create deployment (status: 404)` until the
  Pages source is `workflow`, which is why S07 bootstraps before pushing.
- Which authorisations were asked for (none are expected).

## Open points

- **`lfs: false` on `actions/checkout` v7.0.1** is the default and is written for the
  reader; whether the option is still accepted under that name is confirmed by actionlint
  here and by the first run in S07 (CONVENTIONS.md §10).
- **`just sync` in the `assets` job installs `node_modules` it never reads.** Accepted
  rather than adding a Python-only sync recipe; if the job's time matters, the recipe is a
  `Justfile` change and an S00 follow-up.
- **The composite action's `npm-cache` default** keys on `package-lock.json`; the
  `assets` job's cache is wasted on a job that does not build. Harmless; noted.
