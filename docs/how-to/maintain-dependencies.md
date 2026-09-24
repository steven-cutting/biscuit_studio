---
title: "Maintain dependencies"
kind: "how-to"
audience: [maintainer, agent]
canonical_for: [dependency_maintenance]
requires: []
---

# Maintain dependencies

This page will describe how the pins move: every dependency in `package.json` and
`pyproject.toml` is an exact version, the lockfiles are committed, `just lock-upgrade`
is the one recipe that raises them, `just lock-check` proves the manifests and the
lockfiles agree, and the platform package is raised deliberately after reading the hub's
changelog rather than as part of a routine sweep.
