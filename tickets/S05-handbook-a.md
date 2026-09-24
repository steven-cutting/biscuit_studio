---
id: S05
title: "Handbook A: project, tutorial and how-to pages, and the decision records"
status: done
depends_on: [S00]
parallel_with: [S01, S02, S03, S04, S06]
branch: ticket/s05-handbook-a
estimated_size: L
---

# S05: Handbook A: project, tutorial and how-to pages, and the decision records

## Context

S00 shipped every handbook page `CONVENTIONS.md` §6 lists as a stub: the exact frontmatter,
an H1 equal to the manifest title, and forty words saying what the page will say. The
manifest (`docs/manifest.yml`) and the map (`docs/README.md`) are final and no lane touches
them (CONVENTIONS.md §9). This ticket replaces the stub bodies of the twenty-two pages under
`docs/project/`, `docs/tutorials/`, `docs/how-to/` and `docs/decisions/`. S06 replaces the
other sixteen in the same shape; the two lanes share no path.

Every page is held to the documentation contract the tooling package enforces (H
`/Users/scutting/projects/biscuit_games/docs/reference/documentation-contract.md`, and G
`/Users/scutting/projects/biscuit_games_tooling/src/biscuit_games_tooling/validate_docs.py`):
the first heading is level one and equals the title; at least forty words; no template
delimiter (`validate_docs.py` line 34 rejects the three two-character openers, and the third
is a brace followed by a hash, so prose never writes "each block" with the Svelte spelling
— write the words instead); no `TODO`, `TBD` or `FIXME` marker; every relative link resolves
with exact case and every fragment names a real heading; every page reachable from
`docs/README.md`. Reachability is S00's doing — the map already links every page — so this
ticket cannot break it by adding prose, only by deleting the H1. On top of the contract,
markdownlint (H `.markdownlint-cli2.jsonc`), `typos` and lychee `--offline` run over the
pages in `just check-docs`.

Sources, at the commits CONVENTIONS.md §0 pins, read-only:

