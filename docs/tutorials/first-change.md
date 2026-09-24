---
title: "Make your first change"
kind: "tutorial"
audience: [contributor, agent]
canonical_for: [first_change_tutorial]
requires: []
---

# Make your first change

This page will take a new contributor from a fresh clone to a green gate once through
every layer: installing the toolchains with `just initialize`, reading the platform
package the site depends on, editing one constant under `src/lib/`, writing the test that
measures it, running the narrowest recipe and then `just check`, and reading the
worktree diff before handing the change back for review.
