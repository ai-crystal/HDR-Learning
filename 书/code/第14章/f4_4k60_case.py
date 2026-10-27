# -*- coding: utf-8 -*-
"""第 14 章 图 14-3：4K60 的带宽算例分解。
左：三种 4K60 组合的"纯像素位 + 协议开销"堆叠柱，叠加接口能力线；
右：每像素位数是怎么来的（通道位宽分解，含 4:2:0 的色度折扣）。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt

PX = 3840 * 2160 * 60          # 像素总数/秒 = 4.98 亿
OVH = 0.25                     # 协议开销约 25%

# (名称, 每像素位数, 颜色, 是否放得下 HDMI 2.0)
cases = [
    ("4K60\n8bit 4:4:4",   24, H.TEAL,   True),
    ("4K60\n10bit 4:2:0",  15, H.GREEN,  True),
    ("4K60\n10bit 4:4:4",  30, H.ORANGE, False),
]

fig = plt.figure(figsize=(7.2, 4.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1.72, 1.0], wspace=0.34)
ax = fig.add_subplot(gs[0])
axR = fig.add_subplot(gs[1])

# ================= 左图：总带宽堆叠 =================
y = np.arange(len(cases))[::-1]
for yy, (name, bpp, c, ok) in zip(y, cases):
    raw = PX * bpp / 1e9                      # 纯像素位
    ovh = raw * OVH                           # 协议开销
    ax.barh(yy, raw, height=0.55, color=c, edgecolor="white", linewidth=0.7)
    ax.barh(yy, ovh, left=raw, height=0.55, color="white", edgecolor=c,
            linewidth=1.3, hatch="///", alpha=0.95)
    ax.text(raw / 2, yy, f"{raw:.1f}", ha="center", va="center",
            fontsize=8.4, color="white", fontweight="bold")
    ax.text(raw + ovh + 0.7, yy, f"{raw + ovh:.1f} Gbps", ha="left", va="center",
            fontsize=9.2, color=H.DARK, fontweight="bold", zorder=6,
            bbox=dict(boxstyle="square,pad=0.10", fc="white", ec="none", alpha=0.8))

# 接口能力线
for xv, c, lab, ty in [(18.0, H.ORANGE, "HDMI 2.0　18", 2.45),
                       (25.9, H.TEAL, "DP 1.4 有效　25.9", 2.63),
                       (48.0, H.NAVY, "HDMI 2.1　48", 2.45)]:
    ax.axvline(xv, color=c, ls="--", lw=1.4, zorder=4)
    ax.text(xv, ty, lab, fontsize=7.4, color=c, va="center",
            ha="center", fontweight="bold", zorder=5,
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec=c, lw=0.6, alpha=0.92))

# 结论注记
ax.annotate("超出 0.7 Gbps\n→ HDMI 2.0 装不下", xy=(18.0, 0.05), xytext=(29, 1.15),
            fontsize=8.2, color=H.RED, ha="left", va="center", fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.3,
                            connectionstyle="arc3,rad=-0.2"), zorder=7,
            bbox=dict(boxstyle="round,pad=0.28", fc="#fdf1ec", ec=H.RED, lw=0.9))

ax.set_yticks(y)
ax.set_yticklabels([c[0] for c in cases], fontsize=8.8)
ax.set_xlabel("所需带宽（Gbps）")
ax.set_xlim(0, 54)
ax.set_ylim(-0.62, 2.82)
ax.set_title("左：三种 4K60 组合的带宽账", fontsize=10.5, color=H.NAVY, pad=8)
ax.grid(axis="y", visible=False)
ax.grid(axis="x", color="#dde3ea", lw=0.7)
ax.text(0.985, 0.10, "实心 = 纯像素位　斜纹 = 协议开销约 25%",
        transform=ax.transAxes, ha="right", va="center", fontsize=7.4, color=H.GRAY)

# ================= 右图：每像素位数来源 =================
groups = ["8bit\n4:4:4", "10bit\n4:4:4", "10bit\n4:2:0"]
segs = [
    [("R 8", 8, H.RED), ("G 8", 8, H.GREEN), ("B 8", 8, H.BLUE)],
    [("R 10", 10, H.RED), ("G 10", 10, H.GREEN), ("B 10", 10, H.BLUE)],
    [("Y 10", 10, H.GOLD), ("Cb 2.5", 2.5, H.PURPLE), ("Cr 2.5", 2.5, H.PURPLE)],
]
x = np.arange(len(groups))
for xi, ss in zip(x, segs):
    bot = 0.0
    for name, v, c in ss:
        axR.bar(xi, v, bottom=bot, width=0.56, color=c, edgecolor="white", linewidth=0.9)
        axR.text(xi, bot + v / 2, name, ha="center", va="center", fontsize=7.6,
                 color="white", fontweight="bold")
        bot += v
    axR.text(xi, bot + 0.7, f"{bot:g} bit/像素", ha="center", va="bottom",
             fontsize=9.0, color=H.DARK, fontweight="bold")

axR.text(2, 21, "色度降为\n1/4 采样", ha="center", va="center", fontsize=7.4,
         color=H.PURPLE,
         bbox=dict(boxstyle="round,pad=0.24", fc="#f6f0fb", ec=H.PURPLE, lw=0.8))
axR.annotate("", xy=(2, 15.6), xytext=(2, 19.6),
             arrowprops=dict(arrowstyle="->", color=H.PURPLE, lw=1.1))
axR.set_xticks(x)
axR.set_xticklabels(groups, fontsize=8.6)
axR.set_ylabel("每像素位数（bit）")
axR.set_ylim(0, 38)
axR.set_xlim(-0.6, 2.6)
axR.set_title("右：位数的来源", fontsize=10.5, color=H.NAVY, pad=8)
axR.grid(axis="x", visible=False)
axR.grid(axis="y", color="#dde3ea", lw=0.7)

fig.suptitle("图 14-3　4K60 算例：10bit 4:4:4 要 18.7 Gbps，恰好卡在 HDMI 2.0 之上",
             fontsize=12.6, fontweight="bold", y=1.02)
fig.subplots_adjust(top=0.85, bottom=0.14, left=0.115, right=0.985)
H.save(fig, 14, "f4_4k60_case")
