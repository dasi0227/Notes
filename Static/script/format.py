from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable


DEFAULT_BLACKLIST = ("Blog",)
MARKDOWN_SUFFIXES = {".md", ".markdown"}
INLINE_CODE_RE = re.compile(r"(`+)([^`]*?)\1")
MARKDOWN_LINK_RE = re.compile(r"(!?\[[^\]]*\]\([^)]+\))")
FENCE_RE = re.compile(r"^\s*(```+|~~~+)")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]*(.*?)[ \t]*$")

# 仅匹配“中文术语（English / Acronym）”这类容易被 GitHub 错误渲染的整段加粗
BROKEN_BOLD_RE = re.compile(
    r"(?<!\*)\*\*"
    r"([\u4e00-\u9fffA-Za-z0-9/\-+&· ]+（[A-Za-z0-9][A-Za-z0-9 ,./:+\-&]*）)"
    r"\*\*(?!\*)"
)

CJK_RE = r"[\u3400-\u4dbf\u4e00-\u9fff]"
ASCII_RE = r"[A-Za-z0-9]"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize markdown notes.")
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
        help="Format README.md as a normal markdown file.",
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


def transform_outside_protected_spans(text: str, transform) -> str:
    parts: list[str] = []
    last_end = 0
    protected = re.compile(
        f"{INLINE_CODE_RE.pattern}|{MARKDOWN_LINK_RE.pattern}"
    )
    for match in protected.finditer(text):
        parts.append(transform(text[last_end:match.start()]))
        parts.append(match.group(0))
        last_end = match.end()
    parts.append(transform(text[last_end:]))
    return "".join(parts)


def normalize_cjk_ascii_spacing(segment: str) -> str:
    segment = re.sub(fr"({CJK_RE})\s+({ASCII_RE})", r"\1 \2", segment)
    segment = re.sub(fr"({ASCII_RE})\s+({CJK_RE})", r"\1 \2", segment)
    segment = re.sub(fr"({CJK_RE})({ASCII_RE})", r"\1 \2", segment)
    segment = re.sub(fr"({ASCII_RE})({CJK_RE})", r"\1 \2", segment)
    return segment


def normalize_line_content(line: str) -> str:
    line = BROKEN_BOLD_RE.sub(r"\1", line)
    return transform_outside_protected_spans(line, normalize_cjk_ascii_spacing)


def format_heading_line(line: str) -> str:
    match = HEADING_RE.match(line)
    if not match:
        return line

    hashes, content = match.groups()
    if not content:
        return hashes
    return f"{hashes} {content.strip()}"


def count_table_cells(line: str) -> int:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return len([cell for cell in stripped.split("|")])


def split_table_cells(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]

    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in stripped:
        if escaped:
            current.append(char)
            escaped = False
            continue

        if char == "\\":
            current.append(char)
            escaped = True
            continue

        if char == "|":
            cells.append("".join(current).strip())
            current = []
            continue

        current.append(char)

    cells.append("".join(current).strip())
    return cells


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-+:?", cell) for cell in cells)


def pad_cells(cells: list[str], target: int) -> list[str]:
    if len(cells) < target:
        return cells + [""] * (target - len(cells))
    return cells[:target]


def format_separator(cells: list[str], target: int) -> str:
    normalized = []
    for cell in pad_cells(cells, target):
        marker = cell.strip()
        if not marker:
            normalized.append("---")
        elif marker.startswith(":") and marker.endswith(":"):
            normalized.append(":---:")
        elif marker.startswith(":"):
            normalized.append(":---")
        elif marker.endswith(":"):
            normalized.append("---:")
        else:
            normalized.append("---")
    return "| " + " | ".join(normalized) + " |"


