#!/usr/bin/env bash
# 在 git-bash 下编译书籍 PDF（含 PDF 书签）。
set -euo pipefail
cd "$(dirname "$0")"

PY="${PY:-D:/DevTools/Anaconda3/python.exe}"
NODE="${NODE:-/c/Program Files/nodejs/node.exe}"

echo "[1/3] Markdown -> HTML ..."
"$PY" build_html.py
echo "[2/3] HTML -> PDF ..."
"$NODE" build_pdf.mjs
echo "[3/3] Writing PDF bookmarks ..."
"$PY" apply_outline.py
echo "Done. -> E:/Study/HDR-Learning/书籍输出/HDR超详解.pdf"
