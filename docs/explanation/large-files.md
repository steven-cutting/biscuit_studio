---
title: "Large files"
kind: "explanation"
audience: [contributor, maintainer, operator, agent]
canonical_for: [large_file_policy]
requires: []
---

# Large files

This page will explain the large file policy: the model's native sources and the two
large QA records go through Git LFS because every rebuild rewrites them whole, while the
GLB, the textures, the previews and the viewer stay ordinary blobs because GitHub Pages
serves an LFS pointer as text. It will state the costs that were accepted and the
bandwidth figure the free tier allows.
