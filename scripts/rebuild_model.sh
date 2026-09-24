#!/bin/sh
set -eu

# Rebuilds the approved model from its sources, then puts each output where this
# repository keeps it. Needs Blender and a checkout of biscuit_pics holding the
# study chain assets/models/biscuit/README.md names. Never part of `just check`.
#
#   scripts/rebuild_model.sh /path/to/biscuit_pics
#
# BLENDER names the executable; the default is the macOS application bundle.
#
# It starts only when assets/ and static/pose-studio/ match HEAD, and a run that
# fails or is interrupted restores both to HEAD, so a half-rebuilt set never
# outlives the run.

usage() {
  printf '%s\n' 'usage: scripts/rebuild_model.sh <path to a biscuit_pics checkout>' >&2
  exit 2
}

[ "$#" -eq 1 ] || usage
# Absolute before the cd below: the symlink is resolved from assets/ and the
# study-chain test from the project root, and a relative path satisfies only one.
checkout=$(CDPATH='' cd -- "$1" 2>/dev/null && pwd -P) || usage
blender=${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}

project_root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd -P)
cd "$project_root"

package=assets/models/biscuit
served=static/pose-studio
studies=$checkout/biscuit_pics/generated/3d

[ -d "$studies/miami-cinematic-eyes-refined" ] || {
  printf '%s\n' "no study chain at $studies; see $package/README.md, Provenance" >&2
  exit 2
}
[ -x "$blender" ] || {
  printf '%s\n' "Blender not found at $blender; set BLENDER" >&2
  exit 2
}
git rev-parse --is-inside-work-tree >/dev/null
# A clean start is what makes the restore below safe: anything it removes was
# written by this run.
[ -z "$(git status --porcelain --untracked-files=all -- assets "$served")" ] || {
  printf '%s\n' "assets/ or $served/ differs from HEAD; commit or remove the changes first" >&2
  exit 2
}

# src/common.py and src/viewer.py resolve the studies two directories above the
# package, which is assets/ here. A link there, removed on exit, is what makes
# assets/biscuit_pics/generated/3d/... resolve without editing either script.
link=assets/biscuit_pics
[ ! -e "$link" ] || { printf '%s\n' "$link already exists; remove it first" >&2; exit 2; }

# The manifest walk lists every file, ignored or not, so the build's by-products
# go before it: Python's bytecode caches (PYTHONDONTWRITEBYTECODE reaches uv's
# Python; Blender may ignore it) and the .blend1 backup Blender keeps when
# build.py saves over the existing .blend.
export PYTHONDONTWRITEBYTECODE=1
purge_debris() {
  find "$package" -name __pycache__ -type d -prune -exec rm -rf {} +
  find "$package" -name '*.blend1' -type f -exec rm -f {} +
}

finished=0
cleanup() {
  status=$?
  rm -f "$link" || true
  if [ "$finished" -ne 1 ]; then
    purge_debris || true
    git restore --source=HEAD --staged --worktree -- assets "$served" || true
    git clean -fdq -- assets "$served" || true
    printf '%s\n' "rebuild failed; assets/ and $served/ restored to HEAD" >&2
    [ "$status" -ne 0 ] || status=1
  fi
  exit "$status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
ln -s "$checkout/biscuit_pics" "$link"

# The five commands the package's README gives, in its order, from inside it.
# build.py writes model/biscuit-poseable.blend and model/biscuit-poseable.glb;
# viewer.py writes viewer.html and qa/viewer-package.json; verify.py writes the
# qa records; render.py writes previews/native/; proof_sheet.py writes
# previews/pose-overview.jpg.
(
  cd "$package"
  "$blender" --background --python-exit-code 1 --python src/build.py
  uv run --frozen python src/viewer.py
  "$blender" --background --python-exit-code 1 --python src/verify.py
  "$blender" --background --python-exit-code 1 --python src/render.py
  uv run --frozen python src/proof_sheet.py
)

# The build is done with the checkout; the link leaves before the manifest is
# written, so the walk under assets/ never meets it. The trap stays for an
# interrupted run.
rm -f "$link"
purge_debris

# The three outputs the site serves live beside the viewer, not in the package.
mv "$package/viewer.html" "$served/viewer.html"
mv "$package/model/biscuit-poseable.glb" "$served/model/biscuit-poseable.glb"
mv "$package/previews/pose-overview.jpg" "$served/previews/pose-overview.jpg"

# The viewer links two files the site does not serve; the same three rewrites
# the first import made, asserted the same way. assets/manifest.json records
# them under `patched`.
uv run --frozen python - <<'PYEOF'
from pathlib import Path
p = Path("static/pose-studio/viewer.html")
s = p.read_bytes()
pairs = [
    (b'href="model/biscuit-poseable.blend"', b'href="https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/model/biscuit-poseable.blend"', 2),
    (b'href="README.md"', b'href="https://github.com/steven-cutting/biscuit_studio/blob/main/assets/models/biscuit/README.md"', 1),
]
for old, new, n in pairs:
    assert s.count(old) == n, (old, s.count(old))
    s = s.replace(old, new)
p.write_bytes(s)
PYEOF

just assets-manifest
finished=1

printf '\n%s\n' 'Rebuilt. Read the assets/manifest.json diff, then set each changed entry'
printf '%s\n' 'source to rebuilt:<date> and its source_sha256 to the new viewer digest.'
printf '%s\n' 'Nothing has been staged, committed, tagged, or pushed.'
