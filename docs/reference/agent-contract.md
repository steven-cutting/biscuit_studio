---
title: "Agent contract"
kind: "reference"
audience: [contributor, maintainer, agent]
canonical_for: [agent_contract]
requires: []
---

# Agent contract

Enforced by `bg-validate-agents`, a console script of the `biscuit-games-tooling` package,
run by `just check-agents` and by a pre-commit hook. `AGENTS.md` is the single source of
truth for how an agent works in this repository; everything else in the agent surface exists
only so a particular tool can find it.

## The four surfaces

| Path | Role |
| --- | --- |
| `AGENTS.md` | Canonical. Read natively by Codex, and by anything following the convention. |
| `CLAUDE.md` | A pointer, byte-pinned to `@AGENTS.md` and nothing else. |
| `.github/copilot-instructions.md` | A pointer, byte-pinned to one paragraph. |
| `.agents/skills/` | Canonical task procedures, mirrored by thin bridges under `.claude/skills/` and `.codex/skills/`. |

Byte-pinned is meant literally for the two pointers: the validator compares the whole file
against the expected text, final newline included, rather than a stripped copy of it. A
pointer that forgave surrounding whitespace would be enforcing something weaker than the
word in the table above.

A `CODEX.md` at the repository root is forbidden: Codex reads `AGENTS.md` directly, and a
second file would be a second source of truth.

## What `AGENTS.md` must contain

- At least 300 words.
- Six phrases, each naming an invariant that is expensive to rediscover: `untrusted`,
  `just check`, `explicit authorization`, `ai_tmp/`, `docs/specs/`, and `runes`.

The phrase list is a crude check and is meant to be. It does not verify that the guidance
is good; it verifies that the six topics were not dropped in an edit.

The studio has no `docs/specs/`, and its `AGENTS.md` says so in the very sentence that
carries the phrase: that the repository has none of its own, and that the platform's modules,
installed with the package, govern its surfaces. The validator checks that the phrase is
present, not what the sentence around it means, so the phrase is kept by stating the absence
rather than by pretending to a directory that is not there.

## What a skill must be

This repository carries eight canonical skills, one directory each under `.agents/skills/`:

- `accessibility-review` — review a change against the platform's accessibility
  guarantees, and the viewer against its own checks.
- `asset-change` — import or rebuild an asset under `assets/`: the two how-to pages,
  `just assets-manifest`, reading the diff, `just check-assets`, the EXIF and approval rules,
  the LFS patterns and the `source` field.
- `code-review` — review a change against the invariants, the tests and the documentation
  contract.
- `fix-quality` — diagnose a failing gate at its root rather than suppressing it, including
  a `check-assets` finding, which is never answered by editing the manifest by hand.
- `hub-handover` — when an asset is ready to leave: the promotion procedure, the item written
  into the hub handover page in that page's own register, and never an edit to the other
  repository.
- `plan-change` — plan a change that needs evidence first, including one that moves a
  platform rule (the hub changes first) or an asset out (a handover entry).
- `project-check` — bring a workspace to where the full gate runs, `git lfs install`
  included, and read what it reports.
- `review-docs` — add or revise a handbook page so it satisfies the documentation contract.

Frontmatter of exactly two keys:

```markdown
---
name: asset-change
description: Import or rebuild an asset under assets/ and record it in the manifest with its source.
---
```

- `name` equals the directory name.
- `description` is at least eight words and states a real trigger.
- The body cites `AGENTS.md` and names at least one `just` recipe. A procedure that ends
  without saying how to verify it is not a procedure.

The frontmatter parser is deliberately literal. It splits every line between the `---`
markers on the first colon and treats a line without one as an error, so a blank line
inside the block fails the check with `invalid frontmatter line`. Keep the two keys
adjacent, with nothing between them. The same parser reads the bridges, so the rule holds
there too.

A key that appears twice is an error rather than an overwrite. Left to the usual last-wins
behaviour, a block of three lines would satisfy a rule about two keys on whichever copy
happened to survive, which is the opposite of what "exactly two" is for.

## What a bridge must be

Each of `.claude/skills/<name>/SKILL.md` and `.codex/skills/<name>/SKILL.md` carries the
canonical frontmatter verbatim, then exactly this sentence and nothing else:

```markdown
Follow `../../../.agents/skills/<name>/SKILL.md`. That file is canonical and this bridge adds nothing to it.
```

The body is compared against that template rather than measured against a word budget. A
budget was the earlier rule and it enforced the wrong thing: a bridge could carry an
instruction of its own — an extra step, a caveat, a second pointer — and pass on being
brief. This is an instruction surface, so a clause smuggled into it is read as guidance and
becomes a second source of truth for the skill it points at. A bridge that grows content
fails whether or not it is short.

## The inventory

The validator lists managed files from Git, honouring only this repository's
`.gitignore`, and compares that against what it expects.

- Every expected file must exist. A skill without its two bridges fails.
- No unexpected file may exist under `.agents/`, `.claude/` or `.codex/`. The single
  exception is `.claude/settings.json`, which is tolerated but not required — it carries
  provider configuration rather than agent guidance.
- Managed files must be regular files, never symlinks.

Local assistant state stays out of the inventory by being listed in `.gitignore`. That is
deliberate: the check reads Git rather than walking the filesystem, so an ignored file is
invisible to it.

## Related pages

- [Documentation contract](documentation-contract.md)
- [Quality gates](quality-gates.md)
