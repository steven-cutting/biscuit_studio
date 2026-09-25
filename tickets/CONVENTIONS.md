# Conventions for building `biscuit_studio`

This document is the design every ticket under `tickets/` obeys. A ticket cites it by
section (`CONVENTIONS.md §3`) instead of restating it, and embeds exact content only
where the agent executing the ticket would otherwise have to guess. Where a ticket and
this document disagree, this document wins and the ticket is corrected. Changes to this
document go through a pull request on `main`, never through a lane branch, because every
lane reads it.

## 0. What is being built, and where the sources are

`steven-cutting/biscuit_studio` (this repository; today one commit `1378ee4` holding an
empty `README.md`, no remote, no GitHub repository) becomes the Biscuit Games studio: the
repository where the platform's graphical assets are developed — the poseable 3D model of
Biscuit, the renders and exports made from it, and the 2D illustrations — and a static site
on GitHub Pages that shows them, built on the platform's design system so it reads as the
same product as every game. It consumes `@steven-cutting/biscuit-games` exactly as a game
does; nothing depends on it. Finished assets leave it by copy, recorded in a ledger a
consumer's gate can verify (§1, decision 2).

Five repositories are the sources, cited with a letter and, where it matters, line numbers
that refer to these exact commits:

| Letter | Repository | Local clone | Commit |
| --- | --- | --- | --- |
| **H** | `steven-cutting/biscuit_games`, the hub that publishes the platform package | `/Users/scutting/projects/biscuit_games` | `575e3dd` (HEAD on 2026-09-23; tag `v1.1.0` sits two commits earlier at `ca0ca0a`, and every file this design takes from H is identical at both) |
| **P** | `steven-cutting/poodl`, the first game | `/Users/scutting/projects/poodl` | `a2860fc` |
| **T** | `steven-cutting/biscuit_games_template`, the Copier template that renders a game | `/Users/scutting/projects/biscuit_games_template` | `2283589` |
| **G** | `steven-cutting/biscuit_games_tooling`, the reusable workflows, the composite action and the `biscuit-games-tooling` Python package | `/Users/scutting/projects/biscuit_games_tooling` | `6c5c07f`, which tag `v0.3.0` names (`v0.1.0` = `be41556`, `v0.2.0` = `c0a76b6`) |
| **D** | the `biscuit_pics` worktree `very_nice_three_deeez`, where the approved model lives today | `/Users/scutting/.supacode/repos/biscuit_pics/very_nice_three_deeez` | `1d9d358` |

D is a git worktree of `/Users/scutting/projects/biscuit_pics` on branch
`very_nice_three_deeez`; its object store is 2.7 GB of loose objects and its working tree
3.2 GB. Nothing here imports that history. D is read-only for every ticket.

Tooling verified on this machine on 2026-09-23: uv 0.11.18, just 1.51.0
(`rust-just==1.51.0`), node 26.5.1 with npm 11.17.0, Python 3.14, git-lfs 3.8.0 (installed,
filters configured globally), `gh` 2.100.0 authenticated as `steven-cutting` (scopes `repo`,
`workflow`, `read:org`, `gist`, `admin:public_key`; no `read:packages`), Blender 5.2.1 LTS at
`/Applications/Blender.app`, and a `~/.npmrc` carrying a `npm.pkg.github.com` line (its
token is never read, printed or copied). `typos`, `lychee`, `prek`, `markdownlint-cli2` and
`editorconfig-checker` are not on the PATH; the gate installs them through `uv sync` and
the hook cache. Pillow's current release on PyPI is 12.3.0.

## 1. Decisions taken with the maintainer, and the facts everything rests on

Decisions, taken on 2026-09-23:

1. **The hub's brand rule changes first.** H `docs/design/direction.md` lines 262-263 list
   "3D rendering" and "anything carrying generative-AI artefacts" under **Avoid**, and H
   `docs/design/character.md` (lines 20-21, 91, 106-110) expects Biscuit to be drawn by a
   commissioned illustrator against a reference sheet. The approved model is cel-shaded 3D
   and the `good/` set was generated. Ticket C01 produces a hub decision record and edits
   both pages so that cel-shaded renders from the approved model, and generated art the
   maintainer has vetted, are permitted. Until C01 lands nothing the studio makes is
   promoted into the hub or a game; the studio itself, and its site, are built regardless.
2. **The studio consumes the hub; the hub never depends on the studio.** The site installs
   `@steven-cutting/biscuit-games` at an exact version, like a game (H
   `docs/how-to/consume-the-hub.md`). A finished asset reaches the hub or a game by copy,
   and every copy is recorded in a **structured ledger with a small command-line tool, so
   that a copy is deterministic and a consumer's CI can verify it**. The ledger's design is
   ticket C02, a discussion ticket that produces a design page, a decision and follow-up
   tickets rather than code. Until it lands, the interim procedure is
   `docs/how-to/promote-an-asset.md`: copy by hand, record the studio commit and the sha256
   in the consumer, and write the item into the studio's `docs/operations/hub-handover.md`.
3. **Site stack.** A static SvelteKit site (`@sveltejs/adapter-static`, full prerendering,
   `paths.base` from `BASE_PATH`) wearing the platform's `HeaderBar`, `Wordmark` and
   `app.css`. The existing viewer — D `models/biscuit/viewer.html`, 27,561,425 bytes, a
   hand-written WebGL2 renderer with no dependency and no network request — is served
   **unchanged** as a static file under `static/pose-studio/`, save for three `href`
   rewrites §3 lists. Ticket C03 ports it to a maintained three.js component later.
4. **Storage.** Fresh history: the studio's first commit carries a provenance note naming D
   `1d9d358`, and nothing is filtered out of `biscuit_pics`. Git LFS holds the `.blend` and
   the two large QA JSON files; the GLB, the textures, the previews and the viewer stay
   ordinary blobs because GitHub Pages cannot serve an LFS object. The 1.9 GB rebuild chain
   under D `biscuit_pics/generated/3d/` stays where it is and is cited by path and commit.
5. **Toolchain assembled by hand** from H, P, T and G, each file with its source in the
   provenance table (S00). No Copier link: T renders only a game (four questions, no
   toggle), and a render whose handbook pages were deleted breaks on its next
   `copier update` because `docs/manifest.yml` is re-rendered.
6. **Address.** A public repository and a project Pages site at
   `https://steven-cutting.github.io/biscuit_studio/`, built with
   `BASE_PATH=/biscuit_studio`. The custom domain `pnut.fans` stays with Poodl (H decision
   0012) and nothing here touches it.
7. **What CI checks.** The site (`frontend`), the handbook and the agent contract
   (`documents`), and a sha256 manifest over every asset (`assets`). The Blender pipeline
   is a documented local recipe and is never run in CI.
8. **What is copied from D:** `models/biscuit/` whole (94 files, 92 MB) and `good/` (11
   PNG files, 14 MB). Nothing else: `inspiration/` is third-party copyrighted reference art,
   `biscuit_pics/raw/` is 163 photographs of the real dog, `generated/bad/` is rejected
   work, `generated/3d/` is the rebuild chain, `model_sheets/` is a separate pipeline, and
   `ai_tmp/` is a discarded Chrome profile.
9. **Raw photographs.** No ticket copies a photograph of the real dog. If one is ever
   copied, the maintainer approves it first, one photograph at a time, and it is committed
   only after every metadata field has been stripped from it; `just check-assets` refuses
   any image carrying an EXIF field beyond its resolution regardless of approval, and any
   TIFF. §5.
10. **No component workshop in the first release.** The studio authors no shared
    component; it mounts the platform's. Storybook and Chromatic are not installed, and
    decision 0009 in the studio's own record says why and what would reopen it (C03 does).

Facts, each verified in source, that shape the mechanism:

1. **`bg-run-allium` exits 2 when there is no `.allium` file** (G
   `src/biscuit_games_tooling/run_allium.py` line 40, `NO_INPUTS = 2`). The studio has no
   `docs/specs/`, so `[tool.biscuit-games-tooling] recipes` in `pyproject.toml` omits
   `check-specs` and `analyse-specs`, the `Justfile` carries neither recipe, and the two
   `check-specs`/`analyse-specs` hooks are absent from `.pre-commit-config.yaml`.
2. **`bg-validate-agents` requires six literal phrases in `AGENTS.md`** (G
   `src/biscuit_games_tooling/validate_agents.py` lines 47-54): `untrusted`, `just check`,
   `explicit authorization`, `ai_tmp/`, `docs/specs/` and `runes`. The studio's `AGENTS.md`
   therefore says, in so many words, that it has no `docs/specs/` of its own and that the
   platform's modules govern its surfaces, and states the runes rule for its Svelte. The
   bridge body is exactly `BRIDGE_BODY` (lines 23-26); `.claude/settings.json` is the one
   tolerated extra file (line 32).
