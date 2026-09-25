---
title: "Content policy"
kind: "explanation"
audience: [user, contributor, maintainer, agent]
canonical_for: [content_policy]
requires: []
---

# Content policy

The studio is built from a larger working repository, `biscuit_pics`, that holds much more
than the studio may carry: photographs of the real dog, other people's art, commercial
fonts and a great deal of discarded work. This page owns the rule for what crosses into
this repository and what never does, how generated art is labelled, and what is still
undecided. Every import, rebuild and review answers to it.

## Never committed

**Photographs of the real dog, unless approved and stripped.** The source repository holds
163 photographs of Biscuit under `biscuit_pics/raw/`, and the camera's EXIF block survives
whole in 68 of them. None is
committed here without the maintainer's approval of that particular photograph, and none
with any metadata field left in it. Copying one into this repository is an action of its
own that needs its own authorisation at the time; approval of one photograph is not approval
of the next, and nothing in the first release copies any.

**The reference art.** The source repository's `inspiration/` folder holds about a hundred
and ten images of other studios' and artists' work and fan art, indexed there as style
references only. It is third-party copyrighted material. None of it is committed here, in
whole or in part, and nothing derived from it is presented as the studio's.

**The two commercial fonts.** `OptimaNovaLT-Black.ttf` and `KoreanKRSM.ttf`, under the source
repository's `generated/katherine/dialogue/p5ui/fonts/`, are licensed typefaces. They are
never committed, and the site uses only the two faces the platform package ships.

**The work that did not make it.** Four more parts of the source repository stay there, each
for its own reason:

- `generated/bad/` is rejected work, kept there as a record of what was tried.
- `generated/3d/` is the rebuild chain: 1.9 GB of earlier studies the model's build reads.
  It is cited by path and commit and reached through a link placed only for the length of a
  rebuild; see [Rebuild the model](../how-to/rebuild-the-model.md).
- `model_sheets/` is a separate pipeline whose tiles were generated through an image model
  and carry the same open question as the cel set. It may be revisited.
- `ai_tmp/` is a discarded browser profile, and holds nothing worth keeping.

## Generated art is labelled

The eleven cel illustrations under `assets/illustrations/good/` were made with an image
model, ChatGPT, and picked by hand; the source repository's commit that added them says so.
The studio labels them in three places: every entry in `assets/manifest.json` carries a
`source` naming the file in the source repository at the commit it came from, the gallery
page says in its own words how the drawings were made, and this page says so here.

Whether any of them may leave the studio — into the hub or a game — is the hub's decision,
not the studio's. The hub's design direction lists generated artefacts under what to avoid,
and the studio waits on a hub decision permitting vetted generated art before promoting any.
[The platform upstream](../project/platform.md) points at the pages that decide it.

## The licence is open

The hub's character page says that the licensing of the source repository's material is not
yet decided. The studio inherits that question and does not answer it. Until the maintainer
decides:

- every entry in `assets/manifest.json` carries `licence: "unsettled"`, and the field exists
  so that the answer, when it comes, is a reviewable diff;
- `package.json` says `UNLICENSED`, as the hub's does, and this repository generates no licence
  file;
- an agent or contributor who finds they need an answer records the question and stops,
  rather than choosing a licence on the maintainer's behalf.

Whether the packed textures in the Blender scene were painted from photographs of the dog is
also unknown. They carry no metadata and pass the checker; the question stays with the
licence.

## What enforces it

`just check-assets` enforces the part a machine can see. It refuses any image carrying an
EXIF field beyond its resolution, naming each one — the GPS block, the camera, the date —
and refuses any TIFF outright, because a TIFF's structure is stored as the same tags and
cannot be told from metadata. A photograph that still carries its camera data cannot pass
the gate.

Review enforces the rest, because no gate can tell a permitted image from a forbidden one. A
stripped photograph, a crop of someone else's art and a drawing made here are all PNG files
with clean headers. What stops the wrong one is a person reading the change, the manifest's
`source` field saying where each file came from, and the procedure in
[Import an asset](../how-to/import-an-asset.md).

## Related pages

- [Import an asset](../how-to/import-an-asset.md)
- [Asset manifest](../reference/asset-manifest.md)
- [Security model](security-model.md)
- [Purpose and scope](../project/purpose-and-scope.md)
