# -*- coding: utf-8 -*-
"""图 3-5：元数据在基本流、文件封装、显示接口三层中的落点（框图）。

行是承载层次，列是静态元数据与动态元数据。格内列出该层实际使用的语法元素
名称，不涉及具体厂商扩展。最后一列标注读取时机。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams["mathtext.fontset"] = "dejavusans"

fig = plt.figure(figsize=(9.4, 4.8))
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

COLS = [0.295, 0.605]
CW, CH = 0.270, 0.175
ROWS = [0.735, 0.475, 0.215]

HEAD = ["静态元数据（ST 2086、MaxCLL / MaxFALL）",
        "动态元数据（ST 2094 应用）"]

BODY = [
    ["HEVC SEI 137 / 144\nAV1 metadata OBU 1 / 2\nVUI 传输特性 16 或 18",
     "HEVC SEI 4（t35 厂商私有）\nAV1 metadata OBU 4\n与帧严格对齐"],
    ["MP4 mdcv / clli\nMKV Colour 元素\nTS 只靠 SEI，无额外容器",
     "MP4 dvcC / dvvC 等配置盒\nHDR10+ 的 JSON 旁路文件\ndvcC 只声明配置"],
    ["HDMI EDID 能力块\nDRM InfoFrame（0x87）\nDisplayPort 元数据包",
     "接口层一般只传静态\n动态元数据靠解码器解析\n不占用带宽"],
]

ROWLAB = ["基本流", "文件与封装", "显示接口"]
ROWNOTE = ["解码时读到", "起播前即可读", "链路协商时交换"]

STYLE = [(H.NAVY, "#eaf1f8"), (H.TEAL, "#e6f4f1")]

for r, y in enumerate(ROWS):
    for c, x in enumerate(COLS):
        edge, face = STYLE[c]
        ax.add_patch(FancyBboxPatch((x - CW / 2, y - CH / 2), CW, CH,
                                    boxstyle="round,pad=0.006,rounding_size=0.012",
                                    linewidth=1.3, edgecolor=edge,
                                    facecolor=face, zorder=2))
        ax.text(x, y, BODY[r][c], ha="center", va="center", fontsize=7.8,
                color=H.DARK, linespacing=1.75, zorder=3)
    ax.text(0.055, y + 0.020, ROWLAB[r], rotation=0, ha="left", va="center",
            fontsize=9.2, color=H.DARK)
    ax.text(0.055, y - 0.030, ROWNOTE[r], rotation=0, ha="left", va="center",
            fontsize=7.4, color=H.GRAY)

for c, x in enumerate(COLS):
    ax.text(x, 0.895, HEAD[c], ha="center", va="center", fontsize=8.8,
            color=STYLE[c][0])

# 层与层之间的转交箭头
for i in range(2):
    for x in COLS:
        ax.add_patch(FancyArrowPatch((x, ROWS[i] - CH / 2 - 0.006),
                                     (x, ROWS[i + 1] + CH / 2 + 0.006),
                                     arrowstyle="-|>", mutation_scale=10,
                                     color=H.GRAY, lw=1.1, zorder=1))

ax.plot([0.205, 0.205], [0.115, 0.855], color=H.LGRAY, lw=0.9, ls=(0, (3, 4)),
        zorder=0)

ax.text(0.605, 0.075, "自上而下是写入顺序，显示端解析时先从接口能力看起",
        ha="center", va="center", fontsize=8.0, color=H.GRAY)

H.save(fig, 3, "f5_bitstream_layers")
