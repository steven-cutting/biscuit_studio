---
name: hub-handover
description: Record what the hub or a game owes when an asset made here is ready to leave.
---

# Hand an asset to the hub or a game

1. Read `AGENTS.md`, `docs/how-to/promote-an-asset.md` and `docs/operations/hub-handover.md`. This repository records what another repository has to change; it never changes it. Editing the hub, a game or `biscuit_pics` needs explicit authorization for each action, and approval for one is not approval for the next.
2. Check the hub permits the asset at all. Until the hub's design direction permits renders from the approved model and vetted generated art, nothing made here is promoted; the item is recorded as waiting, and the ticket that changes the hub is named.
3. Name the bytes exactly: the path under `assets/` or `static/pose-studio/`, the sha256 the manifest records, and this repository's commit. That triple is what the consumer records beside its copy, and what a verifier compares.
4. Write the item into `docs/operations/hub-handover.md` in that page's own register — prose grouped by shape, never a checkbox — naming the receiving repository, the file to add there, where the bytes come from, and what the receiving repository's own rules say about it (the hub's `MascotSlot`, favicon and mark are the standing examples).
5. Run `just check-docs`, then `just check`. Hand back with the item's text quoted and every authorisation still to be asked for listed.
