---
title: "Rebuild the model"
kind: "how-to"
audience: [contributor, maintainer, agent]
canonical_for: [model_rebuild_procedure]
requires: []
---

# Rebuild the model

This page will be the rebuild procedure for the approved model: the Blender version the
build expects, the checkout of the earlier studies the build scripts read through a
temporary symlink under `assets/`, the `just model-rebuild` recipe that places and removes
it, the files a rebuild rewrites including the viewer, and how the manifest records the
rebuild date in each entry's source field afterwards.
