---
title: "Test and debug"
kind: "how-to"
audience: [contributor, maintainer, agent]
canonical_for: [test_workflow]
requires: []
---

# Test and debug

This page will describe the test workflow: Vitest under jsdom over `tests/`, the
coverage floor measured over `src/lib/` alone, the watch recipe for iteration, how a
component test queries by accessible role and name, how a port fake is injected instead
of a stubbed global, and how to read a coverage report that names an uncovered branch
before deciding whether to test it or remove it.
