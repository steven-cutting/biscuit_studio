---
title: "Make your first change"
kind: "tutorial"
audience: [contributor, agent]
canonical_for: [first_change_tutorial]
requires: []
---

# Make your first change

About half an hour, from a fresh clone to a green gate. The first run downloads both
toolchains and the hook repositories, so it needs the network. The change is small on
purpose; what matters is that it passes through every layer the repository has. There are
fewer layers here than in a game — no rules, no state, no specifications of its own — and
one a game does not have: the assets and the manifest that vouches for them.

## 1. Get the workspace running

Reading the platform package needs a GitHub token with `read:packages` in `~/.npmrc`, on a
line of this form, which [Develop locally](../how-to/develop-locally.md) explains:

```text
//npm.pkg.github.com/:_authToken=<your token>
```

Then:

```console
just initialize
```

It creates or checks both lockfiles, installs both toolchains from exactly what they say,
runs `git lfs install --local` so the model's `.blend` arrives as a file rather than a
pointer, normalises formatting, and installs the pre-commit hook — but only when the
checkout is the primary one. Git keeps one `.git/hooks` for every worktree of a
repository, so a hook installed from a secondary worktree quietly changes what each of the
others runs on commit; `just initialize` compares the two git directories and declines
rather than doing that.

Then confirm you are starting from green:

```console
just check
```

If something is missing rather than failing, [Develop locally](../how-to/develop-locally.md)
lists the prerequisites.

## 2. See the site

```console
just dev
```

Open the address it prints. There are three routes: the home page, which says what the
studio is; `/model/`, which shows the approved model and links out to the pose studio; and
`/gallery/`, which shows the cel illustrations. The header, the wordmark, every colour,
space and letterform come from the platform package, not from this repository. What is
the studio's own is the name after the wordmark and the pictures.

## 3. Read what decides the look

The look is not decided here. Open [The platform upstream](../project/platform.md) and
follow it to the hub's design direction and character pages: they decide the aesthetic
and Biscuit herself, and the four combinations of theme and high contrast every surface
must stay legible in. The studio restates none of it.

Then open `src/lib/appearance.ts`, the one place in the studio that consults the device.
It asks the platform's preferences port two questions — does the reader want less motion,
and more contrast — and turns the answers into the two attributes the package's stylesheet
keys on. It never touches `document` itself: the layout hands it the document element
inside `onMount`, and a test hands it an element of its own.

## 4. Add a case to the test

`tests/appearance.test.ts` holds the appearance cases. `documentAttributes` is covered for
a device that asks for more contrast, and `applyAppearance` for a device that changes its
mind after the page loaded. Nothing yet asserts the case in between: a device that already
asks for more contrast when `applyAppearance` first runs. Add it — build the fake with
`createFakePreferences({ prefersMoreContrast: true })`, apply it to a
`document.createElement('div')` the test owns, and assert that `data-high-contrast` is
`true` immediately, before any `set()`.

```console
just frontend-unit
```

Work out by hand what the function owes before you write the assertion. If your
expectation and the code disagree, one of them is wrong — decide which by reading
`appearance.ts` again, not by adjusting until it passes. The coverage floor over
`src/lib/**` is 90%, and nothing lands there without a test.

## 5. Add an asset the honest way

Every file under `assets/` and `static/pose-studio/` is listed in `assets/manifest.json`
with its sha256, and the checker refuses anything that is not. See it refuse. Copy any
small PNG of your own into `assets/illustrations/`, say as `first-change.png`, and run:

```console
just check-assets
```

It fails, naming the file:

```text
assets/illustrations/first-change.png: present but not listed; run just assets-manifest
check_assets check: 1 finding(s)
```

Now let the one recipe that writes the manifest do so, and read what it wrote:

```console
just assets-manifest
git diff assets/manifest.json
```

The diff is one new line for your file, with its size, its sha256, `"storage": "blob"`,
`"source": "studio"` and `"licence": "unsettled"`. Reading that diff is the part that
matters: the recipe hashes whatever is in the worktree, so the manifest is only as honest
as the person who reads it. `just check-assets` now passes.

Then undo it, because this tutorial adds nothing:

```console
rm assets/illustrations/first-change.png
git restore assets/manifest.json
just check-assets
```

A real import follows [Import an asset](../how-to/import-an-asset.md), which adds the one
step skipped here: recording where the file came from.

## 6. Run the whole gate

```console
just check
```

It runs every recipe in order — the lock check, the linters, the static and coverage
passes, the build, the asset check, and the documentation and agent validators — and
proves the run did not modify the worktree. The linters read the files Git knows about, so
stage a new file before expecting the gate to see it. Read only the first failure; the
later ones are often consequences. If a gate fails, do not work around it —
[Troubleshooting](../operations/troubleshooting.md) covers the common causes.

## 7. Commit

Where the pre-commit hook is installed, it runs the read-only gate again. Where you skipped
it because this is a secondary worktree, step 6 is the whole of your evidence, so run it
before you commit rather than after. The commit holds your new test case and nothing
else. Nothing is pushed until you ask for it, and nothing is published from your machine:
the site deploys from `main` only after CI passes there.

## What you just touched

The hub's pages, which you read and did not change; the one module that consults the
device, and its test; the asset tree, the manifest and the checker that holds them
together; and the gate. That is the whole loop. A change to the site is this shape; a new
asset is step 5 with its source recorded; a change to the look starts in the hub.

## Related pages

- [Develop locally](../how-to/develop-locally.md)
- [Test and debug](../how-to/test-and-debug.md)
- [Import an asset](../how-to/import-an-asset.md)
- [The platform upstream](../project/platform.md)
