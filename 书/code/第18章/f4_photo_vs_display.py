# -*- coding: utf-8 -*-
"""第 18 章 图 4：摄影的“HDR 合成” ≠ 显示 HDR。"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig = plt.figure(figsize=(7.2, 6.6))
gs = fig.add_gridspec(2, 2, height_ratios=[1.42, 1.0], hspace=0.34, wspace=0.40)
axL = fig.add_subplot(gs[0, 0]); axR = fig.add_subplot(gs[0, 1])
axT = fig.add_subplot(gs[1, 0]); axB = fig.add_subplot(gs[1, 1])

for a in (axL, axR):
    a.set_xlim(0, 100); a.set_ylim(0, 100); a.axis("off"); a.grid(False)


def rbox(a, x, y, w, h, fc, ec=None, lw=1.5, z=2):
    a.add_patch(FancyBboxPatch((x, y), w, h,
                               boxstyle="round,pad=0.3,rounding_size=1.4",
                               linewidth=lw, edgecolor=ec if ec else fc,
                               facecolor=fc, zorder=z))


def arrow(a, x1, y1, x2, y2, color=H.GRAY, lw=1.7, ms=8, z=4):
    a.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                mutation_scale=ms, linewidth=lw, color=color, zorder=z))


# ================= 左上：摄影 HDR 合成 =================
axL.set_title("① 摄影的“HDR 合成”：多张曝光拼进一张 SDR 图", fontsize=9.4,
              fontweight="bold", color=H.NAVY, pad=8)
brackets = [(-2.0, 0.05, 0.30), (0.0, 0.18, 0.62), (2.0, 0.42, 1.00)]
for i, (ev, lo, hi) in enumerate(brackets):
    g = np.linspace(lo, hi, 40)[None, :].repeat(28, axis=0)
    axL.imshow(g, cmap="gray", vmin=0, vmax=1, extent=[3 + i * 13, 14 + i * 13, 58, 88],
               aspect="auto", zorder=2)
    axL.text(8.5 + i * 13, 54, f"{ev:+.0f}EV", ha="center", va="top", fontsize=7.4,
             color=H.NAVY, fontweight="bold")
axL.text(27.5, 91, "同一场景 · 不同曝光", ha="center", va="bottom", fontsize=7.0,
         color="#444")
for gx in (16.6, 29.6):
    axL.text(gx, 71, "+", ha="center", va="center", fontsize=11, color=H.GRAY)
arrow(axL, 44.5, 73, 49.5, 73, color=H.NAVY)
axL.text(47.0, 76.5, "合成", ha="center", va="bottom", fontsize=6.8, color=H.NAVY)

g = np.linspace(0.10, 0.92, 40)[None, :].repeat(28, axis=0)
axL.imshow(g, cmap="gray", vmin=0, vmax=1, extent=[50, 64, 58, 88], aspect="auto", zorder=2)
axL.text(57, 54, "一张 SDR 图", ha="center", va="top", fontsize=6.6, color="#444")
arrow(axL, 65.5, 73, 70.5, 73, color=H.NAVY)
axL.text(68.0, 76.5, "导出", ha="center", va="bottom", fontsize=6.8, color=H.NAVY)

rbox(axL, 71.5, 58, 27, 30, "white", ec=H.NAVY, lw=1.8)
axL.text(85, 82.5, "普通 JPEG", ha="center", va="center", fontsize=8.6,
         fontweight="bold", color=H.NAVY)
axL.text(85, 76.0, "sRGB / 8bit", ha="center", va="center", fontsize=7.2, color="#333")
axL.text(85, 70.5, "SDR 容器", ha="center", va="center", fontsize=7.2, color="#333")
axL.text(85, 64.5, "≈100 nit 峰值", ha="center", va="center", fontsize=7.2, color=H.RED)

rbox(axL, 3, 8, 95.5, 38, "#eef4fa", ec=H.LGRAY, lw=1.2, z=1)
axL.text(50.75, 39.0, "本质：把多张照片的信息“压”进一张普通图像", ha="center", va="center",
         fontsize=7.8, color=H.NAVY, fontweight="bold")
axL.text(50.75, 28.0, "· 做的是拍摄与后期技巧（多张曝光合成一张）\n"
                      "· 最终仍是一张 8bit SDR 图片，用普通屏幕看\n"
                      "· 不需要 HDR 显示器，也没有 PQ / 元数据",
         ha="center", va="center", fontsize=7.0, color="#333", linespacing=1.9)

# ================= 右上：显示 HDR =================
axR.set_title("② 显示 HDR：需要整条链路的真体系", fontsize=9.4,
              fontweight="bold", color=H.TEAL, pad=8)
rbox(axR, 16, 84, 68, 12, "white", ec=H.TEAL, lw=1.8)
axR.text(50, 92.5, "HDR 母版（PQ）", ha="center", va="center", fontsize=8.4,
         fontweight="bold", color=H.TEAL)
axR.text(50, 87.5, "拍摄 / 渲染 / 调色，按绝对光定亮度", ha="center", va="center",
         fontsize=6.8, color="#333")
arrow(axR, 50, 83, 50, 78, color=H.TEAL)

rbox(axR, 8, 66, 84, 12, H.TEAL, z=2)
axR.text(50, 74.4, "编码：PQ + 10bit + BT.2020 容器", ha="center", va="center",
         fontsize=7.8, fontweight="bold", color="white", zorder=3)
axR.text(50, 69.4, "元数据（MaxCLL / MaxFALL）随码流传输", ha="center",
         va="center", fontsize=6.6, color="white", zorder=3)
arrow(axR, 50, 65, 50, 60, color=H.TEAL)

rbox(axR, 8, 48, 84, 12, "white", ec=H.TEAL, lw=1.8)
axR.text(50, 56.4, "传输：HDMI / DP + HDCP 2.2", ha="center", va="center",
         fontsize=8.0, fontweight="bold", color=H.TEAL)
axR.text(50, 51.4, "带宽要够，否则退 8bit 或降色度采样", ha="center", va="center",
         fontsize=6.8, color="#333")
arrow(axR, 50, 47, 50, 42, color=H.TEAL)

rbox(axR, 8, 22, 84, 20, "white", ec=H.RED, lw=1.8)
axR.text(50, 37.0, "HDR 显示器：真的发更亮、更纯的光", ha="center", va="center",
         fontsize=8.4, fontweight="bold", color=H.RED)
axR.text(50, 31.0, "PQ / HLG 反变换 → 峰值可到 600–1000+ nit", ha="center", va="center",
         fontsize=7.0, color="#333")
axR.text(50, 25.5, "没有 HDR 屏 → 只能靠色调映射（第 17 章）", ha="center",
         va="center", fontsize=7.0, color="#333")

rbox(axR, 3, 8, 95.5, 11, "#eaf7f3", ec=H.TEAL, lw=1.2, z=1)
axR.text(50.75, 13.5, "10bit 让暗部不出现色带；元数据决定“怎么映射”", ha="center",
         va="center", fontsize=7.6, color="#0d6b58", fontweight="bold")

# ================= 左下：两栏对照表 =================
axT.axis("off"); axT.grid(False)
axT.set_title("一张表看懂区别", fontsize=9.6, fontweight="bold", color=H.DARK, pad=8)
items = [
    ("目的", "一张图塞更多层次", "让屏幕发光更亮"),
    ("载体", "普通 JPEG / RAW", "PQ 10bit 视频流"),
    ("需要 HDR 屏吗", "不需要", "需要（靠映射）"),
    ("关键词", "多张曝光合成", "PQ + 元数据 + 色域"),
    ("看的人看到", "≈100 nit 一张图", "1000 nit 的高光"),
]
axT.text(33, 96, "摄影 HDR 合成", ha="left", va="center", fontsize=8.6,
         fontweight="bold", color=H.NAVY, transform=axT.transData)
axT.text(70, 96, "显示 HDR", ha="left", va="center", fontsize=8.6,
         fontweight="bold", color=H.TEAL, transform=axT.transData)
for i, (k, a, b) in enumerate(items):
    y = 86 - i * 18
    if i % 2 == 0:
        axT.add_patch(plt.Rectangle((0.2, y - 8), 99.6, 15, facecolor="#f6f8fa",
                                    edgecolor="none", transform=axT.transData, zorder=0))
    axT.text(1, y, k, ha="left", va="center", fontsize=7.2, color=H.DARK,
             fontweight="bold", transform=axT.transData)
    axT.text(33, y, a, ha="left", va="center", fontsize=6.9, color=H.NAVY,
             transform=axT.transData)
    axT.text(70, y, b, ha="left", va="center", fontsize=6.9, color="#0d6b58",
             transform=axT.transData)
axT.axvline(68, ymin=0.02, ymax=0.97, color=H.LGRAY, lw=1.0)
axT.set_xlim(0, 100); axT.set_ylim(0, 100)

# ================= 右下：亮度范围对比 =================
code = np.linspace(0, 1, 256)
axB.semilogx(np.clip(H.pq_eotf(code), 0.01, None), code * (2 ** 10 - 1),
             color=H.ORANGE, lw=2.2, label="PQ（10bit，0–1023 码值）")
axB.semilogx(np.clip(H.srgb_eotf(code) * 100, 0.01, None), code * 255,
             color=H.NAVY, lw=2.2, label="sRGB / SDR（8bit，0–255 码值）")
axB.axvspan(0.01, 100, color=H.NAVY, alpha=0.05, zorder=0)
axB.axvspan(100, 30000, color=H.ORANGE, alpha=0.07, zorder=0)
axB.text(0.016, 55, "SDR 区间\n≤100 nit", fontsize=6.4, color=H.NAVY,
         va="bottom", ha="left", linespacing=1.4)
axB.text(115, 55, "HDR 高光区间\n100 → 10000 nit", fontsize=6.4, color=H.ORANGE,
         va="bottom", ha="left", linespacing=1.4, fontweight="bold")
axB.set_xlim(0.01, 30000); axB.set_ylim(0, 1100)
from matplotlib.ticker import FixedLocator, FuncFormatter
axB.xaxis.set_major_locator(FixedLocator([0.01, 0.1, 1, 10, 100, 1000, 10000]))
axB.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
axB.xaxis.set_minor_formatter(FuncFormatter(lambda v, p: ""))
axB.set_xlabel("显示亮度（nit，对数轴）", fontsize=8.6)
axB.set_ylabel("码值", fontsize=8.6)
axB.set_title("同样的“HDR”，容量完全不同", fontsize=9.6, fontweight="bold",
              color=H.DARK)
axB.legend(fontsize=6.8, loc="upper left")
axB.tick_params(labelsize=7.6)

axL.set_xlim(0, 100); axL.set_ylim(0, 100)
axR.set_xlim(0, 100); axR.set_ylim(0, 100)

H.save(fig, 18, "f4_photo_vs_display")
