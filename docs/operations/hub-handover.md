---
title: "Hub handover"
kind: "operations"
audience: [maintainer, agent]
canonical_for: [hub_handover]
requires: []
---

# Hub handover

**Nothing here has happened.** Every item below is a change to another repository — the hub,
or a game — or a wait on one, and not one of them has been made. This page is the ledger of
what is owed in each direction between the studio and the platform, not a record of work
done. Read it as the current state of the debt, and assume the hub still looks exactly as it
did when the studio was assembled.

Editing another repository needs explicit authorization for each action, and approval for
one action is not approval for the next. This repository records what another repository has
to change; it never changes it. An agent working here writes the item down and stops —
including when the fix is obvious, small, and one command away.

The items are grouped by shape rather than by urgency: what the hub owes the studio, what the
studio will owe the hub, what a promoted asset carries when it goes, and the standing cost
every cross-repository reference carries afterwards.

## What the hub owes the studio

**The brand rule.** The hub's design direction page lists 3D rendering, and anything carrying
generative-AI artefacts, under what to avoid, and its character page expects Biscuit to be
drawn by a commissioned illustrator against a reference sheet. The studio's approved model is
cel-shaded 3D and its eleven drawings were generated. What the studio waits on is a hub
decision record, with matching edits to both pages, that permits cel-shaded renders from the
approved model and generated art the maintainer has vetted. The studio's own site is built
regardless, because showing its work here promotes nothing. Until that decision lands in the
hub, nothing made here is promoted into the hub or a game, and a change that needs to promote
something waits.

**Registering the studio.** The hub's repositories table and its page on what the hub owns
know two kinds of repository, a hub and a game, and nothing else. The studio is neither: it
consumes the package as a game does, but it makes assets rather than playing anything. The
hub owes a row for the studio in that table, a sentence on its boundary page saying what a
studio holds, and a handover section of its own for what it expects from the studio. That
follows the brand rule rather than preceding it, because a registered studio whose work may
not be used would be registering a dead end.

**The window before hydration.** The studio's pages carry the platform default in the
markup — `data-animations="on"` and no `data-high-contrast` — and the layout writes the
device's answer only after hydration. Between first paint and hydration, a device asking for
reduced motion gets the platform's motion durations at their `on` values, and a device asking
for more contrast gets the standard palette. Nothing on the studio's pages animates before
hydration, so the motion half is latent here; the contrast half is visible on every first
paint. The studio cannot close either without a second opinion on the attribute, which the
hub's accessibility page rules out: it calls the attribute the single gate for motion, and a
component's own media query a second opinion on the same question. What the hub can do, in
its `app.css`: a `prefers-contrast: more` rule selecting the high-contrast palette, which that
page already names as the smaller debt and the one to pay first, and a root-level
`prefers-reduced-motion: reduce` rule holding the durations at zero, which is the hub's to
weigh against its stance on the single gate. A game that follows the hub's consumption guide
has the same window.

**What the hub is waiting on art for.** Three things in the hub were deferred until there
was art of Biscuit to put in them, and each is something the studio could supply once the
brand rule permits it. None is decided here, and none is offered until the hub asks.

- *The favicon.* The hub's decision that landed the design system deferred the favicon with
  the mascot, and `src/app.html` in the hub, like the studio's own, still carries an empty
  icon.
- *The real `Monogram`.* The character page's account of what exists today is a placeholder
  mark — the brand initial in a ruled square, set in type until an illustrator draws the real
  one — and nothing in it is drawn from the dog.
- *The `MascotSlot` poses.* The hub's decision porting the rest of the design system refused
  `MascotSlot` because its trigger, the illustrated poses, did not exist. A render of the
  approved model in one of its four poses is the kind of thing that trigger was waiting for,
  if the hub decides a render may stand in for an illustration.

- *An address under the platform's domain.* The studio is served beneath the account's
  user-site domain, at `stevencutting.com/biscuit_studio/`, because the platform's domain
  sits on Poodl's repository and the hub deferred moving it. When that move happens, where
  the studio sits under the new root is the hub's to say, and the studio's deployment page
  and its address decision change to follow.

## What the studio owes the hub

Nothing, until the brand rule changes. The studio holds nothing the hub has asked for, and
offering an asset the hub's own pages forbid would be asking the hub to change its rule by
the back door.

After the rule changes, the studio owes the first promoted assets, each copied by the interim
procedure in [Promote an asset](../how-to/promote-an-asset.md) and recorded in the section
below. It also owes its half of the ledger that replaces that procedure: a structured record
with a small command-line tool, so that a copy is deterministic and a consumer's gate can
verify it. The ledger's design is a separate discussion and is not settled here; see
[Decision 0007](../decisions/0007-assets-travel-by-copy-and-ledger.md).

## What a promoted asset carries

Nothing has been promoted, so this section holds no entry yet. When an asset leaves, it is
written here as a paragraph, not a checkbox, and it carries five things: the studio commit the
copy was taken from; the sha256 the file has in `assets/manifest.json` at that commit; its
path here; its path in the repository that received it; and the date of the copy. The
receiving repository records the same commit and sha256 on its side, so that either end can
find the other.

A later change here to a promoted asset — a rebuild, a replacement, a fix — is written here
too, as a new paragraph under the first, saying what changed and what the consumer would do
to take it. The copy there does not update by itself, and nothing there notices; see
[Maintenance](maintenance.md).

## What a cross-repository link costs

Once a reference crosses a repository boundary it stops being a path and becomes an absolute
URL, and almost nothing checks it.

- The documentation contract skips them entirely. `bg-validate-docs` ignores any absolute URL
  and any `mailto:`, so the exact-case, must-resolve rule that governs every internal link
  does not apply.
- The offline link checker skips them too. The lychee run inside `just check-docs`, and the
  identical one in the commit hook, pass `--offline`.
- Only `just check-links-online` resolves them. It needs the network, so it sits outside
  `just check` deliberately, and it is run by hand — monthly, per
  [Maintenance](maintenance.md).

The consequence is worth stating plainly, because it is permanent rather than a gap someone
will close: a hub page renamed or moved rots silently here, for a month at best and in
practice for however long it is until someone runs the manual recipe. Nothing in the studio's
gate fails when it happens. Nothing in the hub's gate fails either. That is why the studio's
links into the hub live on one page, [The platform upstream](../project/platform.md), and
nowhere else.

Two habits follow. **Prefer whole-page links**, because heading fragments across repositories
are checked by nothing at all — the offline checker will not resolve the page to look for the
anchor, and the online one verifies the page rather than the fragment. And **treat a hub page
path as part of the studio's interface to the hub**: when a link on the platform page breaks,
the fix is a one-line edit there, but when a page the studio relies on disappears, that is an
item for this ledger, written before anything here is changed to suit it.

## Related pages

- [Promote an asset](../how-to/promote-an-asset.md)
- [The platform upstream](../project/platform.md)
- [Maintenance](maintenance.md)
- [Decision 0007: Assets travel by copy and ledger](../decisions/0007-assets-travel-by-copy-and-ledger.md)
