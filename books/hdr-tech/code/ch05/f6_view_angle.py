# -*- coding: utf-8 -*-
"""第 05 章 图 6：视角对对比度与色度的影响（模型估算，用于说明趋势，非厂商实测）。

(a) 归一化对比度随视角的衰减，用 CR(θ)/CR(0) = cos^n(θ) 表示，
    n 分别取 6（VA）、2.2（IPS）、0.8（自发光）；
(b) 色度漂移 Δu'v' 随视角的变化，用 k·(1-cos θ) 表示，
    k 分别取 0.020、0.008、0.003。
两条模型都只刻画单调衰减的趋势与量级，具体数值取决于面板结构与光学膜。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

th = np.linspace(0, 70, 400)
c = np.cos(np.radians(th))

panels = [
    ("VA 液晶（3000:1）", 6.0, 0.020, H.NAVY),
    ("IPS 液晶（1200:1）", 2.2, 0.008, H.TEAL),
    ("自发光（$10^6$:1）", 0.8, 0.003, H.ORANGE),
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 4.0))
fig.subplots_adjust(wspace=0.30)

for name, n, k, color in panels:
    ax1.plot(th, c ** n, color=color, lw=2.1, label=name)
    ax2.plot(th, k * (1 - c), color=color, lw=2.1, label=name)

ax1.axvline(30, color=H.GRAY, lw=0.9, ls=":")
ax1.text(31, 0.06, "30°", fontsize=8.2, color=H.GRAY)
ax1.set_xlim(0, 70)
ax1.set_ylim(0, 1.05)
ax1.set_xlabel("偏离屏幕法线的角度（度）")
ax1.set_ylabel("对比度相对正视角的比例")
ax1.legend(loc="upper right", fontsize=8.0, labelspacing=0.3, borderpad=0.4)
ax1.set_title("(a) 对比度衰减", fontsize=10, pad=4)

ax2.axvline(30, color=H.GRAY, lw=0.9, ls=":")
ax2.set_xlim(0, 70)
ax2.set_ylim(0, 0.0135)
ax2.set_xlabel("偏离屏幕法线的角度（度）")
ax2.set_ylabel("色度漂移 $\\Delta u'v'$")
ax2.axhline(0.004, color=H.GRAY, lw=0.9, ls="--")
ax2.legend(loc="upper left", fontsize=8.0, labelspacing=0.3, borderpad=0.4)
ax2.set_title("(b) 色度漂移", fontsize=10, pad=4)

H.save(fig, 5, "f6_view_angle")
