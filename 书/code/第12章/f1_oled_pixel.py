# -*- coding: utf-8 -*-
"""第12章 f1：OLED 每像素自发光、可完全熄灭示意。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

fig = plt.figure(figsize=(7.2, 5.2))
gs = fig.add_gridspec(2, 2, height_ratios=[1.25, 1.0], hspace=0.42, wspace=0.28)

# ---------------- 上：OLED 像素剖面，每颗子像素独立驱动 ----------------
ax = fig.add_subplot(gs[0, :])
ax.grid(False)
ax.set_xlim(0, 12.0); ax.set_ylim(-1.1, 5.0); ax.axis("off")

X0, W_STACK = 1.50, 9.4
# 基底/驱动电路
ax.add_patch(Rectangle((X0, 0.35), W_STACK, 0.55, fc="#eef2f6", ec="#4a5666", lw=0.9))
ax.text(X0 + W_STACK / 2, 0.62, "玻璃基板 + 像素驱动电路（TFT）", ha="center", va="center",
        fontsize=8.2, color="#4a5666")
# 阳极
ax.add_patch(Rectangle((X0, 0.9), W_STACK, 0.28, fc=H.GRAY, ec="#4a5666", lw=0.8))
ax.text(X0 + 0.18, 1.04, "阳极", fontsize=7.6, color="white", va="center")
# 有机发光层：4 个子像素，第 3 个断电
xs = [2.05, 4.25, 6.45, 8.65]
width = 1.7
on = [True, True, False, True]
vals = [820, 60, 0, 1000]
for x, o, v in zip(xs, on, vals):
    fc = ("#f6c344" if v > 500 else "#f0dfae") if o else "#3a4351"
    ec = "#c8a24a" if o else "#2b323c"
    ax.add_patch(Rectangle((x, 1.18), width, 0.85, fc=fc, ec=ec, lw=1.0))
    ax.text(x + width / 2, 1.60, "有机发光层", ha="center", va="center", fontsize=7.0,
            color="#5a4a10" if o else "#cfd6de")
    ax.text(x + width / 2, -0.30, f"{v} nit", ha="center", va="center", fontsize=9.0,
            color=H.RED if v else H.NAVY, fontweight="bold")
    ax.text(x + width / 2, -0.80, f"子像素 {on[:0] or ''}{['R','G','B','W'][xs.index(x)]}",
            ha="center", va="center", fontsize=7.4, color=H.GRAY)
# 阴极（薄半透明电极）
ax.add_patch(Rectangle((X0, 2.03), W_STACK, 0.22, fc="#bfc9d4", ec="#4a5666", lw=0.8))
ax.text(X0 + W_STACK + 0.15, 2.14, "阴极", fontsize=7.6, color="#4a5666", va="center")
ax.text(X0 + W_STACK + 0.15, 1.04, "阳极", fontsize=7.6, color="#4a5666", va="center")

# 出光箭头
for x, o, v in zip(xs, on, vals):
    cx = x + width / 2
    if o:
        c = "#f2b632" if v > 500 else "#e8d9a8"
        for dx in (-0.5, 0.0, 0.5):
            ax.annotate("", xy=(cx + dx, 3.22), xytext=(cx + dx, 2.32),
                        arrowprops=dict(arrowstyle="-|>", color=c, lw=2.4))
        ax.add_patch(Circle((cx, 2.85), 0.75, fc=c, ec="none", alpha=0.14))
    else:
        ax.text(cx, 2.78, "断电\n0 A", ha="center", va="center", fontsize=8.0,
                color=H.NAVY, fontweight="bold")

# 中文标注
ax.text(X0 + W_STACK / 2, 4.55, "每个子像素自己发光：通电即亮，断电即黑",
        ha="center", fontsize=10.5, color=H.NAVY, fontweight="bold")
ax.text(6.2, 4.05, "不需要背光 → 没有\"背光漏光\"这回事", fontsize=8.6, color=H.ORANGE, ha="center")
ax.text(6.2, 3.62, "第 3 颗子像素电流 = 0 A → 亮度 0 nit（真黑）", fontsize=8.6, color=H.RED, ha="center")
ax.text(11.9, 4.85, "OLED 像素剖面", fontsize=9.0, color=H.GRAY, ha="right", fontweight="bold")
ax.annotate("", xy=(1.15, 1.18), xytext=(1.15, 0.35),
            arrowprops=dict(arrowstyle="-|>", color=H.TEAL, lw=1.6))
ax.text(0.85, 0.78, "逐颗独立供电", ha="center", va="center", rotation=90,
        fontsize=8.2, color=H.TEAL, fontweight="bold")

# ---------------- 左下：像素网格，每格独立取值（含 0） ----------------
ax2 = fig.add_subplot(gs[1, 0])
ax2.grid(False)
vals_grid = np.array([
    [0, 0, 12, 0, 0, 60],
    [0, 900, 8, 0, 480, 0],
    [0, 15, 0, 1000, 20, 0],
    [0, 0, 240, 0, 0, 95],
], dtype=float)
img = np.clip(vals_grid / 1000.0, 0, 1) ** 0.45
ax2.imshow(img, cmap="gray", vmin=0, vmax=1, extent=(0, 6, 0, 4))
for i in range(1, 6):
    ax2.plot([i, i], [0, 4], color="#9aa6b3", lw=0.6)
for j in range(1, 4):
    ax2.plot([0, 6], [j, j], color="#9aa6b3", lw=0.6)
for r in range(4):
    for c in range(6):
        v = int(vals_grid[r, c])
        ax2.text(c + 0.5, 3.5 - r, f"{v}", ha="center", va="center", fontsize=7.4,
                 color="white" if img[r, c] > 0.45 else "#7d8896")
ax2.set_xticks([]); ax2.set_yticks([])
ax2.set_title("像素级独立取值（nit）", fontsize=10, pad=4)
ax2.text(3.0, -1.05, "同一屏上，有的像素 0 nit、有的 1000 nit，互不影响 → 像素级控光",
         ha="center", fontsize=7.4, color=H.GRAY)

# ---------------- 右下：亮度分布条 ----------------
ax3 = fig.add_subplot(gs[1, 1])
labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
vals_bar = [0, 8, 0, 120, 480, 900, 1000, 0]
cols = [H.NAVY if v == 0 else (H.ORANGE if v < 300 else H.RED) for v in vals_bar]
b = ax3.bar(labels, vals_bar, color=cols, edgecolor="#4a5666", lw=0.6)
for rect, v in zip(b, vals_bar):
    ax3.text(rect.get_x() + rect.get_width() / 2, max(v, 0) + 30, f"{v}",
             ha="center", fontsize=7.6, color=H.NAVY if v == 0 else H.RED)
ax3.set_ylim(-15, 1200)
ax3.set_ylabel("像素亮度 (nit)")
ax3.set_xlabel("屏幕上的 8 个像素")
ax3.set_title("亮度可以真的是 0", fontsize=10, pad=4)
ax3.annotate("0 nit = 彻底熄灭", xy=(0.0, 4), xytext=(0.30, 430),
             fontsize=7.8, color=H.NAVY, fontweight="bold",
             arrowprops=dict(arrowstyle="-|>", color=H.NAVY, lw=1.2))
ax3.grid(axis="x", visible=False)

fig.suptitle("OLED：每个像素都是一盏能关掉的小灯", fontsize=14, fontweight="bold", color=H.NAVY, y=0.99)
H.save(fig, 12, "f1_oled_pixel")
