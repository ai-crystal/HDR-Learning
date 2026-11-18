# -*- coding: utf-8 -*-
"""系列通用：把某册的分节 HTML 渲染、合并成 PDF（页眉、页码、书签、字体子集化）。

用法：
    python books/build/build_pdf.py --book books/beginner
"""
import os, sys, json, shutil, subprocess, argparse
from pathlib import Path
import fitz  # PyMuPDF
from styles import CSS_NORMAL, TEMPLATE

REPO = Path(__file__).resolve().parents[2]
ASSETS = REPO / "books" / "build"
OUT = REPO / "output"
SIMHEI = "C:/Windows/Fonts/simhei.ttf"
FONT = fitz.Font(fontfile=SIMHEI)

CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def chrome_path():
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    raise RuntimeError("找不到 Chrome / Edge，请设置环境变量 CHROME")


def render(html: Path, pdf: Path):
    pdf.parent.mkdir(parents=True, exist_ok=True)
    cmd = [chrome_path(), "--headless=new", "--disable-gpu", "--no-sandbox",
           "--allow-file-access-from-files", "--no-pdf-header-footer",
           "--virtual-time-budget=20000", f"--print-to-pdf={pdf}", html.as_uri()]
    subprocess.run(cmd, check=True, timeout=180,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not pdf.exists():
        raise RuntimeError("渲染失败: " + str(html))


def page_count(pdf: Path):
    d = fitz.open(pdf); n = d.page_count; d.close(); return n


def short_title(sec):
    t = sec["title"]
    import re
    m = re.match(r'^第\s*0?(\d+)\s*章', t)
    if m:
        return "第 %s 章" % m.group(1)
    m = re.match(r'^第([一二三四五六七八九十])篇', t)
    if m:
        return "第%s篇" % m.group(1)
    return t


def build_toc_html(manifest, book, cfg, tmp, numbers):
    rows = []
    for m in manifest:
        e = m.get("toc")
        if e not in ("part", "entry"):
            continue
        pg = numbers.get(m["id"], "")
        if e == "part":
            rows.append(f'<div class="toc-part"><span class="t">{m["title"]}</span>'
                        f'<span class="dots"></span><span class="p">{pg}</span></div>')
        else:
            rows.append(f'<div class="toc-item"><span class="t">{m["title"]}</span>'
                        f'<span class="dots"></span><span class="p">{pg}</span></div>')
    body = ('<style>.toc{font-family:"Microsoft YaHei",sans-serif;font-size:11pt;margin-top:6pt}'
            '.toc-part{display:flex;align-items:baseline;font-weight:700;color:#12233b;'
            'margin:13pt 0 4pt;border-bottom:.6pt solid #dce3ea;padding-bottom:3pt}'
            '.toc-item{display:flex;align-items:baseline;margin:3.5pt 0;padding-left:12pt;color:#243244}'
            '.toc .dots{flex:1;border-bottom:1px dotted #b7c0ca;margin:0 6pt 3pt}'
            '.toc .p{font-variant-numeric:tabular-nums;color:#555}</style>'
            '<h1>目录</h1><div class="toc">' + "\n".join(rows) + '</div>')
    tpl = (TEMPLATE
           .replace('file:///E:/Study/HDR技术/book/build/', ASSETS.as_uri() + '/')
           .replace('file:///E:/Study/HDR技术/book/', book.as_uri() + '/'))
    html = tpl.format(title="目录", css=CSS_NORMAL, kind="plain", pagecls="", body=body)
    p = tmp / "html" / "toc.html"
    p.write_text(html, encoding="utf-8")
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default="books/beginner")
    args = ap.parse_args()
    book = (REPO / args.book).resolve()
    name = book.name
    tmp = ASSETS / "tmp" / name
    manifest = json.loads((tmp / "manifest.json").read_text(encoding="utf-8"))
    cfg = json.loads((tmp / "book.json").read_text(encoding="utf-8"))

    pdf_dir = tmp / "pdf"
    counts = {}
    toc_sec = next(m for m in manifest if m["kind"] == "toc")

    for m in manifest:
        if m["kind"] == "toc":
            continue
        p = pdf_dir / (m["id"] + ".pdf")
        render(Path(m["html"]), p)
        counts[m["id"]] = page_count(p)

    # 先占位渲染目录，得到页数
    toc_html = build_toc_html(manifest, book, cfg, tmp, {})
    toc_pdf = pdf_dir / "toc.pdf"
    render(toc_html, toc_pdf)
    counts["toc"] = page_count(toc_pdf)

    def starts_from(cnt):
        st = {}; acc = 0
        for m in manifest:
            st[m["id"]] = acc; acc += cnt[m["id"]]
        return st, acc

    first_id = next(m["id"] for m in manifest if m["numbered"])
    for _ in range(5):
        st, _total = starts_from(counts)
        first = st[first_id]
        nums = {m["id"]: (st[m["id"]] - first + 1) for m in manifest if m["numbered"] and m.get("toc") in ("part", "entry")}
        toc_html = build_toc_html(manifest, book, cfg, tmp, nums)
        render(toc_html, toc_pdf)
        tc = page_count(toc_pdf)
        if tc == counts["toc"]:
            break
        counts["toc"] = tc

    st, total = starts_from(counts)
    first = st[first_id]

    # 合并
    out = fitz.open()
    for m in manifest:
        src = fitz.open(pdf_dir / (m["id"] + ".pdf"))
        out.insert_pdf(src); src.close()

    # 页眉 / 页码
    for i in range(out.page_count):
        sec = None
        for m in manifest:
            if st[m["id"]] <= i < st[m["id"]] + counts[m["id"]]:
                sec = m; break
        if not sec or not sec["numbered"]:
            continue
        page = out[i]
        w, h = page.rect.width, page.rect.height
        num = i - first + 1
        try:
            page.insert_text((56.7, h - 30), cfg.get("title", ""), fontsize=8,
                             fontname="simhei", fontfile=SIMHEI, color=(0.42, 0.45, 0.5))
            s = short_title(sec)
            tw = FONT.text_length(s, fontsize=8)
            page.insert_text((w - 56.7 - tw, h - 30), s, fontsize=8,
                             fontname="simhei", fontfile=SIMHEI, color=(0.42, 0.45, 0.5))
            ns = str(num)
            nw = FONT.text_length(ns, fontsize=9)
            page.insert_text(((w - nw) / 2, 28), ns, fontsize=9,
                             fontname="simhei", fontfile=SIMHEI, color=(0.13, 0.2, 0.31))
        except Exception as e:
            print("stamp warn:", e)

    # 书签
    toc = []
    for m in manifest:
        if m.get("toc") == "part":
            toc.append([1, m["title"], st[m["id"]] + 1 if m["numbered"] else 1])
        elif m.get("toc") == "entry":
            lvl = 2 if m["id"].startswith("ch") else 1
            pg = st[m["id"]] + 1 if m["numbered"] else 1
            toc.append([lvl, m["title"], pg])
    try:
        out.set_toc(toc)
    except Exception as e:
        print("toc warn:", e)
    try:
        out.subset_fonts()
    except Exception:
        pass

    OUT.mkdir(exist_ok=True)
    target = OUT / cfg["pdf"]
    out.save(str(target), garbage=4, deflate=True, clean=True)
    out.close()
    print("OK", target.name, "pages", total, "bookmarks", len(toc),
          "size", round(target.stat().st_size / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
