from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable


DEFAULT_BLACKLIST = ("Blog",)
MARKDOWN_SUFFIXES = {".md", ".markdown"}
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
TOC_LINE_RE = re.compile(r"^\s*[*-]\s+\[[^\]]*\]\(#.*\)\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Regenerate markdown TOC blocks.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Root directory to scan.",
    )
    parser.add_argument(
        "--blacklist",
        nargs="*",
        default=list(DEFAULT_BLACKLIST),
        help="Directory names to skip. Defaults to Blog.",
    )
    parser.add_argument(
        "--include-readme",
        action="store_true",
        help="Generate TOC for README.md too.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Optional markdown files to process.",
    )
    return parser.parse_args()


def should_skip(path: Path, root: Path, blacklist: set[str], include_readme: bool) -> bool:
    if path.suffix.lower() not in MARKDOWN_SUFFIXES:
        return True

    relative = path.relative_to(root)
    if any(part in blacklist for part in relative.parts):
        return True

    if not include_readme and path.name.lower() == "readme.md":
        return True

    return False


def iter_markdown_files(root: Path, blacklist: set[str], include_readme: bool) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file() and not should_skip(path, root, blacklist, include_readme):
            yield path


def normalize_input_paths(
    root: Path,
    paths: list[Path],
    blacklist: set[str],
    include_readme: bool,
) -> list[Path]:
    normalized: list[Path] = []
    seen: set[Path] = set()
    for raw_path in paths:
        path = raw_path if raw_path.is_absolute() else (root / raw_path)
        path = path.resolve()
        if not path.is_file():
            continue
        if should_skip(path, root, blacklist, include_readme):
            continue
        if path in seen:
            continue
        normalized.append(path)
        seen.add(path)
    return sorted(normalized)


def slugify(title: str) -> str:
    slug = title.strip().lower()
    slug = re.sub(r"[`*_~]", "", slug)
    slug = re.sub(r"[^\w\u4e00-\u9fff\-\s]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug


def build_toc(lines: list[str]) -> list[str]:
    toc: list[str] = []
    for line in lines:
        match = HEADING_RE.match(line)
        if not match:
            continue

        level = len(match.group(1))
        if level < 2:
            continue

        title = match.group(2).strip()
        indent = "   " * (level - 2)
        toc.append(f"{indent}* [{title}](#{slugify(title)})")
    return toc


def find_first_heading_indexes(lines: list[str]) -> tuple[int | None, int | None]:
    first_h1 = None
    first_h2 = None
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        if level == 1 and first_h1 is None:
            first_h1 = index
        if level == 2:
            first_h2 = index
            break
    return first_h1, first_h2


def strip_existing_toc(lines: list[str], first_h1: int | None, first_h2: int | None) -> list[str]:
    start = (first_h1 + 1) if first_h1 is not None else 0
    end = first_h2 if first_h2 is not None else len(lines)
    if start >= end:
        return lines

    segment = lines[start:end]
    first_nonblank = next((idx for idx, line in enumerate(segment) if line.strip()), None)
    if first_nonblank is None:
        return lines

    if not TOC_LINE_RE.match(segment[first_nonblank]):
        return lines

    last = first_nonblank
    while last < len(segment):
        current = segment[last]
        if current.strip() == "" or TOC_LINE_RE.match(current):
            last += 1
            continue
        break

    new_segment = segment[:first_nonblank] + segment[last:]
    return lines[:start] + new_segment + lines[end:]

    return lines


def update_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines()
    toc = build_toc(lines)
    if not toc:
        return False

    first_h1, first_h2 = find_first_heading_indexes(lines)
    lines = strip_existing_toc(lines, first_h1, first_h2)
    first_h1, first_h2 = find_first_heading_indexes(lines)

    insert_at = (first_h1 + 1) if first_h1 is not None else first_h2
    if insert_at is None:
        return False

    while insert_at < len(lines) and lines[insert_at].strip() == "":
        del lines[insert_at]
    while insert_at > 0 and lines[insert_at - 1].strip() == "":
        del lines[insert_at - 1]
        insert_at -= 1

    toc_block = [""] + toc + [""]
    lines[insert_at:insert_at] = toc_block

    text = "\n".join(lines)
    if original.endswith("\n"):
        text += "\n"

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def log_change(path: Path, root: Path) -> None:
    try:
        display_path = path.relative_to(root)
    except ValueError:
        display_path = path
    print(f"【目录】{display_path}")


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    blacklist = {item.strip("/") for item in args.blacklist if item.strip("/")}
    target_paths = normalize_input_paths(root, args.paths, blacklist, args.include_readme)
    files = target_paths if target_paths else list(iter_markdown_files(root, blacklist, args.include_readme))

    changed = 0
    for path in files:
        if update_file(path):
            log_change(path, root)
            changed += 1

    print(f"Updated TOC in {changed} files.")


if __name__ == "__main__":
    main()
