---
title: "Quality gates"
kind: "reference"
audience: [contributor, maintainer, agent]
canonical_for: [quality_gate_reference]
requires: []
---

# Quality gates

`just check` runs the gates in the order below and snapshots the worktree between each one.
A recipe that modifies a file fails the run, because checks are read-only. The order is
`recipes` under `[tool.biscuit-games-tooling]` in `pyproject.toml`, which `bg-project-check`
reads and follows with `check-clean`; a gate added to one and not the other is a gate that
either never runs or is never described.

| Order | Gate | Proves |
| --- | --- | --- |
| 1 | `lock-check` | Both manifests agree with both lockfiles. |
| 2 | `lint` | The whole hook gate passes over every tracked file. |
| 3 | `frontend-static` | ESLint, Prettier and `svelte-check --fail-on-warnings` are clean. |
| 4 | `frontend-coverage` | Every test passes and coverage over `src/lib/**` is at or above the floor. |
| 5 | `frontend-build` | The site actually builds, with every route prerenderable and every link the crawler follows resolving. |
| 6 | `check-assets` | Every asset is listed, byte-identical to its manifest entry, and carries no GPS or camera EXIF; the checker's self-test passed first. |
| 7 | `check-docs` | The documentation contract holds, and the Markdown passes markdownlint, `typos` and the offline link check. |
| 8 | `check-agents` | The agent contract holds. |
| 9 | `check-clean` | The run changed nothing. |

No specification gate runs, and the absence is deliberate. The studio has no `docs/specs/`
of its own: the modules that govern its surfaces are the platform's, installed with the
package and checked where they are written. The runner the hub uses, `bg-run-allium`, exits
2 when it finds no module to check rather than passing an empty set, so a gate pointed at
nothing would fail every run. The recipes are therefore absent from the `Justfile`, from
`pyproject.toml`'s list and from the hook gate alike.

The one exclusion set is the other thing to know before reading a failure. Three paths are
skipped by every linter:

```text
assets/models/biscuit/(model|poses|previews|qa|src|textures)/
assets/illustrations/
static/pose-studio/
```

They hold Blender's own build scripts, generated textures and renders, the drawings, and a
26 MB page of inlined base64. None was written to this repository's rules, none is edited by
hand, and the size and spelling hooks would refuse them for reasons that say nothing about
their quality. What guards them instead is `check-assets`. The set is written once in each
tool's own form, in six places: the `exclude` of both pre-commit files, `.prettierignore`,
`eslint.config.js`, `.markdownlint-cli2.jsonc`, `lychee.toml` and `pyproject.toml` (for
`typos` and Ruff), with `.editorconfig` unsetting its rules under the same roots for editors.
A change to the set is made in all six.

Two files under `assets/` are deliberately outside it. `assets/models/biscuit/README.md` is
prose a person reads, so markdownlint and lychee read it too. `assets/manifest.json` is
parsed by `check-json` on every run, so a hand edit that breaks the JSON is caught before
the checker reads it.

One check is deliberately missing from the table. `check-links-online` needs the network,
and a check that can fail because a third party is down is not a gate. It is listed in
[Commands](commands.md).

## What the hook gate contains

`just lint` runs `.pre-commit-config.yaml` over every file Git tracks. This is the read-only
configuration, and it is the one installed as the pre-commit hook. A new file is invisible to
it until it is staged.

| Hook | Checks |
| --- | --- |
| `ruff-check`, `ruff-format-check` | Every Python script under `scripts/`. |
| `eslint` | ESLint and `prettier --check` across `src/`, `tests/` and the configuration files. |
| `validate-docs`, `validate-agents` | The two contracts, so a hook catches them before the aggregate does. |
| Builtin `check-*` | Large files, case conflicts, merge markers, JSON, TOML, YAML, private keys, shebangs. |
| `editorconfig-checker` | Whitespace, line endings, final newlines. |
| `markdownlint-cli2` | Markdown structure. Prettier does not touch Markdown, so they cannot disagree. |
| `typos` | Spelling, excluding the lockfiles and the asset roots. |
| `lychee` | Link targets, offline. |
| `shellcheck` | Every shell script under `scripts/`. |
| `actionlint` | Every GitHub Actions workflow, its structure only — see below. |
| `ripsecrets` | Credential material, with its output suppressed so a match is never logged. |

