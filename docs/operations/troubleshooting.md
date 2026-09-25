---
title: "Troubleshooting"
kind: "operations"
audience: [contributor, maintainer, operator, agent]
canonical_for: [troubleshooting]
requires: []
---

# Troubleshooting

Symptoms as headings, causes and fixes as bodies.

## `just check` reports that a recipe changed the worktree

The recipe is the defect, not your change. Checks are read-only; anything that writes
belongs in `.pre-commit-fix.yaml` and runs from `just fix`. The report names which paths
moved. Move the offending hook, or add the generated path to the ignore rules.

## `docs validation: frontmatter <field> disagrees with the manifest`

Almost always list order. The comparison between `docs/manifest.yml` and a page's
frontmatter is order-sensitive, so `[maintainer, contributor]` fails against
`["contributor", "maintainer"]`. Copy the order from the manifest.

If the field is `title`, check for a stray difference in punctuation — the level-one
heading must match it byte for byte as well.

## `docs validation: not reachable from docs/README.md`

The page exists and is registered, but nothing links to it. Add it to
[the documentation map](../README.md), or to a page that is already reachable.

## A fact written here is the hub's

Two shapes, with opposite fixes. Decide which one you are in before editing anything.

If the subject is the studio's — which assets exist, how they are made, stored, checked and
rebuilt, what the site shows — it belongs here, on the page that owns the topic, and nothing
is owed anywhere.

If the subject is the platform's — how a surface looks, what a token means, how the
character may be drawn, what a component guarantees — then the hub's page is the authority
and a copy here is the fault. Delete the restatement and point at the hub through
[The platform upstream](../project/platform.md). If the studio needs the hub's answer to
change, write the item into [Hub handover](hub-handover.md) and stop there. Editing another
repository needs explicit authorization for each action, and this repository records what the
hub has to change rather than changing it.

No gate will tell you which of the two you are in. `canonical_for` is checked across one
tree, by one validator, reading one worktree; two repositories claiming the same topic is not
a state anything here can observe.

## `agent validation: unexpected managed file`

Something appeared under `.agents/`, `.claude/` or `.codex/` that is neither a declared
skill nor `.claude/settings.json`. If it is local tool state, add it to `.gitignore` —
the inventory reads Git, so an ignored file is invisible to it. If it is real content, it
belongs in `.agents/skills/` with bridges, or somewhere else entirely.

## `agent validation: must stay a thin pointer to the canonical skill`

