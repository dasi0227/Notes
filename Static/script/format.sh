#!/bin/zsh

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
ROOT_DIR=$(cd "$SCRIPT_DIR/../.." && pwd)
MODE="${1:-}"

if [[ "$MODE" != "-git" && "$MODE" != "-all" ]]; then
  echo "Usage: $0 -git | -all"
  exit 1
fi

typeset -a files

if [[ "$MODE" == "-all" ]]; then
  while IFS= read -r file; do
    files+=("$file")
  done < <(
    find "$ROOT_DIR" -type f \( -name '*.md' -o -name '*.markdown' \) \
      ! -path "$ROOT_DIR/Blog/*" \
      ! -name 'README.md' | sort
  )
else
  while IFS= read -r file; do
    [[ -n "$file" ]] || continue
    [[ "$file" == Blog/* ]] && continue
    [[ "$file" == README.md ]] && continue
    [[ "$file" != *.md && "$file" != *.markdown ]] && continue
    files+=("$ROOT_DIR/$file")
  done < <(
    git -C "$ROOT_DIR" log -1 --name-only --pretty=format: -- '*.md' '*.markdown' | sort -u
  )
fi

if [[ ${#files[@]} -eq 0 ]]; then
  echo "No markdown files to process."
  exit 0
fi

echo "Running format.py on ${#files[@]} files..."
python3 "$SCRIPT_DIR/format.py" "${files[@]}"

echo "Running toc.py on ${#files[@]} files..."
python3 "$SCRIPT_DIR/toc.py" "${files[@]}"
