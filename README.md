# HDR 超详解：从像素到眼睛的完整指南

> 作者：Dezeming · 2026

一本讲清高动态范围（HDR）的中文教程：从光与颜色的基础，到色域与传递函数，到 HDR10、杜比视界、HDR10+ 与 HLG 的规则，再到面板、接口、操作系统、播放软件与调色，最后落到选购、校准与排查。全书 6 篇 20 章，配 90 余张原创示意图。

## 在线阅读

本站用 [docsify](https://docsify.js.org/) 构建：打开首页后，章节用 `#/` 路由切换，每章都有独立链接。

- **首页**：`https://<你的用户名>.github.io/<仓库名>/`
- **某一章**：`https://<你的用户名>.github.io/<仓库名>/#/ch07`
- **本地预览**：`cd docs && python -m http.server 8765`，然后打开 `http://127.0.0.1:8765/`

## 下载

- [**整本 PDF（约 18.8 MB）**](docs/HDR超详解.pdf) — 213 页，带书签目录

## 目录

> 网页版在 `docs/`；Markdown 原稿在 `书/正文/`。GitHub 网页端也能直接读 Markdown 与插图。

### 第一篇 基础篇：为什么会有 HDR
1. [从 SDR 说起](书/正文/第01章-从SDR说起.md) · [网页](docs/ch01.md)
2. [亮度、对比度与动态范围](书/正文/第02章-亮度对比度与动态范围.md) · [网页](docs/ch02.md)
3. [人眼如何看光](书/正文/第03章-人眼如何看光.md) · [网页](docs/ch03.md)

### 第二篇 色彩科学篇：颜色的物理与数学
4. [颜色的坐标系](书/正文/第04章-颜色的坐标系.md) · [网页](docs/ch04.md)
5. [色域漫游](书/正文/第05章-色域漫游.md) · [网页](docs/ch05.md)
6. [传递函数与 Gamma](书/正文/第06章-传递函数与Gamma.md) · [网页](docs/ch06.md)
7. [HDR 的两把尺子：PQ 与 HLG](书/正文/第07章-PQ与HLG.md) · [网页](docs/ch07.md)

### 第三篇 标准篇：HDR 世界的规则
8. [HDR10 基石](书/正文/第08章-HDR10基石.md) · [网页](docs/ch08.md)
9. [Dolby Vision 与 HDR10+](书/正文/第09章-DolbyVision与HDR10加.md) · [网页](docs/ch09.md)
10. [位深、编码与色度采样](书/正文/第10章-位深编码与色度采样.md) · [网页](docs/ch10.md)

### 第四篇 硬件篇：光从哪里来
11. [面板与背光](书/正文/第11章-面板与背光.md) · [网页](docs/ch11.md)
12. [自发光时代](书/正文/第12章-自发光时代.md) · [网页](docs/ch12.md)
13. [认证与 DisplayHDR](书/正文/第13章-认证与DisplayHDR.md) · [网页](docs/ch13.md)

### 第五篇 传输与系统篇：把 HDR 送到眼前
14. [接口与带宽](书/正文/第14章-接口与带宽.md) · [网页](docs/ch14.md)
15. [链路握手](书/正文/第15章-链路握手.md) · [网页](docs/ch15.md)
16. [操作系统里的 HDR](书/正文/第16章-操作系统里的HDR.md) · [网页](docs/ch16.md)

### 第六篇 软件与实战篇：从会用到精通
17. [Tone Mapping](书/正文/第17章-ToneMapping.md) · [网页](docs/ch17.md)
18. [内容世界](书/正文/第18章-内容世界.md) · [网页](docs/ch18.md)
19. [选购、校准与色彩管理](书/正文/第19章-选购校准与色彩管理.md) · [网页](docs/ch19.md)
20. [常见误区与精通路线](书/正文/第20章-常见误区与精通路线.md) · [网页](docs/ch20.md)

- [附录 A 术语速查表](书/附录/附录A-术语速查.md) · [网页](docs/appendix-a.md)
- [附录 B 参考文献](书/附录/附录B-参考文献.md) · [网页](docs/appendix-b.md)

## 仓库结构

```text
书/                 书稿 Markdown 原稿
├── 正文/           第 01–20 章
├── 附录/           术语速查、参考文献
├── 图片/           插图（按章分目录）
├── code/           生成插图的 Python 代码（按章）
└── build/          PDF 构建脚本

tools/              站点生成脚本（Markdown → 静态网页）
docs/               可在线阅读的静态站点（GitHub Pages）
```

本仓库只包含**书稿、插图和绘图代码**。写作规范、大纲、参考资料等不在此仓库中。

## 本地构建

```bash
# 1) 生成 PDF（需要 Python + markdown + PyMuPDF、Node、Chrome）
cd 书
python build/build_html.py
node build/build_pdf.mjs
python build/apply_outline.py

# 2) 生成在线阅读站点
cd ..
python tools/build_site.py
```

## 部署到 GitHub Pages

1. 把本仓库推到 GitHub；
2. 仓库 **Settings → Pages → Build and deployment**；
3. Source 选 **Deploy from a branch**，分支选 `main`，目录选 **/docs**；
4. 保存后访问 `https://<用户名>.github.io/<仓库名>/`。

`docs/` 里已放好 `.nojekyll`，避免 Jekyll 处理带下划线/中文的资源。
