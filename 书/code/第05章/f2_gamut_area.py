# -*- coding: utf-8 -*-
"""第 05 章 图 2：各色域覆盖面积对比（条形图，参照 CIE 1931 可见色域）。

左：三角形面积（xy 单位）与占可见色域的比例。
右：以 sRGB 为 1.0 的相对倍数。
"""
import sys
sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
sys.path.insert(0, "E:/Study/HDR-Learning/书/code/第04章")
import numpy as np
import hdrfig as H
import cie1931 as C

plt = H.plt

GAMUTS = [
    ("BT.2020", H.RED, [(0.708, 0.292), (0.170, 0.797), (0.131, 0.046)]),
    ("DCI-P3", H.ORANGE, [(0.680, 0.320), (0.265, 0.690), (0.150, 0.060)]),
    ("Adobe RGB", H.TEAL, [(0.640, 0.330), (0.210, 0.710), (0.150, 0.060)]),
    ("sRGB / BT.709", H.NAVY, [(0.640, 0.330), (0.300, 0.600), (0.150, 0.060)]),
]


def tri_area(p):
    x = np.array([q[0] for q in p])
    y = np.array([q[1] for q in p])
    return 0.5 * abs(x[0] * (y[1] - y[2]) + x[1] * (y[2] - y[0]) + x[2] * (y[0] - y[1]))


LAM, LX, LY = C.spectral_locus()
VIS = 0.5 * abs(np.dot(LX, np.roll(LY, 1)) - np.dot(LY, np.roll(LX, 1)))
AREAS = [tri_area(p) for _, _, p in GAMUTS]

fig = plt.figure(figsize=(7.2, 4.3))
gs = fig.add_gridspec(1, 2, width_ratios=[1.45, 1.0], wspace=0.40,
                      left=0.115, right=0.975, top=0.80, bottom=0.20)
ax0 = fig.add_subplot(gs[0, 0])
ax1 = fig.add_subplot(gs[0, 1])

# ---------------- 左：绝对面积条形 ----------------
names = [g[0] for g in GAMUTS][::-1]
vals = AREAS[::-1]
cols = [g[1] for g in GAMUTS][::-1]
ypos = np.arange(len(names))

ax0.barh(ypos, vals, height=0.62, color=cols, alpha=0.88,
         edgecolor="white", linewidth=1.2, zorder=3)
for y, v in zip(ypos, vals):
    ax0.text(v + 0.006, y, f"{v:.4f}", va="center", ha="left",
             fontsize=8.6, fontweight="bold", color="#2b3540", zorder=5)
    ax0.text(v + 0.006, y - 0.34, f"占可见色域 {v / VIS * 100:.1f}%",
             va="center", ha="left", fontsize=7.6, color=H.GRAY, zorder=5)

ax0.axvline(VIS, color=H.PURPLE, ls="--", lw=1.4, zorder=4)
ax0.text(0.3405, -0.45, "CIE 1931 可见色域 = 0.3342（100%）",
         rotation=90, va="bottom", ha="left", fontsize=7.6, color=H.PURPLE,
         fontweight="bold", zorder=6)
ax0.set_yticks(ypos)
ax0.set_yticklabels(names, fontsize=9.5)
ax0.set_xlim(0, 0.395)
ax0.set_ylim(-0.62, len(names) - 0.38)
ax0.set_xlabel("色域三角形面积（xy 单位）")
ax0.set_title("① 绝对值：把“能显示多少颜色”量化", fontsize=10.5, pad=8)
ax0.grid(axis="x", color="#dde3ea", lw=0.7, zorder=0)
ax0.set_axisbelow(True)
for gl in ax0.get_xgridlines():
    gl.set_zorder(0)

# ---------------- 右：相对 sRGB 倍数 ----------------
rel = np.array(AREAS) / AREAS[-1]
xs = np.arange(len(rel))
ax1.bar(xs, rel, width=0.58, color=[g[1] for g in GAMUTS], alpha=0.88,
        edgecolor="white", linewidth=1.2, zorder=3)
for x, r in zip(xs, rel):
    ax1.text(x, r + 0.05, f"{r:.2f}×", ha="center", va="bottom",
             fontsize=9.0, fontweight="bold", color="#2b3540", zorder=5)
ax1.axhline(1.0, color=H.NAVY, ls=":", lw=1.3, zorder=4)
ax1.text(3.52, 1.0, "基准 1.00", fontsize=7.6,
         color=H.NAVY, ha="left", va="center", zorder=6)
ax1.set_xticks(xs)
ax1.set_xticklabels(["BT.2020", "DCI-P3", "Adobe RGB", "sRGB"], fontsize=7.8)
ax1.set_xlim(-0.62, 4.35)
ax1.set_ylim(0, 2.28)
ax1.set_ylabel("面积倍数（相对 sRGB）")
ax1.set_title("② 相对值：以 sRGB 为 1 的倍数", fontsize=10.5, pad=8)
ax1.grid(axis="y", color="#dde3ea", lw=0.7, zorder=0)
ax1.set_axisbelow(True)
for gl in ax1.get_ygridlines():
    gl.set_zorder(0)
ax1.annotate("BT.2020 ≈ sRGB 的 1.9 倍\n≈ P3 的 1.4 倍",
             xy=(0.08, 1.89), xytext=(1.05, 2.06), fontsize=8.0, color="#2b3540",
             ha="left", va="center", zorder=8,
             arrowprops=dict(arrowstyle="->", color=H.GRAY, lw=1.0),
             bbox=dict(boxstyle="round,pad=0.28", fc="#f7f9fb", ec=H.LGRAY, lw=0.8))

fig.suptitle("各色域覆盖面积对比：BT.2020 是容器，P3 才是现实中最常见的实显水平",
             fontsize=11.5, fontweight="bold", y=0.955)
fig.text(0.5, 0.035,
         "注：面积 = 三角形在 CIE 1931 xy 坐标下的几何面积；可见色域取马蹄形（光谱轨迹 + 紫线）面积 0.3342。\n"
         "不同文献对 BT.2020 有“约 63%”“约 75%”等多种口径，取决于统计基准，比较时务必看口径。",
         ha="center", va="center", fontsize=7.4, color=H.GRAY)

H.save(fig, 5, "f2_gamut_area")
print("VIS =", round(VIS, 5), "AREAS =", [round(a, 5) for a in AREAS])
