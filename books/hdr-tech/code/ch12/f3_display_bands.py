# -*- coding: utf-8 -*-
"""第 12 章 图 3：峰值亮度与 BT.2020 覆盖的演进区间（2015—2026）。

只画公开产品规格的区间，不针对任何型号。区间上下界按各年份整机标称值的
常见分布取整，用来读趋势与量级，不是统计抽样结果。
(a) 峰值亮度，对数纵轴，三种技术路线；
(b) 电视与投影对 BT.2020 色域的覆盖，按 u'v' 色度面积计。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

years = np.array([2015, 2018, 2021, 2024, 2026])

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(9.2, 4.0), gridspec_kw={"width_ratios": [1.06, 1.0]})
fig.subplots_adjust(left=0.085, right=0.975, bottom=0.145, top=0.955, wspace=0.30)

bands = [
    ("液晶整机", [400, 600, 700, 800, 800], [900, 1800, 2600, 4000, 5000], H.NAVY),
    ("自发光整机", [400, 500, 600, 700, 800], [800, 1000, 1500, 3000, 3000], H.RED),
    ("投影", [50, 55, 60, 70, 75], [100, 120, 150, 190, 210], H.TEAL),
]
for name, lo, hi, col in bands:
    ax1.fill_between(years, lo, hi, color=col, alpha=0.16, linewidth=0)
    ax1.plot(years, hi, color=col, linewidth=1.4)
    ax1.plot(years, lo, color=col, linewidth=1.0, alpha=0.65)
    yl = {"液晶整机": hi[-1] * 0.93, "自发光整机": hi[-1] * 0.52}.get(
        name, np.sqrt(lo[-1] * hi[-1]))
    ax1.text(2026.25, yl, name, fontsize=8.2, color=col,
             va="center", ha="left")

ax1.set_yscale("log")
ax1.set_ylim(30, 12000)
ax1.set_xlim(2014.5, 2029.6)
ax1.set_yticks([50, 100, 300, 1000, 3000, 10000])
ax1.set_yticklabels(["50", "100", "300", "1000", "3000", "10000"])
ax1.set_xticks([2015, 2018, 2021, 2024, 2026])
ax1.set_ylabel("标称峰值亮度（cd/m$^2$）")
ax1.axhline(1000, color=H.GRAY, linestyle=(0, (4, 3)), linewidth=1.0)
ax1.text(2014.7, 6300, "虚线为 BT.2408 建议的 1000 cd/m$^2$ 参考峰值", fontsize=7.4,
         color="#5d6b7a", va="bottom", ha="left")
ax1.grid(axis="x", visible=False)
ax1.text(2014.6, 34, "(a)", fontsize=9.5, fontweight="bold", color=H.DARK,
         va="bottom", ha="left")

gb = [
    ("电视整机", [60, 66, 72, 78, 82], [74, 82, 88, 94, 96], H.ORANGE),
    ("投影整机", [70, 78, 86, 92, 95], [82, 88, 94, 98, 99], H.PURPLE),
]
for name, lo, hi, col in gb:
    ax2.fill_between(years, lo, hi, color=col, alpha=0.16, linewidth=0)
    ax2.plot(years, hi, color=col, linewidth=1.4)
    ax2.plot(years, lo, color=col, linewidth=1.0, alpha=0.65)
    ax2.text(2026.25, np.sqrt(lo[-1] * hi[-1]), name, fontsize=8.2, color=col,
             va="center", ha="left")

ax2.set_ylim(50, 104)
ax2.set_xlim(2014.5, 2029.6)
ax2.set_yticks([50, 60, 70, 80, 90, 100])
ax2.set_xticks([2015, 2018, 2021, 2024, 2026])
ax2.set_ylabel("BT.2020 色度面积覆盖率（%）")
ax2.grid(axis="x", visible=False)
ax2.text(2014.6, 51, "(b)", fontsize=9.5, fontweight="bold", color=H.DARK,
         va="bottom", ha="left")

H.save(fig, 12, "f3_display_bands")
