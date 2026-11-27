# -*- coding: utf-8 -*-
"""第 12 章 图 2：ICtCp 与 Jzazbz 的构造流程并列框图。

两条链路都从"绝对三刺激值"开始，都在某个环节插入 PQ 型压缩，但插入的位置
不同：ICtCp 先对 BT.2020 的 R'G'B' 编码再转锥空间，Jzazbz 先对 XYZ 做一次
预混再压缩。框图只画数据流，不写公式推导。
"""
import sys
import os

sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
plt = H.plt

from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(7.5, 4.15))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

BW, BH = 38.0, 12.6
COLS = {0: 2.0, 1: 58.0}
TOP = 84.0
GAP = 5.6


def box(x, y, w, h, text, fc, ec, fs=8.3, tc=H.DARK, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.6,rounding_size=1.2",
                                fc=fc, ec=ec, lw=1.15, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color=tc, zorder=4, linespacing=1.45,
            fontweight="bold" if bold else "normal")


def arrow(x0, y0, x1, y1, col=H.GRAY):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                                 mutation_scale=11, lw=1.15, color=col,
                                 shrinkA=1, shrinkB=1, zorder=2))


LEFT = [
    ("线性 BT.2020  $R,G,B$\n单位 cd/m$^2$", "#eef3f9", H.NAVY),
    ("PQ 编码（ST 2084）\n$R',G',B'$ 落在 0–1", "#e6eff7", H.NAVY),
    ("$M_1$ 定点矩阵  ÷4096\n$L,\\ M,\\ S$ 锥体响应", "#e6eff7", H.NAVY),
    ("加权差\n$I=\\frac{1}{2}(L+M)$，$C_t$，$C_p$", "#dbe8f4", H.NAVY),
]
RIGHT = [
    ("绝对 XYZ\n$Y$ 单位 cd/m$^2$", "#eef7f4", H.TEAL),
    ("预混  $X'=bX-(b-1)Z$\n$Y'=gY-(g-1)X$，$Z'=Z$", "#e6f4ef", H.TEAL),
    ("PQ 型压缩（÷10000）\n$L',M',S'$ 落在 0–1", "#e6f4ef", H.TEAL),
    ("$I_z=\\frac{1}{2}(L'+M')$，$a_z$，$b_z$\n$J_z$ 再压一次", "#d6efe7", H.TEAL),
]

hdr_y = 92.0
for ci, (title, sub, col) in ((0, ("ICtCp", "ITU-R BT.2100", H.NAVY)),
                              (1, ("Jzazbz", "Safdar 等，2017", H.TEAL))):
    x = COLS[ci]
    ax.text(x + BW / 2, hdr_y, title, ha="center", va="center", fontsize=11.0,
            color=col, fontweight="bold")
    ax.text(x + BW / 2, hdr_y - 5.2, sub, ha="center", va="center",
            fontsize=8.2, color=H.GRAY)

for ci, rows in ((0, LEFT), (1, RIGHT)):
    x = COLS[ci]
    for i, (txt, fc, ec) in enumerate(rows):
        y = TOP - i * (BH + GAP)
        box(x, y, BW, BH, txt, fc, ec)
        if i:
            arrow(x + BW / 2, y + BH + GAP - 1.0, x + BW / 2, y + BH + 1.4)

# 末端输出
for ci, txt, col in ((0, "$I$  全分辨率\n$C_t$，$C_p$ 可降采样", H.NAVY),
                     (1, "$J_z$，$a_z$，$b_z$\n直角坐标", H.TEAL)):
    x = COLS[ci]
    y = TOP - 4 * (BH + GAP)
    arrow(x + BW / 2, y + BH + GAP - 1.0, x + BW / 2, y + BH + 1.4)
    ax.text(x + BW / 2, y + BH / 2, txt, ha="center", va="center", fontsize=8.3,
            color=col, linespacing=1.45,
            bbox=dict(fc="white", ec=col, lw=1.0, ls=(0, (3, 2)), pad=4.5))

ax.text(50.0, 4.0,
        "ICtCp 先压缩再旋转，Jzazbz 先预混再压缩，两条链路的色相刻度因此不同",
        ha="center", va="center", fontsize=8.5, color=H.GRAY)

H.save(fig, 12, "f2_pipeline_compare")
