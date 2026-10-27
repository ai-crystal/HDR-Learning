# HDR 超详解：从像素到眼睛的完整指南

> 作者：Dezeming · 2026

一本讲清高动态范围（HDR）的中文教程：从光与颜色的基础，到色域与传递函数，到 HDR10、杜比视界、HDR10+ 与 HLG 的规则，再到面板、接口、操作系统、播放软件与调色，最后落到选购、校准与排查。全书 6 篇 20 章，配 90 余张原创示意图。

## 在线阅读

本站用 [docsify](https://docsify.js.org/) 构建，章节用 `#/` 路由切换，每章都有独立链接：

- 首页：`https://<用户名>.github.io/<仓库名>/`
- 某一章：`https://<用户名>.github.io/<仓库名>/#/book/chapters/ch07`
- 本地预览：在仓库根目录运行 `python -m http.server 8765`，打开 `http://127.0.0.1:8765/`

## 下载

- [**整本 PDF（约 18.8 MB）**](output/HDR超详解.pdf) — 213 页，带书签目录

## 目录

> 书稿只有一份：`book/chapters/`。网页与 GitHub 都直接读它。

### 第一篇 基础篇：为什么会有 HDR
1. [从 SDR 说起](book/chapters/ch01.md)
2. [亮度、对比度与动态范围](book/chapters/ch02.md)
3. [人眼如何看光](book/chapters/ch03.md)

### 第二篇 色彩科学篇：颜色的物理与数学
4. [颜色的坐标系](book/chapters/ch04.md)
5. [色域漫游](book/chapters/ch05.md)
6. [传递函数与 Gamma](book/chapters/ch06.md)
7. [HDR 的两把尺子：PQ 与 HLG](book/chapters/ch07.md)

### 第三篇 标准篇：HDR 世界的规则
8. [HDR10 基石](book/chapters/ch08.md)
9. [Dolby Vision 与 HDR10+](book/chapters/ch09.md)
10. [位深、编码与色度采样](book/chapters/ch10.md)

### 第四篇 硬件篇：光从哪里来
11. [面板与背光](book/chapters/ch11.md)
12. [自发光时代](book/chapters/ch12.md)
13. [认证与 DisplayHDR](book/chapters/ch13.md)

### 第五篇 传输与系统篇：把 HDR 送到眼前
14. [接口与带宽](book/chapters/ch14.md)
15. [链路握手](book/chapters/ch15.md)
16. [操作系统里的 HDR](book/chapters/ch16.md)

### 第六篇 软件与实战篇：从会用到精通
17. [Tone Mapping](book/chapters/ch17.md)
18. [内容世界](book/chapters/ch18.md)
19. [选购、校准与色彩管理](book/chapters/ch19.md)
20. [常见误区与精通路线](book/chapters/ch20.md)

- [附录 A 术语速查表](book/appendix/appendix-a.md)
- [附录 B 参考文献](book/appendix/appendix-b.md)

## 仓库结构

```text
book/
├── chapters/        第 01–20 章（唯一的书稿正文）
├── front/           封面/扉页/版权/前言/篇首/后记/封底
├── appendix/        术语速查、参考文献
├── images/          插图（按章分目录）
├── code/            生成插图的 Python 代码（按章）
└── build/           PDF 构建脚本

tools/build_site.py  docsify 站点生成脚本
output/              整本 PDF（下载）
index.html           在线阅读入口（docsify）
```

本仓库只包含**书稿、插图和绘图代码**；写作规范、大纲、参考资料等不在此仓库。

## 本地构建

```bash
# 1) 生成 PDF（需要 Python + markdown + PyMuPDF、Node、Chrome）
cd book/build
python build_html.py
node build_pdf.mjs
python apply_outline.py
cd ../..

# 2) 重新生成站点入口（侧栏/封面/首页）
python tools/build_site.py
```

## 部署到 GitHub Pages

1. 把仓库推到 GitHub；
2. 仓库 **Settings → Pages → Build and deployment**；
3. Source 选 **Deploy from a branch**，分支 `main`，目录选 **`/ (root)`**；
4. 保存后访问 `https://<用户名>.github.io/<仓库名>/`。

根目录已放 `.nojekyll`，避免 Jekyll 处理带下划线的文件（`_sidebar.md` 等）。
