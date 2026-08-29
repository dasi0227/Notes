#!/usr/bin/env python3
"""
批量重命名 attachments/image/ 下的图片：
- YYYYMMDDNNNNNNN_hash6.ext  -> YYYYMMDD_NNNNNNN.ext
- SpringMVC 前缀              -> 剥掉前缀后按上一条规则
- YYYYMMDDHHMMSS.ext (14 位)  -> YYYYMMDD_HHMMSS.ext
- solution-<32hex>_<hash6>    -> seata-solution.ext（唯一，硬编码）
- 中文名                       -> 不动
同步改写所有 md 引用（URL-encoded 和明文两种都处理）。
Dry-run 默认，加 --apply 才执行。
"""
from __future__ import annotations
import argparse, os, re, sys, urllib.parse
from pathlib import Path

ROOT = Path("/Users/bytedance/Desktop/Notes")

IMG_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
MD_DIRS_SKIP = {".git", "Blog", "Draft", "node_modules"}

RE_MAIN     = re.compile(r"^(\d{8})(\d{7})_[0-9a-f]{6}$")             # 20250916 2330784 _ abf2f8
RE_SPRING   = re.compile(r"^SpringMVC(\d{8})(\d{7})_[0-9a-f]{6}$")    # SpringMVC + 同上
RE_SHORT_TS = re.compile(r"^(\d{8})(\d{6})$")                         # 20260827 200450
NAME_SOLUTION_OLD = "solution-1bdadb80e54074aa3088372c17f0244b_614430"
NAME_SOLUTION_NEW = "seata-solution"

def new_stem(stem: str) -> str | None:
    """返回新 stem，None 表示不改名。"""
    if stem == NAME_SOLUTION_OLD:
        return NAME_SOLUTION_NEW
    m = RE_MAIN.match(stem)
    if m:
        return f"{m.group(1)}_{m.group(2)}"
    m = RE_SPRING.match(stem)
    if m:
        return f"{m.group(1)}_{m.group(2)}"
    m = RE_SHORT_TS.match(stem)
    if m:
        return f"{m.group(1)}_{m.group(2)}"
    return None

def collect_renames() -> list[tuple[Path, Path]]:
    plans = []
    for img_dir in ROOT.rglob("attachments/image"):
        if not img_dir.is_dir():
            continue
        for f in sorted(img_dir.iterdir()):
            if not f.is_file() or f.suffix.lower() not in IMG_EXTS:
                continue
            new = new_stem(f.stem)
            if new is None:
                continue
            target = f.with_name(new + f.suffix)
            if target.exists():
                print(f"! 冲突，跳过: {f} -> {target}", file=sys.stderr)
                continue
            plans.append((f, target))
    return plans

def iter_md_files():
    for p in ROOT.rglob("*.md"):
        if any(part in MD_DIRS_SKIP for part in p.parts):
            continue
        yield p

def rewrite_md(plans: list[tuple[Path, Path]], apply: bool) -> int:
    """把 md 里对 old_basename 的引用改成 new_basename。"""
    changed = 0
    subs = {}
    for old, new in plans:
        subs[old.name] = new.name
        subs[urllib.parse.quote(old.name)] = urllib.parse.quote(new.name)
    if not subs:
        return 0
    for md in iter_md_files():
        text = md.read_text(encoding="utf-8")
        new_text = text
        for old_name, new_name in subs.items():
            if old_name in new_text:
                new_text = new_text.replace(old_name, new_name)
        if new_text != text:
            changed += 1
            if apply:
                md.write_text(new_text, encoding="utf-8")
            else:
                print(f"  would rewrite: {md.relative_to(ROOT)}")
    return changed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    plans = collect_renames()
    print(f"计划重命名 {len(plans)} 张图片：\n")
    for old, new in plans:
        print(f"  {old.parent.relative_to(ROOT)}/{old.name}  ->  {new.name}")

    if not args.apply:
        print(f"\n[dry-run] 未执行。加 --apply 生效。")
        # 也预估 md 改写数
        n = rewrite_md(plans, apply=False)
        print(f"[dry-run] 将改写 md 数：{n}")
        return

    # apply: 先改 md（此时旧图仍存在，Obsidian 短时间会看到断链，接下来立即改文件名）
    n = rewrite_md(plans, apply=True)
    print(f"\n已改写 md：{n}")
    for old, new in plans:
        os.rename(old, new)
    print(f"已重命名图片：{len(plans)}")

if __name__ == "__main__":
    main()
