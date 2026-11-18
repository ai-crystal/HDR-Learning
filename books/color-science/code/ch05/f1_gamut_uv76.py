# -*- coding: utf-8 -*-
"""第 05 章 图 1：sRGB、Display P3、BT.2020 三个色域在 CIE 1976 u'v' 上的叠加。

基色坐标取真实标准值（IEC 61966-2-1、SMPTE RP 431-2、ITU-R BT.2020），
u'v' 由 xy 经标准公式换算；面积用鞋带公式对三角形计算。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import gamut as G
import cie1931 as C

plt = H.plt

fig = plt.figure(figsize=(6.8, 5.9))
ax = fig.add_axes([0.09, 0.14, 0.87, 0.83])

# ---------- 可见光轨迹作为背景 ----------
lam, sx, sy = C.spectral_locus(1500)
su, sv = G.xy_to_uv76(sx, sy)
ax.fill(np.append(su, su[0]), np.append(sv, sv[0]), color="#f3f5f8",
        zorder=0, edgecolor="none")
ax.plot(su, sv, color="#8a97a6", lw=1.6, zorder=2)
ax.plot([su[0], su[-1]], [sv[0], sv[-1]], color="#8a97a6", lw=1.2,
        ls=(0, (4, 3)), zorder=2)

for wl, dx, dy, ha in ((460, 0.022, -0.020, "left"), (520, 0.006, -0.028, "left"),
                       (580, 0.0, 0.022, "center")):
    i = int(np.argmin(np.abs(lam - wl)))
    ax.text(su[i] + dx, sv[i] + dy, f"{wl} nm", fontsize=7.4, color="#69747f",
            ha=ha, va="center", zorder=3)

# ---------- 三个色域 ----------
STYLE = [
    ("sRGB",   H.NAVY,   "sRGB / BT.709：u′v′ 面积 0.0649", (0, (6, 3))),
    ("P3",     H.ORANGE, "Display P3：u′v′ 面积 0.0815", "-"),
    ("BT2020", H.TEAL,   "BT.2020：u′v′ 面积 0.1118", "-"),
]

for name, col, _, ls in STYLE:
    prim = G.PRIMARIES[name]
    xy = np.array([prim["R"], prim["G"], prim["B"], prim["R"]])
    u, v = G.xy_to_uv76(xy[:, 0], xy[:, 1])
    ax.plot(u, v, color=col, lw=2.0, zorder=4, ls=ls)

# 顶点标注：B 基色 sRGB 与 P3 共用，只标一次
LABELS = [
    ("sRGB",   "R", -0.004, -0.034, "center", "top",    "sRGB R"),
    ("sRGB",   "G", -0.040,  0.008, "right",  "center", "sRGB G"),
    ("sRGB",   "B",  0.016, -0.002, "left",   "top",    "sRGB / P3 B"),
    ("P3",     "R",  0.016,  0.006, "left",   "bottom", "P3 R"),
    ("P3",     "G",  0.006,  0.030, "center", "bottom", "P3 G"),
    ("BT2020", "R",  0.010, -0.030, "center", "top",    "BT.2020 R"),
    ("BT2020", "G",  0.000,  0.024, "left",   "bottom", "BT.2020 G"),
    ("BT2020", "B", -0.010, -0.028, "right",  "top",    "BT.2020 B"),
]
for name, key, dx, dy, ha, va, text in LABELS:
    col = dict((n, c) for n, c, _, _ in STYLE)[name]
    uu, vv = G.xy_to_uv76(*G.PRIMARIES[name][key])
    ax.plot([uu], [vv], marker="o", ms=5.6, mfc="white", mec=col, mew=1.6, zorder=6)
    ax.text(uu + dx, vv + dy, text, fontsize=7.2, color=col, ha=ha, va=va,
            zorder=7, bbox=dict(facecolor="white", alpha=0.82, edgecolor="none",
                                pad=0.7))

# ---------- 参考白 ----------
for wname, (x, y), col, dx, ha, fc in (
        ("D65", G.WHITE_XY["D65"], "#2b2b2b", 0.012, "left", "#ffffff"),
        ("DCI", G.WHITE_XY["DCI"], "#7a6420", -0.012, "right", "#ffe9a8")):
    uu, vv = G.xy_to_uv76(x, y)
    ax.plot([uu], [vv], marker="P", ms=7, mfc=fc, mec=col, mew=1.2, zorder=8)
    ax.text(uu + dx, vv + 0.004, wname, fontsize=7.6, color=col, zorder=8,
            ha=ha, va="center")

ax.set_xlim(0.0, 0.66)
ax.set_ylim(0.0, 0.66)
ax.set_xlabel("u′", fontsize=10.5)
ax.set_ylabel("v′", fontsize=10.5)
ax.set_aspect("equal")
ax.grid(color="#e8ecf1", lw=0.7, zorder=1)

handles = [plt.Line2D([], [], color=col, lw=2.0, ls=ls, label=lab)
           for _, col, lab, ls in STYLE]
ax.legend(handles=handles, loc="lower right", bbox_to_anchor=(0.995, 0.02),
          fontsize=7.8, frameon=False, borderpad=0.2, labelspacing=0.35,
          handlelength=2.0)

fig.text(0.5, 0.015,
         "u′v′ 面积由基色三角形算出：sRGB 覆盖 BT.2020 的 58.0%，Display P3 覆盖 72.9%",
         fontsize=7.8, color=H.NAVY, ha="center", va="bottom")

H.save(fig, 5, "f1_gamut_uv76")