3. **GitHub Packages never reads anonymously.** `npm ci` on a laptop needs a
   `read:packages` token in `~/.npmrc` (H `docs/how-to/consume-the-hub.md` lines 20-51);
   CI installs with the run's own `github.token`, and no package grant is needed because
   the package is public (T `tickets/C03-repository-bootstrap.md`, "Deviations"). The
   committed `.npmrc` carries the scope line and nothing else.
4. **GitHub Pages cannot serve an LFS object.** A Pages artefact built from a checkout with
   `lfs: false` contains the pointer text, so anything the site links to directly is an
   ordinary blob. An LFS pointer carries `oid sha256:<hex>` and `size <bytes>`, which is
   what lets `scripts/check_assets.py` verify an LFS-tracked file from the pointer alone,
   and lets every CI job check out with `lfs: false`.
5. **The hook gate would refuse the assets unless told otherwise.**
   `check-added-large-files --maxkb=768` (H `.pre-commit-config.yaml` line 76) refuses a
   16 MB GLB; editorconfig-checker, typos and lychee would each read the 26 MB viewer
   (base64 textures inside); ruff would lint the Blender scripts under
   `assets/models/biscuit/src/` against `strict` rules they were never written to;
   Prettier would reformat the viewer; `eslint .` would walk `assets/`. §2 names the
   exclusions in each file, and they are one pattern set written in six places.
6. **G's `game-ci.yml` cannot be called.** It hard-codes `storybook-*`, `check-specs` and
   `analyse-specs` (its three jobs) with no input to switch one off, so the studio's
   `ci.yml` is bespoke, in the shape of H `.github/workflows/ci.yml`, using G's composite
   action `actions/setup-toolchain` at the `v0.3.0` commit. G's `game-pages.yml` is called
   as-is with `base_path`, exactly as T `template/.github/workflows/pages.yml` does.
7. **The coverage floor stays.** `vite.config.ts` measures `src/lib/**` at 90 on all four
   figures. Everything under `src/lib/` is tested; route-only code lives under
   `src/routes/`, which the glob does not reach.
8. **The three large files are byte-identified.** sha256 at D `1d9d358`:
   `models/biscuit/viewer.html`
   `8838e723399ee4e1eba5e9926da4503fe639459f1b809bc3bf9575856e55170a` (27,561,425 bytes);
   `models/biscuit/model/biscuit-poseable.glb`
   `51d16c1826b2c3ad6ad85fcb176a73e0d1c7a0ac3665ad10f1b6700e9e9be716` (16,112,380 bytes);
   `models/biscuit/model/biscuit-poseable.blend`
   `95d164730e9354ab3d9bd561a73180690bbb055fffa9bf230c735f735234b4c3` (12,004,899 bytes).
   S02 asserts these before and after the copy; §3's `.gitattributes` is what keeps a
   checkout byte-identical to the commit.