def format_table_block(block: list[str]) -> list[str]:
    rows = [split_table_cells(line) for line in block]
    data_rows = [row for row in rows if not is_separator_row(row)]
    if not data_rows:
        return block

    target_cols = max(len(row) for row in data_rows)
    has_separator = any(is_separator_row(row) for row in rows)
    formatted: list[str] = []

    separator_written = False
    for index, row in enumerate(rows):
        if is_separator_row(row):
            if not separator_written:
                formatted.append(format_separator(row, target_cols))
                separator_written = True
            continue

        current = pad_cells(row, target_cols)
        formatted.append("| " + " | ".join(current) + " |")

        if index == 0 and not has_separator:
            formatted.append("| " + " | ".join(["---"] * target_cols) + " |")
            separator_written = True

    return formatted


def format_table_blocks(lines: list[str]) -> list[str]:
    result: list[str] = []
    in_fence = False
    i = 0

    while i < len(lines):
        line = lines[i]
        if FENCE_RE.match(line):
            in_fence = not in_fence
            result.append(line)
            i += 1
            continue

        if in_fence:
            result.append(line)
            i += 1
            continue

        if line.count("|") >= 2:
            block: list[str] = []
            while i < len(lines):
                current = lines[i]
                if FENCE_RE.match(current) or current.count("|") < 2 or not current.strip():
                    break
                block.append(current)
                i += 1

            if len(block) >= 2 and any(is_separator_row(split_table_cells(row)) for row in block[:3]):
                result.extend(format_table_block(block))
                continue

            result.extend(block)
            continue

        result.append(line)
        i += 1

    return result


def log_change(change_type: str, path: Path, root: Path) -> None:
    try:
        display_path = path.relative_to(root)
    except ValueError:
        display_path = path
    print(f"【{change_type}】{display_path}")


def collapse_blank_lines_between_list_items(lines: list[str]) -> list[str]:
    result: list[str] = []
    in_fence = False
    i = 0

    while i < len(lines):
        line = lines[i]
        if FENCE_RE.match(line):
            in_fence = not in_fence
            result.append(line)
            i += 1
            continue

        if in_fence:
            result.append(line)
            i += 1
            continue

        result.append(line)
        if LIST_ITEM_RE.match(line):
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j > i + 1 and j < len(lines) and LIST_ITEM_RE.match(lines[j]):
                i = j
                continue
        i += 1

    return result


def format_file(path: Path, root: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines()

    processed: list[str] = []
    in_fence = False
    heading_changed = False
    spacing_changed = False
    bold_changed = False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            processed.append(line)
            continue

        if in_fence:
            processed.append(line)
            continue

        normalized_line = normalize_line_content(line)
        if normalized_line != line:
            if BROKEN_BOLD_RE.sub(r"\1", line) != line:
                bold_changed = True
            if normalized_line != line:
                spacing_changed = True

        formatted_heading = format_heading_line(normalized_line)
        if formatted_heading != normalized_line:
            heading_changed = True
        processed.append(formatted_heading)

    list_formatted = collapse_blank_lines_between_list_items(processed)
    list_changed = list_formatted != processed

    table_formatted = format_table_blocks(list_formatted)
    table_changed = table_formatted != list_formatted

    processed = table_formatted

    text = "\n".join(processed)
    if original.endswith("\n"):
        text += "\n"

    if text != original:
        path.write_text(text, encoding="utf-8")
        if heading_changed:
            log_change("标题", path, root)
        if spacing_changed:
            log_change("空格", path, root)
        if list_changed:
            log_change("列表", path, root)
        if bold_changed:
            log_change("加粗", path, root)
        if table_changed:
            log_change("表格", path, root)
        return True
    return False


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    blacklist = {item.strip("/") for item in args.blacklist if item.strip("/")}
    target_paths = normalize_input_paths(root, args.paths, blacklist, args.include_readme)
    files = target_paths if target_paths else list(iter_markdown_files(root, blacklist, args.include_readme))

    changed = 0
    for path in files:
        if format_file(path, root):
            changed += 1

    print(f"Formatted {changed} files.")


if __name__ == "__main__":
    main()
