# -*- coding: utf-8 -*-
"""第 14 章 图 14-5：带宽不足时的降级顺序流程图（左），以及降级后带宽阶梯（右）。
所有带宽都用同一条公式估算：像素数/秒 × 每像素位数 × 1.25 开销。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import warnings
warnings.filterwarnings("ignore")

PX = 3840 * 2160 * 60           # 像素总数/秒
OVH = 1.25


def bw(bpp, fps=60, px=PX):
    return px * (fps / 60) * bpp * OVH / 1e9


fig = plt.figure(figsize=(7.2, 4.9))
gs = fig.add_gridspec(1, 2, width_ratios=[1.35, 1.0], wspace=0.42)

# ================== 左：流程图 ==================
axF = fig.add_subplot(gs[0]); axF.axis("off"); axF.set_xlim(0, 1); axF.set_ylim(0, 1)

steps = [
    ("带宽不够", "目标 4K60 10bit 4:4:4 = 18.7 Gbps\n可用带宽（如 HDMI 2.0 = 18）装不下",
     H.RED, "#fdf1ec"),
    ("① 先保分辨率与帧率", "画面尺寸、流畅度优先不动",
     H.NAVY, "white"),
    ("② 降色度采样", "4:4:4 → 4:2:2 → 4:2:0\n色彩细节打折：18.7 → 12.5 → 9.3 Gbps",
     H.TEAL, "#eef7f5"),
    ("③ 降色深", "10bit → 8bit，HDR 暗部层次变薄\n9.3 → 7.5 Gbps",
     H.GREEN, "#eef8f1"),
    ("④ 降刷新率或分辨率", "4K120 → 4K60、4K → 1440p\n不动其他参数也能腾出带宽",
     H.ORANGE, "#fdf5ec"),
    ("⑤ 最后手段：开 DSC", "视觉无损压缩到约 1/3\n18.7 → 约 6.2 Gbps（第 15 章细讲）",
     H.PURPLE, "#f6f0fb"),
]

bh, gap, top = 0.112, 0.030, 0.985
for i, (t, d, c, fc) in enumerate(steps):
    y1 = top - i * (bh + gap)
    axF.add_patch(FancyBboxPatch((0.045, y1 - bh), 0.935, bh,
                                 boxstyle="round,pad=0.006,rounding_size=0.022",
                                 fc=fc, ec=c, lw=1.5, transform=axF.transAxes))
    axF.text(0.485, y1 - 0.027, t, ha="center", va="center", fontsize=9.2,
             color=c, fontweight="bold", transform=axF.transAxes)
    axF.text(0.485, y1 - 0.079, d, ha="center", va="center", fontsize=7.4,
             color="#44525f", transform=axF.transAxes, linespacing=1.35)
    if i < len(steps) - 1:
        axF.add_patch(FancyArrowPatch((0.512, y1 - bh - 0.004),
                                      (0.512, y1 - bh - gap + 0.004),
                                      arrowstyle="-|>", mutation_scale=12,
                                      lw=1.4, color="#8b98a8",
                                      transform=axF.transAxes))

axF.text(0.5, 0.012, "很多设备不会报错，而是“悄悄降级”——请到显卡控制面板 / 显示器信息页\n"
                     "确认当前实际输出格式（分辨率 / 刷新率 / 色深 / 色度采样）",
         ha="center", va="bottom", fontsize=7.6, color=H.RED,
         transform=axF.transAxes,
         bbox=dict(boxstyle="round,pad=0.3", fc="#fdf1ec", ec=H.RED, lw=0.9, alpha=0.95))
axF.text(0.5, 1.005, "左：带宽不足时的降级顺序", ha="center", va="bottom",
         fontsize=10.2, color=H.NAVY, fontweight="bold", transform=axF.transAxes)

# ================== 右：降级后的带宽阶梯 ==================
axB = fig.add_subplot(gs[1])
ladder = [
    ("原始需求\n4K60 10bit 4:4:4", bw(30), H.RED),
    ("降色度采样\n4K60 10bit 4:2:2", bw(20), H.TEAL),
    ("再降色度\n4K60 10bit 4:2:0", bw(15), H.GREEN),
    ("降色深\n4K60 8bit 4:2:0", bw(12), H.ORANGE),
    ("开 DSC 后\n约 1/3 数据量", bw(30) / 3, H.PURPLE),
]
y = np.arange(len(ladder))[::-1]
axB.barh(y, [l[1] for l in ladder], height=0.55,
         color=[l[2] for l in ladder], edgecolor="white", linewidth=0.8)
for yy, (name, v, c) in zip(y, ladder):
    axB.text(v + 0.35, yy, f"{v:.1f} Gbps", va="center", ha="left",
             fontsize=8.6, color=H.DARK, fontweight="bold")

axB.axvline(18.0, color=H.RED, ls="--", lw=1.5)
axB.text(18.2, 4.42, "HDMI 2.0 上限 18.0", fontsize=7.4, color=H.RED,
         fontweight="bold", va="center", ha="left")
axB.text(bw(30) + 0.35, 4.0 - 0.22, "超线，装不下", fontsize=7.0, color=H.RED)

axB.set_yticks(y)
axB.set_yticklabels([l[0] for l in ladder], fontsize=7.2)
axB.set_xlabel("所需带宽（Gbps）")
axB.set_xlim(0, 23)
axB.set_ylim(-0.62, 4.75)
axB.set_title("右：一次降级能省多少", fontsize=10.2, color=H.NAVY, pad=8)
axB.grid(axis="y", visible=False)
axB.grid(axis="x", color="#dde3ea", lw=0.7)

fig.suptitle("图 14-5　带宽不够时系统怎么降级：先动色度采样，再动色深，最后才动分辨率与 DSC",
             fontsize=12.0, fontweight="bold", y=1.02)
fig.subplots_adjust(top=0.87, bottom=0.10, left=0.045, right=0.985)
H.save(fig, 14, "f6_degrade_flow")