A bridge under `.claude/` or `.codex/` has grown content, or its frontmatter has drifted
from the canonical skill. Regenerate it: the canonical frontmatter verbatim, one blank
line, then the fixed pointer sentence and nothing else. The body is compared against a
template rather than measured, so a clause of your own fails however short it is —
[Agent contract](../reference/agent-contract.md#what-a-bridge-must-be) carries the text.

## `svelte-check` reports an unused CSS selector

`npm run check` runs with `--fail-on-warnings`, so a warning fails `just frontend-static`
exactly as an error would. Svelte scopes a component's styles to that component's own
markup and reports a selector it cannot match there.

Delete the selector. `:global` is not the fix — it takes the rule out of the scope that was
protecting it, and buys silence rather than an answer. The pages here name elements rather
than classes in their styles for this reason: an element selector cannot go stale. A value
the platform shares belongs in the hub's stylesheet as a token, not here.

## Coverage fails but everything is tested

Distinguish two cases. If a real path is untested, add the test. If the uncovered branch
cannot be reached by any input — a bounds check after a modulo, a fallback after an
exhaustive assignment — delete the branch. Do not lower the threshold.

Three files are measured: `src/lib/brand.ts`, `src/lib/appearance.ts` and
`src/lib/components/Lockup.svelte`. A new file under `src/lib/` without a test is reported at
zero and drags the aggregate down; code that only a route needs belongs under `src/routes/`,
outside the glob. Vitest 4 prints the per-file table empty, so read
`coverage/coverage-summary.json` for the figures. See [Testing](../reference/testing.md).

## Tests fail because `matchMedia` is not a function

jsdom has no `matchMedia`. Nothing here should call it: the device's preferences are reached
through the port the platform package exports, and a test hands in the package's fake,
`createFakePreferences`, rather than stubbing `window.matchMedia`. If a test reaches the real
adapter, the code under test is reading the port itself instead of taking it as an argument;
make it take the port, as `applyAppearance` does. The real adapter, `createMediaPreferences`,
answers "no preference" where `matchMedia` is absent, which is why the layout's call is safe
under jsdom too.

## Something works under `just dev` but not in the build

Prerendering. Every route is rendered at build time, so module-scope work runs once, in Node,
and the value it computes is baked into the output for every visitor. Anything that must vary
per visitor has to happen in the browser.

The base path is the other difference. `just dev` serves at `/`; the Pages build is made with
`BASE_PATH=/biscuit_studio`, and a link written as a bare absolute path works in one and 404s
in the other. Build and preview with the same value to see what Pages will serve —
[Configuration](../reference/configuration.md) has the pair — and reach a route through
`resolve()` and a file under `static/` through `asset()`.

## `just dev` answers `403` for a gallery drawing

The message reads "outside of Vite serving allow list". The gallery imports its drawings from
`assets/`, outside `src/`, and Vite's development server refuses files outside the directories
it is told to serve. `vite.config.ts` carries `server.fs.allow: ['assets']` for exactly this;
if the line has gone, restore it. Never widen it to the repository root: that would let the
development server hand out any file in the checkout, the lockfiles and the scripts included.
The build and the tests are unaffected, because neither goes through the development server.

## `npm ci` answers `404 Not Found` or `401 Unauthorized` for the platform package

GitHub Packages authenticates every read, even of a public package, and an unauthenticated
request for a package that exists usually answers `404`, which reads as a missing package
rather than a missing token. Check `~/.npmrc` for the line
`//npm.pkg.github.com/:_authToken=<your token>`, with a token carrying `read:packages`, and
that it has not expired. The committed `.npmrc` carries only the scope line and never the
token. [Develop locally](../how-to/develop-locally.md) has the steps. In CI the same failure
means the install step lost `NODE_AUTH_TOKEN` or the workflow lost `packages: read`.

## The first `just lint` takes a minute and fails offline

prek clones every third-party hook repository into its cache on the first run, so the first
`just lint`, and the first `just check`, need the network; `just sync` needs it too, for the
registry. An offline first run fails at `sync` or `lint` for no reason of the studio's. Run
both once with the network; after that the gate is offline.

## `just check-assets` prints `<path>: present but not listed; run just assets-manifest`

A file under `assets/` or `static/pose-studio/` has no manifest entry. If you meant to add
it, follow [Import an asset](../how-to/import-an-asset.md): run `just assets-manifest`, then
read the diff, and give the new entry its real `source` rather than the `studio` the tool
writes. If you did not mean to add it — a stray export, a `.blend1` Blender left behind —
delete the file. The opposite finding, `listed in the manifest but absent from the worktree`,
means a file went missing; restore it with `git restore` unless removing it was the point.

## `just check-assets` prints `<path>: sha256 differs from the manifest; run just assets-manifest and read the diff`

A byte changed. Either an asset was edited by hand, which the rule forbids, or a rebuild or
an import changed it and was not recorded. If the change was not meant, restore the file with
`git restore`. If it was a recorded rebuild or import, run `just assets-manifest` and read the
diff: every changed `sha256` should be one you expected, and each changed entry's `source`
should say where the new bytes came from.

Never edit the manifest by hand to agree with the file. A manifest that agrees with a
tampered file is the one failure the checker cannot see.

## `just check-assets` prints `<path>: carries EXIF (GPSInfo); strip every metadata field before committing`

The image carries metadata beyond its resolution, and the finding names every tag: `GPSInfo`
for a location, `Make`, `Model` or `DateTimeOriginal` for a camera and a time, `Software` for
an editor. Most often it is a photograph, and a photograph of the real dog is committed only
with the maintainer's approval of that photograph. Without that approval, remove the file.
With it, strip every metadata field — re-save the pixels only, or use a tool that removes the
EXIF block whole — and check again. A TIFF is refused outright; export it as PNG. See
[Content policy](../explanation/content-policy.md).

## `just check-assets` prints `<path>: storage 'lfs' but .gitattributes says 'blob'`

The manifest and `.gitattributes` disagree about the path: a file was moved into or out of an
LFS pattern, or a pattern changed, without `just assets-manifest`. Stop before rewriting the
manifest to agree, and work out which side moved. A served file — anything under
`static/pose-studio/`, or a drawing the gallery imports — must never be under an LFS pattern:
Pages would serve its pointer as text and no build would fail. If a served path moved into
LFS, move it back. If a source moved out of LFS, restore the pattern.

## `biscuit-poseable.blend` is 133 bytes of text

The clone was made without git-lfs, so the `.blend` is its pointer: a version line, the oid
and the size. Install git-lfs for the machine, run `git lfs install --local` in the clone —
`just initialize` does — and then `git lfs pull`. The checker passes either way, because it
verifies an LFS file from its pointer.

## A `.blend` was committed as an ordinary blob

On a machine without git-lfs, Git stores a `.blend` the patterns name as a plain blob;
`.gitattributes` still says `lfs` and the bytes still hash to the recorded digest, so the
only witness is the index, and that is what `just check-assets` reads: it refuses the path
with `the index holds the file itself, not an LFS pointer` from the first run after the add,
in the hook gate if it is installed and in the `assets` job otherwise. Two things show it
by hand: `git lfs ls-files` does not list the path, and `git cat-file -s HEAD:<path>` prints
the full size rather than a pointer's 133 bytes. Before pushing, install git-lfs, run
`git lfs install --local`, remove the file from the index with `git rm --cached <path>` and
add it again so the filter stores it, and amend the commit. Once it is pushed, the blob is
in history for good.

## The deploy fails with `Failed to create deployment (status: 404)`

The workflow is fine; the repository's Pages source is not set to GitHub Actions. The build
job succeeds and the deploy job has nowhere to deploy. `scripts/bootstrap_repo.sh` sets the
source, and [Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md) says when to run it.

## The deployed viewer, or its download link, serves a small text file

A served path was moved under an LFS pattern, so the Pages build — which never fetches LFS
objects — published the pointer: a few lines naming an oid and a size. Nothing failed along
the way. Find the pattern in `.gitattributes` that now names the path, and move the file or
narrow the pattern so that nothing under `static/pose-studio/` is LFS; `git check-attr filter
<path>` must print `unspecified`. [Large files](../explanation/large-files.md) explains why
the patterns name sources by path.

## Commits fail in another worktree after `just install-hooks`

`just install-hooks` was run by hand from a secondary worktree. Git keeps one `.git/hooks`
directory and shares it across every worktree of the repository, and the recipe passes
`--overwrite`, so the hook installed here replaced the one every other worktree also
commits through. `just initialize` is not a way in: it compares the common directory
against the git directory and skips the hook in a secondary worktree, saying so.

The installed hook records an absolute path into the virtual environment of the worktree
that installed it, which is why the fault surfaces late and somewhere else. While this
worktree exists that path resolves, so every other worktree keeps committing — through an
environment that is not its own. Remove this worktree and the path names nothing, and
commits fail everywhere at once, reading as a missing interpreter rather than as a hook
that was replaced weeks earlier.

Reinstall from the primary clone. One `just install-hooks` there fixes every worktree at
once, because there is only ever one hook. A commit that cannot wait for that can pass
`--no-verify`, which skips the gate outright rather than passing it, so run `just lint` by
hand first.

Nothing warned you at the time, and nothing will next time either. The check to run before
either command is in
[Commands](../reference/commands.md#do-not-install-the-hook-from-a-secondary-worktree).

## Related pages

- [Develop locally](../how-to/develop-locally.md)
- [Test and debug](../how-to/test-and-debug.md)
- [Commands](../reference/commands.md)
- [Asset manifest](../reference/asset-manifest.md)
- [Maintenance](maintenance.md)
