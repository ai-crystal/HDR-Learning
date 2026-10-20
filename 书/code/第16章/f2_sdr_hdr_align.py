# -*- coding: utf-8 -*-
"""图 16-2　SDR 内容在 HDR 屏上的亮度对齐（「SDR 内容亮度」滑块的作用）

左panel：滑块位置 → SDR 白点实际亮度（对数轴，三块不同峰值显示器），
         标出 SDR 参考白点 100 nit、舒适区、显示峰值。
右panel：同一张 SDR 桌面在滑块过低 / 合适 / 过高时的观感示意。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

fig = plt.figure(figsize=(7.2, 4.3))
gs = fig.add_gridspec(1, 2, width_ratios=[1.55, 1.0], wspace=0.30)
ax = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

# ---------------- 左：滑块 → SDR 白点亮度 ----------------
s = np.linspace(0, 100, 400)
Lmin = 80.0                     # 滑块最小时的白点亮度（示意）
peaks = [600.0, 1000.0, 1600.0]
cols = [H.TEAL, H.NAVY, H.PURPLE]

for p, c in zip(peaks, cols):
    Lmax = 0.48 * p             # 滑块最大时的白点亮度（示意）
    L = Lmin * (Lmax / Lmin) ** (s / 100.0)
    ax.plot(s, L, color=c, lw=2.2, label=f"峰值 {int(p)} nit 的屏")
    ax.scatter([100], [Lmax], color=c, s=22, zorder=5)
    ax.annotate(f"{int(Lmax)}", xy=(100, Lmax), xytext=(-2, 6),
                textcoords="offset points", ha="right", va="bottom",
                fontsize=7.6, color=c, fontweight="bold")

# 舒适区
ax.axhspan(100, 200, color=H.GREEN, alpha=0.13, zorder=0)
ax.axhline(100, color=H.RED, lw=1.4, ls="--")
ax.text(2, 92, "SDR 参考白点 100 nit（第 1 章）", fontsize=7.0,
        color=H.RED, va="top", ha="left")
ax.text(78, 150, "舒适区 ≈100–200 nit", fontsize=7.8, color="#1d6b45",
        ha="center", va="center", fontweight="bold")
# 高亮带：1000 nit 屏 的 100~200 nit 对应的滑块区间
ax.axvspan(6, 33, color=H.ORANGE, alpha=0.10, zorder=0)
ax.text(19.5, 950, "对应滑块\n约 6–33", fontsize=7.2, color="#8a5a12",
        ha="center", va="center", linespacing=1.3)

ax.set_yscale("log")
ax.set_ylim(40, 1800)
ax.set_xlim(0, 100)
ax.set_xlabel("「SDR 内容亮度」滑块位置（%）")
ax.set_ylabel("SDR 白点实际显示亮度（nit）")
ax.set_title("滑块决定 SDR 白点落在哪里", fontsize=11.5)
ax.legend(loc="lower right", fontsize=8, ncol=1)
ax.text(98, 1500, "过高 → 刺眼发白", fontsize=8.2, color=H.RED,
        ha="right", fontweight="bold")
ax.text(2, 44, "过低 → 发灰发暗", fontsize=8.2, color=H.GRAY,
        ha="left", fontweight="bold")

# ---------------- 右：三种滑块位置的观感示意 ----------------
ax2.set_xlim(0, 10); ax2.set_ylim(0, 10)
ax2.axis("off"); ax2.grid(False)

ax2.set_title("同一张 SDR 桌面的三种观感", fontsize=11.5)

cases = [
    # 白区灰度, 标签, 说明, 颜色, 白点亮度示意
    (150, "滑块偏低", "发灰、发暗，文字对比弱", H.GRAY,   "≈ 90 nit"),
    (246, "滑块合适", "白得像以前开 SDR 一样", H.GREEN, "≈ 150 nit"),
    (255, "滑块偏高", "白得刺眼、颜色发飘", H.RED,   "≈ 400 nit"),
]
y0 = 8.60
for gray, tag, note, c, nit in cases:
    hrect = 1.55
    # 外框（桌面）
    ax2.add_patch(Rectangle((0.20, y0 - hrect), 5.45, hrect + 0.42,
                            facecolor="#2b3340", edgecolor=H.DARK, lw=1.0,
                            zorder=1))
    # 标题栏
    ax2.add_patch(Rectangle((0.20, y0 - 0.02), 5.45, 0.44,
                            facecolor="#3d4756", edgecolor=H.DARK, lw=0.8,
                            zorder=2))
    # 文档白区
    ax2.add_patch(Rectangle((0.60, y0 - hrect + 0.12), 3.55, hrect - 0.28,
                            facecolor=(gray / 255, gray / 255, gray / 255),
                            edgecolor="#889", lw=0.7, zorder=2))
    # 文本线条
    for i in range(4):
        lw_ = 2.4 if i != 3 else 1.6
        ax2.add_patch(Rectangle((0.85, y0 - hrect + 0.28 + i * 0.27), lw_, 0.09,
                                facecolor="#6a7480", zorder=3))
    # 标签
    ax2.text(5.90, y0 - hrect + 1.02, tag, fontsize=9.4, color=c,
             fontweight="bold", ha="left", va="center")
    ax2.text(5.90, y0 - hrect + 0.55, note, fontsize=7.0, color=H.DARK,
             ha="left", va="center")
    ax2.text(5.90, y0 - hrect + 0.18, f"白点 {nit}", fontsize=7.4,
             color=c, ha="left", va="center", fontweight="bold")
    y0 -= 2.90

ax2.text(0.20, 0.55,
         "滑块只改变 SDR 内容的白点高度，\n不改变 HDR 内容的映射范围",
         fontsize=7.3, color=H.NAVY, ha="left", va="center",
         fontweight="bold", linespacing=1.4)

H.save(fig, 16, "f2_sdr_hdr_align")
