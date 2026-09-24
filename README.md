# biscuit_studio

The Biscuit Games studio: where the platform's graphical assets are developed — the
poseable model of Biscuit, the renders made from it, the illustrations — and a static site
on GitHub Pages that shows them, built on the platform package
`@steven-cutting/biscuit-games` so it reads as the same product as every game.

Under construction. `tickets/README.md` is the work breakdown and
`tickets/CONVENTIONS.md` the design; `docs/README.md` is the handbook's map.

## Quick start

```console
just initialize
just check
```

`just initialize` is the whole first run: both lockfiles, both toolchains, Git LFS for
this repository, and the hooks. `just check` is every gate, read-only. Reading the
platform package needs a GitHub token carrying `read:packages` in `~/.npmrc`; see
[Develop locally](docs/how-to/develop-locally.md).
