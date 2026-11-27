# -*- coding: utf-8 -*-
"""第 12 章 图 1：HDR 标准的分层地图与一条母版的引用链。

上：五个层次，每层只写这一层真正定下来的东西，层与层之间的箭头表示
    下一层必须满足上一层的要求（上一层引用下一层）。
下：一份母版从调色棚走到屏幕，五个节点以及每个节点上起作用的那份文件。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig = plt.figure(figsize=(8.0, 7.1))
ax1 = fig.add_axes([0.02, 0.42, 0.96, 0.55])
ax2 = fig.add_axes([0.02, 0.02, 0.96, 0.34])
for ax in (ax1, ax2):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

# ---------------- (a) 五层 ----------------
layers = [
    ("母版与制作", "母版显示信息 ST 2086 · 交换框架 ST 2067 · ACES ST 2065-1 · 制作实践 BT.2408", H.NAVY),
    ("编码与元数据", "HEVC 23008-2 · VVC 23090-3 · AV1 · 动态元数据 ST 2094-10/-20/-40 · 容器 BT.2100", H.BLUE),
    ("封装与分发", "MP4 · MPEG-2 TS · ROUTE/DASH · DVB TS 101 154 · ATSC A/341 · AVS3", H.TEAL),
    ("接口与信令", "CTA-861 的 EDID 与 InfoFrame · HDMI 2.1 · DisplayPort 2.1", H.ORANGE),
    ("终端与认证", "VESA DisplayHDR · CTA 认证 · 平台规范（Dolby Vision / HDR10+ / 菁彩 HDR）· BT.2035 观看环境", H.RED),
]
ys = [0.88, 0.69, 0.50, 0.31, 0.12]
h = 0.122
for (name, docs, col), y in zip(layers, ys):
    ax1.add_patch(FancyBboxPatch((0.03, y - h / 2), 0.94, h,
                                 boxstyle="round,pad=0.004,rounding_size=0.012",
                                 linewidth=1.1, edgecolor=col,
                                 facecolor="#f6f8fa"))
    ax1.text(0.055, y + 0.030, name, fontsize=9.6, color=col, fontweight="bold",
             va="center", ha="left")
    ax1.text(0.055, y - 0.030, docs, fontsize=7.9, color="#2b3442",
             va="center", ha="left")

gaps = ["层间靠引用连起来：上层只说自己要多严，具体数值在下层",
        "码流把元数据当成载荷原样搬运",
        "分发不改动语法，只决定带宽与优先级",
        "能力协商决定终端能不能按母版的意图显示"]
for i, (lab, ytop, ybot) in enumerate(zip(
        [gaps[0], gaps[1], gaps[2], gaps[3]],
        [ys[0] - h / 2, ys[1] - h / 2, ys[2] - h / 2, ys[3] - h / 2],
        [ys[1] + h / 2, ys[2] + h / 2, ys[3] + h / 2, ys[4] + h / 2])):
    ax1.add_patch(FancyArrowPatch((0.16, ytop), (0.16, ybot),
                                  arrowstyle="-|>", mutation_scale=11,
                                  linewidth=1.0, color="#6b7a8c",
                                  shrinkA=1, shrinkB=1))
    ax1.text(0.185, (ytop + ybot) / 2, lab, fontsize=7.2, color="#56626f",
             va="center", ha="left")

ax1.text(0.03, 0.992, "(a)", fontsize=10, fontweight="bold", color=H.DARK,
         va="top", ha="left")

# ---------------- (b) 一条链 ----------------
nodes = [
    ("母版", "PQ 绝对亮度\nST 2086 定边界", H.NAVY),
    ("编码器", "SEI 携带 2086\n与 2094 的载荷", H.BLUE),
    ("封装", "MP4 box\nTS descriptor", H.TEAL),
    ("接口", "InfoFrame\n静态元数据", H.ORANGE),
    ("显示", "EDID 声明能力\n本地做映射", H.RED),
]
bw = 0.160
xs = [0.010 + i * (bw + 0.045) for i in range(5)]
ybot2, h2 = 0.36, 0.50
for (name, sub, col), x in zip(nodes, xs):
    ax2.add_patch(FancyBboxPatch((x, ybot2), bw, h2,
                                 boxstyle="round,pad=0.004,rounding_size=0.015",
                                 linewidth=1.1, edgecolor=col,
                                 facecolor="#f6f8fa"))
    ax2.text(x + bw / 2, ybot2 + h2 - 0.09, name, fontsize=9.2, color=col,
             fontweight="bold", ha="center", va="center")
    ax2.text(x + bw / 2, ybot2 + 0.16, sub, fontsize=7.2, color="#2b3442",
             ha="center", va="center", linespacing=1.55)
for i in range(4):
    x0 = xs[i] + bw
    x1 = xs[i + 1]
    ax2.add_patch(FancyArrowPatch((x0 + 0.003, ybot2 + h2 / 2),
                                  (x1 - 0.003, ybot2 + h2 / 2),
                                  arrowstyle="-|>", mutation_scale=12,
                                  linewidth=1.2, color="#5d6b7a",
                                  shrinkA=0, shrinkB=0))
ax2.text(0.5, 0.955, "(b) 一份母版走过的五个节点，每一跳都要重新解释一遍元数据",
         fontsize=8.8, color="#2b3442", ha="center", va="center")
ax2.text(0.5, 0.155, "任何一跳不认识某个字段，就要么按静态元数据处理，要么按自己的屏幕猜",
         fontsize=7.8, color="#5d6b7a", ha="center", va="center")
ax2.text(0.035, 0.02, "PQ 码值 → YCbCr 10 bit → 码流 → 基带 → 面板驱动，链路越往下，能商量的余地越小",
         fontsize=7.6, color="#5d6b7a", ha="left", va="bottom")

plt.rcParams["savefig.dpi"] = 135
H.save(fig, 12, "f1_standards_map")
