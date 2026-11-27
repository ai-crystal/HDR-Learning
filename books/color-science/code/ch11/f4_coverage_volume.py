# -*- coding: utf-8 -*-
"""第 11 章 图 4：覆盖率与色域体积两种度量给出的排序不一致。

六个"设备"的基色都是真实坐标，峰值亮度按各自工艺给一个量级值：
sRGB 300 nit、Display P3 400 nit、量子点面板 500 nit、同基色的 RGBW 版本
（彩色子像素面积乘 0.75，白子像素追加 0.75 倍亮度）、五原色投影 300 nit、
以及 BT.2020 标准色域在 1000 nit 下的参考点。

覆盖率 = 与 BT.2020 三角形在 u'v' 中求交的面积比；
体积 = 在 CIELAB 中按凸包算，参考白为 1000 cd/m2 的 D65，归一化到参考点。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import primaries11 as P

plt = H.plt

bt2020 = [P.PRIMARIES["BT2020"][k] for k in "RGB"]
srgb = [P.PRIMARIES["sRGB"][k] for k in "RGB"]
p3 = [P.PRIMARIES["DisplayP3"][k] for k in "RGB"]
qd = [P.spd_to_xy(630, 25), P.spd_to_xy(525, 30), P.spd_to_xy(462, 20)]
prim3 = [P.xy_of_wavelength(638), P.xy_of_wavelength(532), P.xy_of_wavelength(465)]
prim5 = [prim3[0], P.xy_of_wavelength(590), prim3[1],
         P.xy_of_wavelength(490), prim3[2]]

Wxy = P.WHITE["D65"]
Wxyz = P.xy_to_XYZ(*Wxy, 1.0)


def vol_pct(prim, peak, rgbw=False):
    cols, s = P.covering_matrix(prim, Wxy, peak)
    if rgbw:
        cols = np.column_stack([cols * 0.75, Wxyz * 0.75 * peak])
    return P.lab_volume_abs(cols, levels=13)


VREF = vol_pct(bt2020, 1000.0)

rows = [("sRGB\n300 nit", srgb, 300.0, False),
        ("Display P3\n400 nit", p3, 400.0, False),
        ("量子点面板\n500 nit", qd, 500.0, False),
        ("同基色 RGBW\n白峰 750 nit", qd, 500.0, True),
        ("五原色投影\n300 nit", prim5, 300.0, False),
        ("BT.2020\n1000 nit", bt2020, 1000.0, False)]

cov = []
vol = []
for name, pr, pk, rgbw in rows:
    cov.append(P.coverage(pr, bt2020) * 100.0)
    vol.append(vol_pct(pr, pk, rgbw) / VREF * 100.0)

fig = plt.figure(figsize=(7.4, 3.9))
ax = fig.add_axes([0.075, 0.235, 0.905, 0.70])

x = np.arange(len(rows))
w = 0.36
b1 = ax.bar(x - w / 2, cov, w, color=H.TEAL, alpha=0.9, label="色域覆盖率（u′v′ 面积比）")
b2 = ax.bar(x + w / 2, vol, w, color=H.ORANGE, alpha=0.9, label="色域体积（CIELAB，归一化）")

for xi, v in zip(x - w / 2, cov):
    ax.text(xi, v + 2.0, f"{v:.0f}", ha="center", va="bottom", fontsize=7.4,
            color=H.TEAL)
for xi, v in zip(x + w / 2, vol):
    ax.text(xi, v + 2.0, f"{v:.0f}", ha="center", va="bottom", fontsize=7.4,
            color=H.ORANGE)

ax.set_xticks(x)
ax.set_xticklabels([r[0] for r in rows], fontsize=7.8, linespacing=1.35)
ax.set_ylim(0, 118)
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_ylabel("百分比（%）", fontsize=9.6)
ax.grid(axis="x", visible=False)
ax.legend(loc="upper left", fontsize=8.0, ncol=1, borderpad=0.5)

ax.axhline(100, color="#9aa6b2", lw=0.9, ls=(0, (3, 3)), zorder=0)

ax.annotate("", xy=(4.56, 99.0), xytext=(4.56, 30.0),
            arrowprops=dict(arrowstyle="<->", color="#8c3b1e", lw=1.0))
ax.text(4.70, 64.5, "相差 71 点", fontsize=7.2, color="#8c3b1e", rotation=90,
        ha="center", va="center")

H.save(fig, 11, "f4_coverage_volume")
for (name, pr, pk, rgbw), c, v in zip(rows, cov, vol):
    print(f"{name.replace(chr(10), ' | '):28s} cov {c:5.1f}%  vol {v:5.1f}%")
