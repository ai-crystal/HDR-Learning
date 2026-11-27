# -*- coding: utf-8 -*-
"""第 09 章 图 5：各平台 HDR 能力对照（2 系统级 / 1 有条件 / 0 无公开能力）。

取值依据各家公开文档与 2024 至 2026 年的版本状态，属定性分档，不是精度评分。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
from matplotlib.colors import LinearSegmentedColormap

H.set_book("hdr-tech")
plt = H.plt

rows = ["HDR 视频解码", "HDR 静态图显示", "增益图写入", "增益图读取",
        "超白合成（EDR）", "HDR 屏幕截图"]
cols = ["iOS\niPadOS", "Android", "macOS", "Windows", "浏览器"]

M = np.array([
    [2, 2, 2, 2, 1],
    [2, 2, 2, 1, 1],
    [2, 2, 1, 0, 0],
    [2, 2, 2, 1, 1],
    [2, 1, 2, 1, 1],
    [1, 1, 1, 1, 0],
])

cmap = LinearSegmentedColormap.from_list(
    "cap", ["#eef1f4", "#9dbfd9", "#1f4e79"])

fig, ax = plt.subplots(figsize=(7.2, 4.1))
im = ax.imshow(M, cmap=cmap, vmin=0, vmax=2, aspect="auto")
ax.set_xticks(range(len(cols)))
ax.set_xticklabels(cols, fontsize=9.5)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels(rows, fontsize=9.5)
ax.set_xticks(np.arange(-0.5, len(cols)), minor=True)
ax.set_yticks(np.arange(-0.5, len(rows)), minor=True)
ax.grid(which="minor", color="white", lw=2.0)
ax.grid(which="major", visible=False)
ax.tick_params(which="minor", length=0)
ax.tick_params(length=0)

for i in range(len(rows)):
    for j in range(len(cols)):
        v = M[i, j]
        ax.text(j, i, str(v), ha="center", va="center", fontsize=12,
                color="white" if v == 2 else "#12233b",
                fontweight="bold")

ax.text(0.5, -0.155,
        "2 系统级支持　1 有条件支持　0 无公开能力\n"
        "（据 2024 至 2026 年公开文档整理，属定性分档，以官方文档为准）",
        transform=ax.transAxes, ha="center", va="top",
        fontsize=8.0, color=H.GRAY, linespacing=1.7)

H.save(fig, 9, "f5_platform_matrix")
