# -*- coding: utf-8 -*-
"""第 01 章 图 1：SDR 与 HDR 的亮度范围对比（对数横轴 0.001–10000 nit）。

要点：SDR 把参考白锁在约 100 nit —— 这就是"第一道墙"。
运行：D:/DevTools/Anaconda3/python.exe f1_luminance_range.py
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import numpy as np
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

fig, ax = plt.subplots(figsize=(7.2, 4.8))
ax.set_xscale("log")
ax.set_xlim(1e-3, 1e4)
ax.set_ylim(2.0, 10.4)
ax.set_yticks([])
for sp in ("left", "right", "top"):
    ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color("#4a5666")
ax.grid(axis="x", color="#dde3ea", lw=0.7)
ax.set_axisbelow(True)

ax.set_xticks([1e-3, 1e-2, 1e-1, 1, 10, 100, 1000, 10000])
ax.set_xticklabels(["0.001", "0.01", "0.1", "1", "10", "100", "1000", "10000"])
ax.set_xlabel(r"亮度 L（nit，对数刻度）        1 nit = 1 cd/m$^2$", fontsize=10)

# ---------------- 现实世界锚点 ----------------
scenes = [(0.01, "暗夜街道"), (0.1, "月光"), (1, "烛光"),
          (100, "室内白纸"), (1000, "阴天室外"), (5000, "阳光下白墙")]
for x, name in scenes:
    ax.plot([x, x], [8.35, 9.12], color=H.GRAY, lw=0.9, ls=(0, (3, 2)), zorder=2)
    ax.plot([x], [9.12], marker="v", ms=4.5, color=H.GRAY, zorder=3)
    ax.text(x, 9.20, name, rotation=42, ha="left", va="bottom",
            fontsize=7.6, color="#44515f", rotation_mode="anchor")
ax.text(1.25e-3, 8.75, "现实世界的\n典型亮度", ha="left", va="center",
        fontsize=8.2, color=H.GRAY, linespacing=1.4)

# ---------------- SDR 亮度条 ----------------
ax.add_patch(Rectangle((0.01, 6.90), 100 - 0.01, 0.80, facecolor=H.NAVY,
                       edgecolor="#16375a", lw=1.0, zorder=4))
ax.add_patch(Rectangle((100, 6.90), 1e4 - 100, 0.80, facecolor=H.RED, alpha=0.10,
                       edgecolor=H.RED, lw=0.8, hatch="///", zorder=3))
ax.text(1.3e3, 7.30, "SDR 画不出的高光：一律被压成同一个“白”", ha="center",
        va="center", fontsize=8.2, color=H.RED, fontweight="bold", zorder=6,
        bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="none", alpha=0.85))
ax.text(1.25e-3, 6.50, "SDR：参考白 ≈ 100 nit（黑位 ~0.1 nit，动态范围 ≈ 1000:1）",
        ha="left", va="center", fontsize=8.6, color=H.NAVY, fontweight="bold")

# ---------------- HDR 亮度条 ----------------
ax.add_patch(Rectangle((1e-3, 5.35), 1000 - 1e-3, 0.80, facecolor=H.ORANGE,
                       edgecolor="#b8620f", lw=1.0, zorder=4))
ax.add_patch(Rectangle((1000, 5.35), 1e4 - 1000, 0.80, facecolor=H.ORANGE,
                       alpha=0.28, edgecolor=H.ORANGE, lw=1.0, ls=(0, (4, 2)), zorder=4))
ax.text(3.2e3, 5.75, "PQ 理论峰值 10000 nit", ha="center", va="center",
        fontsize=7.2, color="#8a4a08")
ax.text(1.25e-3, 4.95, r"HDR：峰值 1000–10000 nit，黑位可低到 0.001 nit 以下（动态范围 $\approx$ $10^6$:1）",
        ha="left", va="center", fontsize=8.6, color="#b8620f", fontweight="bold")

# ---------------- 亮度墙 ----------------
ax.plot([100, 100], [2.35, 9.10], color=H.RED, lw=2.2, ls=(0, (5, 3)), zorder=5)
ax.text(120, 8.72, "SDR 亮度墙 ≈ 100 nit", ha="left", va="center",
        fontsize=9.2, color=H.RED, fontweight="bold", zorder=8,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=H.RED, lw=0.9, alpha=0.95))
ax.annotate("", xy=(102, 8.72), xytext=(112, 8.72),
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.4), zorder=8)
# HDR 越过墙的箭头
ax.annotate("", xy=(150, 6.45), xytext=(900, 6.45),
            arrowprops=dict(arrowstyle="->", color="#b8620f", lw=1.6), zorder=7)
ax.text(1000, 6.45, "HDR 越过这堵墙", ha="left", va="center", fontsize=8.0,
        color="#b8620f", fontweight="bold", zorder=7)

# ---------------- 底部结论 ----------------
ax.text(1.25e-3, 3.72, "现实世界：夜路 ≈ 0.01 nit，室内白纸 ≈ 100 nit，阳光下白墙 ≈ 5000 nit，直视太阳 > 100 000 nit",
        ha="left", va="center", fontsize=8.0, color="#33404f",
        bbox=dict(boxstyle="round,pad=0.3", fc="#f5f8fb", ec="#dbe2ea", lw=0.8))  # noqa
ax.text(1.25e-3, 2.78, "SDR 只能表现到 ≈ 100 nit → 白墙、太阳、金属反光统统被压成同一个“白”",
        ha="left", va="center", fontsize=8.0, color=H.RED,
        bbox=dict(boxstyle="round,pad=0.3", fc="#fdf1ee", ec="#f0c8c0", lw=0.8))

handles = [Patch(fc=H.NAVY, ec="#16375a", label="SDR 可表现范围"),
           Patch(fc=H.ORANGE, ec="#b8620f", label="HDR 可表现范围"),
           Patch(fc=H.ORANGE, alpha=0.28, ec=H.ORANGE, ls=(0, (4, 2)), label="HDR 理论高光区"),
           Patch(fc=H.RED, alpha=0.12, ec=H.RED, hatch="///", label="SDR 被削平的高光"),
           Line2D([], [], color=H.GRAY, ls=(0, (3, 2)), marker="v", ms=4, label="现实亮度锚点")]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.155),
          ncol=3, fontsize=7.8, frameon=False, handlelength=1.6, columnspacing=1.6)

ax.set_title("SDR 与 HDR 的亮度范围：从 0.001 nit 到 10000 nit", fontsize=13,
             fontweight="bold", pad=10)

H.save(fig, 1, "f1_luminance_range")
