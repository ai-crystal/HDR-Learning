# -*- coding: utf-8 -*-
"""生成系列站点入口（根 docsify + 各册侧栏/首页），不复制任何 md。"""
import json, re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SITE = "https://ai-crystal.github.io/HDR-Learning"
GITHUB = "https://github.com/ai-crystal/HDR-Learning"
BOOKS = [
    dict(dir="beginner", name="入门篇", num="01", pdf="v1-beginner.pdf", pages=214,
         desc="从像素到眼睛的完整指南：SDR 的来历、亮度与色域、标准、硬件、接口、系统与实战。"),
    dict(dir="color-science", name="色彩科学篇", num="02", pdf="v2-color-science.pdf", pages=52,
         desc="从颜色测量到色貌与色域映射：CIE 体系、均匀色彩空间、CIECAM02/CAM16、色域映射与 HDR 编码。"),
    dict(dir="hdr-tech", name="HDR 技术篇", num="03", pdf="v3-hdr-tech.pdf", pages=50,
         desc="传递函数、元数据、映射与显示：Barten CSF、PQ/HLG 数学、ST 2094、BT.2390、面板与测量。"),
]
IMG_A = '<a href="{href}" target="_blank" rel="noopener" data-router-ignore>{text}</a>'


def read(p):
    return Path(p).read_text(encoding="utf-8")


def first_h1(p):
    for line in read(p).splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return Path(p).stem


def chapter_title(t):
    m = re.match(r'^第\s*0?(\d+)\s*章\s*(.*)$', t)
    if m:
        return f"第 {m.group(1)} 章　{m.group(2).strip()}"
    return t


def volume_data(b):
    d = REPO / "books" / b["dir"]
    cfg = json.loads(read(d / "book.json"))
    secs = json.loads(read(d / "structure.json"))["sections"]
    chs, apps, has_preface = [], [], False
    for s in secs:
        if s["id"] == "preface":
            has_preface = True
        if s["id"].startswith("ch"):
            chs.append((chapter_title(first_h1(d / s["src"])), s["src"]))
        if s["id"].startswith("appendix"):
            apps.append((first_h1(d / s["src"]), s["src"]))
    return cfg, chs, apps, has_preface


def main():
    for b in BOOKS:
        cfg, chs, apps, has_preface = volume_data(b)
        d = REPO / "books" / b["dir"]
        pdf_href = f"output/{b['pdf']}"

        # 本册侧栏
        lines = ["- [系列首页](/README.md)", f"- [本册首页](/books/{b['dir']}/README.md)", ""]
        if has_preface:
            lines += [f"- [前言](/books/{b['dir']}/front/preface.md)", ""]
        for t, src in chs:
            lines.append(f"- [{t}](/books/{b['dir']}/{src})")
        if apps:
            lines += ["", "- **附录**"]
            for t, src in apps:
                lines.append(f"  - [{t}](/books/{b['dir']}/{src})")
        lines += ["", IMG_A.format(href=pdf_href, text="下载 PDF")]
        (d / "_sidebar.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

        # 本册首页
        quote = f"{cfg['title']}：{cfg['subtitle']}" if b["dir"] == "beginner" else cfg["subtitle"]
        toc = []
        if has_preface:
            toc.append("- [前言](front/preface.md)")
        toc += [f"- [{t}]({src})" for t, src in chs]
        if apps:
            toc += ["", "### 附录", ""] + [f"- [{t}]({src})" for t, src in apps]
        (d / "README.md").write_text(
            f"# {cfg['volume']}\n\n> {quote}\n\n{b['desc']}\n\n"
            f"共 {len(chs)} 章 · {b['pages']} 页\n\n"
            f"[从第 1 章开始](chapters/ch01.md)　·　"
            + IMG_A.format(href=f"../../{pdf_href}", text="下载本册 PDF")
            + "\n\n## 目录\n\n" + "\n".join(toc) + "\n\n---\n\n[返回系列首页](../../README.md)\n",
            encoding="utf-8")

    # 根侧栏
    s = ["- [系列首页](/README.md)", ""]
    for b in BOOKS:
        s += [f"- **{b['num']}　{b['name']}**",
              f"  - [本册首页](/books/{b['dir']}/README.md)",
              "  - " + IMG_A.format(href=f"output/{b['pdf']}", text="下载 PDF"), ""]
    (REPO / "_sidebar.md").write_text("\n".join(s).rstrip() + "\n", encoding="utf-8")

    # 根首页
    rows = []
    for b in BOOKS:
        rows.append(f"| {b['num']} | [{b['name']}](books/{b['dir']}/README.md) | {b['desc'].split('：')[0]} | "
                    f"{b['pages']} | [阅读](books/{b['dir']}/README.md) | "
                    + IMG_A.format(href=f"output/{b['pdf']}", text="下载") + " |")
    (REPO / "README.md").write_text(
        "# HDR 技术系列\n\n> 从像素到眼睛，再到色彩科学与工程实现\n\n"
        "同一主题按读者目标拆成三册。入门篇把 SDR 的来历、亮度与色域、标准、硬件、接口、系统与实战一次讲通；"
        "色彩科学篇与 HDR 技术篇分别深入颜色测量、色貌模型、传递函数、元数据与显示实现。\n\n"
        "三册共用一套术语与图示风格。入门篇可以顺序通读，两本专业册适合按需查阅。\n\n"
        "作者：Dr. Dezeming　·　2026\n\n"
        f"**在线阅读**：[在线阅读站]({SITE}/)　·　**仓库**：[GitHub 仓库]({GITHUB})\n\n"
        "## 分册\n\n| 册 | 书名 | 一句话 | 页数 | 在线阅读 | PDF |\n| --- | --- | --- | ---: | --- | --- |\n"
        + "\n".join(rows) + "\n\n"
        "## 怎么读\n\n"
        "- 刚接触 HDR：从入门篇第 1 章开始，把 SDR、亮度、色域与标准串起来。\n"
        "- 要做色彩管理：读色彩科学篇，重点是 CIE 体系、均匀色彩空间与色域映射。\n"
        "- 要做显示或编码：读 HDR 技术篇，重点是 PQ / HLG、ST 2094、BT.2390 与面板测量。\n\n"
        "## 许可\n\n"
        "本系列文字与插图采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可发布，"
        "转载请注明作者与出处。书中引用的论文、数据集与模型归各自作者所有。\n\n---\n\n"
        "作者：Dr. Dezeming　·　2026\n",
        encoding="utf-8")

    # 封面
    (REPO / "_coverpage.md").write_text(
        "# HDR 技术系列\n\n> 从像素到眼睛，再到色彩科学与工程实现\n\n"
        "同一主题按读者目标拆成三册。入门篇把 SDR 的来历、亮度与色域、标准、硬件、接口、系统与实战一次讲通；"
        "色彩科学篇与 HDR 技术篇分别深入颜色测量、色貌模型、传递函数、元数据与显示实现。\n\n"
        "**Dr. Dezeming**　·　2026\n\n"
        '<p class="cover-links">\n'
        '<a href="#/books/beginner/README">开始阅读</a>\n'
        '<a href="#/README">书目与下载</a>\n'
        "</p>\n",
        encoding="utf-8")

    print("series site written")


if __name__ == "__main__":
    main()
