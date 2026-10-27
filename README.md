# HDR 超详解

> 从像素到眼睛的完整指南 · 作者：Dezeming

本书用最直白的方式讲清**高动态范围（HDR）**：从光与颜色的基础，到色域与传递函数，到 HDR10、杜比视界、HDR10+ 与 HLG 的规则，再到面板、接口、操作系统、播放软件与调色，最后落到选购、校准与排查。

- **6 篇 20 章**，配 90 余张原创示意图
- **在线阅读**：[https://ai-crystal.github.io/HDR-Learning/](https://ai-crystal.github.io/HDR-Learning/)
- 左侧目录逐章阅读，或 [**下载整本 PDF**](https://ai-crystal.github.io/HDR-Learning/output/HDR超详解.pdf)

## 目录

- [前言](book/front/preface.md)
- **第一篇　基础篇：为什么会有 HDR**
  - [第 01 章 从 SDR 说起：8 位、sRGB 与它的时代](book/chapters/ch01.md)
  - [第 02 章 亮度、对比度与动态范围：把话说白](book/chapters/ch02.md)
  - [第 03 章 人眼如何看光：对数视觉与 HDR 的意义](book/chapters/ch03.md)
- **第二篇　色彩科学篇：颜色的物理与数学**
  - [第 04 章 颜色的坐标系：CIE、色度图与三刺激值](book/chapters/ch04.md)
  - [第 05 章 色域漫游：sRGB / Rec.709 / DCI-P3 / Rec.2020](book/chapters/ch05.md)
  - [第 06 章 传递函数与 Gamma：从 CRT 到 sRGB](book/chapters/ch06.md)
  - [第 07 章 HDR 的两把尺子：PQ（ST 2084）与 HLG](book/chapters/ch07.md)
- **第三篇　标准篇：HDR 世界的规则**
  - [第 08 章 HDR10：开放标准的基石](book/chapters/ch08.md)
  - [第 09 章 Dolby Vision、HDR10+ 与 HDR Vivid：动态元数据的较量](book/chapters/ch09.md)
  - [第 10 章 位深、编码与色度采样：10bit、4:2:0 与 ICtCp](book/chapters/ch10.md)
- **第四篇　硬件篇：光从哪里来**
  - [第 11 章 面板与背光：LCD、FALD 与 Mini-LED](book/chapters/ch11.md)
  - [第 12 章 自发光时代：OLED、QD-OLED 与 MicroLED](book/chapters/ch12.md)
  - [第 13 章 认证怎么读：VESA DisplayHDR 与亮度/黑位/调光](book/chapters/ch13.md)
- **第五篇　传输与系统篇：把 HDR 送到眼前**
  - [第 14 章 接口与带宽：HDMI、DisplayPort 与 USB-C](book/chapters/ch14.md)
  - [第 15 章 链路握手：EDID、元数据、HDCP 与 DSC](book/chapters/ch15.md)
  - [第 16 章 操作系统里的 HDR：Windows、macOS、主机与手机](book/chapters/ch16.md)
- **第六篇　软件与实战篇：从会用到精通**
  - [第 17 章 Tone Mapping：HDR 如何落进显示器](book/chapters/ch17.md)
  - [第 18 章 内容世界：游戏、影视与创作软件](book/chapters/ch18.md)
  - [第 19 章 选购、校准与色彩管理](book/chapters/ch19.md)
  - [第 20 章 常见误区、术语速查与精通路线](book/chapters/ch20.md)
- [附录 A　术语速查表](book/appendix/appendix-a.md)
- [附录 B　参考文献](book/appendix/appendix-b.md)
- [后记](book/front/afterword.md)

## 构建与发布

- Windows 一键编译：双击仓库根目录的 `build.cmd`（或 `book/build/build.cmd`），生成 `output/HDR超详解.pdf`。
- 部署：GitHub **Settings → Pages**，Source 选 `main`，目录选 `/ (root)`。
