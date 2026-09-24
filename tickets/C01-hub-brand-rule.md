---
id: C01
title: "The hub permits renders from the approved model: decision 0018, direction.md and character.md"
status: open
depends_on: []
parallel_with: []
branch: ticket/c01-hub-brand-rule
estimated_size: M
---

# C01: The hub permits renders from the approved model: decision 0018, direction.md and character.md

## Context

The hub (H, `/Users/scutting/projects/biscuit_games` at `575e3dd`) owns the platform's
aesthetic and the character, and every other repository cites it (H
`docs/project/what-the-hub-owns.md` lines 21-35). Two of its pages rule out, in so many
words, what the studio exists to make:

- H `docs/design/direction.md` lines 262-263, under **Avoid** ("each of these actively
  breaks something above"):

  > - Cartoon styling aimed at children, hyperrealism, 3D rendering, glossy mobile-game
  >   character art, or anything carrying generative-AI artefacts.

- H `docs/design/character.md` lines 20-21 ("A game does not redraw her ... anything it
  wants to change is changed here first"), 25-32 ("Nothing of her ships ... set in type
  until an illustrator draws the real one"), 89-98 ("The first pose set. Commissioned from
  an illustrator."), 106-113 ("A character reference sheet ... is the first thing
  commissioned"), and 128-134 (the photographs live in `biscuit_pics`; "what would come
  across, in what form, and under what licensing, is not yet decided").

The studio holds a cel-shaded, rigged 3D model of Biscuit — D
`/Users/scutting/.supacode/repos/biscuit_pics/very_nice_three_deeez/models/biscuit/` at
`1d9d358`, approved by the maintainer as "the current approved Biscuit model" (its
`README.md` line 3) — and eleven 2D illustrations made with an image model (D `good/`,
commit `c602c38` "best mix and match examples. Created using chatgpt."). CONVENTIONS.md §1
decision 1 is the maintainer's answer: **the hub's rule changes first**, so that cel-shaded
renders from the approved model, and generated art the maintainer has vetted, may ship as
the fuller illustrated register; until this ticket lands, nothing the studio makes is
promoted (CONVENTIONS.md §11).

Two hub mechanisms this ticket runs inside:

- A decision record has a fixed shape and a fixed procedure: H `docs/decisions/README.md`
  lines 53-72 ("Writing a new one": context, decision, consequences including the ones
  that hurt, what would reopen it; a file, a manifest entry, an index row; and the four
  verbs **superseded by**, **narrowed by**, **carried out on**, **overruled on**). The
  highest record is `0017` (H `docs/decisions/` listing on 2026-09-23); this one is
  `0018` unless something has landed since.
- A change to a page a game cites runs the `consumer-impact` skill (H
  `.agents/skills/consumer-impact/SKILL.md`, eight steps) and, where Poodl is affected,
  writes the item into H `docs/operations/poodl-handover.md`. Page paths are outside
  versioning (H `docs/reference/published-artefacts.md` lines 116-123), so no version bump
  follows a prose change; the package is untouched.

H decision 0013 lines 127-129 names "A consumer that is not a Biscuit Games game" as a
reopener of the package decision, because "anything outside that wants a licence file and a
deprecation policy this repository does not have". The studio is such a consumer, owned by
the same account. This ticket does not reopen 0013; it acknowledges the trigger in 0018's
text and says why it does not fire (same account, same version policy, `UNLICENSED` on
both sides), which is what H's README calls **overruled on** a date — a trigger a later
record acts without, "which is not the same as the trigger firing and must never be
written as though it were" (lines 69-71).

Read first: CONVENTIONS.md §1 (decision 1 and fact 9), §5, §9, §11; the five H passages
above; H `docs/decisions/0013-shared-material-travels-as-a-package.md` whole (140 lines,
the shape and the reopener); H `docs/decisions/0010-biscuit-games-design-system.md` line
94-96 and 273 (mascot and favicon deferred, and the reopener); H
`docs/decisions/0017-the-rest-of-the-design-system-is-ported.md` lines 101-104 and 158
(`MascotSlot` refused until "the illustrated poses arriving"); H
`docs/how-to/port-a-design-system-component.md` line 167 (the `MascotSlot` ledger row).

## Goal

A hub pull request, authorised before it is pushed, that:

- adds `docs/decisions/0018-renders-from-the-approved-model-may-ship.md`, indexed and
  registered;
- narrows the **Avoid** bullet in `docs/design/direction.md` so it forbids what it meant
  to forbid and no longer forbids the studio's output;
- rewrites four passages of `docs/design/character.md` so the model is the reference the
  page was waiting for, an illustrator is a route rather than the route, and
  `biscuit_studio` is named as where her assets live;
- records the `consumer-impact` finding (expected: nothing to Poodl), and passes the hub's
  `just check`.

## Non-goals

- Promoting any asset. C01 permits; the interim procedure in the studio's
  `docs/how-to/promote-an-asset.md` and later C02 move things.
- Reopening 0013, adding a licence file, or deciding the licence of the studio's assets
  (CONVENTIONS.md §5: an open question, recorded and not resolved).
- The hub's README table, the ownership page's new paragraph and the studio handover
  page: C04.
- Any edit to `direction.md` beyond the one bullet, or to `character.md` beyond the four
  passages. The pages' other rules — one face, rare breaks, motion off reduces to the
  mark, placement only at boundaries, no first person — stand and 0018 says so.
- A version bump. Nothing packaged changes.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `biscuit_games: docs/decisions/0018-renders-from-the-approved-model-may-ship.md` | other repo | new; shape from H `0013` | the record, step 3 |
| `biscuit_games: docs/decisions/README.md` | other repo | H file | one row after line 43 |
| `biscuit_games: docs/manifest.yml` | other repo | H file | one entry after line 63 (the last decision), before the closing bracket |
| `biscuit_games: docs/design/direction.md` | other repo | H file | lines 262-263, step 4 |
| `biscuit_games: docs/design/character.md` | other repo | H file | lines 25-32, 89-98, 106-113, 128-134, step 5; a **narrowed by** blockquote is not used because the page is not a decision record — the edits stand in the prose |
| `biscuit_games: docs/project/what-the-hub-owns.md` | other repo | H file | line 29 (the Biscuit row of the ownership table) gains "; her assets are made in `biscuit_studio`", step 6 |
| `biscuit_games: docs/operations/poodl-handover.md` | other repo | H file | only if step 7 finds an item |
| `tickets/C01-hub-brand-rule.md` | tickets | this file | `status: done` |

Nothing in the studio changes except this ticket's status line.

## Steps

1. **Confirm the numbering and the lines.** In H at its current `main`: `ls
   docs/decisions/` shows `0017-…` as the highest, and `sed -n 262,263p
   docs/design/direction.md` prints the bullet quoted above. If either has moved, adjust
   every line number below and say so in the hand-back notes; the design does not change.

2. **Create the branch** `ticket/c01-hub-brand-rule` from H's `main`, in a worktree
   (`git worktree add ../biscuit_games-c01 -b ticket/c01-hub-brand-rule main` from the H
   clone). Run `just initialize` there if `node_modules/` is absent; the hub's gate runs
   Storybook and needs the browser.

3. **Write `0018`.** Frontmatter exactly:

   ```markdown
   ---
   title: "Decision 0018: Renders from the approved model may ship"
   kind: "decision"
   audience: [contributor, maintainer, agent]
   canonical_for: [decision_renders_from_the_model]
   requires: []
   ---

   # Decision 0018: Renders from the approved model may ship
   ```

   Then the four sections, in H's register:

   - **Context.** The Avoid bullet and the illustrator brief, quoted; the two registers
     (`character.md` lines 36-40); the fact that a poseable, cel-shaded model of the dog
     now exists and has been approved by the maintainer, in a repository of its own,
     `biscuit_studio`; that the reference sheet `character.md` asked for is what a rigged
     model *is* — proportions, colouring, face, ears, tail and paws fixed once and posed
     many times — so the sheet's purpose is met by a different object; and that eleven
     2D pieces were made with an image model, which the same bullet forbids by artefact.
   - **Decision.** Four sentences of decision and one of scope:
     1. Cel-shaded renders posed from the approved model are permitted as the fuller
        illustrated register, and the model is the character reference sheet: every later
        pose, drawn or rendered, is checked against it.
     2. The **Avoid** bullet is narrowed: what is avoided is 3D that *reads* as 3D — PBR
        materials, gloss, realistic lighting, depth-of-field — and art carrying *visible*
        generative artefacts; a cel render whose surfaces are flat bands and ink, and a
        generated piece the maintainer has vetted for artefacts, are neither.
     3. Generated 2D art ships only after the maintainer has vetted the piece; the
        vetting is recorded where the piece is recorded (the studio's manifest `source`
        and, when C02 lands, the ledger entry).
     4. An illustrator remains a route. "Commissioned from an illustrator" becomes "posed
        and rendered from the approved model in the studio, or commissioned"; nothing
        here prefers one over the other.
     5. Everything else on both pages stands: one face, broken rarely; motion off reduces
        her to the mark; she appears only at boundaries; she never speaks in the first
        person; the mark stays abstract and geometric. This record moves the medium and
        nothing about her behaviour.
   - **Consequences**, each a bold lead sentence then a paragraph, including the ones
     that hurt: an illustrator is no longer the only route, and a commission is no longer
     the first purchase; consistency comes from one model rather than from a sheet, which
     is stronger across a set drawn over months and weaker at the one thing a sheet does
     that a model cannot, which is fix a *drawn* line; "she stays recognisably brown"
     (`character.md` 112-113) is now measured against the model's coat texture, and a
     render that drifts warm has a file to be compared with; the studio is a consumer of
     the package that is not a game, which 0013 named as a reopener — state that the
     trigger is **overruled on** the date of this record and why (the studio is this
     account's, takes the same version policy, publishes nothing, and is `UNLICENSED` as
     the hub is; a licence file is still owed the day anything leaves the account); and
     the honest cost: the bullet was written against a specific failure — glossy
     mobile-game character art — and narrowing it hands the judgement of "reads as 3D" to
     a reviewer's eye rather than to a rule, so the studio's site is where that judgement
     is made visible before anything ships.
   - **What would reopen this.** A render that a stranger reads as a game mascot rather
     than as craft (the second test on `direction.md` lines 292-299); a second character;
     or a licensing answer for `biscuit_pics` that forbids derived work from the
     photographs the model was built from.
   - **Related pages**: `direction.md`, `character.md`, `0010`, `0013`, `0017`, and
     `what-the-hub-owns.md`, as relative links.

4. **Narrow the Avoid bullet.** Replace lines 262-263 of `docs/design/direction.md`:

   before:

   ```markdown
   - Cartoon styling aimed at children, hyperrealism, 3D rendering, glossy mobile-game
     character art, or anything carrying generative-AI artefacts.
   ```

   after:

   ```markdown
   - Cartoon styling aimed at children, hyperrealism, 3D that reads as 3D — physically
     based materials, gloss, realistic lighting — glossy mobile-game character art, or
     anything carrying visible generative-AI artefacts. A cel render posed from the
     approved model is none of these; [decision 0018](../decisions/0018-renders-from-the-approved-model-may-ship.md)
     says where the line is.
   ```

   Nothing else on the page changes. Check the link resolves (`just check-docs`).

5. **Rewrite four passages of `docs/design/character.md`**, keeping every heading and
   every other paragraph:

   - Lines 25-32 (**What exists today**): keep "Nothing of her ships" as the first
     sentence about the hub, then add that the approved model exists in `biscuit_studio`
     (a code span, no link: the studio's handbook is published nowhere and the hub links
     out only from pages that already do) and is the reference sheet; the placeholder mark
     sentence ("set in type until an illustrator draws the real one") becomes "set in type
     until the real one is drawn from the model or by an illustrator".
   - Lines 89-98 (**The first pose set**): "Commissioned from an illustrator." becomes
     "Posed and rendered from the approved model in the studio, or commissioned from an
     illustrator; either way the set is a budget as much as a wish list:". The three
     bullets and the exclusion stand.
   - Lines 106-113 (**The character reference sheet**): the heading stays; the first
     paragraph says the sheet's job — proportions, colouring, face, ears, tail and paws
     fixed before any pose — is done by the approved model, which is posed rather than
     redrawn, and that a drawn pose is checked against a render of it. The brown
     paragraph (112-113) stands, with "measured against the model's coat" appended.
   - Lines 128-134 (**Reference material**): photographs stay in `biscuit_pics`; add that
     the model, its renders and the illustrations live in `biscuit_studio`, that the
     studio copies nothing from `biscuit_pics` but the model package and the cel set, and
     that the licensing sentence stands unchanged — "is not yet decided" is still true.

6. **The ownership row.** `docs/project/what-the-hub-owns.md` line 29 becomes:

   ```markdown
   | Biscuit, and how she is used | [The Biscuit character](../design/character.md); her assets are made in `biscuit_studio` |
   ```

   The "What is not settled" list (125-138) gains nothing: the licence question is
   already recorded on `character.md`, and C04 is where the ownership page grows a
   paragraph about the studio.

7. **Run `consumer-impact`** (H `.agents/skills/consumer-impact/SKILL.md`). Steps 2 and 3
   sort the change: nothing in the package moved, so there is no version; the pages moved,
   so step 5 applies. Step 6: Poodl restates no sentence of `character.md` or
   `direction.md` (check with `grep -rn -i 'illustrator\|3D rendering\|generative' /Users/scutting/projects/poodl/docs/`);
   if nothing is found, write "nothing to Poodl" in the hand-back notes and leave
   `poodl-handover.md` untouched; if something is found, write the item there in that
   page's register.

8. **Add the manifest entry and the index row** exactly as the existing ones are shaped:
   the manifest entry after line 63 (`0017`), the row after line 43 of
   `docs/decisions/README.md`. Run `just check-docs`, then the hub's full `just check`.

9. **Authorisation required:** pushing the branch and opening the hub pull request. Stop
   and ask. After the merge, set this ticket's `status: done` in the studio and commit
   that on `ticket/c01-hub-brand-rule` in the studio; pushing that is authorised
   separately too.

## Acceptance criteria

- [ ] `0018` exists with the frontmatter above, the four sections, and is registered
      (`docs/manifest.yml`) and indexed (`docs/decisions/README.md`); `just check-docs` in
      the hub is green.
- [ ] `docs/design/direction.md` differs from `main` only at the one bullet, and the
      bullet links `0018`.
- [ ] `docs/design/character.md` differs from `main` only inside the four passages, and
      "is not yet decided" (line 133) is still present.
- [ ] `0018` acknowledges 0013's "consumer that is not a game" trigger with the verb
      **overruled on** and a date, and gives the reason.
- [ ] `0018` states, in one place, what does not change: one face, rare breaks, motion
      off reduces to the mark, boundaries only, no first person.
- [ ] The `consumer-impact` outcome is recorded in the hand-back notes, and
      `poodl-handover.md` changed only if an item was found.
- [ ] `package.json` and `CHANGELOG.md` in the hub are untouched.
- [ ] The hub's `just check` is green on the pull request; every push and the pull request
      were authorised first.

## Verification

In the hub worktree, on the branch:

```sh
git diff main --stat
git diff main -- docs/design/direction.md | grep -c '^[-+]  *- Cartoon'
grep -c 'is not yet decided' docs/design/character.md
grep -n 'overruled on' docs/decisions/0018-renders-from-the-approved-model-may-ship.md
just check-docs
just check
```

Expected: six or seven files in the stat (seven if the handover page gained an item); `2`
(one removed, one added line opening the bullet); `1`; one line; green; green.

## Hand-back notes

Filled in by the agent that executes this ticket.

- The decision number used, and the line numbers if they had moved.
- The `consumer-impact` finding: "nothing to Poodl", or the item written.
- The hub pull request and its check outcome.
- What was handed to C04 (anything the ownership page wanted beyond one row).
- Which authorisations were asked for and given, with dates.

## Open points

- Whether "vetted by the maintainer" needs a mechanical trace in the hub or only in the
  studio's manifest. Recommend the studio alone: the hub records rules, not pictures.
- Whether narrowing the bullet should wait for a rendered pose the maintainer can look at
  beside the wordmark, so the "reads as 3D" line is drawn against an example. Recommend:
  land the record now (the studio's site is where the example will be seen) and reopen
  if the first render fails the test.
- Whether `0010`'s "Mascot and favicon deferred" and `0017`'s `MascotSlot` refusal gain a
  **carried out on** mark now. They do not: no asset has arrived. C04 records what the
  hub is waiting for.
