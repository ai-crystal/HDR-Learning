# -*- coding: utf-8 -*-
"""第 01 章 图 4：sRGB 与 BT.709 在 CIE 1931 色度图上的三角形（几乎重合，标 D65）。

要点：sRGB 与 BT.709 的三基色坐标完全相同 —— 它们其实是同一套颜色，区别只在用途与传递函数。
数据：本地 cie1931.py（CIE 1931 2° 标准观察者，5 nm）。
运行：D:/DevTools/Anaconda3/python.exe f4_srgb709.py
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import hdrfig as H
import cie1931 as C
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

SRGB = {"R": (0.640, 0.330), "G": (0.300, 0.600), "B": (0.150, 0.060)}
BT709 = {"R": (0.640, 0.330), "G": (0.300, 0.600), "B": (0.150, 0.060)}   # 与 sRGB 相同
D65 = (0.3127, 0.3290)

tri = np.array([SRGB["R"], SRGB["G"], SRGB["B"]])
tri_area = C.poly_area(tri[:, 0], tri[:, 1])
locus_area = C.locus_area()
cover = 100.0 * tri_area / locus_area
bt2020 = np.array([[0.708, 0.292], [0.170, 0.797], [0.131, 0.046]])
cover2020 = 100.0 * C.poly_area(bt2020[:, 0], bt2020[:, 1]) / locus_area

_, cx, cy = C.spectral_locus(2000)
cent = np.array([0.33, 0.33])

fig, ax = plt.subplots(figsize=(7.2, 5.0))

# ---------------- 可见颜色范围 ----------------
ax.fill(cx, cy, color="#eef2f7", zorder=0)
ax.plot(cx, cy, color="#8894a3", lw=1.5, zorder=2)
ax.plot([cx[0], cx[-1]], [cy[0], cy[-1]], color="#8894a3", lw=1.5,
        ls=(0, (2, 2)), zorder=2)

# 波长刻度（沿外法线方向摆放，避免压线）
for w in [460, 480, 500, 520, 540, 560, 580, 600, 620, 650, 700]:
    x0, y0 = C.xy_at([w])
    x0, y0 = float(x0[0]), float(y0[0])
    v = np.array([x0 - cent[0], y0 - cent[1]])
    v = v / np.hypot(*v)
    ax.plot([x0], [y0], marker=".", ms=4.0, color="#6c7784", zorder=3)
    ax.text(x0 + v[0] * 0.030, y0 + v[1] * 0.030, f"{w}", fontsize=6.6,
            color="#6c7784", ha="center", va="center")

# ---------------- 两个三角形 ----------------
ax.plot(np.append(tri[:, 0], tri[0, 0]), np.append(tri[:, 1], tri[0, 1]),
        color=H.NAVY, lw=2.6, zorder=4, solid_capstyle="round")
ax.plot(np.append(tri[:, 0], tri[0, 0]), np.append(tri[:, 1], tri[0, 1]),
        color=H.ORANGE, lw=2.0, ls=(0, (5, 3)), zorder=5)

# 基色顶点
for k, (px, py) in SRGB.items():
    ax.plot([px], [py], marker="o", ms=6, color=H.NAVY, zorder=6,
            markeredgecolor="white", markeredgewidth=1.2)
lab = {"R": (0.615, 0.292, "center"), "G": (0.313, 0.622, "left"), "B": (0.163, 0.088, "left")}
for k, (px, py) in SRGB.items():
    lx, ly, ha = lab[k]
    ax.text(lx, ly, f"{k} ({px:.3f}, {py:.3f})", fontsize=7.2, color=H.NAVY,
            fontweight="bold", ha=ha, va="center", zorder=7)

# D65 白点
ax.plot([D65[0]], [D65[1]], marker="*", ms=15, color=H.RED, zorder=7,
        markeredgecolor="white", markeredgewidth=1.0)
ax.text(D65[0] - 0.018, D65[1] + 0.030, "D65 白点\n(0.3127, 0.3290)", fontsize=7.6,
        color=H.RED, fontweight="bold", ha="center", va="bottom", zorder=7,
        linespacing=1.3)

# 紫线说明
ax.text(0.470, 0.155, "紫线（非光谱色）", fontsize=6.8, color="#7d8894",
        rotation=25, ha="center", va="bottom", zorder=6)

# 三角形外：sRGB 画不出的例子
for w, lab_, off in [(525, "525nm", (0.026, 0.026)),
                     (610, "610nm", (0.030, 0.028))]:
    x0, y0 = C.xy_at([w]); x0, y0 = float(x0[0]), float(y0[0])
    ax.plot([x0], [y0], marker="x", ms=9, color=H.PURPLE, zorder=6, mew=2.2)
    ax.text(x0 + off[0], y0 + off[1], lab_, fontsize=7.0, color=H.PURPLE,
            ha="left", va="center", fontweight="bold", zorder=7)

ax.set_xlim(-0.02, 0.82)
ax.set_ylim(-0.02, 0.92)
ax.set_aspect("equal", adjustable="box")
ax.set_xlabel("色度坐标 x", fontsize=10)
ax.set_ylabel("色度坐标 y", fontsize=10)

handles = [Line2D([], [], color=H.NAVY, lw=2.6, label="sRGB（1996）"),
           Line2D([], [], color=H.ORANGE, lw=2.0, ls=(0, (5, 3)), label="BT.709（1990）"),
           Line2D([], [], color=H.PURPLE, marker="x", ms=7, ls="none",
                  label="三角形外的纯色（525nm 绿、610nm 红）")]
ax.legend(handles=handles, loc="upper right", bbox_to_anchor=(0.995, 0.995),
          fontsize=7.8, frameon=True, framealpha=0.96, edgecolor="#cfd8e3",
          borderpad=0.6, labelspacing=0.55)

ax.set_title("sRGB 与 BT.709：两条几乎完全重合的三角形", fontsize=13,
             fontweight="bold", pad=10)

# ---------------- 图下说明条 ----------------
fig.subplots_adjust(bottom=0.215)
fig.text(0.5, 0.085,
         "基色坐标（sRGB 与 BT.709 完全相同）：R (0.640, 0.330)　G (0.300, 0.600)　"
         "B (0.150, 0.060)　白点 D65 (0.3127, 0.3290)",
         ha="center", va="center", fontsize=7.6, color="#33404f")
fig.text(0.5, 0.030,
         f"三角形约占 CIE 1931 可见色域面积的 {cover:.1f}%（BT.2020 约 {cover2020:.1f}%）"
         "—— 两者的颜色范围就是同一套，只是用途与传递函数不同",
         ha="center", va="center", fontsize=7.6, color="#33404f")

H.save(fig, 1, "f4_srgb709")
