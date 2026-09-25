---
title: "Configuration"
kind: "reference"
audience: [contributor, maintainer, operator, agent]
canonical_for: [configuration_reference]
requires: []
---

# Configuration

There is no runtime configuration. A static site has no process to configure, so everything
below is read at build time, read by a tool, or is a fixed part of the source.

## Build-time environment

| Variable | Default | Effect |
| --- | --- | --- |
| `BASE_PATH` | empty | Where the site sits inside its domain. Read into `paths.base` by `svelte.config.js`. |

That is the whole list for the site. SvelteKit's `PUBLIC_` convention is available but
unused: a value baked into a public static bundle is not configuration, it is a constant,
and constants belong in source where they can be reviewed.

### The base path

`BASE_PATH` is `/biscuit_studio` when the site is built for Pages and empty everywhere else.
`pages.yml` does not write the value down: it passes the shared workflow a `base_path` made
from the repository's name, read from the event that started the run, and the shared
workflow sets `BASE_PATH` from it. The address Pages serves a project site at is that same
name, so the two cannot drift apart; see
[Decision 0004](../decisions/0004-a-project-pages-site.md).

Locally it is unset, `paths.base` is the empty string, and `just dev` and a plain
`just frontend-build` mount at `/`. SvelteKit writes prerendered links relative to the page,
so the same build works under either base — see
[Architecture](../explanation/architecture.md).

Everything under `static/` is served beneath the base too: the viewer is at
`/biscuit_studio/pose-studio/viewer.html` on Pages and at `/pose-studio/viewer.html` locally.
The routes reach it through `asset()` from `$app/paths`, which is typed against the files
under `static/`, so a wrong path fails `svelte-check`.

If you set the variable locally to see what the deployed build looks like, it belongs on the
preview as well as on the build. `svelte.config.js` reads it when the build is generated and
again when `just preview` decides where to mount the output, so a value given to one and
withheld from the other serves the site at a path the build was not made for.
[Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md) has the two commands.

## Tooling environment

Two things are read by tools rather than by the build, and neither reaches the bundle.

| Variable | Read by | Effect |
| --- | --- | --- |
| `NODE_AUTH_TOKEN` | npm, in CI only | The run's own token, set on the one step that runs `just sync` in each job and on nothing else. npm reads it to install the platform package from GitHub Packages. No stored secret backs it; it is minted for the run and discarded with it. |
| `BLENDER` | `scripts/rebuild_model.sh` | The Blender executable `just model-rebuild` runs. Defaults to the macOS application bundle. |

On a laptop, the registry token lives in `~/.npmrc`, never in this repository, as one line:

```text
//npm.pkg.github.com/:_authToken=<your token>
```

The token needs `read:packages`; GitHub Packages refuses an anonymous read even of a public
package. The committed `.npmrc` carries only the line that maps the `@steven-cutting` scope
to that registry. [Develop locally](../how-to/develop-locally.md) says how to make the token.

## Configuration files

| File | Governs |
| --- | --- |
| `svelte.config.js` | The static adapter with `strict: true`, preprocessing, and the base path. |
| `vite.config.ts` | The dev server, including `server.fs.allow: ['assets']` so `just dev` serves the gallery's drawings; the jsdom unit suite; and the coverage glob and thresholds. |
| `tsconfig.json` | Strict TypeScript, plus `noUncheckedIndexedAccess`, `noImplicitOverride`, `noFallthroughCasesInSwitch`, `isolatedModules` and `checkJs`. |
| `eslint.config.js` | Flat config over the recommended, `strictTypeChecked` and Svelte presets, ignoring `assets/` and `static/`. It declares no rule overrides of its own. |
| `.prettierrc.json` | 100 columns, single quotes, no trailing commas, Svelte block order. |
| `.prettierignore` | Notably excludes Markdown, which markdownlint owns, `docs/manifest.yml`, which is strict JSON despite the extension, and `assets` and `static/pose-studio`. |
| `.markdownlint-cli2.jsonc` | Markdown rules, including the exemptions the documentation contract needs; ignores the asset directories but not `assets/models/biscuit/README.md`. |
| `.editorconfig` | Whitespace. LF, UTF-8, two spaces, four for Python and the `Justfile`, and every rule unset under the two asset roots. |
| `lychee.toml` | Link checking, offline by default; excludes the asset directories but not the model's README. |
| `pyproject.toml` | The pinned Python tooling; Ruff's rules; the `typos` exclusions; and `[tool.biscuit-games-tooling]`, whose `recipes` is the gate `just check` runs and whose `predicates` a page's `requires` may name (there are none). |
| `.pre-commit-config.yaml` | The read-only gate. Installed as the hook. |
| `.pre-commit-fix.yaml` | The mutating counterpart. Run only by `just fix`. |
| `.gitattributes` | Line endings, the three LFS patterns, and the binary files kept byte-identical; [Large files](../explanation/large-files.md) explains each line. |
| `.npmrc` | The one line mapping the platform's scope to GitHub Packages. No token. |
| `.python-version` | `3.14`, for uv. |
| `assets/manifest.json` | Every asset's size, sha256, storage, source and licence; [Asset manifest](asset-manifest.md) is the format. |

The six files that carry the one exclusion set — the pre-commit pair, `.prettierignore`,
`eslint.config.js`, `.markdownlint-cli2.jsonc`, `lychee.toml` and `pyproject.toml` — change
together or not at all. [Quality gates](quality-gates.md) says which paths are in it and
why.

## Values the studio does not decide

The platform's figures — the two contrast floors, the comfortable touch target, the
narrowest supported width, the durations, the palette itself — are declared in the platform's
specification modules and arrive here as the stylesheet and the components that already meet
them. The studio mirrors none of them: there is no `src/lib/config.ts`, and no number the
platform owns is written down a second time in this repository.

A figure a page here needs is read from the hub's page that states it, reached through
[The platform upstream](../project/platform.md), and used by naming the token or the
component that carries it rather than by copying the value.

## Version pins

Exact versions, no ranges, in `package.json` and `pyproject.toml` alike. Node and npm are
additionally constrained by `engines` and recorded in `volta` in `package.json`; Python by
`.python-version`. See [Maintain dependencies](../how-to/maintain-dependencies.md).

| Pin | Version | Where |
| --- | --- | --- |
| Node | 26 (26.5.1 locally) | `engines`, `volta`, the composite action's default |
| npm | 11.17.0 | `packageManager`, `volta`, the composite action's default |
| uv | 0.11.18 | the composite action's default |
| Python | 3.14 | `.python-version`, the composite action's default |
| just | 1.51.0 | the composite action's default |
| `biscuit-games-tooling` | `v0.3.0` | `pyproject.toml`, as a Git dependency at the tag |
| Pillow | 12.3.0 | `pyproject.toml`, for the asset checker's EXIF read |
| `@steven-cutting/biscuit-games` | 1.1.0 | `package.json`, as a dependency, because the built site ships its components |

CI takes the first five from the shared composite action, called at the commit the tooling
package's `v0.3.0` tag names with no input overridden, because every default is already the
studio's pin. The actions in both workflows are pinned to commit SHAs with the tag in a
comment.

`scripts/bootstrap_repo.sh`, which applies the repository settings no file carries, is the
template's script copied verbatim; the studio passes it the three check names rather than
editing it.

## Related pages

- [Commands](commands.md)
- [Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md)
- [Maintain dependencies](../how-to/maintain-dependencies.md)
- [Decision 0004: A project Pages site](../decisions/0004-a-project-pages-site.md)
