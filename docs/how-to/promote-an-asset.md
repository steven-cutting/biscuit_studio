---
title: "Promote an asset"
kind: "how-to"
audience: [maintainer, agent]
canonical_for: [asset_promotion]
requires: []
---

# Promote an asset

Promotion is a finished asset leaving the studio for the hub or a game. It happens by copy:
nothing installs the studio, and the hub never depends on it. This page is the interim
procedure. A structured ledger with a small command-line tool, so that a copy is
deterministic and a consumer's CI can verify it, is the intended replacement, and its
design is a separate discussion; until it lands, a copy is made by hand and written down
on both sides. See [Decision 0007](../decisions/0007-assets-travel-by-copy-and-ledger.md).

## When an asset may leave

Not yet. Nothing made here is promoted until the hub permits it.

The hub's design direction page lists 3D rendering and anything carrying generative
artefacts under Avoid, and its character page expects Biscuit to be drawn by a
commissioned illustrator against a reference sheet. The approved model is cel-shaded 3D,
and the cel set was generated. Both are built and shown here regardless, because the
studio's own site is the studio's business. But putting either into the hub or a game
would break a rule the hub has not changed, and the platform's rules change in the hub
first.

A hub decision that permits cel-shaded renders from the approved model, and generated art
the maintainer has vetted, is what opens the door. Until that decision is recorded in the
hub, and the two pages say what it permits, a request to promote something waits. See
[The platform upstream](../project/platform.md) for where those pages are.

## The interim procedure

Once promotion is permitted, and for each file:

1. **In the consumer** — the hub or a game, in its own repository — copy the file with
   `cp` from a checkout of this repository at a named commit. Take the commit from
   `git rev-parse HEAD` in that checkout, and check the copy with `shasum -a 256` against
   the file's entry in `assets/manifest.json`.
2. **In the consumer, beside the file,** record the studio commit and the sha256 from the
   manifest, in whatever form that repository records a copied file's provenance. A later
   reader of the consumer must be able to find the exact bytes it came from without asking.
3. **In this repository,** write the item into [Hub handover](../operations/hub-handover.md),
   in that page's own register: narrative, grouped by the shape of what is owed, naming
   the consumer, the file, the studio commit and the hash.
4. **Never edit the other repository from here.** Every change in the hub or a game is
   made there, in its own change, and each one needs the maintainer's explicit
   authorization at the time. An agent working in this repository stops at step 3 and
   hands the rest back.

This is the register the hub already keeps for what cannot travel in its package: its
consume-the-hub page lists what still travels by citation, and its Poodl handover records
what the first game owed and took. A copy is written down where it was made and where it
was taken, so that either side can find the other.

## What the copy does not buy

- **Nothing compares the two files afterwards.** Once copied, the consumer's file and
  this repository's are two files that happen to share a hash, and no gate on either side
  notices when one of them changes.
- **A rebuild here changes nothing there.** A promoted asset is frozen at the commit it
  was copied from. If the model is rebuilt and approved again, every consumer still holds
  the old bytes until someone copies the new ones and records that too.
- **No consumer's gate can say so yet.** That is exactly what the ledger is for: a
  consumer's CI reading a structured record of each copy and failing when the bytes and
  the record disagree. Until it exists, the handover page and the consumer's own note are
  the whole record, and review is the whole check.

## What is promoted first

The hub is waiting on Biscuit herself. Its character page says that nothing of her ships
today. Its decision 0010 deferred the mascot and the favicon, and refused to ship a
placeholder slot for poses that did not exist. Its decision 0017 extracted the brand mark
as `Monogram`, which is still set in type rather than drawn from the dog. The favicon, a
real `Monogram` and the poses a `MascotSlot` would show are what the hub would take first.
Whether any of them is made from the approved model, and which render, is the hub's
decision to make once its rule permits it. This page does not make it.

## Related pages

- [Hub handover](../operations/hub-handover.md)
- [The platform upstream](../project/platform.md)
- [Decision 0007: Assets travel by copy and ledger](../decisions/0007-assets-travel-by-copy-and-ledger.md)
- [Import an asset](import-an-asset.md)
