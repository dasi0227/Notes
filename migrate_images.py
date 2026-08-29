#!/usr/bin/env python3
"""
把笔记里的远程图片下载到本地 attachments/image/ 并回写相对路径。

用法:
  python3 migrate_images.py --dry-run    # 只打印计划，不下载不改文件
  python3 migrate_images.py              # 实际执行
"""
import argparse
import hashlib
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET_DIRS = ["Agent", "Algorithm", "Backend", "Project"]
IMG_EXTS = {"png", "jpg", "jpeg", "gif", "webp", "svg", "bmp", "ico"}

MD_IMG = re.compile(r'!\[[^\]]*\]\((https?://[^)\s]+)\)')
HTML_IMG = re.compile(r'<img[^>]+src=[\'"](https?://[^\'"]+)[\'"]', re.I)
OBS_EMBED = re.compile(r'!\[\[(https?://[^\]]+)\]\]')
FENCE = re.compile(r'^```')


def strip_code_fences(text: str) -> str:
    """把 ``` 围栏内的内容替换成同长度空白，避免匹配到代码块里的示例 URL。"""
    lines = text.split('\n')
    in_fence = False
    out = []
    for ln in lines:
        if FENCE.match(ln.strip()):
            in_fence = not in_fence
            out.append(ln)
        elif in_fence:
            out.append(' ' * len(ln))
        else:
            out.append(ln)
    return '\n'.join(out)


def extract_urls(text: str):
    scrubbed = strip_code_fences(text)
    urls = set()
    for pat in (MD_IMG, HTML_IMG, OBS_EMBED):
        for m in pat.finditer(scrubbed):
            urls.add(m.group(1))
    return {u for u in urls if is_image_url(u)}


def is_image_url(url: str) -> bool:
    path = urllib.parse.urlparse(url).path.lower()
    ext = path.rsplit('.', 1)[-1] if '.' in path else ''
    return ext in IMG_EXTS


def target_filename(url: str, dest_dir: Path) -> Path:
    """URL → 本地文件名。同名不同源加短哈希后缀。幂等。"""
    parsed = urllib.parse.urlparse(url)
    raw_name = os.path.basename(parsed.path) or "image"
    stem, dot, ext = raw_name.rpartition('.')
    if not dot:
        stem, ext = raw_name, 'png'
    stem = re.sub(r'[^\w\-.]', '_', stem)
    short = hashlib.sha1(url.encode()).hexdigest()[:6]
    return dest_dir / f"{stem}_{short}.{ext.lower()}"


def collect_plan():
    """返回 [(md_path, url, target_path), ...] 和按 md 的分组。"""
    plan = []
    per_md = {}
    for top in TARGET_DIRS:
        top_dir = ROOT / top
        if not top_dir.exists():
            continue
        for md in top_dir.rglob("*.md"):
            text = md.read_text(encoding='utf-8', errors='ignore')
            urls = extract_urls(text)
            if not urls:
                continue
            dest_dir = md.parent / "attachments" / "image"
            for url in sorted(urls):
                tgt = target_filename(url, dest_dir)
                plan.append((md, url, tgt))
                per_md.setdefault(md, []).append((url, tgt))
    return plan, per_md


def print_dry_run(plan, per_md):
    print(f"\n{'='*70}")
    print(f"DRY-RUN: 不下载、不改文件，仅展示计划")
    print(f"{'='*70}\n")

    total_urls = len(plan)
    unique_urls = len({u for _, u, _ in plan})
    hosts = {}
    for _, u, _ in plan:
        h = urllib.parse.urlparse(u).netloc
        hosts[h] = hosts.get(h, 0) + 1

    print(f"涉及 md 文件数: {len(per_md)}")
    print(f"引用总数     : {total_urls}")
    print(f"去重后 URL 数: {unique_urls}")
    print(f"\n按域名分布:")
    for h, c in sorted(hosts.items(), key=lambda x: -x[1]):
        print(f"  {c:>4}  {h}")

    print(f"\n{'-'*70}")
    print("按 md 分组的迁移清单:")
    print(f"{'-'*70}")
    for md in sorted(per_md.keys()):
        rel_md = md.relative_to(ROOT)
        items = per_md[md]
        print(f"\n[{rel_md}]  ({len(items)} 张)")
        for url, tgt in items:
            rel_tgt = tgt.relative_to(md.parent)
            print(f"  {url}")
            print(f"    → ./{rel_tgt}")

    print(f"\n{'='*70}")
    print("dry-run 完成。确认无误后去掉 --dry-run 参数即可实际执行。")
    print(f"{'='*70}\n")


def download_one(url: str, tgt: Path, retries: int = 3, timeout: int = 15):
    if tgt.exists() and tgt.stat().st_size > 0:
        return True, "skip-exists"
    tgt.parent.mkdir(parents=True, exist_ok=True)
    tmp = tgt.with_suffix(tgt.suffix + ".tmp")
    headers = {
        "User-Agent": "Mozilla/5.0 (image-migration)",
        "Referer": f"{urllib.parse.urlparse(url).scheme}://{urllib.parse.urlparse(url).netloc}/",
    }
    last_err = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
            if not data:
                raise ValueError("empty body")
            tmp.write_bytes(data)
            tmp.rename(tgt)
            return True, f"ok ({len(data)} bytes)"
        except Exception as e:
            last_err = str(e)
            time.sleep(1.5 ** i)
    if tmp.exists():
        tmp.unlink(missing_ok=True)
    return False, last_err or "unknown"


def rewrite_md(md: Path, results: dict):
    """results: {url: target_path or None(失败)}. 只替换成功项。"""
    text = md.read_text(encoding='utf-8')
    changed = False
    for url, tgt in results.items():
        if tgt is None:
            continue
        rel = os.path.relpath(tgt, md.parent).replace(os.sep, '/')
        rel = f"./{rel}" if not rel.startswith('.') else rel
        if url in text:
            text = text.replace(url, rel)
            changed = True
    if changed:
        md.write_text(text, encoding='utf-8')
    return changed


def execute(plan, per_md, workers: int = 12):
    print(f"\n开始下载 {len(plan)} 张图片（并发 {workers}）...\n")
    url_to_tgt = {}
    for _, u, t in plan:
        url_to_tgt[u] = t
    results = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(download_one, u, t): (u, t) for u, t in url_to_tgt.items()}
        for i, fut in enumerate(as_completed(futs), 1):
            u, t = futs[fut]
            ok, msg = fut.result()
            results[u] = t if ok else None
            tag = "OK  " if ok else "FAIL"
            print(f"[{i:>3}/{len(futs)}] {tag}  {u}  ({msg})")

    print(f"\n开始回写 md ...\n")
    changed_files = 0
    for md, items in per_md.items():
        md_results = {u: results.get(u) for u, _ in items}
        if rewrite_md(md, md_results):
            changed_files += 1
            print(f"  updated: {md.relative_to(ROOT)}")

    ok_count = sum(1 for v in results.values() if v is not None)
    fail_count = len(results) - ok_count
    print(f"\n{'='*70}")
    print(f"完成: 下载成功 {ok_count} / 失败 {fail_count} / 修改 md {changed_files} 篇")
    if fail_count:
        print(f"\n失败清单:")
        for u, v in results.items():
            if v is None:
                print(f"  {u}")
    print(f"{'='*70}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()

    plan, per_md = collect_plan()
    if not plan:
        print("没有找到需要迁移的远程图片。")
        return
    if args.dry_run:
        print_dry_run(plan, per_md)
    else:
        execute(plan, per_md, workers=args.workers)


if __name__ == "__main__":
    main()
