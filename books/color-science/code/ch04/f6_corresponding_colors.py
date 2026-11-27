# -*- coding: utf-8 -*-
"""第 04 章 图 6：对应色（corresponding colours）。

以 D65 下的一组色样外观 (J, C, h) 为目标，在光源 A 的白点下反解出
外观相同的三刺激值，这就是光源 A 下的对应色。箭头由 D65 下的色度指向
A 下的对应色色度；右图为对应色的相对亮度变化。
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

WD = C.white_XYZ("D65")
WA = C.white_XYZ("A")


def disp_rgb(XYZ):
    """三刺激值 -> 显示色（线性归一后加 sRGB 伽马）。"""
    r, g, b = S.xyz_to_linear_srgb(*np.asarray(XYZ))
    m = max(r, g, b, 1e-6)
    lin = np.clip(np.array([r, g, b]) / m, 0.0, 1.0)
    return np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055)


def uv(XYZ):
    X, Y, Z = XYZ
    d = X + 15.0 * Y + 3.0 * Z
    return 4.0 * X / d, 9.0 * Y / d


PATCH = [
    ("红", 0.550, 0.330, (4, 6)),
    ("橙", 0.500, 0.410, (-14, 2)),
    ("黄", 0.420, 0.500, (2, 8)),
    ("绿", 0.280, 0.520, (-16, -2)),
    ("青", 0.220, 0.350, (-14, -6)),
    ("蓝", 0.180, 0.160, (4, -10)),
    ("紫", 0.280, 0.200, (6, -8)),
    ("肤色", 0.400, 0.360, (10, 4)),
    ("灰", 0.3127, 0.3290, (10, -8)),
]

rows = []
for name, x, y, off in PATCH:
    XYZ = C.xy_to_XYZ(x, y, 18.0)
    r = C.cam16(XYZ, WD, LA=200.0)
    XYZa = C.cam16_inverse(r["J"], r["C"], r["h"], WA, LA=200.0)[0]
    rows.append(dict(name=name, XYZ=XYZ, XYZa=XYZa, uv=uv(XYZ), uva=uv(XYZa),
                     off=off, J=r["J"], C=r["C"], h=r["h"]))

fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.9),
                         gridspec_kw=dict(width_ratios=[1.30, 1.0], wspace=0.28))
fig.subplots_adjust(left=0.075, right=0.985, top=0.90, bottom=0.155)

# ---------------- (a) u'v' 上的对应色迁移 ----------------
ax = axes[0]
lam, xl, yl = S.spectral_locus(800)
d = -2 * xl + 12 * yl + 3
ax.plot(4 * xl / d, 9 * yl / d, color="#c2cad4", lw=1.2, zorder=1)
ax.plot([4 * xl[0] / d[0], 4 * xl[-1] / d[-1]],
        [9 * yl[0] / d[0], 9 * yl[-1] / d[-1]], color="#c2cad4", lw=1.2, zorder=1)

for r in rows:
    face = disp_rgb(r["XYZ"])
    ax.annotate("", xy=r["uva"], xytext=r["uv"],
                arrowprops=dict(arrowstyle="-|>", color=H.ORANGE, lw=1.2,
                                shrinkA=5, shrinkB=5, alpha=0.85), zorder=3)
    ax.plot(*r["uv"], "o", ms=8.0, mfc="white", mec=H.NAVY, mew=1.4, zorder=4)
    ax.plot(*r["uv"], "o", ms=5.0, mfc=face, mec="none", zorder=5)
    ax.plot(*r["uva"], "o", ms=8.0, mfc=H.NAVY, mec=H.NAVY, mew=1.0, zorder=4)
    ax.plot(*r["uva"], "o", ms=4.2, mfc=face, mec="none", zorder=5)

uw = uv(WD)
ua = uv(WA)
ax.plot(*uw, marker="s", ms=7, mfc="none", mec=H.GRAY, mew=1.4, zorder=5)
ax.plot(*ua, marker="s", ms=7, mfc="none", mec=H.GRAY, mew=1.4, zorder=5)
ax.annotate("D65 白", xy=uw, xytext=(-34, -14), textcoords="offset points",
            fontsize=7.6, color="#5a6673",
            arrowprops=dict(arrowstyle="-", color=H.GRAY, lw=0.8))
ax.annotate("A 白", xy=ua, xytext=(12, -16), textcoords="offset points",
            fontsize=7.6, color="#5a6673",
            arrowprops=dict(arrowstyle="-", color=H.GRAY, lw=0.8))

ax.set_xlim(0.10, 0.50)
ax.set_ylim(0.24, 0.60)
ax.set_xlabel("$u'$", fontsize=10)
ax.set_ylabel("$v'$", fontsize=10)
ax.plot([], [], "o", ms=8.0, mfc="white", mec=H.NAVY, mew=1.4, label="D65 下的色样")
ax.plot([], [], "o", ms=8.0, mfc=H.NAVY, mec=H.NAVY, label="光源 A 下的对应色")
ax.legend(loc="lower right", fontsize=7.8, handletextpad=0.5, borderpad=0.4)

# ---------------- (b) 对应色的亮度变化 ----------------
ax2 = axes[1]
idx = np.arange(len(rows))
dY = [100.0 * (r["XYZa"][1] / r["XYZ"][1] - 1.0) for r in rows]
cols = [disp_rgb(r["XYZ"]) for r in rows]
ax2.bar(idx, dY, color=cols, width=0.66, edgecolor="#3b4653", linewidth=0.6)
ax2.axhline(0, color="#4a5666", lw=1.0)
ax2.set_xticks(idx)
ax2.set_xticklabels([r["name"] for r in rows], fontsize=7.8)
ax2.set_ylim(-2.4, 2.6)
ax2.set_ylabel("对应色的相对亮度变化（%）", fontsize=9.2)
ax2.grid(axis="x", visible=False)
for i, v in enumerate(dY):
    ax2.text(i, v + (0.12 if v >= 0 else -0.12), f"{v:+.1f}", ha="center",
             va="bottom" if v >= 0 else "top", fontsize=7.2, color="#22303f")

H.save(fig, 4, "f6_corresponding_colors")
