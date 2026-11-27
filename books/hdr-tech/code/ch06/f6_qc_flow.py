# -*- coding: utf-8 -*-
"""第 06 章 图 6：HDR 母版交付的质量控制流程（框图，坐标手工排版）。"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(7.4, 4.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.2)
ax.axis("off")

BW, BH = 2.55, 1.05
X0, X1, X2 = 0.60, 3.72, 6.85
YTOP, YBOT = 4.55, 2.35

steps = [
    (X0, YTOP, "1  文件与元数据", "容器、位深、ST 2086\nMaxCLL / MaxFALL"),
    (X1, YTOP, "2  色域与峰值", "越界像素统计\n峰值与元数据一致性"),
    (X2, YTOP, "3  量化与色带", "10/12 位、近黑台阶\n渐变区域"),
    (X2, YBOT, "4  时域稳定", "帧间亮度跳变\nABL 触发频次"),
    (X1, YBOT, "5  参考监视器看片", "高光层次、暗部细节\n图卡白 203 nit"),
    (X0, YBOT, "6  报告与签字", "测量条件、设备\n不确定度"),
]

for x, y, title, sub in steps:
    box = FancyBboxPatch((x, y), BW, BH, boxstyle="round,pad=0.02,rounding_size=0.08",
                         facecolor="#eaf0f7", edgecolor=H.NAVY, lw=1.0)
    ax.add_patch(box)
    ax.text(x + BW / 2, y + BH - 0.24, title, ha="center", va="center",
            fontsize=8.6, color=H.NAVY)
    ax.text(x + BW / 2, y + 0.33, sub, ha="center", va="center",
            fontsize=7.4, color="#3d4c5c", linespacing=1.35)


def arrow(x1, y1, x2, y2, style="-|>", color=H.NAVY, ls="-", rad=0.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=11, lw=1.1, color=color,
                                 linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}"))


arrow(X0 + BW, YTOP + BH / 2, X1, YTOP + BH / 2)
arrow(X1 + BW, YTOP + BH / 2, X2, YTOP + BH / 2)
arrow(X2 + BW / 2, YTOP, X2 + BW / 2, YBOT + BH)
arrow(X2, YBOT + BH / 2, X1 + BW, YBOT + BH / 2)
arrow(X1, YBOT + BH / 2, X0 + BW, YBOT + BH / 2)

# 不通过的回路，走左侧留白，避开所有方框
XL = 0.44
arrow(X0, YBOT + BH / 2, XL, YBOT + BH / 2, style="-", color=H.RED, ls=(0, (4, 2)))
arrow(XL, YBOT + BH / 2, XL, YTOP + BH / 2, style="-", color=H.RED, ls=(0, (4, 2)))
arrow(XL, YTOP + BH / 2, X0, YTOP + BH / 2, color=H.RED, ls=(0, (4, 2)))
ax.text(0.16, (YTOP + YBOT + BH) / 2, "不通过：回修后重跑", fontsize=7.4, color=H.RED,
        rotation=90, va="center", ha="center",
        bbox=dict(boxstyle="round,pad=0.10", facecolor="white", edgecolor="none"))

# 输出
ax.add_patch(FancyBboxPatch((3.05, 0.35), 3.9, 0.80, boxstyle="round,pad=0.02,rounding_size=0.08",
                            facecolor="#f6e7cf", edgecolor=H.ORANGE, lw=1.0))
ax.text(5.0, 0.75, "交付：母版 + 元数据 + QC 报告", ha="center", va="center",
        fontsize=8.4, color="#8a5a1c")
arrow(X0 + BW / 2, YBOT, X0 + BW / 2, 0.75, style="-", color=H.ORANGE)
arrow(X0 + BW / 2, 0.75, 3.05, 0.75, color=H.ORANGE)

H.save(fig, 6, "f6_qc_flow")
