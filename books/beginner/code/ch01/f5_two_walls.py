# -*- coding: utf-8 -*-
"""第 01 章 图 5：SDR 的"两道墙" —— 亮度墙（≈100 nit）与色域墙（sRGB / BT.709）。

左：超过 100 nit 的一切在 SDR 里都被压成同一个"白"。
右：sRGB 三角形之外的颜色（BT.2020 里有一大堆）画不出来。
运行：D:/DevTools/Anaconda3/python.exe f5_two_walls.py
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import hdrfig as H
import cie1931 as C
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

fig = plt.figure(figsize=(7.2, 4.8))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.05], wspace=0.24,
                      left=0.075, right=0.985, top=0.855, bottom=0.245)

# ================= 左：亮度墙 =================
ax = fig.add_subplot(gs[0, 0])
ax.set_yscale("log")
ax.set_ylim(0.008, 60000)
names = ["暗夜\n街道", "烛光", "室内\n白纸", "阴天\n室外", "阳光下\n白墙", "窗边\n高光"]
vals = [1e-2, 1.0, 100.0, 1000.0, 5000.0, 20000.0]
WALL = 100.0
xs = np.arange(len(vals))

for i, v in enumerate(vals):
    bottom = 0.008
    ax.bar(i, min(v, WALL) - bottom, bottom=bottom, width=0.56, color=H.NAVY,
           edgecolor="#16375a", lw=0.8, zorder=3)
    if v > WALL:
        ax.bar(i, v - WALL, bottom=WALL, width=0.56, color=H.RED, alpha=0.16,
               edgecolor=H.RED, lw=0.9, hatch="///", zorder=2)

ax.axhline(WALL, color=H.RED, lw=2.2, ls=(0, (5, 3)), zorder=5)
ax.text(5.42, WALL * 1.4, "SDR 亮度墙 ≈ 100 nit", ha="right", va="bottom",
        fontsize=8.6, color=H.RED, fontweight="bold", zorder=6,
        bbox=dict(boxstyle="round,pad=0.22", fc="white", ec=H.RED, lw=0.8, alpha=0.95))
ax.text(0.03, 0.965, "斜纹 = 现实中存在、\nSDR 却画不出的高光\n（≥1000 nit → 只能当“白”）",
        transform=ax.transAxes, ha="left", va="top", fontsize=7.2,
        color=H.RED, linespacing=1.45, zorder=6,
        bbox=dict(boxstyle="round,pad=0.32", fc="#fdf1ee", ec="#f0c8c0", lw=0.8))

ax.set_xticks(xs)
ax.set_xticklabels(names, fontsize=7.6)
ax.set_ylabel("亮度（nit，对数刻度）", fontsize=9.5)
ax.set_yticks([0.01, 0.1, 1, 10, 100, 1000, 10000])
ax.set_yticklabels(["0.01", "0.1", "1", "10", "100", "1000", "10000"], fontsize=8.2)
ax.set_axisbelow(True)
ax.set_title("墙一：亮度锁死 ≈ 100 nit", fontsize=10.5, fontweight="bold",
             color=H.NAVY, pad=7)

# ================= 右：色域墙 =================
ax2 = fig.add_subplot(gs[0, 1])
_, cx, cy = C.spectral_locus(2000)
ax2.fill(cx, cy, color="#eef2f7", zorder=0)
ax2.plot(cx, cy, color="#8894a3", lw=1.4, zorder=2)
ax2.plot([cx[0], cx[-1]], [cy[0], cy[-1]], color="#8894a3", lw=1.4,
         ls=(0, (2, 2)), zorder=2)

sRGB = np.array([[0.640, 0.330], [0.300, 0.600], [0.150, 0.060]])
BT2020 = np.array([[0.708, 0.292], [0.170, 0.797], [0.131, 0.046]])
for poly, color, ls, lw, z in [(BT2020, H.PURPLE, (0, (5, 3)), 1.8, 3),
                               (sRGB, H.NAVY, "-", 2.4, 4)]:
    ax2.plot(np.append(poly[:, 0], poly[0, 0]), np.append(poly[:, 1], poly[0, 1]),
             color=color, lw=lw, ls=ls, zorder=z)

ax2.plot([0.3127], [0.3290], marker="*", ms=13, color=H.RED, zorder=6,
         markeredgecolor="white", markeredgewidth=1.0)
ax2.text(0.335, 0.343, "D65", fontsize=7.6, color=H.RED, fontweight="bold", zorder=6)

ax2.text(0.42, 0.885, "sRGB / BT.709\n三角形之外：\n鲜艳青、深绿、纯红\n统统画不出",
         ha="left", va="top", fontsize=7.2, color=H.NAVY, linespacing=1.45, zorder=6,
         bbox=dict(boxstyle="round,pad=0.32", fc="white", ec=H.NAVY, lw=0.8, alpha=0.94))
ax2.text(0.030, 0.902, "BT.2020\n（HDR 的容器）", ha="left", va="top", fontsize=7.4,
         color=H.PURPLE, fontweight="bold", linespacing=1.35, zorder=6,
         bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=H.PURPLE, lw=0.8, alpha=0.94))

ax2.set_xlim(-0.02, 0.82)
ax2.set_ylim(-0.02, 0.92)
ax2.set_aspect("equal", adjustable="box")
ax2.set_xlabel("色度 x", fontsize=9.5)
ax2.set_ylabel("色度 y", fontsize=9.5)
ax2.tick_params(labelsize=8.0)
ax2.set_title("墙二：色域锁死 sRGB / BT.709", fontsize=10.5, fontweight="bold",
              color=H.NAVY, pad=7)

handles = [Line2D([], [], color=H.NAVY, lw=2.4, label="sRGB / BT.709"),
           Line2D([], [], color=H.PURPLE, lw=1.8, ls=(0, (5, 3)), label="BT.2020（HDR 目标）")]
ax2.legend(handles=handles, loc="lower right", fontsize=7.2, frameon=True,
           framealpha=0.95, edgecolor="#cfd8e3", borderpad=0.5)

fig.text(0.5, 0.030, "SDR 的两道墙：亮度锁死在 ≈100 nit　｜　色域锁死在 sRGB / BT.709　"
                     "—— HDR 要同时拆掉这两道墙",
         ha="center", va="center", fontsize=8.6, color=H.RED, fontweight="bold",
         bbox=dict(boxstyle="round,pad=0.40", fc="#fdf1ee", ec=H.RED, lw=1.0))

fig.suptitle("SDR 的两道墙", fontsize=13, fontweight="bold", y=0.955)

H.save(fig, 1, "f5_two_walls")
