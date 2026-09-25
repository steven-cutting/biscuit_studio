---
title: "Accessibility"
kind: "explanation"
audience: [user, contributor, maintainer, agent]
canonical_for: [accessibility_model]
requires: []
---

# Accessibility

Accessibility here is inherited, not invented. The platform specifies what every Biscuit
Games surface owes a reader, the package ships those obligations with the components that
discharge them, and the studio's part is to wear the components unchanged and to add
nothing that breaks a promise it did not write. This page says what arrives, what the
studio does about it, where the viewer falls short, and how the rest is checked.

## What the studio inherits

The platform's three Allium modules arrive with `@steven-cutting/biscuit-games`, under
`node_modules/@steven-cutting/biscuit-games/docs/specs/`, and every `@guarantee` clause in
them binds this site as it binds a game. The studio restates none of them and adds none.
The six on the `Appearance` surface are the ones its pages meet most directly:

- `SystemFollowsTheDeviceAsItChanges`
- `ReducedMotionOverridesTheAnimationSetting`
- `MoreContrastFromTheDeviceTurnsHighContrastOn`
- `AppearanceNeverCarriesMeaningAlone`
- `EveryCombinationMeetsTheLegibilityFloor`
- `AnUnavailableControlIsExempt`

They are stated over four combinations: the dark and light themes, each with high contrast
off and on. The palette the stylesheet declares for each is measured where it is declared,
in the hub. The account of what each guarantee means, what discharges it and what the
figures are belongs to the hub's accessibility page; read it through
[The platform upstream](../project/platform.md) rather than a summary here.

## What the studio does about it

`src/app.html` states `data-theme="dark"` and `data-animations="on"`, the platform
default, so the prerendered page paints something the guarantees already cover before
anything hydrates. After hydration, `src/lib/appearance.ts` derives `data-animations` and
`data-high-contrast` from the device through the preferences port the package exports, and
follows the device as it changes. That is more than the hub's own route does, which states
the default and reads no preference, and it is exactly what a game is told to do.

Between first paint and hydration the page carries the default whatever the device asked
for. Closing that window belongs to the platform's stylesheet rather than to a second
opinion here, and it is recorded as something the hub owes in
[Hub handover](../operations/hub-handover.md).

The site adds no colour of its own and no state that colour carries. Every style on the
three routes names a token from the package's stylesheet, the lockup is the platform's
`Wordmark`, and the only interactive elements are ordinary links with their own words.
There is nothing unavailable, nothing selected and nothing toggled for a colour to mean.

## The viewer

The pose studio at `static/pose-studio/viewer.html` is its own page, reached by a link, and
none of the above reaches it. It sits on a cream ground with its own type and its own
controls; no platform token, no theme attribute and no high-contrast palette applies there.
That is the known cost of embedding it unchanged, recorded in
[Decision 0008](../decisions/0008-the-viewer-is-embedded-as-is.md), and it is the first thing
a port into the platform's shell repairs.

What it does on its own terms:

- **Motion.** It never turns on its own. Auto-rotate starts off, is switched by a checkbox or
  the Space key, and stops the moment the device starts asking for reduced motion. It does
  not refuse a reader who turns it back on.
- **Keyboard.** Tab reaches every control and arrow keys adjust a focused slider; on the
  canvas, arrow keys orbit, plus and minus zoom, Home restores the view and Space toggles
  rotation. The canvas carries a label that says so.
- **What it needs.** WebGL 2. A browser without it gets the page with an error saying WebGL
  could not start, and every control disabled; everything the model page says about the
  model is also said in words.

## Images

Every drawing on the gallery is a figure with a caption saying what it is for and alt text
saying what is in it — the grade, the pose, the expression — so a reader who hears only one
of the two loses neither. The page says in its own words that the drawings were generated
and picked by hand. The pose overview on the model page carries alt text naming the four
poses. Nothing a reader needs depends on an image being drawn: every link says where it
goes, and the model's description is a paragraph, not a picture.

## How this is checked

By test, under `tests/`. The appearance test drives the package's fake preferences port
through both values of both device preferences and asserts the attributes on an element the
test owns. The route and page tests render each route and query it the way a screen reader
does, by role and accessible name: the one level-one heading, the main landmark, the links
by their words, eleven figures each with alt text. [Testing](../reference/testing.md) lists
what each file proves.

There is no axe run and no contrast test here. Both live in the hub, where a story run
renders every component and the palette is declared, and this repository has no story run
of its own; see [Decision 0009](../decisions/0009-no-component-workshop-yet.md). A change
that touches a surface is reviewed with the `accessibility-review` skill under
`.agents/skills/`, which walks the guarantees and the viewer's own checks.

Some things still need a person: whether the drawings' alt text says what a sighted reader
sees, how the viewer behaves under a screen reader, and whether a phone at low backlight
keeps the pages legible.

## Related pages

- [The platform upstream](../project/platform.md)
- [Testing](../reference/testing.md)
- [Decision 0008: The viewer is embedded as-is](../decisions/0008-the-viewer-is-embedded-as-is.md)
- [Decision 0009: No component workshop yet](../decisions/0009-no-component-workshop-yet.md)
