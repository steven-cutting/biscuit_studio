---
id: C02
title: "The asset ledger: a design for deterministic, CI-verifiable copies out of the studio"
status: open
depends_on: [S02]
parallel_with: []
branch: ticket/c02-asset-ledger-design
estimated_size: M
---

# C02: The asset ledger: a design for deterministic, CI-verifiable copies out of the studio

## Context

CONVENTIONS.md §1 decision 2: the studio consumes the hub and nothing depends on the
studio, so a finished asset reaches the hub or a game **by copy**. The maintainer's words
when that was decided: "create a simple cli / structured ledger format so that the copies
are deterministic and verifiable in CI. Create a ticket to discuss the design more." This
is that ticket. It produces a design page, a decision record and follow-up tickets. It
produces no code, and it touches no other repository.

What exists on the studio side after S02: `assets/manifest.json` (CONVENTIONS.md §4), one
entry per file under `assets/` and `static/pose-studio/` carrying `path`, `bytes`,
`sha256`, `storage`, `source` and `licence`, verified by `scripts/check_assets.py` on
every `just check`. The interim procedure on the consumer side is the studio's
`docs/how-to/promote-an-asset.md` (S05): copy by hand, record the studio commit and the
sha256 in the consumer, and write the item into `docs/operations/hub-handover.md`. It is
deterministic only as far as a person is, and CI on the consumer verifies nothing.

What exists on the consumer side. Every consumer already installs the `biscuit-games-tooling`
Python package as a dev dependency pinned to a tag (H `pyproject.toml` line 12; T renders
the same) and runs its console scripts from `just` recipes and hooks. The package's
scripts find the repository root through `git rev-parse` and read per-consumer settings
from `[tool.biscuit-games-tooling]` in `pyproject.toml` (G
`/Users/scutting/projects/biscuit_games_tooling/src/biscuit_games_tooling/_project.py`,
64 lines: `root()`, `settings()`, `recipes()`, `predicates()`); they are registered under
`[project.scripts]` in G `pyproject.toml` as `bg-*`. A consumer's CI is G's `game-ci.yml`
(three jobs) for a game, or the hub's inline `ci.yml`. The hub's `consumer-impact` skill
(H `.agents/skills/consumer-impact/SKILL.md`) sorts a change into "travels as the package"
and "travels as a citation"; a copied file is a third thing it has no step for.

What the hub is waiting for from the studio: the favicon and the real `Monogram` (H
decision 0010 lines 94-96; `src/app.html` line 33 still carries `href="data:,"`), and the
illustrated poses that reopen `MascotSlot` (H decision 0017 lines 101-104 and 158; H
`docs/how-to/port-a-design-system-component.md` line 167). Those are the first three
entries any ledger will hold, and nothing can be copied before C01 lands.

The studio's page inventory is frozen by S00 (`docs/manifest.yml` and `docs/README.md`
are touched by no lane, CONVENTIONS.md §9). This ticket adds a page, so it is executed as
an S00 follow-up on `main`: the page, its manifest entry and its link on the map land in
one change on `main` rather than a lane branch.

Read first: CONVENTIONS.md §1 (decision 2), §4, §5, §6, §9; the studio's
`docs/how-to/promote-an-asset.md`, `docs/operations/hub-handover.md` and
`docs/decisions/0007-assets-travel-by-copy-and-ledger.md` as S05 and S06 wrote them; G
`_project.py` and `pyproject.toml` (`[project.scripts]`); H `consume-the-hub.md` lines
20-51 (registry access, for the "raw content needs a token" question); H
`what-the-hub-owns.md` lines 99-123 ("How a fact reaches a game"); H
`published-artefacts.md` lines 80-123; T `tickets/C02-tooling-package.md` (how a `bg-*`
script was added to G, with a golden test).

## Goal

- `docs/explanation/asset-ledger.md` in the studio (topic `asset_ledger_design`): the
  questions below, the three options with their costs, the recommendation, and the
  interfaces it implies, written so that each follow-up ticket can cite a section.
