import os
import re

def find_md_heading_issues(root_dir):
    """
    查找指定目录下所有 Markdown 文件中 ### 后没有空格的标题行
    :param root_dir: 根目录路径
    """
    pattern = re.compile(r"^(#{1,6})([^#\s])")
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".md"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, start=1):
                        if pattern.search(line):
                            print(f"{file_path}:{line_num}: {line.strip()}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
    find_md_heading_issues(root_dir)