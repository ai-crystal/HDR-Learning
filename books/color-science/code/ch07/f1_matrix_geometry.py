# -*- coding: utf-8 -*-
"""第 07 章 图 1：矩阵由基色坐标与白点唯一确定。

(a) xy 图上两套基色三角形与白点；虚线由白点连向三个顶点，对应"只把一个通道从 0 加到满"
(b) 同一组 sRGB 基色配三个不同白点时解出的三个亮度权重
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

fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.0),
                         gridspec_kw={"width_ratios": [1.22, 1.0], "wspace": 0.32})

# ---------------- (a) 色度图上的基色与白点 ----------------
ax = axes[0]
lam, sx, sy = C.spectral_locus(1500)
ax.fill(np.append(sx, sx[0]), np.append(sy, sy[0]), color="#f3f5f8", zorder=0, edgecolor="none")
ax.plot(sx, sy, color="#8a97a6", lw=1.4, zorder=1)
ax.plot([sx[0], sx[-1]], [sy[0], sy[-1]], color="#8a97a6", lw=1.0, ls=(0, (4, 3)), zorder=1)

for name, col, ls, lab in (("sRGB", H.NAVY, "-", "sRGB / BT.709"),
                           ("AdobeRGB", H.ORANGE, "--", "Adobe RGB (1998)")):
    p = R.PRIMARIES[name]
    xy = np.array([p["R"], p["G"], p["B"], p["R"]])
    ax.plot(xy[:, 0], xy[:, 1], color=col, lw=1.9, ls=ls, zorder=4, label=lab)

p = R.PRIMARIES["sRGB"]
wx, wy = R.WHITE["D65"]
for k, col in (("R", H.RED), ("G", H.GREEN), ("B", H.BLUE)):
    vx, vy = p[k]
    ax.plot([wx, vx], [wy, vy], color=col, lw=1.0, ls=(0, (1.6, 2.2)), alpha=0.9, zorder=3)
    for t in (0.34, 0.67):
        ax.plot([wx + t * (vx - wx)], [wy + t * (vy - wy)], "o", ms=3.2,
                color=col, mec="white", mew=0.6, zorder=6)
ax.plot([wx], [wy], "s", ms=6.0, color=H.DARK, mec="white", mew=1.0, zorder=7)
ax.text(wx + 0.014, wy + 0.012, "白点 D65", fontsize=8.2, color=H.DARK,
        ha="left", va="bottom", zorder=8)

for k, dx, dy, ha, va in (("R", 0.012, -0.035, "left", "top"),
                          ("G", 0.010, 0.006, "left", "bottom"),
                          ("B", 0.012, -0.006, "left", "top")):
    ax.text(p[k][0] + dx, p[k][1] + dy, k, fontsize=9.5, color=H.DARK, ha=ha, va=va)

ax.legend(loc="upper right", bbox_to_anchor=(1.005, 0.985), fontsize=8.0,
          handlelength=1.6, borderaxespad=0.1)

ax.set_xlim(0.02, 0.80)
ax.set_ylim(0.0, 0.87)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("(a) 基色与白点在色度图上的位置", fontsize=10.5, pad=6)

# ---------------- (b) 白点决定亮度权重 ----------------
ax = axes[1]
whites = ["D65", "D50", "DCI"]
xpos = np.arange(len(whites))
w = 0.25
for i, (k, col) in enumerate((("R", H.RED), ("G", H.GREEN), ("B", H.BLUE))):
    vals = []
    for wn in whites:
        _, S = R.rgb_to_xyz_matrix("sRGB", wn)
        vals.append(S[i] / S.sum())
    bars = ax.bar(xpos + (i - 1) * w, vals, width=w, color=col, alpha=0.85,
                  edgecolor="white", linewidth=0.8, label=f"{k} 通道")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.015, f"{v:.3f}",
                ha="center", va="bottom", fontsize=7.4, color=H.DARK)

ax.set_xticks(xpos)
ax.set_xticklabels(whites, fontsize=9.0)
ax.set_xlabel("白点")
ax.set_ylabel("亮度权重占白点的比例")
ax.set_ylim(0, 0.88)
ax.set_yticks(np.arange(0, 0.9, 0.2))
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=3, fontsize=8.2,
          columnspacing=1.4, handlelength=1.1, borderaxespad=0.0)
ax.set_title("(b) 同一组基色配不同白点解出的权重", fontsize=10.5, pad=6)
ax.grid(axis="x", visible=False)

H.save(fig, 7, "f1_matrix_geometry")
