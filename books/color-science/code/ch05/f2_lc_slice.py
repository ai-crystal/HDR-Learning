# -*- coding: utf-8 -*-
"""第 05 章 图 2：同一色相（CIELAB 色相角 30°）下三个色域的 L*–C 边界。

边界用二分法求解：固定 L* 与色相角 h，在彩度方向二分，找到仍落在 RGB 立方体内的
最大彩度（判据为线性 RGB 三分量都在 [0, 1] 内，容差 1e-6）。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import gamut as G

plt = H.plt

HUE = 30.0
W = G.xy_to_xyz(*G.WHITE_XY["D65"], 1.0)


def lab_to_xyz(Lab):
    fy = (Lab[0] + 16.0) / 116.0
    fx = fy + Lab[1] / 500.0
    fz = fy - Lab[2] / 200.0
    d = 6.0 / 29.0

    def fi(t):
        return np.where(t > d, t ** 3, 3 * d * d * (t - 4.0 / 29.0))

    return np.stack([fi(fx), fi(fy), fi(fz)], -1) * W


def inv_matrix(name):
    return np.linalg.inv(G.rgb_to_xyz_matrix(G.PRIMARIES[name], "D65"))


def in_gamut(Lab, Minv, eps=1e-6):
    rgb = lab_to_xyz(Lab) @ Minv.T
    return rgb.min() >= -eps and rgb.max() <= 1.0 + eps


def cmax(L, Minv, h=HUE):
    hr = np.radians(h)
    lo, hi = 0.0, 210.0
    if not in_gamut([L, 0.0, 0.0], Minv):
        return np.nan
    if in_gamut([L, hi * np.cos(hr), hi * np.sin(hr)], Minv):
        return hi
    for _ in range(48):
        mid = 0.5 * (lo + hi)
        if in_gamut([L, mid * np.cos(hr), mid * np.sin(hr)], Minv):
            lo = mid
        else:
            hi = mid
    return lo


LS = np.arange(1.0, 100.0, 0.5)
fig = plt.figure(figsize=(6.6, 4.9))
ax = fig.add_axes([0.10, 0.20, 0.87, 0.76])

STYLE = [("sRGB", H.NAVY, (0, (6, 3)), "sRGB"), ("P3", H.ORANGE, "-", "Display P3"),
         ("BT2020", H.TEAL, "-", "BT.2020")]
curves = {}
for name, col, ls, lab in STYLE:
    Minv = inv_matrix(name)
    Cs = np.array([cmax(L, Minv) for L in LS])
    curves[name] = Cs
    ax.plot(Cs, LS, color=col, lw=2.2, ls=ls, zorder=3)
    i = int(np.nanargmax(Cs))
    ax.plot([Cs[i]], [LS[i]], "o", ms=6.2, mfc="white", mec=col, mew=1.6, zorder=4)

# ---------- P3 与 BT.2020 之间的彩度带 ----------
ax.fill_betweenx(LS, curves["P3"], curves["BT2020"], color=H.TEAL, alpha=0.10,
                 zorder=2, lw=0)
ax.text(120, 34, "BT.2020 能显示、\nP3 无法复现的彩度", fontsize=7.8, color="#0f5f50",
        ha="center", va="center")

# ---------- 尖点数值：集中放在右下空白，不用引线 ----------
ax.text(103, 16.5, "尖点（$C$, $L^*$）", fontsize=8.0, color="#39485a", ha="left")
for k, (name, col, _, lab) in enumerate(STYLE):
    i = int(np.nanargmax(curves[name]))
    ax.text(103, 12.0 - 4.2 * k, f"{lab}", fontsize=7.8, color=col, ha="left")
    ax.text(148, 12.0 - 4.2 * k, f"{curves[name][i]:.0f},  {LS[i]:.0f}",
            fontsize=7.8, color=col, ha="right")

ax.set_xlim(0, 160)
ax.set_ylim(0, 100)
ax.set_xlabel("彩度 $C_{ab}$（CIELAB，色相角 30°）", fontsize=10.5)
ax.set_ylabel("明度 $L^*$", fontsize=10.5)

handles = [plt.Line2D([], [], color=col, lw=2.2, ls=ls, label=lab)
           for _, col, ls, lab in STYLE]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.14),
          ncol=3, fontsize=8.6, frameon=False, handlelength=2.2,
          columnspacing=2.0)

H.save(fig, 5, "f2_lc_slice")
