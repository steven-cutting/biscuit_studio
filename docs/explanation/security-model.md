---
title: "Security model"
kind: "explanation"
audience: [user, contributor, maintainer, operator, agent]
canonical_for: [security_model]
requires: []
---

# Security model

This page will explain what a site with no backend does and does not defend: no server,
no accounts and no data about anyone; every dependency and every GitHub Action pinned;
the token for GitHub Packages living only on the developer's machine and in the workflow
run; the secret scanner in the gate with its output suppressed; and the one workflow that
holds write scopes, the Pages deployment.
