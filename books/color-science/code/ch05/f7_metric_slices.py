# -*- coding: utf-8 -*-
"""第 05 章 图 7：度量口径的影响与按亮度切片的色域断面。

左图：三个色域在四种口径下的相对大小（都以 BT.2020 为 100%）。
右图：CIELAB 中按 L* 切片的色域断面面积随明度的变化。
所有数值由基色坐标与矩阵直接计算。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import gamut as G

plt = H.plt

GAMS = ["sRGB", "P3", "BT2020"]
LABELS = {"sRGB": "sRGB", "P3": "Display P3", "BT2020": "BT.2020"}
COLS = {"sRGB": H.GRAY, "P3": H.TEAL, "BT2020": H.NAVY}

area_xy, area_uv, vol_lab, vol_luv = {}, {}, {}, {}
for g in GAMS:
    xy = G.prim_xy(g)
    area_xy[g] = G.uv_area((xy[:, 0], xy[:, 1]))
    uv = G.xy_to_uv76(xy[:, 0], xy[:, 1])
    area_uv[g] = G.uv_area((uv[0], uv[1]))
    vol_lab[g] = G.gamut_volume_lab(g, n=40)
    vol_luv[g] = G.gamut_volume_luv(g, n=40)

fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.8),
                         gridspec_kw=dict(width_ratios=[1.0, 1.10], wspace=0.30))
fig.subplots_adjust(left=0.085, right=0.985, top=0.90, bottom=0.17)

# ---------------- (a) 四种口径 ----------------
ax = axes[0]
METRICS = [("$xy$ 面积", area_xy), ("$u'v'$ 面积", area_uv),
           ("CIELAB 体积", vol_lab), ("CIELUV 体积", vol_luv)]
width = 0.20
xs = np.arange(len(METRICS))
for k, g in enumerate(GAMS):
    vals = [100.0 * m[1][g] / m[1]["BT2020"] for m in METRICS]
    bars = ax.bar(xs + (k - 1) * width, vals, width=width * 0.92,
                  color=COLS[g], edgecolor="#3b4653", linewidth=0.5,
                  label=LABELS[g])
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.2, f"{v:.0f}", ha="center",
                fontsize=7.0, color="#22303f")
ax.set_xticks(xs)
ax.set_xticklabels([m[0] for m in METRICS], fontsize=8.4)
ax.set_ylim(0, 118)
ax.set_ylabel("相对 BT.2020 的百分比（%）", fontsize=9.4)
ax.legend(loc="upper left", fontsize=7.6, ncol=3, columnspacing=0.9,
          handletextpad=0.45, borderpad=0.35)
ax.grid(axis="x", visible=False)
# ---------------- (b) 按 L* 切片的断面面积 ----------------
ax2 = axes[1]
LS = np.arange(8, 97, 4)
for g in GAMS:
    areas = np.array([G.lab_slice_area(g, L, n=72) for L in LS])
    ax2.plot(LS, areas / 1000.0, "-o", color=COLS[g], lw=1.9, ms=3.4,
             label=LABELS[g])
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 40)
ax2.set_xlabel("$L^*$（CIELAB 明度）", fontsize=9.5)
ax2.set_ylabel("断面面积（$10^3$ 平方单位）", fontsize=9.5)
ax2.legend(loc="upper left", fontsize=7.6, handletextpad=0.6, borderpad=0.35)
ax2.annotate("峰值在 $L^*$≈60", xy=(60, 34.4), xytext=(72, 37.0), fontsize=7.2,
             color="#39435a", ha="left",
             arrowprops=dict(arrowstyle="-|>", color="#39435a", lw=0.9,
                             shrinkA=2, shrinkB=4))

H.save(fig, 5, "f7_metric_slices")
