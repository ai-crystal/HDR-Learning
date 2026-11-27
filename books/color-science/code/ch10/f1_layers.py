# -*- coding: utf-8 -*-
"""第 10 章 图 1：色域映射的三个层次（描述、判定、决策）与各层的数据结构。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
import numpy as np

plt = H.plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(7.6, 4.0))
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.grid(False)


def box(x, y, w, h, fc, ec, lw=1.1, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                fc=fc, ec=ec, lw=lw, zorder=z))


def arrow(x1, y1, x2, y2, c="#4a5666"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=14, color=c, lw=1.3,
                                 shrinkA=0, shrinkB=0, zorder=4))


# 输入
box(0.10, 2.42, 1.18, 1.10, "#eef2f6", "#9fb0c0")
ax.text(0.69, 3.24, "源颜色", ha="center", va="center", fontsize=9.6,
        fontweight="bold", color=H.DARK)
ax.text(0.69, 2.88, "XYZ 或 Lab", ha="center", va="center", fontsize=8.2, color="#4a5666")
ax.text(0.69, 2.66, "逐像素处理", ha="center", va="center", fontsize=8.2, color="#4a5666")

LX = [1.75, 4.00, 6.25]
cols = [H.NAVY, H.TEAL, H.ORANGE]
heads = ["描述层", "判定层", "决策层"]
titles = ["色域边界 GBD", "内外与距离", "映射动作"]
items = [
    ["顶点集与拓扑", "凸包、α-shape", "等亮度切片多边形", "gamut ID 与 cusp 表"],
    ["点在体内（射线法）", "超界多远（求交）", "边界法向与色相", "距离场与分隔面"],
    ["裁剪：保色相明度", "压缩：保序与细节", "空间域：保局部对比", "烘焙：3D LUT"],
]
for i in range(3):
    x = LX[i]
    box(x, 4.45, 1.95, 1.05, "white", cols[i], lw=1.4)
    ax.text(x + 0.975, 5.22, f"{i+1} {heads[i]}", ha="center", va="center",
            fontsize=9.8, fontweight="bold", color=cols[i])
    ax.text(x + 0.975, 4.76, titles[i], ha="center", va="center", fontsize=8.8,
            color=H.DARK)
    box(x, 1.62, 1.95, 2.60, "#fbfcfd", "#c9d3de", lw=0.9)
    for k, t in enumerate(items[i]):
        ax.text(x + 0.12, 3.86 - k * 0.62, t, ha="left", va="center", fontsize=8.2,
                color="#39424e")

# 层间箭头（只画在列间空隙里）
arrow(1.30, 2.97, 1.73, 2.97)
arrow(3.72, 2.97, 3.98, 2.97)
arrow(5.97, 2.97, 6.23, 2.97)

# 输出
box(8.52, 2.42, 1.28, 1.10, "#eef2f6", "#9fb0c0")
ax.text(9.16, 3.22, "设备信号", ha="center", va="center", fontsize=9.2,
        fontweight="bold", color=H.DARK)
ax.text(9.16, 2.86, "R G B", ha="center", va="center", fontsize=8.4, color="#4a5666")
ax.text(9.16, 2.64, "或 LUT 索引", ha="center", va="center", fontsize=7.6,
        color="#4a5666")
arrow(8.22, 2.97, 8.50, 2.97)

# 底部虚线：评价回写
ax.plot([8.62, 8.62, 2.72], [2.40, 0.78, 0.78], color="#8d9aa8", lw=1.0,
        ls=(0, (4, 3)), zorder=1)
ax.add_patch(FancyArrowPatch((2.72, 0.78), (2.72, 1.58), arrowstyle="-|>",
                             mutation_scale=12, color="#8d9aa8", lw=1.0, zorder=1))
ax.text(5.55, 0.55, "评价结果回写：调膝点、换锚点、重新烘焙 LUT", ha="center",
        va="center", fontsize=7.8, color="#6b7885")

# 顶部：目标设备参数注入
ax.plot([2.72, 2.72], [5.75, 5.54], color="#8d9aa8", lw=1.0, ls=(0, (4, 3)), zorder=1)
ax.text(2.72, 5.86, "目标设备的基色、白点、峰值亮度", ha="left", va="bottom",
        fontsize=7.9, color="#6b7885")

H.save(fig, 10, "f1_layers")
