---
id: S09
title: "Follow-up: what S00 to S06 handed back to tickets that are done"
status: done
depends_on: [S01, S02, S03, S04, S05, S06]
parallel_with: []
branch: ticket/s09-follow-up-hand-backs
estimated_size: M
---

# S09: Follow-up: what S00 to S06 handed back to tickets that are done

## Context

A ticket that is done or in progress is not reopened (CONVENTIONS.md §9). Instead, each
build ticket's hand-back notes name changes it could not make because the file belonged
to another ticket, or to CONVENTIONS.md, and those changes are collected here. S07 depends
on this ticket, so the fixes are in the first deploy.

Every item below cites where it came from, as `<ticket> hand-back, "<bullet>"`. Read that
bullet in the source ticket's Hand-back notes before acting on it: the notes carry the
evidence, and this ticket only carries the change. The items came from S00, S01, S02, S03
and S04. S05 and S06 were not finished when this ticket was written, so step 1 collects
their items.

Errors in a done ticket's own text (a count in a Verification section, a grep in an
acceptance criterion) are already recorded in that ticket's hand-back notes. They are not
corrected here, because a done ticket's file is a record of what was asked.

This ticket runs after every lane has merged, so it may edit the files CONVENTIONS.md §9
reserves from the lanes (`Justfile`, `pyproject.toml`), the same way S07 and S08 do.

Read first: CONVENTIONS.md §2.1, §2.2, §3, §8, §9, §10 and §11; the Hand-back notes
of S00 to S06; `AGENTS.md`; the `code-review` and `fix-quality` skills.

## Goal

- The home page links to its two routes through `resolve('/model/')` and
  `resolve('/gallery/')`.
- The two skill lines that still describe a game's `docs/specs/` describe the studio.
- The typos check reads `assets/models/biscuit/README.md`, like markdownlint and lychee
  already do.
- The `assets` CI job syncs only the Python environment and carries no registry token.
- CONVENTIONS.md agrees with what S00 to S06 measured.
- The pages S05 owns carry what S00 and S02 handed to them.
- Each item S05 and S06 hand back to a done ticket is either done here or carried forward
  by name.

## Non-goals

