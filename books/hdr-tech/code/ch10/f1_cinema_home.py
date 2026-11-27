# -*- coding: utf-8 -*-
"""第 10 章 图 1：影院与家庭的亮度账、银幕的角分布。

左：几种放映与显示条件的亮度跨度（横轴对数）。每一行的横条从黑位画到峰值，
    标注峰值数字。虚线是 BT.2408 的 HDR 参考白 203 cd/m²。
    （增益 1.0 → 半增益 60°，典型家用漫反射幕；增益 1.8/2.4 → 30°/22°，
    对应影院高增益幕与 3D 金属幕）。曲线按轴上亮度归一化。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(9.0, 4.2), gridspec_kw={"width_ratios": [1.18, 1.0]})
fig.subplots_adjust(left=0.175, right=0.975, bottom=0.145, top=0.955, wspace=0.30)

# ---------------- (a) 亮度跨度 ----------------
rows = [
    ("家庭 SDR 显示", 100, 0.05, H.GRAY, "100"),
    ("家庭 HDR 显示", 1000, 0.005, H.NAVY, "1000"),
    ("DCI 影院 2D", 48, 0.024, H.TEAL, "48"),
    ("DCI 影院 3D", 12, 0.006, H.ORANGE, "12"),
    ("Dolby Cinema", 108, 0.0001, H.RED, "108"),
]
ypos = np.arange(len(rows))[::-1]

for y, (name, peak, black, c, lab) in zip(ypos, rows):
    ax1.plot([black, peak], [y, y], color=c, lw=7.0, solid_capstyle="butt", alpha=0.85, zorder=3)
    ax1.plot([peak], [y], marker="o", ms=6.5, color=c, mec="white", mew=1.1, zorder=5)
    if peak < 200:
        ax1.text(peak * 1.55, y, lab, fontsize=8.6, color=c, va="center", ha="left",
                 fontweight="bold")
    else:
        ax1.text(peak * 0.55, y, lab, fontsize=8.6, color="white", va="center", ha="right",
                 fontweight="bold", zorder=6)

ax1.axvline(203, color=H.GRAY, lw=1.0, ls=(0, (4, 3)), zorder=1)
ax1.text(203 * 1.15, len(rows) - 0.42, "203　BT.2408 参考白", fontsize=7.8, color=H.GRAY,
         va="center", ha="left")

ax1.set_yticks(ypos)
ax1.set_yticklabels([r[0] for r in rows], fontsize=9.2)
ax1.set_xscale("log")
ax1.set_xlim(5e-5, 1.2e4)
ax1.set_ylim(-0.7, len(rows) + 0.05)
ax1.set_xlabel("亮度（cd/m$^2$，对数刻度）")
ax1.set_xticks([1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1000])
ax1.set_xticklabels(["1e-4", "1e-3", "1e-2", "0.1", "1", "10", "100", "1000"])
ax1.minorticks_off()
ax1.grid(axis="y", visible=False)
ax1.set_title("(a) 亮度跨度", fontsize=10.5, pad=6)

# ---------------- (b) 银幕角分布 ----------------
theta = np.linspace(0, 75, 400)
curves = [(1.0, 60.0, H.GRAY, "增益 1.0", (46, 0.79)),
          (1.8, 30.0, H.TEAL, "增益 1.8", (49, 0.40)),
          (2.4, 22.0, H.RED, "增益 2.4", (38, 0.145))]
for gain, half, c, lab, (tx, ty) in curves:
    n = np.log(0.5) / np.log(np.cos(np.deg2rad(half)))
    r = np.cos(np.deg2rad(theta)) ** n
    ax2.plot(theta, r, color=c, lw=2.2, zorder=3)
    ax2.text(tx, ty, lab, fontsize=8.2, color=c, ha="left", va="bottom",
             bbox=dict(facecolor="white", edgecolor="none", pad=1.2), zorder=6)

ax2.axhline(0.5, color=H.LGRAY, lw=1.0, ls=(0, (3, 3)), zorder=1)
ax2.text(73, 0.52, "-3 dB", fontsize=7.8, color=H.GRAY, ha="right", va="bottom")

ax2.axvline(30, color=H.ORANGE, lw=0.9, ls=(0, (5, 2)), zorder=1)
ax2.text(31.5, 1.10, "影院侧座约 ±30°", fontsize=7.8, color=H.ORANGE, ha="left", va="top")

ax2.set_xlim(0, 75)
ax2.set_ylim(0, 1.18)
ax2.set_xlabel("偏离银幕法线的角度（度）")
ax2.set_ylabel("相对轴上亮度")
ax2.set_xticks([0, 15, 30, 45, 60, 75])
ax2.set_title("(b) 银幕角分布", fontsize=10.5, pad=6)

H.save(fig, 10, "f1_cinema_home")
