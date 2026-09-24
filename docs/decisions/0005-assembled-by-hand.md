---
title: "Decision 0005: Assembled by hand, not rendered from the template"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_assembled_by_hand]
requires: []
---

# Decision 0005: Assembled by hand, not rendered from the template

## Context

Every Biscuit Games game starts from the Copier template, `steven-cutting/biscuit_games_template`,
and takes its updates through `copier update`. The studio needs most of what the template
carries — the toolchain, the hook gate, the agent contract's shape, the app shell, the Pages
workflow — and several things it does not have.

The template renders only a game. It asks four questions and has no toggle for a
repository that is not one: every render carries Storybook and Chromatic, the
specification gates and a `docs/specs/` directory, and a handbook written for a game. The
studio needs none of those, and needs an asset gate, Git LFS and pages the template has
never heard of.

Rendering and then deleting does not survive. A render whose handbook pages were removed
breaks on its next `copier update`, because `docs/manifest.yml` is a rendered file: the
update restores the entries for pages that no longer exist, and the documentation contract
refuses a manifest entry with no page.

## Decision

Assemble the studio by hand. Copy the generic pieces by path from the hub, Poodl, the
template and the tooling repository, each at a named commit, and take no Copier link: no
`.copier-answers.yml`, and nothing that `copier update` could act on.

Each file's source is recorded. The groups and the commits they came from are in the
table on [Repository map](../project/repository-map.md), and the agent contract's
Provenance section names the same commits.

## Consequences

**Toolchain changes arrive by hand.** A fix the template ships to every game does not
reach the studio on its own. Someone reads the template's changes and the tooling
package's changelog and carries what applies, one file at a time; see
[Maintain dependencies](../how-to/maintain-dependencies.md).

**The studio can diverge without a template change.** No workshop, an assets gate, LFS,
no specifications, and a deploy that waits for CI are all the studio's own choices, made
without asking the template to grow an option for one repository.

**Provenance is a table a person maintains.** Nothing checks that a copied file still
matches its source, or that the table names every file. The commits are pinned in the
table so a later comparison is possible, not automatic.

## What would reopen this

The template growing a shape for a repository that is not a game, which would make a
render with an update path worth more than a hand-assembled copy. A third repository that
is neither a game nor the hub, which would make that shape worth building.

## Related pages

- [Repository map](../project/repository-map.md)
- [The platform upstream](../project/platform.md)
- [Maintain dependencies](../how-to/maintain-dependencies.md)