- `docs/decisions/0010-assets-leave-through-a-ledger.md` (topic
  `decision_asset_ledger`), indexed and registered, choosing the option.
- Follow-up tickets written into `tickets/` and added to `tickets/README.md`'s index and
  graph, one per repository the design touches, each self-contained in the format
  `tickets/README.md` states.
- `docs/how-to/promote-an-asset.md` gains one paragraph saying the interim procedure is
  interim and naming the decision; `docs/operations/hub-handover.md` gains the ledger as
  an item the hub will take.

## Non-goals

- Code. No `bg-check-ledger`, no `bg-copy-asset`, no ledger file anywhere. The follow-up
  tickets are where those are built, after the maintainer has answered the open points.
- Editing G, H or a game. Every follow-up that does is authorisation-gated in its own
  text.
- Deciding the licence of the studio's assets (CONVENTIONS.md §5). The ledger carries the
  field; it does not answer it.
- Changing `assets/manifest.json`'s format. If the design needs a field the manifest
  lacks, the follow-up ticket for the studio adds it, with `check_assets.py`.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `docs/explanation/asset-ledger.md` | repo (S00 follow-up on `main`) | new | the design page |
| `docs/manifest.yml` | repo (no lane; S00 follow-up) | S00's file | two entries: the page, after `explanation/content-policy.md`; the decision, after `0009` |
| `docs/README.md` | repo (no lane; S00 follow-up) | S00's file | one link under "Understand" |
| `docs/decisions/0010-assets-leave-through-a-ledger.md` | repo | new; shape from the studio's `0007` | the record |
| `docs/decisions/README.md` | repo | S05's file | one row |
| `docs/how-to/promote-an-asset.md` | repo | S05's file | one paragraph after the first, naming the decision and the interim status |
| `docs/operations/hub-handover.md` | repo | S06's file | one item: the ledger the hub takes |
| `tickets/S09-…md`, `tickets/G01-…md`, `tickets/H01-…md` (names in step 6) | tickets | new | the follow-ups |
| `tickets/README.md` | tickets | maintainer's index | rows and graph lines for the follow-ups |
| `tickets/C02-asset-ledger-design.md` | tickets | this file | `status: done` |

## Steps

1. **Read the interim procedure and the studio manifest** as they exist on `main`, and
   copy the manifest's field list into the page: the ledger reuses the manifest's names
   for the same facts, so a reader holds one vocabulary.

