# -*- coding: utf-8 -*-
"""第 07 章 图 2：九套 RGB 空间的基色三角形与白点。

(a) 显示与影视常用的四套：sRGB、Adobe RGB、DCI-P3 / Display P3、BT.2020
(b) 制作与存档常用的四套：ACES AP1、ACES AP0、ProPhoto、Adobe Wide Gamut
三角形坐标全部取自公开标准（见 rgbspace.py 表头）。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C
import rgbspace as R

plt = H.plt
from matplotlib.lines import Line2D

LABEL = {"sRGB": "sRGB / BT.709", "AdobeRGB": "Adobe RGB (1998)",
         "DisplayP3": "Display P3", "BT2020": "BT.2020",
         "AP1": "ACES AP1", "AP0": "ACES AP0",
         "ProPhoto": "ProPhoto (ROMM)", "WideGamut": "Adobe Wide Gamut"}

fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.5),
                         gridspec_kw={"wspace": 0.16})

GROUPS = [
    ("(a) 显示与影视", [("sRGB", H.NAVY, "-"), ("AdobeRGB", H.GREEN, "-"),
                     ("DisplayP3", H.ORANGE, "-"), ("BT2020", H.TEAL, "-")],
     [("D65", H.DARK, "s"), ("DCI", H.GRAY, "D")]),
    ("(b) 制作与存档", [("AP1", H.PURPLE, "--"), ("AP0", H.RED, "-"),
                     ("ProPhoto", H.GOLD, "-"), ("WideGamut", H.BLUE, "-")],
     [("D60", H.DARK, "s"), ("D50", H.GRAY, "D")]),
]

for ax, (title, spaces, whites) in zip(axes, GROUPS):
    lam, sx, sy = C.spectral_locus(1500)
    ax.fill(np.append(sx, sx[0]), np.append(sy, sy[0]), color="#f3f5f8", zorder=0,
            edgecolor="none")
    ax.plot(sx, sy, color="#8a97a6", lw=1.3, zorder=1)
    ax.plot([sx[0], sx[-1]], [sy[0], sy[-1]], color="#8a97a6", lw=0.9, ls=(0, (4, 3)),
            zorder=1)

    handles = []
    for name, col, ls in spaces:
        p = R.PRIMARIES[name]
        xy = np.array([p["R"], p["G"], p["B"], p["R"]])
        ax.plot(xy[:, 0], xy[:, 1], color=col, lw=1.8, ls=ls, zorder=4)
        handles.append(Line2D([], [], color=col, lw=1.8, ls=ls, label=LABEL[name]))

    for wn, col, mk in whites:
        wx, wy = R.WHITE[wn]
        ax.plot([wx], [wy], mk, ms=5.0, color=col, mec="white", mew=0.9, zorder=6)
        handles.append(Line2D([], [], color=col, marker=mk, ls="none", ms=5.0,
                              label=f"白点 {wn}"))

    ax.set_xlim(-0.06, 0.84)
    ax.set_ylim(-0.11, 1.02)
    ax.text(0.995, 0.012, "x", transform=ax.transAxes, fontsize=10, ha="right",
            va="bottom", color="#4a5666")
    ax.set_title(title, fontsize=10.5, pad=6)
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.115),
              fontsize=7.6, handlelength=1.7, labelspacing=0.34, borderaxespad=0.0,
              ncol=2, columnspacing=1.4)

axes[0].set_ylabel("y")
axes[1].set_yticklabels([])

H.save(fig, 7, "f2_gamut_triangles")
