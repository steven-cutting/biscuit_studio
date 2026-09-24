---
id: S11
title: "The rebuild, run end to end: the success path and the interrupted path of scripts/rebuild_model.sh"
status: open
depends_on: [S09]
parallel_with: [S07, S08, S10]
branch: ticket/s11-rebuild-success-path
estimated_size: S
---

# S11: The rebuild, run end to end: the success path and the interrupted path of scripts/rebuild_model.sh

## Context

S02 wrote `scripts/rebuild_model.sh`, which `just model-rebuild` runs. It tested the
script's refusals and its restore after a failed build using a fake `BLENDER`, but never
ran it for real. From its hand-back notes, "`scripts/rebuild_model.sh` deviates from the
embedded text": "The success path needs Blender and the real study chain and was not run,
nor was the `INT`/`TERM` routing." This ticket runs both paths.

Nothing this repository serves has been rebuilt since the import. A real rebuild shows
whether the model's own build is reproducible: whether Blender, at the version installed,
writes the same bytes the manifest records. It also shows whether the script's
precondition, restore and debris purge behave as `docs/how-to/rebuild-the-model.md` says.
The answer decides what a future rebuild costs in history (CONVENTIONS.md §11, "A 26 MB
file in ordinary history").

This ticket commits **no rebuilt asset**. Committing a rebuild is a change to what the
site serves and what the manifest records, so the maintainer decides it on the evidence
recorded here.

Read first: CONVENTIONS.md §0 (D's path and commit), §3, §4 and §11; S02's hand-back
notes; `scripts/rebuild_model.sh`; `assets/models/biscuit/README.md` (Provenance, and the
five build commands); `docs/how-to/rebuild-the-model.md`; the `asset-change` skill.

## Goal

- One real `just model-rebuild` run against D at `1d9d358` has finished, with its
  duration, its exit status and the manifest diff it produced recorded.
- Every file the run changed is listed, with whether its bytes match the manifest's.
  The files that differ are explained where the evidence allows: timestamps, renderer
  noise, or a Blender version difference.
- An interrupted run (`INT`, then `TERM`) was shown to restore `assets/` and
  `static/pose-studio/` to `HEAD` and to remove the `assets/biscuit_pics` link.
- `docs/how-to/rebuild-the-model.md` matches what was observed.

## Non-goals

- Committing any file under `assets/` or `static/pose-studio/`, or `assets/manifest.json`.
- Writing to D, or running any of D's scripts from inside D (CONVENTIONS.md §9).
- Making the build deterministic. If it is not, record where it differs, and the
  maintainer decides whether that is a ticket.
- C03's three.js viewer.

## Files touched

| Path | Class | Change |
| --- | --- | --- |
| `scripts/rebuild_model.sh` | script | only if a run shows a defect; the fix and its evidence recorded |
| `docs/how-to/rebuild-the-model.md` | page | what the run showed that the page does not say, such as duration, what differs and the clean-up after a successful run that is not committed |
| `tickets/CONVENTIONS.md` | tickets | §11 "The rebuild reaches outside the repository", if the interrupted run shows the link is removed, not left; S10, which may run alongside, edits only a different §11 bullet |
| `tickets/S11-rebuild-success-path.md` | tickets | `status:` line, hand-back notes |

## Steps

1. **Ask first.** The run keeps Blender busy for minutes and rewrites up to 112 MB of the
   worktree before this ticket restores it. Get the maintainer's go-ahead, and record it.

2. **Preconditions.** Record the output of each:

   ```sh
   D=/Users/scutting/.supacode/repos/biscuit_pics/very_nice_three_deeez
   git -C "$D" rev-parse HEAD
   git -C "$D" status --short | wc -l
   /Applications/Blender.app/Contents/MacOS/Blender --version | head -1
   git status --porcelain --untracked-files=all -- assets static/pose-studio | wc -l
   git lfs ls-files --long
   ```

   Expected: `1d9d358…`; `0`; the Blender version, which
   `assets/models/biscuit/README.md` may name for comparison; `0`; the three LFS objects,
   starred as present. Stop and report if D is not at `1d9d358` or is dirty.

3. **The success path.** From a clean worktree, run `time just model-rebuild "$D"` and
   record the exit status, the wall-clock time and the script's last three lines. Then,
   before touching anything:

   ```sh
   git status --short -- assets static/pose-studio
   git diff --stat -- assets/manifest.json
   just check-assets
   ls -la assets/biscuit_pics 2>&1
   find assets -name '__pycache__' -o -name '*.blend1'
   git -C "$D" status --short | wc -l
   ```

   Expected: a list of changed files; a manifest diff; `check_assets check: ok`, because
   the script rewrote the manifest from the new bytes; no link; no debris; `0`. D is
   untouched. For each changed path, quote the old digest from `git show HEAD:assets/manifest.json`
   and the new one. Group the changes into files whose bytes match the manifest and files
   whose bytes differ. For each file that differs, say why if a byte-level look can tell
   (for example, a changed timestamp in the GLB's JSON chunk, or pixel noise in a render).
   Do not guess. For the viewer, also check that the three `patched` rewrites still hold
   (`grep -o 'href="[^"]*"' static/pose-studio/viewer.html | sort | uniq -c`, compared with
   S02's hand-back).

4. **Put the worktree back.** The script does not restore after a successful run, which is
   correct, since committing is the maintainer's call. So:

   ```sh
   git restore --source=HEAD --staged --worktree -- assets static/pose-studio
   git clean -fdq -- assets static/pose-studio
   git status --porcelain --untracked-files=all -- assets static/pose-studio | wc -l
   just check-assets
   ```

   Expected: `0`, then `check_assets check: ok`. Confirm that `git lfs ls-files --long`
   still stars the three objects.

5. **The interrupted path.** Use a fake `BLENDER` in `ai_tmp/`, as S02 did: a script
   that appends a line to `assets/models/biscuit/model/rig.json`, creates
   `assets/models/biscuit/previews/stray.png`, then sleeps for 60 seconds. Run
   `BLENDER=<fake> sh scripts/rebuild_model.sh "$D" &` and, within the sleep, send
   `INT` to the process group, as a terminal's interrupt does. Record the exit status (130
   is expected), the script's message, `git status --short -- assets static/pose-studio`
   (empty is expected), and whether `assets/biscuit_pics` still exists. Repeat with `TERM`
   sent to the script's own process (143 is expected). If either run leaves the worktree
   changed, that is a defect: restore by hand as in step 4, fix the script, re-run both
   signals, and record the fix and the new output.

6. **Write down what was learned.** Add to `docs/how-to/rebuild-the-model.md` what a
   maintainer needs and the page lacks. That is the run's duration on this machine, which
   outputs are reproducible and which are not, and the step-4 commands for a run whose
   output will not be committed. Write it in the page's own register. If step 5 showed
   the link is removed on interrupt, correct CONVENTIONS.md §11's sentence "A rebuild
   interrupted half-way leaves the link" to match. Run `just check-docs`.

7. Run the verification, fill in the hand-back notes, set `status: done`, and commit.
   Pushing and the pull request are authorised separately.

## Acceptance criteria

- [ ] The maintainer's go-ahead for the real run is recorded.
- [ ] The real run's exit status, duration and changed-file list are recorded, each changed
      file with its old and new digest and whether it matches the manifest.
- [ ] D's `status --short` counts `0` after the run.
- [ ] After step 4, `git status --porcelain -- assets static/pose-studio` is empty and
      `just check-assets` is green.
- [ ] Both signals restored the worktree and removed the link, or a script fix is
      recorded that makes them do so.
- [ ] `git diff main --stat` names only files from the table.
- [ ] `just check` is green.

## Verification

```sh
git diff main --stat
git status --porcelain --untracked-files=all -- assets static/pose-studio | wc -l
test -e assets/biscuit_pics; echo "link rc=$?"
just check-assets
just check-docs
just check
```

Expected: only the table's files; `0`; `link rc=1`; `check_assets check: ok`; both green.

## Hand-back notes

Filled in by the agent that executes this ticket.

- The maintainer's go-ahead, with the date.
- Step 2's output, quoted.
- The real run: exit status, duration, the changed files grouped as matching or
  differing, with digests and the reason where one was found.
- The two interrupted runs' output.
- Any script fix, with the reason for it.
- A recommendation to the maintainer: whether a rebuild at this Blender version can be
  committed as a no-op, or what it would add to history.
- Anything that belongs to a done ticket, written as an item for a follow-up
  (CONVENTIONS.md §9).

## Open points

- **Whether Blender's `.blend` save is ever byte-stable.** It likely embeds a save
  timestamp, and the GLB exporter may embed a generator version. If only those differ,
  the maintainer may want the rebuild recipe to say so up front rather than let each
  rebuild rediscover it.
- **Whether the renders are reproducible on this GPU and Blender version.** Record, and
  do not try to fix it.
