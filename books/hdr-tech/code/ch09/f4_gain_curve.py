# -*- coding: utf-8 -*-
"""第 09 章 图 4：增益图在重建时的三条曲线（按 sRGB EOTF 与 203 nit 白点计算）。"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

code = np.linspace(0, 255, 512)
lin = H.srgb_eotf(code / 255.0) * 203.0

fig, ax = plt.subplots(figsize=(7.2, 4.2))
for g, c, lab in [(0.0, H.GRAY, "增益 0 档（SDR 原样）"),
                  (1.5, H.TEAL, "增益 1.5 档"),
                  (3.0, H.ORANGE, "增益 3 档")]:
    ax.plot(code, lin * 2 ** g, color=c, lw=2.2, label=lab)

ax.axhline(203, color=H.NAVY, lw=1.0, ls=":")
ax.text(6, 214, "SDR 白 203 nit", fontsize=8.2, color=H.NAVY)
ax.axhline(1000, color=H.RED, lw=1.1, ls="--")
ax.text(6, 1055, "显示峰值 1000 nit", fontsize=8.2, color=H.RED)

ax.fill_between(code, 1000, 2200, where=(lin * 2 ** 3.0) > 1000,
                color=H.ORANGE, alpha=0.12, lw=0)
ax.text(66, 1730, "超峰值的部分在这里被压回", fontsize=8.2, color=H.ORANGE,
        ha="left", va="center")

ax.set_yscale("log")
ax.set_xlim(0, 255)
ax.set_ylim(0.5, 2200)
ax.set_xlabel("基础层码值（8 bit）")
ax.set_ylabel("重建后的绝对亮度（nit，对数）")
ax.legend(loc="lower right", fontsize=8.6)
H.save(fig, 9, "f4_gain_curve")
