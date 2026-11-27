# -*- coding: utf-8 -*-
"""第 12 章 图 4：各类评价指标的适用域，横轴亮度、纵轴失真类型。

横条长度表示该指标在公开文献与实践中被验证过的亮度区间，
不是它能算的亮度上限，超出区间仍然能算出数，只是数不可信。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

fig, ax = plt.subplots(figsize=(8.4, 4.5))
fig.subplots_adjust(left=0.225, right=0.975, bottom=0.145, top=0.90)

# (行中心, 行名)
rows = [
    (5.0, "主观偏好"),
    (4.0, "时域（闪烁、拖影）"),
    (3.0, "光晕与局部调光"),
    (2.0, "压缩与量化"),
    (1.0, "色调映射与削波"),
]

# 每行若干条：(指标, 起始 nit, 结束 nit, 颜色)
bars = {
    5.0: [("主观实验 BT.500", 0.001, 10000, H.DARK)],
    4.0: [("ClearMR", 0.05, 10000, H.GOLD), ("主观实验（只测到 24 帧）", 0.01, 4000, H.GRAY)],
    3.0: [("HDR-VDP-3", 0.002, 10000, H.PURPLE)],
    2.0: [("PSNR", 0.02, 10000, H.RED), ("SSIM / MS-SSIM", 0.1, 3000, H.ORANGE),
          ("VMAF（HDR 模型）", 0.05, 4000, H.BLUE), ("ΔE_ITP（BT.2124）", 0.005, 10000, H.TEAL)],
    1.0: [("ΔE_ITP", 0.005, 10000, H.TEAL), ("HDR-VDP-3 的检测图", 0.005, 10000, H.PURPLE)],
}

BH = 0.155
for yc, name in rows:
    n = len(bars[yc])
    span = 0.74
    step = span / n
    for i, (lab, x0, x1, col) in enumerate(bars[yc]):
        y0 = yc + span / 2 - (i + 1) * step + (step - BH) / 2
        ax.broken_barh([(x0, x1 - x0)], (y0, BH), facecolors=col, alpha=0.78,
                       edgecolors="none")
        ax.text(x0 * 1.35, y0 + BH / 2, lab, fontsize=7.3, color="white",
                va="center", ha="left", fontweight="bold")

ax.set_xscale("log")
ax.set_xlim(0.001, 10000)
ax.set_ylim(0.45, 5.92)
ax.set_yticks([r[0] for r in rows])
ax.set_yticklabels([r[1] for r in rows], fontsize=8.6)
ax.set_xlabel("画面亮度（cd/m$^2$）")
ax.set_xticks([0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000])
ax.set_xticklabels(["0.001", "0.01", "0.1", "1", "10", "100", "1000", "10000"])
ax.grid(axis="y", visible=False)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

for xv, lab, ha in [(0.005, "典型黑位 0.005", "left"), (100, "SDR 白 100", "center"),
                    (1000, "HDR 参考峰值 1000", "center")]:
    ax.axvline(xv, color="#8a96a3", linestyle=(0, (3, 3)), linewidth=0.9, zorder=0)
    ax.text(xv, 5.63, lab, fontsize=7.2, color="#5d6b7a",
            va="center", ha=ha, zorder=6)

ax.text(0.0013, 0.50, "条越短，说明该指标在这个亮度范围内缺验证，不是不能算",
        fontsize=7.4, color="#5d6b7a", va="bottom", ha="left")

H.save(fig, 12, "f4_metric_domains")
