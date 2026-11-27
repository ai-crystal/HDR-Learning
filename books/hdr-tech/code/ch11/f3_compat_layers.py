# -*- coding: utf-8 -*-
"""第 11 章 图 3：兼容层的码流结构与元数据开销。

(a) 五种承载结构。基础层画成粗条，增强层画在下方，元数据画成条上方的小竖线，
    静态元数据只有一处，动态元数据每帧一处。右侧一列写出设备不支持时退化成什么。
(b) 元数据与音视频码率的量级对比（横轴对数）。码率按 4K 24 帧、视频 15 Mb/s、
    每帧元数据 40–50 字节估算，只用于比较量级。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
from matplotlib.patches import Rectangle

H.set_book("hdr-tech")
plt = H.plt

fig = plt.figure(figsize=(8.4, 4.35))
gs = fig.add_gridspec(1, 2, width_ratios=[1.66, 1.0], wspace=0.60,
                      left=0.165, right=0.985, bottom=0.135, top=0.945)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

# ---------------- (a) 层结构 ----------------
ROWS = [
    ("HDR10", "hdr", "static", "HDR10"),
    ("HDR10+", "hdr", "dyn", "HDR10"),
    ("杜比视界 8.1", "hdr", "dyn", "HDR10"),
    ("杜比视界 7", "hdr_el", "dyn", "HDR10"),
    ("SL-HDR1", "sdr", "dyn", "SDR 基础层"),
]

BL_X0, BL_X1 = 0.0, 86.0
for k, (name, kind, meta, fallback) in enumerate(ROWS):
    y = len(ROWS) - 1 - k
    color = H.BLUE if kind.startswith("hdr") else H.GOLD
    ax1.add_patch(Rectangle((BL_X0, y - 0.19), BL_X1 - BL_X0, 0.38,
                            facecolor=color, edgecolor="white", lw=0.8, alpha=0.88, zorder=3))
    ax1.text((BL_X0 + BL_X1) / 2, y,
             "基础层　HDR10 基流" if kind != "sdr" else "基础层　SDR 10 bit",
             fontsize=7.2, color="white", ha="center", va="center", zorder=4)

    if kind == "hdr_el":
        ax1.add_patch(Rectangle((BL_X0, y + 0.22), BL_X1 - BL_X0, 0.15,
                                facecolor=H.ORANGE, edgecolor="white", lw=0.5,
                                hatch="////", alpha=0.85, zorder=3))
        ax1.text(BL_X1 + 1.2, y + 0.295, "增强层", fontsize=6.8, color=H.ORANGE,
                 ha="left", va="center")

    if meta == "static":
        ax1.plot([4, 4], [y + 0.20, y + 0.40], color=H.RED, lw=3.2,
                 solid_capstyle="butt", zorder=5)
        ax1.text(6.5, y + 0.30, "ST 2086 + MaxCLL / MaxFALL，全片一处", fontsize=6.9,
                 color=H.RED, ha="left", va="center")
    else:
        yt = 0.50 if kind == "hdr_el" else 0.20
        for xf in np.linspace(2, 84, 29):
            ax1.plot([xf, xf], [y + yt, y + yt + 0.16], color=H.TEAL, lw=1.0, zorder=5)
        ax1.text(BL_X1 + 1.2, y + yt + 0.08, "逐帧", fontsize=6.9, color=H.TEAL,
                 ha="left", va="center")

    ax1.text(BL_X1 + 10.5, y, fallback, fontsize=7.3, color="#40505f",
             ha="left", va="center")

ax1.text(BL_X1 + 10.5, len(ROWS) - 0.20, "不支持时退化为", fontsize=7.0,
         color="#7f8c8d", ha="left", va="center")
ax1.text(-0.5, len(ROWS) - 0.20, "(a)", fontsize=10, fontweight="bold",
         color=H.DARK, va="center")

ax1.set_yticks(range(len(ROWS)))
ax1.set_yticklabels([r[0] for r in ROWS][::-1], fontsize=8.2)
ax1.set_ylim(-0.85, len(ROWS) - 0.05)
ax1.set_xlim(-0.5, 118)
ax1.set_xticks([])
ax1.set_xlabel("沿时间轴（示意，不按真实帧数）", fontsize=9)
ax1.grid(False)
for sp in ("top", "right", "bottom"):
    ax1.spines[sp].set_visible(False)

# ---------------- (b) 码率开销 ----------------
ITEMS = [
    ("视频　4K 24p　15 Mb/s", 15000.0, H.NAVY),
    ("音频　5.1　640 kb/s", 640.0, H.BLUE),
    ("杜比视界 RPU　每帧 50 B", 9.6, H.ORANGE),
    ("HDR10+ 元数据　每帧 40 B", 7.7, H.TEAL),
]
ys = np.arange(len(ITEMS))[::-1]
for y, (name, val, c) in zip(ys, ITEMS):
    ax2.barh(y, val, height=0.44, color=c, alpha=0.88, edgecolor="white", lw=0.6)
    ax2.text(val * 1.4, y, f"{val:g}", fontsize=7.4, color="#40505f", va="center", ha="left")

ax2.set_xscale("log")
ax2.set_xlim(0.02, 200000)
ax2.set_yticks(list(ys))
ax2.set_yticklabels([i[0] for i in ITEMS], fontsize=7.2)
ax2.set_ylim(-1.35, len(ITEMS) - 0.4)
ax2.set_xlabel("每秒占用的码率（kb/s，对数刻度）", fontsize=9)
ax2.set_xticks([0.1, 1, 10, 100, 1000])
ax2.set_xticklabels(["0.1", "1", "10", "100", "1000"])
ax2.text(0.024, len(ITEMS) - 0.62, "(b)", fontsize=10, fontweight="bold", color=H.DARK)
ax2.text(0.024, -0.82, "HDR10 静态元数据全片只写一处\n摊到每秒不足 0.01 kb/s",
         fontsize=6.8, color=H.RED, va="center", ha="left", linespacing=1.5)

H.save(fig, 11, "f3_compat_layers")
