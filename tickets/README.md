# Tickets for building `biscuit_studio`

This directory is the work breakdown for setting up the Biscuit Games studio: the
repository where the platform's graphical assets are developed, and the static site on
GitHub Pages that shows them. Each ticket is written for an AI agent with no other context,
working in its own git worktree. `CONVENTIONS.md` is the shared design every ticket obeys
and cites by section; read it first, then the ticket.

Filing these as GitHub issues, creating the GitHub repository, pushing, tagging and opening
pull requests are separately authorised actions. Nothing here has been filed, and the
repository exists only as a local clone with one empty commit.

## Index

Build tickets, in dependency order. The `status:` field in each ticket's frontmatter is
authoritative; this table is a snapshot.

| Id | Title | File | Depends on | Parallel with | Status |
| --- | --- | --- | --- | --- | --- |
| S00 | Foundation: toolchain, contracts, large-file policy, the asset checker, an empty site, stubs for every path | `S00-foundation.md` | none | none | open |
| S01 | Site shell: the platform package, the lockup, appearance on the document element | `S01-site-shell.md` | S00 | S02 to S06 | open |
| S02 | Asset import: the approved model and the cel set from `biscuit_pics`, LFS, the manifest | `S02-asset-import.md` | S00 | S01, S03 to S06 | open |
| S03 | Showcase routes: the model page around the embedded viewer, and the gallery | `S03-showcase-routes.md` | S01, S02 | S04 to S06 | open |
| S04 | Workflows: `ci.yml` with three jobs, `pages.yml` through the shared workflow | `S04-workflows.md` | S00 | S01 to S03, S05, S06 | open |
| S05 | Handbook A: project, tutorial, how-to pages and the decision records | `S05-handbook-a.md` | S00 | S01 to S04, S06 | open |
| S06 | Handbook B: explanation, reference and operations pages | `S06-handbook-b.md` | S00 | S01 to S05 | open |
| S09 | Follow-up: what S00 to S06 handed back to tickets that are done | `S09-follow-up-hand-backs.md` | S01 to S06 | none | open |
| S07 | Repository: create it, bootstrap its settings, first push, first deploy | `S07-repository.md` | S01 to S06, S09 | S11 | open |
| S08 | Maintainer docs: `README.md`, `CHANGELOG.md` 0.1.0, `AGENTS.md` provenance | `S08-maintainer-docs.md` | S07 | S11 | open |
| S10 | Gallery thumbnails: WebP copies of the cel set, made by a recipe and listed in the manifest | `S10-gallery-thumbnails.md` | S08 | S11 | open |
| S11 | The rebuild, run end to end: the success and interrupted paths of `scripts/rebuild_model.sh` | `S11-rebuild-success-path.md` | S09 | S07, S08, S10 | open |
| S12 | Domain: the studio's address when the platform moves to `pnut.fans` | `S12-platform-domain.md` | S07, the hub's decision | S08, S10, S11 | open |
| S13 | Model update: the approved model re-imported from `biscuit_pics` at `891c44c` | `S13-model-update.md` | S02, S08 | S10, S11, S12 | done |

Cross-repository and design tickets. Each is a recommendation written to be picked up on
its own; C01 is the one that gates anything leaving the studio.

| Id | Title | File | Depends on | Status |
| --- | --- | --- | --- | --- |
| C01 | The hub permits renders from the approved model: a hub decision, `direction.md` and `character.md` | `C01-hub-brand-rule.md` | none; before any asset is promoted | open |
| C02 | The asset ledger: a design for deterministic, CI-verifiable copies | `C02-asset-ledger-design.md` | S02 | open |
| C03 | A three.js viewer inside the shell, retiring the embedded file | `C03-threejs-viewer.md` | S03, C01 | open |
| C04 | The hub registers the studio: its repositories table, the boundary page, a handover section | `C04-hub-registers-the-studio.md` | C01 | open |

## Dependency graph

```text
S00 ──┬── S01 ──┬── S03 ──┐
      ├── S02 ──┘         │
      ├── S04 ────────────┼── S09 ──┬── S07 ── S08 ── S10
      ├── S05 ────────────┤         │
      └── S06 ────────────┘         └── S11

C01 ── C04
C02 waits for S02 (the manifest exists)
C03 waits for S03 and C01
```

The graph is acyclic: S00, then five lanes (S01, S02, S04, S05, S06) in parallel, S03 once
S01 and S02 have merged, then S09 (the follow-up that carries what the lanes handed back
to tickets already done), then S07 and S08 in sequence, and S10 after S08. S11 needs only
S09 and runs beside the rest. The C tickets stand apart; C01 can
start at any time because it touches only the hub.

## How to pick up a ticket

1. Create a worktree on the branch the ticket's `branch:` field names, from `main`, after
   every ticket it depends on has merged. Below, `<branch>` is that field, which is
   lowercase (`ticket/s02-asset-import`), and `<id>` is the ticket id (`S02`):

   ```sh
   supacode repo worktree-new --branch <branch> --base main --name <id>
   ```

   Outside a Supacode terminal:

   ```sh
   git worktree add ../<id> -b <branch> main
   ```

2. Read `CONVENTIONS.md`, then the ticket. Read the source files the ticket names in the
   clones `CONVENTIONS.md` §0 pins, at the commits it pins. `biscuit_pics` is read-only.
3. Edit only the files the ticket lists, plus the `status:` line of the ticket itself. A
   change needed elsewhere is handed back in the ticket's hand-back notes, not made.
   A ticket that is done, or in progress, is never reopened: what is handed back to it
   goes into a follow-up ticket, and only a ticket nobody has started is amended in place
   (CONVENTIONS.md §9).
4. Run the ticket's verification commands and quote their output in the hand-back notes.
5. Commit on the ticket branch. Pushing and opening the pull request are separately
   authorised: stop and ask.

## Definition of done

For a build ticket: `just check` is green in this repository, the ticket's acceptance
criteria are met, its verification commands ran with the output quoted in the hand-back
notes, every open point is answered or explicitly carried forward, and the ticket's
`status:` is `done` in the same pull request.

For a cross-repository or design ticket: the recommendation is implemented where the
ticket says, its acceptance criteria are met, and every action that touches another
repository or a repository setting was authorised before it was taken.

## Ticket format

Every ticket carries frontmatter (`id`, `title`, `status`, `depends_on`, `parallel_with`,
`branch`, `estimated_size`) and these sections in this order: Context, Goal, Non-goals,
Files touched, Steps, Acceptance criteria, Verification, Hand-back notes, Open points.
Repository paths are written as code spans, never as links, because the hook gate S00
installs runs lychee offline over this directory.

Ids: `S` is a build ticket executed in this repository; `C` is a cross-repository or design
ticket. A follow-up that C02 writes for another repository is filed here too, with the
prefix `G` (executed in `biscuit_games_tooling`) or `H` (executed in `biscuit_games`), and
is added to the tables above when it is written.