- Editing the ticket file of S00 to S08, or any C ticket, except this one's `status:`.
- The gallery thumbnails (S10) and the rebuild's success-path run (S11).
- The licence of the studio's assets (`docs/explanation/content-policy.md` records it as
  open), and whether the packed textures are photo-derived (S02 hand-back, "Whether the
  packed textures are photo-derived": the maintainer does not know). Both are carried
  forward and left unresolved.
- The same `workflow_run` gap in T's `pages.yml` and G's shared workflow (S04 hand-back,
  "Adversarial review, and the gate"). Those belong to other repositories, and a `G` or
  `T` ticket is written only if the maintainer asks for one.
- Installing hooks, pushing, opening the pull request.

## Files touched

| Path | Class | Owner | Change |
| --- | --- | --- | --- |
| `src/routes/+page.svelte` | route | S01 | `resolve('/model/')`, `resolve('/gallery/')`; comment rewritten (step 2) |
| `tests/route.test.ts` | test | S01 | only if step 2 changes what the test can assert; the expected hrefs stay `/model/` and `/gallery/` |
| `.agents/skills/accessibility-review/SKILL.md` | skill | S00 | the introductory paragraph (step 3) |
| `.agents/skills/code-review/SKILL.md` | skill | S00 | step 1 of the procedure (step 3) |
| `pyproject.toml` | repo (no lane) | S00 | `[tool.typos.files] extend-exclude` narrowed (step 4) |
| `Justfile` | repo (no lane) | S00 | a `sync-python` recipe (step 5); the `assets-manifest` comment (step 1b) |
| `.github/workflows/ci.yml` | workflow | S04 | the `assets` job runs `just sync-python` (step 5) |
| `docs/reference/commands.md` | page | S06 | the new recipe (step 5); the `assets-manifest` row (step 1b) |
| `docs/how-to/develop-locally.md` | page | S05 | only what S05 did not land (step 7) |
| `docs/how-to/rebuild-the-model.md` | page | S05 | only what S05 did not land (step 7) |
| `docs/decisions/0006-sources-in-lfs-served-files-as-blobs.md` | page | S05 | only if it does not quote the figure S02 read (step 7); the sentence about the checker and the index (step 1a) |
| `scripts/check_assets.py` | repo (no lane) | S00 | the index-blob check, the `source` form check, and `write` running `self-test` first (steps 1a, 1b) |
| `docs/reference/asset-manifest.md` | page | S06 | the checker as steps 1a and 1b leave it |
| `docs/explanation/large-files.md` | page | S06 | the gate now refuses a `.blend` stored as a blob (step 1a) |
| `docs/operations/troubleshooting.md` | page | S06 | the same (step 1a) |
| `docs/how-to/import-an-asset.md` | page | S05 | the sentence about the checker and the index (step 1a) |
| `docs/explanation/security-model.md` | page | S06 | the `source` field's form is checked (step 1b) |
| `docs/reference/testing.md` | page | S06 | only if it says `write` skips the self-test (step 1b) |
| `docs/reference/documentation-contract.md` | page | S06 | the README is read by `typos` too (step 1c) |
| `docs/reference/quality-gates.md` | page | S06 | the `assets` job and the token's steps (step 1d) |
| `tickets/CONVENTIONS.md` | tickets | shared | the corrections in step 6, and §4 and §11 for steps 1a, 1b and 1e |
| `tickets/S09-follow-up-hand-backs.md` | tickets | this file | `status:` line, hand-back notes |

Step 1 may add rows, for the files that S05's and S06's hand-back items need, before
anything else is edited.

## Steps

1. **Collect S05's and S06's items.** Read both tickets' Hand-back notes. Every item
   addressed to a done ticket, to CONVENTIONS.md or to "a follow-up" is in scope. Add each
   one to this ticket's Steps as a numbered sub-item citing its source, and add its files
   to the table above, in the ticket's first commit and before editing anything else.
   An item that needs a decision the maintainer has not made goes to Open points instead.
   Record in the hand-back notes what was taken and what was left.

   Collected on 2026-09-24. S05 addresses nothing to a follow-up by name; S06 addresses
   six items to S09. The maintainer decided the two that needed a decision (1a's checker
   change and 1b) when this step was written: both are taken.

   1. **1a. The raw `.blend` gap** (S06 hand-back, "The storage-drift claim is false;
      handed to S09."). `git check-attr` reads `.gitattributes`, not how Git stored the
      file, so a `.blend` committed on a machine without git-lfs passes `check-assets`.
      Correct the CONVENTIONS.md §11 bullet (step 6). Close the gap, as the maintainer
      chose: `check_tree` reads, for every path whose attribute storage is `lfs` and which
      the index holds, the index blob through `git cat-file -p :<path>`, and refuses one
      that is not an LFS pointer; an untracked path is skipped, since the index holds
      nothing for it yet. The self-test proves it with `git hash-object -w` and
      `git update-index --add --cacheinfo`, which bypass the filter, so the stage needs no
      git-lfs. Then the pages that say nothing in the gate notices
      (`docs/explanation/large-files.md`, `docs/operations/troubleshooting.md`,
      `docs/reference/asset-manifest.md`), decision 0006's sentence about the index, and
      `docs/how-to/import-an-asset.md`'s, say what the checker now does.
   2. **1b. The Codex review's two code-side findings** (S06 hand-back, "Other items for
      S09", "The Codex review's two code-side findings"). `check` requires `source` to be
      one of the three forms `docs/reference/asset-manifest.md` gives
      (`<repository>@<commit>:<path>`, `rebuilt:<date>`, `studio`), with self-test cases;
      and `write` runs `self-test` before it writes. `docs/reference/asset-manifest.md`,
      `docs/explanation/security-model.md`, `docs/reference/commands.md`'s
      `assets-manifest` row, the `Justfile` comment above `assets-manifest`, and
      `docs/reference/testing.md` if it says `write` skips the self-test, follow.
   3. **1c. The documentation contract names `typos`** (S06 hand-back, "Other items for
      S09", "S09 step 4 changes a sentence here."): once step 4 narrows the exclude,
      `docs/reference/documentation-contract.md`'s sentence that the model's README "is
      linted by markdownlint and the offline link checker only" names `typos` too.
   4. **1d. Quality gates and the `assets` job** (S06 hand-back, "Other items for S09",
      "S09 step 5"): `docs/reference/quality-gates.md`'s `assets` bullet says the job runs
      `just sync-python`, and its `NODE_AUTH_TOKEN` sentence says the token sits on the
      `just sync` step of the `frontend` and `documents` jobs.
   5. **1e. Git LFS per clone** (S06 hand-back, "Other items for S09", "§11 per machine";
      S05 hand-back, Deviations, "Git LFS per clone, not per machine."): CONVENTIONS.md
      §11's bullet says git-lfs is installed once per machine and `git lfs install --local`
      runs in each clone, as the pages already do (step 6, the same bullet as 1a).
   6. **1f. The pointer is 133 bytes** (S06 hand-back, "Other items for S09", "The pointer
      is 133 bytes"): `rg -n '\b130\b' tickets/CONVENTIONS.md docs/ AGENTS.md` finds
      nothing, so only S06's own text says "130". Nothing to change; recorded.
   7. **1g. The LFS figure in 0006** (S05 hand-back, Open points, "The LFS figure in
      0006"): decision 0006 already says 10 GiB, 10 GiB and 0.3%; CONVENTIONS.md §3's 3%
      is step 6's correction. Nothing beyond step 6.
   8. **1h. Written as the design says** (S05 hand-back, "Written as the design says
      rather than as the repository is"): S05's pages were written before S03's routes
      merged. Check the three-route sentences and the model page's "look differs" sentence
      against `src/routes/` and record; edit only if one is false.

   Left, under Open points: the `accessibility-review` skill's step 7 (S06 hand-back, Open
   points, "The viewer and reduced motion"), which the maintainer chose to leave.

2. **Home page links** (S01 hand-back, "To S03": once the routes exist,
   `resolve('/model/')` and `resolve('/gallery/')` "are the form to use, here on the home
   page too"; S03 did not change the home page). In `src/routes/+page.svelte`, replace
   `const home = resolve('/')` and the two `{home}…/` hrefs with two constants initialised
   by `resolve('/model/')` and `resolve('/gallery/')`, or the calls inline. Rewrite the
   comment's second paragraph so that it no longer says the routes do not exist. Keep the
   sentence about element selectors. The navigation lint rule accepts both forms, because
   it checks the leading expression of an `href`. `tests/route.test.ts` keeps expecting
   `/model/` and `/gallery/`. After `BASE_PATH=/biscuit_studio just frontend-build`,
   `build/index.html` must still carry `href="./model/"` and `href="./gallery/"` (S01
   hand-back, "The built `href` is relative").

3. **Two skill lines** (S00 hand-back, "Two skill lines the edit list did not reach").
   In `.agents/skills/accessibility-review/SKILL.md` line 8, the `@guarantee` clauses are
   the platform's, in the Allium modules installed with `@steven-cutting/biscuit-games`
   (`AGENTS.md`, "What this project is"), not in a `docs/specs/appearance.allium` of the
   studio's own. Also, "every game inherits them" becomes "this studio inherits them, as
   every game does". In `.agents/skills/code-review/SKILL.md` step 1, "the specification
   module the change touches" becomes the platform specification that governs the
   surface the change touches. Change nothing else in either file, and leave the bridges
   under `.claude/` and `.codex/` unchanged. Run `just check-agents`.

4. **Typos reads the model's README** (S02 hand-back, "The README was invisible to the
   gate": `pyproject.toml` still excludes `assets/` whole, "left as the belt it is, since
   `pyproject.toml` was not in the authorisation"). Replace the `"assets/"` entry in
   `[tool.typos.files] extend-exclude` with the §2.1 set: the six
   `assets/models/biscuit/<dir>/` paths and `"assets/illustrations/"`. Keep
   `"static/pose-studio/"` and the two lockfiles. Rewrite the comment above the list so it
   says the README and the manifest are read. Then run `just lint`. The typos hook runs
   with `--force-exclude`, so a hook run over the README passes whether or not typos
   read it. Prove the file is read the way S02 proved lychee: append a common misspelling
   (the word "the" with its last two letters swapped) to the README as a scratch edit, run
   `uv run --frozen prek run typos --files assets/models/biscuit/README.md`, and quote the
   finding. The hook also runs with `--write-changes`, so it may rewrite the word and
   report modified files. Then run `git checkout -- assets/models/biscuit/README.md` and
   `just check-assets`, and quote both. If typos flags a word
   in `assets/models/biscuit/README.md`, the README is an asset and is not edited by hand
   (`AGENTS.md` invariant 8), so the repair is a single `extend-words` entry in
   `pyproject.toml` with a comment giving the reason. Record the word in the notes. Then
   check the other five places §2.1 names, plus `.editorconfig`, against the §2.1 table,
   and record any that disagree. Change only `pyproject.toml` here.

5. **A Python-only sync for the `assets` job** (S04 open point, "`just sync` in the
   `assets` job installs `node_modules` it never reads", which names the recipe as "a
   `Justfile` change and an S00 follow-up"). Add a recipe after `sync` in the `Justfile`:

   ```just
   # The Python half of `sync`, for a job that runs only Python recipes. It needs
   # no registry token and installs no node_modules.
   sync-python:
       uv sync --frozen
   ```

   In `.github/workflows/ci.yml`, the `assets` job runs `just sync-python`, and that step
   carries no `env:` and no `NODE_AUTH_TOKEN`. Rewrite the comment above it to match. The
   job id stays `assets`, so neither the required check nor `pages.yml`'s `workflow_run`
   gate changes. Keep the two pinned SHAs and their `# v…` comments unchanged. Add the
   recipe to `docs/reference/commands.md` beside `sync`, in that page's form. Run
   actionlint through `just lint` and `npx prettier --check .github/workflows/`, then
   check that `NODE_AUTH_TOKEN` now occurs twice in `ci.yml` instead of three times.

6. **CONVENTIONS.md corrections.** The maintainer authorised each of these when this
   ticket was written; make them and nothing else:
   - §2.1: the `pyproject.toml` row reads as step 4 leaves the file, with "(corrected by
     S09)".
   - §2.2: one bullet naming the `sync-python` recipe from step 5.
   - §2.4: the `[tool.typos.files]` block as step 4 leaves it.
   - §3 table (S02 hand-back, "Step 10", and S00 hand-back, "Handed to S02"): the viewer is
     27,561,668 bytes after S02's rewrite, `previews/**` holds 22 files, `textures/*.png`
     totals 10,040,783, and `illustrations/good/*.png` totals 15,137,724. Take every figure
     from `assets/manifest.json` again rather than from this line.
   - §3 costs and the §10 LFS claim (S02 hand-back, "The LFS quota figure"): the free tier
     is 10 GiB of storage and 10 GiB of bandwidth a month (GitHub Docs, "About storage and
     bandwidth usage", read 2026-09-23), with metered billing beyond that, so a clone that
     fetches the 32.3 MB spends about 0.3% of a month's bandwidth. In §10, mark the claim
     as failed and corrected.
   - §8: the `assets` job runs `sync-python`, and `NODE_AUTH_TOKEN` sits on the `just sync`
     step of the other two jobs.
   - §10: after each claim assigned to S00 to S04, add one clause giving its outcome and
     the hand-back that settled it. The claim about importing PNG files from outside
     `src/` failed for `vite dev`, and `server.fs.allow: ['assets']` in `vite.config.ts` is
     the correction (S03 hand-back, "The four CONVENTIONS §10 claims"). The
     `document.title` claim held (S01 hand-back, "`document.title` under jsdom"). Leave
     the claims assigned to S07 as they are.
   - §11, "The gallery page is heavy": replace "thumbnails are an open point on S03" with
     "thumbnails are S10", and give the measured 15,141,024 bytes (S03 hand-back,
     "Browser check").
   - §2.7 (S01 hand-back, "To S00 or CONVENTIONS.md"): this said §2.7 described the page
     reaching `base`. When this ticket was written, `grep -nw base tickets/CONVENTIONS.md`
     found `base` only in §0 and §2.5 (`paths.base`, which stays true). Check again and
     correct §2.7 only if it still describes `base`. Record which.
   - Added on 2026-09-24 with the maintainer's authorisation, each marked "(corrected by
     S09)": §2.2's `assets-manifest` comment reads as the `Justfile` has it since S05's
     sixth commit (it keeps `patched` too and reads the viewer's `source_sha256` from its
     build record); §4's `check`, `write` and `self-test` bullets say what steps 1a and 1b
     add; §11's `git lfs install` bullet says per clone, and that the checker refuses a
     `.blend` whose index blob is not a pointer (steps 1a and 1e).

7. **S05's pages** (S00 hand-back, "`git lfs install --local` in a secondary worktree"
   and "The gate reads the index, not the worktree"; S02 hand-back, "`scripts/rebuild_model.sh`
   deviates from the embedded text", and "The LFS quota figure"). S05 was asked to read
   those notes, so check its pages before editing them:
   - `docs/how-to/develop-locally.md` must say that `prek run --all-files` lints only the
     files `git ls-files` reports, so a new file is invisible to `just lint` until it is
     staged. It must also say that in a secondary worktree, `git lfs install --local`
     writes to the repository's shared `.git/config` and `.git/hooks`, like
     `just install-hooks`, which is why hooks are installed from the primary checkout only.
   - `docs/how-to/rebuild-the-model.md` must say that the script refuses to start unless
     `assets/` and `static/pose-studio/` match `HEAD`. It must also say that on failure or
     interruption the script restores both from `HEAD` and removes what the run created,
     and that it purges `__pycache__` and `*.blend1` under the package.
   - Decision 0006 must quote 10 GiB and 10 GiB, with the date, if it quotes a figure.

   Add a missing sentence in the page's own register. Do not rewrite what S05 wrote.

8. **Maintainer action** (S00 hand-back, "`just install-hooks` was not run"). When this
   ticket was written, the primary checkout's `.git/hooks` held only git-lfs's four hooks
   and no pre-commit hook. Ask the maintainer to run `just install-hooks` from
   `~/projects/biscuit_studio`, not from this worktree. Record their answer, and
   `ls .git/hooks` afterwards if they ran it.

9. Run the verification, fill in the hand-back notes, set `status: done`, and commit.
   Pushing and the pull request are authorised separately.

## Acceptance criteria

- [ ] `grep -c "resolve('/model/')\|resolve('/gallery/')" src/routes/+page.svelte` prints
      `2` or more, and `grep -c "const home" src/routes/+page.svelte` prints `0`.
- [ ] `build/index.html` after `BASE_PATH=/biscuit_studio just frontend-build` carries
      `href="./model/"` and `href="./gallery/"`.
- [ ] `grep -c 'docs/specs/appearance.allium' .agents/skills/accessibility-review/SKILL.md`
      prints `0`, and `just check-agents` is green.
- [ ] `pyproject.toml`'s typos exclude no longer holds `"assets/"`. The scratch
      misspelling in step 4 was reported, the README was restored, and `just check-assets`
      is green afterwards.
- [ ] `just --summary` lists `sync-python`, the `assets` job in `ci.yml` runs it,
      `grep -c NODE_AUTH_TOKEN .github/workflows/ci.yml` prints `2`, and
      `docs/reference/commands.md` names the recipe.
- [ ] CONVENTIONS.md carries each correction in step 6, and nothing else in it changed
      (`git diff main -- tickets/CONVENTIONS.md` shows only those hunks).
- [ ] Each S05 page check in step 7 is either true of `main` before this ticket or made
      true by it, and the notes say which.
- [ ] Every item step 1 collected is done or listed under Open points.
- [ ] No file of S00 to S08's tickets or the C tickets changed.
- [ ] `just check` is green.

## Verification

```sh
just frontend-static
just frontend-unit
BASE_PATH=/biscuit_studio just frontend-build
grep -o 'href="\./\(model\|gallery\)/"' build/index.html
just check-agents
uv run --frozen prek run typos --files assets/models/biscuit/README.md; echo "rc=$?"
git status --short assets/
just --summary | tr ' ' '\n' | grep -x sync-python
grep -c NODE_AUTH_TOKEN .github/workflows/ci.yml
just check-docs
git diff main --stat
git diff main --stat -- 'tickets/S0*' 'tickets/C0*'
just check
```

Expected: the first three exit 0. The grep prints `href="./model/"` and
`href="./gallery/"`. `check-agents` validates eight skills. `rc=0` on the restored README, and an empty
`git status` under `assets/`. `sync-python`. `2`.
`check-docs` validates thirty-nine pages. The first stat names only files from the table
(including any rows step 1 added). The second stat shows only this ticket. `just check`
ends green with the worktree unchanged.

## Hand-back notes

Executed on 2026-09-24 on the Supacode worktree branch `S09-follow-up-hand-backs`, not the
`ticket/s09-follow-up-hand-backs` the `branch:` field names, as every ticket since S00 has
been (nothing in the checks reads the branch name). Nine commits; the first touched only
this file, as step 1 requires. Pushing and the pull request were not done and are asked
for separately.

**Step 1, what was taken and what was left.** S05 addresses nothing to a follow-up by
name; its Deviations bullet "Git LFS per clone, not per machine" and its Open point "The LFS
figure in 0006" were taken as 1e and 1g. S06 addresses six items to S09: 1a, 1b, 1c, 1d, 1e
and 1f, all taken; its Open point about the `accessibility-review` skill's step 7 was left,
by the maintainer's choice, and is under Open points. The maintainer chose to take 1a's
checker change and both of 1b's when asked at the start, so no item needed a decision
afterwards. Item 1h was checked and needed no edit: `src/routes/` holds `/`, `/model/` and
`/gallery/`, and the model page says beside the download that the GLB's PBR materials look
different from the studio's cel shading, so `develop-locally.md`, `first-change.md`,
`deploy-to-github-pages.md`, `rebuild-the-model.md` and decision 0008 are true as written.

**Step 2.** `src/routes/+page.svelte` holds `const model = resolve('/model/')` and
`const gallery = resolve('/gallery/')`, the two anchors take them whole, and the comment's
second paragraph now says the links are resolved against the routes that exist; the
sentence about element selectors is kept. `tests/route.test.ts` is unchanged and its
`/model/` and `/gallery/` expectations pass. `svelte-check`, ESLint and Prettier accept the
form. The build under `BASE_PATH=/biscuit_studio` carries `href="./model/"` and
`href="./gallery/"`, quoted below.

**Step 3.** The two lines only. `accessibility-review` line 8 now reads "The `@guarantee`
clauses in the platform's Allium modules, installed with `@steven-cutting/biscuit-games`,
are the acceptance criteria, not aspirations, and this studio inherits them, as every game
does." `code-review` step 1 reads "the platform specification that governs the surface the
change touches". The sixteen bridges are untouched; `check-agents` validated 8 skills.

**Step 4.** `pyproject.toml`'s typos exclude names the six package directories and
`assets/illustrations/`, keeps `static/pose-studio/` and the two lockfiles, and its comment
says the README and the manifest are read. `just lint` passed. Proof: with the word "the"
appended to the README with its last two letters swapped (spelled out here, the hook would
rewrite it), `uv run --frozen prek run typos --files assets/models/biscuit/README.md`
printed `typos ... Failed`, `- hook id: typos`, `- files were modified by this hook`, exit
1, and `git diff --stat` showed the README with 2 insertions (the hook runs with
`--write-changes`, so it rewrote the word rather than naming it). `git checkout --
assets/models/biscuit/README.md` exited 0, `git status --short assets/` was empty, and
`just check-assets` printed `check_assets check: ok`. Typos flagged no word in the README
or in `assets/manifest.json` (both run through the hook: `Passed`), so no `extend-words`
entry was needed. The other five §2.1 places and `.editorconfig` agree with the §2.1 table
as it stood, and `.pre-commit-fix.yaml` carries the same `(?x)` block as the gate.

**Step 5.** `sync-python` sits after `sync` in the `Justfile` with the ticket's comment.
The `assets` job runs it with no `env:`; its comment says the job needs no node_modules
and no registry token, without naming the variable, so `NODE_AUTH_TOKEN` occurs twice in
`ci.yml`. The two SHAs and their `# v…` comments are unchanged. `commands.md` has a
`just sync-python` row under Setup. For 1d, `quality-gates.md`'s `assets` bullet names
`sync-python`, and its token sentence names the `frontend` and `documents` jobs. actionlint
and check-yaml passed in the hook run; `npx prettier --check .github/workflows/` printed
"All matched files use Prettier code style!".

**Steps 1a and 1b, the checker.** `scripts/check_assets.py`: `index_findings` runs
`git ls-files -z` over every path whose attribute storage is `lfs` and `git cat-file blob
:<path>` over each the index holds, and refuses one whose blob is not an LFS pointer with
"the index holds the file itself, not an LFS pointer; run git lfs install --local, then git
rm --cached and git add it"; `entry_findings` refuses a `source` outside the three forms
(`SOURCE`, a regex; the message names the forms); `main` runs `self_test` before `write`
as well as before `check`, and writes nothing if it fails. The self-test gained
`self_test_index` (a raw blob and then the pointer bytes put into the index through
`git hash-object -w --stdin` and `git update-index --add --cacheinfo`, so no LFS filter is
involved and the outcome does not depend on the machine) and `self_test_source` (`unknown`
refused; the import, `rebuilt:` and `studio` forms accepted, ending on `studio` so the
stage is left as `write` wrote it). `just check-assets` and `check_assets.py write` both
print `ok` on the real tree, and `write` left `assets/manifest.json` unchanged. Ruff lint
and format pass. The pages now say what the checker does: `asset-manifest.md` (the
`source` forms, the `check` and `write` paragraphs, two new reasons in the table, the
self-test list, and "It sees how a file was stored only once it is in the index" in place
of "It does not see how a file was stored"), `large-files.md` and `troubleshooting.md`
(the gate refuses a raw `.blend` from the first run after `git add`; the `git lfs
ls-files` and `git cat-file -s` diagnostics and the repair are kept), `security-model.md`
(`source` checked for form, not truth), `commands.md`'s `assets-manifest` row and the
`Justfile` comment above it (the self-test runs first), `testing.md` (the two new
self-test cases; both subcommands self-test first), `import-an-asset.md` step 4, and
decision 0006's sentence about the index. CONVENTIONS.md §4 says the same.

**Step 6.** Every correction in the list, each marked "(corrected by S09)" or citing S09,
plus the three the maintainer authorised on the day (§2.2's `assets-manifest` comment, §4
for the checker, §11 for 1a and 1e). The §3 figures were read from `assets/manifest.json`
again on the day: viewer 27,561,668; `textures/*.png` 36 files, 10,040,783; `previews/**`
22 files, 9,754,946 (the ticket's "about 9.1 MB" replaced by the manifest's total);
`illustrations/good/*.png` 11 files, 15,137,724; LFS objects 32,281,033 in all. §10: one
outcome clause after each claim assigned to S00 to S04, citing the hand-back; the four S07
claims are untouched. **§2.7 check:** `grep -nw base tickets/CONVENTIONS.md` finds `base`
at lines 67 (§0), 495 and 506 (§2.5, `paths.base`), 662 (§3, `miami-angular-base`) and 938
(§9, `--base main`); none in §2.7, so §2.7 is unchanged and S01's note described a
sentence that was not there. `git diff main -- tickets/CONVENTIONS.md` holds only these
hunks.

**Step 7, what S05 had already landed.** All of it. `develop-locally.md` carries "The gate
reads the index, not the worktree" with `git ls-files` and the staging sentence, and "The
hook is installed only from the primary checkout" with the shared `.git/hooks` and the
`git lfs install --local` writing to the shared `.git/config`. `rebuild-the-model.md`
carries the clean-tree precondition ("What it needs" and step 1), the restore on failure
or interruption, and the `__pycache__` and `.blend1` purge (step 4). Decision 0006 quotes
10 GiB and 10 GiB with the date 2026-09-23. Nothing was added for step 7; 0006's one edit
is 1a's.

**Step 8.** Asked at the start; the maintainer said they would run `just install-hooks`
from `~/projects/biscuit_studio` and did so during this ticket: the first commit here
already ran the gate as a hook. `ls ~/projects/biscuit_studio/.git/hooks`, samples
omitted, afterwards:

```text
post-checkout
post-commit
post-merge
pre-commit
pre-push
```

**Verification output**, run in order after the last content commit:

```text
$ just frontend-static
1790307411204 COMPLETED 426 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS
rc=0
$ just frontend-unit
 Test Files  5 passed (5)
      Tests  20 passed (20)
$ BASE_PATH=/biscuit_studio just frontend-build
  Wrote site to "build"
  done
$ grep -o 'href="\./\(model\|gallery\)/"' build/index.html
href="./model/"
href="./gallery/"
$ just check-agents
Validated AGENTS.md, 2 adapters, and 8 skills.
$ uv run --frozen prek run typos --files assets/models/biscuit/README.md; echo "rc=$?"
typos....................................................................Passed
rc=0
$ git status --short assets/
(no output)
$ just --summary | tr ' ' '\n' | grep -x sync-python
sync-python
$ grep -c NODE_AUTH_TOKEN .github/workflows/ci.yml
2
$ just check-assets
check_assets check: ok
$ just check-docs
Validated 39 pages and 40 canonical topics.
$ git diff main --stat
 .agents/skills/accessibility-review/SKILL.md       |   2 +-
 .agents/skills/code-review/SKILL.md                |   2 +-
 .github/workflows/ci.yml                           |  11 +-
 Justfile                                           |  14 ++-
 .../0006-sources-in-lfs-served-files-as-blobs.md   |   6 +-
 docs/explanation/large-files.md                    |  11 +-
 docs/explanation/security-model.md                 |   4 +-
 docs/how-to/import-an-asset.md                     |   6 +-
 docs/operations/troubleshooting.md                 |  17 +--
 docs/reference/asset-manifest.md                   |  50 ++++----
 docs/reference/commands.md                         |   3 +-
 docs/reference/documentation-contract.md           |   4 +-
 docs/reference/quality-gates.md                    |   8 +-
 docs/reference/testing.md                          |  20 ++--
 pyproject.toml                                     |  13 ++-
 scripts/check_assets.py                            | 126 +++++++++++++++++++--
 src/routes/+page.svelte                            |  23 ++--
 tickets/CONVENTIONS.md                             | 116 +++++++++++++------
 tickets/S09-follow-up-hand-backs.md                |  79 ++++++++++++-
 19 files changed, 385 insertions(+), 130 deletions(-)
$ git diff main --stat -- 'tickets/S0*' 'tickets/C0*'
 tickets/S09-follow-up-hand-backs.md | 79 +++++++++++++++++++++++++++++++++++--
 1 file changed, 75 insertions(+), 4 deletions(-)
```

Every file in the first stat is in the table.

**For the next follow-up** (found here, belonging to tickets that are done, not fixed
outside this table):

- S03's ticket file ends with leftover template bullets under its Hand-back notes (one
  says "The three CONVENTIONS.md §10 claims assigned here" while the executed notes cover
  four). A record, not a defect; noted so nobody reads them as findings.
- `docs/how-to/develop-locally.md` has no heading
  `do-not-install-the-hook-from-a-secondary-worktree`; S06 retargeted the two links that
  named it (S06 hand-back, Deviations, "Two fragments retargeted"). Nothing is broken; if
  the page ever grows that heading, the links can point at it again.

**`just check`:** run after the notes were written, before the final commit: every recipe
passed and it ended with `All checks passed and the worktree is unchanged.`

## Open points

- **The licence** and **whether the packed textures are photo-derived** remain open
  (S02 hand-back). Nothing here resolves them.
- **The `workflow_run` gap in T and G** (S04 hand-back). Ask the maintainer whether a `G`
  or `T` ticket should be written. Recommend asking once S07 has proved the gate on the
  studio's first deploy.
- **The `accessibility-review` skill's step 7** (S06 hand-back, Open points, "The viewer
  and reduced motion") speaks of `data-animations` for the viewer, which the embedded page
  never reads; it is true of the port that replaces it. The maintainer chose on
  2026-09-24 to leave it, so step 3 changes nothing else in the file. For the next
  follow-up if the viewer is ported before the port's own ticket rewrites the skill.
- **Whether `just check-assets` needs a sync at all** in CI. `uv run --frozen` builds the
  environment on first use, so the job might run without `sync-python`. Keep the explicit
  recipe, because a job that names its setup is easier to read than one relying on
  `uv run`'s side effect, and say so if the maintainer asks.
