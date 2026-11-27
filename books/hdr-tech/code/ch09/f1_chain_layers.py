# -*- coding: utf-8 -*-
"""第 09 章 图 1：移动端 HDR 链路的分层示意（采集 / 文件 / 平台 / 显示）。"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

H.set_book("hdr-tech")
plt = H.plt

fig, ax = plt.subplots(figsize=(7.8, 4.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

cols = [
    ("采集", 12.0, H.NAVY, [
        "相机 RAW\n10 / 12 bit 线性",
        "多帧合成\n局部色调映射",
        "HDR 视频\nHLG 或 PQ 10 bit",
    ]),
    ("文件与编码", 37.0, H.TEAL, [
        "HEIF\nApple 增益图",
        "JPEG\nUltra HDR 增益图",
        "AVIF\ntmap 与增益图",
        "HEVC / AV1\n10 bit 视频",
    ]),
    ("平台合成", 63.0, H.ORANGE, [
        "Android\nGainmap API，EGL 10 bit",
        "iOS 与 macOS\nCore Image，EDR",
        "Windows\n高级颜色与 scRGB",
    ]),
    ("显示", 88.0, H.PURPLE, [
        "SDR 白锚点\n203 nit 或用户亮度",
        "EDR 余量\n峰值除以白点",
        "ABL 与功耗\n按平均亮度降额",
    ]),
]

BW = 21.0
for title, cx, color, items in cols:
    # 层标题
    ax.add_patch(FancyBboxPatch((cx - BW / 2, 88.5), BW, 8.0,
                                boxstyle="round,pad=0.6,rounding_size=1.2",
                                linewidth=1.0, edgecolor=color,
                                facecolor=color, alpha=0.92))
    ax.text(cx, 92.5, title, ha="center", va="center", color="white",
            fontsize=10.5, fontweight="bold")
    n = len(items)
    top = 82.0
    gap = 3.2
    h = (top - 10.0 - gap * (n - 1)) / n
    h = min(h, 15.0)
    for i, s in enumerate(items):
        y = top - (i + 1) * h - i * gap
        ax.add_patch(FancyBboxPatch((cx - BW / 2, y), BW, h,
                                    boxstyle="round,pad=0.4,rounding_size=0.8",
                                    linewidth=0.9, edgecolor=color,
                                    facecolor="white", alpha=1.0))
        ax.text(cx, y + h / 2, s, ha="center", va="center", fontsize=7.6,
                color="#22303f", linespacing=1.55)

for x0, x1 in [(23.6, 25.6), (48.6, 50.6), (74.6, 76.6)]:
    ax.add_patch(FancyArrowPatch((x0, 55), (x1, 55), arrowstyle="-|>",
                                 mutation_scale=14, linewidth=1.6,
                                 color=H.GRAY))

ax.text(50, 6.0, "同一份内容在每一层都有一次「按本层能力重新映射」的机会，\n"
                 "层数越多，高光被重复压缩的风险越大",
        ha="center", va="center", fontsize=8.2, color=H.GRAY, linespacing=1.6)

H.save(fig, 9, "f1_chain_layers")
