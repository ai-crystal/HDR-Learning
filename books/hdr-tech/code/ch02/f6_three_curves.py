# -*- coding: utf-8 -*-
"""图 2-6：三条传递函数在“信号—亮度”平面上的形状。

纵轴取对数，横轴是归一化信号。PQ 近似对数分配，整条曲线在对数纵轴上接近
直线；HLG 在 Lw = 1000 cd/m² 下的端到端曲线呈幂律，暗部被抬起、亮部被压缩；
BT.1886 的 gamma 2.2（白场 100 cd/m²）在暗部最陡，中高段迅速贴近白场。
PQ 58% 与 HLG 75% 都落在 203 cd/m²，这是 BT.2408 把两条路线对齐的锚点。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import FuncFormatter, NullFormatter
plt.rcParams["mathtext.fontset"] = "dejavusans"


def dec(v):
    s = f"{v:.0e}"
    return s.replace("e+0", "e").replace("e+", "e").replace("e-0", "e-")


LW = 1000.0
GAM = 1.2 + 0.42 * np.log10(LW / 1000.0)

sig = np.linspace(1e-4, 1.0, 1200)
pq = np.maximum(H.pq_eotf(sig), 1e-5)
hlg = LW * np.maximum(H.hlg_eotf(sig), 1e-12) ** GAM
g22 = 100.0 * sig ** 2.2

fig, ax = plt.subplots(figsize=(7.6, 4.3))
fig.subplots_adjust(left=0.098, right=0.975, bottom=0.145, top=0.95)

ax.semilogy(sig, pq, color=H.NAVY, lw=2.4, label="PQ（ST 2084，0–10000 cd/m$^2$）")
ax.semilogy(sig, hlg, color=H.ORANGE, lw=2.4,
            label="HLG（Lw = 1000 cd/m$^2$，系统 gamma 1.2）")
ax.semilogy(sig, g22, color=H.GRAY, lw=2.0, ls=(0, (5, 2)),
            label="BT.1886（白场 100 cd/m$^2$）")

ax.axhline(203.0, color=H.RED, lw=0.8, ls=(0, (2, 2)), zorder=1)
ax.text(0.012, 230, "203 cd/m$^2$", fontsize=7.8, color=H.RED, ha="left",
        va="bottom")
for xs, c in [(0.5807, H.NAVY), (0.75, H.ORANGE)]:
    ax.plot([xs], [203.0], "o", ms=6.0, color=c, mec="white", mew=0.9, zorder=6)

ax.annotate("58%", xy=(0.573, 214), xytext=(0.44, 620), fontsize=8.2,
            color=H.NAVY, ha="center", va="center",
            arrowprops=dict(arrowstyle="-", color=H.NAVY, lw=0.8,
                            shrinkA=2, shrinkB=4))
ax.annotate("75%", xy=(0.753, 214), xytext=(0.79, 430), fontsize=8.2,
            color=H.ORANGE, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=H.ORANGE, lw=0.8,
                            shrinkA=2, shrinkB=4))

ax.text(0.055, 6e-4, "PQ 在暗部极陡，\n同样信号对应的亮度跨度大", fontsize=7.9,
        color=H.NAVY, ha="left", va="bottom")
ax.text(0.335, 2.6e-3, "同一信号值下，HLG 的暗部比 PQ 亮、亮部比 PQ 暗", fontsize=7.9,
        color=H.ORANGE, ha="left", va="bottom")

ax.set_xlim(0, 1.0)
ax.set_ylim(1e-5, 3e4)
ax.set_xticks([0, 0.25, 0.5, 0.58, 0.75, 1.0])
ax.set_xticklabels(["0", "0.25", "0.50", "0.58", "0.75", "1.0"])
ax.set_yticks([1e-4, 1e-2, 1, 100, 1e4])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: dec(v) if v < 1e-1
                                            else f"{v:g}".replace("e+", "e")))
ax.yaxis.set_minor_formatter(NullFormatter())
ax.set_xlabel("归一化信号值")
ax.set_ylabel("显示亮度（cd/m$^2$，对数刻度）")
ax.legend(loc="lower right", fontsize=8.0, handlelength=2.6,
          borderpad=0.5, labelspacing=0.4)

H.save(fig, 2, "f6_three_curves")
