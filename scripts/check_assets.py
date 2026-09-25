"""Every asset listed, and byte-identical to its listing: the checker behind `just check-assets`.

`assets/manifest.json` records every file under `assets/` and `static/pose-studio/`
with its size, its sha256, whether Git LFS holds it, where it came from and under
what licence. `check` proves the worktree agrees with the manifest, after proving
itself with `self-test`; `write` rewrites the manifest from the worktree, keeping the
fields only a person can know, after the same self-test; `self-test` builds a small
tree and asserts the pointer read, the index read, the sha256 comparison, the EXIF
refusal, the `source` forms and the provenance checks are all live.
The format is owned by docs/reference/asset-manifest.md.
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
from PIL.ExifTags import TAGS

ROOTS = ("assets", "static/pose-studio")
MANIFEST = Path("assets/manifest.json")
FIXTURE = Path("tests/fixtures/exif-gps.jpg")
POINTER_HEAD = b"version https://git-lfs.github.com/spec/v1"
POINTER = re.compile(
    r"^version https://git-lfs\.github\.com/spec/v1\noid sha256:([0-9a-f]{64})\nsize (\d+)\n"
)
INSPECTED_SUFFIXES = frozenset(
    {
        ".png",
        ".apng",
        ".jpg",
        ".jpeg",
        ".jpe",
        ".jfif",
        ".mpo",
        ".webp",
        ".gif",
        ".bmp",
        ".avif",
        ".heic",
        ".heif",
    }
)
UNINSPECTABLE_SUFFIXES = frozenset({".tif", ".tiff"})
GPS_IFD = 0x8825
EXIF_IFD = 0x8769
RESOLUTION_TAGS = frozenset({0x011A, 0x011B, 0x0128})  # XResolution, YResolution, ResolutionUnit
REQUIRED_FIELDS = ("path", "bytes", "sha256", "storage", "source", "licence")
OPTIONAL_FIELDS = ("source_sha256", "patched")
STORAGES = frozenset({"blob", "lfs"})
HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
# The three forms of `source` that docs/reference/asset-manifest.md gives: imported
# from a repository at a commit, regenerated here on a date, or made here.
SOURCE = re.compile(r"^(?:[A-Za-z0-9._-]+@[0-9a-f]{7,40}:.+|rebuilt:\d{4}-\d{2}-\d{2}|studio)$")
SOURCE_FORMS = "<repository>@<commit>:<path>, rebuilt:<date> or studio"
# A served file patched after its build, mapped to the record its build writes with
# the unpatched digest under "sha256": viewer.py writes qa/viewer-package.json before
# scripts/rebuild_model.sh rewrites the viewer's links. The entry's source_sha256 is
# therefore derived from the worktree by `write` and proved by `check`, never copied.
PROVENANCE = {
    "static/pose-studio/viewer.html": Path("assets/models/biscuit/qa/viewer-package.json"),
}


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
        return parse_pointer(path.read_bytes()[:512])
    except OSError:
        return None


def parse_pointer(head: bytes) -> tuple[str, int] | None:
    """The oid and size the first bytes of an LFS pointer carry, or None for any other bytes."""
    if not head.startswith(POINTER_HEAD):
        return None
    match = POINTER.match(head.decode("ascii", errors="replace"))
    return (match.group(1), int(match.group(2))) if match else None


def index_findings(root: Path, paths: list[Path], storage: dict[Path, str]) -> list[str]:
    """Every LFS path the index holds as the file itself rather than as a pointer.

    `.gitattributes` says what should be in LFS; only the index says what Git stored. A
    `.blend` added on a machine without git-lfs is a full blob whose bytes still hash to
    the recorded oid, so nothing else here would notice. A path not yet in the index is
    skipped: there is nothing to read until it is added.
    """
    tracked = [p.as_posix() for p in paths if storage.get(p) == "lfs"]
    if not tracked:
        return []
    listed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--", *tracked],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    findings: list[str] = []
    for name in filter(None, listed.split("\0")):
        blob = subprocess.run(
            ["git", "-C", str(root), "cat-file", "blob", f":{name}"],
            check=True,
            capture_output=True,
        ).stdout
        if parse_pointer(blob[:512]) is None:
            findings.append(
                f"{name}: the index holds the file itself, not an LFS pointer; run git lfs install --local, then git rm --cached and git add it"
            )
    return findings


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
    """Why an image may not be committed: EXIF beyond its resolution, or a format that cannot be inspected."""
    suffix = path.suffix.lower()
    if suffix not in INSPECTED_SUFFIXES | UNINSPECTABLE_SUFFIXES or pointer(path) is not None:
        return []
    if suffix in UNINSPECTABLE_SUFFIXES:
        return [
            "a TIFF, whose structure is stored as EXIF tags and cannot be told from metadata; export it as PNG"
        ]
    try:
        with Image.open(path) as image:
            exif = image.getexif()
    except (UnidentifiedImageError, OSError) as error:
        return [f"not a readable image ({error})"]
    tags = sorted(set(exif) - RESOLUTION_TAGS) + sorted(exif.get_ifd(EXIF_IFD))
    if exif.get_ifd(GPS_IFD) and GPS_IFD not in tags:
        tags.append(GPS_IFD)
    if not tags:
        return []
    names = ", ".join(TAGS.get(tag, f"0x{tag:04X}") for tag in tags)
    return [f"carries EXIF ({names}); strip every metadata field before committing"]


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
    source = entry.get("source")
    if source and not (isinstance(source, str) and SOURCE.match(source)):
        findings.append(f"{name}: source must be {SOURCE_FORMS}")
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
    findings.extend(f"{name}: {reason}" for reason in provenance_findings(entry))
    return findings


def provenance_findings(entry: dict[str, object]) -> list[str]:
    """Why the optional fields, present only where true, are not true: shape, or one without the other."""
    findings: list[str] = []
    if ("source_sha256" in entry) != ("patched" in entry):
        findings.append("source_sha256 and patched go together")
    if "source_sha256" in entry:
        source = entry["source_sha256"]
        if not isinstance(source, str) or not HEX_SHA256.match(source):
            findings.append("source_sha256 must be 64 lowercase hex digits")
        elif source == entry.get("sha256"):
            findings.append(
                "source_sha256 equals sha256, so nothing was patched; remove both fields"
            )
    if "patched" in entry:
        patched = entry["patched"]
        if (
            not isinstance(patched, list)
            or not patched
            or not all(isinstance(item, str) and item for item in patched)
        ):
            findings.append("patched must be a non-empty list of non-empty strings")
    return findings


def recorded_source_sha256(root: Path, name: str) -> str | None:
    """The unpatched digest the build recorded for `name`, or None when no record is present."""
    record = PROVENANCE.get(name)
    if record is None or not (root / record).is_file():
        return None
    try:
        data = json.loads((root / record).read_text(encoding="utf-8"))
    except OSError, ValueError:
        return None
    sha = data.get("sha256") if isinstance(data, dict) else None
    return sha if isinstance(sha, str) and HEX_SHA256.match(sha) else None


def record_findings(root: Path, entries: dict[str, dict[str, object]]) -> list[str]:
    """Every patched file whose source_sha256 is not what its build recorded."""
    findings: list[str] = []
    for name, record in PROVENANCE.items():
        entry = entries.get(name)
        if entry is None or not (root / record).is_file():
            continue
        recorded = recorded_source_sha256(root, name)
        if recorded is None:
            findings.append(f"{record.as_posix()}: carries no readable sha256 for {name}")
        elif entry.get("source_sha256") != recorded:
            findings.append(
                f"{name}: source_sha256 must equal the sha256 in {record.as_posix()}; run just assets-manifest"
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
    findings.extend(index_findings(root, files, storage))
    findings.extend(record_findings(root, entries))
    return findings


def render(assets: list[dict[str, object]]) -> str:
    if not assets:
        return '{\n  "schema_version": 1,\n  "assets": []\n}\n'
    lines = ",\n".join("    " + json.dumps(entry, separators=(", ", ": ")) for entry in assets)
    return '{\n  "schema_version": 1,\n  "assets": [\n' + lines + "\n  ]\n}\n"


def write_tree(root: Path) -> list[str]:
    """Rewrite the manifest from the worktree, keeping what only a person can know.

    A patched file's source_sha256 is not that: its build recorded it, so it is read
    from the record (PROVENANCE) rather than carried forward.
    """
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
        if (recorded := recorded_source_sha256(root, name)) is not None:
            entry["source_sha256"] = recorded
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
        problems.extend(self_test_index(stage, models / "model.blend"))
        problems.extend(self_test_source(stage))
        shutil.copy(fixture, models / "photo.jpg")
        if not any("GPS" in found for found in write_tree(stage)):
            problems.append("an image carrying GPS EXIF was not refused")
        (models / "photo.jpg").unlink()
        if found := write_tree(stage):
            problems.append(f"the tree was refused after the photograph left: {found}")

        def expect(name: str, marker: str | None, exif: Image.Exif | None = None) -> None:
            """Save a one-pixel image as `name`; assert `check` names `marker`, or passes when None."""
            target = models / name
            Image.new("RGB", (1, 1), (61, 35, 19)).save(
                target, **({"exif": exif} if exif is not None else {})
            )
            found = write_tree(stage)
            if marker is None and found:
                problems.append(f"{name} was refused: {found}")
            if marker is not None and not any(marker in item for item in found):
                problems.append(f"{name} was not refused naming {marker}: {found}")
            target.unlink()
            if leftover := write_tree(stage):
                problems.append(f"the tree was refused after {name} left: {leftover}")

        dated = Image.Exif()
        dated.get_ifd(EXIF_IFD)[0x9003] = "2026:09:23 00:00:00"
        expect("dated.jpg", "EXIF", dated)
        render = Image.Exif()
        render[0x011A] = 72.0
        render[0x011B] = 72.0
        expect("render.png", None, render)
        tagged = Image.Exif()
        tagged[0x0131] = "self-test"
        expect("tagged.webp", "EXIF", tagged)
        expect("clean.webp", None)
        expect("flat.tif", "TIFF")
        problems.extend(self_test_provenance(stage))
        with (models / "blob.bin").open("r+b") as stream:
            stream.seek(0)
            stream.write(b"B")
        if not any("sha256" in found for found in check_tree(stage)):
            problems.append("a changed byte was not refused")
    return problems


def self_test_index(stage: Path, blend: Path) -> list[str]:
    """Prove a `.blend` the index holds as the file itself is refused, and a pointer is not.

    `hash-object --stdin` and `update-index --cacheinfo` put the blob in the index without
    the LFS filter, so the stage needs no git-lfs and the outcome does not depend on the
    machine's configuration.
    """
    problems: list[str] = []
    name = blend.relative_to(stage).as_posix()

    def stage_blob(content: bytes) -> None:
        oid = (
            subprocess.run(
                ["git", "-C", str(stage), "hash-object", "-w", "--stdin"],
                input=content,
                check=True,
                capture_output=True,
            )
            .stdout.decode("ascii")
            .strip()
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(stage),
                "update-index",
                "--add",
                "--cacheinfo",
                f"100644,{oid},{name}",
            ],
            check=True,
        )

    stage_blob(b"not really a blend")
    if not any("not an LFS pointer" in found for found in check_tree(stage)):
        problems.append("a .blend the index holds as the file itself was not refused")
    stage_blob(blend.read_bytes())
    if found := check_tree(stage):
        problems.append(f"a .blend the index holds as a pointer was refused: {found}")
    return problems


def self_test_source(stage: Path) -> list[str]:
    """Prove `source` is held to its three forms; ends with the entry as `write` left it."""
    problems: list[str] = []
    name = "assets/models/blob.bin"
    cases = (
        ("unknown", False),
        ("biscuit_pics@1d9d358:models/blob.bin", True),
        ("rebuilt:2026-09-24", True),
        ("studio", True),
    )
    for source, accepted in cases:
        entries = load_manifest(stage)
        entries[name] = {**entries[name], "source": source}
        (stage / MANIFEST).write_text(render(list(entries.values())), encoding="utf-8")
        found = [item for item in check_tree(stage) if "source must be" in item]
        if accepted and found:
            problems.append(f"source {source!r} was refused: {found}")
        if not accepted and not found:
            problems.append(f"source {source!r} was not refused")
    return problems


def self_test_provenance(stage: Path) -> list[str]:
    """Prove the optional fields are checked for shape and, for the viewer, against its build record."""
    problems: list[str] = []
    viewer = "static/pose-studio/viewer.html"
    record = PROVENANCE[viewer]
    built = b"<html>biscuit</html>"
    (stage / viewer).parent.mkdir(parents=True)
    (stage / viewer).write_bytes(built.replace(b"biscuit", b"biscuit, patched"))
    (stage / record).parent.mkdir(parents=True)
    (stage / record).write_text(json.dumps({"sha256": hashlib.sha256(built).hexdigest()}))
    # write derives source_sha256 from the record; patched stays a person's to write, and
    # check says so until they do.
    if not any("go together" in found for found in write_tree(stage)):
        problems.append("a derived source_sha256 without patched was not refused")
    if load_manifest(stage)[viewer].get("source_sha256") != hashlib.sha256(built).hexdigest():
        problems.append("write did not take the viewer's source_sha256 from its build record")

    def expect(marker: str | None, **fields: object) -> None:
        """Rewrite the manifest with the viewer entry changed; assert `check` names `marker`, or passes when None."""
        entries = load_manifest(stage)
        entries[viewer] = {**entries[viewer], **fields}
        (stage / MANIFEST).write_text(render(list(entries.values())), encoding="utf-8")
        found = check_tree(stage)
        if marker is None and found:
            problems.append(f"a viewer entry with {fields} was refused: {found}")
        if marker is not None and not any(marker in item for item in found):
            problems.append(f"a viewer entry with {fields} was not refused naming {marker}")

    recorded = hashlib.sha256(built).hexdigest()
    expect(None, source_sha256=recorded, patched=["one link"])
    expect("64 lowercase hex", source_sha256="ABC", patched=["one link"])
    expect("must equal", source_sha256="0" * 64, patched=["one link"])
    expect("non-empty list", source_sha256=recorded, patched=[""])
    (stage / viewer).write_bytes(built)
    expect(
        "nothing was patched",
        source_sha256=recorded,
        sha256=recorded,
        bytes=len(built),
        patched=["x"],
    )
    (stage / viewer).unlink()
    (stage / record).unlink()
    if leftover := write_tree(stage):
        problems.append(f"the tree was refused after the viewer and its record left: {leftover}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify or rewrite assets/manifest.json.")
    parser.add_argument("command", choices=("check", "write", "self-test"))
    command = parser.parse_args().command
    root = repository_root()
    findings = self_test(root)
    if not findings and command == "write":
        findings = write_tree(root)
    elif not findings and command == "check":
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