2. **Write the questions**, each as a heading on the design page, each answered with a
   recommendation and the reason:

   - **Where the ledger lives.** In the consumer: `assets/ledger.json` at the hub's or the
     game's root, strict JSON, one entry per copied file, sorted by `local_path`:

     ```json
     {"local_path": "src/lib/assets/brand/monogram.svg", "studio_ref": "v0.2.0", "studio_commit": "<40 hex>", "studio_path": "assets/marks/monogram.svg", "bytes": 1234, "sha256": "<hex>", "licence": "unsettled", "vetted": "2026-10-01"}
     ```

     `studio_ref` is the tag the copy was made from; `studio_commit` is what the tag
     resolved to on the day, so a moved tag is visible. `vetted` is the date the
     maintainer approved the piece (C01's condition for generated art), absent for a
     render from the model.
   - **Where the checker lives.** Three options:
     - **A.** A `bg-check-ledger` console script in G, beside the six that exist, run by a
       `just check-ledger` recipe the consumer adds to its `recipes` list. Cost: a G
       release and a moved pin in every consumer (T `C02-tooling-package.md` is the shape:
       one script, a golden test, a tag). Benefit: every consumer already installs G, the
       script reads the root and the settings the way the others do, and a bug is fixed
       once.
     - **B.** A script shipped inside the hub package's `files` (H `package.json` lines
       27-34) and run through `npm exec`. Cost: the hub package grows a Node script for a
       Python toolchain, and a game that has not bumped the package has no checker.
     - **C.** A copy of the studio's `scripts/check_assets.py` in each consumer. Cost:
       three copies of one script, the arrangement H decision 0001 exists to end.
     - **Recommend A.**
   - **What "deterministic" means.** A copy is a command, not a drag: `bg-copy-asset
     <studio-ref> <studio-path> <local-path>` fetches the bytes at that ref, writes them,
     hashes them, and writes or replaces the ledger entry. Two ways to fetch, both
     without a clone: `gh api repos/steven-cutting/biscuit_studio/contents/<path>?ref=<ref>`
     with `Accept: application/vnd.github.raw` (needs `gh` authenticated, which every
     contributor and CI already has), or `git archive --remote` (GitHub does not serve
     it). Recommend `gh api`. An LFS-tracked source (the `.blend`) is never copied: the
     ledger refuses a `studio_path` whose manifest entry says `storage: lfs`, because a
     consumer wants renders and marks, not sources.
   - **What "verifiable in CI without the network" means.** `bg-check-ledger check`
     hashes every `local_path` and compares to the entry; refuses a file with no entry
     under a directory the consumer names in `[tool.biscuit-games-tooling] ledger_roots`;
     refuses an entry with no file. That is the gate. `bg-check-ledger verify-upstream`
     is the optional online half, like `just check-links-online`: it reads the studio's
     `assets/manifest.json` at `studio_commit` through `gh api` and asserts the entry's
     `sha256` equals the manifest's for `studio_path`, so a rewritten studio history is
     caught. Monthly, by hand, per the consumer's `maintenance.md`.
   - **The studio's side.** The ledger's `sha256` must equal the manifest's at
     `studio_commit`; `bg-copy-asset` reads the manifest first and refuses a
     `studio_path` the manifest does not list. So the studio's manifest is the source of
     truth and the ledger is its shadow.
   - **Tags.** The studio cuts tags `v*` with a `CHANGELOG.md` entry naming which assets
     changed, so `studio_ref` is a name a person can read. Recommend yes; the `0.1.0`
     entry S08 writes is the first. What a level means for an asset: a changed render of
     an existing pose is MINOR (a consumer should look), a removed or renamed asset is
     MAJOR, a rebuilt file with identical bytes is nothing.
   - **What changes in the two skills.** The hub's `consumer-impact` gains a step for the
     third way a fact travels ("as a copied file, in the ledger; a rename here is a
     ledger entry that stops verifying upstream"); the studio's `hub-handover` becomes
     "write the entry the consumer will copy with `bg-copy-asset`, and record it in
     `hub-handover.md` until the consumer has run it".
   - **Licences.** The ledger copies `licence` from the manifest and refuses nothing on
     it: `unsettled` is a word in a file until the maintainer answers CONVENTIONS.md §5's
     question, and the design page says so plainly.

3. **Write the decision record** `0010` in the shape of the studio's `0007` and H's
   `0013`: context (this page), decision (option A, the two commands, the two checks, the
   tags), consequences (a G release per change to the checker; a token in every
   consumer's CI is already there; the online half is manual; a consumer that never runs
   `bg-copy-asset` keeps a copy no gate sees, which is the interim state named as a debt),
   what would reopen it (a consumer outside this account; the hub deciding assets belong
   in the package after all).

4. **The S00 follow-up.** Add the manifest entries and the map link in the same change,
   on `main`, because `docs/manifest.yml` and `docs/README.md` are touched by no lane
   (CONVENTIONS.md §9). The page's frontmatter: `title: "The asset ledger"`, `kind:
   "explanation"`, `audience: [contributor, maintainer, agent]`, `canonical_for:
   [asset_ledger_design]`, `requires: []`. The decision's: `title: "Decision 0010: Assets
   leave through a ledger"`, `kind: "decision"`, `audience: [contributor, maintainer,
   agent]`, `canonical_for: [decision_asset_ledger]`, `requires: []`.

5. **Edit the two existing pages**: `promote-an-asset.md` gains, after its first
   paragraph, "This procedure is interim. Decision 0010 replaces the copy with a command
   and the note with a ledger entry; until the follow-up tickets land, do the steps below
   and record the commit and the hash by hand." `hub-handover.md` gains the ledger as an
   item in its own register.

6. **Write the follow-up tickets**, each in the format `tickets/README.md` states, sized
   and branched, self-contained, authorisation-gated where they touch another repository:
   - `S09-studio-releases.md` (studio): tag policy, `CHANGELOG.md` levels for assets,
     `just release-check <tag>` recipe asserting the tag names `package.json`'s version
     and a changelog heading (H `scripts/check_release.py` and `just package-version` are
     the shape), and a `release.yml` that does nothing but check — the studio publishes
     no package. Depends on S08.
   - `G01-check-ledger.md` (tooling): `bg-check-ledger` and `bg-copy-asset` in G, with the
     `ledger_roots` setting, a golden test over a fixture ledger and a fixture manifest,
     a G tag. Depends on 0010; **authorisation required** for the G push and PR.
   - `H01-first-ledger-entries.md` (hub): the hub adds `assets/ledger.json`, the
     `just check-ledger` recipe, the `recipes` entry, and copies the first assets when
     they exist — the favicon and the monogram — replacing `href="data:,"`; a package
     MINOR (a token or component added: H `published-artefacts.md` line 88-89). Depends
     on C01, G01 and the assets existing; **authorisation required**.
   Add each to `tickets/README.md`'s second table and to the graph.

7. Run `just check-docs` and `just check`. Set `status: done`. Commit on `main` for the
   S00 follow-up part (the page, the manifest, the map) and on the ticket branch for the
   rest — or, if the maintainer prefers one change, on the branch with a note that it
   touches the two no-lane files. Say which in the hand-back notes. Pushing and the pull
   request are authorised separately.

## Acceptance criteria

- [ ] `docs/explanation/asset-ledger.md` exists, is registered and reachable, answers the
      eight questions of step 2 each under its own heading, lays out options A, B and C
      with a cost each, and recommends one.
- [ ] `docs/decisions/0010-assets-leave-through-a-ledger.md` exists, is registered and
      indexed, and carries context, decision, consequences and what would reopen it.
- [ ] The ledger entry shape and the two command names appear on the page exactly once
      each as code, and every follow-up ticket cites the page's section rather than
      restating it.
- [ ] Three follow-up tickets exist under `tickets/` in the stated format, and
      `tickets/README.md`'s index and graph include them.
- [ ] `promote-an-asset.md` and `hub-handover.md` each gained exactly the paragraph or
      item described.
- [ ] No file outside the studio changed; no code was added.
- [ ] `just check` is green.

## Verification

```sh
just check-docs
grep -c 'bg-copy-asset\|bg-check-ledger' docs/explanation/asset-ledger.md
ls tickets/S09-*.md tickets/G01-*.md tickets/H01-*.md
grep -c 'S09\|G01\|H01' tickets/README.md
just check
```

Expected: green; a count of at least 2; three files listed; a count of at least 6 (index
rows and graph); green.

## Hand-back notes

Filled in by the agent that executes this ticket.

- The option recommended and the one-sentence reason.
- Whether the S00 follow-up landed on `main` directly or on the branch, and why.
- The three follow-up tickets' ids, sizes and dependencies.
- Every open point below, answered by the maintainer or carried forward.

## Open points

Each is the maintainer's to decide; the page records the recommendation and the answer.

- Should the checker live in G (option A), or is a G release per change too heavy for a
  script three repositories run?
- Should a consumer pin a studio tag or a bare commit? Tags read; commits do not move.
- Should `bg-copy-asset` refuse a `licence: unsettled` asset, or only record it? The
  recommendation is record only, until §5's question is answered.
- Should the online half (`verify-upstream`) run in CI on a schedule, as T's template CI
  does weekly, or stay manual like `check-links-online`?
- Is `gh api` acceptable as the fetch path, given it ties the copy to a `gh` login, or
  should the studio publish a release asset per tag that `curl` can read anonymously
  (the repository is public)?
- Does the hub want the ledger before the first asset exists (an empty file and a recipe
  that passes), or only with the first entry?
