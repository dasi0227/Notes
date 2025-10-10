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
            if j < n and lines[j].lstrip().startswith("- ") and count != 0:
                print(f"{file}: 第 {i} 列表行和第 {j} 列表行有 {count} 个空行，已压缩为 0 行")
                i = j
                continue
        i += 1

    file.write_text("\n".join(new_lines), encoding="utf-8")

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

def format_bold(file: Path):
    text = file.read_text(encoding="utf-8")
    text = re.sub(r"\*{3,}(.*?)\*{3,}", r"**\1**", text)
    file.write_text(text, encoding="utf-8")

def format_table(file: Path):
    """
    规范化 Markdown 表格：
    - 第一行（表头）每列加粗
    - 每行的第一列加粗
    - 保证竖线 | 对齐，不多空格
    - 支持整篇文件多张表格
    """
    lines = file.read_text(encoding="utf-8").splitlines()
    new_lines = []
    n = len(lines)
    i = 0

    while i < n:
        line = lines[i]

        # 判断是否进入表格块
        if line.strip().startswith("|") and line.strip().endswith("|"):
            table_block = []
            # 收集整个表格
            while i < n and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_block.append(lines[i])
                i += 1

            # === 对整张表格进行格式化 ===
            for idx, row in enumerate(table_block):
                parts = [p.strip() for p in row.strip().split("|") if p.strip() != ""]

                # 第二行如果是分隔行 | ---- | ---- | 跳过处理
                if all(set(p) <= {"-", ":"} for p in parts):
                    new_lines.append("| " + " | ".join(parts) + " |")
                    continue

                if idx == 0:
                    # 第一行 → 每列都加粗
                    parts = [f"**{p}**" for p in parts]
                else:
                    # 其他行 → 仅第一列加粗
                    if parts:
                        parts[0] = f"**{parts[0]}**"

                new_line = "| " + " | ".join(parts) + " |"
                new_lines.append(new_line)

            # 继续外层循环（不要忘了 continue）
            continue
        else:
            # 非表格行
            new_lines.append(line)
            i += 1

    # 写回文件
    file.write_text("\n".join(new_lines), encoding="utf-8")



if __name__ == "__main__":
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(curr_dir, "../../"))
    # root_dir = "./"
    for file in Path(root_dir).rglob("*.md"):
        format_heading(file)
        format_list(file)
        format_space(file)
        format_table(file)
        format_bold(file)
        if file.name.lower() == "readme.md":
            continue
        insert_toc(file)