---
title: "Decision 0003: A Python toolchain in a frontend repository"
kind: "decision"
audience: [maintainer, agent]
canonical_for: [decision_python_toolchain]
requires: []
---

# Decision 0003: A Python toolchain in a frontend repository

This record will state why a frontend repository carries a small Python toolchain: uv
provides a pinned prek for the hook gate, ruff for the one script, Pillow for the
checker's EXIF read and the tooling package for the two validators and the project
check. It will give the alternatives, a Node only gate or global installs, and why exact
pins in one lockfile won.
