---
title: "Decision 0008: The viewer is embedded as-is"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_viewer_embedded]
requires: []
---

# Decision 0008: The viewer is embedded as-is

This record will state that the existing hand written WebGL viewer is served unchanged as
a static file with three link targets rewritten, rather than ported into the site's
components first. It will give the reason, that the viewer has no dependency and no
network request and already works, the accepted cost of its size in ordinary history,
and the later ticket that ports it to three.js.