- H = `/Users/scutting/projects/biscuit_games` at `575e3dd`. The pages this ticket adapts:
  `docs/project/purpose-and-scope.md` (89 lines; sections "What it does" 24-52, "What it
  deliberately does not do" 53-76, "Who it is for" 77-83), `docs/project/repository-map.md`
  (107 lines; the tree 11-59, "What each part is responsible for" 60-81, "What is not here"
  82-101), `docs/project/terminology.md` (47 lines; "The platform" 16-29, "The repository"
  30-42), `docs/tutorials/first-change.md` (149 lines; seven numbered sections 16-136,
  "What you just touched" 137-143), `docs/decisions/README.md` (78 lines; "The record"
  23-43, "The numbering" 45-51, "Writing a new one" 53-72),
  `docs/decisions/0013-shared-material-travels-as-a-package.md` (the shape every record
  takes: Context, Decision, Consequences, What would reopen this, Related pages),
  `docs/design/character.md` lines 20-21, 91, 106-110 and 128-134, and
  `docs/design/direction.md` lines 262-263.
- T = `/Users/scutting/projects/biscuit_games_template/template` at `2283589`. The pages
  this ticket adapts: `docs/project/platform.md` (104 lines),
  `docs/how-to/develop-locally.md` (112 lines; "Prerequisites" 11-24, "First run" 25-53,
  "Every day" 54-88, "Before handing work back" 89-98, "Keeping the workspace current"
  99-106), `docs/how-to/test-and-debug.md` (75 lines; "Run the suites" 11-29, "Narrow down
  a failing test" 30-41, "Debug a coverage failure" 42-53, "Debug a browser problem"
  54-69), `docs/how-to/maintain-dependencies.md` (184 lines; "Check that the lockfiles
  still match" 20-28, "Update deliberately" 29-39, "Upgrading a package" 40-59, "Moving
  the design system package" 60-90, "Moving the tooling package" 91-115, "Moving the
  Allium binary" 116-150, "Take a template update" 151-157, "Actions in the workflows"
  158-179), `docs/how-to/deploy-to-github-pages.md.jinja` (91 lines),
  `docs/decisions/0001-static-site-no-backend.md` (53 lines),
  `docs/decisions/0004-python-toolchain.md` (61 lines),
  `docs/decisions/0008-design-system-as-a-package.md` (81 lines) and
  `docs/decisions/0010-a-project-pages-site.md.jinja` (68 lines).
- D = `/Users/scutting/.supacode/repos/biscuit_pics/very_nice_three_deeez` at `1d9d358`:
  `models/biscuit/README.md` (78 lines; "Provenance" 11-15, "Pose her in Blender" 27-40,
  "Portable model and saved poses" 42-53, "Rebuild and verification" 61-78), the source
  the rebuild and import pages describe.

Read first: CONVENTIONS.md §1 (every decision and fact), §2 (the tree), §3 (large files
and the viewer's three rewritten hrefs), §4 (the manifest), §5 (content policy), §6 (the
page table with the exact title, kind, audience and slug of every page here), §8 (CI and
Pages), §9, §10 and §11. Then the S00 ticket's hand-back notes, because S00 wrote the
stubs, the `Justfile` and `scripts/check_assets.py` that several pages describe.

## Goal

At the end of this ticket, on branch `ticket/s05-handbook-a`, the twenty-two pages below
carry their real prose, each satisfying the contract; `just check-docs` and `just check`
are green; no file outside the list changed.

## Non-goals

- `docs/manifest.yml`, `docs/README.md`, any frontmatter, any title. Frozen by S00.
- The sixteen pages S06 owns (`docs/explanation/`, `docs/reference/`,
  `docs/operations/`). Where a page here has to point at one of those, it links to the
  page by its path — the stub exists, so the link resolves — and says nothing the owning
  page decides.
- Root `README.md`, `CHANGELOG.md`, `AGENTS.md`: S08.
- Any code, recipe, workflow, asset or manifest change. A fact a page needs that the
  repository does not yet make true is written as the design says it (CONVENTIONS.md) and
  named in the hand-back notes for the ticket that makes it true.
- Cross-repository links anywhere but `docs/project/platform.md` (CONVENTIONS.md §6, last
  paragraph). Every other page names a hub page in prose or links to `project/platform.md`.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `docs/project/purpose-and-scope.md` | page | new; H `docs/project/purpose-and-scope.md` for shape | replace stub body |
| `docs/project/platform.md` | page | T `docs/project/platform.md` | replace stub body (step 3) |
| `docs/project/repository-map.md` | page | H `docs/project/repository-map.md` | replace stub body |
| `docs/project/terminology.md` | page | H `docs/project/terminology.md` | replace stub body |
| `docs/tutorials/first-change.md` | page | H `docs/tutorials/first-change.md` | replace stub body |
| `docs/how-to/develop-locally.md` | page | T `docs/how-to/develop-locally.md` | replace stub body |
| `docs/how-to/test-and-debug.md` | page | T `docs/how-to/test-and-debug.md` | replace stub body |
| `docs/how-to/deploy-to-github-pages.md` | page | T `docs/how-to/deploy-to-github-pages.md.jinja` | replace stub body |
| `docs/how-to/maintain-dependencies.md` | page | T `docs/how-to/maintain-dependencies.md` | replace stub body |
| `docs/how-to/import-an-asset.md` | page | new | replace stub body (step 5) |
| `docs/how-to/rebuild-the-model.md` | page | new; D `models/biscuit/README.md` 61-78 | replace stub body (step 5) |
| `docs/how-to/promote-an-asset.md` | page | new | replace stub body (step 5) |
| `docs/decisions/README.md` | page | H `docs/decisions/README.md` | replace stub body (step 6) |
| `docs/decisions/0001-static-site-no-backend.md` | page | T `docs/decisions/0001-static-site-no-backend.md` | replace stub body |
| `docs/decisions/0002-the-hub-is-upstream.md` | page | T `docs/decisions/0008-design-system-as-a-package.md`, generalised | replace stub body |
| `docs/decisions/0003-python-toolchain.md` | page | T `docs/decisions/0004-python-toolchain.md` | replace stub body |
| `docs/decisions/0004-a-project-pages-site.md` | page | T `docs/decisions/0010-a-project-pages-site.md.jinja` | replace stub body |
| `docs/decisions/0005-assembled-by-hand.md` | page | new | replace stub body (step 7) |
| `docs/decisions/0006-sources-in-lfs-served-files-as-blobs.md` | page | new | replace stub body (step 7) |
| `docs/decisions/0007-assets-travel-by-copy-and-ledger.md` | page | new | replace stub body (step 7) |
| `docs/decisions/0008-the-viewer-is-embedded-as-is.md` | page | new | replace stub body (step 7) |
| `docs/decisions/0009-no-component-workshop-yet.md` | page | new | replace stub body (step 7) |

The table is the whole scope. Nothing outside it is edited except the `status:` line of
this ticket.

## Steps

Work from the repository root on branch `ticket/s05-handbook-a`. Every page keeps S00's
frontmatter and H1 byte for byte; only the body below the H1 changes. Run
`uv run --frozen bg-validate-docs` after every few pages rather than at the end, because it
reports every violation at once and a stale link is cheaper to find early.

### Step 1: The rules every page obeys

Before writing, read the contract page and `validate_docs.py` lines 20-40 (`KINDS`,
`AUDIENCES`, `MINIMUM_WORDS`, `LINK`, `BAD_CONTENT`). Then, on every page:

- Forty words is a floor, not a target; a page that only meets it says nothing.
- Say "this repository" or "the studio", never "this game"; the studio is not a game and
  CONVENTIONS.md §1 decision 2 is why.
- Relative links only, to pages that exist (every registered page has a stub) and to
  `../../src/...`-style code paths only where H's page does the same; a path that is
  mentioned rather than followed is a code span.
- The hub is cited by page name in prose ("the hub's design direction page") or by a link
  to `platform.md`, never by URL. Only `docs/project/platform.md` carries `https://` links,
  and each of those is a whole-page GitHub blob URL.
- Prose that describes a Svelte block writes the words ("an each block", "an if block");
  the two-character opener the block uses is a template delimiter to the validator.
- Name the risks CONVENTIONS.md §11 assigns to a page's subject, where the page owns that
  subject: the 26 MB history cost and the GLB's PBR look (rebuild page), the hub rule
  standing until C01 (promote page and `platform.md`), the network on a first run
  (develop-locally), `git lfs install` being per machine (develop-locally and import page),
  the manifest being as honest as its review (import page), the three rewritten hrefs
  pointing at `main` (rebuild page), and a Pages pointer if a served path moves into LFS
  (deploy page).

### Step 2: The project pages

`docs/project/purpose-and-scope.md`. H's page is the shape (three sections and Related
pages); the content is the studio's. **What it does**: the repository where Biscuit's
graphical assets are developed and kept — the approved poseable model (`.blend`, GLB, the
rig, the poses, the textures, the QA record), the renders and exports made from it, and the
2D illustrations — and a static site on GitHub Pages at
`https://steven-cutting.github.io/biscuit_studio/` (written as a code span, not a link) that
shows them on the platform's design system. It consumes `@steven-cutting/biscuit-games`
exactly as a game does, and it publishes nothing a game installs. **What it deliberately
does not do**: it does not decide the character, the aesthetic or a token (the hub's
`character.md` and `direction.md` do, and a change goes there first — CONVENTIONS.md §1
decision 1, C01); it does not hold the rebuild chain, the raw photographs or the reference
art (§1 decision 8, §5); it ships no game, no component and no package; it runs Blender
nowhere in CI; it holds no photograph of the real dog without the maintainer's approval of
that photograph and every metadata field stripped (§1 decision 9). **Who it is for**: the
maintainer, an agent working here, and a game or the hub wanting an asset — which they get
by the procedure on `how-to/promote-an-asset.md`. Related pages: `what the hub owns` is
reached through `platform.md`; link `platform.md`, `repository-map.md`,
`../explanation/content-policy.md`, `../decisions/README.md`.

