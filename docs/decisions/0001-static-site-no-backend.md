---
title: "Decision 0001: A static site with no backend"
kind: "decision"
audience: [maintainer, agent]
canonical_for: [decision_no_backend]
requires: []
---

# Decision 0001: A static site with no backend

This record will state that the site is a static build with no server: a SvelteKit
application with the static adapter, every route prerendered, deployed to GitHub Pages
as a directory. It will give the context, that the site only shows assets and collects
nothing, the alternatives considered, and the consequence that nothing may assume a
request, a session or an origin it can talk to.
