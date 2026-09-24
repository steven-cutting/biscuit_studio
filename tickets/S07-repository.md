---
id: S07
title: "Repository: create it, bootstrap its settings, first push, first deploy"
status: open
depends_on: [S01, S02, S03, S04, S05, S06]
parallel_with: []
branch: ticket/s07-repository
estimated_size: M
---

# S07: Repository: create it, bootstrap its settings, first push, first deploy

## Context

Every lane has merged to `main` and `just check` is green there, but the repository still
exists only as a local clone: no remote, and `gh repo view steven-cutting/biscuit_studio`
answers `Could not resolve to a Repository`. This ticket makes the GitHub repository,
applies the settings no file can carry, pushes `main` once, and proves the three checks
and the Pages deployment with the first runs. CONVENTIONS.md §1 decision 6 fixes the
address — a public repository, a project Pages site at
`https://steven-cutting.github.io/biscuit_studio/`, `BASE_PATH=/biscuit_studio` — and §8
fixes the settings: Pages source `workflow`, protection on `main` requiring `frontend`,
`documents` and `assets`, private vulnerability reporting on.

The settings are applied with `scripts/bootstrap_repo.sh`, T's script copied verbatim by
S00 (`/Users/scutting/projects/biscuit_games_template/scripts/bootstrap_repo.sh`, 382
lines; T `README.md` lines 130-160, "Bootstrap a repository"). Its `--checks` default is a
game's `ci / frontend,ci / documents,ci / stories` (line 37), which is why this ticket
passes `--checks frontend,documents,assets`: the studio's `ci.yml` is bespoke (S04), and a
check's context is the job id. What the script does, what each step reads and mutates,
and what its dry run prints are in T `tickets/C03-repository-bootstrap.md` lines 174-259
(the six steps) and 444-747 (what actually happened when it ran). Three facts from that
record shape the order below:

