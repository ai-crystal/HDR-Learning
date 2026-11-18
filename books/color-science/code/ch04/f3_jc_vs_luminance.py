# -*- coding: utf-8 -*-
"""第 04 章 图 3：固定色度下，明度 J、彩度 C、色彩量 M 随相对亮度的变化，
以及适应亮度 L_A 的影响。数值由 cam02.py 的 CIECAM02 正向模型计算。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cam02 as C

plt = H.plt

W = C.white_XYZ("D65")
X_CH, Y_CH = 0.50, 0.40          # 固定的橙红色度（x, y）
YREL = np.logspace(np.log10(0.5), np.log10(1000), 240)

LAS = [(100, H.BLUE, "-"), (1000, H.ORANGE, "-"), (10000, H.RED, "-")]

data = {}
for LA, _, _ in LAS:
    res = [C.cam02(C.xy_to_XYZ(X_CH, Y_CH, y), W, LA=LA, Yb=20.0) for y in YREL]
    data[LA] = dict(J=np.array([r["J"] for r in res]),
                    C=np.array([r["C"] for r in res]),
                    M=np.array([r["M"] for r in res]))

fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.9))
fig.subplots_adjust(left=0.085, right=0.985, top=0.86, bottom=0.16, wspace=0.30)

# ---------- (a) 明度 ----------
ax = axes[0]
for LA, col, ls in LAS:
    ax.plot(YREL, data[LA]["J"], color=col, ls=ls, lw=2.0,
            label=f"$L_A$ = {LA} cd/m$^2$")
ax.axvline(100, color="#8a97a6", lw=1.0, ls=(0, (5, 3)))
ax.text(112, 30, "参考白 $Y$ = 100", fontsize=8.0, color="#5a6673", va="bottom")
ax.set_xscale("log")
ax.set_xlim(0.5, 1000)
ax.set_ylim(0, 380)
ax.set_xlabel("相对亮度 $Y$（$Y_w$ = 100）", fontsize=10)
ax.set_ylabel("明度 $J$", fontsize=10)
ax.legend(loc="upper left", fontsize=8.4)
ax.text(0.97, 0.42, "三条曲线\n几乎重合", transform=ax.transAxes, fontsize=8.2,
        color="#39485a", ha="right", va="center")

# ---------- (b) 彩度与色彩量 ----------
ax = axes[1]
for LA, col, ls in LAS:
    ax.plot(YREL, data[LA]["C"], color=col, ls="-", lw=2.0)
    ax.plot(YREL, data[LA]["M"], color=col, ls=(0, (4, 2)), lw=1.7)
ax.axvline(100, color="#8a97a6", lw=1.0, ls=(0, (5, 3)))

from matplotlib.lines import Line2D
handles = [Line2D([], [], color=c, lw=2.0, label=f"$L_A$ = {la} cd/m$^2$")
           for la, c, _ in LAS]
handles += [Line2D([], [], color="#39485a", lw=2.0, ls="-", label="实线：彩度 $C$"),
            Line2D([], [], color="#39485a", lw=1.7, ls=(0, (4, 2)),
                   label="虚线：色彩量 $M$")]
ax.legend(handles=handles, loc="upper left", fontsize=8.0, ncol=1,
          handlelength=1.8, borderpad=0.4, labelspacing=0.35)

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.5, 1000)
ax.set_ylim(10, 400)
ax.set_xlabel("相对亮度 $Y$（$Y_w$ = 100）", fontsize=10)
ax.set_ylabel("$C$ 与 $M$", fontsize=10)
ax.text(112, 11.5, "参考白", fontsize=8.0, color="#5a6673", va="bottom")

H.save(fig, 4, "f3_jc_vs_luminance")
