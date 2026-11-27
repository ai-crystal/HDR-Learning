# -*- coding: utf-8 -*-
"""图 8-1 游戏渲染到显示的完整链路，标出每一步的数值范围。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("hdr-tech")
import numpy as np
import matplotlib.patches as mp

plt = H.plt

fig, ax = plt.subplots(figsize=(7.4, 5.6))
ax.set_xlim(0, 11)
ax.set_ylim(0, 10)
ax.axis("off")

rows = [
    ("场景渲染", "FP16 线性 scRGB", "0 到数千 nit，1.0 记 80 nit", H.NAVY),
    ("后处理", "泛光 / 景深 / 抗锯齿", "仍是线性，峰值可能过万", H.BLUE),
    ("自动曝光", "整帧乘一个增益", "归一化到 0 到 1 的显示量", H.TEAL),
    ("色调映射", "按亮度比例压缩", "0 到显示器峰值", H.ORANGE),
    ("编码", "scRGB 或 PQ", "scRGB 取 L/80，PQ 取码值 0 到 1", H.PURPLE),
    ("合成与 UI", "UI 单独一层，不参与映射", "UI 白 = scRGB 1.0 或 PQ 0.58", H.GOLD),
    ("显示", "桌面合成或独占全屏", "EOTF 还原为绝对亮度", H.RED),
]

n = len(rows)
top, bot = 9.45, 0.70
h = (top - bot) / n
bh = h * 0.66

for i, (name, sub, rng, col) in enumerate(rows):
    y = top - (i + 1) * h + (h - bh) / 2
    box = mp.FancyBboxPatch((0.30, y), 3.0, bh,
                            boxstyle="round,pad=0.02,rounding_size=0.10",
                            linewidth=1.4, edgecolor=col, facecolor=col + "1a")
    ax.add_patch(box)
    ax.text(1.80, y + bh * 0.64, name, ha="center", va="center",
            fontsize=11, color=col, fontweight="bold")
    ax.text(1.80, y + bh * 0.25, sub, ha="center", va="center",
            fontsize=8.2, color="#3b4654")
    if i < n - 1:
        y1 = y - (h - bh)
        ax.annotate("", xy=(1.80, y1), xytext=(1.80, y),
                    arrowprops=dict(arrowstyle="-|>", color="#8d99a6",
                                    lw=1.1, shrinkA=0, shrinkB=0))
    ax.plot([3.50, 3.80], [y + bh / 2] * 2, color=col, lw=1.0, ls=":")
    ax.text(3.92, y + bh / 2, rng, ha="left", va="center",
            fontsize=8.8, color="#2c3e50")

# 右端分组标注
xb, xt = 9.95, 10.42
ax.plot([xb, xb], [9.45, 6.30], color=H.NAVY, lw=1.1)
ax.plot([xb, xb], [6.30, 0.70], color=H.RED, lw=1.1)
ax.plot([xb, xb + 0.12], [9.45, 9.45], color=H.NAVY, lw=1.1)
ax.plot([xb, xb + 0.12], [6.30, 6.30], color="#8d99a6", lw=1.1)
ax.plot([xb, xb + 0.12], [0.70, 0.70], color=H.RED, lw=1.1)
ax.text(xt, 7.88, "引擎内部运算", ha="center", va="center", rotation=90,
        fontsize=9.2, color=H.NAVY)
ax.text(xt, 3.50, "交给输出端", ha="center", va="center", rotation=90,
        fontsize=9.2, color=H.RED)

H.save(fig, 8, "f1_pipeline")
