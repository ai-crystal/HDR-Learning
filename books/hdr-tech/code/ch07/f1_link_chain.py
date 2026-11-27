# -*- coding: utf-8 -*-
"""图 7-1：端到端 HDR 链路，从母版文件到面板发光。

左侧是链路节点，右侧是每一段真正发生的事：位深、色度、容器、带宽。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

STAGES = [
    ("母版与套底", "#dce9f5", H.BLUE,
     "12 bit、PQ、BT.2020、4:4:4\n母版峰值 1000 或 4000 nit"),
    ("编码前处理", "#dce9f5", H.BLUE,
     "位深降到 10 bit 并加抖动\n色度降到 4:2:0，切块"),
    ("视频编码", "#dfe6f2", H.NAVY,
     "HEVC Main10、AV1、VVC、AVS3\n输出 10 bit 4:2:0 码流"),
    ("封装", "#dfe6f2", H.NAVY,
     "MP4 写入 hvcC、mdcv、clli\n或 MKV 的 Colour 元素"),
    ("传输与分发", "#d8f0ea", H.TEAL,
     "广播 TS、流媒体 DASH 与 HLS\n4K 常在 15 至 25 Mbps"),
    ("解码与重建", "#fae6d2", H.ORANGE,
     "解出 10 bit 基带信号\n附带的元数据一起交给显示端"),
    ("显示与呈现", "#fae6d2", H.ORANGE,
     "按元数据做色调映射\n面板受峰值与 ABL 限制"),
]

fig, ax = plt.subplots(figsize=(7.9, 5.5))
ax.set_axis_off()
ax.set_xlim(0, 10)
ax.set_ylim(0.0, 10.2)

TOP, HH, GAP = 9.9, 0.92, 0.42
X0, BW = 0.15, 4.55
ys = []
for i, (name, fc, ec, note) in enumerate(STAGES):
    y = TOP - HH - i * (HH + GAP)
    ys.append(y)
    p = FancyBboxPatch((X0, y), BW, HH,
                       boxstyle="round,pad=0.02,rounding_size=0.10",
                       fc=fc, ec=ec, lw=1.1, zorder=2)
    ax.add_patch(p)
    ax.text(X0 + BW / 2, y + HH / 2, name, ha="center", va="center",
            fontsize=9.6, color=H.DARK, zorder=3)
    ax.text(X0 + BW + 0.35, y + HH / 2, note, ha="left", va="center",
            fontsize=7.8, color="#4a5666", zorder=3, linespacing=1.6)
    if i > 0:
        y0 = ys[i - 1]
        ax.add_patch(FancyArrowPatch((X0 + BW / 2, y0), (X0 + BW / 2, y + HH + 0.02),
                                     arrowstyle="-|>", mutation_scale=9,
                                     color="#8b98a8", lw=1.2, zorder=1))

# 链路两端的边界标记
for yv, lab in [(ys[0] + HH + 0.16, "制作端（影厅、调色棚）"),
                (ys[-1] - 0.28, "观看端（客厅、手机）")]:
    ax.plot([X0, X0 + BW], [yv, yv], color=H.GRAY, lw=0.8, ls=(0, (3, 3)))
    ax.text(X0 + BW + 0.35, yv, lab, ha="left", va="center",
            fontsize=7.6, color=H.GRAY)

ax.text(0.05, 0.20,
        "链路越往后，可用的位深与色度精度只减不增，任何一段的降位深都会永久留在信号里。",
        fontsize=8.0, color=H.RED, ha="left", va="center")

H.save(fig, 7, "f1_link_chain")
