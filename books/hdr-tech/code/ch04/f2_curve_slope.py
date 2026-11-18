# -*- coding: utf-8 -*-
"""第 04 章 图 2：各算子的对数斜率（局部对比保持度）。

斜率定义为 d(log L_out) / d(log L_in)，等于 1 表示该亮度附近的明暗差异被原样保留，
小于 1 表示局部对比被压缩，趋近 0 表示该段亮度被压成一片。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt


def reinhard(L, Lw=4.0):
    return L * (1.0 + L / Lw ** 2) / (1.0 + L)


def hable(x, A=0.15, B=0.50, C=0.10, D=0.20, E=0.02, F=0.30):
    return (x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F) - E / F


def aces_fit(x):
    x = np.clip(x, 0.0, None)
    return np.clip(x * (2.51 * x + 0.03) / (x * (2.43 * x + 0.59) + 0.14), 0.0, 1.0)


nit = np.logspace(np.log10(0.2), np.log10(399.0), 2000)
PEAK = 400.0

curves = {
    "Reinhard 扩展式": reinhard(nit / 100.0, Lw=PEAK / 100.0),
    "Hable / Uncharted 2": hable(nit / 100.0) / hable(PEAK / 100.0),
    "ACES 拟合": aces_fit((nit / 100.0) / (PEAK / 100.0)) / aces_fit(1.0),
    "线性截断": np.clip(nit / PEAK, 0.0, 1.0),
}
colors = {"Reinhard 扩展式": H.BLUE, "Hable / Uncharted 2": H.ORANGE,
          "ACES 拟合": H.RED, "线性截断": H.LGRAY}

fig, ax = plt.subplots(figsize=(7.2, 4.2))
for name, y in curves.items():
    y = np.clip(y, 1e-6, None)
    slope = np.gradient(np.log10(y), np.log10(nit))
    kw = dict(lw=1.6, ls=(0, (4, 2))) if name == "线性截断" else dict(lw=2.2)
    ax.plot(nit, np.clip(slope, 0, 1.68), color=colors[name], label=name, **kw)

ax.axhline(1.0, color=H.GRAY, lw=1.0, ls=":", label="斜率 1（对比不变）")
ax.axvline(100.0, color=H.GRAY, lw=1.0, ls=":")

ax.set_xscale("log")
ax.set_xlim(0.2, 420)
ax.set_ylim(0.0, 1.72)
ax.set_xlabel("输入亮度（nit，对数刻度）")
ax.set_ylabel("斜率 d(log $L_{out}$) / d(log $L_{in}$)")
ax.legend(loc="lower left", fontsize=8.5)
H.save(fig, 4, "f2_curve_slope")
