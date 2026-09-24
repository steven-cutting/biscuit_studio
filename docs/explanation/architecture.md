---
title: "Architecture"
kind: "explanation"
audience: [contributor, maintainer, operator, agent]
canonical_for: [system_architecture]
requires: []
---

# Architecture

This page will explain how the site is put together: a SvelteKit application with the
static adapter and full prerendering, so the build is a directory a host serves as is;
the platform's header, wordmark and stylesheet mounted from the package rather than
copied; the viewer served unchanged as a static file beside the model it links; and why
nothing here assumes a server, a session or an origin.
