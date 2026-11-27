# -*- coding: utf-8 -*-
"""第 10 章 图 4：三条广播路线的分层对照。

按"封装与传输 / 视频编码 / HDR 承载 / 音频"四层并排，底部是共同的制作端。
只画方框与连线，不涉及任何统计数据。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

H.set_book("hdr-tech")
plt = H.plt

fig, ax = plt.subplots(figsize=(9.2, 4.7))
fig.subplots_adjust(left=0.005, right=0.995, bottom=0.02, top=0.98)
ax.set_xlim(-0.46, 3.02)
ax.set_ylim(0.0, 5.42)
ax.axis("off")

W = 0.90
cols = [
    ("ATSC 3.0", "北美、韩国", 0.02, H.NAVY),
    ("DVB UHD-1\nPhase 2", "欧洲、澳洲", 1.06, H.TEAL),
    ("ISDB-S3", "日本 4K / 8K", 2.10, H.ORANGE),
]
rows = [
    ("封装与传输", 3.98, [
        "IP 组播\nROUTE / DASH\nA/331",
        "MPEG-2 TS\nDVB-T2 / S2X\nTS 101 154",
        "ISDB-S3\nSTD-B44\n12 GHz 转发器",
    ]),
    ("视频编码", 3.08, ["HEVC Main10\n4:2:0 10 bit\nA/341",
                      "HEVC Main10\n4:2:0 10 bit\nTS 101 154",
                      "HEVC Main10\n4:2:2 10 bit\nSTD-B32"]),
    ("HDR 承载", 2.08, ["HLG 与 PQ 并列\nPQ 靠 SEI 静态元数据\nSL-HDR1 可选",
                      "HLG 强制\nPQ 加静态元数据可选\n相位 2 的核心要求",
                      "HLG 为主\n4K 与 8K 同时开播\n不带动态元数据"]),
    ("音频", 1.18, ["AC-4\n或 MPEG-H", "AC-4\n或 E-AC-3", "MPEG-4 AAC\n22.2 声道"]),
]

for name, sub, x0, c in cols:
    ax.add_patch(FancyBboxPatch((x0, 4.86), W, 0.44,
                                boxstyle="round,pad=0.02,rounding_size=0.05",
                                fc=c, ec=c, lw=0.8, zorder=3))
    ax.text(x0 + W / 2, 5.155, name, ha="center", va="center", color="white",
            fontsize=9.0, fontweight="bold", zorder=4, linespacing=1.15)
    ax.text(x0 + W / 2, 4.945, sub, ha="center", va="center", color="white",
            fontsize=7.2, zorder=4)

for label, y0, texts in rows:
    ax.text(-0.42, y0 + 0.40, label, ha="left", va="center", fontsize=9.0, color=H.DARK)
    for (name, sub, x0, c), t in zip(cols, texts):
        ax.add_patch(FancyBboxPatch((x0, y0), W, 0.80,
                                    boxstyle="round,pad=0.02,rounding_size=0.04",
                                    fc="white", ec=c, lw=1.1, zorder=3))
        ax.text(x0 + W / 2, y0 + 0.40, t, ha="center", va="center", fontsize=7.3,
                color=H.DARK, zorder=4, linespacing=1.45)

ax.add_patch(FancyBboxPatch((0.02, 0.14), 2.98, 0.62,
                            boxstyle="round,pad=0.02,rounding_size=0.05",
                            fc="#eef3f8", ec=H.GRAY, lw=1.0, zorder=3))
ax.text(1.51, 0.45, "共同的制作端：一条 HLG 信号（SDR 终端可直接显示），或 PQ 加静态／动态元数据",
        ha="center", va="center", fontsize=8.4, color=H.DARK, zorder=4)

for x in [0.47, 1.51, 2.55]:
    ax.add_patch(FancyArrowPatch((x, 1.16), (x, 0.80), arrowstyle="-|>", mutation_scale=9,
                                 color=H.GRAY, lw=0.9, zorder=2))

H.save(fig, 10, "f4_broadcast_stack")
