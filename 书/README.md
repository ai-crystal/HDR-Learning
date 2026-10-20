# HDR 超详解 · 书籍工程

本文由 Markdown 源文件编译成 PDF。作者：许春晓，2026 年 10 月。

## 目录结构

```text
书/
├── 00-封面.md               # 封面
├── 01-扉页.md               # 扉页
├── 02-版权页.md             # 版权与出版信息
├── 03-前言.md               # 前言
├── 篇一-篇首.md … 篇六-篇首.md   # 六个篇章的篇首语
├── 正文/                    # 第 01–20 章正文
├── 附录/附录A-术语速查.md     # 附录 A：术语速查
├── 附录/附录B-参考文献.md     # 附录 B：参考文献（≥50 份）
├── 后记.md
├── 封底.md
├── 图片/<NN>/               # 每章插图（NN=01..20，由 code 内脚本生成）
├── code/<第NN章>/*.py       # 每章绘图脚本（可独立运行）
├── code/common/hdrfig.py    # 绘图通用工具（中文字体/统一配色/HDR 数学函数）
├── code/_图示规格.md         # 全书图示规格与风格约定
├── 构建PDF.cmd              # 一键编译（Windows 双击运行）
└── build/                   # 构建脚本与运行库
    ├── build_html.py        # Markdown -> HTML（含封面/目录/分节）
    ├── build_pdf.mjs        # HTML -> PDF（Chrome 渲染 + 合并 + 页码）
    ├── build.sh             # git-bash 版构建脚本
    ├── mermaid.min.js       # 图表渲染库
    ├── tex-svg.js           # 数学公式渲染（MathJax，输出 SVG）
    ├── pdf-lib.min.js       # PDF 合并 / 页码
    └── fontkit.umd.js       # 字体嵌入支持
```

## 如何编译成 PDF

**方式一：双击 `构建PDF.cmd`**（Windows）即可，产物在：

```text
E:\Develop\HDR-Learning\书籍输出\HDR超详解.pdf
```

**方式二：手动三步**（在 `书/` 目录下）：

```bash
# 1) Markdown -> HTML，并生成 build/manifest.json
D:\DevTools\Anaconda3\python.exe build\build_html.py

# 2) HTML -> PDF（调用系统 Chrome 渲染，再用 pdf-lib 合并并加盖页码）
node build\build_pdf.mjs

# 3) 写入 PDF 书签（章节大纲）
D:\DevTools\Anaconda3\python.exe build\apply_outline.py
```

> git-bash 用户可直接运行 `bash build/build.sh`。

### 依赖环境

| 组件 | 需要的路径 | 用途 |
|---|---|---|
| Python | `D:\DevTools\Anaconda3\python.exe`（含 `markdown` 包） | Markdown → HTML |
| Node.js | `node` 或 `C:\Program Files\nodejs\node.exe` | 渲染编排与 PDF 合成 |
| Chrome | `C:\Program Files\Google\Chrome\Application\chrome.exe` | HTML → PDF 渲染引擎 |
| PyMuPDF | `D:\DevTools\Anaconda3`（`pip install pymupdf`） | 写入 PDF 书签（步骤 3） |

## 图示与代码

全书插图（亮度/色域/PQ/HLG/接口带宽/面板/流程等）均由 `code/` 下的 Python 脚本生成，统一使用 `code/common/hdrfig.py` 保证风格一致：

- 绘图解释器：`D:\DevTools\Anaconda3\python.exe`（matplotlib）；需要 OpenGL 时用 `D:\DevTools\Anaconda3\envs\moge3\python.exe`（moderngl）。
- 重新生成某章插图：

  ```bash
  cd code\第07章
  for %f in (*.py) do D:\DevTools\Anaconda3\python.exe %f
  ```

  图片会自动输出到 `图片/07/`。
- 新增插图后重新双击 `构建PDF.cmd`，图片会自动缩放并按图注排版。

## 如何加自定义图片

1. 把图片放进 `图片/<NN>/`（例如 `图片/07/pq曲线.png`）。
2. 在对应章节 Markdown 里引用：`![图 7-x　图注](图片/07/pq曲线.png)`。
3. 重新编译。方括号里的文字会成为图下方图注。图表（Mermaid 流程图）会由 `mermaid.min.js` 在渲染时自动画成矢量图。

## 编译逻辑简述

1. `build_html.py` 读取各 Markdown，按“封面 / 前后辅文 / 篇首 / 章节 / 附录”生成分节 HTML，并写出 `build/manifest.json`。
2. `build_pdf.mjs` 用 Chrome 逐节渲染成 A4 PDF，统计各节页数 → 生成带页码的目录 → 合并全书 → 用 pdf-lib 在每个正文页加盖页眉（书名 + 章名）与页码；并写出 `build/outline.json`（书签数据）。
3. `apply_outline.py` 用 PyMuPDF 把 `outline.json` 写入 PDF 的大纲（书签）：封面 / 前言 / 目录 / 六篇 / 二十章 / 附录 A·B / 后记，共 30+ 条，二三级层次。
3. 封面、扉页、版权页、前言、目录不编页码；正文从“第一篇”开始为第 1 页。

## 修改内容

- 改正文：编辑 `正文/第NN章-*.md`。
- 调版式/字体/页边距：编辑 `build/build_html.py` 顶部的 CSS 常量，然后重新编译。
