# Changelog

All notable changes to this repository are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
the versions are tags on `main`. A tag is cut only when the maintainer authorises it;
the entry below was written before the tag existed and says what the tag will name.

## [Unreleased]

## [0.1.0] - 2026-09-25

### Added

- The toolchain and the gate: `just check` runs `lock-check`, `lint`, `frontend-static`,
  `frontend-coverage`, `frontend-build`, `check-assets`, `check-docs` and `check-agents`,
  then proves the worktree unchanged, with a read-only hook gate under `prek` and every
  dependency pinned to an exact version.
- The site: three prerendered routes — home, the model and the gallery — built on the
  platform package `@steven-cutting/biscuit-games` at `1.1.0`, with the device's motion and
  contrast preferences written on the document through the package's port.
- The approved poseable model imported from `biscuit_pics` at `1d9d358`, with its pose
  studio, GLB, previews and native sources, and the cel set of two bodies and nine heads;
  `assets/manifest.json` records every file's sha256 and source, and `just check-assets`
  proves it and refuses image metadata.
- The large-file policy: the model's native sources in Git LFS, and everything the site
  serves as an ordinary blob.
- The handbook: thirty-nine registered pages under `docs/`, among them nine decision
  records.
- The agent contract: `AGENTS.md`, its provider bridges, and eight skills under
  `.agents/skills/`.
- The CI and Pages workflows, and the first deployment of the site to
  `stevencutting.com/biscuit_studio/`.

[Unreleased]: https://github.com/steven-cutting/biscuit_studio/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/steven-cutting/biscuit_studio/releases/tag/v0.1.0