- **The Pages source must be `workflow` before `deploy-pages` runs**, or the build job
  succeeds and the deploy job fails with `Failed to create deployment (status: 404)` (T
  C03 lines 18-26). The `POST /repos/{owner}/{repo}/pages` with `build_type=workflow` was
  accepted on a repository with no commits (T C03 lines 625-629, "C01 had already accepted
  the same POST on a repository with no commits"), so the source can be set between
  creating the repository and the first push.
- **Branch protection needs the branch to exist** (T C03 line 258, "The branch must exist
  before protection can be set"), so the script's protection step can only succeed after
  the first push. Protection before or after the owner's own push blocks nothing:
  administrators are not bound (T C03 lines 350-352).
- **No package grant is needed.** `@steven-cutting/biscuit-games` is public, and every
  workflow installs it with the run's own token (T C03 lines 648-656). The script still
  prints its step 5, because nothing can read the setting back.

So the order is: create the repository empty; set the Pages source with the one API call
the script's step 1 would make; push; run the script with `--apply` for everything else;
run it again to prove `changed: 0`.

Git LFS: `git lfs install` (which S00's `scripts/initialize.sh` runs) installs a pre-push
hook that uploads the objects a push references, so the three LFS files (§3) travel with
the first `git push`. GitHub enables LFS on every repository by default. `git lfs push
--all origin main` afterwards is a no-op that confirms it, and a fresh clone on a machine
with git-lfs is the proof.

Every action that touches GitHub below is marked **Authorisation required**: creating the
repository, setting the Pages source, pushing, each `--apply`, and the optional hygiene
settings. Read-only `gh api` GETs, `gh run list`, `gh run watch`, `curl` and the script's
dry run are not (CONVENTIONS.md §9). The `gh` login is `steven-cutting` with `repo` and
`workflow` scopes (§0), which is what every call below needs.

Read first: CONVENTIONS.md §0, §1 (decision 6, facts 3, 4), §3, §8, §9, §10 (the six
claims assigned to S07), §11. T `README.md` lines 130-160 and T C03 whole. This
repository's `scripts/bootstrap_repo.sh` (its usage is lines 12-18), `.github/workflows/`
(S04), `assets/manifest.json` (the viewer's and the GLB's `sha256`, which step 8 compares
against what Pages serves), `docs/how-to/deploy-to-github-pages.md` (S05).

## Goal

- `steven-cutting/biscuit_studio` exists, public, with `main` pushed from this clone and
  the three LFS objects uploaded.
- Pages source `workflow`; `main` protected requiring `frontend`, `documents` and
  `assets` (strict false, no review, no force push, no deletion, administrators unbound);
  private vulnerability reporting on; a second `--apply` prints `changed: 0`.
- The first `CI` run is green on all three jobs and the first `Deploy to GitHub Pages`
  run is green; `https://steven-cutting.github.io/biscuit_studio/` answers `200`, the
  model page links the pose studio, and the viewer and the GLB are served byte-identical
  to the manifest.
- A fresh clone receives the real `.blend`.
- Every GitHub action was authorised before it happened and is recorded in the hand-back
  table.

## Non-goals

- `README.md`, `CHANGELOG.md`, `AGENTS.md`'s provenance: S08.
- A custom domain, a tag, a release, filing any ticket as an issue.
- A Chromatic project or token (`--chromatic-token-stdin` is never passed; §1 decision
  10).
- Changing any file in this repository other than this ticket. If a run fails on
  something a file caused, the fix is a follow-up on `main` through a pull request, not a
  push to `main` from here, and this ticket records it.
- Touching H, P, T, G, D or a game.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `steven-cutting/biscuit_studio` (repository, no file) | GitHub | `gh repo create` | created, public |
| `steven-cutting/biscuit_studio` (settings, no file) | GitHub | `scripts/bootstrap_repo.sh`, one API call | Pages source, protection on `main`, vulnerability reporting; optionally hygiene |
| `.git/config` (local, not committed) | local | `git remote add` | `origin` added |
| `tickets/S07-repository.md` | ticket | this file | `status:` line, hand-back notes |

The table is the whole scope. No tracked file other than this ticket changes.

## Steps

Work from the repository root. This ticket's own commit (the status line and the notes)
lands on `ticket/s07-repository` and reaches `main` through a pull request like every
other ticket; the steps below act on `main` as it stands after S01 to S06 merged.

### Step 1: Confirm the starting state

```sh
git branch --show-current
git status --short | wc -l
git log --oneline | head -3
git remote -v | wc -l
gh repo view steven-cutting/biscuit_studio 2>&1 | head -1
git lfs ls-files --long
git lfs env | grep -E '^(git-lfs|Endpoint)'
just check
```

Expected: `main`; `0`; the merge commits of the six lanes; `0` (no remote); `GraphQL:
Could not resolve to a Repository with the name 'steven-cutting/biscuit_studio'`; three
LFS files; a git-lfs version and no endpoint yet; `just check` green. If a remote or the
repository already exists, stop: the maintainer created it by hand, and the steps below
assume they did not.

Also confirm the lanes' statuses: every `tickets/S0[1-6]-*.md` has `status: done`.

### Step 2: Dry-run the bootstrap against a repository that does not exist yet

```sh
scripts/bootstrap_repo.sh steven-cutting/biscuit_studio --checks frontend,documents,assets; echo "rc=$?"
```

The script reads with `gh api`, and every read answers `404` on a repository that does
not exist. Record what it prints: a `404` read as "no Pages site", "not protected" and
"false" is the script treating absence as a state (T C03 lines 196-198 and 682-685), and
the run should still end `changed: 0 (dry run; 3 would change)` with `rc=0`. If it aborts
instead, note it; the real dry run is step 5, after the repository exists.

### Step 3: Create the repository

**Authorisation required:** creating a public repository on GitHub. Stop and ask, then:

```sh
gh repo create steven-cutting/biscuit_studio --public --description "The Biscuit Games studio: the models, renders and illustrations behind the games, and the site that shows them."
git remote add origin git@github.com:steven-cutting/biscuit_studio.git
gh repo view steven-cutting/biscuit_studio --json name,visibility,defaultBranchRef --jq '[.name, .visibility, .defaultBranchRef.name] | join(" ")'
```

Expected: the repository URL; then `biscuit_studio PUBLIC` with an empty default branch
(no commits yet). Created empty rather than with `--source . --push`, so the Pages source
can be set before any workflow runs. The description is `package.json`'s
(CONVENTIONS.md §2.3). SSH because `gh auth status` reports `Git operations protocol:
ssh` (§0); if the push in step 6 is refused for a key reason, `gh repo set-default` and
`https://` are the fallback, recorded.

### Step 4: Set the Pages source before anything deploys

**Authorisation required:** enabling GitHub Pages. Stop and ask, then the one call the
script's step 1 makes on a repository with no site (T C03 line 206):

```sh
gh api -X POST repos/steven-cutting/biscuit_studio/pages -f build_type=workflow
gh api repos/steven-cutting/biscuit_studio/pages --jq '[.build_type, .html_url] | join(" ")'
```

Expected: a JSON body; then `workflow https://steven-cutting.github.io/biscuit_studio/`.
If the `POST` answers `409`, a site exists: `PUT` the same body instead. If it answers
`422` asking for a source, send
`{"build_type": "workflow", "source": {"branch": "main", "path": "/"}}` with `--input -`
(the fallback T C03 step 2 gives) and record that it was needed. Setting it here, rather
than through the script after the push, is what lets the first push's `Deploy to GitHub
Pages` run succeed; the script reports `already` for this step from now on.

### Step 5: The real dry run

Read-only, no authorisation:

```sh
scripts/bootstrap_repo.sh steven-cutting/biscuit_studio --checks frontend,documents,assets
```

Expected: step 1 `state: workflow`, `already`; step 2 `state: not protected (HTTP 404)`
with `wanted: false assets,documents,frontend false false false false false` (the script
sorts the names) and the `PUT` it would make; step 3 `skipped: no token supplied`; step 4
`state: false` and the `PUT` it would make; step 5 the package note; step 6 `skipped:
--hygiene not given`; `changed: 0 (dry run; 2 would change)`; `rc=0`.

### Step 6: Push `main`

**Authorisation required:** the first push. Stop and ask, then:

```sh
git push -u origin main
git lfs push --all origin main
git lfs ls-files --long
```

Expected: the push prints the LFS upload progress for three objects before the git
objects (the pre-push hook), then `main -> main`; `git lfs push --all` finds nothing left
to upload; the three files are still listed. If the push is refused with an LFS error
(`batch response`, `Repository or object not found`), LFS is not enabled on the
repository, which GitHub does by default: read `gh api repos/steven-cutting/biscuit_studio
--jq .has_lfs` if the field exists, record it, and stop rather than pushing the objects
some other way.

The push starts two runs: `CI` and `Deploy to GitHub Pages`.

### Step 7: Apply the rest of the bootstrap, twice

**Authorisation required:** changing the repository's settings. Stop and ask, then:

```sh
scripts/bootstrap_repo.sh steven-cutting/biscuit_studio --checks frontend,documents,assets --apply
scripts/bootstrap_repo.sh steven-cutting/biscuit_studio --checks frontend,documents,assets --apply
```

Expected, first run: step 1 `already`; step 2 `+ gh api -X PUT
repos/steven-cutting/biscuit_studio/branches/main/protection --input -`; step 4 `+ gh api
-X PUT repos/steven-cutting/biscuit_studio/private-vulnerability-reporting` (the
repository is public, so the endpoint answers rather than `404`); `changed: 2`. Second
run: `already` on every step that reads, `skipped` on 3 and 6, no line beginning `+`,
`changed: 0`. The second run is the idempotency check, and it is separately authorised
because `--apply` is; ask for both together, as one action with a stated second run.

`--hygiene` (delete branch on merge, wiki off, projects off; T C03 step 6) is a separate
**Authorisation required** choice. Offer it; if the maintainer wants it, add `--hygiene`
to a third `--apply` and record `changed: 1`, then a fourth for `changed: 0`. T C03's
hand-back notes that `delete_branch_on_merge` deletes a merged branch, which matters to
any automation that expects one to survive; nothing here does.

Read back:

```sh
gh api repos/steven-cutting/biscuit_studio/branches/main/protection --jq '[.required_status_checks.strict, ([.required_status_checks.checks[].context] | sort | join(",")), .enforce_admins.enabled, .allow_force_pushes.enabled, .allow_deletions.enabled, (.required_pull_request_reviews != null), (.restrictions != null)] | map(tostring) | join(" ")'
gh api repos/steven-cutting/biscuit_studio/private-vulnerability-reporting --jq .enabled
gh secret list -R steven-cutting/biscuit_studio
```

Expected: `false assets,documents,frontend false false false false false`; `true`;
nothing. The `app_id` on each check is `null` until a workflow has reported under it,
then GitHub's (`15368`); T C03 lines 676-680 record the same and that it does not affect
matching.

### Step 8: The first runs, and what they served

```sh
gh run list -R steven-cutting/biscuit_studio --limit 5
gh run watch -R steven-cutting/biscuit_studio --exit-status "$(gh run list -R steven-cutting/biscuit_studio --workflow CI --limit 1 --json databaseId --jq '.[0].databaseId')"
gh run watch -R steven-cutting/biscuit_studio --exit-status "$(gh run list -R steven-cutting/biscuit_studio --workflow 'Deploy to GitHub Pages' --limit 1 --json databaseId --jq '.[0].databaseId')"
gh run view -R steven-cutting/biscuit_studio "$(gh run list -R steven-cutting/biscuit_studio --workflow 'Deploy to GitHub Pages' --limit 1 --json databaseId --jq '.[0].databaseId')" --log | grep -i 'BASE_PATH' | head -3
gh api repos/steven-cutting/biscuit_studio/environments --jq '.environments[].name'
```

Expected: `CI` `success` with jobs `frontend`, `documents`, `assets`; `Deploy to GitHub
Pages` `success`; `BASE_PATH: /biscuit_studio` (this settles the §10 claim that
`github.event.repository.name` keeps the underscore); `github-pages`, created by the
first deploy. If the deploy failed with `status: 404`, step 4 did not take: fix it, then
`gh run rerun` the deploy run (**Authorisation required**, it is a deployment) and record
it. If `CI` failed, the log names the recipe; the fix is a follow-up on `main` through a
pull request (Non-goals), and this ticket waits for it.

Then what Pages serves, compared with the manifest:

```sh
curl -sI https://steven-cutting.github.io/biscuit_studio/ | head -1
curl -s https://steven-cutting.github.io/biscuit_studio/ | grep -o '<title>[^<]*</title>'
curl -s https://steven-cutting.github.io/biscuit_studio/model/ | grep -c 'pose-studio/viewer.html'
curl -sL https://steven-cutting.github.io/biscuit_studio/pose-studio/viewer.html | shasum -a 256
curl -sL https://steven-cutting.github.io/biscuit_studio/pose-studio/model/biscuit-poseable.glb | shasum -a 256
curl -sI https://steven-cutting.github.io/biscuit_studio/pose-studio/previews/pose-overview.jpg | head -1
uv run --frozen python -c "import json; m={e['path']: e['sha256'] for e in json.load(open('assets/manifest.json'))['assets']}; print(m['static/pose-studio/viewer.html']); print(m['static/pose-studio/model/biscuit-poseable.glb'])"
```

Expected: `HTTP/2 200`; `<title>Biscuit Studio</title>`; a count of at least `1`; two
digests that equal the two the manifest prints, in that order (the GLB's is
`51d16c1826b2c3ad6ad85fcb176a73e0d1c7a0ac3665ad10f1b6700e9e9be716`, CONVENTIONS.md §1
fact 8; the viewer's is S02's post-rewrite digest); `HTTP/2 200`. The two digest matches
settle the §10 claims that the Pages actions accept a 26 MB and a 16 MB file and serve
them unchanged. Pages can take a minute after the run to serve the new content; retry
`curl` rather than reading a `404` as failure inside that minute.

### Step 9: A fresh clone receives the objects

```sh
rm -rf ai_tmp/clone
git clone git@github.com:steven-cutting/biscuit_studio.git ai_tmp/clone
git -C ai_tmp/clone lfs ls-files --long
shasum -a 256 ai_tmp/clone/assets/models/biscuit/model/biscuit-poseable.blend
stat -f %z ai_tmp/clone/assets/models/biscuit/model/biscuit-poseable.blend
rm -rf ai_tmp/clone
```

Expected: the clone fetches three LFS objects; the digest is
`95d164730e9354ab3d9bd561a73180690bbb055fffa9bf230c735f735234b4c3` and the size
`12004899`. A digest of a 130-byte pointer means the objects did not upload in step 6.
`ai_tmp/` is gitignored; the clone is removed either way.

### Step 10: Commit, notes, status

On `ticket/s07-repository`, fill in the hand-back notes including the authorisation
table, set `status: done`. Opening the pull request is separately authorised; it will be
the first pull request behind the three required checks, which is the last proof this
ticket gives.

## Acceptance criteria

- [ ] `gh repo view steven-cutting/biscuit_studio --json visibility --jq .visibility`
      prints `PUBLIC`, and `git remote get-url origin` prints the repository.
- [ ] `gh api repos/steven-cutting/biscuit_studio/pages --jq .build_type` prints
      `workflow`, and `.html_url` is `https://steven-cutting.github.io/biscuit_studio/`.
- [ ] The protection read in step 7 prints
      `false assets,documents,frontend false false false false false`.
- [ ] Private vulnerability reporting reads `true`; `gh secret list` prints nothing.
- [ ] The second `--apply` printed `changed: 0` with no line beginning `+`.
- [ ] The first `CI` run and the first `Deploy to GitHub Pages` run are `success`, and
      the deploy log shows `BASE_PATH: /biscuit_studio`.
- [ ] `curl -sI` of the site root answers `200`; the viewer's and the GLB's served
      digests equal the manifest's.
- [ ] A fresh clone's `.blend` has the fact-8 digest and `12004899` bytes.
- [ ] Every `gh repo create`, `POST /pages`, `git push`, `--apply` and (if taken)
      `--hygiene` was authorised before it happened and appears in the hand-back table.
- [ ] No tracked file other than this ticket changed.

## Verification

Read-only, after the steps:

```sh
gh repo view steven-cutting/biscuit_studio --json name,visibility --jq '[.name, .visibility] | join(" ")'
gh api repos/steven-cutting/biscuit_studio/pages --jq '[.build_type, .html_url] | join(" ")'
gh api repos/steven-cutting/biscuit_studio/branches/main/protection --jq '[.required_status_checks.checks[].context]'
gh api repos/steven-cutting/biscuit_studio/private-vulnerability-reporting --jq .enabled
gh run list -R steven-cutting/biscuit_studio --limit 4
curl -sI https://steven-cutting.github.io/biscuit_studio/ | head -1
scripts/bootstrap_repo.sh steven-cutting/biscuit_studio --checks frontend,documents,assets
```

Expected: `biscuit_studio PUBLIC`; `workflow https://steven-cutting.github.io/biscuit_studio/`;
`["frontend","documents","assets"]` (in the order sent); `true`; `CI` and `Deploy to
GitHub Pages` both `success`; `HTTP/2 200`; the dry run ending `changed: 0 (dry run; 0
would change)`.

## Hand-back notes

Filled in by the agent that executes this ticket.

- The output of steps 1, 2, 5, 7 (both runs and the read-backs), 8 and 9, quoted, with
  elisions in square brackets.
- Which of the §10 claims assigned to this ticket held: `POST /pages` on an empty
  repository; `gh repo create` without `--source`; `github.event.repository.name` with
  the underscore; Pages serving the two large files unchanged; `lfs: false` checking out
  pointers (read the `assets` job's log for the checker's summary line); the LFS objects
  travelling with the first push; `--checks` with plain names.
- Any fallback taken: the `409`/`422` Pages branches, `https://` instead of SSH, a
  deploy re-run.
- Whether `--hygiene` was wanted, and the run that applied it.
- How long the first `CI` run took per job.
- Which authorisations were asked for and given, as a table of date, action, given.

## Open points

- **Whether the first deploy races step 4.** The source is set before the push, so the
  deploy job should find it; if it still answers `404`, the cause is elsewhere and the
  re-run is the remedy. Record which.
- **`gh api repos/{owner}/{repo} --jq .has_lfs`** may not be a field the API exposes;
  the fresh clone is the real test, and the field is read only if the push fails.
- **The `app_id` on the required checks** is `null` until each job has reported once;
  confirm after the first pull request that the three contexts matched their runs, as T
  C03 found.
- **Bandwidth spent.** The clone in step 9 fetches 32.3 MB of LFS objects; note it
  against the quota figure S02 recorded.
