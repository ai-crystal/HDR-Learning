# -*- coding: utf-8 -*-
"""第 08 章 图 1：色彩管理链路的五段结构与每段所依赖的数据。

上排是五段变换，每段下方写它读写的文件内容；
中间的括号把五段分成"源设备坐标 / PCS / 目标设备坐标"三段语义；
最下方是 profile 的来源，即仪器测量与拟合。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt = H.plt

fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
ax.grid(False)

boxes = [
    (1.0, "源 码 值", "8 / 10 / 12 bit", H.NAVY),
    (20.5, "线 性 化", "src 的 TRC", H.BLUE),
    (40.0, "源 → PCS", "A2B0 / mAB", H.TEAL),
    (59.5, "PCS → 目标", "B2A0 / mAB", H.ORANGE),
    (79.0, "目 标 码 值", "面板 EOTF", H.RED),
]
W, Y, HH = 17.0, 70.0, 20.0

for x, title, sub, col in boxes:
    ax.add_patch(FancyBboxPatch((x, Y), W, HH,
                                boxstyle="round,pad=0.0,rounding_size=1.6",
                                fc="white", ec=col, lw=1.5, zorder=3))
    ax.text(x + W / 2, Y + HH * 0.63, title, ha="center", va="center",
            fontsize=8.6, color=col, zorder=4)
    ax.text(x + W / 2, Y + HH * 0.25, sub, ha="center", va="center",
            fontsize=6.6, color=H.GRAY, zorder=4)

for x in (18.0, 37.5, 57.0, 76.5):
    ax.add_patch(FancyArrowPatch((x + 0.2, Y + HH / 2), (x + 2.3, Y + HH / 2),
                                 arrowstyle="-|>", mutation_scale=10,
                                 color=H.DARK, lw=1.2, zorder=5))

# 每段下方的一行数据说明
notes = ["带标记的编码值", "解码曲线", "曲线 → CLUT\n→ 矩阵 → 曲线",
         "意图标签 + BPC", "未校正的硬件"]
for (x, _, _, col), note in zip(boxes, notes):
    ax.text(x + W / 2, 65.5, note, ha="center", va="center",
            fontsize=6.2, color=H.DARK, zorder=4, linespacing=1.45)

# 三段语义括号
def bracket(x0, x1, y, text, col):
    ax.plot([x0, x0, x1, x1], [y + 2.2, y, y, y + 2.2], color=col, lw=1.0,
            zorder=3)
    ax.text((x0 + x1) / 2, y - 5.0, text, ha="center", va="center",
            fontsize=7.2, color=col, zorder=4, linespacing=1.5)

bracket(1.0, 37.5, 52.0, "设备坐标（源）", H.NAVY)
bracket(40.0, 76.5, 52.0, "PCS：$XYZ$ 或 $L^*a^*b^*$，白点 D50", H.TEAL)
bracket(79.0, 96.0, 52.0, "设备坐标（目标）", H.RED)

# 底部：测量与拟合
ax.add_patch(FancyBboxPatch((18.0, 12.0), 60.0, 15.0,
                            boxstyle="round,pad=0.0,rounding_size=1.4",
                            fc="#fbf6ec", ec=H.GOLD, lw=1.2, ls=(0, (4, 2)),
                            zorder=3))
ax.text(48.0, 22.0, "校准测量：分光计 / 校正过的色度计", ha="center",
        va="center", fontsize=7.8, color=H.DARK, zorder=4)
ax.text(48.0, 16.6, "拟合后采样到格点，写成 A2B / B2A 标签",
        ha="center", va="center", fontsize=6.9, color=H.GRAY, zorder=4)

for tx in (48.5, 68.0):
    ax.add_patch(FancyArrowPatch((tx, 27.5), (tx, 41.0),
                                 arrowstyle="-|>", mutation_scale=9,
                                 color=H.GOLD, lw=1.0, ls=(0, (4, 2)), zorder=4))
ax.text(58.0, 33.5, "profile", fontsize=6.4, color="#a8873c", ha="center",
        va="center", zorder=4)

H.save(fig, 8, "f1_cms_chain")
