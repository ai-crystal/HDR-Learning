# -*- coding: utf-8 -*-
"""第 11 章 图 3：三种子像素排布（示意）。

(a) 条状 RGB        每个像素三色齐备，同色子像素在竖直方向排成一条线
(b) PenTile RGBG    2×2 共四个子像素，绿色两个、红蓝各一个
(c) 三角排布        每行错开半格，三色的重心构成三角点阵

三种排布画在同一尺寸的方格里，方便直接比子像素数量；子像素大小与间距是
示意值，不代表具体产品的开口率。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: F401
from matplotlib.patches import Rectangle, FancyBboxPatch

plt = H.plt

CR = "#c0392b"
CG = "#27ae60"
CB = "#2d6fbf"

fig, axes = plt.subplots(1, 3, figsize=(7.4, 3.05),
                         gridspec_kw=dict(wspace=0.13, left=0.02, right=0.985,
                                          top=0.925, bottom=0.115))
for ax in axes:
    ax.set_xlim(-0.05, 4.05)
    ax.set_ylim(-0.05, 3.05)
    ax.set_aspect("equal")
    ax.axis("off")


def cell(ax, x, y, w, h, color, r=0.05):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                linewidth=0, facecolor=color))


# ---------- (a) 条状 ----------
ax = axes[0]
PW, PH, gap = 1.0, 0.78, 0.20
for row in range(3):
    for col in range(4):
        x0, y0 = col * PW, row * (PH + gap)
        for k, c in enumerate((CR, CG, CB)):
            cell(ax, x0 + 0.035 + k * (PW / 3), y0 + 0.02, PW / 3 - 0.07, PH, c)
ax.set_title("(a) 条状 RGB 排布", fontsize=9.2, pad=5)
ax.text(2.0, -0.20, "每像素 3 个子像素，共 24.9 M", fontsize=7.5, color="#4a5666",
        ha="center", va="top")
for k, lab in enumerate("RGB"):
    ax.text(0.20 + k * (PW / 3), 2.86, lab, fontsize=7.0, color="#4a5666", ha="center")

# ---------- (b) PenTile RGBG ----------
ax = axes[1]
S, gp = 0.5, 0.055
for row in range(6):
    for col in range(8):
        if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
            c = CG
        elif row % 2 == 0:
            c = CR
        else:
            c = CB
        cell(ax, col * S + gp / 2, row * S + gp / 2, S - gp, S - gp, c, r=0.04)
ax.set_title("(b) PenTile RGBG 排布", fontsize=9.2, pad=5)
ax.text(2.0, -0.20, "每 2×2 格 4 个子像素，共 16.6 M", fontsize=7.5, color="#4a5666",
        ha="center", va="top")
ax.add_patch(Rectangle((0.02, 0.02), S * 2.0, S * 2.0, fill=False,
                       edgecolor="#12233b", lw=1.2, ls=(0, (3, 2))))
ax.annotate("G 两个，R B 各一", xy=(S * 2.02, S * 1.05), xytext=(S * 2.55, S * 0.55),
            fontsize=7.0, color="#12233b", ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color="#12233b", lw=0.8),
            bbox=dict(facecolor="white", alpha=0.94, edgecolor="#12233b",
                      lw=0.5, pad=1.6))

# ---------- (c) 三角排布 ----------
ax = axes[2]
CW, RH, SW, SH = 0.86, 0.86, 0.38, 0.34
for j in range(3):
    for i in range(4):
        x0 = i * CW + (j % 2) * 0.5 * CW
        y0 = 0.12 + j * RH
        cell(ax, x0 + 0.24, y0 + 0.46, SW, SH, CG)
        cell(ax, x0 + 0.02, y0 + 0.08, SW, SH, CR)
        cell(ax, x0 + 0.46, y0 + 0.08, SW, SH, CB)
ax.set_title("(c) 三角错位排布", fontsize=9.2, pad=5)
ax.text(2.0, -0.20, "每像素 3 个子像素，行间错开半格", fontsize=7.5, color="#4a5666",
        ha="center", va="top")
ax.annotate("", xy=(0.0, 1.62), xytext=(0.0, 2.48), annotation_clip=False,
            arrowprops=dict(arrowstyle="<->", color="#7f8c8d", lw=0.9))
ax.text(-0.10, 2.05, "行错半格", fontsize=6.9, color="#7f8c8d", rotation=90,
        ha="right", va="center")

H.save(fig, 11, "f3_subpixel_layout")
