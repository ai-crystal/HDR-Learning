# -*- coding: utf-8 -*-
"""第 12 章 图 3：色相刻度在四种度量里的重分配。

固定 L* 与 C*_ab，沿 CIELAB 的等色相射线取 72 个方向（每 5 度一个），把每个
色样转成绝对 XYZ，再读各空间自己的色相角。左图画的是减去圆周均值之后的偏差，
右图是相邻两个色样之间的角步长与 CIELAB 的 5 度之比。
CIELAB 在 C*=50 处几乎是一条平线，这不是巧合，参照就是它。
"""
import os
import sys
import numpy as np

sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metrics as M

plt = H.plt

WHITE_LUM = 203.0
L_STAR, C_STAR = 60.0, 50.0
mm = M.Metrics(white_lum=WHITE_LUM)

hs = np.arange(0.0, 360.0, 5.0)
xyz = M.lab_to_xyz(M.lch_to_lab(np.full_like(hs, L_STAR),
                                np.full_like(hs, C_STAR), hs), white_ref=WHITE_LUM)

CURVES = [
    ("CAM16  $h$", "16", H.PURPLE),
    ("Jzazbz  $h_z$", "jz", H.TEAL),
    ("ICtCp  $\\arctan(C_p/C_t)$", "itp", H.ORANGE),
]

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.5),
                         gridspec_kw=dict(wspace=0.26))

ax = axes[0]
for name, key, col in CURVES:
    h = M.hue_in(key, xyz, mm)
    d = (h - hs + 180.0) % 360.0 - 180.0
    ang = np.radians(d)
    mean = np.degrees(np.arctan2(np.sin(ang).mean(), np.cos(ang).mean()))
    d = (d - mean + 180.0) % 360.0 - 180.0
    ax.plot(hs, d, color=col, lw=1.9, label=name)
ax.axhline(0, color=H.NAVY, lw=1.3, ls=(0, (5, 3)), label="CIELAB 参照")
ax.set_xlim(0, 360)
ax.set_xticks([0, 60, 120, 180, 240, 300, 360])
ax.set_xlabel("CIELAB 色相角 $h_{ab}$ / °")
ax.set_ylabel("色相偏差（减去圆周均值）/ °")
ax.set_ylim(-34, 28)

ax = axes[1]
for name, key, col in CURVES:
    h = M.hue_in(key, xyz, mm)
    d = np.unwrap(np.radians(h))
    step = np.diff(d) / np.radians(5.0)
    ax.plot(hs[:-1] + 2.5, step, color=col, lw=1.9, label=name)
ax.axhline(1.0, color=H.NAVY, lw=1.3, ls=(0, (5, 3)))
ax.set_xlim(0, 360)
ax.set_xticks([0, 60, 120, 180, 240, 300, 360])
ax.set_xlabel("CIELAB 色相角 $h_{ab}$ / °")
ax.set_ylabel("角步长比（对 $h_{ab}$ 的 5° 步长归一）")
ax.set_ylim(0.35, 1.9)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=8.2,
           handlelength=1.6, columnspacing=1.5, frameon=False,
           bbox_to_anchor=(0.5, -0.10))

H.save(fig, 12, "f3_hue_scale")
