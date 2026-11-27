# -*- coding: utf-8 -*-
"""图 3-6：主流 HDR 格式在不同显示能力下的降级路径（矩阵示意）。

行是内容格式，列是终端能力，格内文字给出该组合下的处理方式。
颜色区分三档：直通、需要映射或转换、需要专用解码器。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams["mathtext.fontset"] = "dejavusans"

fig = plt.figure(figsize=(9.0, 4.6))
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

STYLE = {
    "pass": (H.GREEN, "#e8f4ec"),
    "map": (H.ORANGE, "#fdf3e2"),
    "need": (H.RED, "#fbeae8"),
}

ROWS = [
    ("HDR10", "PQ + 静态元数据", [
        ("pass", "直通\n按 ST 2086 元数据映射"),
        ("map", "跨传递函数\n需重新映射"),
        ("map", "静态映射\n按 MaxCLL 压暗"),
    ]),
    ("HDR10+", "ST 2094-40 动态", [
        ("map", "有解码器则逐帧\n否则退化为 HDR10"),
        ("map", "需重新映射"),
        ("map", "逐帧或静态映射"),
    ]),
    ("杜比视界", "12 bit ICtCp", [
        ("map", "Profile 8.1 兼容层\nProfile 5 需授权解码"),
        ("need", "Profile 8.4\n需授权解码"),
        ("need", "解码器内映射\n需授权"),
    ]),
    ("HDR Vivid", "PQ + 动态元数据", [
        ("map", "需 Vivid 解码\n否则按 PQ 近似"),
        ("map", "需重新映射"),
        ("map", "映射到 SDR 亮度"),
    ]),
    ("HLG", "场景参考", [
        ("map", "OOTF 重算\n再二次映射"),
        ("pass", "直通\n按自身峰值定 γ"),
        ("pass", "可直接显示\n偏暗、对比拉大"),
    ]),
]

COLS = ["PQ 电视（HDR10 基线）", "HLG 电视", "SDR 电视"]
X0, CW, GAP = 0.265, 0.232, 0.014
Y0, RH = 0.745, 0.142

for j, name in enumerate(COLS):
    ax.text(X0 + j * (CW + GAP) + CW / 2, 0.905, name, ha="center",
            va="center", fontsize=9.0, color=H.DARK)

for i, (fmt, note, cells) in enumerate(ROWS):
    y = Y0 - i * RH
    ax.text(0.245, y + 0.028, fmt, ha="right", va="center", fontsize=9.2,
            color=H.DARK)
    ax.text(0.245, y - 0.032, note, ha="right", va="center", fontsize=7.6,
            color=H.GRAY)
    for j, (kind, txt) in enumerate(cells):
        edge, face = STYLE[kind]
        x = X0 + j * (CW + GAP)
        ax.add_patch(FancyBboxPatch((x, y - RH / 2 + 0.014), CW,
                                    RH - 0.028,
                                    boxstyle="round,pad=0.004,rounding_size=0.010",
                                    linewidth=1.0, edgecolor=edge,
                                    facecolor=face, zorder=2))
        ax.text(x + CW / 2, y, txt, ha="center", va="center", fontsize=7.4,
                color=H.DARK, linespacing=1.5, zorder=3)

# 图例
lx = [0.265, 0.475, 0.685]
for i, (kind, lab) in enumerate([("pass", "直通"), ("map", "映射 / 转换"),
                                 ("need", "需专用解码")]):
    ax.add_patch(FancyBboxPatch((lx[i], 0.035), 0.028, 0.032,
                                boxstyle="round,pad=0.002,rounding_size=0.006",
                                linewidth=1.0, edgecolor=STYLE[kind][0],
                                facecolor=STYLE[kind][1], zorder=2))
    ax.text(lx[i] + 0.038, 0.051, lab, ha="left", va="center", fontsize=8.2,
            color=H.DARK)

H.save(fig, 3, "f6_degradation_paths")