`docs/project/repository-map.md`. H's page with its tree (lines 11-59) replaced by
CONVENTIONS.md §2's tree as it will stand after every lane merges (without the owner and
source columns — a reader of the handbook does not know the tickets), grouped as H groups
its own: root files, `src/`, `assets/` (with `manifest.json` first, then `models/biscuit/`
and `illustrations/good/`), `static/pose-studio/`, `tests/`, `docs/`, `scripts/`, the
three agent-contract directories, `.github/`. **What each part is responsible for**: H's
paragraphs for `src/`, `tests/`, `docs/`, `scripts/` and the agent surface, rewritten for
the studio (no `stories/`, no `dist/`, no `docs/specs/`), plus new paragraphs for `assets/`
(sources, never served; listed in the manifest; the model's own Blender scripts under
`assets/models/biscuit/src/` are excluded from every linter by the one exclusion set §2.1
names) and `static/pose-studio/` (what the site serves byte for byte: the viewer, the GLB
and the overview image, beside each other because the viewer links them relatively — §3).
**What is not here**: the rebuild chain, the raw photographs, the reference art, the model
sheets and the discarded Chrome profile, each named with its D path as a code span and the
reason from §1 decision 8; and a component workshop, with a link to
`../decisions/0009-no-component-workshop-yet.md`.

`docs/project/terminology.md`. H's two sections. **The platform**: keep H's entries that
still apply (the hub, the package, a game, the design system, a token, the four
combinations, the specifications — noting the studio restates none), and add: *the
studio* (this repository), *the approved model* (what `assets/models/biscuit/` holds and
only the maintainer replaces), *the viewer* or *pose studio* (the served
`static/pose-studio/viewer.html`), *the manifest* (`assets/manifest.json`), *a source*
(an asset the site never serves; LFS when large) and *a served file*. **The repository**:
H's entries for the gate, a recipe, a lane, a port and a fake, plus *an import*, *a
rebuild* and *a promotion*, each pointing at its how-to page.

### Step 3: `docs/project/platform.md`

T's page with these changes and no others:

- "This game" → "This repository", "the game" → "the studio", throughout. The opening
  sentence becomes: "This repository is the platform's studio, and the platform is a
  repository of its own".
- Section "What is decided there, and what is this game's" → keep the heading text with
  "this game's" → "the studio's"; the second paragraph lists what the studio decides: which
  assets exist, how they are made and rebuilt, how they are stored, and which one is the
  approved model. Add the sentence: "The studio waits on a hub decision permitting renders
  from the model; until it lands nothing here is promoted."
- Section "What is installed": T's, with "which is where the specifications
  `tests/platformSpecs.test.ts` reads actually live" replaced by "readable under
  `node_modules/@steven-cutting/biscuit-games/`".
- Section "What holds the two together": replace T's paragraph on restatement with two
  sentences: the studio restates no clause and runs no Allium checker, because it adds no
  rule of its own; every platform figure it wears arrives as the stylesheet and the
  components, so a change there arrives as a version bump `just check` can see. Keep T's
  last sentence.
- The table: keep every T row whose target still exists in H at `575e3dd` (all of them do;
  check with `ls` on H), drop the "Their decision 0015" and "Their decision 0016" rows
  (play surfaces are nothing to the studio), and add two rows: "Design direction" already
  exists — append to its description "; its Avoid list is what C01 changes"; and add
  "Poodl handover" is already there — keep. Add a row for the hub's
  `docs/how-to/consume-the-hub.md` if T lacks it (it has one; keep it).
- Section "What nothing here checks": T's verbatim.
- Related pages: `../decisions/0002-the-hub-is-upstream.md`,
  `../how-to/maintain-dependencies.md`, `../operations/hub-handover.md`,
  `../reference/quality-gates.md`.

Every `https://` link on this page is a whole-page blob URL under
`https://github.com/steven-cutting/biscuit_games/blob/main/docs/`. No fragment.

### Step 4: The tutorial and the four adapted how-to pages

`docs/tutorials/first-change.md`. H's seven steps, with these changes: step 1 is
`just initialize` then `just check`, and names the `~/.npmrc` token line as
`develop-locally.md` does; step 2 "See the site" stays (`just dev`, the three routes);
step 3 "Read what decides the behaviour" becomes "Read what decides the look": the hub's
pages through `../project/platform.md`, and the studio's `src/lib/appearance.ts` as the one
place the device is consulted (CONVENTIONS.md §2.7); step 4 adds a case to
`tests/appearance.test.ts` (a device that asks for more contrast); step 5, H's "Add a
story state", is replaced by "Add an asset the honest way": copy a small PNG into
`assets/illustrations/`, run `just check-assets` and watch it refuse the unlisted file, run
`just assets-manifest`, read the diff, run `just check-assets` again — then delete the file
and restore the manifest, because the tutorial adds nothing; step 6 `just check`; step 7
commit. "What you just touched" lists the studio's layers.

