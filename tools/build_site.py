# -*- coding: utf-8 -*-
"""生成 docsify 在线阅读站点（#/ 路由），直接引用 book/ 下唯一的 Markdown 原稿。

输出到仓库根目录：
  index.html      docsify 外壳
  _sidebar.md     侧栏
  _coverpage.md   封面
  README.md       首页（同时作为 GitHub 仓库首页）
  .nojekyll
不复制 md / 图片；PDF 直接链接 output/HDR超详解.pdf。
"""
import os, re

BASE = "E:/Study/HDR技术"
BOOK = BASE + "/book"

SECTIONS = [
    dict(id="preface", title="前言", src="front/preface.md", kind="entry"),
    dict(id="part1", title="第一篇　基础篇：为什么会有 HDR", src="front/part1.md", kind="part"),
    dict(id="ch01", src="chapters/ch01.md"),
    dict(id="ch02", src="chapters/ch02.md"),
    dict(id="ch03", src="chapters/ch03.md"),
    dict(id="part2", title="第二篇　色彩科学篇：颜色的物理与数学", src="front/part2.md", kind="part"),
    dict(id="ch04", src="chapters/ch04.md"),
    dict(id="ch05", src="chapters/ch05.md"),
    dict(id="ch06", src="chapters/ch06.md"),
    dict(id="ch07", src="chapters/ch07.md"),
    dict(id="part3", title="第三篇　标准篇：HDR 世界的规则", src="front/part3.md", kind="part"),
    dict(id="ch08", src="chapters/ch08.md"),
    dict(id="ch09", src="chapters/ch09.md"),
    dict(id="ch10", src="chapters/ch10.md"),
    dict(id="part4", title="第四篇　硬件篇：光从哪里来", src="front/part4.md", kind="part"),
    dict(id="ch11", src="chapters/ch11.md"),
    dict(id="ch12", src="chapters/ch12.md"),
    dict(id="ch13", src="chapters/ch13.md"),
    dict(id="part5", title="第五篇　传输与系统篇：把 HDR 送到眼前", src="front/part5.md", kind="part"),
    dict(id="ch14", src="chapters/ch14.md"),
    dict(id="ch15", src="chapters/ch15.md"),
    dict(id="ch16", src="chapters/ch16.md"),
    dict(id="part6", title="第六篇　软件与实战篇：从会用到精通", src="front/part6.md", kind="part"),
    dict(id="ch17", src="chapters/ch17.md"),
    dict(id="ch18", src="chapters/ch18.md"),
    dict(id="ch19", src="chapters/ch19.md"),
    dict(id="ch20", src="chapters/ch20.md"),
    dict(id="appendix-a", title="附录 A　术语速查表", src="appendix/appendix-a.md", kind="entry"),
    dict(id="appendix-b", title="附录 B　参考文献", src="appendix/appendix-b.md", kind="entry"),
    dict(id="afterword", title="后记", src="front/afterword.md", kind="entry"),
]

PDF = "../output/HDR超详解.pdf"   # 从 book/ 视角；站点里写 output/HDR超详解.pdf


def first_h1(path):
    for line in open(path, encoding="utf-8"):
        if line.startswith("# "):
            return line[2:].strip()
    return os.path.splitext(os.path.basename(path))[0]


def short_title(t):
    t = re.sub(r'^第\s*0?(\d+)\s*章\s*', r'第 \1 章 ', t)
    for sep in ("：", ":", "——", "（"):
        if sep in t:
            t = t.split(sep)[0]
    return t.strip()


