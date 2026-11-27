# -*- coding: utf-8 -*-
"""第 12 章 图 2：关键标准的版本演进（2014—2026）。

横条表示一份文件持续有效的时间段，圆点是已知的主要版本节点。
年份取各组织公开的出版与修订时间，只标主要节点，不是全部修订。
标签的上下位置逐个指定，避免相邻行互相压住。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

fig, ax = plt.subplots(figsize=(8.2, 5.6))
fig.subplots_adjust(left=0.225, right=0.985, bottom=0.105, top=0.972)

X0, X1 = 2013.2, 2027.4
END = 2026.4

rows = [
    ("BT.2100（ITU-R）", 2016.5, H.NAVY,
     [(2016.5, "2016 首版", 1, "left"), (2018.6, "ICtCp", -1, "center"),
      (2022.9, "2023 修订", 1, "center")]),
    ("BT.2390 报告", 2016.7, H.NAVY,
     [(2016.7, "2016", -1, "center"), (2019.8, "EETF", 1, "center"),
      (2023.6, "2023", -1, "center")]),
    ("BT.2408 报告", 2017.9, H.NAVY,
     [(2017.9, "2017 参考白 203", 1, "left"), (2021.0, "图形白", -1, "center"),
      (2024.4, "2024", 1, "center")]),
    ("ST 2084 / 2086（SMPTE）", 2014.6, H.ORANGE,
     [(2014.6, "2014 PQ 与母版", -1, "left"), (2018.4, "2086 修订", 1, "center")]),
    ("ST 2094 系列（SMPTE）", 2016.2, H.ORANGE,
     [(2016.2, "2094-10", -1, "left"), (2017.6, "2094-40", 1, "center")]),
    ("HEVC / AV1 / VVC / AVS3", 2013.3, H.TEAL,
     [(2013.3, "HEVC", -1, "left"), (2018.2, "AV1", 1, "center"),
      (2019.4, "AVS3", -1, "center"), (2020.6, "VVC", 1, "center")]),
    ("CTA-861.3 / HDR10 / HDR10+", 2015.1, H.PURPLE,
     [(2015.1, "861.3", -1, "left"), (2017.3, "HDR10+", 1, "center")]),
    ("DVB UHD-1 Ph2 / ATSC 3.0", 2016.9, H.GREEN,
     [(2017.4, "ATSC 3.0", -1, "center"), (2018.3, "DVB Ph2", 1, "center"),
      (2020.4, "美国开播", 1, "left")]),
    ("DisplayHDR 分级", 2018.8, H.RED,
     [(2018.8, "1.0", -1, "center"), (2019.9, "True Black", 1, "left"),
      (2022.2, "1.2", -1, "center")]),
    ("Dolby Vision / 菁彩 HDR", 2014.2, H.GOLD,
     [(2014.2, "DV 电视", -1, "left"), (2020.2, "CUVA", 1, "center")]),
]

ypos = list(range(len(rows)))[::-1]
DY = 0.34
for (lab, start, col, marks), y in zip(rows, ypos):
    ax.plot([start, END], [y, y], color=col, linewidth=6.5, alpha=0.20,
            solid_capstyle="round", zorder=2)
    ax.plot([start, END], [y, y], color=col, linewidth=1.0, alpha=0.9, zorder=3)
    for i, (x, txt, side, ha) in enumerate(marks):
        ax.plot([x], [y], marker="o", markersize=7.0 if i == 0 else 4.8, color=col,
                markeredgecolor="white", markeredgewidth=1.0, zorder=6)
        ax.text(x, y + side * DY, txt, fontsize=7.4, color="#33404f",
                ha=ha, va="bottom" if side > 0 else "top", zorder=7)

ax.set_yticks(ypos)
ax.set_yticklabels([r[0] for r in rows], fontsize=8.4)
ax.set_ylim(-0.72, len(rows) - 0.28)
ax.set_xlim(X0, X1)
ax.set_xticks(range(2014, 2027, 2))
ax.tick_params(axis="x", labelsize=9)
ax.grid(axis="y", visible=False)
ax.grid(axis="x", color="#e3e8ee", linewidth=0.7)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

ax.axvspan(2026.2, X1, color="#f1f3f6", zorder=0)
ax.text(2027.15, -0.62, "仍在修订", fontsize=7.2, color="#8a96a3",
        ha="right", va="bottom")

H.save(fig, 12, "f2_timeline")