`docs/how-to/develop-locally.md`. T's page with: **Prerequisites** gaining `git-lfs`
("installed and `git lfs install` run once per machine; `scripts/initialize.sh` runs it,
and a clone made without it holds pointer text where `assets/models/biscuit/model/biscuit-poseable.blend`
should be") and a `~/.npmrc` line written as `//npm.pkg.github.com/:_authToken=<your token>`
(T lines 11-24 already carry it; keep that form exactly, because ripsecrets flags a bare
word there — CONVENTIONS.md §9). **First run**: T lines 25-53 minus the Chromium sentence
(line 50) and the allium sentence; say what `just initialize` does here: both locks, both
installs, `git lfs install`, formatting, hooks from the primary checkout only. **Every
day**: T lines 54-88 minus `just storybook` (line 68) and its paragraph; add the three
routes and `BASE_PATH= just preview` for a build. **Before handing work back** and
**Keeping the workspace current**: T's. Name the first-run network risk (§11).

`docs/how-to/test-and-debug.md`. T's page with: **Run the suites** listing
`just frontend-unit`, `just frontend-coverage`, `just frontend-watch <path>` and
`just check-assets` (no `storybook-test`, line 17); **Narrow down a failing test**: T's,
with lines 38-40 (the specification is the arbiter) replaced by "the hub's page that owns
the behaviour is the arbiter; see `../project/platform.md`"; **Debug a coverage failure**:
T's, naming `src/lib/brand.ts`, `src/lib/appearance.ts` and
`src/lib/components/Lockup.svelte` as the whole measured surface (CONVENTIONS.md §1 fact
7) and `src/routes/` as outside it; **Debug a browser problem**: T's, plus a paragraph on
the viewer: it is a static file, `just dev` serves it at `/pose-studio/viewer.html`, it
needs WebGL 2, and a problem inside it is debugged against D's `models/biscuit/src/`
sources named on `rebuild-the-model.md`, not against anything under `src/`.

`docs/how-to/deploy-to-github-pages.md`. T's page rendered for this repository:
`{{ pages_url }}` → `https://steven-cutting.github.io/biscuit_studio/` (as a code span, not
a link, because lychee runs offline and the site does not exist until S07),
`{{ repository }}` → `steven-cutting/biscuit_studio`, `{{ base_path }}` → `/biscuit_studio`.
**One-time setup** keeps step 1 (the Pages source), drops step 2 (the package is public,
no grant is needed — T `tickets/C03-repository-bootstrap.md` "Deviations"), and says the
repository's own `scripts/bootstrap_repo.sh steven-cutting/biscuit_studio --checks frontend,documents,assets`
applies step 1 with `gh` together with branch protection and vulnerability reporting
(CONVENTIONS.md §8), each `--apply` an authorised action. Drop lines 40-43's `404 Not Found`
paragraph (the grant); keep the `Failed to create deployment (status: 404)` sentence.
**What the workflow does**: T's, plus: the build checks out with `lfs: false`, which is
correct because nothing under `static/` is LFS, and the risk that a served path moved into
LFS would deploy pointer text (§11). **Reproduce a deployment locally**: T's with
`BASE_PATH=/biscuit_studio`. Add a paragraph **What the site serves**: the three routes,
`pose-studio/viewer.html`, `pose-studio/model/biscuit-poseable.glb` and
`pose-studio/previews/pose-overview.jpg`, each beneath `/biscuit_studio/`. Related pages:
`../decisions/0004-a-project-pages-site.md`, `../explanation/architecture.md`,
`../reference/configuration.md`, `../operations/maintenance.md`.

`docs/how-to/maintain-dependencies.md`. T's page with: lines 56 (Playwright), 85
(Chromatic), 116-150 ("Moving the Allium binary") and 151-157 ("Take a template update")
dropped; "Moving the design system package" (60-90) kept minus the
`tests/platformSpecs.test.ts` paragraph (80), replaced by "the studio restates nothing, so
a bump is read in the package's `CHANGELOG.md` and proved by `just check`"; "Moving the
tooling package" (91-115) kept, with `just install-allium` and the specification sentences
(108, 111) dropped and the pin named as `@v0.3.0`; a new short section **Moving Pillow**:
`pillow` is a dev dependency for `scripts/check_assets.py` alone, pinned exactly, moved
like any Python pin, and `just check-assets` (whose `self-test` opens the EXIF fixture) is
the proof; "Actions in the workflows" kept, naming G's `setup-toolchain` composite action
and `game-pages.yml`, both pinned by SHA with the tag in a comment, and that moving one is
a two-file change (`ci.yml` and `pages.yml`).

### Step 5: The three new how-to pages

`docs/how-to/import-an-asset.md` — title `Import an asset`. Sections:

1. **Before anything**: the content policy (`../explanation/content-policy.md`): nothing
   from `inspiration/`, no raw photograph without the maintainer's approval of that
   photograph and every metadata field stripped, no commercial font, and the licence of the
   studio's own assets is unsettled (CONVENTIONS.md §5). Copying a photograph is a
   separately authorised action.
2. **Where it goes**: a source under `assets/` (`assets/models/<name>/` or
   `assets/illustrations/<set>/`); a file the site serves under `static/pose-studio/` or a
   route that imports it. The large-file policy (`../explanation/large-files.md`) decides
   LFS: a source over a few megabytes that a rebuild rewrites goes through LFS by a
   pattern in `.gitattributes`; anything served never does. Changing `.gitattributes` is
   not a lane's to do alone — say it is a change to the policy page and the file together.
3. **The procedure**: copy with `cp` from a read-only source; record the source commit
   (`git -C <source> rev-parse HEAD`); `git lfs track` is never run by hand — the patterns
   are already in `.gitattributes`, and `git check-attr filter <path>` shows which applies;
   `just check-assets` refuses the unlisted file (quote the line shape `<path>: not in
   assets/manifest.json`); `just assets-manifest` writes the entry with `source: "studio"`
   and `licence: "unsettled"`; edit the entry's `source` to
   `<repository>@<commit>:<path>`; read the whole manifest diff; `just check-assets`;
   `just check`. State that the tool never rewrites `source`, so a wrong one is a wrong one
   until a person fixes it (§11).
4. **What the checker refuses**: the list from CONVENTIONS.md §4 (unlisted, missing,
   mismatched bytes or sha256, an LFS pointer disagreeing with the entry, `storage`
   disagreeing with `git check-attr`, GPS or camera EXIF).
5. **Images**: every `.png`, `.jpg` and `.jpeg` is opened by Pillow; an image the
   maintainer approved is stripped first (`Image.open(p).save(q)` with no `exif` argument
   writes none; say that, and say exiftool is not a dependency here).

Related pages: `../reference/asset-manifest.md`, `../explanation/large-files.md`,
`../explanation/content-policy.md`, `rebuild-the-model.md`, `promote-an-asset.md`.

`docs/how-to/rebuild-the-model.md` — title `Rebuild the model`. From D
`models/biscuit/README.md` lines 61-78 and CONVENTIONS.md §3. Sections:

1. **What a rebuild is and is not**: it regenerates `assets/models/biscuit/` (the `.blend`,
   the GLB, the rig, the QA record, the previews) and the served viewer from the earlier
   studies; it is never run in CI (CONVENTIONS.md §1 decision 7); a rebuild replaces the
   approved model only when the maintainer approves the replacement (D README line 9 and
   65 say the same, and the rule is kept).
2. **What it needs**: Blender 5.2.1 (verified; D README line 63), Python 3 with Pillow (the
   repository's own venv has it), and a checkout of `biscuit_pics` at the commit
   `assets/models/biscuit/README.md` names, because the build reads the seven-folder chain
   under `biscuit_pics/generated/3d/` (list it as CONVENTIONS.md §3 does) and `viewer.py`
   reads camera frames from
   `miami-cinematic-sweater-foreleg-refined/qa/viewer-package.json`. The chain is not in
   this repository and is not going to be (§1 decision 4).
3. **The recipe**: `just model-rebuild /path/to/biscuit_pics` runs
   `scripts/rebuild_model.sh`, which is S02's. Describe what it does from CONVENTIONS.md
   §2 and D README lines 67-74: the five commands (`build.py`, `viewer.py`, `verify.py`,
   `render.py`, `proof_sheet.py`) run from `assets/models/biscuit/`, the viewer output
   moved to `static/pose-studio/viewer.html` and its three hrefs rewritten (§3), then
   `just assets-manifest` with `source: "rebuilt:<date>"` on every regenerated entry, and
   the diff read. If S02 has merged when this page is written, read S02's hand-back notes
   for how the script locates the chain (an argument, an environment variable, or both)
   and write that; if it has not, write the recipe's documented interface
   (`just model-rebuild <biscuit_pics path>`) and mark the page's open point in the
   hand-back notes.
4. **The optional checks**: `verify_browser.mjs` against an isolated Chrome profile and
   `verify_interchange.py`, from D README lines 76-78; where their reports land (`qa/`).
5. **What every rebuild costs**: 26 MB of ordinary history for the viewer and about 32 MB
   of LFS objects (§3), which is why rebuilds are rare and approved; the GLB carries PBR
   materials while the viewer and Blender carry the approved cel look (D README line 44);
   the three rewritten hrefs point at `main` (§11).

Related pages: `import-an-asset.md`, `../explanation/large-files.md`,
`../decisions/0006-sources-in-lfs-served-files-as-blobs.md`,
`../decisions/0008-the-viewer-is-embedded-as-is.md`.

`docs/how-to/promote-an-asset.md` — title `Promote an asset`. The interim procedure
CONVENTIONS.md §1 decision 2 names, to be replaced by what C02 designs. Sections:

1. **When an asset may leave**: not before the hub permits it. The hub's design direction
   page lists 3D rendering and generative artefacts under Avoid, and its character page
   expects an illustrator; a hub decision (C01) changes that, and until it lands nothing is
   promoted (§11). Say it plainly and link `../project/platform.md`.
2. **The interim procedure**: in the consumer (the hub or a game), copy the file with `cp`
   from a checkout of this repository at a named commit; record in the consumer, beside
   the file, the studio commit and the sha256 from `assets/manifest.json`; in this
   repository, write the item into `../operations/hub-handover.md` in that page's register
   (narrative, grouped by shape, naming the consumer, the file, the commit and the hash);
   never edit the other repository from here — that needs explicit authorization for each
   action. This is the register of the hub's own `consume-the-hub.md` "What still travels
   by citation" and its Poodl handover: a copy is written down where it was made and where
   it was taken.
3. **What the copy does not buy**: nothing compares the two files afterwards; a rebuild
   here changes nothing there; the ledger C02 designs is what will make a consumer's gate
   say so.
4. **What is promoted first**: name what the hub is waiting on (the favicon, the real
   `Monogram`, the `MascotSlot` poses — H decisions 0010 and 0017, `character.md` "What
   exists today") without deciding any of it.

Related pages: `../operations/hub-handover.md`, `../project/platform.md`,
`../decisions/0007-assets-travel-by-copy-and-ledger.md`, `import-an-asset.md`.

### Step 6: `docs/decisions/README.md`

H's page with: the second paragraph replaced by "These are decisions about how this
repository is built. What the platform's surfaces do is decided in the hub's specifications
and cited through `../project/platform.md`; the studio adds no rule of its own." **The
record**: nine rows, the titles exactly as CONVENTIONS.md §6 gives them (`A static site with
no backend`, `The hub is upstream`, `A Python toolchain in a frontend repository`, `A
project Pages site`, `Assembled by hand`, `Sources in LFS, served files as blobs`, `Assets
travel by copy and a ledger`, `The viewer is embedded as-is`, `No component workshop yet`).
**The numbering**: the series is the studio's own and starts at 0001; the first four were
taken from the template's records (T `0001`, `0008`, `0004`, `0010`) and generalised for a
repository that is not a game, and each says so under its heading; a slug never moves.
**Writing a new one** and the supersession paragraph: H's verbatim (lines 53-72). Related
pages: `../README.md`, `../project/platform.md`, `../explanation/architecture.md`.

### Step 7: The nine decision records

Every record: `## Context`, `## Decision`, `## Consequences` (the ones that hurt included),
`## What would reopen this`, `## Related pages`. The four carried ones open with an
italic provenance line in T's form: *Carried from the Biscuit Games template's decision
NNNN at `2283589`, and restated for a repository that is not a game.*

- **0001** `A static site with no backend`: T 0001 with "This game is a single-player
  game…" → the studio is a repository of assets and a site that shows them; no accounts,
  no server; the browser-state paragraph (T 31-33) dropped (the site stores nothing);
  the base-path paragraph pointing at `0004-a-project-pages-site.md`.
- **0002** `The hub is upstream`: T 0008 generalised. Context: the hub decides the look
  and publishes it as the package; the studio has nothing to delete because it started
  with the package. Decision: installed exactly (T's bullet, with the `.npmrc` and token
  sentences); the studio restates no figure and no clause (replacing T's two restatement
  bullets); no workshop composes the hub's (replacing T's workshop bullet; link
  `0009-no-component-workshop-yet.md`); one page points outward (`../project/platform.md`).
  Add a bullet: the character and the aesthetic are the hub's, so the studio changes the
  hub first — the first such change is the hub decision permitting renders from the model.
  Consequences: T's four, minus the clause paragraph, plus: the studio's own output is
  gated by a page it does not own. Reopeners: T's plus the hub declining to permit renders
  at all.
- **0003** `A Python toolchain in a frontend repository`: T 0004 with: the dependencies are
  `prek`, `ruff`, `pillow` and `biscuit-games-tooling`; `scripts/` holds the first-run
  script, `check_assets.py` and the rebuild script; Pillow is the one library the asset
  checker needs (EXIF); the allium installer sentence in the reopener dropped.
- **0004** `A project Pages site`: T 0010 rendered: the address, `pages.yml` calling
  `game-pages.yml` with the repository name from the event, `BASE_PATH` empty locally;
  Consequences: one setting before the first push (the Pages source; no package grant,
  the package is public), the address in the handbook is prose, every path goes through
  `paths.base`, and two more: the build checks out without LFS objects, so nothing served
  may ever be LFS-tracked; and the deploy runs on `workflow_run` after `CI`, publishing
  only a commit CI passed, a deliberate deviation from T (S04 hand-back). Reopeners: a custom domain; the platform serving the studio
  beneath a domain of its own (the hub's decision 0012 is where that is deferred).
- **0005** `Assembled by hand`: Context: T renders only a game (four questions, no toggle),
  and a render whose handbook pages are deleted breaks on its next `copier update`
  because `docs/manifest.yml` is re-rendered (CONVENTIONS.md §1 decision 5). Decision:
  copy the generic pieces from the hub, Poodl, the template and the tooling package by
  path, each with its source recorded in S00's provenance table in this handbook's
  `repository-map.md`, and take no Copier link. Consequences: toolchain changes arrive by
  hand, not by `copier update`; the studio can diverge (no workshop, an assets gate)
  without a template change; every file's provenance is a table a person maintains.
  Reopeners: the template growing a shape for a repository that is not a game; a third
  non-game repository.
- **0006** `Sources in LFS, served files as blobs`: CONVENTIONS.md §3 whole. Context: a
  92 MB model package, a 26 MB viewer, Pages serving pointer text for an LFS object, a
  free LFS tier. Decision: the `.gitattributes` patterns (quote them), the table of what is
  where and why, every CI checkout `lfs: false`, the checker reading pointers. Consequences:
  26 MB of history per viewer rebuild (accepted while rare; the three.js port is the exit,
  link `0008-the-viewer-is-embedded-as-is.md`); `git lfs install` per machine; a served
  path moved into LFS silently breaks the site; the free tier's figures (write the figure
  S02's hand-back notes report, or CONVENTIONS.md §3's figure marked "at the time of
  writing" if S02 has not merged). Reopeners: LFS quota exhausted; the viewer retired; a
  second model.
- **0007** `Assets travel by copy and a ledger`: CONVENTIONS.md §1 decision 2. Context: the
  hub's decision 0013 moved files into a package for the same reason (nothing compared two
  copies); the studio's assets are not a package's business — a game installs a stylesheet,
  not a `.blend` — and the hub never depends on the studio. Decision: a finished asset
  reaches the hub or a game by copy; every copy is recorded in a structured ledger with a
  small command-line tool so a copy is deterministic and a consumer's CI can verify it; the
  design of that ledger is a separate discussion (C02); until then the interim procedure on
  `../how-to/promote-an-asset.md` and the entry in `../operations/hub-handover.md`.
  Consequences: two copies exist and nothing compares them yet; a promoted asset is frozen
  at a commit; the hub rule (C01) gates the first promotion. Reopeners: the ledger landing
  (which narrows this record rather than superseding it); the hub choosing to install
  assets as a package after all.
- **0008** `The viewer is embedded as-is`: CONVENTIONS.md §1 decision 3 and §3. Context: a
  26 MB dependency-free WebGL2 page with the approved cel look, a 16 MB GLB with PBR
  materials, and a site that has to ship. Decision: serve the viewer unchanged under
  `static/pose-studio/` beside the two files it links, rewrite exactly three hrefs and
  record them in the manifest, link it from the model page rather than framing it inside
  the shell; port it to a maintained three.js component later (C03). Consequences: the
  viewer ignores the platform's tokens and theme (it is its own page, cream ground, its own
  type); it honours reduced motion on its own terms; every rebuild rewrites 26 MB; the two
  looks (viewer, GLB) differ and the model page says so. Reopeners: the three.js port; the
  file exceeding what Pages serves comfortably; the hub's rule refusing the look.
- **0009** `No component workshop yet`: CONVENTIONS.md §1 decision 10. Context: every
  sibling carries Storybook and Chromatic (the hub's decisions 0008 and 0009, cited
  through `../project/platform.md`); the studio authors no shared component and mounts the
  platform's. Decision: no Storybook, no Chromatic, no `stories/`, no `CHROMATIC_PROJECT_TOKEN`;
  the gate has three CI jobs, not four. Consequences: no visual review of the site;
  `tests/` is the whole evidence; the story-level accessibility checks the hub runs do not
  run here. Reopeners: the first component authored here (the three.js viewer, C03, is the
  likely one); a page whose look needs review across the four combinations.

Related pages on each record: two to four, relative, chosen from the pages that own the
subject.

### Step 8: Verify and hand back

Run the verification below, quote the output, set `status: done`, commit on the branch.

## Acceptance criteria

- [ ] All twenty-two files in Files touched differ from S00's stubs only below the H1;
      `git diff main -- docs/manifest.yml docs/README.md` is empty, and for every page the
      first nine lines (frontmatter, blank, H1) are unchanged from `main`.
- [ ] `uv run --frozen bg-validate-docs` prints `Validated 39 pages and <N> canonical
      topics.` and exits 0.
- [ ] `just check-docs` exits 0 (markdownlint, typos, lychee offline, the validator).
- [ ] Every page in Files touched has at least 150 words below the frontmatter (the
      contract's forty is a floor; a real page clears this comfortably), measured by
      `wc -w`.
- [ ] `grep -rn 'https://' docs/project docs/tutorials docs/how-to docs/decisions` matches
      lines in `docs/project/platform.md` only, and every match there is a
      `https://github.com/steven-cutting/biscuit_games/blob/main/docs/` URL without `#`.
- [ ] `grep -rln 'this game' docs/` is empty.
- [ ] `docs/decisions/README.md` has nine numbered rows, and each names a file that exists.
- [ ] Every risk CONVENTIONS.md §11 assigns to a subject a page here owns is named on that
      page (Step 1's list).
- [ ] `just check` is green.
- [ ] Each open point below is answered in the hand-back notes.

## Verification

From the repository root, on the branch:

```sh
uv run --frozen bg-validate-docs
just check-docs
for f in docs/project/*.md docs/tutorials/*.md docs/how-to/*.md docs/decisions/*.md; do printf '%6d %s\n' "$(wc -w < "$f")" "$f"; done
grep -rn 'https://' docs/project docs/tutorials docs/how-to docs/decisions
grep -rln 'this game' docs/ || echo none
git diff --stat main -- docs/manifest.yml docs/README.md
just check
```

Expected: `Validated 39 pages and <N> canonical topics.`; `just check-docs` exits 0; every
count at or above 150 (S06's stubs under other directories are not listed); `https://`
matches only in `docs/project/platform.md`; `none`; an empty diff stat; `just check` green
with every recipe listed.

## Hand-back notes

Filled in by the agent that executed this ticket, on branch `S05-handbook-a` in a Supacode
worktree, 2026-09-24. Four commits on the branch, this one included; nothing pushed. As
agreed on S00, the work stays on the worktree's branch rather than `ticket/s05-handbook-a`;
no check reads the branch name. Decided with the maintainer before writing: the Pages
address is written without its scheme off `project/platform.md` (below), no Codex review,
one commit per group of pages.

- **Verification**, run from the repository root after the third commit and the two
  follow-up edits below:

  ```text
  $ uv run --frozen bg-validate-docs
  Validated 39 pages and 40 canonical topics.
  $ just check-docs
  markdownlint ... Passed  /  typos ... Passed  /  lychee ... Passed
  Validated 39 pages and 40 canonical topics.
  $ grep -rn 'https://' docs/project docs/tutorials docs/how-to docs/decisions
  15 lines, all docs/project/platform.md: line 12 and the 14 table rows 61-74, each
  https://github.com/steven-cutting/biscuit_games/blob/main/docs/<page>.md, none with #
  $ grep -rln 'this game' docs/ || echo none
  none
  $ git diff --stat main -- docs/manifest.yml docs/README.md
  (empty)
  $ just check
  ==> just check-assets     check_assets check: ok
  ==> just check-docs       Validated 39 pages and 40 canonical topics.
  ==> just check-agents     Validated AGENTS.md, 2 adapters, and 8 skills.
  ==> just check-clean      The worktree matches the check baseline.
  All checks passed and the worktree is unchanged.
  ```

  `git diff --name-only main` lists exactly the twenty-two pages and this ticket, and for
  every page the first nine lines (frontmatter, blank, H1) match `main`.
- **Word counts** (`wc -w`, whole file), every one above 150:

  ```text
     791 docs/project/platform.md              1040 docs/tutorials/first-change.md
     687 docs/project/purpose-and-scope.md      448 docs/decisions/0001-static-site-no-backend.md
    1273 docs/project/repository-map.md          725 docs/decisions/0002-the-hub-is-upstream.md
     723 docs/project/terminology.md             535 docs/decisions/0003-python-toolchain.md
     902 docs/how-to/deploy-to-github-pages.md   619 docs/decisions/0004-a-project-pages-site.md
     871 docs/how-to/develop-locally.md          458 docs/decisions/0005-assembled-by-hand.md
    1011 docs/how-to/import-an-asset.md          657 docs/decisions/0006-sources-in-lfs-served-files-as-blobs.md
    1031 docs/how-to/maintain-dependencies.md    497 docs/decisions/0007-assets-travel-by-copy-and-ledger.md
     797 docs/how-to/promote-an-asset.md         501 docs/decisions/0008-the-viewer-is-embedded-as-is.md
    1056 docs/how-to/rebuild-the-model.md        389 docs/decisions/0009-no-component-workshop-yet.md
     661 docs/how-to/test-and-debug.md           557 docs/decisions/README.md
  ```

  (Counted before the two follow-up edits, which changed a word or two on
  `platform.md` and `terminology.md`.)
- **S02 had merged** when `rebuild-the-model.md` was written, so the page describes the
  real `scripts/rebuild_model.sh`: one positional path to the `biscuit_pics` checkout
  root, made absolute; `BLENDER` for the executable, defaulting to the macOS bundle; the
  refusals with status 2 (missing path, no study chain, no Blender, `assets/` or
  `static/pose-studio/` differing from `HEAD`, an existing `assets/biscuit_pics`); the
  symlink; the five commands; the purge of `__pycache__` and `*.blend1`; the three moves
  and the three asserted rewrites; `just assets-manifest`; and the trap that restores both
  trees to `HEAD` on failure or interruption, as S02 asked. Neither script reads an
  environment variable for the chain; the argument is the only interface.
- **S07 had not merged.** The address is written as the design says,
  `steven-cutting.github.io/biscuit_studio/`, and S07 confirms it on the first deploy.
- **Written as the design says rather than as the repository is:**
  - The three routes `/`, `/model/` and `/gallery/` (`develop-locally.md`,
    `first-change.md` step 2, `deploy-to-github-pages.md` "What the site serves",
    `repository-map.md`'s tree), and the model page saying beside the GLB download that
    its look differs (`rebuild-the-model.md`, decision 0008): **S03**.
  - The gallery importing the illustrations and the build fingerprinting them under
    `_app/` (`deploy-to-github-pages.md`, `repository-map.md`, `terminology.md`): the
    CONVENTIONS.md §10 Vite-import claim, **S03**.
  - The live address, the deploy gate's first run, and `scripts/bootstrap_repo.sh`
    applying the Pages source: **S07**.
- **Deviations from this ticket**, each with the reason:
  - *No `https://` scheme off `platform.md`.* Steps 2 and 4 asked for the Pages address
    as a code span with its scheme, which the `https://` acceptance grep matches. The
    maintainer chose to keep the criterion: the address is
    `steven-cutting.github.io/biscuit_studio/`, and the viewer's two rewritten GitHub URLs
    are described in words on `rebuild-the-model.md` and decision 0008, never written out.
  - *`platform.md`, beyond Step 3's list:* T's first link named the hub's repository root,
    which the grep's blob-URL rule refuses, so it names the hub's `docs/README.md`; the
    "What nothing here checks" opener, verbatim in T, said "an `https://` URL" and now
    says "an absolute URL into another repository", for the same grep. The two new
    sentences in "What holds the two together" end "never as a number written down a
    second time here" rather than repeating T's following sentence about version bumps.
    The boundary paragraph's example ("a cell is a cell … is this game's") had no studio
    reading and was rewritten around the character and a pose. The Consume the hub row
    says the studio "followed it by hand" rather than "was rendered with it done", and the
    Architecture decisions row says "the three below", since two rows were dropped.
  - *The checker's refusal line.* The ticket's shape `<path>: not in
    assets/manifest.json` is not what `scripts/check_assets.py` prints. A live run, with a
    4×4 PNG copied to `assets/illustrations/first-change.png` and then removed with the
    manifest restored, printed `assets/illustrations/first-change.png: present but not
    listed; run just assets-manifest` and `check_assets check: 1 finding(s)`, exit 1. The
    tutorial and `import-an-asset.md` quote that.
  - *Git LFS per clone, not per machine.* `scripts/initialize.sh` runs
    `git lfs install --local`, which configures the clone (and, from a worktree, the
    shared `.git/config`), so the pages say git-lfs is installed once per machine and
    `git lfs install --local` runs in each clone. CONVENTIONS.md §11's "per machine" is
    looser than the script.
  - *Frozen titles win.* The H1s S00 wrote for 0005 ("Assembled by hand, not rendered from
    the template") and 0007 ("Assets travel by copy and ledger") differ from Step 6's
    list; the index keeps S00's, which are the manifest's titles.
  - *The deploy page describes the `workflow_run` gate.* Step 4 predates S04's gate; the
    page says what `pages.yml` does now (after CI, only a push to `main` still at its head,
    no manual run, `gh run rerun` for a redeploy, the `name: CI` hazard) and decision 0004
    carries it as a consequence, as S04 corrected.
  - *`repository-map.md` gained "Where each part came from"*, a table of source
    repositories and commits by group, because decision 0005 (Step 7) cites a provenance
    table on that page and Step 2 did not provide one. It carries no ticket or owner
    column.
  - *`test-and-debug.md` gained "Debug an asset failure"*, a short section on reading
    `just check-assets` findings, which T has no counterpart for.
  - *`terminology.md`'s Lane row* is not one of H's entries (H has none); written fresh,
    without pointing a handbook reader at `tickets/`.
  - *`maintain-dependencies.md`* adds a sixth step to "Moving the design system package":
    look at the three routes in the four combinations, replacing T's Chromatic review.
  - *Decision 0004* opens with the italic provenance line although T's `.jinja` record
    has none, as Step 7 asks of all four carried records.
- **Found, not changed:** the viewer's `source_sha256` after a rebuild. The script's
  closing message says to set it "to the new viewer digest", which would make it equal to
  `sha256` if read literally, while CONVENTIONS.md §4 defines it as the source's digest
  when the committed bytes differ. The page says to update it for the new page, as the
  script asks, without choosing; whoever runs the first rebuild settles which digest is
  meant. A candidate note for S02's script or `reference/asset-manifest.md` (S06).
- **Authorisations.** `just sync` read the npm registry with the token already in
  `~/.npmrc`, needed for `just check`; nothing else touched the network. Pushing and
  opening the pull request have not been done and need separate authorisation.
- **Open points.**
  - *`rebuild-the-model.md` and S02*: settled; S02 had merged and the page describes its
    script.
  - *The address and S07*: carried forward; S07 confirms
    `github.event.repository.name` is `biscuit_studio`.
  - *The LFS figure in 0006*: settled from S02's note, 10 GiB of storage and 10 GiB of
    bandwidth a month, metered beyond, read 2026-09-23; 0006 says so and puts the three
    objects at about 0.3% of a month's bandwidth, not §3's 3%.
  - *The ledger's shape on `promote-an-asset.md`*: confirmed; the page describes the
    interim procedure only and says the ledger's design is a separate discussion.
  - *The tutorial's line shape*: settled by the live run above.

## Open points

- `how-to/rebuild-the-model.md` describes `scripts/rebuild_model.sh`, which S02 writes.
  If S02 has not merged, the page describes the recipe's interface from CONVENTIONS.md
  §2.2 and this is carried forward for S02's hand-back to confirm.
- `how-to/deploy-to-github-pages.md` names an address nothing has served yet. S07 confirms
  it and reports back if `github.event.repository.name` differs from `biscuit_studio`.
- `decisions/0006` quotes a free-tier LFS figure S02 is asked to read from GitHub's
  documentation. Write CONVENTIONS.md §3's figure marked "at the time of writing" if S02's
  note is not yet available.
- Whether the `promote-an-asset.md` page should already carry the ledger's intended shape
  from C02. It should not: C02 is a discussion, and the page describes the interim
  procedure only. Confirm this reading in the hand-back notes.
- The tutorial's step 5 has the reader add and then remove an asset. Whether
  `just check-assets` refuses the unlisted file with the exact line shape the page quotes
  depends on S00's `check_assets.py`; read S00's hand-back notes and quote the real line.
