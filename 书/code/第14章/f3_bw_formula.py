# -*- coding: utf-8 -*-
"""第 14 章 图 14-2：带宽公式分解示意。
上半：像素总数/秒 × 每像素位数 × 开销因子 = 所需带宽 的链路框图；
下半：逐因子放大——1080p60 8bit → 4K60 10bit → 4K120 10bit 的带宽增长。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import warnings
warnings.filterwarnings("ignore")

OVH = 1.25


def demand(w, h, fps, bpp):
    """所需带宽 Gbps：像素数/秒 × 每像素位数 × 开销因子。"""
    return w * h * fps * bpp * OVH / 1e9


# ---------------- 画布 ----------------
fig = plt.figure(figsize=(7.2, 4.9))
gs = fig.add_gridspec(2, 1, height_ratios=[1.02, 1.0], hspace=0.42)
axT = fig.add_subplot(gs[0]); axT.axis("off")
axB = fig.add_subplot(gs[1])

# ================= 上半：公式链路 =================
boxes = [
    dict(t="① 像素总数/秒", f="宽 × 高 × 帧率",
         e="3840 × 2160 × 60\n≈ 4.98 亿 像素/秒", c=H.BLUE),
    dict(t="② 每像素位数", f="色深 × 通道 × 折扣",
         e="10 bit × 3 通道\n= 30 bit/像素", c=H.TEAL),
    dict(t="③ 开销因子", f="编码 + 同步间隙",
         e="8b/10b 约 1.25\n其他编码约 1.1", c=H.PURPLE),
    dict(t="④ 所需带宽", f="① × ② × ③",
         e="4K60 10bit 4:4:4\n≈ 18.7 Gbps", c=H.ORANGE),
]
bw, gap, x0 = 0.216, 0.052, 0.006
yl, bh = 0.30, 0.66
for i, b in enumerate(boxes):
    x = x0 + i * (bw + gap)
    axT.add_patch(FancyBboxPatch((x, yl), bw, bh,
                                 boxstyle="round,pad=0.006,rounding_size=0.02",
                                 fc="white", ec=b["c"], lw=1.6,
                                 transform=axT.transAxes, zorder=2))
    axT.text(x + bw / 2, yl + bh - 0.115, b["t"], ha="center", va="center",
             fontsize=9.6, color=b["c"], fontweight="bold", transform=axT.transAxes)
    axT.text(x + bw / 2, yl + bh - 0.335, b["f"], ha="center", va="center",
             fontsize=7.0, color="#4a5666", transform=axT.transAxes)
    axT.text(x + bw / 2, yl + 0.135, b["e"], ha="center", va="center",
             fontsize=7.0, color=b["c"], style="italic", transform=axT.transAxes)
    if i < 3:
        axT.text(x + bw + gap / 2, yl + bh / 2, "×", ha="center", va="center",
                 fontsize=14, color="#8b98a8", fontweight="bold",
                 transform=axT.transAxes)
# 等号（用竖线分隔第三、四块，表示"得出"）
axT.add_patch(FancyArrowPatch((0.0, 0.115), (1.0, 0.115),
                              arrowstyle="-|>", mutation_scale=13,
                              lw=1.2, color="#8b98a8", transform=axT.transAxes))
axT.text(0.5, 0.055, "所需带宽 ≈ 像素总数/秒 × 每像素位数 × 开销因子",
         ha="center", va="center", fontsize=9.4, color=H.DARK, fontweight="bold",
         transform=axT.transAxes)
axT.text(0.006, 1.02, "上半：一条公式拆成四块", ha="left", va="center",
         fontsize=9.6, color=H.NAVY, fontweight="bold", transform=axT.transAxes)

# ================= 下半：逐因子放大 =================
cases = [
    ("1080p60　8bit 4:4:4",  1920, 1080,  60, 24, H.BLUE,   "基准（SDR 小流量）"),
    ("4K60　8bit 4:4:4",     3840, 2160,  60, 24, H.TEAL,   "分辨率 ×4"),
    ("4K60　10bit 4:4:4",    3840, 2160,  60, 30, H.ORANGE, "色深 ×1.25"),
    ("4K120　10bit 4:4:4",   3840, 2160, 120, 30, H.RED,    "帧率 ×2"),
]
vals = [demand(c[1], c[2], c[3], c[4]) for c in cases]
labels = [c[0] for c in cases]
cols = [c[5] for c in cases]
notes = [c[6] for c in cases]

y = np.arange(len(cases))[::-1]
base = vals[0]
axB.barh(y, vals, height=0.56, color=cols, edgecolor="white", linewidth=0.8)
for yy, v, n in zip(y, vals, notes):
    wb = dict(boxstyle="square,pad=0.12", fc="white", ec="none", alpha=0.85)
    axB.text(v + 0.6, yy + 0.13, f"{v:.1f} Gbps", va="center", ha="left",
             fontsize=9.0, color=H.DARK, fontweight="bold", bbox=wb, zorder=6)
    axB.text(v + 0.6, yy - 0.22, n, va="center", ha="left",
             fontsize=7.2, color=H.GRAY, bbox=wb, zorder=6)
    if v != base:
        axB.text(0.9, yy, f"×{v/base:.2f}", va="center", ha="left",
                 fontsize=8.4, color="white", fontweight="bold", zorder=6)

# 接口能力线
for xv, c, lab in [(14.4, H.BLUE, "HDMI 2.0 有效 14.4"),
                   (25.9, H.TEAL, "DP 1.4 有效 25.9"),
                   (42.7, H.NAVY, "HDMI 2.1 有效 42.7")]:
    axB.axvline(xv, color=c, ls="--", lw=1.3, alpha=0.9)
    axB.text(xv, 3.52, lab, fontsize=7.4, color=c, va="center", ha="center",
             fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.16", fc="white", ec=c, lw=0.6, alpha=0.9))

axB.set_yticks(y)
axB.set_yticklabels(labels, fontsize=9.0)
axB.set_xlabel("所需带宽（Gbps，含约 1.25 开销）")
axB.set_xlim(0, 46)
axB.set_ylim(-0.6, 3.9)
axB.set_title("下半：三个因子一起长大，需求 10 倍起跳", fontsize=10.5, color=H.NAVY, pad=8)
axB.grid(axis="y", visible=False)
axB.grid(axis="x", color="#dde3ea", lw=0.7)

fig.suptitle("图 14-2　带宽是怎么算出来的：像素总数/秒 × 每像素位数 × 开销因子",
             fontsize=13, fontweight="bold", y=1.03)
fig.subplots_adjust(top=0.87, bottom=0.11, left=0.17, right=0.985)
H.save(fig, 14, "f3_bw_formula")
