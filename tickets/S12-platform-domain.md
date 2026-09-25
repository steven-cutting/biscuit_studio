---
id: S12
title: "Domain: the studio's address when the platform moves to pnut.fans"
status: open
depends_on: [S07]
parallel_with: [S08, S10, S11]
branch: ticket/s12-platform-domain
estimated_size: S
---

# S12: Domain: the studio's address when the platform moves to pnut.fans

## Context

S07's first deploy showed that the studio is served at
`https://stevencutting.com/biscuit_studio/`, not at the github.io address decision 6
had named: the account's user site (`steven-cutting/steven-cutting.github.io`) carries
the custom domain `stevencutting.com`, and GitHub serves every project site of an
account beneath its user site's domain. The github.io address answers `301` to it. On
2026-09-24 the maintainer asked for the studio to live under `pnut.fans`, as Poodl does,
and on the facts below chose to keep the served address for now and to make the move
with the platform-wide switch to `pnut.fans` that is planned for every Biscuit Games
repository. This ticket holds that move for the studio. It is blocked until the hub
decides the shape.

The facts, measured or read on 2026-09-24:

- `pnut.fans` is the custom domain on the `poodl` repository's Pages site (P decision
  0009, `gh api repos/steven-cutting/poodl/pages` reads `workflow pnut.fans
  https://pnut.fans/ true`). GitHub allows one custom domain per repository, and one
  repository per domain, so this repository cannot take the same name while Poodl holds
  it.
- A project site nests beneath the *user site's* domain only. A custom domain on another
  repository (Poodl's, or the hub's) never serves this repository's build, so
  `pnut.fans/biscuit_studio/` is reachable only if `pnut.fans` becomes the user site's
  domain or if Poodl's staging step copies the studio's build into its own upload, which
  P decision 0009 and H decision 0012 both reject.
- H decision 0012 defers moving the domain root off Poodl until a second game is served
  or the hub site is worth visiting, and says the move is a move and not an addition.
- No subdomain of `pnut.fans` resolves today (`studio.pnut.fans`,
  `biscuit-studio.pnut.fans` answer nothing). The DNS records are at the registrar and
  are written down only in P `docs/how-to/deploy-to-github-pages.md`; the `MX` and `SPF`
  records carry mail and are never replaced wholesale.
- `pages.yml` sets `base_path` from `github.event.repository.name`, so a domain of this
  repository's own, served from its root, needs the workflow to pass an empty base path
  (decision 0004 names this as the one change), a deviation from the template's file.

Two shapes fit, and the choice is the hub's, not this repository's:

1. **A subdomain of this repository's own**, such as `studio.pnut.fans`: one `CNAME`
   record at the registrar pointing at `steven-cutting.github.io.`, the domain set on this
   repository's Pages site, HTTPS enforced once the certificate is issued, and `pages.yml`
   passing an empty `base_path`. Poodl and the hub are untouched.
2. **`pnut.fans` as the user site's domain**: the domain moves from `poodl` to
   `steven-cutting.github.io`, every project site is then served at `pnut.fans/<repo>/`,
   Poodl's landing page moves to the user site's repository, Poodl's `BASE_PATH` stays
   `/poodl`, and `stevencutting.com` needs a new home for the About page. This is the
   shape that makes the studio's address `pnut.fans/biscuit_studio/` and reverses P 0009
   and H 0012 in a way neither wrote down.

Read first: CONVENTIONS.md §1 decision 6 and §9; this repository's decision 0004,
`docs/how-to/deploy-to-github-pages.md` and `docs/operations/hub-handover.md`; H decision
0012; P decision 0009 and P `docs/how-to/deploy-to-github-pages.md`.

## Goal

- The hub has decided the shape, recorded in a hub decision record that supersedes or
  amends H 0012, before anything here changes.
- The studio's address follows: the repository's Pages settings, `pages.yml` if the base
  path changes, and the four places that name the address (decision 0004, the deploy
  how-to, `docs/project/purpose-and-scope.md`, `AGENTS.md`), plus CONVENTIONS.md decision
  6 and `README.md` once S08 has written it.
- HTTPS enforced on the new address; the old address measured for its redirect and the
  result recorded, as P did.

## Non-goals

- Deciding the shape here. The hub is the source of truth for the platform's address;
  this ticket asks and waits.
- Editing `poodl`, the hub, the user site's repository or the DNS records from this
  repository. Each is a separately authorised action on another repository.
- A domain for this repository that the platform does not share.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `steven-cutting/biscuit_studio` (Pages settings, no file) | GitHub | `gh api` | custom domain and HTTPS, once decided |
| `.github/workflows/pages.yml` | workflow | S04 | `base_path`, only if the site moves to a root |
| `docs/decisions/0004-a-project-pages-site.md` | docs | S05 | the address and the domain paragraph |
| `docs/how-to/deploy-to-github-pages.md` | docs | S05 | the address and the DNS record, if any |
| `docs/project/purpose-and-scope.md` | docs | S05 | the address |
| `docs/operations/hub-handover.md` | docs | S06 | the address item closed |
| `AGENTS.md` | contract | S00 | the address |
| `README.md` | docs | S08 | the address |
| `tickets/CONVENTIONS.md` | ticket | S00 | decision 6 |
| `tickets/S12-platform-domain.md` | ticket | this file | `status:` line, hand-back notes |

## Steps

1. Ask the hub for the decision, citing the facts above; record the request in
   `docs/operations/hub-handover.md`. Stop until the hub's decision record exists.
2. With the shape decided: the DNS record (the maintainer's, at the registrar, and only
   the record the shape needs), then the Pages setting (**Authorisation required**), then
   `https_enforced` once GitHub reports the certificate approved.
3. `pages.yml` if the base path changes, with the S04 comment updated to say why.
4. The address in every file listed, and the redirect from the old address measured with
   `curl -sI` and quoted.
5. `just check`, then the hand-back notes and `status: done`.

## Acceptance criteria

- [ ] A hub decision record names the shape, and this repository cites it.
- [ ] `gh api repos/steven-cutting/biscuit_studio/pages --jq '[.cname, .html_url,
      .https_enforced] | join(" ")'` prints the decided domain, the decided address, and
      `true`.
- [ ] `curl -sI` of the decided address answers `200`; of
      `https://stevencutting.com/biscuit_studio/` answers a redirect or `200`, recorded
      either way.
- [ ] No file names the old address except this ticket, S07 and CONVENTIONS.md's record
      of the correction.

## Verification

```sh
gh api repos/steven-cutting/biscuit_studio/pages --jq '[.build_type, .cname, .html_url, .https_enforced] | map(tostring) | join(" ")'
rg -n 'steven-cutting\.github\.io|stevencutting\.com' AGENTS.md README.md docs
just check
```

## Hand-back notes

Filled in by the agent that executes this ticket.

## Open points

- **Whether the hub reopens 0012 for the studio alone.** Its own reopening conditions are
  a second served game or a hub site worth visiting; the studio is neither a game nor the
  hub, and the maintainer's stated plan is a switch of every repository, which is the
  second condition arriving at once.
- **The old address after the move.** P measured that a project site's former address
  under the user domain redirects to the new domain's root with the path prefix
  stripped; whether that holds for a subdomain is unknown until measured.
