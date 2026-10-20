# -*- coding: utf-8 -*-
"""把 build/outline.json 里的章节大纲写入 PDF 书签（需要用 PyMuPDF）。

读取 build/last_output.txt 得到 build_pdf.mjs 实际写出的 PDF 路径，
因此无论输出到主文件还是 HDR超详解-new.pdf，都能正确加上书签。
"""
import json
import os
import pymupdf

BOOK = "E:/Study/HDR-Learning/书"
OUTDIR = "E:/Study/HDR-Learning/书籍输出"

last = BOOK + "/build/last_output.txt"
if os.path.exists(last):
    PDF = open(last, encoding="utf-8").read().strip()
else:
    PDF = OUTDIR + "/HDR超详解.pdf"

toc = json.load(open(BOOK + "/build/outline.json", encoding="utf-8"))

doc = pymupdf.open(PDF)
n = doc.page_count
clean = []
for lvl, title, page in toc:
    page = max(1, min(int(page), n))
    lvl = max(1, int(lvl))
    if clean and lvl > clean[-1][0] + 1:
        lvl = clean[-1][0] + 1
    clean.append([lvl, title, page])
doc.set_toc(clean)

tmp = PDF + ".tmp.pdf"
doc.save(tmp, garbage=3, deflate=True)
doc.close()

try:
    os.replace(tmp, PDF)
    print("bookmarks applied ->", PDF, "(", len(clean), "entries )")
except Exception as e:
    alt = PDF[:-4] + "-bookmarked.pdf"
    try:
        os.replace(tmp, alt)
        print("目标被占用，已输出为", alt, "->", e)
    except Exception:
        print("写入失败：目标文件被占用，请关闭后重试。")
