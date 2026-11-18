# -*- coding: utf-8 -*-
"""图 3-1：HDR 元数据从母版到显示的链路（框图）。

三行分别对应静态元数据、视频基本流、动态元数据，四列对应制作母版、编码、
封装与传输、显示终端。仅表达数据流向，不涉及具体厂商实现。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams["mathtext.fontset"] = "dejavusans"

fig = plt.figure(figsize=(9.2, 4.9))
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

COLS = [0.235, 0.455, 0.665, 0.875]
BW, BH = 0.180, 0.190
ROWS = {"static": 0.720, "video": 0.450, "dynamic": 0.180}

STYLE = {
    "static": (H.NAVY, "#eaf1f8"),
    "video": (H.GRAY, "#f2f4f6"),
    "dynamic": (H.ORANGE, "#fdf1e4"),
}

TEXT = {
    "static": [
        "调色台\nST 2086 母版显示参数\nMaxCLL / MaxFALL 统计",
        "HEVC SEI 137 / 144\nAV1 HDR_MDCV / HDR_CLL",
        "MP4 mdcv / clli\nTS 描述符、HDMI InfoFrame",
        "读取峰值与色域\n建立静态映射曲线",
    ],
    "video": [
        "PQ 或 HLG 视频\n10 / 12 bit 4:2:0",
        "HEVC Main10 / AV1\n传输特性 16 或 18",
        "码流、文件、接口",
        "解码为线性光",
    ],
    "dynamic": [
        "逐帧元数据生成\n（可缺省）",
        "ST 2094\nSEI t35 / metadata OBU",
        "随帧同步传输\n需解码器支持",
        "逐帧映射\n杜比视界 / HDR10+",
    ],
}

for key, y in ROWS.items():
    edge, face = STYLE[key]
    for i, x in enumerate(COLS):
        box = FancyBboxPatch((x - BW / 2, y - BH / 2), BW, BH,
                             boxstyle="round,pad=0.006,rounding_size=0.012",
                             linewidth=1.2, edgecolor=edge, facecolor=face,
                             zorder=2)
        ax.add_patch(box)
        ax.text(x, y, TEXT[key][i], ha="center", va="center",
                fontsize=7.5, color=H.DARK, linespacing=1.6, zorder=3)
    for i in range(3):
        x0 = COLS[i] + BW / 2 + 0.008
        x1 = COLS[i + 1] - BW / 2 - 0.008
        ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>",
                                     mutation_scale=9, color=edge, lw=1.2,
                                     zorder=1, shrinkA=0, shrinkB=0))

for i, name in enumerate(["制作母版", "编码", "封装与传输", "显示终端"]):
    ax.text(COLS[i], 0.895, name, ha="center", va="center", fontsize=9.4,
            color=H.DARK)
for x in [0.345, 0.560, 0.770]:
    ax.plot([x, x], [0.045, 0.855], color=H.LGRAY, lw=0.9, ls=(0, (3, 4)),
            zorder=0)

for key, lab in [("static", "静态元数据"), ("video", "视频基本流"),
                 ("dynamic", "动态元数据")]:
    ax.text(0.035, ROWS[key], lab, rotation=90, ha="center", va="center",
            fontsize=8.6, color=STYLE[key][0])

H.save(fig, 3, "f1_metadata_pipeline")
