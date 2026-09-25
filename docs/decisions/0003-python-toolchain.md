---
title: "Decision 0003: A Python toolchain in a frontend repository"
kind: "decision"
audience: [maintainer, agent]
canonical_for: [decision_python_toolchain]
requires: []
---

# Decision 0003: A Python toolchain in a frontend repository

*Carried from the Biscuit Games template's decision 0004 at `2283589`, and restated for a repository that is not a game.*

## Context

The studio's site ships no Python. The hook gate it inherits runs on `prek` under `uv`, and
the documentation and agent contracts are enforced by two Python checkers. The studio adds
a third check of its own, over the asset manifest, and it has to read the EXIF of every
image it lists. A frontend repository could avoid Python entirely by moving the hook runner
to a Node equivalent and rewriting the checkers in TypeScript.

## Decision

Keep the Python toolchain. `pyproject.toml` declares a virtual project — `package = false`
— whose dependencies are `prek`, `ruff`, `pillow` and `biscuit-games-tooling`, each pinned
exactly and locked in `uv.lock`. The first two are tools; `pillow` is the one library the
asset checker needs, to read EXIF; the last is the package whose console scripts are the
documentation and agent checkers themselves, pinned to a release tag of
`steven-cutting/biscuit_games_tooling`.

Ruff lints the Python this repository adds. `scripts/` holds the first-run script,
`check_assets.py` and the rebuild script. The model's own Blender scripts under
`assets/models/biscuit/src/` are Python too, but they run inside Blender and are excluded
from the gate, because they are imported assets rather than this repository's code.

## Consequences

Contributors need `uv` as well as Node, and both have to be installed before
`just initialize`, which runs each of them to lock and install its own dependencies.
Neither the site nor anything it serves contains any Python.

The two contracts stay as they are, rather than being rewritten and re-debugged. That is
most of the value: `bg-validate-docs` and `bg-validate-agents` come from a working
implementation, so their behaviour is known rather than newly invented. Every Biscuit Games
repository runs the same release of them, and a fix arrives as a moved pin rather than as
an edit merged into each copy.

The asset checker is one script and one library, where the same check in Node would need
an EXIF parser chosen and trusted from scratch. Pillow's wheels bundle the image formats
the checker opens, which ties the gate to what those wheels support; a release that
dropped one fails the checker's self-test rather than passing silently.

`prek` brings pinned third-party hooks with it — `typos`, `lychee`, `shellcheck`,
`actionlint`, `ripsecrets`, `editorconfig-checker` — each locked to a commit SHA. Assembling
an equivalent set on Node would be a project in itself.

The cost is an extra toolchain to install, keep current, and explain. It is accepted
deliberately rather than by drift.

## What would reopen this

A Node-native hook runner with the same pinned-hook ecosystem, or the checkers becoming so
simple that rewriting them is cheaper than keeping Python around. Either would have to
replace the whole tooling package, not only the two validators, because the gate runner is
in it as well, and would have to bring an EXIF reader the asset checker could trust.

## Related pages

- [Quality gates](../reference/quality-gates.md)
- [Maintain dependencies](../how-to/maintain-dependencies.md)
- [Asset manifest](../reference/asset-manifest.md)
