---
title: "Repository map"
kind: "project"
audience: [contributor, maintainer, agent]
canonical_for: [repository_layout]
requires: []
---

# Repository map

The site sits at the repository root. There is no `frontend/` directory because there is
no backend to be a sibling of.

`src/` is the site: a few routes, the lockup, and the one module that consults the device.
The design system is not here; it is installed from the platform package. What makes the
studio different from a game is `assets/`, which keeps the sources, and
`static/pose-studio/`, which is what the site serves of them.

```text
.
├── AGENTS.md              Engineering conventions and the agent working agreement
├── CLAUDE.md              One line, deferring to AGENTS.md
├── README.md, CHANGELOG.md, SECURITY.md
├── Justfile               Every supported command
├── package.json           The site: Svelte, SvelteKit, Vite, Vitest, and the platform package
├── pyproject.toml         Repository tooling only: prek, ruff, Pillow and biscuit-games-tooling
├── .gitattributes         Line endings, and which sources go through Git LFS
├── svelte.config.js       adapter-static, and the base path read from BASE_PATH
├── vite.config.ts         Vitest, and the coverage floor over src/lib/
├── src/
│   ├── app.html           The page shell, stating the platform's default appearance
│   ├── app.d.ts           SvelteKit's ambient types
│   ├── lib/
│   │   ├── brand.ts       The site's name, title and description, written once
│   │   ├── appearance.ts  The device's preferences, written on the document element
│   │   └── components/    Lockup.svelte, the platform wordmark with the studio's name
│   └── routes/            The home page, the model page and the gallery, prerendered
├── assets/
│   ├── manifest.json      Every asset's size, sha256, storage and source
│   ├── models/biscuit/    The approved model: README, model/, poses/, previews/, qa/,
│   │                      src/ (its own Blender and Python scripts) and textures/
│   └── illustrations/good/  The cel set: eleven generated, vetted illustrations
├── static/
│   ├── .nojekyll          Tells Pages to serve the build as it is
│   └── pose-studio/       The viewer, and the GLB and overview image it links
├── tests/                 Vitest suites, never colocated with src/, and fixtures/
├── docs/                  This handbook
├── scripts/               The first run, the asset checker, the model rebuild, the bootstrap
├── .agents/skills/        Canonical agent procedures, eight of them
├── .claude/skills/        A bridge per skill, each deferring to .agents/
├── .codex/skills/         The same bridge, for a different reader
└── .github/workflows/     ci.yml, the three required checks; pages.yml, the deployment
```

Other directories appear once the tools have run, and none of them are tracked:
`node_modules/`, `.venv/` and `.svelte-kit/` hold what the installs and SvelteKit write,
and `build/` and `coverage/` hold output. They are gitignored because `just check`
snapshots the worktree between recipes, and a generated file Git can see aborts the run
before the recipe's own exit code is read. `assets/biscuit_pics` is gitignored too: it is
the link a model rebuild places for as long as the rebuild runs.

## What each part is responsible for

