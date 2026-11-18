# -*- coding: utf-8 -*-
"""第 02 章 图 3：白点与色适应。

左：三个颜色从光源 A 适应到 D65 前后在色度图上的位移（Bradford 变换），
    以及几个标准白点的位置。
右：Bradford 的 LMS 增益与直接在 XYZ 上缩放得到的增益对比。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C
from matplotlib.lines import Line2D

plt = H.plt

M_BFD = np.array([[0.8951, 0.2664, -0.1614],
                  [-0.7502, 1.7135, 0.0367],
                  [0.0389, -0.0685, 1.0296]])
M_INV = np.linalg.inv(M_BFD)


def xy_to_XYZ(x, y, Y=1.0):
    return np.array([x * Y / y, Y, (1 - x - y) * Y / y])


def XYZ_to_xy(v):
    s = v.sum()
    return v[0] / s, v[1] / s


W_A = xy_to_XYZ(0.44757, 0.40745)      # 光源 A
W_D65 = xy_to_XYZ(0.31272, 0.32903)    # 光源 D65

gain_b = (M_BFD @ W_D65) / (M_BFD @ W_A)
CAT_BFD = M_INV @ np.diag(gain_b) @ M_BFD
CAT_XYZ = np.diag(W_D65 / W_A)

COLORS = [("橙红", (0.520, 0.360)),
          ("黄绿", (0.330, 0.455)),
          ("青蓝", (0.240, 0.300))]

fig = plt.figure(figsize=(7.2, 4.4))
gs = fig.add_gridspec(1, 2, width_ratios=[1.18, 1.0], wspace=0.32)

# ==================== 左：适应前后的位移 ====================
ax = fig.add_subplot(gs[0])

WPS = [("D65", 0.31272, 0.32903, "*", 13, "#f7d774"),
       ("A", 0.44757, 0.40745, "o", 8, "white"),
       ("D50", 0.34567, 0.35850, "s", 7, "white"),
       ("E", 1 / 3, 1 / 3, "D", 6.5, "white")]
for name, x0, y0, mk, ms, fc in WPS:
    ax.plot([x0], [y0], marker=mk, ms=ms, mfc=fc, mec="#111111", mew=1.1, zorder=8)

for name, (x0, y0) in COLORS:
    x1, y1 = XYZ_to_xy(CAT_BFD @ xy_to_XYZ(x0, y0))
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=H.NAVY, lw=1.6,
                                shrinkA=2, shrinkB=3, mutation_scale=11),
                zorder=6)
    ax.plot([x0], [y0], "o", ms=5.2, mfc="#2c3e50", mec="white", mew=0.9, zorder=7)
    ax.plot([x1], [y1], "o", ms=5.2, mfc="white", mec=H.NAVY, mew=1.4, zorder=7)
    mx, my = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
    dx, dy = x1 - x0, y1 - y0
    nn = np.hypot(dx, dy)
    ax.text(mx - dy / nn * 0.026, my + dx / nn * 0.026, name, fontsize=7.6,
            color=H.NAVY, ha="center", va="center", zorder=9,
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=0.6))

ax.set_xlim(0.12, 0.56)
ax.set_ylim(0.10, 0.50)
ax.set_aspect("equal")
ax.set_xlabel("色度坐标 x")
ax.set_ylabel("色度坐标 y")
ax.set_xticks([0.15, 0.25, 0.35, 0.45, 0.55])
ax.set_yticks([0.15, 0.25, 0.35, 0.45])

handles = [
    Line2D([], [], color=H.NAVY, lw=1.6, marker=">", ms=5,
           label="Bradford：A → D65"),
    Line2D([], [], marker="o", color="none", mfc="#2c3e50", mec="white", ms=5.5,
           label="适应前"),
    Line2D([], [], marker="o", color="none", mfc="white", mec=H.NAVY, mew=1.4,
           ms=5.5, label="适应后"),
    Line2D([], [], marker="*", color="none", mfc="#f7d774", mec="#111111", ms=12,
           label="D65 (0.3127, 0.3290)"),
    Line2D([], [], marker="o", color="none", mfc="white", mec="#111111", ms=7,
           label="A (0.4476, 0.4074)"),
    Line2D([], [], marker="s", color="none", mfc="white", mec="#111111", ms=6,
           label="D50 (0.3457, 0.3585)"),
    Line2D([], [], marker="D", color="none", mfc="white", mec="#111111", ms=6,
           label="E (0.3333, 0.3333)"),
]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.145),
          ncol=2, fontsize=7.2, frameon=False, columnspacing=1.4,
          handlelength=1.5, labelspacing=0.45)

# ==================== 右：增益对比 ====================
ax2 = fig.add_subplot(gs[1])
xo = np.arange(3)
bw = 0.34
xyz_gain = W_D65 / W_A
ax2.bar(xo - bw / 2, gain_b, bw, color=H.NAVY, edgecolor="#12314d", lw=0.8,
        label="Bradford（LMS 通道）")
ax2.bar(xo + bw / 2, xyz_gain, bw, color=H.ORANGE, edgecolor="#8a4a10", lw=0.8,
        label="XYZ 直接缩放")
for i in range(3):
    ax2.text(xo[i] - bw / 2, gain_b[i] + 0.05, f"{gain_b[i]:.3f}", ha="center",
             va="bottom", fontsize=7.4, color=H.NAVY)
    ax2.text(xo[i] + bw / 2, xyz_gain[i] + 0.05, f"{xyz_gain[i]:.3f}", ha="center",
             va="bottom", fontsize=7.4, color="#8a4a10")
ax2.set_xticks(xo)
ax2.set_xticklabels(["L / X", "M / Y", "S / Z"])
ax2.set_ylim(0, 3.75)
ax2.set_ylabel("适应增益（A → D65）")
ax2.grid(axis="x", visible=False)
ax2.legend(loc="upper left", fontsize=7.6, frameon=False, handlelength=1.5)
ax2.axhline(1.0, color="#8d99a6", lw=0.9, ls=(0, (4, 3)), zorder=1)

H.save(fig, 2, "f3_adaptation")
print("Bradford gains LMS:", np.round(gain_b, 4))
print("XYZ gains:", np.round(xyz_gain, 4))
print("CAT_BFD =")
print(np.round(CAT_BFD, 4))
