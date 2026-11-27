# -*- coding: utf-8 -*-
"""第 07 章 图 6：位深与码值分配的效率。

纵轴 = 相邻码值之间的相对亮度台阶（(L(n+1) - L(n)) / L(n)），
与人眼的亮度分辨阈值（约 1%）比较，可以看出每种编码在哪个亮度段用完码值。
线性编码按 0 到 100 尼特满量程计；PQ 按 0 到 10000 尼特绝对量程计。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rgbspace as R

plt = H.plt

L = np.logspace(-2.3, 3.0, 700)          # 0.005 到 1000 尼特


def step_from_curve(eotf, bits, lmax):
    """给定 EOTF，返回每个亮度处的相对台阶（%）。"""
    v = eotf(L / lmax)                    # 反查码值
    dv = 1.0 / (2 ** bits - 1)
    l2 = lmax * R.pq_eotf(np.clip(v + dv * 0, 0, 1))  # 占位，下面统一处理
    return v, dv


fig, ax = plt.subplots(figsize=(7.2, 4.2))

# 线性编码：台阶 = Lmax / (2^b - 1)，相对台阶除以 L
for bits, col, ls in ((8, H.RED, "-"), (10, H.ORANGE, "-"), (12, H.GOLD, (0, (5, 2)))):
    rel = (100.0 / (2 ** bits - 1)) / L * 100
    ax.plot(L, rel, color=col, lw=1.7, ls=ls, label=f"线性 {bits} bit")

# sRGB 8 bit
v = R.srgb_oetf(np.clip(L / 100.0, 0, 1))
dv = 1.0 / 255.0
L2 = 100.0 * R.srgb_eotf(np.clip(v + dv, 0, 1))
rel = (L2 - L) / L * 100
rel = np.where(v + dv <= 1.0, rel, np.nan)
ax.plot(L, rel, color=H.NAVY, lw=1.9, label="sRGB 8 bit")

# PQ 10 / 12 bit
for bits, col, ls in ((10, H.TEAL, "-"), (12, H.PURPLE, (0, (5, 2)))):
    v = R.pq_oetf(L)
    dv = 1.0 / (2 ** bits - 1)
    L2 = R.pq_eotf(np.clip(v + dv, 0, 1))
    rel = (L2 - L) / L * 100
    ax.plot(L, rel, color=col, lw=1.7, ls=ls, label=f"PQ {bits} bit")

ax.axhline(1.0, color="#4a5666", lw=1.0, ls=(0, (3, 3)), label="1% 参考线")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.005, 1000)
ax.set_ylim(0.02, 400)
ax.set_xticks([0.01, 0.1, 1, 10, 100, 1000])
ax.set_xticklabels(["0.01", "0.1", "1", "10", "100", "1000"])
ax.set_yticks([0.1, 1, 10, 100])
ax.set_yticklabels(["0.1", "1", "10", "100"])
ax.set_xlabel("显示亮度（尼特）")
ax.set_ylabel("相邻码值的相对台阶  %")
ax.legend(loc="upper right", fontsize=7.6, ncol=2, handlelength=2.0,
          labelspacing=0.35, columnspacing=1.3, borderaxespad=0.3)

H.save(fig, 7, "f6_bitdepth")