| Path | Responsibility |
| --- | --- |
| `src/lib/` | Everything the site computes rather than renders: the name in `brand.ts`, and in `appearance.ts` the two attributes the device decides, derived through the preferences port the platform package exports and written on an element the caller passes in. `components/Lockup.svelte` is the platform's `Wordmark` with the studio's name. Nothing lands here without a test, because the coverage floor measures exactly this directory. |
| `src/routes/` | Assembling the platform's components and the studio's lockup into pages, and the only place `document` is reached, inside `onMount` in the layout. Prerendered, so nothing here may assume a request. Outside the coverage glob, so it holds no logic worth testing. |
| `assets/` | The sources. Nothing under it is served: the site imports the illustrations it shows, and links the viewer, which lives under `static/`. Every file is listed in `assets/manifest.json` and nothing is edited by hand; an import follows [Import an asset](../how-to/import-an-asset.md) and a rebuild follows [Rebuild the model](../how-to/rebuild-the-model.md). The model's own scripts under `assets/models/biscuit/src/` run inside Blender against its API and were never written to this repository's lint rules, so they sit in the one exclusion set every linter shares, with the rest of the imported files. |
| `static/pose-studio/` | What the site serves byte for byte: the viewer, `model/biscuit-poseable.glb` and `previews/pose-overview.jpg`. The three sit beside each other because the viewer links the GLB and the overview image by relative path, so moving one breaks it. Each is an ordinary Git blob, never an LFS object, because Pages would serve the pointer text. See [Large files](../explanation/large-files.md). |
| `tests/` | Vitest suites named for what they cover, not for the file they mirror, and `fixtures/exif-gps.jpg`, the image the asset checker's self-test must refuse. |
| `docs/` | This handbook. Registered in `docs/manifest.yml`, reachable from `docs/README.md`, and held to the [documentation contract](../reference/documentation-contract.md). There is no `docs/specs/`: every rule a surface obeys is the platform's. |
| `scripts/` | `initialize.sh`, the first run; `check_assets.py`, the manifest checker behind `just check-assets` and `just assets-manifest`; `rebuild_model.sh`, behind `just model-rebuild`; and `bootstrap_repo.sh`, which applies the repository settings no file carries. The checkers every Biscuit Games repository runs are not here: they are the console scripts of the `biscuit-games-tooling` package, pinned in `pyproject.toml`. |
| `.agents/skills/` | The eight agent procedures, canonical. `.claude/skills/` and `.codex/skills/` mirror them one file per skill, each pointing at the `.agents/` original and adding nothing of its own. |
| `.github/workflows/` | `ci.yml` runs the `frontend`, `documents` and `assets` jobs; `pages.yml` deploys the site after CI passes. See [Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md). |

## Where each part came from

The studio was assembled by hand rather than rendered from the template; see
[Decision 0005](../decisions/0005-assembled-by-hand.md). Each group of files names its
source repository and the commit it was taken at, so a later change upstream can be
compared with what was copied.

| Files | Source |
| --- | --- |
| The toolchain configuration, the hook gate, the `Justfile`, the skills, the handbook's shape | The hub, `steven-cutting/biscuit_games` at `575e3dd` |
| The agent contract's shape, the app shell, `pages.yml`, `SECURITY.md`, `scripts/bootstrap_repo.sh` | The template, `steven-cutting/biscuit_games_template` at `2283589` |
| The validators, the composite action `ci.yml` uses, the shared Pages workflow | The tooling repository, `steven-cutting/biscuit_games_tooling` at `v0.3.0` |
| `.npmrc` | Poodl at `a2860fc` |
| Everything under `assets/` and `static/pose-studio/` | `biscuit_pics` at `1d9d358`, each file's path recorded in its manifest `source` |
| `scripts/check_assets.py`, `scripts/rebuild_model.sh`, `src/lib/appearance.ts`, `src/lib/brand.ts`, this handbook's prose | Written here |

## What is not here

The absences are as deliberate as the contents, and describing any of them as present is
wrong rather than merely early.

- **The rebuild chain.** The earlier studies the model's build reads,
  `biscuit_pics/generated/3d/` in `biscuit_pics`, are 1.9 GB and stay there, cited by path
  and commit. A rebuild points at a checkout of them; see
  [Rebuild the model](../how-to/rebuild-the-model.md).
- **The photographs of the real dog.** `biscuit_pics/raw/` holds 163 of them, many with
  camera metadata intact. None is copied without the maintainer's approval of that
  photograph; see [Content policy](../explanation/content-policy.md).
- **The reference art.** `inspiration/` is third-party copyrighted material kept as style
  reference only.
- **The rejected work and the other pipelines.** `biscuit_pics/generated/bad/` is rejected
  work and `model_sheets/` is a separate pipeline that has not been reviewed for the
  studio.
- **The discarded Chrome profile.** `ai_tmp/` in `biscuit_pics` was an isolated browser
  profile from the viewer's checks, and is working state rather than an asset.
- **A component workshop.** No Storybook, no Chromatic and no `stories/`, because the
  studio authors no shared component; see
  [Decision 0009](../decisions/0009-no-component-workshop-yet.md).
- **Specifications, and the package build.** No `docs/specs/`, no `dist/` and no publish
  workflow: nothing here states a rule or ships a package.

## Related pages

- [Purpose and scope](purpose-and-scope.md)
- [The platform upstream](platform.md)
- [Architecture](../explanation/architecture.md)
- [Commands](../reference/commands.md)
