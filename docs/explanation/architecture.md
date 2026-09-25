---
title: "Architecture"
kind: "explanation"
audience: [contributor, maintainer, operator, agent]
canonical_for: [system_architecture]
requires: []
---

# Architecture

Biscuit Studio is a static site. The build produces a directory of files; a host serves
them unchanged; everything after that happens in the browser. There is no request the
application can make to itself, no session, and no origin it trusts. That constraint is
not a limitation working around a missing backend. It is the architecture, and the studio
needs it less than any game does: it shows three pages and a model. See
[Decision 0001](../decisions/0001-static-site-no-backend.md).

The directory is published. GitHub Pages serves it as a project site under the
repository's name, so every route and every file lives beneath `/biscuit_studio/` rather
than at a domain root, which stays with the first game; see
[Decision 0004](../decisions/0004-a-project-pages-site.md).

## Build

SvelteKit with `@sveltejs/adapter-static`, prerendering every route. `+layout.ts` sets
`prerender = true` for the whole tree, so a route that could not be rendered at build time
fails the build rather than shipping broken. `ssr` is on and `trailingSlash` is `always`,
so each route becomes a directory with an `index.html` inside it — the shape a plain file
host serves without being configured.

Prerendering has one consequence worth stating plainly: **module-scope work runs once, at
build time, in Node.** Anything that must differ per visitor — asking the device a
question, looking at the clock — has to happen in the browser after hydration, not while
the page is being generated. The one thing here that asks the device a question is the
preferences port, and it is called after hydration; the side-effects section below.

`src/lib/` holds three files and nothing is packaged from it. `brand.ts` is the one place
the site's name, title and description are written. `appearance.ts` derives the two
device-dependent attributes on the root element. `components/Lockup.svelte` hands the
platform's `Wordmark` the word `studio`. Everything else the pages wear — `HeaderBar`,
`Wordmark`, `CardLabel`, the token stylesheet and the two faces — is imported from
`@steven-cutting/biscuit-games`, never copied.

Two more things reach the build, by two different routes:

- **`static/pose-studio/`** is copied into `build/` byte for byte by `adapter-static`: the
  viewer, the GLB it links, and the overview image. The build neither reads nor rewrites
  them, which is why their sha256 in `build/` is the one `assets/manifest.json` records.
- **`assets/`** is reached only through Vite imports, and only from the two showcase
  routes. The gallery imports its eleven PNG files, which the build fingerprints under
  `_app/immutable/assets/`; `vite dev` needs `server.fs.allow: ['assets']` in
  `vite.config.ts` to serve them. Nothing else under `assets/` is shipped.

The eleven drawings are about 15 MB, and they are the gallery's weight. That is accepted
for the first release; smaller copies made by a recipe are the planned repair, not a
change a reader should make by hand.

The build is portable across base paths. `paths.base` is read from `BASE_PATH` at build
time, and SvelteKit writes prerendered links relative, so the same pages work from `/`
locally and from `/biscuit_studio/` on Pages.
[Configuration](../reference/configuration.md) records where the value comes from.

## Runtime shape

```text
src/routes/           the three pages, and the one place the document is reached
src/lib/              the name, and the appearance derivation; pure
src/lib/components/   the lockup, drawn by the platform's Wordmark
static/pose-studio/   the viewer: a page of its own, served as a file
```

Three routes, each the platform's chrome around a little content. `+layout.svelte` imports
the package's `app.css`, which puts every route inside the same palette, and wires
appearance once. `/` is a sentence and two links. `/model/` shows the pose overview, a
paragraph on the model, and three links: the viewer, the GLB, and the Blender scene on
GitHub, because the `.blend` is an LFS object and Pages would serve its pointer. `/gallery/`
shows the eleven cel drawings, each a figure with its own caption and alt text.

The viewer is not a route. It is a hand-written WebGL 2 page of its own, 26 MB with every
texture inlined, served as a static file under `static/pose-studio/`; the model page links
to it and never frames it. It keeps its own light palette and its own type, and nothing of
the platform's reaches it. [Decision 0008](../decisions/0008-the-viewer-is-embedded-as-is.md)
says why it is kept as-is and what replaces it.

The GLB beside it does not look like the viewer. It carries standard PBR materials, while
the viewer and the Blender scene carry the approved cel shading, so the same model opened in
another tool looks plainer. The model page says so beside the download link; a port of the
viewer to a maintained renderer has to reproduce the cel look rather than take the GLB's.

## State

There is none. The studio keeps nothing about a visitor: no settings, no statistics,
nothing in device storage and nothing carried in a URL. Clearing browser data loses
nothing, because there was nothing there to lose. The viewer's saved poses and PNG files
are downloads the reader keeps; the page stores none of them.

The one piece of state the site has is stated rather than held. `src/app.html` carries
`data-theme="dark"` and `data-animations="on"` on the root element — the default record
from the platform's appearance module, installed with the package — so the prerendered
page paints the platform default with no store to hydrate first. The theme never changes
afterwards: the studio ships no settings control, so `dark` is the whole of it. The other
attribute, and `data-high-contrast`, are re-derived from the device after hydration.

## Side effects

One thing reaches outside the page: the device's reduced-motion and more-contrast
preferences, read through the preferences port the package exports. `applyAppearance` in
`src/lib/appearance.ts` takes an element and a port, writes `data-animations` and
`data-high-contrast` on the element, and rewrites them whenever the port reports a change.
`document.documentElement` is reached inside `onMount` in `src/routes/+layout.svelte` and
nowhere else, which is where the real element and `createMediaPreferences()` are handed
over. The test hands `applyAppearance` an element it owns and the package's fake port, and
stubs nothing. No storage, no clock, no randomness and no network call.

The rule that governs that effect governs every one after it. It sits behind a port: an
interface in the application's vocabulary, a real adapter taking its platform object as a
defaulted argument rather than reading a global, and an in-memory fake that tests inject.
The reasoning is the hub's decision on ports and fakes, reached through
[The platform upstream](../project/platform.md); the studio holds no record of its own on it,
because it adds no port of its own.

## What is not here

No API, no database, no authentication, no background jobs, no telemetry. Those are not
deferred; they are out of scope, as [Purpose and scope](../project/purpose-and-scope.md)
records.

No game. Rules, boards and scores belong to the repository that plays them. No package
either: nothing is published from `src/lib/`, and anything another repository would render
unchanged belongs in the hub. No component workshop, because the studio authors no shared
component; see [Decision 0009](../decisions/0009-no-component-workshop-yet.md).

And no Blender in CI. The model is rebuilt by a local recipe that reads a chain of earlier
studies kept in the repository they came from; CI only proves that what is committed is
what the manifest lists. [Large files](large-files.md) says why the rebuild chain is not
here.

## Related pages

- [Decision 0001: A static site with no backend](../decisions/0001-static-site-no-backend.md)
- [Decision 0004: A project Pages site](../decisions/0004-a-project-pages-site.md)
- [Decision 0008: The viewer is embedded as-is](../decisions/0008-the-viewer-is-embedded-as-is.md)
- [Large files](large-files.md)
- [Configuration](../reference/configuration.md)
- [Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md)
