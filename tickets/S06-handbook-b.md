---
id: S06
title: "Handbook B: explanation, reference and operations pages"
status: done
depends_on: [S00]
parallel_with: [S01, S02, S03, S04, S05]
branch: ticket/s06-handbook-b
estimated_size: L
---

# S06: Handbook B: explanation, reference and operations pages

## Context

S00 shipped every handbook page `CONVENTIONS.md` §6 lists as a stub: the exact frontmatter,
an H1 equal to the manifest title, and forty words saying what the page will say. The
manifest (`docs/manifest.yml`) and the map (`docs/README.md`) are final and no lane touches
them (CONVENTIONS.md §9). This ticket replaces the stub bodies of the sixteen pages under
`docs/explanation/`, `docs/reference/` and `docs/operations/`. S05 replaces the other
twenty-two (`project/`, `tutorials/`, `how-to/`, `decisions/`) in the same shape; the two
lanes share no path, and where a page here has to point at one of S05's, the stub exists
and the link resolves.

Every page is held to the documentation contract the tooling package enforces (H
`/Users/scutting/projects/biscuit_games/docs/reference/documentation-contract.md`; G
`/Users/scutting/projects/biscuit_games_tooling/src/biscuit_games_tooling/validate_docs.py`
lines 20-40 for the constants): the first heading is level one and equals the title; at
least forty words; no template delimiter (the validator's third pattern is a brace
followed by a hash, so prose about a Svelte block writes the words "each block" and never
the opener); no `TODO`, `TBD` or `FIXME`; every relative link resolves with exact case and
every fragment names a real heading; every page reachable from `docs/README.md`, which
S00's map already guarantees. Markdownlint (H `.markdownlint-cli2.jsonc`), `typos` and
lychee `--offline` also run over the pages in `just check-docs`.

Sources, at the commits CONVENTIONS.md §0 pins, read-only:

