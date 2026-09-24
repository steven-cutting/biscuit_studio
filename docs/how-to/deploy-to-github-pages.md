---
title: "Deploy to GitHub Pages"
kind: "how-to"
audience: [maintainer, operator, agent]
canonical_for: [deployment_procedure]
requires: []
---

# Deploy to GitHub Pages

This page will be the deployment procedure: the Pages workflow that calls the shared
workflow from the tooling repository with the base path taken from the repository name,
the static build with `BASE_PATH` set to `/biscuit_studio`, the checkout that leaves LFS
objects as pointers because nothing the site serves lives in LFS, and how to confirm the
deployed site serves the viewer and the model with the recorded checksums.
