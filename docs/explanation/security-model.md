---
title: "Security model"
kind: "explanation"
audience: [user, contributor, maintainer, operator, agent]
canonical_for: [security_model]
requires: []
---

# Security model

The studio has no server, no accounts and no data about anyone. It serves three pages and a
model viewer as static files, and everything it holds is a picture of a dog and the tooling
that checks the pictures. That removes most of the attack surface a web application usually
has, and it is worth being precise about what remains rather than claiming the problem
away.

## What there is to protect

Not the reader. The site collects nothing and stores nothing:

- **Nothing is collected.** No analytics, no telemetry, no error reporting, no cookies.
  Nothing leaves the browser.
- **Nothing is stored.** There is nowhere to upload anything to, and nothing is kept on the
  device either. The one thing code reads is the device's own motion and contrast
  preferences, through the port the platform package exports, and it writes nothing back.
  The viewer's saved poses and PNG files are downloads the reader keeps.
- **There are no credentials in the product, and none in the repository.** No sign-in, no
  tokens, nothing secret in the build or the bundle, and no stored secret of any kind: no
  deployment key, no service token. The `ripsecrets` gate exists to keep it that way.

What there is to protect is the integrity of the assets and the line around what may be
committed at all.

- **The assets are what they say they are.** Every file under `assets/` and
  `static/pose-studio/` is listed in `assets/manifest.json` with its size, its sha256 and
  where it came from; [Asset manifest](../reference/asset-manifest.md) is the format.
- **Nothing is committed that may not be.** No photograph of the real dog without the
  maintainer's approval of that photograph and with every metadata field stripped, and no
  third-party art. [Content policy](content-policy.md) owns the rule.

## What is deployed

A project site on GitHub Pages, served beneath the repository's name. `pages.yml` is the
one workflow that publishes, and it holds the two publishing scopes, `pages: write` and
`id-token: write`; nothing else here holds either. It runs only after CI has passed for a
push to `main` that is still `main`'s head, so what it publishes is a commit the three
checks have passed.

Inside the shared workflow it calls, the scopes are split by job. The build job holds
`contents: read` and `packages: read`, installs the platform package with the run's own
token, and never holds a publishing scope. The deploy job holds `pages: write` and
`id-token: write` and runs no install. The run's token is minted for the run and discarded
with it, so there is no stored credential anywhere to leak or rotate.
[Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md) is the procedure.

## What the build defends

- **Supply chain.** Every dependency is pinned exactly and locked; `just lock-check` fails
  if a manifest and its lockfile disagree. GitHub Actions and the shared workflow are pinned
  to commit SHAs, not to mutable tags. The platform package arrives at an exact version.
- **Workflow permissions.** Continuous integration runs with `contents: read` and
  `packages: read` and nothing more, and the registry token sits on the one step that
  installs rather than on the job. Each workflow declares its own scopes in its own file,
  so they are visible rather than inherited.
- **Credential leakage.** `ripsecrets` scans every commit, and its output is suppressed so a
  match never copies the matched value into a log.
- **Assets.** `just check-assets` runs on every `just check` and as a required check, and
  refuses a file that is not listed, a listing with no file, and a changed byte anywhere
  under `assets/` and `static/pose-studio/`. It also refuses an image carrying EXIF beyond
  its resolution, and any TIFF, so a photograph's location and camera cannot arrive
  unnoticed.
- **Third-party content at runtime.** There is none. The pages load no external script,
  font or image: the typefaces arrive with the package and are served from the same origin,
  and the viewer inlines every texture and fetches nothing. The two links out, to the
  Blender scene and the model's README on GitHub, are navigation a reader chooses.

The manifest is only as honest as its review. `just assets-manifest` recomputes every hash
from the worktree, so a tampered file and a rewritten manifest pass together. The guard is
a person reading the manifest's diff on every import and rebuild, and the `source` field,
which the tool never rewrites and checks only for form: whether the repository, commit and
path it names are real is for the reviewer to see.

## What a copy does not defend

An asset leaves the studio by copy: a file placed in the hub or a game, recorded with the
studio commit and the sha256 it had. See
[Decision 0007](../decisions/0007-assets-travel-by-copy-and-ledger.md). A copy is a
snapshot, and nothing compares it with the studio afterwards. If the file is rebuilt or
replaced here, the consumer's copy stays as it was, and if the copy is edited there, nothing
here notices.

What would close that is a ledger a consumer's gate can verify, which is a separate
discussion and not settled. Until then the protection is procedural:
[Promote an asset](../how-to/promote-an-asset.md) and
[Hub handover](../operations/hub-handover.md) record every copy, and review is what reads
them.

## What is out of scope

Denial of service against GitHub's own infrastructure, and anything a person can do to
their own browser. There is no shared state, so nothing one visitor does can affect another.

## Reporting

See `SECURITY.md` at the repository root.

## Related pages

- [Content policy](content-policy.md)
- [Asset manifest](../reference/asset-manifest.md)
- [Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md)
- [Quality gates](../reference/quality-gates.md)
