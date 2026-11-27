# -*- coding: utf-8 -*-
"""第 05 章 图 5：插值路径与色相折返。

左图：同一对端点色在 RGB 线性插值、CIELAB 直角坐标插值、LCh 极坐标插值下
      走过的路径（a*b* 平面），端点色取自 sRGB 的深蓝与亮黄。
右图：色相角从 350° 插到 10° 时，直线插值会绕经 180°（青绿），
      折返处理才会走 0°（红）这条短路。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import gamut as G
import cie1931 as S

plt = H.plt

A_RGB = np.array([0.05, 0.10, 0.55])
B_RGB = np.array([0.95, 0.90, 0.20])
T = np.linspace(0, 1, 120)

fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.85),
                         gridspec_kw=dict(width_ratios=[1.10, 1.0], wspace=0.30))
fig.subplots_adjust(left=0.085, right=0.985, top=0.90, bottom=0.16)

# ---------------- (a) 三条插值路径 ----------------
ax = axes[0]
lab_a = np.atleast_2d(G.rgb_to_lab(A_RGB, "sRGB"))[0]
lab_b = np.atleast_2d(G.rgb_to_lab(B_RGB, "sRGB"))[0]

# RGB 线性
rgb_path = A_RGB[None, :] * (1 - T)[:, None] + B_RGB[None, :] * T[:, None]
lab_rgb = G.rgb_to_lab(rgb_path, "sRGB")
# Lab 直角坐标线性
lab_lin = lab_a[None, :] * (1 - T)[:, None] + lab_b[None, :] * T[:, None]
# LCh 极坐标（短弧）
La, Ca, ha = G.lab_to_lch(lab_a)
Lb, Cb, hb = G.lab_to_lch(lab_b)
dh = ((hb - ha + 180) % 360) - 180
lab_lch = G.lch_to_lab(La + (Lb - La) * T, Ca + (Cb - Ca) * T, ha + dh * T)

for path, col, ls, lab in [(lab_rgb, H.RED, "-", "RGB 线性插值"),
                           (lab_lin, H.GRAY, (0, (4, 2)), "CIELAB 直角坐标插值"),
                           (lab_lch, H.TEAL, "-", "LCh 极坐标插值")]:
    ax.plot(path[:, 1], path[:, 2], color=col, ls=ls, lw=1.9, label=lab, zorder=3)
    ax.plot(path[::12, 1], path[::12, 2], "o", ms=3.4, mfc=col, mec=col, zorder=4)

for lab, name in [(lab_a, "深蓝"), (lab_b, "亮黄")]:
    ax.plot(lab[1], lab[2], "o", ms=8.0, mfc="white", mec="#2b3a4a", mew=1.5, zorder=5)

ax.annotate("深蓝", xy=(lab_a[1], lab_a[2]), xytext=(54, -54),
            fontsize=8.0, color="#2b3a4a",
            arrowprops=dict(arrowstyle="-", color="#9aa7b5", lw=0.8,
                            shrinkA=2, shrinkB=4))
ax.annotate("亮黄", xy=(lab_b[1], lab_b[2]), xytext=(-52, 50),
            fontsize=8.0, color="#2b3a4a",
            arrowprops=dict(arrowstyle="-", color="#9aa7b5", lw=0.8,
                            shrinkA=2, shrinkB=4))
ax.annotate("RGB 插值贴着灰轴走", xy=(2.0, 4.0), xytext=(-68, -22),
            fontsize=7.4, color=H.RED, ha="left",
            arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=0.9,
                            shrinkA=2, shrinkB=4))
ax.axhline(0, color="#e2e7ed", lw=0.9, zorder=1)
ax.axvline(0, color="#e2e7ed", lw=0.9, zorder=1)
ax.set_xlim(-72, 74)
ax.set_ylim(-60, 58)
ax.set_xlabel("$a^*$", fontsize=10)
ax.set_ylabel("$b^*$", fontsize=10)
ax.legend(loc="lower left", fontsize=7.4, handletextpad=0.6, borderpad=0.35)

# ---------------- (b) 色相折返 ----------------
ax2 = axes[1]
t = np.linspace(0, 1, 200)
h_start, h_end = 350.0, 10.0
dh_short = ((h_end - h_start + 180) % 360) - 180        # 20°
h_wrap = h_start + dh_short * t                          # 350 -> 380，跨过 360
h_naive = h_start + (h_end - h_start) * t                # 350 -> 10，绕经 180

ax2.plot(t, h_naive, "-", color=H.RED, lw=2.0, label="直线插值（绕经青绿）")
ax2.plot(t, h_wrap, "-", color=H.TEAL, lw=2.0, label="折返处理（经 0°）")
ax2.axhline(180, color="#c2cad4", lw=0.8, ls=(0, (3, 3)))
ax2.axhline(360, color="#c2cad4", lw=0.8, ls=(0, (3, 3)))
ax2.text(0.015, 363, "360° 即 0°", fontsize=7.2, color="#6b7886", va="bottom")
ax2.set_xlim(0, 1)
ax2.set_ylim(-6, 402)
ax2.set_xlabel("插值位置 $t$", fontsize=9.5)
ax2.set_ylabel("色相角 $h_{ab}$（°）", fontsize=9.5)
ax2.set_yticks([0, 60, 120, 180, 240, 300, 360])
ax2.legend(loc="lower left", fontsize=7.6, handletextpad=0.6, borderpad=0.35)
ax2.text(0.015, 186, "180°：青绿", fontsize=7.2, color="#6b7886", va="bottom")

H.save(fig, 5, "f5_interp_hue_wrap")
