# -*- coding: utf-8 -*-
"""第 03 章 图 7：同一组色样对在五种色差度量下的秩次排序。

左图为秩次图（平行坐标），每条折线是一个色样对，横轴是五种度量，
纵轴是秩次 1（最小）到 8（最大）。右图为五种度量两两之间的
斯皮尔曼秩相关系数。色差全部按公式算：
ΔE76/ΔE94/ΔE2000 见 colordiff.py，CMC(2:1) 与 CAM02-UCS 见 ucs_metrics.py。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import colordiff as D
import ucs_metrics as U
from scipy.stats import spearmanr

plt = H.plt
NL = chr(10)

PAIRS = [
    ("近白", (96.0, 0.0, 2.0), (94.0, 0.0, 1.0)),
    ("中性灰", (60.0, 0.0, 0.0), (57.0, 0.0, 0.0)),
    ("肤色", (66.0, 18.0, 25.0), (63.0, 14.0, 22.0)),
    ("深红", (40.0, 52.0, 30.0), (37.0, 47.0, 27.0)),
    ("叶绿", (70.0, -45.0, 35.0), (68.0, -41.0, 31.0)),
    ("天蓝", (55.0, -12.0, -42.0), (53.0, -9.0, -37.0)),
    ("亮黄", (88.0, -5.0, 80.0), (85.0, -4.0, 74.0)),
    ("暗紫", (25.0, 20.0, -15.0), (23.0, 17.0, -12.0)),
]

V = U.viewing((95.047, 100.0, 108.883), La=64.0, Yb=20.0)
METRICS = ["ΔE76", "ΔE94", "ΔE2000", "CMC(2:1)", "CAM02-UCS"]

vals = np.zeros((len(PAIRS), len(METRICS)))
for i, (name, a, b) in enumerate(PAIRS):
    vals[i, 0] = D.de76(a, b)
    vals[i, 1] = D.de94(a, b)
    vals[i, 2] = D.de2000(a, b)
    vals[i, 3] = U.cmc(a, b)
    vals[i, 4] = U.de_ucs(V, a, b)

ranks = np.argsort(np.argsort(vals, axis=0), axis=0) + 1

fig = plt.figure(figsize=(7.4, 4.35))
ax = fig.add_axes([0.082, 0.185, 0.400, 0.775])
ax2 = fig.add_axes([0.625, 0.185, 0.290, 0.775])

cols = [H.PLGRAY if False else "#b8c4d0"] * len(PAIRS)
order = np.argsort(vals[:, 2])
shades = ["#dfe6ee", "#c6d2df", "#a9bacb", "#8aa0b6", "#6c88a2", "#4e6f8e",
          "#2f5679", "#1f4e79"]
for k, i in enumerate(order):
    ax.plot(range(len(METRICS)), ranks[i], "-o", color=shades[k], lw=1.7, ms=4.6,
            mfc="white", mew=1.3, zorder=4 + k)
    ax.text(-0.16, ranks[i, 0], PAIRS[i][0], fontsize=7.2, color="#2c3e50",
            ha="right", va="center")
    ax.text(len(METRICS) - 0.84, ranks[i, -1], PAIRS[i][0], fontsize=7.2,
            color="#2c3e50", ha="left", va="center")

ax.set_xlim(-1.45, len(METRICS) - 0.10)
ax.set_ylim(8.6, 0.4)
ax.set_xticks(range(len(METRICS)))
ax.set_xticklabels(["76", "94", "2000", "CMC", "CAM02"], fontsize=8.2)
ax.set_yticks(range(1, 9))
ax.set_ylabel("秩次（1 为最小色差）", labelpad=2)
ax.set_xlabel("色差度量：ΔE 的年份 / CMC(2:1) / CAM02-UCS", labelpad=2)
ax.grid(axis="x", visible=False)
ax.text(2.0, 0.75, "折线交叉说明排序不稳", fontsize=7.4, color="#2c3e50",
        ha="center", va="center",
        bbox=dict(facecolor="white", alpha=0.92, edgecolor=H.LGRAY,
                  boxstyle="round,pad=0.3"))

# ---------- 右：秩相关矩阵 ----------
n = len(METRICS)
R = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        R[i, j] = spearmanr(vals[:, i], vals[:, j]).correlation

im = ax2.imshow(R, cmap="YlGnBu", vmin=0.0, vmax=1.0)
ax2.set_xticks(range(n))
ax2.set_yticks(range(n))
short = ["76", "94", "00", "CMC", "UCS"]
ax2.set_xticklabels(short, fontsize=8.0)
ax2.set_yticklabels(short, fontsize=8.0)
ax2.set_xlabel("色差度量", labelpad=2)
ax2.set_ylabel("色差度量", labelpad=2)
ax2.grid(False)

for i in range(n):
    for j in range(n):
        ax2.text(j, i, "%.2f" % R[i, j], ha="center", va="center",
                 fontsize=7.0, color="white" if R[i, j] > 0.62 else "#2c3e50")

ax2.set_title("斯皮尔曼秩相关系数", fontsize=8.6, color="#2c3e50", pad=6)

cb = fig.colorbar(im, ax=ax2, fraction=0.045, pad=0.04)
cb.ax.tick_params(labelsize=7.5)
cb.set_label("秩相关", fontsize=7.8)

H.save(fig, 3, "f7_ranking")
print("秩次表（行：色样对，列：" + ", ".join(METRICS) + "）")
for i, (name, a, b) in enumerate(PAIRS):
    print("%4s " % name + " ".join("%d" % r for r in ranks[i])
          + "  |  " + " ".join("%5.2f" % v for v in vals[i]))
print("rho(76,00)=%.2f  rho(94,UCS)=%.2f  rho(00,UCS)=%.2f"
      % (R[0, 2], R[1, 4], R[2, 4]))
