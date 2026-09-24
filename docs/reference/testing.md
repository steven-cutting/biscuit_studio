---
title: "Testing"
kind: "reference"
audience: [contributor, maintainer, agent]
canonical_for: [testing_reference]
requires: []
---

# Testing

This page will be the reference for the test setup: the Vitest configuration inside
`vite.config.ts`, the jsdom environment, the setup file that registers the matchers, the
include pattern over `tests/`, the coverage provider and the four thresholds over
`src/lib/`, the naming rule for test files, and the rule that a test injects a fake
through a port rather than stubbing a global.