INDEX = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>HDR 超详解 · 从像素到眼睛的完整指南</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<style>
  :root{ --navy:#12233b; --accent:#1f4e79; }
  body{ font-family:"Noto Serif SC","Source Han Serif SC","Songti SC","SimSun",Georgia,serif; }
  .sidebar{ font-family:"Noto Sans SC","Microsoft YaHei",sans-serif; }
  .markdown-section{ max-width:820px; font-size:16.5px; line-height:1.85; color:#1c2430; }
  .markdown-section h1,.markdown-section h2,.markdown-section h3,.markdown-section h4{
    font-family:"Noto Sans SC","Microsoft YaHei",sans-serif; color:var(--navy); }
  .markdown-section h1{ font-size:28px; border-bottom:2px solid var(--navy); padding-bottom:10px; }
  .markdown-section h2{ font-size:21px; margin-top:34px; }
  .markdown-section h3{ font-size:17.5px; color:var(--accent); }
  .markdown-section blockquote{ border-left:3px solid var(--accent); background:#f5f8fb; color:#3d4b5a; }
  .markdown-section table th{ background:#eef3f8; }
  .markdown-section img{ border-radius:6px; }
  .markdown-section pre{ border-radius:8px; }
  .app-nav{ font-family:"Noto Sans SC","Microsoft YaHei",sans-serif; }

  .cover{ background: linear-gradient(180deg, rgba(5,7,13,.82) 0%, rgba(5,7,13,.35) 34%, rgba(5,7,13,.72) 62%, rgba(5,7,13,.97) 90%), url("book/images/logo/cover_bg.jpg") center 42%/cover no-repeat !important; }
  .cover:before{ background: transparent !important; }
  .cover .cover-main{ color:#fff; max-width:900px; background:rgba(5,7,13,.34); border-radius:18px; padding:34px 42px; box-shadow:0 10px 40px rgba(0,0,0,.35); }
  .cover .cover-main h1, .cover .cover-main h1 a, .cover .cover-main h1 span{ color:#fff !important; }
  .cover .cover-main h1{ font-family:"Georgia","Noto Serif SC",serif; font-size:clamp(46px,8vw,84px); letter-spacing:4px; color:#fff; margin:0; text-shadow:0 3px 24px rgba(0,0,0,.55); }
  .cover .cover-main p{ color:#e8eef6; font-family:"Noto Sans SC","Microsoft YaHei",sans-serif; }
  .cover .cover-main blockquote{ color:#cfd9e6; border:none; background:none; margin:18px 0 26px; }
  .cover .cover-main > p:last-child a{ background:transparent; color:#fff; border:1px solid rgba(255,255,255,.6); border-radius:999px; padding:10px 22px; margin:6px; }
  .cover .cover-main > p:last-child a:first-child{ background:#fff; color:var(--navy); border-color:#fff; font-weight:700; }
  .cover .cover-main > p:last-child a:hover{ opacity:.9; }
  .cover .mask{ background:transparent; }
</style>
</head>
<body>
<div id="app">加载中…</div>
<script>
  window.$docsify = {
    name: 'HDR 超详解',
    loadSidebar: true,
    subMaxLevel: 2,
    coverpage: true,
    homepage: 'README.md',
    auto2top: true,
    maxLevel: 2,
    search: { maxAge: 86400000, paths: 'auto', placeholder: '搜索…', noData: '没有找到结果' },
    copyCode: { buttonText: '复制', errorText: '复制失败' },
    pagination: { previousText: '上一章', nextText: '下一章' },
    plugins: [
      function (hook) {
        hook.beforeEach(function (md) {
          var state = { open: true };
          var parts = md.split(/(```[\s\S]*?```)/g);
          return parts.map(function (seg, i) {
            if (i % 2 === 1) return seg;
            return seg.replace(/`[^`]*`|"/g, function (m) {
              if (m !== '"') return m;
              if (state.open) { state.open = false; return '“'; }
              state.open = true; return '”';
            });
          }).join('');
        });
      }
    ]
  };
</script>
<script src="https://cdn.jsdelivr.net/npm/docsify@4"></script>
<script src="https://cdn.jsdelivr.net/npm/docsify@4/lib/plugins/search.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/docsify@4/lib/plugins/pagination.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/docsify@4/lib/plugins/copy-code.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/docsify-katex@1/dist/docsify-katex.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/docsify-mermaid@2/dist/docsify-mermaid.js"></script>
</body>
</html>
"""


def main():
    for s in SECTIONS:
        if not s.get("title"):
            s["title"] = first_h1(os.path.join(BOOK, s["src"]))

    # 侧栏
    lines = ["- [前言](book/front/preface.md)", ""]
    for s in SECTIONS:
        if s["id"] == "preface":
            continue
        link = "book/" + s["src"]
        if s.get("kind") == "part":
            lines.append(f"- **{s['title']}**")
        elif s["id"].startswith("ch"):
            lines.append(f"  - [{short_title(s['title'])}]({link})")
        else:
            lines.append(f"- [{s['title']}]({link})")
    open(BASE + "/_sidebar.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")

    # 封面
    open(BASE + "/_coverpage.md", "w", encoding="utf-8").write(
        "# HDR 超详解\n\n"
        "> 从像素到眼睛的完整指南\n\n"
        "- 6 篇 20 章 · 90 余张原创示意图\n"
        "- 从光与颜色，到面板、接口、系统与调色\n\n"
        "[开始阅读](book/chapters/ch01.md)\n"
        "[下载 PDF](output/HDR超详解.pdf)\n")

    # 首页
    toc = []
    for s in SECTIONS:
        link = "book/" + s["src"]
        if s.get("kind") == "part":
            toc.append(f"- **{s['title']}**")
        elif s["id"].startswith("ch"):
            toc.append(f"  - [{s['title']}]({link})")
        else:
            toc.append(f"- [{s['title']}]({link})")
    open(BASE + "/README.md", "w", encoding="utf-8").write(
        "# HDR 超详解\n\n"
        "> 从像素到眼睛的完整指南 · 作者：Dezeming\n\n"
        "本书用最直白的方式讲清**高动态范围（HDR）**：从光与颜色的基础，到色域与传递函数，"
        "到 HDR10、杜比视界、HDR10+ 与 HLG 的规则，再到面板、接口、操作系统、播放软件与调色，"
        "最后落到选购、校准与排查。\n\n"
        "- **6 篇 20 章**，配 90 余张原创示意图\n"
        "- **在线阅读**：[https://ai-crystal.github.io/HDR-Learning/](https://ai-crystal.github.io/HDR-Learning/)\n"
        "- 左侧目录逐章阅读，或 [**下载整本 PDF**](output/HDR超详解.pdf)\n\n"
        "## 目录\n\n" + "\n".join(toc) + "\n")

    open(BASE + "/index.html", "w", encoding="utf-8").write(INDEX)
    open(BASE + "/.nojekyll", "w", encoding="utf-8").write("")
    print("site files written at repo root")


if __name__ == "__main__":
    main()
