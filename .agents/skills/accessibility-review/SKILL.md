---
name: accessibility-review
description: Review a component, token, or specification change against the platform's stated accessibility guarantees.
---

# Review a change for accessibility

The `@guarantee` clauses in `docs/specs/appearance.allium` are the acceptance criteria, not aspirations, and every game inherits them. Each one names an obligation a change can break silently.

1. Read `AGENTS.md` and `docs/explanation/accessibility.md`, then read the guarantees on the `Appearance` surface.
2. Check the legibility floor in all four combinations of theme and high contrast, not the one the change was looked at in. Text on an operable control reaches `minimum_text_contrast` against what is behind it; a control that draws a boundary reaches `minimum_boundary_contrast` against the page; a control that draws none is identified by its own words.
3. Check the colour obligation. Every state a component expresses carries a shape, a word, or both alongside the colour, and has an accessible name.
4. Check the unavailable case. A control the reader cannot operate is exempt from the figures and from nothing else: it still reports its state to the accessibility tree and keeps every non-colour indication its live form carried.
5. Check keyboard operation. Every control is reachable and invocable from the keyboard alone, with visible focus, and is a comfortable target at the narrowest supported width.
6. Check motion. Animation runs only when the setting allows it and the operating system expresses no reduced-motion preference; the operating system wins.
7. Check the viewer, whether the embedded page or the component that replaces it. Its auto-rotation stops when `data-animations` is absent from the document element and never restarts on its own; the canvas's background follows the platform's theme rather than a colour of its own; the page never sets `touch-action: none` on anything wider than the canvas, so pinch-zoom survives; and the model is decorative, so nothing a reader needs is carried by it alone.
8. Report findings by severity with `file:line` references, then run `just frontend-static` and `just check`.
