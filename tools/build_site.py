# -*- coding: utf-8 -*-
"""生成 docsify 可在线阅读站点（#/ 路由），输出到 docs/。

docs/
  index.html        docsify 外壳
  _coverpage.md     封面
  _sidebar.md       侧栏目录
  README.md         首页
  ch01.md …        各章（从 书/ 复制，图片路径改为 图片/）
  图片/…            插图
  HDR超详解.pdf      整书下载
  .nojekyll
"""
import os, re, glob, shutil
from PIL import Image

BASE = "E:/Study/HDR技术"
SRC = BASE + "/书"
OUT = BASE + "/docs"
IMG_SRC = SRC + "/图片"
IMG_OUT = OUT + "/图片"
PDF_SRC = BASE + "/书籍输出/HDR超详解.pdf"

SECTIONS = [
    dict(id="preface", title="前言", src="03-前言.md", kind="entry"),
    dict(id="part1", title="第一篇　基础篇：为什么会有 HDR", src="篇一-篇首.md", kind="part"),
    dict(id="ch01", src="正文/第01章-从SDR说起.md"),
    dict(id="ch02", src="正文/第02章-亮度对比度与动态范围.md"),
    dict(id="ch03", src="正文/第03章-人眼如何看光.md"),
    dict(id="part2", title="第二篇　色彩科学篇：颜色的物理与数学", src="篇二-篇首.md", kind="part"),
    dict(id="ch04", src="正文/第04章-颜色的坐标系.md"),
    dict(id="ch05", src="正文/第05章-色域漫游.md"),
    dict(id="ch06", src="正文/第06章-传递函数与Gamma.md"),
    dict(id="ch07", src="正文/第07章-PQ与HLG.md"),
    dict(id="part3", title="第三篇　标准篇：HDR 世界的规则", src="篇三-篇首.md", kind="part"),
    dict(id="ch08", src="正文/第08章-HDR10基石.md"),
    dict(id="ch09", src="正文/第09章-DolbyVision与HDR10加.md"),
    dict(id="ch10", src="正文/第10章-位深编码与色度采样.md"),
    dict(id="part4", title="第四篇　硬件篇：光从哪里来", src="篇四-篇首.md", kind="part"),
    dict(id="ch11", src="正文/第11章-面板与背光.md"),
    dict(id="ch12", src="正文/第12章-自发光时代.md"),
    dict(id="ch13", src="正文/第13章-认证与DisplayHDR.md"),
    dict(id="part5", title="第五篇　传输与系统篇：把 HDR 送到眼前", src="篇五-篇首.md", kind="part"),
    dict(id="ch14", src="正文/第14章-接口与带宽.md"),
    dict(id="ch15", src="正文/第15章-链路握手.md"),
    dict(id="ch16", src="正文/第16章-操作系统里的HDR.md"),
    dict(id="part6", title="第六篇　软件与实战篇：从会用到精通", src="篇六-篇首.md", kind="part"),
    dict(id="ch17", src="正文/第17章-ToneMapping.md"),
    dict(id="ch18", src="正文/第18章-内容世界.md"),
    dict(id="ch19", src="正文/第19章-选购校准与色彩管理.md"),
    dict(id="ch20", src="正文/第20章-常见误区与精通路线.md"),
    dict(id="appendix-a", title="附录 A　术语速查表", src="附录/附录A-术语速查.md", kind="entry"),
    dict(id="appendix-b", title="附录 B　参考文献", src="附录/附录B-参考文献.md", kind="entry"),
    dict(id="afterword", title="后记", src="后记.md", kind="entry"),
]


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


