---
id: C04
title: "The hub registers the studio: its repositories table, the boundary page, a studio handover page"
status: open
depends_on: [C01]
parallel_with: []
branch: ticket/c04-hub-registers-the-studio
estimated_size: S
---

# C04: The hub registers the studio: its repositories table, the boundary page, a studio handover page

## Context

The hub (H, `/Users/scutting/projects/biscuit_games` at `575e3dd`) knows two kinds of
repository. Its `README.md` lines 18-23 carry one table, "The games" (Poodl and Pawjong);
`docs/project/what-the-hub-owns.md` draws its whole boundary as hub against game (lines
17-19, 44-68) with one test, "Would a second game need this, unchanged?" (line 72), and
lists what is not settled (125-138). The template, the tooling package and the studio are
named nowhere in it as members of a family; T and G appear only as a `pyproject.toml` pin
and a Provenance paragraph.

The studio is a third kind: it holds Biscuit's assets and nothing about the rules for her;
the hub holds the rules and, today, none of the assets. C01 narrowed the hub's brand rule
and put one clause on the ownership row (`what-the-hub-owns.md` line 29). What C01 left
for this ticket, by its Non-goals: the README table, the boundary page's paragraph, and a
ledger of what the hub and the studio owe each other.

That ledger has the shape of H `docs/operations/poodl-handover.md` (topic
`poodl_handover`): narrative prose grouped by shape, "None of this has happened" at the
top, never a checkbox, and "this repository records what Poodl has to change; it never
changes it" (lines 9-19 of that page). The studio's own `docs/operations/hub-handover.md`
(S06) is the mirror on the studio's side. What the hub is waiting for is already written
down in three places: decision 0010 lines 94-96 ("Mascot and favicon deferred ...
`app.html` keeps its empty data-URI icon until the reduced icon-mark exists") and line 273
(the reopener); decision 0017 lines 101-104 and 158 (`MascotSlot` refused until "the
illustrated poses arriving"); and `docs/how-to/port-a-design-system-component.md` line
167 (the `MascotSlot` ledger row, "Waits for the illustrated poses"). `character.md`
lines 25-32, as C01 rewrote them, name the studio as where the model is.

Adding a page to the hub is a manifest entry, a map link and an index of nothing else
(`docs/manifest.yml` is strict JSON; `docs/README.md` lists every operations page under
"Run it", lines 71-75). Page paths are outside versioning (H
`docs/reference/published-artefacts.md` lines 116-123); nothing packaged changes, so no
version bump. The `consumer-impact` skill (H `.agents/skills/consumer-impact/SKILL.md`)
still runs, because the ownership page is one every game cites.

Read first: CONVENTIONS.md §1 (decision 2), §6, §9; the H passages above; H
`docs/operations/poodl-handover.md` lines 1-24 and 695-723 (the register, and what a
cross-repository link costs); the C01 hand-back notes (what C01 handed here); the
studio's `docs/operations/hub-handover.md` as S06 wrote it, so the two ledgers name the
same items from opposite sides.

## Goal

A hub pull request, authorised before it is pushed, that:

- replaces the README's "The games" table with "The repositories", listing the hub, the
  games, the studio, the template and the tooling package with one line each and an
  address where one exists;
- adds one section to `docs/project/what-the-hub-owns.md`, "A repository that is neither
  hub nor game", and the companion test beside the existing one;
- adds `docs/operations/studio-handover.md` (topic `studio_handover`), registered and
  reachable, holding what the hub owes the studio and what it takes from it, in the
  register of the Poodl page;
- records the `consumer-impact` finding and passes the hub's `just check`.

## Non-goals

- Copying any asset into the hub: nothing exists to copy until the studio renders a mark
  and a pose, and the copy is C02's ledger or the interim procedure, run from the hub side
  under its own authorisation.
- Editing `direction.md`, `character.md` or any decision record: C01 did.
- A hub decision record. Naming a third kind of repository is a boundary statement on the
  page that owns `repository_boundaries`, not a platform decision; if the maintainer
  disagrees, the record is a follow-up.
- The template's and Poodl's copies of any page: they cite the hub's and hold no copy of
  these three.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `biscuit_games: README.md` | other repo | H file | lines 18-23 replaced by the table in step 2 |
| `biscuit_games: docs/project/what-the-hub-owns.md` | other repo | H file | a section after "The test" (line 97) and one sentence in "The test", step 3 |
| `biscuit_games: docs/operations/studio-handover.md` | other repo | new; shape from `poodl-handover.md` | step 4 |
| `biscuit_games: docs/manifest.yml` | other repo | H file | one entry after line 44 (`poodl-handover`) |
| `biscuit_games: docs/README.md` | other repo | H file | one link under "Run it" after line 75 |
| `biscuit_games: docs/operations/poodl-handover.md` | other repo | H file | only if step 5 finds an item |
| `tickets/C04-hub-registers-the-studio.md` | tickets | this file | `status: done` |

## Steps

1. **Confirm C01 has merged** (`git log --oneline main -- docs/decisions/0018-*` in H
   shows the commit) and read its hand-back notes for anything handed here. Branch from
   H's `main` in a worktree.

2. **The README table.** Replace lines 18-23 with:

   ```markdown
   ## The repositories

   | Repository | What it is | Where |
   | --- | --- | --- |
   | Biscuit Games (this one) | The hub: the design system, the character's rules, every cross-cutting decision. | — |
   | Poodl | An unlimited-play, Wordle-style word game. | <https://pnut.fans/poodl/> |
   | Pawjong | A tile game. Intended, not yet built. | — |
   | Biscuit Studio | Where Biscuit is made: the poseable model, the renders and the illustrations, and a site that shows them. It consumes this repository's package and nothing depends on it. | <https://stevencutting.com/biscuit_studio/> |
   | biscuit_games_template | The Copier template a new game is rendered from. | — |
   | biscuit_games_tooling | The reusable workflows, the toolchain action and the `biscuit-games-tooling` checkers every repository here runs. | — |
   ```

   The studio's address is the one S07 deployed; read it from the studio's `README.md`
   rather than assuming. Markdown's autolink form keeps lychee offline quiet about it.

3. **The boundary page.** In "The test" (lines 70-97), after the paragraph ending "the
   arrangement decision 0001 exists to end" (line 96-97), add a short paragraph: the test
   has a companion for anything that is a picture rather than a rule — **is this a rule
   about her, or a picture of her?** A rule is decided here; a picture is made in the
   studio and copied out. Then a new section before "How a fact reaches a game":

   ```markdown
   ## A repository that is neither hub nor game

   Biscuit Studio holds her assets: the poseable model, the renders and exports made
   from it, and the illustrations. It decides nothing about her — her registers, her
   voice and where she may appear are [The Biscuit character](../design/character.md)'s,
   and the studio cites that page as a game does — and it consumes this repository's
   package for its own site exactly as a game does. Nothing here depends on it: a mark or
   a pose reaches this repository by copy, recorded on both sides, and
   [Studio handover](../operations/studio-handover.md) is the ledger of what is owed in
   each direction. The studio's own handbook says what it will not commit and why.
   ```

4. **The studio handover page.** Frontmatter `title: "Studio handover"`, `kind:
   "operations"`, `audience: [maintainer, agent]`, `canonical_for: [studio_handover]`,
   `requires: []`. Body, in the Poodl page's register: an opening paragraph in the same
   words as that page's lines 9-19 with the repository name swapped ("None of this has
   happened"; the hub records and never edits the studio); then three groups:

   - **What this repository takes from the studio, when it exists**: the reduced
     icon-mark as the favicon (`src/app.html` line 33's `href="data:,"`, decision 0010
     lines 94-96), the real `Monogram` replacing the placeholder set in type (H
     `src/lib/components/Monogram.svelte` lines 6-8), and the first pose set for
     `MascotSlot` (decision 0017 lines 101-104; the porting guide's line 167 row).
     Each names the hub file that changes, the version level a consumer sees (a component
     changing its rendering with its name and props kept: MINOR per `published-artefacts.md`
     lines 88-96), and that the copy is made under C02's ledger once it exists and under
     the studio's interim procedure until then.
   - **What this repository owes the studio**: a decided licence for the assets (the
     open question `character.md` lines 128-134 still records); an answer to whether the
     hub's handbook will ever ship with the package (`what-the-hub-owns.md` lines 127-131),
     because the studio's `docs/project/platform.md` carries the same rotting links every
     game does; and a G release of `bg-check-ledger` when C02's follow-up lands.
   - **What a cross-repository link costs**: two sentences pointing at the Poodl page's
     section of that name rather than restating it.

5. **Run `consumer-impact`.** The ownership page moved (a section added, nothing renamed);
   no anchor a game cites changed — check by grepping Poodl's and the template's
   `docs/project/platform.md` for `what-the-hub-owns.md#` (T's page links whole pages,
   line 67). Expected: nothing to Poodl; record it. If a fragment link is found, write the
   item into `poodl-handover.md`.

6. **Register and link**: the manifest entry after line 44, the map link after line 75.
   `just check-docs`, then the hub's `just check`.

7. **Authorisation required:** pushing and opening the hub pull request. Stop and ask.
   After the merge, set `status: done` here and commit on the studio branch; pushing that
   is authorised separately.

## Acceptance criteria

- [ ] H `README.md` carries "The repositories" with six rows and no longer carries "The
      games"; the studio's address matches the studio's `README.md`.
- [ ] `what-the-hub-owns.md` gained the companion question and the one section, and
      nothing else in it changed (`git diff main --stat` shows two hunks).
- [ ] `docs/operations/studio-handover.md` exists, is registered with the frontmatter
      above, is linked from `docs/README.md`, opens with "None of this has happened", and
      names the three assets the hub is waiting for with the hub file each changes.
- [ ] Every link on the new page resolves offline; the only `https://` link is the
      studio's address.
- [ ] The `consumer-impact` outcome is in the hand-back notes.
- [ ] `package.json` and `CHANGELOG.md` in the hub are untouched.
- [ ] The hub's `just check` is green on the pull request; the push and the pull request
      were authorised first.

## Verification

In the hub worktree, on the branch:

```sh
git diff main --stat
grep -c '^| ' README.md
grep -n 'None of this has happened' docs/operations/studio-handover.md
grep -c 'studio-handover' docs/manifest.yml docs/README.md
just check-docs
just check
```

Expected: five files (six with the Poodl page); at least 8 table rows in the README (two
header lines and six repositories); one line; `1` for each of the two files; green;
green.

## Hand-back notes

Filled in by the agent that executes this ticket.

- The `consumer-impact` finding.
- The hub pull request and its check outcome.
- Any wording the maintainer changed in the table or the section, so the studio's
  `platform.md` and `hub-handover.md` can be kept in step (handed to the studio as a
  follow-up, not made here).
- Which authorisations were asked for and given, with dates.

## Open points

- Whether the template and the tooling package belong in a user-facing README table at
  all, or in a maintainer section further down. Recommend the table: a reader who finds
  one repository should be able to find the rest from it.
- Whether "A repository that is neither hub nor game" deserves a decision record, since
  it changes what `repository_boundaries` means. Recommend not now; C01's `0018` already
  names the studio, and a boundary sentence on the owning page is where the hub keeps
  such things.
- Whether the studio's `docs/project/platform.md` should link the new hub page. It
  should, and that is a one-row edit to a studio page owned by S05, handed back to the
  studio rather than made here.