Third-party hooks are pinned to commit SHAs with a version comment beside each.

`check-added-large-files` runs with `--maxkb=768`, and that limit is why the exclusion set
has to exist rather than being a convenience: the GLB is 16 MB, the viewer 26 MB, and the
largest texture over 2 MB. The limit still stands everywhere else, so a large file added
outside the asset roots — a screenshot in `docs/`, a build output committed by mistake — is
refused. An asset belongs under `assets/`, where the manifest lists it, not under a raised
limit.

One gap is worth knowing about rather than being surprised by. `actionlint` analyses a
`run:` block by handing it to `shellcheck`, and it reports nothing at all when it cannot find
`shellcheck` on its own `PATH`. Under `prek` each hook gets its own environment, so the
shell embedded in a workflow goes unread. Every `run:` in the studio's two workflows is one
`just` recipe, so there is nothing there to read today; a longer block added later deserves
a `shellcheck` run by hand until the gap is closed.

## The mutating counterpart

`.pre-commit-fix.yaml` holds the hooks that write: Ruff autofix and format, end-of-file and
trailing-whitespace repair, and `markdownlint --fix`. It carries the same `exclude`, is never
installed as a hook, and runs only from `just fix`.

## In continuous integration

`.github/workflows/ci.yml` runs the same recipes in three jobs, and those three are the whole
of continuous integration here. Each job checks out without persisting credentials, then
installs the toolchain through the shared composite action from the tooling repository,
pinned to the commit its `v0.3.0` tag names, with no input overridden.

- **`frontend`** runs `just sync`, then `lock-check`, `frontend-static`, `frontend-coverage`
  and `frontend-build`.
- **`documents`** runs `just sync`, then `lint`, `check-docs` and `check-agents`. The last two
  repeat what `lint` already ran, so a documentation or agent-contract regression names
  itself in the step list rather than inside `lint`.
- **`assets`** checks out with `lfs: false`, then runs `just sync-python` and `check-assets`.
  The checker needs only the Python environment, so the job installs no `node_modules` and
  carries no registry token.

`NODE_AUTH_TOKEN`, set to the run's own token, sits on the `just sync` step of the `frontend`
and `documents` jobs and on nothing else: a step with no use for the credential should not carry one. The workflow
holds `contents: read` and `packages: read` and nothing more.

`lfs: false` is the checkout's default, and it is written out in the `assets` job because
the job depends on it. The checker verifies an LFS-tracked file from the pointer it checks
out as — the oid a pointer carries is the object's sha256 — so the job never fetches an
object and spends none of the LFS bandwidth. Nothing in CI runs a command that does not exist
in the `Justfile`, no job carries a `paths` filter or a `name:`, and the job ids are the check
names.

The deploy is a separate workflow, `pages.yml`, which runs after `CI` completes and publishes
only a push to `main` that passed and is still `main`'s head; see
[Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md).

## On `main`

`main` is protected, and `frontend`, `documents` and `assets` must all pass before a branch
merges into it. Those three names are the CI jobs, and they are the only required checks.

The branch is not required to be up to date with `main` first, and no review is required —
neither earns its cost on a repository with one author. Force pushes and deletion are
refused. Administrators are not bound by the rule, so the direct push remains available when
it is genuinely wanted; the protection is there to stop an unproved merge, not to stop the
author. None of this is in a file: `scripts/bootstrap_repo.sh` applies it, with the three
names passed to its `--checks` option, and
[Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md) says when it is run.

What the protection buys is narrower than it sounds. Two paths still reach `main` ahead of a
green run: the administrator pushing directly, and an ordinary merge, because three green
checks are green for the branch, not for the `main` the merge produces. Neither reaches the
site unchecked, because `pages.yml` deploys only a commit whose own CI run passed. Watch the
run in both cases anyway, because `main` is what the next branch starts from.

## Related pages

- [Commands](commands.md)
- [Testing](testing.md)
- [Quality philosophy](../explanation/quality-philosophy.md)
