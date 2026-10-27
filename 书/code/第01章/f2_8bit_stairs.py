# -*- coding: utf-8 -*-
"""第 01 章 图 2：8bit 与 10bit 的灰度量化"台阶"（色带 banding 的由来）。

上两行：6/8/10/12bit 的整段灰度，以及最暗 12% 的放大（色带在暗部最明显）。
下：暗部台阶放大曲线 —— 8bit 一级跳多少 nit、10bit 细 4 倍。
运行：D:/DevTools/Anaconda3/python.exe f2_8bit_stairs.py
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import numpy as np
import hdrfig as H
import matplotlib.pyplot as plt

BITS = [(6, "6bit · 64 级", "#7f8c8d", "#22314a", 0.9),
        (8, "8bit · 256 级（SDR 标准）", H.RED, H.RED, 2.2),
        (10, "10bit · 1024 级（HDR 起步）", H.GREEN, H.GREEN, 2.2),
        (12, "12bit · 4096 级", "#7f8c8d", "#22314a", 0.9)]

CROP = 0.12     # 暗部放大比例

fig = plt.figure(figsize=(7.2, 5.8))
gs = fig.add_gridspec(3, 4, height_ratios=[0.85, 0.85, 2.2], hspace=0.95, wspace=0.075,
                      left=0.085, right=0.985, top=0.895, bottom=0.075)


def draw_strip(ax, bit, edge, lw, crop=False):
    img = H.banding_gray(bit, width=1024, height=110)
    if crop:
        w = int(img.shape[1] * CROP)
        img = img[:, :w]
        extent = [0, CROP, 0, 1]
    else:
        extent = [0, 1, 0, 1]
    ax.imshow(img, cmap="gray", vmin=0, vmax=255, aspect="auto",
              interpolation="nearest", extent=extent)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(True); sp.set_color(edge); sp.set_linewidth(lw)


for j, (bit, title, edge, tcolor, lw) in enumerate(BITS):
    ax = fig.add_subplot(gs[0, j])
    draw_strip(ax, bit, edge, lw)
    ax.set_title(title, fontsize=8.4, pad=3.5, color=tcolor, fontweight="bold")
    ax2 = fig.add_subplot(gs[1, j])
    draw_strip(ax2, bit, edge, lw, crop=True)

fig.text(0.005, 0.685, "整段灰度", rotation=90, ha="left", va="center",
         fontsize=8.0, color="#33404f", fontweight="bold")
fig.text(0.005, 0.545, f"暗部 {int(CROP * 100)}% 放大", rotation=90, ha="left",
         va="center", fontsize=8.0, color=H.RED, fontweight="bold")

# ---------------- 暗部台阶放大曲线 ----------------
ax = fig.add_subplot(gs[2, :])
t = np.linspace(0, 1, 8000)
span = 0.08                      # 只取全码值最暗的 8%
peak = 100.0                     # 假定峰值白 = 100 nit
first_step = {}
for bit, color, lw, ls, z in [(8, H.RED, 2.2, "-", 4),
                              (10, H.GREEN, 2.0, "-", 3),
                              (12, H.GRAY, 1.4, (0, (5, 2)), 2)]:
    levels = 2 ** bit - 1
    code = np.floor(t * span * levels) / levels
    ax.plot(t, H.srgb_eotf(code) * peak, color=color, lw=lw, ls=ls, zorder=z,
            label=f"{bit}bit：{2 ** bit} 级")
    first_step[bit] = float(H.srgb_eotf(1.0 / levels) * peak)

ax.set_xlim(0, 0.30)
ax.set_ylim(0, 0.62)
ax.set_xlabel("暗部渐变的位置（0 → 全码值的 8%，只取最暗的一小段）", fontsize=9.5)
ax.set_ylabel("输出亮度（nit）\n峰值白按 100 nit 计", fontsize=9.5)
ax.grid(color="#dde3ea", lw=0.7)
ax.set_axisbelow(True)

ax.annotate(f"8bit 第 1 级就跳 {first_step[8]:.3f} nit",
            xy=(1.0 / 255 / span, 0.012), xytext=(0.075, 0.415),
            fontsize=8.4, color=H.RED, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.3),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=H.RED, lw=0.8, alpha=0.95))
ax.annotate(f"10bit 第 1 级只跳 {first_step[10]:.3f} nit（细 4 倍）",
            xy=(1.0 / 1023 / span, 0.004), xytext=(0.128, 0.165),
            fontsize=8.4, color=H.GREEN, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=H.GREEN, lw=1.3),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=H.GREEN, lw=0.8, alpha=0.95))

n8, n10 = span * 255, span * 1023
ax.text(0.30, 0.585,
        f"同一段暗部：8bit 只有约 {n8:.0f} 级可用，10bit 有约 {n10:.0f} 级。人眼对暗部最敏感，\n"
        f"所以“色带”总是先出现在暗部 —— 这就是 HDR 坚持 10bit 起步的直接原因。",
        ha="right", va="top", fontsize=8.2, color="#22314a",
        bbox=dict(boxstyle="round,pad=0.35", fc="#f5f8fb", ec="#dbe2ea", lw=0.8))
ax.legend(loc="upper left", fontsize=8.2, frameon=False)

fig.suptitle("位深决定“台阶”粗细：8bit 的 256 级 vs 10bit 的 1024 级",
             fontsize=13, fontweight="bold", y=0.965)

H.save(fig, 1, "f2_8bit_stairs")
