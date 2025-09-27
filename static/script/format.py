import re
import os
from pathlib import Path

empty_line_in_md = ["", "", ""]

def insert_toc(file_path):
    """
    在第一个一级标题和第一个二级标题之间插入 TOC
    """
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # --- 生成 TOC ---
    toc = []
    pattern = re.compile(r"^(#{2,6})\s+(.*)")
    for line in lines:
        match = pattern.match(line)
        if match:
            level = len(match.group(1)) - 1
            title = match.group(2).strip()
            anchor = re.sub(r"[^\w\s-]", "", title).lower()
            anchor = re.sub(r"\s+", "-", anchor)
            toc.append(f"{'   ' * level}* [{title}](#{anchor})")
    toc_text = "\n".join(toc)

    # --- 插入 TOC ---
    first_h1_idx, first_h2_idx = None, None
    for i, line in enumerate(lines):
        if line.startswith("# "):
            first_h1_idx = i
        elif line.startswith("## "):
            first_h2_idx = i
            break

    if first_h1_idx is not None and first_h2_idx is not None:
        new_lines = (
            lines[:first_h1_idx + 1]
            + empty_line_in_md
            + toc_text.splitlines()
            + empty_line_in_md
            + lines[first_h2_idx:]
        )
        path.write_text("\n".join(new_lines), encoding="utf-8")
    else:
        print(f"插入 TOC 失败：{file_path}")

def format_heading(file_path):
    """
    规范化 Markdown 文件：
    1. 确保所有标题 # 和标题内容之间有空格。
    2. 确保所有二级标题之前严格只有一个空行。
    """
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    new_lines = []

    for line in lines:
        # 规则1：修正 # 和标题内容之间的空格
        match = re.match(r"^(#+)\s*(.*)", line)
        if match:
            line = f"{match.group(1)} {match.group(2)}"

        # 规则2：二级标题前严格一行空行
        if line.startswith("## ") and new_lines:
            while new_lines and new_lines[-1].strip() == "":
                new_lines.pop()
            new_lines.extend(empty_line_in_md)

        new_lines.append(line)

    file_path.write_text("\n".join(new_lines), encoding="utf-8")

if __name__ == "__main__":
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(curr_dir, "../../"))
    for file_name in Path(root_dir).rglob("*.md"):
        format_heading(file_name)
        if file_name.name.lower() == "readme.md":
            continue
        insert_toc(file_name)