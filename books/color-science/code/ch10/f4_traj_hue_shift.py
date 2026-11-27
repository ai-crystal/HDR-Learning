# -*- coding: utf-8 -*-
"""第 10 章 图 4：三类映射在 a*b* 平面上的落点轨迹与色相偏移。

(a) 固定 L* = 55、色相 262 度，在 BT.2020 上取 8 个彩度递增的源色，
    分别用逐通道裁剪、等色相裁剪、膝形压缩映射到 Display P3，把落点连成轨迹。
(b) 逐通道裁剪造成的色相偏移随色相角的变化（与等色相/膝形的零偏移对比）。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cslib as L

plt = H.plt

fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.0),
                         gridspec_kw={"width_ratios": [1.1, 1.0], "wspace": 0.34})

LL, HUE = 55.0, 262.0

# ---------------- (a) 四个色相方向上的落点轨迹 ----------------
ax = axes[0]
for g, col, ls, lab in (("BT2020", H.GRAY, (0, (4, 3)), "BT.2020 边界"),
                        ("P3", H.NAVY, "-", "Display P3 边界")):
    hs, cs = L.gamut_ring(LL, g, n_hue=180)
    ok = np.isfinite(cs)
    pts = np.array([L.lch_to_lab([LL, c, h]) for h, c in zip(hs[ok], cs[ok])])
    ax.plot(np.append(pts[:, 1], pts[0, 1]), np.append(pts[:, 2], pts[0, 2]),
            color=col, lw=1.5, ls=ls, label=lab, zorder=2)

for hue, base_col in ((35.0, H.RED), (145.0, H.TEAL), (262.0, H.PURPLE), (315.0, H.ORANGE)):
    c_lim = L.cmax(LL, hue, "P3")
    if not np.isfinite(c_lim):
        continue
    src_cs = np.linspace(0.6 * c_lim, 1.45 * c_lim, 7)
    src_lab = np.array([L.lch_to_lab([LL, c, hue]) for c in src_cs])
    clip = np.array([L.clip_target(x, "P3") for x in src_lab])
    hcl = np.array([L.hue_clip(x, "P3") for x in src_lab])
    ax.plot(src_lab[:, 1], src_lab[:, 2], "o", ms=3.4, color=base_col,
            mec="white", mew=0.5, alpha=0.85, zorder=5)
    ax.plot(clip[:, 1], clip[:, 2], "-", marker="s", ms=4.0, color=base_col,
            lw=1.2, zorder=6)
    ax.plot(hcl[:, 1], hcl[:, 2], ":", marker="^", ms=3.6, color=base_col,
            lw=1.0, zorder=7)

# 图例代理
from matplotlib.lines import Line2D
handles = [
    Line2D([], [], color=H.GRAY, ls=(0, (4, 3)), lw=1.5, label="BT.2020 边界"),
    Line2D([], [], color=H.NAVY, lw=1.5, label="Display P3 边界"),
    Line2D([], [], color=H.DARK, marker="o", ls="", ms=3.6, label="源色"),
    Line2D([], [], color=H.DARK, marker="s", ls="-", ms=4.0, label="逐通道裁剪"),
    Line2D([], [], color=H.DARK, marker="^", ls=":", ms=3.6, label="等色相裁剪"),
]
ax.legend(handles=handles, loc="upper left", fontsize=7.2, handlelength=1.6,
          framealpha=0.92)

ax.set_xlabel("$a^*$")
ax.set_ylabel("$b^*$")
ax.set_title("(a) $L^*=55$ 上四个色相方向的落点", fontsize=10.2, pad=6)
ax.set_aspect("equal", adjustable="datalim")
ax.tick_params(labelsize=8.5)

# ---------------- (b) 色相偏移 ----------------
ax = axes[1]
hues = np.arange(0, 360, 30.0)
shift = []
for h in hues:
    c_l = L.cmax(LL, h, "P3")
    if not np.isfinite(c_l) or c_l <= 0:
        shift.append(0.0)
        continue
    lab_s = L.lch_to_lab([LL, 1.3 * c_l, h])
    out = L.clip_target(lab_s, "P3")
    h_out = np.degrees(np.arctan2(out[2], out[1])) % 360
    shift.append(L.hue_diff(h_out, h))

ax.bar(hues, shift, width=8.0, color=[H.RED if abs(s) > 2 else H.GRAY for s in shift],
       edgecolor="white", linewidth=0.6, zorder=3)
ax.axhline(2.0, color=H.NAVY, lw=1.0, ls=(0, (4, 3)), zorder=1)
ax.axhline(-2.0, color=H.NAVY, lw=1.0, ls=(0, (4, 3)), zorder=1)
ax.text(3, 2.6, "±2° 可察觉线", fontsize=7.6, color=H.NAVY)
ax.set_xlabel("色相角 $h_{ab}$（°）")
ax.set_ylabel("逐通道裁剪后的色相偏移（°）")
ax.set_title("(b) 色相偏移随色相角的变化", fontsize=10.2, pad=6)
ax.set_xlim(-12, 350)
ax.set_xticks(np.arange(0, 361, 60))
ax.tick_params(labelsize=8.5)
ax.grid(axis="y", alpha=0.45, zorder=0)

H.save(fig, 10, "f4_traj_hue_shift")
