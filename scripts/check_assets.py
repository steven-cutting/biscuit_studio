"""Every asset listed, and byte-identical to its listing: the checker behind `just check-assets`.

`assets/manifest.json` records every file under `assets/` and `static/pose-studio/`
with its size, its sha256, whether Git LFS holds it, where it came from and under
what licence. `check` proves the worktree agrees with the manifest, after proving
itself with `self-test`; `write` rewrites the manifest from the worktree, keeping the
fields only a person can know; `self-test` builds a small tree and asserts the pointer
read, the sha256 comparison and the EXIF refusal are all live. The format is owned by
docs/reference/asset-manifest.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, UnidentifiedImageError

ROOTS = ("assets", "static/pose-studio")
MANIFEST = Path("assets/manifest.json")
FIXTURE = Path("tests/fixtures/exif-gps.jpg")
POINTER_HEAD = b"version https://git-lfs.github.com/spec/v1"
POINTER = re.compile(
    r"^version https://git-lfs\.github\.com/spec/v1\noid sha256:([0-9a-f]{64})\nsize (\d+)\n"
)
IMAGE_SUFFIXES = frozenset({".png", ".jpg", ".jpeg"})
GPS_IFD = 0x8825
IDENTIFYING_TAGS = {
    0x010F: "Make",
    0x0110: "Model",
    0xA431: "BodySerialNumber",
    0xA435: "LensSerialNumber",
}
REQUIRED_FIELDS = ("path", "bytes", "sha256", "storage", "source", "licence")
OPTIONAL_FIELDS = ("source_sha256", "patched")
STORAGES = frozenset({"blob", "lfs"})


def repository_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], check=False, capture_output=True, text=True
    )
    if result.returncode != 0:
        print("check_assets: run this from inside a Git worktree", file=sys.stderr)
        raise SystemExit(2)
    return Path(result.stdout.strip())


def listed_files(root: Path) -> list[Path]:
    """Every file under the two roots, relative to `root`, the manifest itself excluded."""
    found: list[Path] = []
    for top in ROOTS:
        base = root / top
        if base.is_dir():
            found.extend(p.relative_to(root) for p in base.rglob("*") if p.is_file())
    return sorted(p for p in found if p != MANIFEST)


def attribute_storage(root: Path, paths: list[Path]) -> dict[Path, str]:
    """`lfs` or `blob` per path, as .gitattributes says, whether or not the file exists."""
    if not paths:
        return {}
    result = subprocess.run(
        ["git", "-C", str(root), "check-attr", "filter", "--", *(p.as_posix() for p in paths)],
        check=True,
        capture_output=True,
        text=True,
    )
    storage: dict[Path, str] = {}
    for line in result.stdout.splitlines():
        name, _, value = line.rsplit(": ", 2)
        storage[Path(name)] = "lfs" if value == "lfs" else "blob"
    return storage


def pointer(path: Path) -> tuple[str, int] | None:
    """The oid and size an LFS pointer carries, or None for any other file."""
    try:
        head = path.read_bytes()[:512]
    except OSError:
        return None
    if not head.startswith(POINTER_HEAD):
        return None
    match = POINTER.match(head.decode("ascii", errors="replace"))
    return (match.group(1), int(match.group(2))) if match else None


def digest(path: Path) -> tuple[str, int]:
    sha = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            sha.update(chunk)
            size += len(chunk)
    return sha.hexdigest(), size


def measure(path: Path) -> tuple[str, int]:
    """sha256 and size of the object: the pointer's when Git holds only that, else the bytes'."""
    found = pointer(path)
    return found if found is not None else digest(path)


def exif_findings(path: Path) -> list[str]:
    """Why an image may not be committed: location or camera identity left inside it."""
    if path.suffix.lower() not in IMAGE_SUFFIXES or pointer(path) is not None:
        return []
    try:
        with Image.open(path) as image:
            exif = image.getexif()
    except (UnidentifiedImageError, OSError) as error:
        return [f"not a readable image ({error})"]
    findings = [f"carries EXIF {name}" for tag, name in IDENTIFYING_TAGS.items() if exif.get(tag)]
    if exif.get_ifd(GPS_IFD):
        findings.append("carries GPS EXIF; strip every metadata field before committing")
    return findings


def load_manifest(root: Path) -> dict[str, dict[str, object]]:
    data = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    assets = data.get("assets")
    if not isinstance(assets, list):
        raise TypeError("assets must be a list")
    entries: dict[str, dict[str, object]] = {}
    for index, entry in enumerate(assets):
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise TypeError(f"entry {index} must be an object with a path")
        if entry["path"] in entries:
            raise ValueError(f"{entry['path']} is listed twice")
        entries[entry["path"]] = entry
    return entries


def entry_findings(
    name: str, entry: dict[str, object], measured: tuple[str, int], storage: str
) -> list[str]:
    findings: list[str] = []
    allowed = set(REQUIRED_FIELDS) | set(OPTIONAL_FIELDS)
    if unknown := sorted(set(entry) - allowed):
        findings.append(f"{name}: unknown manifest field(s) {unknown}")
    findings.extend(
        f"{name}: manifest entry lacks {field}"
        for field in REQUIRED_FIELDS
        if not entry.get(field)
    )
    sha, size = measured
    if entry.get("sha256") != sha:
        findings.append(
            f"{name}: sha256 differs from the manifest; run just assets-manifest and read the diff"
        )
    if entry.get("bytes") != size:
        findings.append(f"{name}: size differs from the manifest")
    if entry.get("storage") not in STORAGES:
        findings.append(f"{name}: storage must be blob or lfs")
    elif entry.get("storage") != storage:
        findings.append(
            f"{name}: storage {entry.get('storage')!r} but .gitattributes says {storage!r}"
        )
    return findings


def check_tree(root: Path) -> list[str]:
    """Every finding against the manifest and the worktree, or an empty list."""
    try:
        entries = load_manifest(root)
    except (OSError, TypeError, ValueError) as error:
        return [f"{MANIFEST.as_posix()}: {error}"]
    files = listed_files(root)
    storage = attribute_storage(root, files)
    present = {p.as_posix() for p in files}
    findings = [
        f"{name}: listed in the manifest but absent from the worktree"
        for name in sorted(set(entries) - present)
    ]
    for relative in files:
        name = relative.as_posix()
        entry = entries.get(name)
        if entry is None:
            findings.append(f"{name}: present but not listed; run just assets-manifest")
            continue
        findings.extend(entry_findings(name, entry, measure(root / relative), storage[relative]))
        findings.extend(f"{name}: {reason}" for reason in exif_findings(root / relative))
    return findings


def render(assets: list[dict[str, object]]) -> str:
    if not assets:
        return '{\n  "schema_version": 1,\n  "assets": []\n}\n'
    lines = ",\n".join("    " + json.dumps(entry, separators=(", ", ": ")) for entry in assets)
    return '{\n  "schema_version": 1,\n  "assets": [\n' + lines + "\n  ]\n}\n"


def write_tree(root: Path) -> list[str]:
    """Rewrite the manifest from the worktree, keeping what only a person can know."""
    try:
        existing = load_manifest(root)
    except OSError, TypeError, ValueError:
        existing = {}
    files = listed_files(root)
    storage = attribute_storage(root, files)
    assets: list[dict[str, object]] = []
    for relative in files:
        name = relative.as_posix()
        sha, size = measure(root / relative)
        old = existing.get(name, {})
        entry: dict[str, object] = {
            "path": name,
            "bytes": size,
            "sha256": sha,
            "storage": storage[relative],
            "source": old.get("source", "studio"),
            "licence": old.get("licence", "unsettled"),
        }
        for field in OPTIONAL_FIELDS:
            if field in old:
                entry[field] = old[field]
        assets.append(entry)
    (root / MANIFEST).write_text(render(assets), encoding="utf-8")
    return check_tree(root)


def self_test(root: Path) -> list[str]:
    """Prove the checker is live on a tree built for the purpose."""
    fixture = root / FIXTURE
    if not fixture.is_file():
        return [f"{FIXTURE.as_posix()}: the EXIF fixture is missing"]
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as temporary:
        stage = Path(temporary)
        subprocess.run(["git", "init", "-q", "-b", "main", str(stage)], check=True)
        (stage / ".gitattributes").write_text("*.blend filter=lfs diff=lfs merge=lfs -text\n")
        models = stage / "assets" / "models"
        models.mkdir(parents=True)
        (models / "blob.bin").write_bytes(b"biscuit" * 1000)
        oid = hashlib.sha256(b"not really a blend").hexdigest()
        (models / "model.blend").write_bytes(
            POINTER_HEAD + f"\noid sha256:{oid}\nsize 18\n".encode()
        )
        Image.new("RGB", (1, 1), (61, 35, 19)).save(models / "clean.png")
        if found := write_tree(stage):
            problems.append(f"a clean tree was refused: {found}")
        listed = load_manifest(stage).get("assets/models/model.blend", {})
        if (
            listed.get("sha256") != oid
            or listed.get("storage") != "lfs"
            or listed.get("bytes") != 18
        ):
            problems.append("the LFS pointer was not read for its oid, size and storage")
        shutil.copy(fixture, models / "photo.jpg")
        if not any("GPS" in found for found in write_tree(stage)):
            problems.append("an image carrying GPS EXIF was not refused")
        (models / "photo.jpg").unlink()
        if found := write_tree(stage):
            problems.append(f"the tree was refused after the photograph left: {found}")
        with (models / "blob.bin").open("r+b") as stream:
            stream.seek(0)
            stream.write(b"B")
        if not any("sha256" in found for found in check_tree(stage)):
            problems.append("a changed byte was not refused")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify or rewrite assets/manifest.json.")
    parser.add_argument("command", choices=("check", "write", "self-test"))
    command = parser.parse_args().command
    root = repository_root()
    if command == "write":
        findings = write_tree(root)
    else:
        findings = self_test(root)
        if command == "check" and not findings:
            findings = check_tree(root)
    for finding in findings:
        print(finding, file=sys.stderr)
    if findings:
        print(f"check_assets {command}: {len(findings)} finding(s)", file=sys.stderr)
        return 1
    print(f"check_assets {command}: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
