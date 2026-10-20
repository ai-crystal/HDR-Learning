# -*- coding: utf-8 -*-
"""图 13-1　DisplayHDR 普通族 400/500/600/1000/1400：峰值亮度、黑位（对数轴）、对比度。

黑位那一列才是 HDR 观感的灵魂：从 0.4 nit 到 0.02 nit 差了 20 倍，
对应对比度从 1000:1 一路涨到约 70000:1。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np

levels = ["400", "500", "600", "1000", "1400"]
peak = np.array([400, 500, 600, 1000, 1400], dtype=float)   # nit
black = np.array([0.4, 0.2, 0.1, 0.05, 0.02], dtype=float)  # nit
contrast = peak / black
colors = [H.GRAY, H.BLUE, H.TEAL, H.ORANGE, H.RED]

fig, axes = H.plt.subplots(1, 3, figsize=(7.2, 3.7))
fig.subplots_adjust(wspace=0.46)

# ---------- (1) 峰值亮度 ----------
ax = axes[0]
bars = ax.bar(levels, peak, color=colors, edgecolor="white", linewidth=0.8, width=0.66)
for b, v in zip(bars, peak):
    ax.text(b.get_x() + b.get_width() / 2, v + 25, f"{v:.0f}", ha="center",
            va="bottom", fontsize=9, fontweight="bold", color="#333333")
ax.axhline(400, color=H.GOLD, ls="--", lw=1.2)
ax.text(0.03, 0.955, "- - 400 nit（入门门槛）", transform=ax.transAxes,
        ha="left", va="top", fontsize=8, color=H.GOLD, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
ax.set_title("峰值亮度 (nit)", pad=8)
ax.set_ylabel("亮度 (nit)")
ax.set_ylim(0, 1650)
ax.grid(axis="x", visible=False)

# ---------- (2) 黑位（对数轴） ----------
ax = axes[1]
bars = ax.bar(levels, black, color=colors, edgecolor="white", linewidth=0.8, width=0.66)
for b, v in zip(bars, black):
    ax.text(b.get_x() + b.get_width() / 2, v * 1.18, f"{v:g}", ha="center",
            va="bottom", fontsize=8.5, fontweight="bold", color="#333333",
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
ax.set_yscale("log")
ax.set_ylim(0.01, 1.6)
ax.set_yticks([0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 1.0])
ax.set_yticklabels(["0.01", "0.02", "0.05", "0.1", "0.2", "0.4", "1"])
ax.minorticks_off()
ax.set_title("黑位 (nit，对数轴)", pad=8)
ax.set_ylabel("最暗亮度 (nit，对数)")
ax.grid(axis="x", visible=False)
ax.annotate("黑位降低 20 倍\n（暗场更干净）",
            xy=(4.0, 0.022), xytext=(1.55, 0.42),
            fontsize=8, color=H.NAVY, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=H.NAVY, lw=1.1,
                            connectionstyle="arc3,rad=-0.25"))

# ---------- (3) 对比度（对数轴） ----------
ax = axes[2]
bars = ax.bar(levels, contrast, color=colors, edgecolor="white", linewidth=0.8, width=0.66)
labels = ["1000:1", "2500:1", "6000:1", "20000:1", "70000:1"]
for b, v, t in zip(bars, contrast, labels):
    ax.text(b.get_x() + b.get_width() / 2, v * 1.16, t, ha="center",
            va="bottom", fontsize=8.2, fontweight="bold", color="#333333")
ax.set_yscale("log")
ax.set_ylim(500, 420000)
ax.set_yticks([1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000])
ax.set_yticklabels(["1000", "2000", "5000", "1万", "2万", "5万", "10万", "20万"])
ax.minorticks_off()
ax.set_title("对比度 = 峰值 ÷ 黑位", pad=8)
ax.set_ylabel("对比度（倍，对数）")
ax.grid(axis="x", visible=False)

for ax in axes:
    ax.set_xlabel("DisplayHDR 等级")
    ax.tick_params(axis="x", length=0)

fig.suptitle("DisplayHDR 普通族：等级越高，黑位越低、对比度越高", fontsize=13,
             fontweight="bold", y=1.05)
fig.text(0.5, -0.11,
         "注：数值为 VESA 规范量级/约值，具体以官方最新版为准；"
         "分区调光在 500 及以上为要求项，400 不要求。",
         ha="center", fontsize=8, color=H.GRAY)

H.save(fig, 13, "f1_levels")
