#!/usr/bin/env python3
"""Build and verify a deterministic EveryInfra plugin release archive.

The builder intentionally uses only the Python standard library. It validates
public JSON, YAML structure, SVG assets, and local Markdown links before
writing a ZIP under ``dist/``. The resulting archive is verified against the
current source tree before it replaces any previous archive with the same name.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import tempfile
import urllib.parse
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable


REPO = Path(__file__).resolve().parent.parent
DIST = REPO / "dist"
PACKAGE_NAME = "everyinfra-agent-plugins"
PLUGIN = REPO / "plugins" / "everyinfra"
MANIFESTS = (
    PLUGIN / "plugin.json",
    PLUGIN / ".codex-plugin" / "plugin.json",
    PLUGIN / ".claude-plugin" / "plugin.json",
    PLUGIN / ".cursor-plugin" / "plugin.json",
)
VERSIONED_MARKETPLACES = (
    REPO / ".claude-plugin" / "marketplace.json",
    REPO / ".github" / "plugin" / "marketplace.json",
)
REQUIRED_ARCHIVE_PATHS = {
    ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json",
    ".cursor-plugin/marketplace.json",
    ".github/plugin/marketplace.json",
    ".github/workflows/validate.yml",
    "AGENTS.md",
    "CHANGELOG.md",
    "CLAUDE.md",
    "LICENSE",
    "README.md",
    "RELEASING.md",
    "llms.txt",
    "plugins/everyinfra/.codex-plugin/plugin.json",
    "plugins/everyinfra/.claude-plugin/plugin.json",
    "plugins/everyinfra/.cursor-plugin/plugin.json",
    "plugins/everyinfra/plugin.json",
    "scripts/build_release.py",
    "scripts/validate.py",
}
EXCLUDED_DIR_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "dist",
    "node_modules",
}
EXCLUDED_FILE_NAMES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".log", ".pyc", ".pyo", ".swp"}
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]\n]*\]\(([^)\n]+)\)")
YAML_KEY_RE = re.compile(r"(?:[^\s:#][^:]*|['\"][^'\"]+['\"]):(?:\s.*)?$")


class ReleaseError(RuntimeError):
    """Raised when source or archive validation fails."""


@dataclass(frozen=True)
class SourceFile:
    relative_path: PurePosixPath
    data: bytes


def relative_label(path: Path) -> str:
    try:
        return path.relative_to(REPO).as_posix()
    except ValueError:
        return str(path)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReleaseError(f"missing JSON file: {relative_label(path)}") from exc
    except json.JSONDecodeError as exc:
        raise ReleaseError(f"invalid JSON in {relative_label(path)}: {exc}") from exc


def release_version() -> str:
    versions: dict[str, str] = {}
    for path in MANIFESTS:
        document = load_json(path)
        if not isinstance(document, dict) or not isinstance(document.get("version"), str):
            raise ReleaseError(f"{relative_label(path)} must declare a string version")
        versions[relative_label(path)] = document["version"]

    unique_versions = set(versions.values())
    if len(unique_versions) != 1:
        detail = ", ".join(f"{path}={version}" for path, version in versions.items())
        raise ReleaseError(f"plugin manifest versions do not match: {detail}")
    version = unique_versions.pop()
    if not VERSION_RE.fullmatch(version):
        raise ReleaseError(f"plugin version is not release-safe SemVer: {version!r}")

    for path in VERSIONED_MARKETPLACES:
        document = load_json(path)
        if not isinstance(document, dict) or not isinstance(document.get("plugins"), list):
            raise ReleaseError(f"{relative_label(path)} must contain a plugins array")
        matches = [
            entry
            for entry in document["plugins"]
            if isinstance(entry, dict) and entry.get("name") == "everyinfra"
        ]
        if len(matches) != 1 or matches[0].get("version") != version:
            raise ReleaseError(
                f"{relative_label(path)} must contain one everyinfra entry at version {version}"
            )
    return version


def is_excluded(relative_path: Path) -> bool:
    if any(part in EXCLUDED_DIR_NAMES for part in relative_path.parts):
        return True
    name = relative_path.name
    if name in EXCLUDED_FILE_NAMES or relative_path.suffix in EXCLUDED_SUFFIXES:
        return True
    return name == ".env" or name.startswith(".env.")


def source_bytes(path: Path) -> bytes:
    if not path.is_symlink():
        return path.read_bytes()
    resolved = path.resolve(strict=True)
    try:
        resolved.relative_to(REPO.resolve())
    except ValueError as exc:
        raise ReleaseError(f"refusing external symlink: {relative_label(path)} -> {resolved}") from exc
    if not resolved.is_file():
        raise ReleaseError(f"symlink does not resolve to a file: {relative_label(path)}")
    return resolved.read_bytes()


def collect_source_files() -> list[SourceFile]:
    files: list[SourceFile] = []
    for path in REPO.rglob("*"):
        relative = path.relative_to(REPO)
        if is_excluded(relative) or (not path.is_file() and not path.is_symlink()):
            continue
        files.append(SourceFile(PurePosixPath(relative.as_posix()), source_bytes(path)))
    files.sort(key=lambda item: item.relative_path.as_posix())
    if not files:
        raise ReleaseError("release source tree is empty")
    return files


def validate_json_files(files: Iterable[SourceFile]) -> int:
    count = 0
    for source in files:
        if source.relative_path.suffix != ".json":
            continue
        count += 1
        try:
            json.loads(source.data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ReleaseError(f"invalid JSON in {source.relative_path}: {exc}") from exc
    return count


def validate_yaml_structure(path: PurePosixPath, text: str) -> None:
    """Validate the indentation-based YAML subset used by GitHub metadata.

    GitHub parses the workflow itself before running it. This additional check
    covers issue forms and catches malformed indentation, tabs, missing mapping
    separators, unsafe YAML features, and broken block scalar structure without
    adding PyYAML as a release dependency.
    """

    previous_indent = 0
    previous_opens_block = False
    block_scalar_indent: int | None = None
    saw_document_content = False

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if "\t" in raw_line:
            raise ReleaseError(f"{path}:{line_number} contains a tab")
        if raw_line.rstrip() != raw_line:
            raise ReleaseError(f"{path}:{line_number} has trailing whitespace")
        stripped = raw_line.lstrip(" ")
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw_line) - len(stripped)

        if block_scalar_indent is not None:
            if indent >= block_scalar_indent:
                continue
            block_scalar_indent = None

        if indent % 2:
            raise ReleaseError(f"{path}:{line_number} uses non-two-space indentation")
        if indent > previous_indent and not previous_opens_block:
            raise ReleaseError(f"{path}:{line_number} increases indentation without a parent")
        if indent > previous_indent + 2:
            raise ReleaseError(f"{path}:{line_number} jumps more than one indentation level")
        if re.search(r"(?:^|\s)[&*!][A-Za-z0-9_-]+", stripped):
            raise ReleaseError(f"{path}:{line_number} uses unsupported YAML anchors, aliases, or tags")

        content = stripped[2:] if stripped.startswith("- ") else stripped
        if stripped == "-":
            opens_block = True
        elif YAML_KEY_RE.fullmatch(content):
            _, value = content.split(":", 1)
            value = value.strip()
            opens_block = (
                stripped.startswith("- ")
                or not value
                or value in {"|", ">", "|-", ">-", "|+", ">+"}
            )
            if value in {"|", ">", "|-", ">-", "|+", ">+"}:
                block_scalar_indent = indent + 2
        elif stripped.startswith("- "):
            opens_block = False
        else:
            raise ReleaseError(f"{path}:{line_number} is not a YAML mapping or sequence item")

        saw_document_content = True
        previous_indent = indent
        previous_opens_block = opens_block

    if not saw_document_content:
        raise ReleaseError(f"{path} is empty")


def validate_yaml_files(files: Iterable[SourceFile]) -> int:
    count = 0
    for source in files:
        if source.relative_path.suffix not in {".yml", ".yaml"}:
            continue
        count += 1
        try:
            text = source.data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ReleaseError(f"{source.relative_path} is not UTF-8") from exc
        validate_yaml_structure(source.relative_path, text)
    return count


def validate_svg_files(files: Iterable[SourceFile]) -> int:
    count = 0
    for source in files:
        if source.relative_path.suffix != ".svg":
            continue
        count += 1
        try:
            root = ET.fromstring(source.data)
        except ET.ParseError as exc:
            raise ReleaseError(f"invalid SVG XML in {source.relative_path}: {exc}") from exc
        if root.tag.rsplit("}", 1)[-1] != "svg":
            raise ReleaseError(f"{source.relative_path} does not have an SVG root element")
        if "viewBox" not in root.attrib:
            raise ReleaseError(f"{source.relative_path} must declare a viewBox")
        for element in root.iter():
            local_name = element.tag.rsplit("}", 1)[-1]
            if local_name in {"script", "foreignObject"}:
                raise ReleaseError(f"{source.relative_path} contains unsafe <{local_name}>")
            for attribute, value in element.attrib.items():
                if attribute.rsplit("}", 1)[-1] == "href":
                    resource = urllib.parse.urlsplit(value)
                    if resource.scheme or resource.netloc:
                        raise ReleaseError(f"{source.relative_path} contains an external resource")
    return count


def without_fenced_code(text: str) -> str:
    output: list[str] = []
    in_fence = False
    fence_character = ""
    for line in text.splitlines():
        match = re.match(r"^\s*(```+|~~~+)", line)
        if match:
            marker = match.group(1)
            if not in_fence:
                in_fence = True
                fence_character = marker[0]
            elif marker[0] == fence_character:
                in_fence = False
            continue
        if not in_fence:
            output.append(line)
    return "\n".join(output)


def validate_markdown_links(files: Iterable[SourceFile]) -> int:
    existing_paths = {source.relative_path.as_posix() for source in files}
    count = 0
    for source in files:
        if source.relative_path.suffix != ".md":
            continue
        try:
            text = without_fenced_code(source.data.decode("utf-8"))
        except UnicodeDecodeError as exc:
            raise ReleaseError(f"{source.relative_path} is not UTF-8") from exc
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            count += 1
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            decoded = urllib.parse.unquote(target)
            parsed = urllib.parse.urlsplit(decoded)
            if parsed.scheme:
                if parsed.scheme not in {"http", "https", "mailto", "codex"}:
                    raise ReleaseError(
                        f"{source.relative_path} uses unsupported link scheme: {target}"
                    )
                continue
            if not parsed.path:
                continue
            base = PurePosixPath(source.relative_path).parent
            candidate_parts: list[str] = []
            for part in (base / parsed.path).parts:
                if part in {"", "."}:
                    continue
                if part == "..":
                    if not candidate_parts:
                        raise ReleaseError(f"{source.relative_path} link escapes the repository: {target}")
                    candidate_parts.pop()
                else:
                    candidate_parts.append(part)
            candidate = PurePosixPath(*candidate_parts).as_posix()
            if candidate not in existing_paths and not any(
                path.startswith(candidate.rstrip("/") + "/") for path in existing_paths
            ):
                raise ReleaseError(f"{source.relative_path} has a broken local link: {target}")
    return count


def validate_source(files: list[SourceFile]) -> None:
    json_count = validate_json_files(files)
    yaml_count = validate_yaml_files(files)
    svg_count = validate_svg_files(files)
    link_count = validate_markdown_links(files)
    print(
        "Source asset validation passed: "
        f"{json_count} JSON, {yaml_count} YAML, {svg_count} SVG, {link_count} Markdown links"
    )


def archive_root(version: str) -> PurePosixPath:
    return PurePosixPath(f"{PACKAGE_NAME}-{version}")


def archive_path(version: str) -> Path:
    return DIST / f"{PACKAGE_NAME}-{version}.zip"


def zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (stat.S_IFREG | 0o644) << 16
    return info


def write_archive(destination: Path, version: str, files: list[SourceFile]) -> None:
    root = archive_root(version)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        bundle.comment = f"EveryInfra agent plugin release {version}".encode("ascii")
        for source in files:
            member = (root / source.relative_path).as_posix()
            bundle.writestr(zip_info(member), source.data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def verify_archive(path: Path, version: str, files: list[SourceFile]) -> None:
    if not path.is_file():
        raise ReleaseError(f"release archive does not exist: {path}")
    root = archive_root(version)
    expected = {(root / source.relative_path).as_posix(): source.data for source in files}
    expected_paths = set(expected)

    with zipfile.ZipFile(path, "r") as bundle:
        bad_member = bundle.testzip()
        if bad_member:
            raise ReleaseError(f"archive CRC check failed for {bad_member}")
        members = bundle.infolist()
        names = [member.filename for member in members]
        if len(names) != len(set(names)):
            raise ReleaseError("archive contains duplicate paths")
        if set(names) != expected_paths:
            missing = sorted(expected_paths - set(names))
            extra = sorted(set(names) - expected_paths)
            raise ReleaseError(f"archive content drifted; missing={missing}, extra={extra}")
        for member in members:
            pure_name = PurePosixPath(member.filename)
            if pure_name.is_absolute() or ".." in pure_name.parts:
                raise ReleaseError(f"archive contains an unsafe path: {member.filename}")
            mode = member.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise ReleaseError(f"archive contains a symlink: {member.filename}")
            if member.date_time != ZIP_TIMESTAMP:
                raise ReleaseError(f"archive member timestamp drifted: {member.filename}")
            if bundle.read(member) != expected[member.filename]:
                raise ReleaseError(f"archive member differs from source: {member.filename}")

    relative_names = {
        PurePosixPath(name).relative_to(root).as_posix() for name in expected_paths
    }
    missing_required = sorted(REQUIRED_ARCHIVE_PATHS - relative_names)
    if missing_required:
        raise ReleaseError(f"archive is missing required public files: {missing_required}")


def build_release(version: str, files: list[SourceFile]) -> Path:
    DIST.mkdir(parents=True, exist_ok=True)
    destination = archive_path(version)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".{PACKAGE_NAME}-{version}-", suffix=".zip.tmp", dir=DIST, delete=False
        ) as temporary:
            temporary_path = Path(temporary.name)
        write_archive(temporary_path, version, files)
        verify_archive(temporary_path, version, files)
        os.replace(temporary_path, destination)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return destination


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check-source",
        action="store_true",
        help="validate JSON, YAML structure, SVG assets, and local Markdown links without building",
    )
    mode.add_argument(
        "--verify",
        type=Path,
        metavar="ARCHIVE",
        help="verify an existing archive against the current source tree",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        version = release_version()
        files = collect_source_files()
        validate_source(files)
        if args.check_source:
            return 0
        if args.verify is not None:
            verify_archive(args.verify.resolve(), version, files)
            print(f"Release archive verification passed: {args.verify}")
            return 0
        destination = build_release(version, files)
        print(f"Release archive built and verified: {destination.relative_to(REPO)}")
        return 0
    except (OSError, ReleaseError, zipfile.BadZipFile) as exc:
        print(f"Release build failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
