# -*- coding: utf-8 -*-
"""第 11 章 图 1：HDR 到 SDR 的三条变换路径。

三行分别对应变换发生在显示端、播放器端、母版端。每行的四个方框从左到右是
母版、码流、变换环节、终端。右侧一列文字说明参数写在哪、覆盖范围、能否复核。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

H.set_book("hdr-tech")
plt = H.plt

fig, ax = plt.subplots(figsize=(7.6, 4.7))
fig.subplots_adjust(left=0.012, right=0.988, bottom=0.015, top=0.985)
ax.set_xlim(0.0, 10.4)
ax.set_ylim(0.0, 4.80)
ax.axis("off")

ROWS = [
    ("显示端　电视固件自己压", 3.74, 0.58, [
        ("HDR 母版\n4000 nit PQ", H.BLUE),
        ("HDR 码流\nPQ + 静态元数据", H.BLUE),
        ("电视内部\n色调映射", H.RED),
        ("SDR 面板\n或低亮面板", H.GRAY),
    ], "参数：写在固件里\n范围：全片一条曲线\n复核：做不到\n一致性：随品牌而变"),

    ("播放器端　机顶盒或播放器压", 2.42, 0.58, [
        ("HDR 母版", H.BLUE),
        ("HDR 码流", H.BLUE),
        ("播放器或机顶盒\n色调映射", H.ORANGE),
        ("SDR 电视", H.GRAY),
    ], "参数：菜单里的几档\n范围：全片或单档\n复核：偶尔\n一致性：中"),

    ("母版端　单独做一版 SDR", 1.10, 0.58, [
        ("HDR 母版", H.BLUE),
        ("调色台\n逐镜头 trim", H.TEAL),
        ("SDR 母版\nBT.1886", H.TEAL),
        ("SDR 电视", H.GRAY),
    ], "参数：每个镜头一组\n范围：逐镜头\n复核：调色师逐个看\n一致性：高"),
]

BW, BH = 1.50, 0.58
XS = [0.34, 2.09, 3.84, 5.59]

for title, yc, hh, boxes, note in ROWS:
    ax.add_patch(Rectangle((0.24, yc - 0.50), 10.10, 1.00,
                           facecolor="#f6f8fb", edgecolor="#e2e8ef",
                           lw=0.8, zorder=0))
    ax.text(0.34, yc + 0.56, title, fontsize=8.8, color=H.DARK,
            fontweight="bold", va="bottom", ha="left", zorder=4)

    for i, ((label, color), x) in enumerate(zip(boxes, XS)):
        key = (i == 2)
        ax.add_patch(FancyBboxPatch((x, yc - BH / 2), BW, BH,
                                    boxstyle="round,pad=0.012,rounding_size=0.06",
                                    facecolor=color, edgecolor="white",
                                    lw=1.0 if key else 0.6,
                                    alpha=0.94 if key else 0.80, zorder=3))
        ax.text(x + BW / 2, yc, label, fontsize=7.3, color="white",
                ha="center", va="center", linespacing=1.45, zorder=4,
                fontweight="bold" if key else "normal")
        if i < 3:
            ax.add_patch(FancyArrowPatch((x + BW + 0.015, yc),
                                         (XS[i + 1] - 0.015, yc),
                                         arrowstyle="-|>", mutation_scale=9,
                                         color="#8a97a6", lw=1.0, zorder=2))

    ax.text(7.32, yc, note, fontsize=7.0, color="#40505f",
            ha="left", va="center", linespacing=1.7, zorder=4)

ax.text(0.34, 0.24, "变换点越往上游走，可控性越高，付出的工时也越多",
        fontsize=7.4, color="#6b7a8a", style="italic", va="center")

H.save(fig, 11, "f1_three_paths")
