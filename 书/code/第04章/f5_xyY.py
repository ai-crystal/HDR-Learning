# -*- coding: utf-8 -*-
"""第 04 章 图 5：XYZ → 色度坐标 (x, y) 与亮度 Y 的拆解。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import hdrfig as H
import cie1931 as C

plt = H.plt
from matplotlib.patches import Rectangle, FancyArrowPatch

fig = plt.figure(figsize=(7.2, 4.7))
gs = fig.add_gridspec(2, 2, width_ratios=[1.22, 1.0], height_ratios=[0.95, 1.15],
                      wspace=0.36, hspace=0.52)

# ---------------- 数据：一个橙红色（X:Y:Z = 1.00 : 0.72 : 0.28） ----------------
XV, YV, ZV = 1.00, 0.72, 0.28
TOT = XV + YV + ZV
cx, cy = XV / TOT, YV / TOT            # 0.50, 0.36
SWATCH = C.xy_to_srgb01(cx, cy, 1.0)

# ==================== 左：拆解流程 ====================
ax = fig.add_subplot(gs[:, 0])
ax.set_title("一个颜色 = 三个数，再拆成“种类 + 亮度”", pad=6)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
for s in ax.spines.values():
    s.set_visible(False)

# 色块
ax.add_patch(Rectangle((0.40, 0.925), 0.20, 0.070, facecolor=SWATCH,
                       edgecolor="#4a5666", lw=0.9))
ax.text(0.38, 0.960, "画面的颜色", fontsize=8.6, ha="right", va="center",
        color="#2c3e50", fontweight="bold")

# 三个三刺激值柱
scale = 0.42
bars = [("X", XV, H.NAVY, 0.790), ("Y", YV, H.GREEN, 0.675), ("Z", ZV, H.RED, 0.560)]
for name, val, col, ycor in bars:
    w = val / XV * scale
    ax.add_patch(Rectangle((0.40, ycor - 0.033), w, 0.066, facecolor=col, alpha=0.87,
                           edgecolor="none"))
    ax.text(0.375, ycor, name, fontsize=9.4, color=col, fontweight="bold",
            ha="right", va="center")
    ax.text(0.40 + w + 0.013, ycor, f"{val:.2f}", fontsize=8.6, color=col,
            va="center", fontweight="bold")
ax.text(0.40, 0.872, "三刺激值 X、Y、Z", fontsize=8.4, color="#2c3e50", ha="left",
        va="center", fontweight="bold")

# 归一化箭头
ax.annotate("", xy=(0.30, 0.445), xytext=(0.30, 0.500),
            arrowprops=dict(arrowstyle="-|>", color=H.GRAY, lw=1.6))
ax.text(0.33, 0.472, f"全部除以 (X+Y+Z) = {TOT:.2f}", fontsize=8.2, color=H.GRAY,
        ha="left", va="center")

# 归一化后的比例条（x + y + z = 1）
x0, wtot = 0.40, 0.42
segs = [("x", cx, H.NAVY), ("y", cy, H.ORANGE), ("z", 1 - cx - cy, H.GOLD)]
cur = x0
for name, frac, col in segs:
    w = frac * wtot
    ax.add_patch(Rectangle((cur, 0.345), w, 0.080, facecolor=col, alpha=0.88,
                           edgecolor="white", lw=1.2))
    ax.text(cur + w / 2, 0.385, name, fontsize=9.0, color="white", fontweight="bold",
            ha="center", va="center")
    ax.text(cur + w / 2, 0.312, f"{frac:.2f}", fontsize=8.0, color=col,
            ha="center", va="center", fontweight="bold")
    cur += w
ax.text(0.375, 0.385, "比例", fontsize=8.6, color="#2c3e50", ha="right",
        va="center", fontweight="bold")
ax.text(0.40, 0.248, "x + y + z = 1：只有两个自由度", fontsize=8.0,
        color="#2c3e50", ha="left", va="center")

# 结论两框
ax.add_patch(Rectangle((0.12, 0.045), 0.42, 0.120, facecolor="#eef4fa",
                       edgecolor=H.NAVY, lw=1.0))
ax.text(0.33, 0.105, f"① (x, y) = ({cx:.2f}, {cy:.2f})\n决定“是什么颜色”", fontsize=7.6,
        color=H.NAVY, ha="center", va="center", fontweight="bold")
ax.add_patch(Rectangle((0.57, 0.045), 0.42, 0.120, facecolor="#eefaf1",
                       edgecolor=H.GREEN, lw=1.0))
ax.text(0.78, 0.105, f"② Y = {YV:.2f}\n决定“有多亮”", fontsize=7.6,
        color=H.GREEN, ha="center", va="center", fontweight="bold")

# 两条引导箭头
ax.annotate("", xy=(0.30, 0.172), xytext=(0.32, 0.300),
            arrowprops=dict(arrowstyle="-|>", color=H.NAVY, lw=1.3))
ax.annotate("", xy=(0.78, 0.175), xytext=(0.712, 0.660),
            arrowprops=dict(arrowstyle="-|>", color=H.GREEN, lw=1.3,
                            connectionstyle="arc3,rad=-0.25", linestyle="--"))
ax.text(0.905, 0.560, "Y 绕过\n归一化", fontsize=7.4, color=H.GREEN, ha="center",
        va="center", fontweight="bold")

# ==================== 右上：只看 x、y = 颜色种类 ====================
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_title("① 只看 (x, y)：色度", pad=4)
lam, sx, sy = C.spectral_locus()
ax2.plot(sx, sy, color=H.GRAY, lw=1.6)
ax2.plot([sx[0], sx[-1]], [sy[0], sy[-1]], color=H.GRAY, lw=1.2, ls=(0, (4, 3)))
mx, my = C.WHITE_POINTS["D65"]
ax2.plot([mx], [my], marker="o", ms=7, mfc="white", mec="#111111", mew=1.6)
ax2.text(mx - 0.02, my - 0.085, "D65", fontsize=7.4, ha="center", color="#111111",
         fontweight="bold")
ax2.plot([cx], [cy], marker="o", ms=7.5, mfc=SWATCH, mec="white", mew=1.3)
ax2.annotate(f"({cx:.2f}, {cy:.2f})", xy=(cx, cy), xytext=(cx + 0.075, cy + 0.17),
             fontsize=7.8, color=H.ORANGE, fontweight="bold", ha="center",
             arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=1.0))
ax2.set_xlim(-0.04, 0.88)
ax2.set_ylim(-0.04, 0.94)
ax2.set_aspect("equal")
ax2.set_xticks([]); ax2.set_yticks([])
ax2.grid(False)
for s in ax2.spines.values():
    s.set_visible(False)
ax2.text(0.015, 0.035, "点在马蹄里的位置\n= 色调 + 饱和度", fontsize=7.2, color=H.GRAY,
         ha="left", va="bottom")

# ==================== 右下：Y 决定有多亮 ====================
ax3 = fig.add_subplot(gs[1, 1])
ax3.set_title("② Y 从 0 到 1：颜色种类不变，只是变亮", pad=4)

levels = np.linspace(0.004, 1.0, 420)
base = np.clip(np.array(C.xyz_to_linear_srgb(*C.xy_to_xyz(cx, cy, 1.0))), 0, None)
base = base / base.max()
lin = np.clip(base[None, :] * levels[:, None], 0, 1)
a_ = 0.0031308
enc = np.where(lin <= a_, 12.92 * lin, 1.055 * np.power(lin, 1 / 2.4) - 0.055)
ax3.imshow(enc[:, None, :], extent=[-0.55, 0.55, 0, 1.0], aspect="auto",
           origin="lower", interpolation="bicubic")
for yv, tag in ((0.02, "0.02"), (0.10, "0.10"), (0.5, "0.50"), (1.0, "1.00")):
    ax3.plot([-0.55, 0.55], [yv, yv], color="white", lw=0.7, alpha=0.75)
    ax3.text(0.58, yv, tag, fontsize=7.0, color=H.GRAY, va="center")
ax3.set_xlim(-0.58, 1.05)
ax3.set_ylim(-0.02, 1.08)
ax3.set_xticks([])
ax3.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax3.set_ylabel("Y（相对亮度）", fontsize=9)
ax3.grid(False)
ax3.tick_params(axis="y", labelsize=7.5)
for s in ("top", "right", "bottom"):
    ax3.spines[s].set_visible(False)
ax3.text(1.02, 0.72, "真实 HDR 里\nY 还能远大于 1", fontsize=7.6, color=H.GREEN,
         ha="right", va="center", fontweight="bold",
         bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=0.6))

H.save(fig, 4, "f5_xyY")
