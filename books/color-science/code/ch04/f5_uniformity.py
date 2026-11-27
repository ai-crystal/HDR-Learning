# -*- coding: utf-8 -*-
"""第 04 章 图 5：CIELAB 与 CAM16-UCS 的均匀性对比。

在 CAM16 里取 12 条等色相线（J = 60，M 由小到大），沿 M' 等距打点。
若 CIELAB 均匀，这些点在 a*b* 平面上应等距；实际间距随色相与彩度变化很大。
右图统计每个色相方向上相邻两步在 a*b* 中的 ΔE*ab。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cam02 as C
import cie1931 as S

plt = H.plt

W = C.white_XYZ("D65")
LA = 200.0
FL = C._luminance_level(LA)


def disp_rgb(XYZ):
    """三刺激值 -> 用于绘图的显示色（线性归一后加 sRGB 伽马）。"""
    r, g, b = S.xyz_to_linear_srgb(*np.asarray(XYZ))
    m = max(r, g, b, 1e-6)
    lin = np.clip(np.array([r, g, b]) / m, 0.0, 1.0)
    return np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055)


def xyz_to_lab(XYZ):
    t = np.asarray(XYZ) / np.asarray(W)
    d = 6.0 / 29.0
    f = np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4.0 / 29.0)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], axis=-1)


HUE = np.arange(0, 360, 30)
M_STEPS = np.linspace(3.0, 70.0, 200)
Mp = np.log1p(0.0228 * M_STEPS) / 0.0228
N_STEP = 16
MP_TARGET = np.linspace(Mp[0], Mp[-1], N_STEP)

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.9),
                         gridspec_kw=dict(width_ratios=[1.18, 1.0],
                                          wspace=0.30))
fig.subplots_adjust(left=0.075, right=0.985, top=0.90, bottom=0.155)

# ---------------- (a) a*b* 平面上的等色相点 ----------------
ax = axes[0]
stats = []
for h in HUE:
    Ms = np.interp(MP_TARGET, Mp, M_STEPS)
    labs = []
    xyzs = []
    for M in Ms:
        Cc = M / FL ** 0.25
        XYZ = C.cam16_inverse(60.0, Cc, h, W, LA=LA)[0]
        xyzs.append(XYZ)
        labs.append(xyz_to_lab(XYZ))
    labs = np.array(labs)
    xyzs = np.array(xyzs)
    face = disp_rgb(xyzs[len(xyzs) // 2])
    ax.plot(labs[:, 1], labs[:, 2], "-", color=face * 0.75 + 0.12, lw=1.5, zorder=2)
    ax.scatter(labs[:, 1], labs[:, 2], s=16, facecolor=face, edgecolor="#3b4653",
               linewidth=0.45, zorder=3)
    d = np.sqrt(np.sum(np.diff(labs, axis=0) ** 2, axis=1))
    stats.append((h, d.mean(), d.min(), d.max()))

ax.axhline(0, color="#c2cad4", lw=0.8, zorder=1)
ax.axvline(0, color="#c2cad4", lw=0.8, zorder=1)
ax.set_xlim(-42, 82)
ax.set_ylim(-78, 92)
ax.set_xlabel("$a^*$", fontsize=10)
ax.set_ylabel("$b^*$", fontsize=10)
ax.set_aspect("equal")
ax.annotate("彩度高处间距被拉开", xy=(38, 62), xytext=(48, 80), fontsize=7.4,
            color="#39485a",
            arrowprops=dict(arrowstyle="-|>", color="#39485a", lw=0.9,
                            shrinkA=2, shrinkB=3))

# ---------------- (b) 每个色相的平均步长 ----------------
ax2 = axes[1]
idx = np.arange(len(HUE))
means = np.array([s[1] for s in stats])
lo = means - np.array([s[2] for s in stats])
hi = np.array([s[3] for s in stats]) - means
cols = []
for h in HUE:
    XYZ = C.cam16_inverse(60.0, 45.0 / FL ** 0.25, h, W, LA=LA)[0]
    cols.append(disp_rgb(XYZ))
ax2.bar(idx, means, color=cols, edgecolor="#3b4653", linewidth=0.6, width=0.72)
ax2.errorbar(idx, means, yerr=[lo, hi], fmt="none", ecolor="#4a5666",
             elinewidth=0.9, capsize=2.4, capthick=0.9)
g = means.mean()
ax2.axhline(g, color=H.RED, lw=1.1, ls=(0, (5, 3)))
ax2.text(-0.55, g + 0.75, f"均值 {g:.2f}", fontsize=7.4, color=H.RED,
         ha="left", va="bottom")
ax2.set_xticks(idx)
ax2.set_xticklabels([f"{h}" for h in HUE], fontsize=7.4)
ax2.set_xlabel("CAM16 色相角 $h$（°）", fontsize=9.5)
ax2.set_ylabel("相邻两步的 $\\Delta E^*_{ab}$", fontsize=9.5)
ax2.set_ylim(0, 11.6)
ax2.grid(axis="x", visible=False)

H.save(fig, 4, "f5_uniformity")
