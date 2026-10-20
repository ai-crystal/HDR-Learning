# HDR-Learning

HDR 学习资料库。作者：许春晓。

## 目录

| 路径 | 内容 |
|---|---|
| `书/` | **书籍工程**：Markdown 源文件 + 编译脚本，产出 PDF 电子书 |
| `书/README.md` | 书籍结构、如何编译、如何加图 |
| `书籍输出/` | 编译产物：`HDR超详解.pdf` |
| `参考资料/` | 三篇来源文章的要点整理 |
| `00-全书大纲与术语表.md` | 全书大纲与统一术语表（编辑参考，不进入书内） |

## 快速开始：编译成 PDF

双击 `书/构建PDF.cmd`，产物输出到：

```
书籍输出\HDR超详解.pdf
```

或在 `书/` 目录手动两步：

```bash
D:\DevTools\Anaconda3\python.exe build\build_html.py   # Markdown -> HTML + 目录
node build\build_pdf.mjs                               # HTML -> PDF + 合并 + 页码
```

## 关于这本书

《HDR 超详解：从像素到眼睛的完整指南》六篇二十章，从光与色彩的基础一路讲到面板、接口、操作系统、软件与实战，帮只有基础计算机知识的人真正读懂 HDR。详细说明见 `书/README.md`。
