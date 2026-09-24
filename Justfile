set positional-arguments := true
set shell := ["sh", "-eu", "-c"]

default:
    @just --list

# ------------------------------------------------------------------ setup ---

# One explicit first-run command. Never stages, commits, tags, or pushes.
initialize:
    sh scripts/initialize.sh

sync:
    uv sync --frozen
    test -f package-lock.json || { printf '%s\n' 'package-lock.json is missing; run just initialize first' >&2; exit 2; }
    npm ci --no-audit

lock:
    uv lock
    npm install --package-lock-only --ignore-scripts --no-audit

lock-upgrade:
    uv lock --upgrade
    npm update --package-lock-only --ignore-scripts --no-audit

lock-check:
    uv lock --check
    npm ci --ignore-scripts --dry-run --no-audit

install-hooks:
    git rev-parse --is-inside-work-tree >/dev/null
    test -f uv.lock || { printf '%s\n' 'uv.lock is missing; run just initialize first' >&2; exit 2; }
    uv run --frozen prek install --overwrite --hook-type=pre-commit

# ---------------------------------------------------------------- develop ---

dev:
    npm run dev

# Serves the build in build/.
preview:
    npm run preview

# The iteration loop. Here rather than in the check section because it never
# exits; `just frontend-unit` is the recipe that answers. It pins `vite.config.ts`
# for the same reason both other test recipes do — left to its own discovery
# Vitest would still find `vite.config.ts`; the pin is kept so the three test
# recipes read the same.
# Watch one path, or everything: `just frontend-watch tests/brand.test.ts`.
frontend-watch target="":
    npm run test:watch -- ${1:+"$1"}

# ----------------------------------------------------------------- format ---

format:
    uv run --frozen ruff check --fix-only .
    uv run --frozen ruff format .
    npm run format

fix:
    -uv run --frozen prek run --all-files --config .pre-commit-fix.yaml
    uv run --frozen prek run --all-files --config .pre-commit-fix.yaml
    npm run lint:fix
    just lint

# ------------------------------------------------------------------ check ---

lint:
    uv run --frozen prek run --all-files

frontend-static:
    npm run lint
    npm run check

frontend-unit:
    npm run test

frontend-coverage:
    npm run coverage

frontend-build:
    npm run build

# --------------------------------------------------------------- documents ---

check-docs:
    uv run --frozen prek run --all-files markdownlint-cli2 typos lychee
    uv run --frozen bg-validate-docs

check-agents:
    uv run --frozen bg-validate-agents

# ------------------------------------------------------------------ assets ---

# Every file under assets/ and static/pose-studio/ against assets/manifest.json:
# present, listed, and byte-identical to the recorded sha256. An LFS pointer is
# verified from the oid it carries, so a checkout with lfs: false passes and CI
# never fetches an object. Refuses EXIF beyond an image's resolution, and TIFF.
check-assets:
    uv run --frozen python scripts/check_assets.py check

# Rewrites assets/manifest.json from the worktree. The one recipe that writes
# it; it keeps every entry's `source` and `licence` fields and recomputes the
# rest. Run it after an import, then read the diff before committing.
assets-manifest:
    uv run --frozen python scripts/check_assets.py write

# ------------------------------------------------------------------- model ---

# Rebuilds the approved model from its sources. Needs Blender and a checkout of
# biscuit_pics at the commit assets/models/biscuit/README.md names, because the
# build reads the earlier studies there. Never part of `just check`.
#   just model-rebuild /path/to/biscuit_pics
model-rebuild biscuit_pics:
    sh scripts/rebuild_model.sh "$1"

check-links-online:
    uv run --frozen prek run --all-files --hook-stage manual lychee-online

# ---------------------------------------------------------------- aggregate ---

check-clean baseline="":
    uv run --frozen bg-project-check clean "$1"

# The complete gate.
check:
    uv run --frozen bg-project-check run
