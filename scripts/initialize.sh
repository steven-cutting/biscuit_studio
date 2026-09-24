#!/bin/sh
set -eu

project_root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd -P)
cd "$project_root"

git rev-parse --is-inside-work-tree >/dev/null

uv lock
uv sync --frozen

npm install --package-lock-only --ignore-scripts --no-audit
npm ci --no-audit

# Git LFS holds the model's native sources (.gitattributes names them). This
# installs the LFS hooks and filter into this repository's .git/config only,
# so nothing on the machine outside the repository changes and a second run
# is a no-op. Without it a clone sees pointer text where the .blend should be,
# and a commit would store a real .blend as an ordinary blob.
git lfs install --local

# Formatting is normalised once here rather than leaving the first `just check`
# to fail on it.
uv run --frozen ruff check --fix-only .
uv run --frozen ruff format .
npm run lint:fix

# Hooks are installed only from the primary checkout. Every worktree of this
# repository shares one .git/hooks directory, and `prek install` writes a shim
# naming an absolute path into whichever worktree ran it — so a hook installed
# from a secondary worktree runs that worktree's virtual environment for commits
# made anywhere, and keeps doing so after the worktree is deleted, at which point
# every commit fails on a `prek` that is not on PATH. The comparison is the test
# git itself uses: in a secondary worktree the common directory and the git
# directory differ.
if [ "$(git rev-parse --git-common-dir)" = "$(git rev-parse --git-dir)" ]; then
    just install-hooks
else
    printf '%s\n' 'Secondary worktree: skipping install-hooks.' >&2
    printf '%s\n' 'Run just install-hooks once from the primary checkout.' >&2
fi

printf '\n%s\n' 'Ready. Next: just check.'
printf '%s\n' 'Nothing has been staged, committed, tagged, or pushed.'