9. **Four native renders carry resolution EXIF; no other image in scope carries any.**
   Pillow's `getexif()` returns an empty mapping for every PNG under D `good/` and D
   `models/biscuit/textures/`, and for every file under D `models/biscuit/previews/` except
   the four under `native/` (`lying.png`, `paw-raised.png`, `sitting.png`,
   `standing.png`), which carry exactly `XResolution` and `YResolution` = 72 (checked
   2026-09-23 on D `1d9d358`, after S00's review; the first check had missed them). The
   EXIF check in §4 allows the resolution triple and refuses every other tag, so the first
   import passes as copied, and its fixture test is what proves it is live. S02's Step 6
   sweep counts any tag, so it reports those four files; S02 corrects its expected line.
10. **The viewer links four relative targets** (counted with `grep -o 'href="[^"]*"'`):
    `model/biscuit-poseable.blend` twice, `model/biscuit-poseable.glb` once,
    `previews/pose-overview.jpg` three times, `README.md` once. It fetches nothing; every
    texture and the geometry are inlined. §3 says which of those are kept beside it and
    which are rewritten.

## 2. Repository tree (exact paths), with the ticket that owns each

Legend: the owner is the ticket whose Files-touched table lists the path in its final form;
S00 creates every path below either final or as a stub the owner replaces. Paths marked
**(no lane)** are written by S00 and touched by no lane; a lane that needs a change there
hands it back. "H", "P", "T", "G", "D" as §0.

```text
.editorconfig                 S00   H verbatim, plus the two sections §2.1 gives
.gitattributes                S00   §3, exact
.gitignore                    S00   T's `template/.gitignore` minus the allium, storybook, chromatic and vitest-browser blocks (lines 24-47), plus one line `assets/biscuit_pics` (the symlink `scripts/rebuild_model.sh` places so the model's build scripts find the earlier studies; §3). No LFS cache entry: git-lfs keeps its cache under .git/
.markdownlint-cli2.jsonc      S00   H's, `ignores` gaining the seven §2.1 `assets/…` paths and "static", losing "dist" and "storybook-static" (S02 narrowed "assets" so the model README is linted)
.npmrc                        S00   P verbatim (one line, the scope)
.pre-commit-config.yaml       S00   H's with the `exclude` regex of §2.1, minus the eslint `files` entries that name storybook, minus check-specs and analyse-specs
.pre-commit-fix.yaml          S00   H's with the same `exclude`
.prettierignore               S00   H's minus `storybook-static`, plus `assets` and `static/pose-studio`
.prettierrc.json              S00   H verbatim
.python-version               S00   `3.14`
AGENTS.md                     S00   §7 (S08 edits the Provenance section only)
CLAUDE.md                     S00   `@AGENTS.md` and one newline, byte-pinned
CHANGELOG.md                  S00   stub; S08 writes 0.1.0
README.md                     S00   replaces the empty file; S08 writes the real one
SECURITY.md                   S00   T `template/SECURITY.md` verbatim (it already says "this repository" throughout, and its private-reporting fallback paragraph stays)
Justfile                      S00   §2.2, exact
package.json                  S00   §2.3, exact
package-lock.json             S00   generated; committed
pyproject.toml                S00   §2.4, exact
uv.lock                       S00   generated; committed
eslint.config.js              S00   H's minus the storybook import and spread, `ignores` gaining 'assets/' and 'static/'
svelte.config.js              S00   §2.5, exact
tsconfig.json                 S00   H verbatim
vite.config.ts                S00   H verbatim
lychee.toml                   S00   H's, `exclude_path` gaining the seven §2.1 `assets/…` paths and "static/pose-studio", minus "storybook-static" (S02 narrowed "assets" so the model README's links are checked)
.claude/settings.json         S00   H verbatim
.agents/skills/<8>/SKILL.md   S00   §7, final
.claude/skills/<8>/SKILL.md   S00   bridges, exact body
.codex/skills/<8>/SKILL.md    S00   bridges, exact body
.github/copilot-instructions.md   S00   H verbatim, byte-pinned by the validator
.github/workflows/ci.yml      S04   §8
.github/workflows/pages.yml   S04   §8
scripts/initialize.sh         S00   H's minus lines 15-30 and 32-37 (no browser, no allium), committed 100755
scripts/check_assets.py       S00   §4, final
scripts/rebuild_model.sh      S02   S00 ships a two-line stub that prints "see tickets/S02" and exits 2; S02 replaces it
scripts/bootstrap_repo.sh     S00   T `scripts/bootstrap_repo.sh` verbatim (382 lines), committed 100755; S07 runs it
static/.nojekyll              S00   empty
static/pose-studio/viewer.html                       S02   D `models/biscuit/viewer.html`, three hrefs rewritten (§3)
static/pose-studio/model/biscuit-poseable.glb         S02   D, byte-identical, plain blob
static/pose-studio/previews/pose-overview.jpg         S02   D, byte-identical, plain blob
assets/manifest.json          S02   S00 ships `{"schema_version": 1, "assets": []}` plus a newline; S02 fills it with `just assets-manifest`
assets/models/biscuit/README.md                       S02   D's README adapted (§3)
assets/models/biscuit/model/biscuit-poseable.blend    S02   D, LFS
assets/models/biscuit/model/rig.json                  S02   D
assets/models/biscuit/poses/*.json (4)                S02   D
assets/models/biscuit/previews/** (21 files)          S02   D; `pose-overview.jpg` is not among them, it lives beside the viewer (§3)
assets/models/biscuit/qa/** (10 files; geometry/rigged.json and native-samples.json in LFS)   S02   D
assets/models/biscuit/src/** (15 files)               S02   D verbatim; excluded from every linter (§2.1)
assets/models/biscuit/textures/*.png (36)             S02   D
assets/illustrations/good/*.png (11)                  S02   D `good/`
src/app.html                  S01   T `template/src/app.html` with `data-animations="on"` added as H's line 29 has it
src/app.d.ts                  S00   H verbatim
src/lib/brand.ts              S00   §2.6, exact
src/lib/appearance.ts         S01   §2.7
src/lib/components/Lockup.svelte   S01   T CONVENTIONS §7 shape, `product={STUDIO_NAME}`
src/routes/+layout.svelte     S01   T's plus the `onMount` that wires appearance (§2.7)
src/routes/+layout.ts         S00   T verbatim, "The game" → "The site"
src/routes/+page.svelte       S01   S00 ships a placeholder (one `<main>` with a sentence) so `frontend-build` has a route
src/routes/model/+page.svelte S03
src/routes/gallery/+page.svelte   S03
tests/setup.ts                S00   one line, H verbatim
tests/brand.test.ts           S00   asserts the three constants are non-empty strings and the lockup words are lowercase
tests/lockup.test.ts          S01   T's shape
tests/appearance.test.ts      S01
tests/route.test.ts           S01   T's shape
tests/pages.test.ts           S03
tests/fixtures/exif-gps.jpg   S00   a 1×1 JPEG carrying a GPS IFD, generated by the script §4 shows; the fixture `check_assets.py`'s own test refuses
tests/check_assets.test.py    S00   pytest is not installed; this is NOT a file. `check_assets.py --self-test` is the test (§4)
docs/manifest.yml             S00   §6, complete and final (no lane)
docs/README.md                S00   §6, complete and final (no lane)
docs/**/*.md (every page)     S00 stubs; S05 and S06 replace (§6 says which)
tickets/                      the maintainer's; each ticket edits its own `status:` line
```

`tests/check_assets.test.py` above is listed to say it does not exist. The Python tooling
has no pytest (H's `pyproject.toml` has none, and adding one is a dependency this
repository does not need for one script); the asset checker carries a `--self-test`
subcommand instead, §4.

### 2.1 The one exclusion set, written in six places

The paths every linter skips:

```text
assets/models/biscuit/(model|poses|previews|qa|src|textures)/
assets/illustrations/
static/pose-studio/
```

`assets/models/biscuit/README.md` and `assets/manifest.json` are deliberately not in it:
the README is linted like any Markdown, and `check-json` reads the manifest.

Where each is written:

| File | Form |
| --- | --- |
| `.pre-commit-config.yaml` and `.pre-commit-fix.yaml` `exclude` | three lines added to H's `(?x)` block: `assets/models/biscuit/(model\|poses\|previews\|qa\|src\|textures)/\|`, `assets/illustrations/\|`, `static/pose-studio/\|`, before `uv\.lock$` |
| `.prettierignore` | `assets` and `static/pose-studio`, each on its own line, after `package-lock.json` |
| `eslint.config.js` `ignores` | `'assets/'` and `'static/'` appended to H's array |
| `.markdownlint-cli2.jsonc` `ignores` | the six `assets/models/biscuit/<dir>` paths, `"assets/illustrations"` and `"static"` appended — not `"assets"`, which would hide the README (corrected by S02) |
| `lychee.toml` `exclude_path` | the six `assets/models/biscuit/<dir>` paths, `"assets/illustrations"` and `"static/pose-studio"` appended — not `"assets"`, for the same reason (corrected by S02) |
| `pyproject.toml` `[tool.typos.files] extend-exclude` | `"assets/"` and `"static/pose-studio/"` appended |
| `.editorconfig` | two sections appended: `[assets/**]` and `[static/pose-studio/**]`, each setting `indent_style`, `indent_size`, `end_of_line`, `insert_final_newline` and `trim_trailing_whitespace` to `unset` — the belt under the prek exclude, for editors |

Whether the prek `exclude` alone suffices for editorconfig-checker and typos is an
unverified claim (§10); the `.editorconfig` sections and the typos entry are written
regardless, because a belt costs nothing.

### 2.2 `Justfile` (complete)

H's `Justfile` (`/Users/scutting/projects/biscuit_games/Justfile`) is the source. Take it
whole and make exactly these changes; every recipe not named below is H's verbatim.

- Delete lines 4-6 (the Storybook telemetry export and its comment).
- Delete `install-allium` (lines 39-44), `storybook-browsers` and
  `storybook-browsers-deps` (46-56), `storybook` (67-70), `storybook-build` and
  `storybook-test` (112-122), `check-specs` and `analyse-specs` (133-151), and the whole
  package and publish sections (165-237).
- `frontend-watch` (72-79): keep, and rewrite the comment's mention of
  `vitest.config.ts` to say "left to its own discovery Vitest would still find
  `vite.config.ts`; the pin is kept so the three test recipes read the same".
- After `check-agents`, add:

```just
# ------------------------------------------------------------------ assets ---

# Every file under assets/ and static/pose-studio/ against assets/manifest.json:
# present, listed, and byte-identical to the recorded sha256. An LFS pointer is
# verified from the oid it carries, so a checkout with lfs: false passes and CI
# never fetches an object. Refuses EXIF beyond an image's resolution, and TIFF.
check-assets:
    uv run --frozen python scripts/check_assets.py check

# Rewrites assets/manifest.json from the worktree. The one recipe that writes
# it; it keeps every entry's `source` and `licence` fields and recomputes the
# rest. Run it after an import, then read the diff before committing.
assets-manifest:
    uv run --frozen python scripts/check_assets.py write

# ------------------------------------------------------------------- model ---

# Rebuilds the approved model from its sources. Needs Blender and a checkout of
# biscuit_pics at the commit assets/models/biscuit/README.md names, because the
# build reads the earlier studies there. Never part of `just check`.
#   just model-rebuild /path/to/biscuit_pics
model-rebuild biscuit_pics:
    sh scripts/rebuild_model.sh "$1"
```

- `check` and `check-clean` stay as H has them; `bg-project-check` reads the recipe list
  from `pyproject.toml` (§2.4).

### 2.3 `package.json` (complete)

```json
{
  "name": "biscuit-studio",
  "version": "0.1.0",
  "private": true,
  "description": "The Biscuit Games studio: the models, renders and illustrations behind the games, and the site that shows them.",
  "license": "UNLICENSED",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/steven-cutting/biscuit_studio.git"
  },
  "type": "module",
  "packageManager": "npm@11.17.0",
  "engines": {
    "node": ">=26 <27",
    "npm": ">=11 <12"
  },
  "volta": {
    "node": "26.5.1",
    "npm": "11.17.0"
  },
  "scripts": {
    "prepare": "svelte-kit sync",
    "dev": "vite dev --host 127.0.0.1",
    "build": "vite build",
    "preview": "vite preview --host 127.0.0.1",
    "check": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json --fail-on-warnings",
    "lint": "svelte-kit sync && eslint . && prettier --check .",
    "lint:fix": "svelte-kit sync && eslint . --fix && prettier --write .",
    "format": "prettier --write .",
    "test": "vitest run --config vite.config.ts",
    "coverage": "vitest run --config vite.config.ts --coverage",
    "test:watch": "vitest --config vite.config.ts"
  },
  "dependencies": {
    "@steven-cutting/biscuit-games": "1.1.0"
  },
  "devDependencies": {
    "@eslint/js": "10.0.1",
    "@sveltejs/adapter-static": "3.0.10",
    "@sveltejs/kit": "2.70.2",
    "@sveltejs/vite-plugin-svelte": "7.3.0",
    "@testing-library/jest-dom": "7.0.0",
    "@testing-library/svelte": "5.4.2",
    "@testing-library/user-event": "14.6.3",
    "@types/node": "26.2.0",
    "@vitest/coverage-v8": "4.1.10",
    "eslint": "10.8.1",
    "eslint-plugin-svelte": "3.22.0",
    "globals": "17.9.0",
    "jsdom": "30.0.1",
    "prettier": "3.9.6",
    "prettier-plugin-svelte": "4.1.1",
    "svelte": "5.56.8",
    "svelte-check": "4.7.5",
    "typescript": "6.0.3",
    "typescript-eslint": "8.66.0",
    "vite": "8.2.1",
    "vitest": "4.1.10"
  }
}
```

Every pin is H `package.json` at `575e3dd` (lines 74-110) less Storybook, Chromatic,
publint, `@sveltejs/package`, Playwright and the two `@vitest/browser*` packages. The
platform package is a `dependency`, not a dev dependency, because the built site ships its
components. `private: true` because nothing publishes it.

### 2.4 `pyproject.toml` (complete)

```toml
[project]
# Not `biscuit-games-tooling`, which is the package the dev group installs: uv
# refuses a project that depends on a package sharing its own name.
name = "biscuit-studio-tooling"
version = "0.1.0"
description = "Repository tooling for the Biscuit Games studio. Not the site; see package.json for that."
requires-python = ">=3.14"
dependencies = []

[dependency-groups]
dev = [
  "biscuit-games-tooling @ git+https://github.com/steven-cutting/biscuit_games_tooling@v0.3.0",
  "pillow==12.3.0",
  "prek==0.4.12",
  "ruff==0.16.2",
]

[tool.uv]
# The studio ships no Python package. This project exists so `uv run --frozen`
# can provide a pinned prek, ruff, Pillow and biscuit-games-tooling to the hooks
# and recipes; see docs/decisions/0003-python-toolchain.md.
package = false
default-groups = ["dev"]

[tool.ruff]
line-length = 99
target-version = "py314"
unsafe-fixes = false
src = ["scripts"]
# The Blender scripts under assets/ are the model's own build tooling, run inside
# Blender against bpy, and were never written to these rules. They are excluded
# here as well as in the hook gate so `ruff check .` by hand agrees with it.
extend-exclude = ["assets"]

[tool.ruff.lint]
select = [
  "A", "ANN", "ARG", "B", "BLE", "C4", "COM", "DTZ", "E",
  "EM", "EXE", "F", "FA", "FLY", "FURB", "G", "I", "INP", "INT",
  "ISC", "LOG", "N", "PERF", "PGH", "PIE", "PL", "PTH", "PYI",
  "Q", "RET", "RSE", "RUF", "S", "SIM", "SLF", "T10", "TC",
  "TID", "TRY", "UP", "W",
]
ignore = ["COM812", "E501", "ISC001"]
fixable = ["ALL"]
unfixable = []

[tool.ruff.lint.flake8-tidy-imports]
ban-relative-imports = "all"

[tool.ruff.lint.per-file-ignores]
# A single-file command-line checker: it prints, it takes no annotations beyond
# its own signatures, and it shells out to git by design.
"scripts/**" = [
  "ANN", "BLE001", "EM101", "EM102", "INP001", "PLR0912", "PLR0915",
  "PLR2004", "S404", "S603", "S607", "T201", "TRY003",
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"

[tool.typos.files]
# Lockfiles carry hashes that look like typos; the assets carry base64 and
# Blender's own vocabulary.
extend-exclude = [
  "package-lock.json",
  "uv.lock",
  "assets/",
  "static/pose-studio/",
]

[tool.biscuit-games-tooling]
# What `just check` runs, in order, before `check-clean`. No check-specs or
# analyse-specs: this repository has no docs/specs/, and bg-run-allium exits 2
# on an empty input set rather than passing it.
recipes = [
  "lock-check", "lint", "frontend-static", "frontend-coverage", "frontend-build",
  "check-assets", "check-docs", "check-agents",
]
# Predicates a page's `requires` may name, true when enabled. None.
predicates = {}
```

Whether `pillow==12.3.0` resolves for Python 3.14 alongside the tooling package is an
unverified claim (§10). If it does not, S00 pins the newest that does and records it.

### 2.5 `svelte.config.js` (complete)

```js
import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/**
 * A static site with no server: every route is prerendered and the build is a
 * directory a host serves as-is.
 *
 * `paths.base` reads BASE_PATH, which pages.yml sets to `/biscuit_studio` from
 * the repository name so the app is built to live where Pages serves it; it is
 * empty locally. `just preview` needs the same value the build had. See
 * docs/how-to/deploy-to-github-pages.md.
 */

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({ pages: 'build', assets: 'build', strict: true }),
    paths: { base: process.env.BASE_PATH ?? '' }
  }
};

export default config;
```

No `typescript.config` hook: H's exists only to bring Storybook's directories into the
TypeScript project (H `svelte.config.js` lines 21-40).

### 2.6 `src/lib/brand.ts` (complete)

```ts
/**
 * What this site is called, wherever the platform asks for a name.
 *
 * `STUDIO_NAME` is the words the lockup shows after the platform's own:
 * `Wordmark`'s `product` prop renders "biscuit games / <STUDIO_NAME>", and every
 * page's only `h1` reads exactly that. `STUDIO_TITLE` is the document title and
 * `STUDIO_DESCRIPTION` its description.
 *
 * A file of its own, because this is the one place the name is written: every
 * component, page and test reads it from here.
 */
export const STUDIO_NAME = 'studio';
export const STUDIO_TITLE = 'Biscuit Studio';
export const STUDIO_DESCRIPTION =
  'Where Biscuit is made: the model, the renders and the illustrations behind the games.';
```

### 2.7 Appearance on the document element

The hub's own route writes `data-theme="dark" data-animations="on"` and reads no device
preference (H `src/app.html` lines 2-28 say so and why). The studio does what a game is
told to do (H `docs/how-to/consume-the-hub.md` §4-5): it states the platform default in
`app.html` and, after hydration, derives the two device-dependent attributes through the
port the package exports.

`src/lib/appearance.ts` exports one pure function and one that takes an element:

```ts
import {
  animationsActive,
  highContrastActive,
  type PreferencesPort
} from '@steven-cutting/biscuit-games';

/** The two attributes the device decides, given the studio's fixed settings. */
export function documentAttributes(port: PreferencesPort): {
  animations: 'on' | null;
  highContrast: 'true' | null;
} {
  return {
    animations: animationsActive(true, port.prefersReducedMotion()) ? 'on' : null,
    highContrast: highContrastActive(false, port.prefersMoreContrast()) ? 'true' : null
  };
}

/**
 * Writes them on `root` now and on every change the port reports. Returns the
 * unsubscribe. `root` is passed in rather than read from `document`, so nothing
 * here touches a global and a test hands it a jsdom element.
 */
export function applyAppearance(root: Element, port: PreferencesPort): () => void {
  const write = () => {
    const { animations, highContrast } = documentAttributes(port);
    if (animations === null) root.removeAttribute('data-animations');
    else root.setAttribute('data-animations', animations);
    if (highContrast === null) root.removeAttribute('data-high-contrast');
    else root.setAttribute('data-high-contrast', highContrast);
  };
  write();
  return port.subscribe(write);
}
```

The theme stays `dark`: the studio ships no settings control, so `theme` is the platform
default, `dark_active` is true, and `data-theme="dark"` is stated in `app.html` exactly as
H and T do. `+layout.svelte` calls `applyAppearance(document.documentElement,
createMediaPreferences())` inside `onMount` and returns the unsubscribe; `document` is
reached there and nowhere else, and `src/routes/` is outside the coverage glob. The test
(`tests/appearance.test.ts`) injects `createFakePreferences`, renders nothing, and asserts
on a `document.createElement('div')` — an element the test owns, not a global it stubs —
that the attributes follow `set()`.

## 3. Large-file policy

`.gitattributes` (complete):

```text
* text=auto eol=lf

package-lock.json linguist-generated=true
uv.lock linguist-generated=true

# Large-file policy: docs/explanation/large-files.md. Sources the site never
# serves go through LFS; what the site serves, and what a browser reads, stays
# an ordinary blob because GitHub Pages serves an LFS pointer as text.
*.blend filter=lfs diff=lfs merge=lfs -text
assets/models/biscuit/qa/geometry/*.json filter=lfs diff=lfs merge=lfs -text
assets/models/biscuit/qa/native-samples.json filter=lfs diff=lfs merge=lfs -text

# Binary and generated: never normalised, never diffed, so a checkout is
# byte-identical to the commit and assets/manifest.json stays true.
*.glb -text -diff
*.png -text -diff
*.jpg -text -diff
static/pose-studio/viewer.html -text -diff linguist-generated=true
```

What is LFS, and what is not, with the reason:

| Path | Bytes | Storage | Why |
| --- | --- | --- | --- |
| `assets/models/biscuit/model/biscuit-poseable.blend` | 12,004,899 | LFS | the native source; every rebuild rewrites all of it |
| `assets/models/biscuit/qa/geometry/rigged.json` | 17,750,241 | LFS | a QA record, regenerated by every rebuild, read by nothing on the site |
| `assets/models/biscuit/qa/native-samples.json` | 2,525,893 | LFS | the same |
| `static/pose-studio/viewer.html` | 27,561,425 | blob | served by Pages |
| `static/pose-studio/model/biscuit-poseable.glb` | 16,112,380 | blob | linked from the viewer and the model page; served by Pages |
| `static/pose-studio/previews/pose-overview.jpg` | 398,799 | blob | linked from the viewer |
| `assets/models/biscuit/textures/*.png` (36) | 12,209,289 total | blob | the largest is 2,288,330; sources, but small and rarely regenerated |
| `assets/models/biscuit/previews/**` (21) | about 9.1 MB | blob | the native renders and the studio screenshots; `pose-overview.jpg` is the one preview that lives under `static/pose-studio/previews/` instead, because the viewer links it |
| `assets/illustrations/good/*.png` (11) | 14,092,724 total | blob | imported by the gallery page |

Two things §1 fact 4 forces: every CI checkout stays `lfs: false`, and
`scripts/check_assets.py` verifies an LFS-tracked file from its pointer. `git lfs
install` is per machine and `scripts/initialize.sh` runs it (S00); a clone made without
git-lfs sees pointer text where the `.blend` should be, and
`docs/how-to/develop-locally.md` says so.

Costs, stated so they are chosen rather than found: GitHub's free LFS tier is 1 GB of
storage and 1 GB of bandwidth a month at the time of writing (an unverified claim, §10);
the three LFS objects are 32.3 MB, so a clone that fetches them spends 3% of a month's
bandwidth. Every rebuild of the viewer adds 26 MB of ordinary history, accepted while
rebuilds are rare and named in decision 0006; C03 is the exit.

**The viewer's three rewritten hrefs.** D's viewer links `model/biscuit-poseable.blend`
(twice) and `README.md` (once) relative to itself. Neither is served: the `.blend` is LFS
and the README lives under `assets/`. S02 rewrites those three attribute values, and only
those, to
`https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/model/biscuit-poseable.blend`
and `https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/README.md`
(GitHub renders an LFS file's page with a download button). The other four hrefs are kept
and their targets placed beside the viewer, which is why `static/pose-studio/` has a
`model/` and a `previews/` directory, and why `pose-overview.jpg` and the GLB exist in one
place only: under `static/`, never duplicated under `assets/`. The manifest entry for the viewer records D's sha256
as `source_sha256` and the committed bytes' sha256 as `sha256`, with `patched` listing the
three rewrites, so the difference is written down rather than discovered.

**D's README** becomes `assets/models/biscuit/README.md`: the same prose with every
relative link corrected to the studio layout (`../../../static/pose-studio/viewer.html`
and so on), the two `biscuit_pics/generated/3d/…` links turned into code spans naming the
D path and commit, and a leading **Provenance** section that names D `1d9d358`, the date,
the seven-folder rebuild chain the build reads
(`miami-cinematic-eyes-refined` → `miami-cinematic-sweater-foreleg-refined` →
`miami-cinematic-tail-drape-studies` (variant D3) → `ear-profile-studies` → `ear-studies`
→ `cinematic-studies` → `miami-angular-base`, plus the camera frames `viewer.py` reads from
`miami-cinematic-sweater-foreleg-refined/qa/viewer-package.json`), and the sentence that
the chain stays in `biscuit_pics`. It is linted as Markdown and lychee resolves its links
offline; it is outside `docs/`, so the documentation contract does not register it.

## 4. The asset manifest and `scripts/check_assets.py`

`assets/manifest.json` is strict JSON, one object per line inside `assets`, sorted by
`path`, ending in one newline (Prettier ignores it; `check-json` parses it). Every file
under `assets/` and `static/pose-studio/` has an entry, except `assets/manifest.json`
itself. An entry:

```json
{"path": "static/pose-studio/model/biscuit-poseable.glb", "bytes": 16112380, "sha256": "51d16c…", "storage": "blob", "source": "biscuit_pics@1d9d358:models/biscuit/model/biscuit-poseable.glb", "licence": "unsettled"}
```

Fields, all required, in this order: `path` (repository-relative, forward slashes),
`bytes`, `sha256` (of the committed bytes; for an LFS file, the object's, read from the
pointer), `storage` (`blob` or `lfs`), `source` (`<repository>@<commit>:<path>` for an
import, or `rebuilt:<date>` for a regenerated file, or `studio` for one made here), and
`licence` (`unsettled` until §5's open question is answered; the field exists so that
answering it is a diff). Two optional fields, present only where true and always
together: `source_sha256` (64 lowercase hex digits, never equal to `sha256`; when the
committed bytes differ from the source's; for a `rebuilt:` entry the source is the build
output, so it is the digest of the file before any patch the rebuild script applies —
for the viewer, the `sha256` that `viewer.py` records in `qa/viewer-package.json`, which
`write` copies and `check` proves) and `patched` (a non-empty list of non-empty strings
saying what changed).

`scripts/check_assets.py` (S00, final; ruff-clean under §2.4; Pillow is its one import
beyond the standard library; the ledger keys it prints are its interface). Subcommands:

- `check` (what `just check-assets` runs): walk both roots; refuse a file with no entry
  and an entry with no file; for each `blob` entry recompute `bytes` and `sha256` and
  refuse a mismatch; for each `lfs` entry read the pointer (`version
  https://git-lfs.github.com/spec/v1`, `oid sha256:<hex>`, `size <n>`) and refuse a
  mismatch against the entry — and, when the object is present rather than the pointer,
  hash it instead; for every raster image (`.png`, `.apng`, `.jpg`, `.jpeg`, `.jpe`,
  `.jfif`, `.mpo`, `.webp`, `.gif`, `.bmp`, `.avif`, `.heic`, `.heif`) open it with
  Pillow, read `getexif()`, and refuse the file if any IFD0 tag other than `XResolution`
  (`0x011A`), `YResolution` (`0x011B`) and `ResolutionUnit` (`0x0128`) is set, or the
  Exif IFD (`0x8769`) or the GPS IFD (`0x8825`) holds anything, naming every tag found;
  refuse a `.tif` or `.tiff` outright, because a TIFF stores its structure as IFD0 tags,
  and refuse a raster suffix Pillow cannot open as unreadable; assert `storage` agrees
  with `git check-attr
  filter <path>` (`lfs` ↔ `filter: lfs`); refuse `source_sha256` or `patched` present
  without the other, a `source_sha256` that is not 64 lowercase hex digits or equals
  `sha256`, and a `patched` that is not a non-empty list of non-empty strings; and for
  `static/pose-studio/viewer.html`, when `assets/models/biscuit/qa/viewer-package.json`
  is present, refuse a `source_sha256` that differs from that record's `sha256`. Exit 0
  and print one summary line; on any refusal print every finding, one per line as
  `<path>: <reason>`, and exit 1.
- `write` (what `just assets-manifest` runs): recompute every entry from the worktree,
  keeping `source`, `licence`, `source_sha256` and `patched` from the existing entry
  where one exists and writing `source: "studio"`, `licence: "unsettled"` for a new
  file, except that the viewer's `source_sha256` is read from `qa/viewer-package.json`
  whenever that record is present; then run `check` and exit with its status. It never
  deletes a `source` field.
- `self-test`: build a temporary tree with one blob, one hand-written LFS pointer, one
  clean PNG and `tests/fixtures/exif-gps.jpg`; assert `check` passes on the first three
  and refuses the fourth with `GPS`; then, each generated in the temporary tree, assert a
  JPEG carrying only `DateTimeOriginal` and a WebP carrying only `Software` are refused
  with `EXIF`, a PNG carrying only `XResolution` and `YResolution` and a clean WebP pass,
  and a clean TIFF is refused with `TIFF`; then, with a patched viewer and a
  `qa/viewer-package.json` recording the unpatched digest in the temporary tree, assert
  `write` takes `source_sha256` from the record and refuses it until `patched` is
  written, a well-formed pair passes, and a malformed digest, a digest the record does
  not name, an empty `patched` item and a digest equal to `sha256` are each refused;
  assert a tampered byte is refused; exit 0 on success. The `check` subcommand runs `self-test` first, so `just check-assets` proves its
  own checker is live on every run and §2.2's recipe stays one command.

The fixture `tests/fixtures/exif-gps.jpg` is generated once by S00 with Pillow — a 1×1
RGB image saved with an `Exif` block carrying `GPSInfo` (`{1: "N", 2: ((51, 1), (30, 1),
(0, 1))}`) — committed, listed in nothing (it is under `tests/`, not `assets/`), and its
sha256 recorded in S00's hand-back notes.

## 5. Content policy: what is never committed

Owned by `docs/explanation/content-policy.md` (S06); stated here because every lane obeys
it:

- **No photograph of the real dog** without the maintainer's approval of that photograph,
  and none with any metadata left in it. D `biscuit_pics/raw/` (163 files) and its README
  say camera EXIF survives whole in 68 of them. Decision 9 in §1.
- **Nothing from D `inspiration/`**: 110 files of Atlus, Soejima and Studio 4C material
  and fan art, indexed there as "style references only".
- **Neither font under D `biscuit_pics/generated/katherine/dialogue/p5ui/fonts/`**
  (`OptimaNovaLT-Black.ttf`, `KoreanKRSM.ttf`); both are commercial.
- **No file under D `generated/bad/`, `generated/3d/`, `model_sheets/` or `ai_tmp/`**, by
  decision 8. `model_sheets/` may be revisited; its tiles were generated through an
  OpenAI image model and carry the same question as the cel set.
- **The licence of the studio's own assets is an open question**, not resolved by any
  ticket. H `docs/design/character.md` lines 128-134 say `biscuit_pics` licensing "is not
  yet decided"; the manifest's `licence` field is `unsettled` until the maintainer decides,
  and `package.json` is `UNLICENSED` as the hub's is. A ticket that finds it needs an
  answer records the question in its hand-back notes and stops.
- **Generated art is labelled as such.** The eleven files under `good/` were made with
  ChatGPT (D commit `c602c38`, "best mix and match examples. Created using chatgpt.").
  Their manifest `source` says `biscuit_pics@1d9d358:good/<name>` and the gallery page
  says how they were made; C01 is what decides whether they may leave the studio.

## 6. Handbook: every page the studio ships

The contract is H `docs/reference/documentation-contract.md`, enforced by
`bg-validate-docs` (G `validate_docs.py`: six manifest keys, frontmatter equal to the
manifest entry including list order, H1 equal to the title, 40 words, no template
delimiters or `TODO`, relative links resolved with exact case, every page reachable from
`docs/README.md`, nothing unregistered). `docs/manifest.yml` is strict JSON in H's layout
(one entry per line, a blank line between groups) and, with `docs/README.md`, is written by
S00 in final form and touched by no lane.

The page list, owner, kind, audience and topic slug. `H:` means the page is H's of the
same name adapted (Storybook, Chromatic, the package, the specifications and "game"
removed; the studio's own recipes and gates added); `T:` the same from T's rendered page;
`new` is written fresh.

| Page | Owner | Source | Kind | Audience | `canonical_for` |
| --- | --- | --- | --- | --- | --- |
| `README.md` | S00 | H, rewritten | project | user, contributor, maintainer, operator, agent | `documentation_navigation` |
| `project/purpose-and-scope.md` | S05 | new | project | user, contributor, maintainer, agent | `project_purpose`, `project_non_goals` |
| `project/platform.md` | S05 | T: | project | contributor, maintainer, agent | `platform_upstream` |
| `project/repository-map.md` | S05 | H: | project | contributor, maintainer, agent | `repository_layout` |
| `project/terminology.md` | S05 | H: | project | contributor, maintainer, operator, agent | `project_terminology` |
| `tutorials/first-change.md` | S05 | H: | tutorial | contributor, agent | `first_change_tutorial` |
| `how-to/develop-locally.md` | S05 | T: | how-to | contributor, maintainer, agent | `local_development` |
| `how-to/test-and-debug.md` | S05 | T: | how-to | contributor, maintainer, agent | `test_workflow` |
| `how-to/deploy-to-github-pages.md` | S05 | T: | how-to | maintainer, operator, agent | `deployment_procedure` |
| `how-to/maintain-dependencies.md` | S05 | T: | how-to | maintainer, agent | `dependency_maintenance` |
| `how-to/import-an-asset.md` | S05 | new | how-to | contributor, maintainer, agent | `asset_import_procedure` |
| `how-to/rebuild-the-model.md` | S05 | new | how-to | contributor, maintainer, agent | `model_rebuild_procedure` |
| `how-to/promote-an-asset.md` | S05 | new | how-to | maintainer, agent | `asset_promotion` |
| `explanation/architecture.md` | S06 | H: | explanation | contributor, maintainer, operator, agent | `system_architecture` |
| `explanation/large-files.md` | S06 | new | explanation | contributor, maintainer, operator, agent | `large_file_policy` |
| `explanation/content-policy.md` | S06 | new | explanation | user, contributor, maintainer, agent | `content_policy` |
| `explanation/accessibility.md` | S06 | H: | explanation | user, contributor, maintainer, agent | `accessibility_model` |
| `explanation/security-model.md` | S06 | H: | explanation | user, contributor, maintainer, operator, agent | `security_model` |
| `explanation/quality-philosophy.md` | S06 | H: | explanation | contributor, maintainer, agent | `quality_philosophy` |
| `reference/commands.md` | S06 | H: | reference | contributor, maintainer, operator, agent | `command_reference` |
| `reference/configuration.md` | S06 | H: | reference | contributor, maintainer, operator, agent | `configuration_reference` |
| `reference/testing.md` | S06 | H: | reference | contributor, maintainer, agent | `testing_reference` |
| `reference/quality-gates.md` | S06 | H: | reference | contributor, maintainer, agent | `quality_gate_reference` |
| `reference/asset-manifest.md` | S06 | new | reference | contributor, maintainer, agent | `asset_manifest_format` |
| `reference/documentation-contract.md` | S06 | H: | reference | contributor, maintainer, agent | `documentation_contract` |
| `reference/agent-contract.md` | S06 | H: | reference | contributor, maintainer, agent | `agent_contract` |
| `operations/maintenance.md` | S06 | H: | operations | maintainer, operator, agent | `maintenance_routine` |
| `operations/troubleshooting.md` | S06 | H: | operations | contributor, maintainer, operator, agent | `troubleshooting` |
| `operations/hub-handover.md` | S06 | new | operations | maintainer, agent | `hub_handover` |
| `decisions/README.md` | S05 | H: | decision | contributor, maintainer, agent | `decision_index` |
| `decisions/0001-static-site-no-backend.md` | S05 | T: | decision | maintainer, agent | `decision_no_backend` |
| `decisions/0002-the-hub-is-upstream.md` | S05 | T 0008, generalised | decision | contributor, maintainer, agent | `decision_hub_upstream` |
| `decisions/0003-python-toolchain.md` | S05 | T: | decision | maintainer, agent | `decision_python_toolchain` |
| `decisions/0004-a-project-pages-site.md` | S05 | T: | decision | contributor, maintainer, agent | `decision_project_pages_site` |
| `decisions/0005-assembled-by-hand.md` | S05 | new | decision | contributor, maintainer, agent | `decision_assembled_by_hand` |
| `decisions/0006-sources-in-lfs-served-files-as-blobs.md` | S05 | new | decision | contributor, maintainer, operator, agent | `decision_large_file_storage` |
| `decisions/0007-assets-travel-by-copy-and-ledger.md` | S05 | new | decision | contributor, maintainer, agent | `decision_asset_distribution` |
| `decisions/0008-the-viewer-is-embedded-as-is.md` | S05 | new | decision | contributor, maintainer, agent | `decision_viewer_embedded` |
| `decisions/0009-no-component-workshop-yet.md` | S05 | new | decision | contributor, maintainer, agent | `decision_no_workshop` |

Thirty-nine pages. Titles are the H1s: for a `decision` page, `Decision NNNN: <title>` exactly as
H does; for the rest, the natural title (`Import an asset`, `Rebuild the model`,
`Promote an asset`, `Large files`, `Content policy`, `Asset manifest`, `Hub handover`,
`The platform upstream`, and the H/T titles for the rest). S00 writes `docs/manifest.yml`
with these thirty-nine entries in this order, grouped as H groups them, and `docs/README.md` in
H's section order (Start here, How to, Understand, Look up, Run it, Decisions) linking every
non-decision page directly and the decisions through `decisions/README.md`. S00's stubs
carry the frontmatter, the H1 and forty words saying what the page will say; S05 and S06
replace the stubs and touch neither the manifest nor the map. A lane that finds it needs a
page renamed or added hands it back as an S00 follow-up on `main`. A ticket that runs after
every lane (S07, S08, any C ticket) may add a page, and does so through the same route: the
page, its manifest entry and its map link in one change on `main`, with the count above
updated here. C02 is expected to add `explanation/asset-ledger.md` and decision `0010`.

Cross-repository links are `https://github.com/steven-cutting/biscuit_games/blob/main/docs/<path>`
blob URLs to whole pages, never to a fragment, and they live on `project/platform.md`
and nowhere else, as T's page does and H's handover prescribes (H
`docs/operations/poodl-handover.md`, "What a cross-repository link costs"). The
documentation contract skips `https://` links and lychee runs `--offline`; only
`just check-links-online` resolves them, by hand.

## 7. Agent contract

Enforced by `bg-validate-agents` (§1 fact 2). `AGENTS.md` is T's rendered
`template/AGENTS.md.jinja` (173 lines) rewritten for a repository that is not a game,
under 300 words nowhere near a risk. Its shape and what changes:

- **What this project is**: the §0 paragraph, the address, and this sentence: "This
  repository has no `docs/specs/` of its own. How its surfaces look, how they are worked
  and what they owe are the platform's three Allium modules, installed with the package;
  the studio adds no rule of its own and restates none."
- **Invariants**, eight: (1) the hub is the source of truth for shared behaviour, and the
  studio changes the hub first (C01 is the worked example); (2) Svelte 5 runes only, as
  T's; (3) side effects behind a port — the device's preferences through the port the
  package exports, `document` reached in `onMount` in `src/routes/` and nowhere else, and
  every side effect the studio adds gets a port with a fake; (4) exact pins, as T's, plus
  `pillow`; (5) the static build has no server; (6) colour never carries meaning alone; (7)
  coverage does not fall below the floor; (8) **every asset is listed in
  `assets/manifest.json` with its sha256 and its source, `just check-assets` proves it, and
  nothing under `assets/` or `static/pose-studio/` is edited by hand — an import is
  `docs/how-to/import-an-asset.md`, a rebuild is `docs/how-to/rebuild-the-model.md`, and no
  photograph of the real dog is committed without the maintainer's approval of that
  photograph and every metadata field stripped first.**
- **Stack and conventions**: T's, minus stories and Storybook, plus the large-file policy
  and the one exclusion set (§2.1, §3).
- **Change workflow**: T's seven steps, plus: a change that promotes an asset to the hub
  or a game follows `docs/how-to/promote-an-asset.md` and records the item in
  `docs/operations/hub-handover.md`; a change to the viewer or the model records its
  rebuild in the manifest's `source`.
- **Safety and authority**: T's, with "enabling GitHub Pages" kept, and "copying a
  photograph of the real dog" and "editing `biscuit_pics`, the hub or a game" added to the
  class of separately authorised actions.
- **Documentation and durable context**, **External automation policy**: T's verbatim.
- **Provenance**: hand-assembled from H `575e3dd`, P `a2860fc`, T `2283589`, G `v0.3.0`
  and D `1d9d358`; the decisions the studio's own record carries (§6, 0001-0009); the
  deviations from a game (no specs, no workshop, an assets gate, LFS). S08 finalises this
  section; S00 writes it with the same facts and a shorter deviations list.

Eight skills under `.agents/skills/`, each with a `.claude/` and a `.codex/` bridge whose
body is exactly `BRIDGE_BODY` with the name substituted, frontmatter of exactly `name` and
`description` (eight words or more, a real trigger), and a body that cites `AGENTS.md` and
names a `just` recipe:

| Skill | Source | Edits |
| --- | --- | --- |
| `accessibility-review` | H | drop steps 3 (contrast test) and 8 (axe in the story run); step 9 names `just frontend-static` and `just check`; add a step for the viewer: auto-rotation stops when `data-animations` is absent, the canvas page follows the platform's `data-theme`, pinch-zoom is never blocked |
| `code-review` | H | step 2 names the studio's eight invariants; step 5 names the `onMount` exception; step 8 becomes "a fact about the platform belongs in the hub; a change that moves an asset out runs `hub-handover`" |
| `fix-quality` | H | dispatch list gains `check-assets` ("a file under `assets/` or `static/pose-studio/` changed without `just assets-manifest`, or an image carries EXIF; never edit the manifest by hand to make it agree") and loses `check-specs` |
| `plan-change` | H | step 4 becomes "if the change moves a platform rule, the hub changes first (C01's shape); if it moves an asset out, plan the `hub-handover` entry" |
| `project-check` | H | step 2 drops the allium binary and names `git lfs install`; the gate list is §2.4's |
| `review-docs` | H | verbatim |
| `asset-change` | new | import or rebuild an asset: the two how-to pages, `just assets-manifest`, read the diff, `just check-assets`, the EXIF and approval rules, LFS patterns, the `source` field |
| `hub-handover` | new | when an asset is ready to leave: `docs/how-to/promote-an-asset.md`, the interim copy procedure, write the item into `docs/operations/hub-handover.md` in that page's own register, never edit the other repository |

`CLAUDE.md` is exactly `@AGENTS.md` and one newline. `.github/copilot-instructions.md` is
H's three lines byte for byte. `.claude/settings.json` is H's (it enables the allium
plugin, which the studio never uses; kept because it is the one file the validator
tolerates and removing it changes nothing).

## 8. CI and Pages

Three required checks on `main`: `frontend`, `documents`, `assets`. Each job in
`.github/workflows/ci.yml` (S04) is H's inline shape (H `.github/workflows/ci.yml`
lines 19-43) with the five toolchain steps replaced by one:

```yaml
      - uses: steven-cutting/biscuit_games_tooling/actions/setup-toolchain@6c5c07f6bec86e86b3930dfa41392e4b440e8c85 # v0.3.0
```

and `just sync` carrying `NODE_AUTH_TOKEN: ${{ github.token }}` on that step alone, as G
`game-ci.yml` does. Workflow `permissions`: `contents: read`, `packages: read`.
`frontend`: sync, lock-check, frontend-static, frontend-coverage, frontend-build.
`documents`: sync, lint, check-docs, check-agents. `assets`: checkout with `lfs: false`
stated explicitly (it is the default, and the comment says the pointer is what the checker
reads), sync, check-assets. No job carries a `paths` filter or a `name:`: a skipped
required check blocks the merge, and the job id is the check's name (T C03).

`.github/workflows/pages.yml` (S04) is T `template/.github/workflows/pages.yml` (39 lines)
with one deviation: it runs on `workflow_run` after `CI` completes, not on push, and its job
deploys only when that run succeeded for a push to `main` whose `head_sha` is still
`github.sha`, because protection does not bind administrators and a direct push would
otherwise publish unchecked (S04 hand-back). It calls G `game-pages.yml` at `6c5c07f…` with
`base_path: /${{ github.event.repository.name }}`, which is `/biscuit_studio`. No `stage`,
`artifact_path` default `build`. The build job checks out with `lfs: false`, which is
correct: nothing under `static/` is LFS.

Repository settings no file carries — Pages source `workflow`, protection on `main`
requiring the three checks, private vulnerability reporting — are applied by
`scripts/bootstrap_repo.sh steven-cutting/biscuit_studio --checks frontend,documents,assets`
(T's script, copied verbatim; its `--checks` default names a game's `ci / …` contexts,
which is why the option is passed). S07 runs it, dry then `--apply`, each `--apply`
separately authorised.

## 9. Rules for tickets and lanes

- **Worktrees and branches.** Each ticket is executed on the branch its `branch:` field
  names (`ticket/s02-asset-import`) in its own worktree, created from `main` after every
  ticket it depends on has merged. From a Supacode terminal:
  `supacode repo worktree-new --branch <branch> --base main --name <id>`; otherwise
  `git worktree add ../<id> -b <branch> main`. A ticket touches only its listed files plus
  the `status:` line of its own `tickets/<id>-*.md`.
- **S00 ships a shape-complete skeleton.** `just check` can only be green if every path
  §2 names exists from the first commit: every registered page with valid frontmatter, a
  matching H1 and forty words; `AGENTS.md` with the six phrases and 300 words; all eight
  skills and sixteen bridges; a placeholder route; an empty manifest that `check-assets`
  passes. Lanes **replace** stubs.
- **Files no lane touches:** `docs/manifest.yml`, `docs/README.md`, `Justfile`,
  `pyproject.toml`, `package.json`, `.gitattributes`, `.pre-commit-config.yaml`,
  `.pre-commit-fix.yaml`, `scripts/check_assets.py`. A lane that needs a change there
  stops and hands it back as an S00 follow-up on `main`. (The lockfiles change whenever
  `package.json` or `pyproject.toml` do, so they are in the same class.) The rule is about
  lanes running side by side: S07, S08 and the C tickets run after every lane has merged and
  may edit any of these files they list, C03's `package.json` dependency being the worked
  example.
- **No path appears in two lanes' Files-touched lists.** The lanes are S01 to S06; the
  tickets were checked against each other; an agent that finds a need to edit another
  lane's file hands it back instead. S07 and S08 run after every lane and may touch what
  they list.
- **A done ticket is not reopened.** Once a ticket's `status:` is `done`, or once an
  agent has started executing it, no other ticket edits its file or reopens it to change
  the work it delivered; the executing agent still writes its own hand-back notes and
  `status:` line, as §9 above allows. A hand-back addressed to such a ticket, a correction to one of its
  passages, and a defect found in its work after it is done all go into a follow-up
  ticket: the next free `S` id, which cites each item by its source ticket and hand-back
  bullet, lists the files it touches like any other ticket, and depends on the tickets
  whose work it changes. A follow-up that nothing has started yet absorbs new items in
  place; one that has started gets a follow-up of its own. A ticket nobody has started
  may be amended in place instead, and the commit that amends it says which hand-back
  it carries. S09 is the first follow-up, holding what S00 to S06 handed back.
- **Self-contained.** A ticket is written for an agent with no context: it embeds exact
  content or cites this document by section, and names the H, P, T, G and D paths to read.
  It never cites a chat transcript, a scratch directory or a tool result.
- **Paths as code spans.** Ticket text writes repository paths as code spans, never as
  relative Markdown links: S00's hook gate runs lychee offline over `tickets/`, and a link
  to a file that does not exist yet fails it.
- **Definition of done**, for every build ticket: `just check` green in this repository,
  the ticket's own acceptance criteria met, the verification commands run with their
  output quoted in the hand-back notes, and the ticket's `status:` set to `done` in the
  same pull request.
- **Separately authorised actions.** Commits on the ticket branch are the ticket's work.
  Pushing, opening a pull request, creating the GitHub repository, changing a repository
  setting, enabling Pages, tagging, filing issues, editing another repository (H, P, T, G,
  D or a game) and copying any photograph of the real dog are each a separately authorised
  action: the ticket says where one occurs, and the agent stops and asks the maintainer
  rather than proceeding. Nothing under `tickets/` has been filed as a GitHub issue.
- **D is read-only.** Every ticket that reads D does so with `cp`, `shasum` and `git
  show`; nothing writes there, and nothing runs D's scripts from inside D.
- **Credentials.** The GitHub Packages token lives only in `~/.npmrc` on the developer's
  machine and in `github.token` in CI. No file in this repository carries a token, and
  documentation writes `<your token>` after `_authToken=` because ripsecrets flags a bare
  word there.

## 10. Unverified claims, and the ticket that checks each

Each claim below was reasoned from source but not executed. The named ticket runs the check
and records the outcome in its hand-back notes; a claim that fails is a design change that
goes back through this document.

- `pillow==12.3.0` resolves under `uv lock` for Python 3.14 beside the tooling package,
  and `Image.getexif()` exposes the GPS IFD through `get_ifd(0x8825)` without an extra
  dependency. `len(getexif())` is zero for every clean PNG, JPEG, WebP, GIF, BMP and AVIF
  Pillow writes, but a clean TIFF holds ten structural tags, which is why §4 refuses TIFF
  outright; Pillow's PNG writer drops an `Exif` whose IFD0 is empty, so the sub-IFD case
  in the self-test is a JPEG. **S00.**
- The prek `exclude` regex alone keeps editorconfig-checker, typos, lychee and
  `check-added-large-files` off the assets, so the `.editorconfig` sections and the typos
  entry are belts rather than the thing holding. **S00** (with the stub manifest) and
  **S02** (with the real files: `just lint` must pass with a 26 MB file in the tree).
- `vitest --coverage` with thresholds passes on a `src/lib/` holding only `brand.ts`,
  which `tests/brand.test.ts` imports. **S00.**
- `svelte-check --fail-on-warnings` and `vite build` tolerate a 26 MB file under
  `static/`, and `adapter-static` copies it into `build/` unchanged, sha256 preserved.
  **S03.**
- `@sveltejs/kit` accepts a route directory (`src/routes/model/`) and a static directory
  (`static/pose-studio/`) that do not collide; the two names were chosen apart on purpose.
  **S03.**
- The prerender crawler (`strict: true`) treats an `<a href>` into `static/` as an asset
  rather than a route it must render, and the client router leaves an anchor carrying
  `rel="external"` and `data-sveltekit-reload` alone, so a click on the viewer or the GLB
  leaves the app rather than becoming a 404 inside the shell. Both attributes are written
  regardless; the claim is what happens without them. **S03.**
- `actions/upload-pages-artifact` and `deploy-pages` accept an artefact holding a 26 MB
  file and a 16 MB file, and the deployed site serves both with `200` and the recorded
  sha256. **S07.**
- `actions/checkout` with `lfs: false` (the default) checks out the pointer text, and
  `git check-attr filter` inside the job reports `lfs` for the three patterns. **S04**
  writes it, **S07** proves it on the first run.
- GitHub's free LFS tier is 1 GB storage and 1 GB bandwidth a month. **S02** reads the
  current figure from GitHub's documentation and writes it into
  `docs/explanation/large-files.md`'s owner's hand-back (S06 carries it onto the page).
- `git lfs push --all origin main` after `gh repo create --push` uploads the three
  objects, and a fresh `git clone` (with git-lfs installed) receives real files. **S07.**
- `gh repo create steven-cutting/biscuit_studio --public --source . --remote origin
  --push` accepts an existing local repository with commits. **S07.**
- `github.event.repository.name` is `biscuit_studio` (underscore preserved) on `push` and
  `workflow_dispatch`, so `BASE_PATH` is `/biscuit_studio`. **S07.**
- A Vite import of a PNG from outside `src/` but inside the repository root
  (`import src from '../../../assets/illustrations/good/warm-head.png'`) resolves in
  build, dev and jsdom without `server.fs.allow`. **S03.**
- `document.title` is reflected by a `<svelte:head><title>` under jsdom (T CONVENTIONS
  §12 recorded the same claim for a game; drop the case rather than weaken it if it
  proves flaky). **S01.**
- `scripts/bootstrap_repo.sh` accepts `--checks frontend,documents,assets` (names without
  spaces) and writes them as the required contexts. **S07.**

## 11. Risks every ticket states where it applies

- **A 26 MB file in ordinary history.** Every viewer rebuild adds it again. Accepted while
  rebuilds are rare; C03 retires the file. `docs/explanation/large-files.md` and decision
  0006 say so.
- **The hub's rule stands until C01 lands.** Nothing the studio renders is promoted before
  then, and a ticket that needs to promote something waits.
- **The hook gate's first run needs the network** (prek clones every hook on the first
  `lint`), and `npm ci` needs the registry token. An offline first run fails at `sync` or
  `lint` for no studio reason.
- **The GLB's look is not the viewer's.** D's README says the GLB carries standard PBR
  materials while the viewer and Blender carry the approved cel shading. The model page
  says so beside the download link; C03 has to reproduce the cel look in three.js.
- **Same-hunk appends conflict inline** in `docs/manifest.yml`, `docs/README.md` and
  `AGENTS.md`. Lanes do not touch the first two; S08 is the only ticket after S00 that
  edits the third.
- **`check-assets` is only as honest as the manifest.** `just assets-manifest` rewrites
  hashes from the worktree, so a tampered asset plus a rewritten manifest passes. The
  guard is review: the diff of the manifest is read on every import, and `source` is never
  rewritten by the tool.
- **The rebuild reaches outside the repository.** D `models/biscuit/src/common.py` line 10
  and `viewer.py` line 6 resolve the repository root as the package's second parent, which
  in the studio is `assets/`; `scripts/rebuild_model.sh` therefore places a gitignored
  symlink `assets/biscuit_pics` at the checkout it is given and removes it afterwards. A
  rebuild interrupted half-way leaves the link; `.gitignore` keeps it out of the index.
- **`git lfs install` is per machine.** A contributor without it commits a real `.blend`
  as a blob. `scripts/initialize.sh` runs it; `check-assets`'s `git check-attr` comparison
  reports `storage` drift, but only after the object is already in the index.
- **Pages serves a stale pointer if a served path ever moves into LFS.** The
  `.gitattributes` patterns name sources by path; a rename that puts a served file under
  `assets/models/biscuit/qa/geometry/` would silently break the site.
- **The gallery page is heavy** (eleven PNG files, 14 MB). Accepted for the first release;
  thumbnails are an open point on S03.
- **The three rewritten hrefs point at `main`.** A branch rename or a path move under
  `assets/models/biscuit/` breaks two links inside a file no linter reads. The manifest's
  `patched` field is where the three are written down.
- **Nothing here checks a cross-repository link.** `project/platform.md`'s blob URLs rot
  silently; `just check-links-online` is monthly and by hand.
