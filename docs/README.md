---
title: "Documentation map"
kind: "project"
audience: [user, contributor, maintainer, operator, agent]
canonical_for: [documentation_navigation]
requires: []
---

# Documentation map

Every page below is registered in `manifest.yml`, owns at least one topic, and is
reachable from here. That is the whole of the arrangement; the rules behind it are in
[Documentation contract](reference/documentation-contract.md).

This repository is the Biscuit Games studio: where the platform's graphical assets are
developed, and a static site that shows them. It holds no specification of its own —
how a surface looks, how it is worked and what it owes are the platform's three Allium
modules, which arrive with the package this site installs; see
[The platform upstream](project/platform.md). What is decided here is decided in
[the decision records](decisions/README.md).

## Start here

- [Purpose and scope](project/purpose-and-scope.md) — what this repository is for, and what it is not.
- [The platform upstream](project/platform.md) — what the hub decides, and where to read it.
- [Repository map](project/repository-map.md) — where everything lives.
- [Terminology](project/terminology.md) — the words this repository uses precisely.
- [Make your first change](tutorials/first-change.md) — clone to green gate, once through every layer.

## How to

- [Develop locally](how-to/develop-locally.md)
- [Test and debug](how-to/test-and-debug.md)
- [Import an asset](how-to/import-an-asset.md)
- [Rebuild the model](how-to/rebuild-the-model.md)
- [Promote an asset](how-to/promote-an-asset.md)
- [Maintain dependencies](how-to/maintain-dependencies.md)
- [Deploy to GitHub Pages](how-to/deploy-to-github-pages.md)

## Understand

- [Architecture](explanation/architecture.md) — how a static site with no server is put together.
- [Large files](explanation/large-files.md) — what Git LFS holds, what stays a blob, and why.
- [Content policy](explanation/content-policy.md) — what is never committed, and the licence question that is still open.
- [Accessibility](explanation/accessibility.md) — the obligations the site inherits from the platform.
- [Security model](explanation/security-model.md) — what a site with no backend does and does not defend.
- [Quality philosophy](explanation/quality-philosophy.md) — why each gate exists.

## Look up

- [Commands](reference/commands.md)
- [Configuration](reference/configuration.md)
- [Asset manifest](reference/asset-manifest.md)
- [Testing](reference/testing.md)
- [Quality gates](reference/quality-gates.md)
- [Documentation contract](reference/documentation-contract.md)
- [Agent contract](reference/agent-contract.md)

## Run it

- [Maintenance](operations/maintenance.md)
- [Troubleshooting](operations/troubleshooting.md)
- [Hub handover](operations/hub-handover.md) — what the hub and the games still have to change, and what they owe this repository.

## Decisions

- [Architecture decisions](decisions/README.md) — the record of what was chosen and why.
