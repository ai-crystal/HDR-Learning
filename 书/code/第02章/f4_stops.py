# -*- coding: utf-8 -*-
"""图 02-4 stop（档）阶梯：1 → 1024 nit

上图：线性坐标下每档翻倍，后段几乎"吃掉"整个高度；
下图：对数坐标下每档等高——说明为什么描述亮度跨度要用"档"。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np

plt = H.plt

k = np.arange(0, 11)            # 0..10 档
vals = 2.0 ** k                 # 1 .. 1024 nit

fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.4),
                         gridspec_kw=dict(hspace=0.42))
cmap = plt.get_cmap("viridis")
colors = [cmap(0.05 + 0.85 * i / (len(k) - 1)) for i in range(len(k))]

# ---- 上图：线性坐标 ----
ax = axes[0]
ax.bar(k, vals, width=0.66, color=colors, edgecolor="white", linewidth=1.0,
       zorder=3)
for i, v in enumerate(vals):
    ax.text(i, v + 18, f"{v:g}", ha="center", va="bottom", fontsize=8.5,
            color=H.DARK, fontweight="bold")
ax.set_ylim(0, 1220)
ax.set_xticks(k)
ax.set_xticklabels([f"{i} 档" for i in k], fontsize=8.5)
ax.set_ylabel("亮度（nit，线性轴）")
ax.set_title("线性坐标看「档」：每档翻一倍，但后段几乎吃掉全部高度", fontsize=11.5)
ax.text(0.02, 0.97, "1 档 = 2 nit\n……\n10 档 = 1024 nit", ha="left", va="top",
        fontsize=9.5, color=H.DARK,
        bbox=dict(boxstyle="round,pad=0.42", fc="#f4f7fb", ec=H.NAVY, lw=1.0),
        transform=ax.transAxes)
ax.xaxis.grid(False)

# ---- 下图：对数坐标 ----
ax = axes[1]
ax.bar(k, vals, width=0.66, color=colors, edgecolor="white", linewidth=1.0,
       zorder=3, bottom=0.5)
for i, v in enumerate(vals):
    ax.text(i, v * 1.22, f"{v:g}", ha="center", va="bottom", fontsize=8.5,
            color=H.DARK, fontweight="bold")
    ax.text(i, 0.62, f"{i}", ha="center", va="bottom", fontsize=8,
            color="white", fontweight="bold", zorder=5)
ax.set_yscale("log")
ax.set_ylim(0.5, 3000)
ax.set_xticks(k)
ax.set_xticklabels([f"{i} 档" for i in k], fontsize=8.5)
ax.set_ylabel("亮度（nit，对数轴）")
ax.set_title("对数坐标：每档等高——这才是人眼与「档」的直觉", fontsize=11.5)
ax.set_yticks([1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])
ax.set_yticklabels(["1", "2", "4", "8", "16", "32", "64", "128", "256",
                    "512", "1024"], fontsize=8)
ax.xaxis.grid(False)
# 相邻档的"翻倍"标注
for i in range(1, len(k)):
    ax.annotate("", xy=(i - 0.33, vals[i]), xytext=(i - 0.33, vals[i - 1]),
                arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=1.1))
ax.text(0.02, 0.97, "×2　×2　×2 …… 每升一档，亮度翻倍",
        transform=ax.transAxes, ha="left", va="top",
        fontsize=9, color=H.ORANGE, fontweight="bold")

fig.suptitle("用「档（stop）」数亮度跨度：每翻一倍是一档，1 → 1024 nit 共 10 档",
             fontsize=12.8, fontweight="bold", y=0.99)
H.save(fig, 2, "f4_stops")
