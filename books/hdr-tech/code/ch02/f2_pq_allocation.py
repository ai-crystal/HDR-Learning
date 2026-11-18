# -*- coding: utf-8 -*-
"""图 2-2：PQ 码值在亮度区间上的分配（按 ST 2084 公式逐点计算）。

把 10 bit 与 12 bit 的码值按对应亮度归入若干区段，统计每段占用的码值数量，
用 100% 堆叠条表示码值预算的分配比例。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
plt.rcParams["mathtext.fontset"] = "dejavusans"

BANDS = [(0.0, 1.0, "0 – 1"), (1.0, 10.0, "1 – 10"), (10.0, 100.0, "10 – 100"),
         (100.0, 1000.0, "100 – 1000"), (1000.0, 10000.0, "1000 – 10000")]
COLORS = [H.RED, H.ORANGE, H.TEAL, H.BLUE, H.NAVY]

fig, ax = plt.subplots(figsize=(9.0, 3.9))
fig.subplots_adjust(left=0.085, right=0.975, bottom=0.30, top=0.90)

bits_list = [10, 12]
for row, bits in enumerate(bits_list):
    n = 2 ** bits - 1
    codes = np.arange(0, n + 1)
    lum = H.pq_eotf(codes / n)
    counts, total = [], len(codes)
    for lo, hi, _ in BANDS:
        counts.append(int(np.sum((lum >= lo) & (lum < hi))))
    left = 0.0
    for (lo, hi, lab), cnt, c in zip(BANDS, counts, COLORS):
        pct = cnt / total * 100.0
        ax.barh(row, pct, left=left, height=0.52, color=c, edgecolor="white",
                linewidth=1.2)
        if pct > 9:
            ax.text(left + pct / 2, row, f"{cnt}\n{pct:.1f}%", ha="center",
                    va="center", fontsize=8.4, color="white")
        left += pct
    ax.text(-1.2, row, f"{bits} bit\n共 {n + 1} 个码值", ha="right", va="center",
            fontsize=9.0, color=H.DARK)

ax.set_yticks([])
ax.set_ylim(-0.75, 1.42)
ax.set_xlim(0, 100)
ax.set_xlabel("码值预算占比（%）")
ax.grid(axis="y", visible=False)

handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in COLORS]
ax.legend(handles, [f"{lab} cd/m$^2$" for _, _, lab in BANDS],
          loc="upper center", bbox_to_anchor=(0.5, -0.30), ncol=5,
          fontsize=8.6, frameon=False, handlelength=1.2, columnspacing=1.6)
for row in [0, 1]:
    ax.axhline(row - 0.34, color=H.LGRAY, lw=0.8, zorder=0)

H.save(fig, 2, "f2_pq_allocation")
