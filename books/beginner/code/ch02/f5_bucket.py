# -*- coding: utf-8 -*-
"""图 02-5 小水杯 vs 大水桶：容量 = 动态范围

用两个容器的「高度（以档为单位）」表示动态范围，
说明 HDR 不只是把杯子换成桶，而是同时抬高上限、压低下限。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np
from matplotlib.patches import Polygon, FancyArrowPatch

plt = H.plt

fig, ax = plt.subplots(figsize=(7.2, 4.7))
ax.set_xlim(-2.6, 14.0)
ax.set_ylim(-0.45, 8.6)
ax.axis("off")

UNIT = 0.235            # 1 档 = 0.235 单位高


def draw_vessel(x0_top, x1_top, x0_bot, x1_bot, y0, stops, face, edge,
                top_nit, bot_nit, label, ratio_text, side="left"):
    h = stops * UNIT
    y1 = y0 + h
    ax.add_patch(Polygon([[x0_bot, y0], [x1_bot, y0], [x1_top, y1],
                          [x0_top, y1]], closed=True, fill=False,
                         edgecolor=edge, lw=2.4, zorder=4))
    ax.add_patch(Polygon([[x0_bot + 0.07, y0 + 0.06], [x1_bot - 0.07, y0 + 0.06],
                          [x1_top - 0.07, y1 - 0.07], [x0_top + 0.07, y1 - 0.07]],
                         closed=True, facecolor=face, alpha=0.28,
                         edgecolor="none", zorder=3))
    for s in range(1, int(np.ceil(stops)) + 1):
        yy = y0 + s * UNIT
        if yy < y1 - 0.001:
            ax.plot([x0_top + 0.03, x1_top - 0.03], [yy, yy], color=edge,
                    lw=0.7, alpha=0.45, zorder=5)
    # 水面
    ax.plot([x0_top, x1_top], [y1, y1], color=face, lw=4.0,
            solid_capstyle="round", zorder=6, alpha=0.9)
    # 容量双箭头（在容器右侧）
    ax.annotate("", xy=(x1_top + 0.28, y0), xytext=(x1_top + 0.28, y1),
                arrowprops=dict(arrowstyle="<->", color=edge, lw=1.7))
    ax.text(x1_top + 0.48, (y0 + y1) / 2, f"{stops:g} 档", color=edge,
            fontsize=11, fontweight="bold", va="center", ha="left")
    # 名称
    ax.text((x0_top + x1_top) / 2, y1 + 0.28, label, ha="center", va="bottom",
            color=edge, fontsize=11.5, fontweight="bold")
    # 上限 / 下限亮度
    if side == "left":
        ax.text(x0_top - 0.12, y1, f"最亮 {top_nit:g} nit", ha="right",
                va="bottom", fontsize=8.8, color=edge, fontweight="bold")
        ax.text(x0_bot - 0.12, y0, f"最暗 {bot_nit:g} nit", ha="right",
                va="top", fontsize=8.8, color=H.GRAY)
    else:
        cx = (x0_top + x1_top) / 2
        ax.text(cx, y1 + 0.86, f"最亮 {top_nit:g} nit", ha="center",
                va="bottom", fontsize=8.8, color=edge, fontweight="bold")
        ax.text(cx, y0 - 0.88, f"最暗 {bot_nit:g} nit", ha="center",
                va="top", fontsize=8.8, color=H.GRAY)
    # 容量说明
    ax.text((x0_top + x1_top) / 2, y0 - 0.45, ratio_text, ha="center",
            va="top", fontsize=9.8, color=edge, fontweight="bold")


# 小水杯：SDR，10 档（100 : 0.1）
draw_vessel(1.0, 2.8, 1.4, 2.4, 0.9, 10, H.NAVY, H.NAVY,
            100.0, 0.1, "SDR：小水杯", "容量 ≈ 1000:1")

# 大水桶：HDR，约 17.6 档（1000 : 0.005）
draw_vessel(6.0, 9.6, 6.5, 9.1, 0.9, 17.6, H.ORANGE, "#c9670f",
            1000.0, 0.005, "HDR：大水桶", "容量 ≈ 200 000:1", side="top")

# 中间的对比箭头（位于两容器之间）
ax.add_patch(FancyArrowPatch((3.45, 2.15), (5.75, 4.05), arrowstyle="->",
                             mutation_scale=15, color=H.DARK, lw=1.9))
ax.text(4.68, 3.55, "上限抬高\n10×", fontsize=9, color=H.DARK,
        fontweight="bold", ha="center", va="bottom", linespacing=1.3)
ax.add_patch(FancyArrowPatch((3.45, 1.10), (5.75, 0.95), arrowstyle="->",
                             mutation_scale=15, color=H.DARK, lw=1.9))
ax.text(4.68, 1.32, "黑位压低 20×", fontsize=9, color=H.DARK,
        fontweight="bold", ha="center", va="bottom")

ax.text(5.4, 7.05, "水量 = 亮度；容器高度 = 动态范围（档）",
        ha="center", va="center", fontsize=9.8, color=H.DARK,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.42", fc="#f4f7fb", ec=H.NAVY, lw=1.0))

ax.set_title("把 SDR / HDR 想成水杯与水桶：容量就是动态范围",
             fontsize=12, fontweight="bold", pad=12)
H.save(fig, 2, "f5_bucket")
