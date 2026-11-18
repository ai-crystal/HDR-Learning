# -*- coding: utf-8 -*-
"""第 06 章 图 3：10 bit 与 12 bit PQ 编码的相邻码值亮度台阶。

PQ 码值 k/N 与 (k+1)/N 解码后得到两个绝对亮度，二者之差即该亮度处的量化台阶。
同时给出对应的 ΔE_ITP（中性灰，I 轴差值乘 720）。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import ictcp as T

plt = H.plt

fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.9))
fig.subplots_adjust(left=0.085, right=0.985, top=0.93, bottom=0.19, wspace=0.28)

BITS = [(10, H.NAVY, "-"), (12, H.ORANGE, (0, (6, 3)))]

for bits, col, ls in BITS:
    N = 2 ** bits - 1
    k = np.arange(1, N)
    lo = T.pq_eotf(k / N)
    hi = T.pq_eotf((k + 1) / N)
    mid = 0.5 * (lo + hi)
    step = hi - lo
    axes[0].plot(mid, step, color=col, lw=2.0, ls=ls, label=f"{bits} bit")
    axes[1].plot(mid, 100 * step / np.maximum(mid, 1e-9), color=col, lw=2.0, ls=ls,
                 label=f"{bits} bit")

for ax in axes:
    ax.set_xscale("log")
    ax.set_xlim(1e-2, 1e4)
    ax.axvline(100, color="#b9a29b", lw=1.0, ls=(0, (5, 3)))
    ax.set_xlabel("亮度（cd/m$^2$）", fontsize=10)
    ax.grid(which="major", color="#dde3ea", lw=0.7)

axes[0].set_yscale("log")
axes[0].set_ylabel("相邻码值的亮度差（cd/m$^2$）", fontsize=9.6)
axes[0].legend(loc="upper left", fontsize=8.6, frameon=False)
axes[0].text(110, 3e-3, "参考白\n203 cd/m$^2$", fontsize=7.6, color="#69747f",
             va="bottom")

axes[1].set_yscale("log")
axes[1].set_ylabel("相对亮度台阶（%）", fontsize=10)
axes[1].legend(loc="upper right", fontsize=8.6, frameon=False)
axes[1].axhline(1.0, color="#c9d3de", lw=1.0)
axes[1].text(1.4e-2, 1.15, "1% 台阶", fontsize=7.6, color="#69747f", va="bottom")

H.save(fig, 6, "f3_pq_step")
