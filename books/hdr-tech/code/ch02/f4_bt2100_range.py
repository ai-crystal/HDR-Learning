# -*- coding: utf-8 -*-
"""图 2-4：BT.2100 的窄范围码值分配。

8 / 10 / 12 bit 三种码值空间按满量程比例对齐后画在一起，可以看到三者的有效
视频区间都落在满量程的 6.25% 到 92% 附近，脚部与头部各留出一段。
BT.2100 的黑电平 64（10 bit）与白电平 940 即来自这里，PQ 与 HLG 的信号
都映射到这段 877 级的区间上，因此 203 cd/m² 的参考白落在码值 573 与 721。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import FuncFormatter, NullFormatter
plt.rcParams["mathtext.fontset"] = "dejavusans"

fig, ax = plt.subplots(figsize=(7.8, 3.9))
fig.subplots_adjust(left=0.145, right=0.975, bottom=0.155, top=0.94)

rows = [
    (8, 16, 235, 1, 240, 255, "8 bit（BT.709 惯例）"),
    (10, 64, 940, 4, 1019, 1023, "10 bit（BT.2100 窄范围）"),
    (12, 256, 3760, 16, 4079, 4095, "12 bit（BT.2100 窄范围）"),
]
ys = [2.0, 1.0, 0.0]
for (bits, lo, hi, lo_f, hi_f, hi_code, lab), y in zip(rows, ys):
    full = 2 ** bits - 1
    ax.barh(y, hi / full * 100, left=0, height=0.40, color=H.LGRAY,
            edgecolor=H.GRAY, lw=0.8, zorder=2)
    ax.barh(y, (hi - lo) / full * 100, left=lo / full * 100, height=0.40,
            color=H.BLUE, alpha=0.5, edgecolor=H.NAVY, lw=0.9, zorder=3)
    ax.text(-1.2, y, lab, ha="right", va="center", fontsize=8.5, color=H.DARK)
    ax.text(lo / full * 100 / 2, y + 0.26, f"脚部 {lo_f}–{lo - 1}",
            ha="center", va="bottom", fontsize=7.4, color=H.GRAY)
    ax.text((lo + hi) / 2 / full * 100, y,
            f"有效视频 {lo}–{hi}，{hi - lo + 1} 级", ha="center", va="center",
            fontsize=8.0, color="white", zorder=4)
    ax.text(100.0, y + 0.26, f"头部 {hi + 1}–{hi_f}",
            ha="right", va="bottom", fontsize=7.4, color=H.GRAY)

lo10, hi10 = 64, 940
marks = [(0.5807, "PQ 203 cd/m$^2$ → 573", H.RED, -1.6, "right", 1.35),
         (0.75, "HLG 75% → 721", H.ORANGE, 0.0, "center", 0.60)]
for frac, lab, c, dx, ha, ty in marks:
    x = (lo10 + frac * (hi10 - lo10)) / 1023 * 100
    ax.plot([x], [0.795], "^", ms=6.5, color=c, mec="white", mew=0.7, zorder=6)
    ax.annotate(lab, xy=(x, 1.205 if ty > 1 else 0.78), xytext=(x + dx, ty),
                fontsize=8.0, color=c, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=c, lw=0.8,
                                shrinkA=1, shrinkB=1))

ax.set_xlim(-1, 101)
ax.set_ylim(-0.62, 2.62)
ax.set_yticks([])
ax.set_xticks([0, 6.25, 25, 50, 75, 91.9, 100])
ax.set_xticklabels(["0", "6.25%", "25%", "50%", "75%", "92%", "100%"])
ax.grid(axis="y", visible=False)
ax.set_xlabel("码值占满量程的比例（三种位深按比例对齐）")

H.save(fig, 2, "f4_bt2100_range")
