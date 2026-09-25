---
title: "Decision 0002: The hub is upstream"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_hub_upstream]
requires: []
---

# Decision 0002: The hub is upstream

*Carried from the Biscuit Games template's decision 0008 at `2283589`, and restated for a repository that is not a game.*

## Context

The hub, `steven-cutting/biscuit_games`, decides how Biscuit Games looks and publishes it as
`@steven-cutting/biscuit-games`. The package carries the stylesheet and the typefaces; the
chrome every surface wears — `HeaderBar`, `Wordmark`, `Monogram` and the rest of the
components it exports; the preferences port with its fake; and the platform's three
specification modules. The hub also decides Biscuit herself: her look, her registers and
where she may appear, on its character and design direction pages.

Poodl ported a copy of the design system in first and replaced it with the package once
the hub existed. Its record explains what the copy cost: every copy was correct on the day
it was made and unverifiable from the next, and nothing anywhere compared the two.

The studio is where pictures of Biscuit are made, which puts it closer to the hub's
authority than any game. It starts with the package and has nothing to delete.

## Decision

The hub is upstream of the studio, for the look and for the character alike.

- **Installed exactly.** The version `package.json` pins, no caret, matching invariant 4.
  GitHub Packages authenticates every read, so a committed `.npmrc` names the registry for
  the scope and holds no token; the token is a contributor's own in `~/.npmrc`, and in CI
  it is `github.token`, the one GitHub mints for the run, granted `packages: read`.
- **The studio restates no figure and no clause.** It adds no rule of its own, so it has
  nothing to hold equal to the platform's text: every figure it wears arrives in the
  stylesheet and the components, and every rule its surfaces obey is the package's.
- **No workshop composes the hub's.** The studio authors no shared component and runs no
  component workshop; see [Decision 0009](0009-no-component-workshop-yet.md).
- **One page points outward.** [The platform upstream](../project/platform.md) is where
  this handbook hands a reader to the hub, and it is the only page here that does.
- **The character and the aesthetic are the hub's, so the studio changes the hub first.**
  Where the studio needs the platform to permit something it forbids today, the hub's
  decision and pages change before anything here relies on it. The first such change is a
  hub decision permitting renders from the approved model, which the hub's design direction
  page today lists under Avoid.

## Consequences

**A first run needs a credential.** There is no anonymous install, and the registry answers
an unauthenticated read by naming the package rather than the missing token — a 404 that
sends a reader to look for the wrong fault. That is the honest price of the mechanism, and
it is written down where a first run meets it, including the troubleshooting page.

**A build here can fail because of something that happened there.** That is the point:
drift becomes a version number in a lockfile rather than a difference nobody can see. What
it costs is that a platform release nobody has read can break this repository's gate, and
the gate is the only thing that will ever say the studio is behind.

**The cross-repository links rot silently.** Nothing offline checks them, and
`just check-links-online` is monthly and manual.

**The studio's own output is gated by a page it does not own.** The model is approved and
the cel set is vetted, and neither may leave the studio until the hub's pages say so.
The studio can build, keep and show them, and cannot promote one; see
[Promote an asset](../how-to/promote-an-asset.md). The timing of the studio's first
promotion is the hub's to decide.

## What would reopen this

A contributor the token scheme cannot serve. A component or a token the studio needs and
the platform will not take. The platform publishing its handbook, which would turn the
citations into something a package carries. The hub declining to permit renders from the
model at all, which would leave the studio making assets no consumer may use, and would
reopen what the studio is for rather than only this record.

## Related pages

- [The platform upstream](../project/platform.md)
- [Maintain dependencies](../how-to/maintain-dependencies.md)
- [Hub handover](../operations/hub-handover.md)
- [Quality gates](../reference/quality-gates.md)
