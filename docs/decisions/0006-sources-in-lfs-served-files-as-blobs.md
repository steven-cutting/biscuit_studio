---
title: "Decision 0006: Sources in LFS, served files as blobs"
kind: "decision"
audience: [contributor, maintainer, operator, agent]
canonical_for: [decision_large_file_storage]
requires: []
---

# Decision 0006: Sources in LFS, served files as blobs

This record will state which files Git LFS holds and which stay ordinary blobs: the
model's native source and the two large QA records in LFS because every rebuild rewrites
them whole; the GLB, the textures, the previews and the viewer as blobs because GitHub
Pages serves an LFS pointer as text. It will name the accepted cost of a large viewer in
ordinary history and the ticket that retires it.