- H = `/Users/scutting/projects/biscuit_games` at `575e3dd`. The pages this ticket
  adapts, with the sections each has: `docs/explanation/architecture.md` (127 lines:
  intro 11-23, "Build" 25-46, "Runtime shape" 47-72, "State" 73-87, "Side effects"
  88-104, "What is not here" 105-120), `docs/explanation/accessibility.md` (344 lines:
  intro 11-28, "How the figures are measured" 29-68, "What the specification decides"
  69-137, "The one exemption, and how narrow it is" 138-167, "What the specifications
  carry beyond appearance" 168-282, "How this is checked" 283-337),
  `docs/explanation/security-model.md` (131 lines: "What there is to protect" 18-42,
  "Nothing is deployed" 43-54, "What the build defends" 55-89, "What a version does not
  defend" 90-115, "What is out of scope" 116-121, "Reporting" 122-125),
  `docs/explanation/quality-philosophy.md` (90 lines: five sections 15-85),
  `docs/reference/commands.md` (135 lines: "Setup" 16-41, "Dependencies" 42-49, "Develop"
  50-62, "Format and repair" 63-76, "Check" 77-90, "Documents and agents" 91-107,
  "Publish" 108-123, "Aggregate" 124-130), `docs/reference/configuration.md` (151 lines:
  "Build-time environment" 14-44 with "The base path" 24-44, "Tooling environment" 45-63,
  "Configuration files" 64-100 with "Storybook appearance globals" 86-100, "Values the
  specifications decide" 101-128, "Version pins" 129-145), `docs/reference/testing.md`
  (274 lines: "Framework" 11-23, "Layout" 24-55, "Conventions" 56-124, "Story tests"
  125-171, "Coverage" 172-206, "What the current suite proves" 207-223, "The contrast
  test" 224-268), `docs/reference/quality-gates.md` (165 lines: the table 9-30, the
  allium paragraphs 31-53, "What the hook gate contains" 68-98, "The mutating
  counterpart" 99-104, "In continuous integration" 105-137, "On `main`" 138-159),
  `docs/reference/documentation-contract.md` (90 lines), `docs/reference/agent-contract.md`
  (104 lines: "The four surfaces" 16-32, "What `AGENTS.md` must contain" 33-41, "What a
  skill must be" 42-69, "What a bridge must be" 70-85, "The inventory" 86-100),
  `docs/operations/maintenance.md` (108 lines: "Routine" 18-35, "Checking the links to
  Poodl" 36-66, "Per change to a shared surface" 67-88, "Secrets" 89-101),
  `docs/operations/troubleshooting.md` (189 lines; fifteen `##` entries at 13, 19, 28, 33,
  55, 62, 70, 92, 105, 115, 126, 139, 153, 159), `docs/operations/poodl-handover.md` (the
  register `hub-handover.md` takes: lines 9-23 for the opening, 695-722 for "What a
  cross-repository link costs"), `docs/how-to/consume-the-hub.md` lines 180-194 ("What
  still travels by citation"), `docs/design/character.md` lines 23-35 ("What exists
  today") and 128-134, `docs/decisions/0010-biscuit-games-design-system.md` and
  `docs/decisions/0017-the-rest-of-the-design-system-is-ported.md` (what the hub is
  waiting on art for).
- G = `/Users/scutting/projects/biscuit_games_tooling` at `6c5c07f`:
  `src/biscuit_games_tooling/validate_agents.py` lines 23-54 (`BRIDGE_BODY`, `TOLERATED`,
  `ADAPTERS`, `REQUIRED_GUIDANCE`), `run_allium.py` line 40 (`NO_INPUTS = 2`),
  `_project.py` lines 16-30 (`DEFAULT_RECIPES`), `actions/setup-toolchain/action.yml`,
  `.github/workflows/game-pages.yml`.
- T = `/Users/scutting/projects/biscuit_games_template` at `2283589`:
  `tickets/C03-repository-bootstrap.md` ("Deviations": the package is public, no grant).

Read first: CONVENTIONS.md §1 (every decision and fact), §2 (the tree, §2.1 the one
exclusion set, §2.2 the `Justfile`, §2.4 `pyproject.toml`, §2.7 appearance), §3 (large
files), §4 (the manifest and `scripts/check_assets.py`), §5 (content policy), §6 (the page
table with the exact title, kind, audience and slug of every page here), §7 (the agent
contract), §8 (CI and Pages), §9, §10 and §11. Then S00's hand-back notes: S00 wrote the
`Justfile`, `scripts/check_assets.py`, the eight skills and `AGENTS.md`, and several pages
here describe them.

## Goal

At the end of this ticket, on branch `ticket/s06-handbook-b`, the sixteen pages below
carry their real prose, each satisfying the contract; `just check-docs` and `just check`
are green; no file outside the list changed.

## Non-goals

- `docs/manifest.yml`, `docs/README.md`, any frontmatter, any title. Frozen by S00.
- S05's twenty-two pages. A page here links to one of them by path and decides nothing the
  owning page decides.
- Root `README.md`, `CHANGELOG.md`, `AGENTS.md`, `SECURITY.md`: S00 and S08.
- Any code, recipe, workflow, asset or manifest change. A fact a page needs that the
  repository does not yet make true is written as the design says it (CONVENTIONS.md) and
  named in the hand-back notes for the ticket that makes it true.
- Cross-repository links. They live on `docs/project/platform.md` only (CONVENTIONS.md §6,
  last paragraph); every page here names a hub page in prose or links to
  `../project/platform.md`.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `docs/explanation/architecture.md` | page | H `docs/explanation/architecture.md` | replace stub body |
| `docs/explanation/large-files.md` | page | new; CONVENTIONS.md §3 | replace stub body (step 3) |
| `docs/explanation/content-policy.md` | page | new; CONVENTIONS.md §5 | replace stub body (step 3) |
| `docs/explanation/accessibility.md` | page | H `docs/explanation/accessibility.md` | replace stub body |
| `docs/explanation/security-model.md` | page | H `docs/explanation/security-model.md` | replace stub body |
| `docs/explanation/quality-philosophy.md` | page | H `docs/explanation/quality-philosophy.md` | replace stub body |
| `docs/reference/commands.md` | page | H `docs/reference/commands.md` | replace stub body |
| `docs/reference/configuration.md` | page | H `docs/reference/configuration.md` | replace stub body |
| `docs/reference/testing.md` | page | H `docs/reference/testing.md` | replace stub body |
| `docs/reference/quality-gates.md` | page | H `docs/reference/quality-gates.md` | replace stub body |
| `docs/reference/asset-manifest.md` | page | new; CONVENTIONS.md §4 | replace stub body (step 5) |
| `docs/reference/documentation-contract.md` | page | H `docs/reference/documentation-contract.md` | replace stub body |
| `docs/reference/agent-contract.md` | page | H `docs/reference/agent-contract.md` | replace stub body |
| `docs/operations/maintenance.md` | page | H `docs/operations/maintenance.md` | replace stub body |
| `docs/operations/troubleshooting.md` | page | H `docs/operations/troubleshooting.md` | replace stub body |
| `docs/operations/hub-handover.md` | page | new; H `docs/operations/poodl-handover.md` for register | replace stub body (step 6); carry the item S01 hands over: the window before hydration in which a device asking for reduced motion or more contrast still gets the platform default, closed by `prefers-reduced-motion` and `prefers-contrast` rules in the hub's `app.css` |

Sixteen rows: six under `docs/explanation/`, seven under `docs/reference/`, three under
`docs/operations/`, which is every page CONVENTIONS.md §6's table assigns to S06, out of
the thirty-nine the table lists in all. Do not add a page.

The table is the whole scope. Nothing outside it is edited except the `status:` line of
this ticket.

## Steps

Work from the repository root on branch `ticket/s06-handbook-b`. Every page keeps S00's
frontmatter and H1 byte for byte; only the body below the H1 changes. Run
`uv run --frozen bg-validate-docs` after every few pages.

### Step 1: The rules every page obeys

- Forty words is a floor, not a target.
- "This repository" or "the studio", never "this game" and never "the hub" for this
  repository.
- Relative links only, to pages that exist; a path mentioned rather than followed is a
  code span.
- The hub is cited by page name in prose or by a link to `../project/platform.md`, never by
  URL.
- Prose about a Svelte block writes the words, never the two-character opener.
- Name the CONVENTIONS.md §11 risks a page's subject owns: the 26 MB history cost and the
  served-path-into-LFS risk (`large-files.md`); the manifest being as honest as its review
  and `git lfs install` being per machine (`asset-manifest.md` and `troubleshooting.md`);
  the hub rule standing until C01 (`hub-handover.md`); the first run needing the network
  (`troubleshooting.md`); cross-repository links rotting silently (`maintenance.md` and
  `hub-handover.md`); the gallery's weight and the GLB's PBR look (`architecture.md`).

### Step 2: The four adapted explanation pages

`docs/explanation/architecture.md`. H's page with: intro (11-23) rewritten — the studio is
a static site (link `../decisions/0001-static-site-no-backend.md`), and it *is* deployed,
to a project Pages site (link `../decisions/0004-a-project-pages-site.md`), so the "Today
there is no host" paragraph (20-23) is replaced by two sentences on what is served and
from where. **Build** (25-46): H's, with `src/lib/` described as `brand.ts`,
`appearance.ts` and `Lockup.svelte` and nothing packaged; add that `static/pose-studio/`
is copied into `build/` byte for byte by `adapter-static`, and that `assets/` is reached
only by Vite imports from the two showcase routes (the gallery imports eleven PNG files, 14 MB,
which is the page's weight and is accepted for the first release — §11). **Runtime shape**
(47-72): H's, for three routes instead of one, and the viewer as a separate page the model
route links to rather than frames (`../decisions/0008-the-viewer-is-embedded-as-is.md`),
with the GLB's PBR look named beside it. **State** (73-87): H's; the two attributes
`app.html` states, and that line 81's reference to the hub's specification module becomes
"the platform's appearance module, installed with the package". **Side effects** (88-104):
H's first paragraph replaced by CONVENTIONS.md §2.7 — the preferences port the package
exports, `applyAppearance` in `src/lib/appearance.ts`, `document.documentElement` reached in
`onMount` in `src/routes/+layout.svelte` and nowhere else, the test handing in an element
it owns; keep H's paragraph on the port's shape and cite the hub's decision on ports
through `../project/platform.md` rather than a local record. **What is not here**
(105-120): no API, no game, no package, no workshop
(`../decisions/0009-no-component-workshop-yet.md`), no Blender in CI, and no rebuild chain
(`large-files.md`). Related pages: the two decisions above, `large-files.md`,
`../reference/configuration.md`, `../how-to/deploy-to-github-pages.md`.

`docs/explanation/accessibility.md`. H's page is 344 lines about the platform's measured
palette, its play surface and its story run; almost none of that is the studio's to
restate. Write a page of five sections that cites and does not copy: **What the studio
inherits** — the platform's three modules arrive with the package and every guarantee in
them binds this site; the four theme and contrast combinations; name the guarantees by
their exact names (`SystemFollowsTheDeviceAsItChanges`,
`ReducedMotionOverridesTheAnimationSetting`, `MoreContrastFromTheDeviceTurnsHighContrastOn`,
`AppearanceNeverCarriesMeaningAlone`, `EveryCombinationMeetsTheLegibilityFloor`,
`AnUnavailableControlIsExempt`) and say the hub's accessibility page owns their account
(link `../project/platform.md`). **What the studio does about it** — `app.html` states
`dark`; `src/lib/appearance.ts` derives `data-animations` and `data-high-contrast` from the
device through the port (CONVENTIONS.md §2.7), which is more than the hub's own route does
and exactly what a game is told to do; the site adds no colour of its own and no state
that colour carries. **The viewer** — it is its own page on a cream ground with its own
type, it honours reduced motion on its own terms (auto-rotate off), it is keyboard
operable per D's README lines 25, it needs WebGL 2, and none of the platform's tokens reach
it; that is a known cost of embedding it as-is
(`../decisions/0008-the-viewer-is-embedded-as-is.md`) and the first thing the three.js port
repairs. **Images** — every illustration on the gallery carries alt text that says what the
picture is and how it was made; the previews on the model page likewise; nothing a reader
needs depends on an image being drawn. **How this is checked** — `tests/` (the appearance
test, the route tests querying by role and name); no axe run and no contrast test here,
because no story run exists (`../decisions/0009-no-component-workshop-yet.md`) and the
palette is measured where it is declared; the `accessibility-review` skill. Related pages:
`../project/platform.md`, `../reference/testing.md`, the two decisions.

`docs/explanation/security-model.md`. H's page with: **What there is to protect** (18-42)
rewritten — the site holds no reader data and stores nothing; what there is to protect is
the integrity of the assets (the manifest, link `../reference/asset-manifest.md`) and the
content policy (`content-policy.md`: no photograph of the real dog without approval and
stripping, no third-party art); line 33's Chromatic secret dropped — the studio holds no
stored secret at all. **Nothing is deployed** (43-54) becomes **What is deployed**: a
project Pages site, the two publishing scopes held by `pages.yml`'s deploy job and by
nothing else, the build job holding `contents: read` and `packages: read`, the run's own
token installing the package, no stored credential anywhere. **What the build defends**
(55-89): H's, minus the allium sentence (58) and the Chromatic paragraphs (62-75); add that
`just check-assets` refuses a changed byte under `assets/` and `static/pose-studio/`, and
that the manifest is only as honest as its review (§11). **What a version does not defend**
(90-115): rewritten as "What a copy does not defend" — a promoted asset is a copy at a
commit, nothing compares it later, C02 is the ledger (`../decisions/0007-assets-travel-by-copy-and-ledger.md`).
**What is out of scope** and **Reporting**: H's, with `SECURITY.md` cited. Related pages:
`content-policy.md`, `../reference/asset-manifest.md`, `../how-to/deploy-to-github-pages.md`.

`docs/explanation/quality-philosophy.md`. H's five sections nearly verbatim: "Checks are
read-only", "Fix the cause, not the report", "Unreachable is not untested", "Tests inject,
they do not stub" all stand; lines 37-48's Poodl examples are replaced by the studio's
(the one exclusion set §2.1 is a suppression written once with its reason, not a rule
disabled at a call site; `applyAppearance` taking an element rather than reading
`document`). "The specification is the arbiter" (81-85) becomes "The hub is the arbiter":
a look or a rule the studio disagrees with is changed in the hub first, and the first
worked example is the decision permitting renders from the model. Add a sixth section
**An asset is evidence too**: the manifest, the checker's self-test on every run, and the
rule that nothing under `assets/` is edited by hand. Related pages:
`../reference/quality-gates.md`, `../reference/testing.md`, `../reference/asset-manifest.md`.

### Step 3: The two new explanation pages

`docs/explanation/large-files.md` — title `Large files`. CONVENTIONS.md §3, in prose:
**Why two storages** (Pages serves an LFS pointer as text; a source a rebuild rewrites is
history the clone carries forever); **The patterns** (`.gitattributes` quoted whole, with
the reason for each line); **What is where** (the table of the nine rows with bytes,
storage and reason, and the total of 32.3 MB in LFS; take each byte figure from
`assets/manifest.json`, not from §3, whose `textures/` and `illustrations/good/` totals
are wrong: the manifest sums them to 10,040,783 and 15,137,724, S02's hand-back notes);
**What it costs** (the free tier's storage and bandwidth figures as S02's hand-back notes
read them from GitHub's documentation on 2026-09-23: 10 GiB of storage and 10 GiB of
bandwidth a month, with metered billing beyond that rather than data packs, and a
download counting against the repository owner — write the date beside the figure;
a clone that fetches spends about 0.3% of a month's bandwidth; every viewer rebuild
adds 26 MB of ordinary history; `git lfs install` is per machine and
`scripts/initialize.sh` runs it; every CI checkout is `lfs: false` and the checker reads
pointers); **The risk** (a served path moved under an LFS pattern silently deploys pointer
text; the patterns name sources by path for that reason); **The three rewritten hrefs**
(what they are, why, that the manifest's `patched` field records them and that they point
at `main`). Related pages: `../decisions/0006-sources-in-lfs-served-files-as-blobs.md`,
`../reference/asset-manifest.md`, `../how-to/import-an-asset.md`,
`../how-to/rebuild-the-model.md`.

`docs/explanation/content-policy.md` — title `Content policy`. CONVENTIONS.md §5 whole, as
the owning page: **Never committed** (each bullet as a paragraph: photographs of the real
dog without the maintainer's approval of that photograph and with any metadata left in
them, and that copying one is a separately authorised action; the reference art under the
source repository's `inspiration/`, named as third-party copyrighted material; the two
commercial fonts; the rejected work, the rebuild chain, the model sheets and the scratch
profile, each as a code-span path); **Generated art is labelled** (the eleven cel
illustrations were made with an image model, the manifest says so in `source`, the
gallery says so on the page, and whether they may leave the studio is the hub's decision —
link `../project/platform.md` and say the studio waits on it); **The licence is open**
(the hub's character page says the photographs' licensing is undecided; the manifest's
`licence` field is `unsettled` until the maintainer decides; `package.json` is
`UNLICENSED`; an agent that needs an answer records the question and stops); **What
enforces it** (`just check-assets` refuses GPS and camera EXIF; review refuses the rest —
no gate can tell a permitted image from a forbidden one). Related pages:
`../how-to/import-an-asset.md`, `../reference/asset-manifest.md`, `security-model.md`,
`../project/purpose-and-scope.md`.

### Step 4: The six adapted reference pages

`docs/reference/commands.md`. H's tables with the studio's recipes, which are exactly
CONVENTIONS.md §2.2's: **Setup** — `initialize`, `sync`, `install-hooks` (keep H's
"Do not install the hook from a secondary worktree" subsection, lines 27-41, verbatim);
drop `install-allium`, `storybook-browsers`, `storybook-browsers-deps` (23-25).
**Dependencies** — `lock`, `lock-upgrade`, `lock-check`. **Develop** — `dev`, `preview`
(with `BASE_PATH`), `frontend-watch`; drop `storybook` (56) and the paragraph at 59.
**Format and repair** — `format`, `fix`. **Check** — `lint`, `frontend-static`,
`frontend-unit`, `frontend-coverage`, `frontend-build`; drop 86-89. **Documents and
agents** — `check-docs`, `check-agents`; drop `check-specs`, `analyse-specs` and the allium
paragraph (97-106). New section **Assets** — `check-assets` (what it refuses, that it runs
`self-test` first), `assets-manifest` (the one recipe that writes the manifest; keeps
`source`), `model-rebuild <biscuit_pics>` (needs Blender; never in `just check`; link
`../how-to/rebuild-the-model.md`). **Publish** — none: the site is published by
`pages.yml` once CI passes on a push to `main`, and no recipe publishes anything (replace 108-123).
**Aggregate** — `check-clean`, `check`, `check-links-online`. Each row's description in
H's register, one sentence, saying what it proves and whether it needs the network.

`docs/reference/configuration.md`. H's page with: **Build-time environment** — "The base
path" (24-44) rewritten: `BASE_PATH` is `/biscuit_studio` in `pages.yml` (read from the
event) and empty locally; the two decision-0012 sentences (29-30) dropped; add that
`static/pose-studio/` is served beneath the base too. **Tooling environment** (45-63)
minus `CHROMATIC_PROJECT_TOKEN` and `STORYBOOK_DISABLE_TELEMETRY` (51-52); add
`NODE_AUTH_TOKEN` (CI only, the run's token, on the step that installs) and the `~/.npmrc`
token line written as `<your token>`. **Configuration files** (64-85): the studio's files
— every root config in CONVENTIONS.md §2 with one sentence each, `assets/manifest.json`
and `.gitattributes` added, `vitest.config.ts` and the four Storybook rows (70, 73-76)
dropped; drop "Storybook appearance globals" (86-100). **Values the specifications
decide** (101-128) becomes **Values the studio does not decide**: the platform's figures
arrive in the stylesheet and the components, the studio mirrors none in a `config.ts`
(there is no `src/lib/config.ts`), and a figure the site needs is read from the hub's page
through `../project/platform.md`. **Version pins** (129-145): H's with the pins the studio
holds — Node, npm, uv, Python, just (the five G's action defaults), the tooling package at
`v0.3.0`, Pillow, the platform package at `1.1.0`; the allium sentences (142-144) dropped;
that `scripts/bootstrap_repo.sh` is T's verbatim. Related pages: `commands.md`,
`../how-to/deploy-to-github-pages.md`, `../how-to/maintain-dependencies.md`,
`../decisions/0004-a-project-pages-site.md`.

`docs/reference/testing.md`. H's 274 lines become a page a third as long: **Framework**
(11-23) — Vitest under jsdom with Testing Library, `vite.config.ts` names the one suite;
lines 16-23 (the Storybook config) dropped. **Layout** (24-55) — `tests/` never colocated;
the five files (`setup.ts`, `brand.test.ts`, `lockup.test.ts`, `appearance.test.ts`,
`route.test.ts`, `pages.test.ts`) and `tests/fixtures/exif-gps.jpg`, each with one
sentence; `*.spec.ts` reserved; no `stories/`. **Conventions** (56-124) — H's rules that
still apply: query by accessible role and name never by class or test id; inject fakes,
never stub a global (the fake preferences port from the package; the element a test hands
`applyAppearance`); one assertion per claim; lines 82-124's play-surface examples dropped.
**Coverage** (172-206) — the floor, the glob, the three measured files, `src/routes/`
outside it, and why `Lockup.svelte` has no if block. **What the current suite proves**
(207-223) — a table of the six files as CONVENTIONS.md §2 and S01/S03 describe them (write
what the design says; S01 and S03 confirm). Drop "Story tests" (125-171) and "The contrast
test" (224-268) and say in one sentence, under Framework, that neither exists here and
why (`../decisions/0009-no-component-workshop-yet.md`; the palette is measured where it is
declared). Add **The asset checker's own test**: `scripts/check_assets.py self-test`, run
first by `just check-assets`, and the fixture it refuses. Related pages:
`quality-gates.md`, `../how-to/test-and-debug.md`, `asset-manifest.md`.

`docs/reference/quality-gates.md`. H's table (9-30) with the studio's nine rows:
`lock-check`, `lint`, `frontend-static`, `frontend-coverage`, `frontend-build`,
`check-assets` ("Every asset is listed, byte-identical to its manifest entry, and carries
no GPS or camera EXIF; the checker's self-test passed first"), `check-docs`,
`check-agents`, `check-clean`; the allium paragraphs (31-53) replaced by one paragraph
saying why no specification gate runs (`bg-run-allium` exits 2 on an empty input set;
the studio has no `docs/specs/`; CONVENTIONS.md §1 fact 1) and one on the one exclusion
set (§2.1: which hooks skip the assets and why, that the set is written in six files, and
that `assets/models/biscuit/README.md` and `assets/manifest.json` are deliberately not in
it). **What the hook gate contains** (68-98): H's list minus eslint's storybook paths,
check-specs and analyse-specs, with `check-added-large-files --maxkb=768` explained
against the exclusion. **The mutating counterpart** (99-104): H's. **In continuous
integration** (105-137): the three jobs from CONVENTIONS.md §8 (`frontend`, `documents`,
`assets`), each with its steps, the composite action, `NODE_AUTH_TOKEN` on the install
step alone, `lfs: false` and why. **On `main`** (138-159): the three checks required, not
up to date, no review, no force push, administrators not bound, applied by
`scripts/bootstrap_repo.sh` (`../how-to/deploy-to-github-pages.md`). Related pages:
`commands.md`, `testing.md`, `../explanation/quality-philosophy.md`.

`docs/reference/documentation-contract.md`. H's page verbatim (90 lines) with two edits:
"This project defines none" stands; the paragraph on `docs/specs/` (lines 78-80 region,
"Only `docs/**/*.md` is in scope…") loses its Allium sentence and says instead that
`assets/models/biscuit/README.md` sits outside `docs/` and outside the contract, and is
linted by markdownlint and lychee only.

`docs/reference/agent-contract.md`. H's page with: **The four surfaces** verbatim; **What
`AGENTS.md` must contain** verbatim, plus one sentence after the six phrases: the studio
has no `docs/specs/`, and its `AGENTS.md` says so in the sentence that carries the phrase,
because the validator checks presence and not meaning; **What a skill must be** with
"ten canonical skills" → "eight canonical skills" and the eight names from
CONVENTIONS.md §7 in a list with one line each (the two new ones, `asset-change` and
`hub-handover`, described from §7's table); **What a bridge must be** and **The
inventory** verbatim.

### Step 5: `docs/reference/asset-manifest.md`

Title `Asset manifest`. CONVENTIONS.md §4 as a reference page: **The file**
(`assets/manifest.json`, strict JSON, one object per line sorted by `path`, one trailing
newline, ignored by Prettier and parsed by `check-json`; every file under `assets/` and
`static/pose-studio/` except the manifest itself). **An entry** (the example quoted, then
a table of the six required fields with type and meaning, then the two optional fields
`source_sha256` and `patched` and when each is present; the `source` forms
`<repository>@<commit>:<path>`, `rebuilt:<date>`, `studio`; `licence` is `unsettled`
until decided — `../explanation/content-policy.md`). **The checker**
(`scripts/check_assets.py`: `check`, `write`, `self-test`, each as §4 gives it, with the
exact refusal reasons and the exit codes; how an LFS pointer is verified and why CI never
fetches; the EXIF tags refused, by name and hex). **What it does not prove** (a rewritten
manifest passes; `source` is never rewritten by the tool; review reads the diff — §11).
**The recipes** (`just check-assets`, `just assets-manifest`). Related pages:
`../how-to/import-an-asset.md`, `../explanation/large-files.md`,
`../explanation/content-policy.md`, `commands.md`.

### Step 6: The three operations pages

`docs/operations/maintenance.md`. H's page with: **Routine** (18-35) — weekly: read a
failing run of `ci.yml` or `pages.yml`; monthly: `just check-links-online` and the
dependency review (H's paragraph, minus the TypeScript aside if it no longer applies —
check H's `package.json` pins against `typescript-eslint`'s support and keep the sentence
only if S00's hand-back says the same hold is in force); per change: below. **Checking the
links to Poodl** (36-66) becomes **Checking the links to the hub**: the blob URLs on
`../project/platform.md`, `just check-links-online`, what a failure means (a page moved in
the hub), and that nothing offline checks them (§11). **Per change to a shared surface**
(67-88) becomes **Per change to an asset that has left**: a rebuild or a replacement of a
promoted asset is a change to what a consumer holds a copy of; run the `hub-handover`
skill, write the item into `hub-handover.md`, change nothing in the other repository; and
**Per rebuild of the model**: `../how-to/rebuild-the-model.md`, the maintainer's approval,
the history cost. **Secrets** (89-101): there are none — no Chromatic, no deployment
credential; `pages.yml` deploys with the run's own token under `pages: write` and
`id-token: write`; the registry token lives in `~/.npmrc` and in `github.token`. Related
pages: `hub-handover.md`, `../how-to/maintain-dependencies.md`,
`../explanation/security-model.md`.

`docs/operations/troubleshooting.md`. H's entries kept where they apply, each as a `##`
heading in H's form: lines 13-32 (a recipe changed the worktree; the two `docs validation`
messages) verbatim; 33-54 ("A page written here is already owned by Poodl") rewritten as
"A fact written here is the hub's" (record it in `hub-handover.md`; never edit the hub);
55-69 (the two `agent validation` messages) verbatim; 70-91 (the specifications) dropped;
92-104 (`svelte-check` unused selector) kept; 105-114 (coverage) kept, naming the three
measured files; 115-125 and 126-138 (Storybook) dropped; 139-152 (`matchMedia` under
jsdom) kept, saying the fake port from the package is the answer; 153-158 (`just dev`
versus the build) kept, with `BASE_PATH` named; 159-182 (hooks in another worktree)
verbatim. New entries, each with the message the tool prints and the repair:
`check-assets: <path>: not in assets/manifest.json` (run `just assets-manifest`, read the
diff); `check-assets: <path>: sha256 differs` (an asset was edited by hand or a rebuild was
not recorded; never edit the manifest to agree); `check-assets: <path>: carries GPS EXIF`
(strip it, and only with approval); `check-assets: <path>: storage lfs but filter is
unset` (a file landed as a blob because `git lfs install` had not run — §11);
`biscuit-poseable.blend` is 130 bytes of text (a clone without git-lfs; install it and
`git lfs pull`); `npm ci` answers `404 Not Found` for the platform package (no
`read:packages` token in `~/.npmrc` — the registry lies); the first `just lint` takes a
minute and needs the network (prek clones every hook); `Failed to create deployment
(status: 404)` (the Pages source is not GitHub Actions; `scripts/bootstrap_repo.sh`);
the deployed viewer's download link serves a small text file (a served path was moved
under an LFS pattern); `just dev` answers `403` for a gallery drawing with "outside of
Vite serving allow list" (an import from `assets/` needs `server.fs.allow: ['assets']` in
`vite.config.ts`, which S03 added; never widen it to the repository root). Quote each
message from S00's `check_assets.py` and hand-back notes rather than from this ticket
where the two differ.

`docs/operations/hub-handover.md` — title `Hub handover`. The studio's ledger, in the
register of the hub's Poodl handover (narrative prose grouped by shape, never a
checkbox). Opening paragraph in H's form (poodl-handover lines 11-23): **Nothing here has
happened.** Every item is a change to another repository or a wait on one, none has been
made, editing another repository needs explicit authorization for each action, this
repository records and never acts. Sections:

1. **What the hub owes the studio.** The brand rule: the hub's design direction page lists
   3D rendering and generative artefacts under Avoid and its character page expects a
   commissioned illustrator; a hub decision (C01) permitting cel-shaded renders from the
   approved model and vetted generated art is what the studio waits on, and until it lands
   nothing here is promoted (§11). Registering the studio: the hub's repositories table
   and its boundary page know a hub and a game and nothing else; C04 adds the studio. What
   the hub is waiting on art for: the favicon (the hub's decision 0010 deferred it, and
   `app.html` still carries an empty icon), the real `Monogram` (the character page's "What
   exists today": a placeholder mark set in type until an illustrator draws the real one),
   and the `MascotSlot` poses (the hub's decision 0017 refused the slot until the
   illustrated poses arrive) — each named as something the studio can supply once the rule
   permits it, and none decided here.
2. **What the studio owes the hub.** Nothing until the rule changes. After it: the first
   promoted assets, each by the interim procedure (`../how-to/promote-an-asset.md`), and
   the ledger C02 designs.
3. **What a promoted asset carries.** The studio commit, the manifest sha256, the path
   here and the path there, the date, written in this section as prose when it happens.
4. **What a cross-repository link costs.** H's poodl-handover lines 695-722 restated for
   the studio: the contract skips `https://`, lychee is offline, only
   `just check-links-online` resolves, whole-page links only, a hub page path is part of
   the studio's interface to the hub and rots silently.

Related pages: `../how-to/promote-an-asset.md`, `../project/platform.md`,
`maintenance.md`, `../decisions/0007-assets-travel-by-copy-and-ledger.md`.

### Step 7: Verify and hand back

Run the verification below, quote the output, set `status: done`, commit on the branch.

## Acceptance criteria

- [ ] All sixteen files in Files touched differ from S00's stubs only below the H1;
      `git diff main -- docs/manifest.yml docs/README.md` is empty, and for every page the
      first nine lines (frontmatter, blank, H1) are unchanged from `main`.
- [ ] `uv run --frozen bg-validate-docs` prints `Validated 39 pages and <N> canonical
      topics.` and exits 0.
- [ ] `just check-docs` exits 0.
- [ ] Every page in Files touched has at least 150 words below the frontmatter, measured
      by `wc -w`.
- [ ] `grep -rn 'https://' docs/explanation docs/reference docs/operations` is empty.
- [ ] `grep -rln 'this game' docs/` is empty, and `grep -rn 'Chromatic\|Storybook'
      docs/explanation docs/reference docs/operations` matches only sentences saying the
      studio has neither (allow the decision-0009 citations).
- [ ] `docs/operations/hub-handover.md` opens with "Nothing here has happened" and
      contains no `- [ ]`.
- [ ] `docs/reference/quality-gates.md`'s table lists exactly the recipes
      `pyproject.toml` `[tool.biscuit-games-tooling] recipes` names, in that order, plus
      `check-clean` last.
- [ ] `docs/reference/commands.md` names every recipe `just --list` prints and no other.
- [ ] Every risk CONVENTIONS.md §11 assigns to a subject a page here owns is named on that
      page (Step 1's list).
- [ ] `just check` is green.
- [ ] Each open point below is answered in the hand-back notes.

## Verification

From the repository root, on the branch:

```sh
uv run --frozen bg-validate-docs
just check-docs
for f in docs/explanation/*.md docs/reference/*.md docs/operations/*.md; do printf '%6d %s\n' "$(wc -w < "$f")" "$f"; done
grep -rn 'https://' docs/explanation docs/reference docs/operations || echo none
grep -rln 'this game' docs/ || echo none
just --list | sed -n '2,$p' | awk '{print $1}' | sort > ai_tmp/recipes.txt
grep -o '`just [a-z-]*' docs/reference/commands.md | sed 's/`just //' | sort -u > ai_tmp/documented.txt
diff ai_tmp/recipes.txt ai_tmp/documented.txt && echo recipes-agree
git diff --stat main -- docs/manifest.yml docs/README.md
just check
```

Expected: `Validated 39 pages and <N> canonical topics.`; `just check-docs` exits 0; every
count at or above 150; `none`; `none`; `recipes-agree` (the `default` recipe and any
recipe taking an argument appear in both lists by name); an empty diff stat; `just check`
green.

## Hand-back notes

Filled in by the agent that executed this ticket, on branch `S06-handbook-b` in a Supacode
worktree, 2026-09-24. Six commits on the branch, the fifth being these notes; nothing pushed. As agreed
on S00, the work stays on the worktree's branch rather than `ticket/s06-handbook-b`; no check
reads the branch name. Decided with the maintainer before writing: `just sync` and prek's hook
clones authorised; no ticket ids on handbook pages (future work described in words, as S05
did: the hub decision permitting renders, the ledger's design, the hub registering the studio,
the three.js port, the gallery thumbnails); one commit per group of pages; a Codex adversarial
review before hand-back; and the §11 error below handed to S09 rather than corrected here.

- **Verification**, run from the repository root after the last page commit:

  ```text
  $ uv run --frozen bg-validate-docs
  Validated 39 pages and 40 canonical topics.
  $ just check-docs
  markdownlint ... Passed  /  typos ... Passed  /  lychee ... Passed
  Validated 39 pages and 40 canonical topics.
  $ grep -rn 'https://' docs/explanation docs/reference docs/operations || echo none
  none
  $ grep -rln 'this game' docs/ || echo none
  none
  $ diff ai_tmp/recipes.txt ai_tmp/documented.txt && echo recipes-agree
  recipes-agree
  $ git diff --stat main -- docs/manifest.yml docs/README.md
  (empty)
  $ just check
  ==> just check-assets     check_assets check: ok
  ==> just check-docs       Validated 39 pages and 40 canonical topics.
  ==> just check-agents     Validated AGENTS.md, 2 adapters, and 8 skills.
  ==> just check-clean      The worktree matches the check baseline.
  All checks passed and the worktree is unchanged.
  ```

  The two `>` redirects in the Verification block were run as `>|`, because the shell has
  `noclobber`, after `mkdir -p ai_tmp`. `git diff --name-only main` lists exactly the sixteen
  pages (and this ticket, after this commit), and for every page the first nine lines match
  `main`. `grep -rn 'Chromatic\|Storybook'` over the three directories matches nothing at all:
  the pages say "no component workshop" and "no story run" and cite decision 0009 instead.
  `docs/operations/hub-handover.md` opens with "Nothing here has happened" and holds no
  `- [ ]`. `quality-gates.md`'s table is `pyproject.toml`'s eight recipes in order, then
  `check-clean`.
- **Word counts** (`wc -w`, whole file), every one above 150:

  ```text
     907 docs/explanation/accessibility.md       973 docs/reference/agent-contract.md
    1243 docs/explanation/architecture.md       1705 docs/reference/asset-manifest.md
     798 docs/explanation/content-policy.md     1154 docs/reference/commands.md
    1274 docs/explanation/large-files.md        1219 docs/reference/configuration.md
     900 docs/explanation/quality-philosophy.md  542 docs/reference/documentation-contract.md
     943 docs/explanation/security-model.md     1437 docs/reference/quality-gates.md
    1378 docs/operations/hub-handover.md        1156 docs/reference/testing.md
    1019 docs/operations/maintenance.md
    2182 docs/operations/troubleshooting.md
  ```

- **Every lane had merged** (S00 to S05, `main` at `c735798`), so nothing on these pages is
  written as the design says rather than as the repository is. `large-files.md` carries
  S02's figures: 10 GiB of storage and 10 GiB of bandwidth a month, metered beyond, read
  from GitHub's documentation on 2026-09-23 (the date is on the page), about 0.3% per full
  fetch; every byte figure is read from `assets/manifest.json` (viewer 27,561,668,
  `textures/` 10,040,783 over 36 files, `previews/` 9,754,946 over 22, `illustrations/good/`
  15,137,724 over 11; LFS total 32,281,033). `testing.md`'s suite table describes the six
  files S01 and S03 committed, read from the tests themselves.
- **The `check-assets` messages** on `troubleshooting.md` and `asset-manifest.md` are quoted
  from `scripts/check_assets.py`, not from this ticket, which paraphrased them. The ticket's
  `check-assets: <path>: not in assets/manifest.json` is really
  `<path>: present but not listed; run just assets-manifest`; `sha256 differs` is
  `<path>: sha256 differs from the manifest; run just assets-manifest and read the diff`;
  `carries GPS EXIF` is `<path>: carries EXIF (GPSInfo); strip every metadata field before
  committing`; and the storage finding is `<path>: storage 'lfs' but .gitattributes says
  'blob'` (either way round). The script prints no `check-assets:` prefix, so the headings
  read "`just check-assets` prints ...". `asset-manifest.md` quotes all seventeen reasons (sixteen in its table, one against the viewer's build record).
- **The storage-drift claim is false; handed to S09.** The ticket's entry "storage lfs but
  filter is unset (a file landed as a blob because `git lfs install` had not run)" describes
  something the checker cannot see, and CONVENTIONS.md §11 ("`check-assets`'s `git
  check-attr` comparison reports `storage` drift") and decision 0006 (S05: "the checker's
  comparison with `git check-attr` reports it only once it is already in the index") say the
  same. `git check-attr` reads `.gitattributes`, not whether the filter is installed, and a
  raw `.blend` hashes to the oid the entry records. Proved in a throwaway repository in the
  session scratchpad, with `GIT_CONFIG_GLOBAL=/dev/null` so no LFS filter was configured:

  ```text
  no lfs filter configured
  check_assets write: ok
  index blob size: 5000                      (a raw blob, not a pointer)
  assets/models/scene.blend: filter: lfs
  check_assets check: ok
  rc=0
  (then, with .gitattributes emptied)
  assets/models/scene.blend: storage 'lfs' but .gitattributes says 'blob'
  check_assets check: 1 finding(s)
  ```

  So the pages say the truth: nothing in the gate notices a `.blend` committed as a blob
  (`large-files.md`, `asset-manifest.md`), `troubleshooting.md` has an entry for spotting it
  (`git lfs ls-files` omits the path; `git cat-file -s HEAD:<path>` prints the full size
  rather than 133), and the storage message is filed under its real cause, a path moved
  into or out of a pattern without `just assets-manifest`. For S09: correct the §11 bullet
  and decision 0006's sentence; and, if the maintainer wants the gap closed, a checker change
  that reads each `lfs` entry's index blob (`git cat-file`) and refuses one that is not a
  pointer.
- **Other items for S09** (addressed to done tickets, CONVENTIONS.md or a reserved file):
  - *The Codex review's two code-side findings* (below): `check_assets.py` could validate the
    three `source` forms with self-test cases, and `write` could run `self-test` before its
    comparison. The pages now describe the script as it is.
  - *S09 step 4 changes a sentence here.* `documentation-contract.md` says the model's README
    "is linted by markdownlint and the offline link checker only", which is true today
    because `pyproject.toml`'s typos exclude still names `assets/`. When S09 narrows that
    exclude, add `docs/reference/documentation-contract.md` to its table and make the sentence
    name `typos` too; `quality-gates.md`'s "(for `typos` and Ruff)" and
    `configuration.md`'s `pyproject.toml` row stay true.
  - *S09 step 5* adds `sync-python` to `commands.md` "in that page's form": a row in the Setup
    table. The `assets` bullet on `quality-gates.md` ("runs `just sync` and `check-assets`")
    and its `NODE_AUTH_TOKEN` sentence ("sits on the `just sync` step of each job") then need
    the same change; add the page to S09's table.
  - *§11 "per machine"*, repeating S05's note: `scripts/initialize.sh` runs
    `git lfs install --local`, so the pages here say git-lfs is installed once per machine and
    `git lfs install --local` runs in each clone.
  - *The pointer is 133 bytes* (`git cat-file -s HEAD:assets/models/biscuit/model/biscuit-poseable.blend`),
    not the ticket's "130".
- **Deviations from this ticket**, each with the reason:
  - *No ticket ids*, by the maintainer's decision above; "C02 is the ledger" and the like are
    written as the work they name.
  - *`https://` and template delimiters.* The pages never write the scheme, so the
    documentation contract's external-link rule is "any absolute URL, and any `mailto:`", the
    LFS pointer's first line is "the LFS specification's version line", and the committed
    `.npmrc` is described rather than quoted. `pages.yml`'s base-path expression and the token
    expression are written in words, because the validator refuses brace-brace.
  - *`testing.md` lists six files, not "five".* Step 4 says "the five files" and names six
    (`setup.ts` and five `*.test.ts`); the page lists all six and the fixture.
  - *`agent-contract.md`'s example skill* is `asset-change` rather than H's `component-change`,
    which does not exist here; the frontmatter is copied from the real file.
  - *Two fragments retargeted.* H's troubleshooting and commands pages link
    `develop-locally.md#do-not-install-the-hook-from-a-secondary-worktree`; S05's
    `develop-locally.md` has no such heading, so `commands.md` links the page and
    `troubleshooting.md` links `commands.md`'s own heading of that name.
  - *`maintenance.md`'s link section* says that not even `just check-links-online` follows the
    three links from the viewer and the model page to this repository's GitHub files, because
    lychee reads Markdown only; the ticket did not ask for it, and a reader would otherwise
    assume the monthly run covered them.
  - *`troubleshooting.md`'s `npm ci` entry* names both `404 Not Found` (H's consume page: the
    registry lies) and `401 Unauthorized` (what S05's `develop-locally.md` quotes).
  - *Added entries* beyond Step 6's list: "`listed in the manifest but absent`" folded into the
    unlisted-file entry, and "A `.blend` was committed as an ordinary blob" (above).
- **Codex adversarial review** (`--base main`, 2026-09-24): verdict `needs-attention`, two
  medium findings, both confirmed against the script and fixed in the pages with the
  maintainer's agreement (fourth commit); the code changes go to S09 above.
  - *`source` forms documented as enforced* (`asset-manifest.md`): the checker only refuses a
    missing or empty `source`. The page now says the three forms are a convention review
    holds, and `security-model.md` says the tool never checks the field beyond its presence.
  - *`just assets-manifest` said to run the self-test* (`asset-manifest.md`, `commands.md`):
    `write` compares the tree without `self-test`. Both pages now say so and point at
    `just check-assets`.
- **Open points.**
  - *The checker's messages*: settled; the pages follow the script (above).
  - *TypeScript*: `typescript-eslint` 8.66.0 declares `typescript >=4.8.4 <6.1.0` (its
    `peerDependencies` and `SUPPORTED_TYPESCRIPT_VERSIONS`), and the pin 6.0.3 is inside it.
    S00's hand-back names no hold, so H's "held back a major version" sentence was dropped and
    replaced by the checkable one: a TypeScript release at or past 6.1 waits for a linter that
    accepts it.
  - *The viewer and reduced motion*: settled by reading `static/pose-studio/viewer.html`. It
    creates `matchMedia('(prefers-reduced-motion: reduce)')`, starts with auto-rotate off
    (`spin=false`), toggles it by a checkbox and the Space key, and stops it when the query
    changes to `reduce`; it does not refuse a reader who turns it back on. `accessibility.md`
    says exactly that, so the sentence was sharpened rather than weakened. It also says, from
    the same file, that a browser without WebGL 2 gets an error message and disabled controls.
    The `accessibility-review` skill's step 7 still speaks of `data-animations` for the viewer,
    which the embedded page never reads; true of the port that replaces it, not of the file
    today.
  - *Hashes on `large-files.md`*: confirmed; the three large files' sha256 stay in the
    manifest only, and the page gives bytes, storage and reason.

## Open points

- `troubleshooting.md` quotes refusal messages from `scripts/check_assets.py`. If S00's
  script words them differently from CONVENTIONS.md §4, the page follows the script and
  the hand-back says so.
- `maintenance.md` inherits H's sentence about TypeScript being held back a major version
  for the linter. Whether it still applies at the studio's pins is checked against
  `typescript-eslint`'s supported range at `8.66.0` and `typescript` `6.0.3`; keep or drop
  the sentence and say which.
- `accessibility.md` states that the viewer honours reduced motion "on its own terms". D's
  README line 25 says auto-rotate can be toggled and the survey of the file found it
  respects the reduced-motion media query; confirm by reading
  `static/pose-studio/viewer.html` for `prefers-reduced-motion` once S02 has merged, and
  weaken the sentence to "offers a toggle" if the query is absent.
- Whether `large-files.md` should carry the sha256 of the three large files (CONVENTIONS.md
  §1 fact 8) or leave them to the manifest alone. Leave them to the manifest: a hash on a
  prose page is a second copy nothing checks. Confirm this reading.
