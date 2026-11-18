# -*- coding: utf-8 -*-
"""生成系列站点入口：根目录 docsify + 各册侧栏/首页（不复制任何 md）。"""
import json, os, re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SITE = "https://ai-crystal.github.io/HDR-Learning"
BOOKS = [
    dict(dir="beginner", name="入门篇", pdf="HDR-Basics.pdf", pages=214,
         desc="从像素到眼睛的完整指南：SDR 的来历、亮度与色域、标准、硬件、接口、系统与实战。"),
    dict(dir="color-science", name="色彩科学篇", pdf="HDR-ColorScience.pdf", pages=52,
         desc="从颜色测量到色貌与色域映射：CIE 体系、均匀色彩空间、CIECAM02/CAM16、色域映射与 HDR 编码。"),
    dict(dir="hdr-tech", name="HDR 技术篇", pdf="HDR-Technology.pdf", pages=50,
         desc="传递函数、元数据、映射与显示：Barten CSF、PQ/HLG 数学、ST 2094、BT.2390、面板与测量。"),
]


def read(p):
    return Path(p).read_text(encoding="utf-8")


def first_h1(p):
    for line in read(p).splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return Path(p).stem


def short(t):
    t = re.sub(r'^第\s*0?(\d+)\s*章\s*', r'第 \1 章 ', t)
    for sep in ("：", ":", "——", "（"):
        if sep in t:
            t = t.split(sep)[0]
    return t.strip()


def volume_info(b):
    d = REPO / "books" / b["dir"]
    cfg = json.loads(read(d / "book.json"))
    st = json.loads(read(d / "structure.json"))["sections"]
    chs = []
    for s in st:
        if s.get("toc") == "entry" and s["id"].startswith("ch"):
            t = first_h1(d / s["src"])
            chs.append((s["id"], t, f"books/{b['dir']}/{s['src']}"))
    return cfg, chs


def main():
    # 各册侧栏与首页
    for b in BOOKS:
        cfg, chs = volume_info(b)
        lines = [f"- [{cfg['volume'] or '本册'}首页](books/{b['dir']}/README.md)", ""]
        for cid, t, link in chs:
            lines.append(f"- [{short(t)}]({link})")
        lines += ["", f"- [下载 PDF]({SITE}/output/{b['pdf']})",
                  f"- [返回系列首页](README.md)"]
        (REPO / "books" / b["dir"] / "_sidebar.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

        toc = "\n".join(f"{i+1}. [{t}]({link})" for i, (cid, t, link) in enumerate(chs))
        (REPO / "books" / b["dir"] / "README.md").write_text(
            f"# {cfg['title']}\n\n> {cfg['subtitle']} · {cfg['volume']}\n\n{b['desc']}\n\n"
            f"- 作者：{cfg['author']}\n- 页数：约 {b['pages']} 页\n"
            f"- [**下载 PDF**]({SITE}/output/{b['pdf']})\n\n## 目录\n\n{toc}\n",
            encoding="utf-8")

    # 根侧栏
    s = ["- [系列首页](README.md)", ""]
    for b in BOOKS:
        s.append(f"- **{b['name']}**　[{b['dir']}](books/{b['dir']}/README.md)")
    s += ["", f"- [PDF 下载]({SITE}/output/HDR-Basics.pdf)"]
    (REPO / "_sidebar.md").write_text("\n".join(s) + "\n", encoding="utf-8")

    # 根首页
    rows = []
    for b in BOOKS:
        rows.append(f"| {b['name']} | {b['desc']} | {b['pages']} | "
                    f"[阅读](books/{b['dir']}/README.md) | [PDF]({SITE}/output/{b['pdf']}) |")
    (REPO / "README.md").write_text(
        "# HDR 技术系列\n\n> 从入门到专业的三册 · 作者：Dr. Dezeming\n\n"
        "同一主题按读者目标拆成三册：入门篇负责把概念讲通，色彩科学篇与 HDR 技术篇分别深入色彩与工程细节。\n\n"
        "- **在线阅读**：[" + SITE + "/](" + SITE + "/)\n\n"
        "## 分册\n\n| 分册 | 内容 | 页数 | 在线阅读 | PDF |\n|---|---|---|---|---|\n"
        + "\n".join(rows) + "\n\n"
        "## 阅读建议\n\n入门篇可按顺序通读；两本专业分册可以按需查阅，交叉处（PQ、色域、元数据）有相互引用。\n\n"
        "## 构建\n\n双击仓库根目录的 `build.cmd` 编译全部；`build.cmd beginner` 只编译入门篇。\n",
        encoding="utf-8")

    # 封面
    (REPO / "_coverpage.md").write_text(
        "# HDR 技术系列\n\n> 从像素到眼睛，再到色彩科学与工程实现\n\n"
        "- 入门篇 · 色彩科学篇 · HDR 技术篇\n- 三册共用一套术语与图示风格\n\n"
        f"[开始阅读](books/beginner/chapters/ch01.md)\n[下载入门篇]({SITE}/output/HDR-Basics.pdf)\n",
        encoding="utf-8")

    print("series site written")


if __name__ == "__main__":
    main()
