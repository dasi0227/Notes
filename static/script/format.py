import re
import os
from pathlib import Path

empty_line_in_md = ["", "", ""]

def insert_toc(file: Path):
    """
    在第一个一级标题和第一个二级标题之间插入 TOC
    """
    lines = file.read_text(encoding="utf-8").splitlines()

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

    if first_h1_idx is None or first_h2_idx is None:
        print(f"插入 TOC 失败：{file}")
        return
    
    new_lines = (
        lines[:first_h1_idx + 1]
        + empty_line_in_md
        + toc_text.splitlines()
        + empty_line_in_md
        + lines[first_h2_idx:]
    )
    file.write_text("\n".join(new_lines), encoding="utf-8")

def format_heading(file: Path):
    """
    规范化标题
    """
    lines = file.read_text(encoding="utf-8").splitlines()
    
    new_lines = []
    for line in lines:
        # 确保所有标题 # 和标题内容之间有空格
        match = re.match(r"^(#+)\s*(.*)", line)
        if match:
            line = f"{match.group(1)} {match.group(2)}"

        # 确保所有二级标题之前严格只有一个空行
        if line.startswith("## ") and new_lines:
            while new_lines and new_lines[-1].strip() == "":
                new_lines.pop()
            new_lines.extend(empty_line_in_md)

        new_lines.append(line)

    file.write_text("\n".join(new_lines), encoding="utf-8")

def format_list(file: Path):
    """
    规范化两个列表项之间没有多余的空行
    """
    lines = file.read_text(encoding="utf-8").splitlines()
    
    i = 0
    new_lines = []
    n = len(lines)

    while i < n:
        new_lines.append(lines[i])
        
        # 当前行是列表
        if lines[i].lstrip().startswith("- "):
            j = i + 1
            count = 0
            # 检测后面的空行
            while j < n and lines[j].strip() == "":
                count += 1
                j += 1
            # 下一个非空行也是列表
            if j < n and lines[j].lstrip().startswith("- ") and count >= 2:
                print(f"{file}: 第 {i} 列表行和第 {j} 列表行有 {count} 个空行，已压缩为 1 行")
                new_lines.append("")
                i = j
                continue
        i += 1

    file.write_text("\n".join(lines), encoding="utf-8")

def format_space(file: Path):
    """
    规范化中文字符与非中文字符间的空格
    """
    text = file.read_text(encoding="utf-8")

    # 1. 中文在左，英文或数字在右 -> 加空格
    text = re.sub(r"([\u4e00-\u9fff])([`A-Za-z0-9])", r"\1 \2", text)

    # 2. 英文或数字在左，中文在右 -> 加空格
    text = re.sub(r"([`A-Za-z0-9])([\u4e00-\u9fff])", r"\1 \2", text)

    file.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(curr_dir, "../../"))
    for file in Path(root_dir).rglob("*.md"):
        format_heading(file)
        format_list(file)
        format_space(file)
        if file.name.lower() == "readme.md":
            continue
        insert_toc(file)