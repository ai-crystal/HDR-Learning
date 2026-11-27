# -*- coding: utf-8 -*-
"""第 12 章 图 4：绝对亮度对色差读数的影响。

同一个内容整体搬到亮 k 倍的屏上（参考白与适应亮度一起按比例放大），四种度量
给出的读数变化。$\Delta E_{00}$ 按定义完全不变，因为它只看得见相对参考白的坐标，
另外三套在绝对亮度上计算的度量都会变，变化幅度各不相同。
右图用 CAM16 的彩度与色彩量解释这份差异的来源，Hunt 效应让高亮度下的彩度
本身变大，色彩量涨得更快。
"""
import os
import sys
import numpy as np
import matplotlib.ticker as mticker

sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metrics as M

plt = H.plt

BASE = 203.0
L, C, h = 70.0, 45.0, 40.0
DL, DC, DH = -2.0, 4.0, 1.5

lab1 = M.lch_to_lab(L, np.array(C), np.array(h))
lab2 = M.lch_to_lab(L + DL, np.array(C + DC), np.array(h + DH))
x1 = M.lab_to_xyz(lab1, white_ref=BASE)
x2 = M.lab_to_xyz(lab2, white_ref=BASE)

KS = np.logspace(0, 1, 60)

KEYS = [("$\\Delta E_{00}$", "dE00", H.NAVY),
        ("$\\Delta E_{ITP}$", "dEITP", H.ORANGE),
        ("$\\Delta E_z$", "dEz", H.TEAL),
        ("$\\Delta E'_{CAM16}$", "dEu", H.PURPLE)]

ref = {}
curves = {k: [] for _, k, _ in KEYS}
curves_c, curves_m = [], []
for k in KS:
    mm = M.Metrics(white_lum=BASE * k, L_A=0.2 * BASE * k)
    r = mm.all(x1 * k, x2 * k)
    if not ref:
        ref = dict(r)
    for _, key, _ in KEYS:
        curves[key].append(r[key] / ref[key])
    cam = mm.cam.forward(x1 * k)
    curves_c.append(cam["C"])
    curves_m.append(cam["M"])

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.4),
                         gridspec_kw=dict(wspace=0.28))

ax = axes[0]
for txt, key, col in KEYS:
    ax.plot(KS, curves[key], color=col, lw=2.0, label=txt)
ax.axhline(1.0, color=H.LGRAY, lw=1.0, ls="--")
ax.set_xscale("log")
ax.xaxis.set_minor_formatter(mticker.NullFormatter())
ax.set_xlim(1, 10)
ax.set_xticks([1, 2, 5, 10])
ax.set_xticklabels(["1", "2", "5", "10"])
ax.set_ylim(0.90, 1.76)
ax.set_xlabel("参考白相对 203 cd m$^{-2}$ 的倍数")
ax.set_ylabel("读数相对 203 cd m$^{-2}$ 处的比值")
ax.legend(loc="upper left", fontsize=8.2, handlelength=1.6,
          borderpad=0.45, labelspacing=0.3)
ax.text(9.4, 0.928, "$\\Delta E_{00}$ 恒为 1", fontsize=8.0, color=H.NAVY,
        ha="right")

ax = axes[1]
ax.plot(KS, curves_c, color=H.RED, lw=2.0, label="彩度 $C$")
ax.plot(KS, curves_m, color=H.GOLD, lw=2.0, label="色彩量 $M$")
ax.set_xscale("log")
ax.xaxis.set_minor_formatter(mticker.NullFormatter())
ax.set_xlim(1, 10)
ax.set_xticks([1, 2, 5, 10])
ax.set_xticklabels(["1", "2", "5", "10"])
ax.set_ylim(0, 72)
ax.set_xlabel("参考白相对 203 cd m$^{-2}$ 的倍数")
ax.set_ylabel("CAM16 的彩度与色彩量")
ax.legend(loc="upper left", fontsize=8.4, handlelength=1.6)
ax.text(9.6, curves_c[-1] - 4.0, "%.1f" % curves_c[-1], fontsize=8.4,
        color=H.RED, ha="right")
ax.text(9.6, curves_m[-1] + 2.2, "%.1f" % curves_m[-1], fontsize=8.4,
        color=H.GOLD, ha="right")
ax.text(1.08, curves_c[0] + 2.0, "%.1f" % curves_c[0], fontsize=8.4,
        color=H.RED)
ax.text(1.08, curves_m[0] - 4.0, "%.1f" % curves_m[0], fontsize=8.4,
        color=H.GOLD)

H.save(fig, 12, "f4_luminance_drift")
