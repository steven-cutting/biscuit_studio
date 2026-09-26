---
id: S08
title: "Maintainer docs: README.md, CHANGELOG.md 0.1.0, AGENTS.md provenance"
status: done
depends_on: [S07]
parallel_with: [S11]
branch: ticket/s08-maintainer-docs
estimated_size: S
---

# S08: Maintainer docs: README.md, CHANGELOG.md 0.1.0, AGENTS.md provenance

## Context

Every lane has merged and S07 has created the GitHub repository, applied its settings and
deployed the site once. What remains is the three root files a reader meets first: S00
shipped `README.md` and `CHANGELOG.md` as stubs and wrote `AGENTS.md` with a short
Provenance section (CONVENTIONS.md §2, §7). This ticket writes them in final form, using
facts that only exist now: the address the site is served at, the checks `main` requires,
and which decision records the studio's own record carries.

Read first: CONVENTIONS.md §0, §1, §2, §7 and §9; H `README.md`
(`/Users/scutting/projects/biscuit_games/README.md`, 88 lines, the shape); T `README.md`
(`/Users/scutting/projects/biscuit_games_template/README.md`) lines 130-155 ("Bootstrap a
repository") and 247-259 ("Bootstrap of this repository"), the two sections whose shape
the studio's "Bootstrap of this repository" takes; the studio's own `AGENTS.md`
(S00's), `docs/decisions/README.md` (S05's) and the S07 ticket's hand-back notes, which
record the deployed address, the first run's check names and what the bootstrap script
changed.

The agent contract (`bg-validate-agents`, G
`/Users/scutting/projects/biscuit_games_tooling/src/biscuit_games_tooling/validate_agents.py`
lines 47-54) requires the six phrases `untrusted`, `just check`, `explicit authorization`,
`ai_tmp/`, `docs/specs/` and `runes` in `AGENTS.md` and at least 300 words; an edit to the
Provenance section must leave all six standing. The documentation contract lints
`README.md` and `CHANGELOG.md` as root files (markdownlint, typos, lychee offline) but
registers neither, so neither carries frontmatter.

Tagging `v0.1.0` is a separately authorised action (CONVENTIONS.md §9) and this ticket
does not tag: it writes the changelog entry the tag will name and stops.

## Goal

- `README.md` says what the studio is, where the site is, how to start, how the repository
  is laid out, where the handbook begins, and what the boundary with the hub is.
- `CHANGELOG.md` carries a `0.1.0` entry describing the first release and the two link
  definitions Keep a Changelog expects.
- `AGENTS.md`'s Provenance section names the five sources at their commits, the nine
  decision records, and the deviations from a game, and `just check-agents` is green.

## Non-goals

- Tagging, pushing, opening the pull request: each is authorised separately.
- Any handbook page under `docs/`: S05 and S06 own them; a fact this ticket wants to state
  and cannot find on a page is handed back to the page's owner, not written here.
- Any other section of `AGENTS.md`. Only Provenance changes.
- Setting another ticket's `status:`. Each ticket sets its own.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `README.md` | repo | S00's stub; shape from H `README.md` and T `README.md` 247-259 | replaced |
| `CHANGELOG.md` | repo | S00's stub | the `0.1.0` entry and the link definitions |
| `AGENTS.md` | repo | S00's file | the Provenance section only |
| `tickets/S08-maintainer-docs.md` | tickets | this file | `status: done` |

## Steps

1. Read the S07 hand-back notes and copy out: the deployed address (expected
   `https://stevencutting.com/biscuit_studio/`), the three required contexts
   (`frontend`, `documents`, `assets`), whether `--hygiene` was applied, and whether
   private vulnerability reporting is on. These are the facts the README states; do not
   state one the notes do not carry.

2. Write `README.md` with these sections, in this order, in H's register:

   - `# Biscuit Studio`, then two paragraphs: the studio is the Biscuit Games repository
     where the platform's graphical assets are developed — the poseable model, the renders
     and exports from it, the illustrations — and the static site that shows them; it
     consumes `@steven-cutting/biscuit-games` like a game and nothing depends on it;
     finished assets leave by copy, recorded in the manifest and, once C02 lands, a ledger.
     A **Status** line in bold as H line 7 has it, naming what is in place after S07.
   - `## The site`: the address, what it shows (the model page with the pose studio, the
     gallery), and that it is a project Pages site under `/biscuit_studio` (CONVENTIONS.md
     §1 decision 6).
   - `## Quick start`: the `just initialize` / `just check` block as H lines 27-30, then
     the two things a first run needs that no lockfile carries: a `read:packages` token in
     `~/.npmrc` (write the line as `//npm.pkg.github.com/:_authToken=<your token>`, never
     a bare word after the `=`, CONVENTIONS.md §9) and `git lfs install`, which
     `scripts/initialize.sh` runs and which a clone without git-lfs has to run itself
     before the `.blend` is anything but pointer text. The worktree warning about
     `just install-hooks` from H lines 44-46.
   - `## Check your work`: H lines 48-53 verbatim.
   - `## Layout`: a `text` block naming `assets/` (the sources and the manifest),
     `static/pose-studio/` (what the site serves byte for byte), `src/lib/` (brand,
     appearance, the lockup), `src/routes/` (the three pages), `docs/`, `tests/`,
     `scripts/` (the asset checker, the rebuild script, the bootstrap script),
     `tickets/` (the work breakdown this repository was built from).
   - `## Documentation`: H lines 70-79, with the studio's own four starting pages:
     `docs/project/purpose-and-scope.md`, `docs/project/platform.md`,
     `docs/explanation/content-policy.md`, `docs/decisions/README.md`, as relative links
     (they exist now; lychee resolves them offline).
   - `## Boundaries`: the hub owns the rules about Biscuit and the design system, the
     studio owns her assets, files travel one way as the package and the other way by copy,
     with links to `docs/project/platform.md` and `docs/how-to/promote-an-asset.md`.
   - `## Bootstrap of this repository`: T lines 247-259's shape. CI runs three jobs on
     every pull request, push to `main` and dispatch; all three are required checks on
     `main`, applied by `scripts/bootstrap_repo.sh steven-cutting/biscuit_studio --checks
     frontend,documents,assets`, in one round because none of the three depends on a
     setting outside this repository; the Pages source is GitHub Actions; neither job
     carries a `paths` filter or a `name:`. State the vulnerability-reporting and
     `--hygiene` outcomes as S07 recorded them.

   Every link is relative and resolves; every path is a code span; no bare URL other than
   the site address in angle brackets.

3. Write `CHANGELOG.md`:

   ```markdown
   # Changelog

   All notable changes to this repository are documented here.

   The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
   the versions are tags on `main`. A tag is cut only when the maintainer authorises it;
   the entry below was written before the tag existed and says what the tag will name.

   ## [Unreleased]

   ## [0.1.0] - <date>

   ### Added

   - ...
   ```

   The `Added` list names, one bullet each: the toolchain and the gate (`just check`, its
   eight recipes by name); the site (three routes, the platform package at `1.1.0`, the
   appearance wiring); the approved model imported from `biscuit_pics` at `1d9d358`, the
   cel set, the manifest and `just check-assets`; the large-file policy; the handbook
   (forty pages, nine decisions); the agent contract (eight skills); the workflows and the
   Pages deployment at the address. Use the date S07's first deploy succeeded. Then the two
   link definitions:

   ```markdown
   [Unreleased]: https://github.com/steven-cutting/biscuit_studio/compare/v0.1.0...HEAD
   [0.1.0]: https://github.com/steven-cutting/biscuit_studio/releases/tag/v0.1.0
   ```

   Both resolve only after the tag exists; lychee runs `--offline` and skips them.

4. Rewrite the **Provenance** section of `AGENTS.md`, and nothing above it. It says:
   the repository was assembled by hand (not rendered from the template) from the hub at
   `575e3dd`, Poodl at `a2860fc`, the template at `2283589`, the tooling package at
   `v0.3.0` and the `biscuit_pics` worktree at `1d9d358`, on 2026-09-23, by the tickets
   under `tickets/`; that what it decides is recorded in `docs/decisions/` as 0001 to
   0009, listed one line each with the title `docs/decisions/README.md` gives; and the
   deliberate deviations from a game rendered by the template, each with its decision:
   no `docs/specs/` of its own (the platform's modules govern; `check-specs` and
   `analyse-specs` are absent — decision 0002), no component workshop (0009), an `assets`
   gate and a manifest (0007), sources in LFS (0006), hand-assembled (0005), the viewer
   embedded as-is (0008). Keep the sentence S00 wrote that the studio has no
   `docs/specs/` of its own wherever it sits; do not move the six phrases.

5. Run `just check-docs`, `just check-agents`, then `just check`. Set `status: done`.
   Commit on the branch. Pushing and the pull request are authorised separately.

## Acceptance criteria

- [ ] `README.md` carries the eight sections of step 2 in that order; every relative
      link resolves (`just check-docs` is green, which runs lychee offline over root
      files); the site address appears exactly once in angle brackets.
- [ ] `README.md` states no fact about repository settings that S07's hand-back notes do
      not carry.
- [ ] `CHANGELOG.md` parses as Keep a Changelog: `## [Unreleased]`, `## [0.1.0] - <date>`,
      an `### Added` list, and the two link definitions at the end.
- [ ] `AGENTS.md` differs from `main` only inside the Provenance section
      (`git diff main -- AGENTS.md` shows hunks under that heading alone).
- [ ] `uv run --frozen bg-validate-agents` exits 0 and the six phrases are each present.
- [ ] `just check` is green.
- [ ] No tag was created, nothing was pushed.

## Verification

```sh
just check-docs
just check-agents
for p in untrusted 'just check' 'explicit authorization' 'ai_tmp/' 'docs/specs/' runes; do printf '%s: ' "$p"; grep -c -- "$p" AGENTS.md; done
git diff main --stat -- AGENTS.md README.md CHANGELOG.md
git tag --list
just check
```

Expected: the first two exit 0; six counts, each at least 1; three files in the stat;
`git tag --list` prints nothing; `just check` ends green with the worktree unchanged.

## Hand-back notes

Executed on 2026-09-25 on the Supacode worktree branch `S08-maintainer-docs`, not the
`ticket/s08-maintainer-docs` the `branch:` field names, as every ticket since S00 has been
(nothing in the checks reads the branch name). The worktree was fresh, so `just sync` ran
first.

**Line counts and date.** `README.md` 115 lines, `CHANGELOG.md` 36, `AGENTS.md` 218. The
`0.1.0` entry is dated `2026-09-25`, the UTC date of S07's successful deploy run
`36097753484` (S07 ran on 2026-09-24 local time); the maintainer chose the UTC date.

**Decisions taken with the maintainer before writing.**

- The handbook is described as thirty-nine pages, not the forty step 3 names:
  `docs/manifest.yml` registers thirty-nine (`bg-validate-docs` prints `Validated 39
  pages`), as CONVENTIONS.md §6 says.
- Open point 2: the README names the pose studio as `pose-studio/viewer.html` under the
  site, with its size (27.6 MB, the manifest's 27,561,668 bytes), as a path rather than a
  second URL, so the site address stays the one bare URL.
- Open point 1 is not this ticket's to settle: whether `v0.1.0` waits for C01 is decided
  when the tag is authorised.

**Facts checked against the source rather than the ticket.** The model page links to the
pose studio rather than embedding it, so the README says "offers it three ways". The
appearance wiring writes `data-animations` and `data-high-contrast` only (the studio's
theme is fixed), so the changelog says "motion and contrast preferences". Every repository
setting the README's last section states is in S07's hand-back notes: the three contexts
in one round, the Pages source, vulnerability reporting `true`, `--hygiene` applied, and
HTTPS enforced by a separate call.

**Verification**, run with the three files staged:

```text
$ just check-docs
markdownlint.............................................................Passed
typos....................................................................Passed
lychee...................................................................Passed
Validated 39 pages and 40 canonical topics.
$ just check-agents
Validated AGENTS.md, 2 adapters, and 8 skills.
$ for p in ...; do ...; done
untrusted: 1
just check: 5
explicit authorization: 1
ai_tmp/: 1
docs/specs/: 2
runes: 1
$ git diff main --stat -- AGENTS.md README.md CHANGELOG.md
 AGENTS.md    |  57 +++++++++++++++++++++---------
 CHANGELOG.md |  32 +++++++++++++----
 README.md    | 114 +++++++++++++++++++++++++++++++++++++++++++++++++++++------
 3 files changed, 170 insertions(+), 33 deletions(-)
$ git tag --list
$ just check
All checks passed and the worktree is unchanged.
```

`git diff main -- AGENTS.md` has one hunk, `@@ -176,20 +176,43 @@`, whose only changed
lines sit below `## Provenance` (line 177). The site address appears once in angle
brackets in `README.md` and is its only `https://` string.

**Handed on:** nothing. Every fact the README states was found on a handbook page, in a
workflow or script, or in S07's notes.

**Not done, by design.** `v0.1.0` is untagged: tagging is the maintainer's call and a
separately authorised action. Nothing was pushed and no pull request was opened.

## Open points

- Whether the first tag should wait for C01 (the hub's brand rule), since until it lands
  the release notes describe assets that cannot leave the studio. Recommend: tag anyway;
  the changelog says what the studio holds, not what the hub accepts.
- Whether `README.md` should carry the pose-studio address
  (`https://stevencutting.com/biscuit_studio/pose-studio/viewer.html`) beside the
  site address, given the 26 MB download behind it. Recommend: name it, with the size.