def build_image(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        im = Image.open(src)
    except Exception:
        shutil.copy2(src, dst); return
    w, h = im.size
    if w > 1400:
        im = im.resize((1400, int(h * 1400 / w)), Image.LANCZOS)
    if dst.lower().endswith(('.jpg', '.jpeg')):
        im.convert("RGB").save(dst, quality=88, optimize=True)
    else:
        im.save(dst, optimize=True)


def copy_images():
    if os.path.isdir(IMG_OUT):
        shutil.rmtree(IMG_OUT)
    n = 0
    for root, _, files in os.walk(IMG_SRC):
        for f in files:
            if not f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg')):
                continue
            if f.lower().startswith(('logo1', 'logo2', 'logo3')):
                continue
            src = os.path.join(root, f)
            dst = os.path.join(IMG_OUT, os.path.relpath(src, IMG_SRC))
            build_image(src, dst); n += 1
    print("images:", n)


INDEX_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>HDR 超详解 · 从像素到眼睛的完整指南</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/docsify@4/lib/themes/vue.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<style>
  :root{ --navy:#12233b; --gold:#c8a24a; --accent:#1f4e79; }
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

  /* 封面 */
  .cover{ background: linear-gradient(180deg, rgba(5,7,13,.82) 0%, rgba(5,7,13,.35) 34%, rgba(5,7,13,.72) 62%, rgba(5,7,13,.97) 90%), url("图片/logo/cover_bg.jpg") center 42%/cover no-repeat !important; }
  .cover:before{ background: transparent !important; }
  .cover .cover-main{ color:#fff; max-width:900px; background:rgba(5,7,13,.34); border-radius:18px; padding:34px 42px; box-shadow:0 10px 40px rgba(0,0,0,.35); }
  .cover .cover-main h1{ font-family:"Georgia","Noto Serif SC",serif; font-size:clamp(46px,8vw,84px); letter-spacing:4px; color:#fff; margin:0; text-shadow:0 3px 24px rgba(0,0,0,.55); }
  .cover .cover-main h1 span{ color:#fff; }
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
    plugins: []
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



def to_cn_quotes(text):
    """把正文里的直引号 "..." 换成中文引号 “...”，避免 docsify 的加粗失效，也更符合中文排版。
    跳过代码块与行内代码。"""
    state = {"open": True}
    def conv(s):
        buf = []
        for ch in s:
            if ch == '"':
                buf.append("“" if state["open"] else "”")
                state["open"] = not state["open"]
            else:
                buf.append(ch)
        return "".join(buf)
    parts = re.split(r'(```.*?```)', text, flags=re.S)
    out = []
    for seg in parts:
        if seg.startswith('```'):
            out.append(seg); continue
        subs = re.split(r'(`[^`]*`)', seg)
        for i, sub in enumerate(subs):
            if not sub.startswith('`'):
                subs[i] = conv(sub)
        out.append("".join(subs))
    return "".join(out)

def main():
    os.makedirs(OUT, exist_ok=True)

    # 标题
    for s in SECTIONS:
        if not s.get("title"):
            s["title"] = first_h1(os.path.join(SRC, s["src"]))

    # 章节 markdown（图片路径 ../图片 -> 图片）
    for s in SECTIONS:
        text = open(os.path.join(SRC, s["src"]), encoding="utf-8").read()
        text = text.replace("](../图片/", "](图片/")
        text = to_cn_quotes(text)
        open(os.path.join(OUT, s["id"] + ".md"), "w", encoding="utf-8").write(text)

    # 侧栏
    lines = ["- [前言](preface.md)", ""]
    for s in SECTIONS:
        if s["id"] == "preface":
            continue
        if s.get("kind") == "part":
            lines.append(f"- **{s['title']}**")
        elif s["id"].startswith("ch"):
            lines.append(f"  - [{short_title(s['title'])}]({s['id']}.md)")
        else:
            lines.append(f"- [{s['title']}]({s['id']}.md)")
    open(os.path.join(OUT, "_sidebar.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

    # 封面
    cover = """# HDR 超详解

> 从像素到眼睛的完整指南

- 6 篇 20 章 · 90 余张原创示意图
- 从光与颜色，到面板、接口、系统与调色

[开始阅读](ch01.md)
[下载 PDF](HDR超详解.pdf)
"""
    open(os.path.join(OUT, "_coverpage.md"), "w", encoding="utf-8").write(cover)

    # 首页
    home = """# HDR 超详解

> 从像素到眼睛的完整指南 · 作者：Dezeming

本书用最直白的方式讲清**高动态范围（HDR）**：从光与颜色的基础，到色域与传递函数，到 HDR10、杜比视界、HDR10+ 与 HLG 的规则，再到面板、接口、操作系统、播放软件与调色，最后落到选购、校准与排查。

- **6 篇 20 章**，配 90 余张原创示意图
- 可从左上角目录逐章阅读，也可 [**下载整本 PDF**](HDR超详解.pdf)

## 目录

- [前言](preface.md)
- **第一篇 基础篇：为什么会有 HDR**
  - [第 1 章 从 SDR 说起](ch01.md)
  - [第 2 章 亮度、对比度与动态范围](ch02.md)
  - [第 3 章 人眼如何看光](ch03.md)
- **第二篇 色彩科学篇**
  - [第 4 章 颜色的坐标系](ch04.md)
  - [第 5 章 色域漫游](ch05.md)
  - [第 6 章 传递函数与 Gamma](ch06.md)
  - [第 7 章 HDR 的两把尺子：PQ 与 HLG](ch07.md)
- **第三篇 标准篇**
  - [第 8 章 HDR10 基石](ch08.md)
  - [第 9 章 Dolby Vision 与 HDR10+](ch09.md)
  - [第 10 章 位深、编码与色度采样](ch10.md)
- **第四篇 硬件篇**
  - [第 11 章 面板与背光](ch11.md)
  - [第 12 章 自发光时代](ch12.md)
  - [第 13 章 认证与 DisplayHDR](ch13.md)
- **第五篇 传输与系统篇**
  - [第 14 章 接口与带宽](ch14.md)
  - [第 15 章 链路握手](ch15.md)
  - [第 16 章 操作系统里的 HDR](ch16.md)
- **第六篇 软件与实战篇**
  - [第 17 章 Tone Mapping](ch17.md)
  - [第 18 章 内容世界](ch18.md)
  - [第 19 章 选购、校准与色彩管理](ch19.md)
  - [第 20 章 常见误区与精通路线](ch20.md)
- [附录 A 术语速查表](appendix-a.md)
- [附录 B 参考文献](appendix-b.md)
- [后记](afterword.md)
"""
    open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write(home)

    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(INDEX_HTML)
    open(os.path.join(OUT, ".nojekyll"), "w", encoding="utf-8").write("")

    # 清理旧的静态页（保留 index.html）
    for f in glob.glob(OUT + "/*.html"):
        if os.path.basename(f) != "index.html":
            os.remove(f)

    copy_images()
    if os.path.exists(PDF_SRC):
        shutil.copy2(PDF_SRC, OUT + "/HDR超详解.pdf")
        print("pdf", round(os.path.getsize(PDF_SRC) / 1e6, 1), "MB")
    print("done:", len(SECTIONS), "chapters")


if __name__ == "__main__":
    main()
