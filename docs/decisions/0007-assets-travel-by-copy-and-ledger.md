---
title: "Decision 0007: Assets travel by copy and ledger"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_asset_distribution]
requires: []
---

# Decision 0007: Assets travel by copy and ledger

## Context

A finished asset made here is meant for the hub or a game: a render of Biscuit for a header,
a favicon, a pose where the hub's character page expects one. It has to reach them
somehow.

The hub has been here before. Its decision 0013 moved the design system into a package
because copies drifted: every copy was correct on the day it was made and unverifiable from
the next, and nothing compared two copies of the same file. A package fixed that for code
and tokens.

The studio's assets are not a package's business. A game installs a stylesheet and a
component, not a `.blend`, twenty textures and a 26 MB viewer; and a package would make the
hub and every game depend on the studio, when the direction runs the other way — the studio
consumes the hub, and the hub never depends on the studio.

## Decision

A finished asset reaches the hub or a game by copy. Every copy is to be recorded in a
structured ledger, with a small command-line tool that makes the copy, so that a copy is
deterministic and a consumer's CI can verify that the bytes it holds are the bytes the
ledger names. The design of that ledger is a separate discussion and is not settled here.

Until it lands, the interim procedure on
[Promote an asset](../how-to/promote-an-asset.md) stands: copy by hand from a named studio
commit, record that commit and the manifest's sha256 beside the file in the consumer, and
write the item into [Hub handover](../operations/hub-handover.md) in this repository.

## Consequences

**Two copies exist, and nothing compares them yet.** The consumer's file and the studio's
share a hash on the day of the copy and nothing after. Until the ledger exists, review is
the whole check.

**A promoted asset is frozen at a commit.** A rebuild here changes nothing there. A
consumer that wants the new version copies it again and records the new commit.

**The hub's rule gates the first promotion.** The hub's design direction page lists 3D
rendering and generated artefacts under Avoid, so nothing is copied out until a hub
decision permits cel-shaded renders from the approved model; see
[Decision 0002](0002-the-hub-is-upstream.md).

**The dependency direction holds.** No consumer installs, clones or fetches the studio.
A consumer's build is never broken by a change here, which is the other side of the first
consequence.

## What would reopen this

The ledger landing, which narrows this record rather than superseding it: the copy stays,
and the interim procedure is replaced by the tool. The hub choosing to install assets as a
package after all, which would reverse the dependency direction and supersede this.

## Related pages

- [Promote an asset](../how-to/promote-an-asset.md)
- [Hub handover](../operations/hub-handover.md)
- [The platform upstream](../project/platform.md)
- [Decision 0002: The hub is upstream](0002-the-hub-is-upstream.md)
