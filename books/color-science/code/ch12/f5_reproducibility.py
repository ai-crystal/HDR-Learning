# -*- coding: utf-8 -*-
"""第 12 章 图 4：测量可复现性的两端。

左图：黑位读数由环境光在屏面的反射决定，$L_{refl}=\\rho E/\\pi$。同一块屏在 5 lx
与 200 lx 的暗室里，读出的黑位可以差一个数量级以上，OLED 的真黑被完全淹没。
右图：白场读数随探头倾角的变化，按 $\\cos^n\\theta$ 的亮度衰减模型，指数分别取
1.5、2.0、2.5，对应不同面板的视角特性。两端的误差来源不同，混在一个"重复性"
指标里就说不清是谁的问题。
"""
import os
import sys
import numpy as np

sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metrics as M

plt = H.plt

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.4),
                         gridspec_kw=dict(wspace=0.30))

# ---------------- (a) 黑位与环境照度
ax = axes[0]
E = np.logspace(-1, np.log10(500), 200)
STRAY = 0.002
for rho, col, ls in ((0.001, H.NAVY, "-"), (0.005, H.ORANGE, "-"),
                     (0.02, H.TEAL, "-")):
    L = rho * E / np.pi + STRAY
    ax.plot(E, L, color=col, lw=1.9, ls=ls,
            label="$\\rho=%.1f\\%%$" % (rho * 100))
ax.axhline(0.005, color=H.PURPLE, lw=1.4, ls=(0, (5, 3)))
ax.text(0.13, 0.0058, "OLED 真黑 0.005", fontsize=7.8, color=H.PURPLE, va="bottom",
        bbox=dict(fc="white", ec="none", pad=1.2))
ax.axhline(0.05, color=H.RED, lw=1.4, ls=(0, (5, 3)))
ax.text(0.13, 0.056, "LCD 真黑 0.05", fontsize=7.8, color=H.RED, va="bottom",
        bbox=dict(fc="white", ec="none", pad=1.2))
for lx, txt in ((5.0, "5 lx"), (200.0, "200 lx")):
    ax.axvline(lx, color=H.GRAY, lw=0.9, ls=":")
    ax.text(lx * 0.78, 3.4, txt, fontsize=7.8, color=H.GRAY, rotation=90,
            va="top", ha="center")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.1, 500)
ax.set_ylim(1e-3, 5)
ax.set_xlabel("暗室照度 $E$ / lx")
ax.set_ylabel("黑位读数 / cd m$^{-2}$")
ax.legend(loc="upper left", fontsize=8.2, handlelength=1.6, title="屏面反射率",
          title_fontsize=8.2)

# ---------------- (b) 白场与探头倾角
ax = axes[1]
th = np.linspace(0, 20, 200)
for n, col in ((1.5, H.NAVY), (2.0, H.ORANGE), (2.5, H.TEAL)):
    ax.plot(th, 100 * (1 - np.cos(np.radians(th)) ** n), color=col, lw=1.9,
            label="$n=%.1f$" % n)
ax.plot([5], [100 * (1 - np.cos(np.radians(5)) ** 2.0)], marker="o", ms=4.4,
        mfc="white", mec=H.ORANGE, mew=1.4, zorder=5)
ax.axvline(5, color=H.GRAY, lw=0.8, ls=":")
ax.set_xlim(0, 20)
ax.set_ylim(0, 18)
ax.set_xlabel("探头偏离法线的角度 $\\theta$ / °")
ax.set_ylabel("白场读数相对法线的偏差 / %")
ax.legend(loc="upper left", fontsize=8.2, handlelength=1.6,
          title="亮度随角衰减的指数", title_fontsize=8.2)

H.save(fig, 12, "f5_reproducibility")
