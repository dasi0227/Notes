import os

replace_dict = {
    "cover_computernetwork.webp": "network.png",
    "cover_computergraphic.webp": "graphic.png",
    "cover_distributedsystem.webp": "distributed.png",
    "cover_analysis.webp": "analysis.png",
    "cover_compile.webp": "compile.png",
    "cover_parallel.webp": "parallel.png",
    "cover_database.webp": "database.png",
    "cover_AI.webp": "ai.png",
    "cover_machinelearning.webp": "ml.png",
    "cover_algorithm.webp": "algorithm.png",
    "cover_frontend.webp": "frontend.png",
    "cover_hexo.webp": "hexo.png"
}

def replace_in_file(file_path, replace_map):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for old, new in replace_map.items():
            content = content.replace(old, new)

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已修改文件: {file_path}")
    except Exception as e:
        print(f"跳过文件: {file_path}, 原因: {e}")

def traverse_and_replace(root_dir, replace_map):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            replace_in_file(file_path, replace_map)

if __name__ == "__main__":
    target_directory = "/Users/wyw/Desktop/Blog/source/_posts"
    traverse_and_replace(target_directory, replace_dict)