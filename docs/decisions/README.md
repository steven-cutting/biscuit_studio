---
title: "Architecture decisions"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_index]
requires: []
---

# Architecture decisions

A record of what was chosen, what it cost, and what would have to change for the choice
to be revisited. Each entry is numbered and never renumbered; a decision that is
superseded is marked rather than deleted, because the reasoning is what makes the
successor legible.

These are decisions about how this repository is built. What the platform's surfaces do is
decided in the hub's specifications and cited through
[The platform upstream](../project/platform.md); the studio adds no rule of its own.

## The record

| Number | Decision |
| --- | --- |
| [0001](0001-static-site-no-backend.md) | A static site with no backend |
| [0002](0002-the-hub-is-upstream.md) | The hub is upstream |
| [0003](0003-python-toolchain.md) | A Python toolchain in a frontend repository |
| [0004](0004-a-project-pages-site.md) | A project Pages site |
| [0005](0005-assembled-by-hand.md) | Assembled by hand, not rendered from the template |
| [0006](0006-sources-in-lfs-served-files-as-blobs.md) | Sources in LFS, served files as blobs |
| [0007](0007-assets-travel-by-copy-and-ledger.md) | Assets travel by copy and ledger |
| [0008](0008-the-viewer-is-embedded-as-is.md) | The viewer is embedded as-is |
| [0009](0009-no-component-workshop-yet.md) | No component workshop yet |

## The numbering

The series is the studio's own and starts at 0001. The first four were taken from the
Biscuit Games template's records — its 0001, 0008, 0004 and 0010, in that order — and
generalised for a repository that is not a game, and each says so under its heading. The
other five were written here. The hub's records and a game's are numbered independently,
so a bare number means nothing without the repository; where a page here cites one of the
hub's, it says so. A slug never moves.

## Writing a new one

Copy the shape of an existing entry: context, the decision, the consequences including
the ones that hurt, and what would reopen it. Add the file, add a manifest entry, add a
row above. A decision nobody can find is not recorded.

Superseding one is that work plus a mark. The successor is a new numbered entry with a topic
slug of its own. The old entry keeps its number, its file, its topic slug and every word of its
reasoning, and gains a dated blockquote directly under its level-one heading saying what
replaced it and when; its row above gains the same sentence after an em dash. Nothing is
deleted and nothing is rewritten, because the reasoning is what makes the successor legible.

Three verbs, and they mean different things. A record is **superseded by** a successor that
replaces its answer, **narrowed by** one that changes part of its letter and none of its
reasoning, and **carried out on** a date when what it planned actually happened — the third is
not a supersession at all, and its mark sits beside the paragraph that stopped being true
rather than at the top. A fourth reads a reopener rather than a decision: a trigger is
**overruled on** a date when a later record acts without it, which is not the same as the
trigger firing and must never be written as though it were. A slug never moves, whichever
verb applies, because a slug is what a cross-repository reference names.

## Related pages

- [Documentation map](../README.md)
- [The platform upstream](../project/platform.md)
- [Architecture](../explanation/architecture.md)
