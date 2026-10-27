# -*- coding: utf-8 -*-
"""f3_subsampling：4:4:4 / 4:2:2 / 4:2:0 的亮度与色度采样点阵。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np

N = 8                     # 8x8 亮度像素块
rows = np.arange(N) + 0.5
cols = np.arange(N) + 0.5

formats = [
    ("4:4:4", "色度全份（100%）", 1, 1),
    ("4:2:2", "色度水平减半（≈67%）", 2, 1),
    ("4:2:0", "色度横纵各减半（≈50%）", 2, 2),
]

fig, axes = H.plt.subplots(1, 3, figsize=(7.2, 3.5))

for ax, (name, note, dx, dy) in zip(axes, formats):
    ax.set_xlim(0, N); ax.set_ylim(0, N)
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(N + 1)); ax.set_yticks(np.arange(N + 1))
    ax.set_xticklabels([]); ax.set_yticklabels([])
    ax.grid(True, color="#e6ebf1", lw=0.6)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_edgecolor(H.NAVY); s.set_linewidth(1.2)

    # 亮度 Y：每个像素点都有
    YX, YY = np.meshgrid(cols, rows)
    ax.scatter(YX.ravel(), YY.ravel(), s=26, marker="s",
               facecolor=H.NAVY, edgecolor="white", linewidth=0.5, zorder=3)

    # 色度 Cb/Cr：按采样率取点
    cxs = cols[::dx] if dx > 1 else cols
    cys = rows[::dy] if dy > 1 else rows
    CX, CY = np.meshgrid(cxs, cys)
    ax.scatter(CX.ravel(), CY.ravel(), s=62, marker="o",
               facecolor="none", edgecolor=H.ORANGE, linewidth=1.8, zorder=4)

    nC = len(cxs) * len(cys)
    ax.set_title(f"{name}　色度点 {nC}/64", fontsize=11, color=H.NAVY,
                 fontweight="bold", pad=8)
    ax.text(0.5, -0.09, note, transform=ax.transAxes, ha="center", va="top",
            fontsize=9, color=H.ORANGE)

# 图例
from matplotlib.lines import Line2D
handles = [
    Line2D([], [], marker="s", linestyle="none", markersize=8,
           markerfacecolor=H.NAVY, markeredgecolor="white", label="亮度 Y（每像素 1 个）"),
    Line2D([], [], marker="o", linestyle="none", markersize=9,
           markerfacecolor="none", markeredgecolor=H.ORANGE, markeredgewidth=1.8,
           label="色度 Cb/Cr（人眼不敏感，可少存）"),
]
fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False,
           fontsize=9, bbox_to_anchor=(0.5, -0.02))

fig.suptitle("图 10-3　色度采样点阵：4:4:4 / 4:2:2 / 4:2:0",
             fontsize=13, fontweight="bold", y=1.02)
fig.tight_layout(rect=[0, 0.04, 1, 0.99])
H.save(fig, 10, "f3_subsampling")
