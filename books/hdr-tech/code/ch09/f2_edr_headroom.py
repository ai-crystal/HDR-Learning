# -*- coding: utf-8 -*-
"""第 09 章 图 2：EDR 余量随 SDR 白点变化（余量 = log2(峰值 / SDR 白)）。"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

white = np.linspace(60, 1100, 600)
peaks = [(800, H.TEAL, "峰值 800 nit"), (1200, H.BLUE, "峰值 1200 nit"),
         (1600, H.ORANGE, "峰值 1600 nit")]

fig, ax = plt.subplots(figsize=(7.2, 4.1))
for pk, c, lab in peaks:
    ax.plot(white, np.log2(pk / white), color=c, lw=2.2, label=lab)

ax.axvline(203, color=H.GRAY, lw=1.0, ls=":")
ax.text(210, 3.62, "BT.2408 参考白 203 nit", fontsize=8.2, color=H.GRAY)
ax.axhline(1.0, color=H.RED, lw=1.0, ls="--")
ax.text(70, 1.12, "1 档余量", fontsize=8.2, color=H.RED)

ax.plot([203], [np.log2(1600 / 203)], "o", ms=6, color=H.ORANGE)
ax.annotate("3.0 档", xy=(203, np.log2(1600 / 203)), xytext=(300, 3.25),
            fontsize=9, color=H.ORANGE,
            arrowprops=dict(arrowstyle="-", color=H.ORANGE, lw=1.0))

ax.set_xlim(60, 1100)
ax.set_ylim(0, 4.0)
ax.set_xlabel("屏幕上的 SDR 白点亮度（nit）")
ax.set_ylabel("EDR 余量（档，log2 峰值除以白点）")
ax.legend(loc="upper right", fontsize=8.6)
ax.grid(alpha=0.55)
H.save(fig, 9, "f2_edr_headroom")
