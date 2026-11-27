# -*- coding: utf-8 -*-
"""第 07 章 图 3：六条传递函数的形状与局部斜率。

(a) 编码值随线性光的变化（线性轴取对数）
(b) 局部伽马 d(log 码值)/d(log 线性)，反映曲线在每一段把多少码值留给暗部
公式来源：IEC 61966-2-1（sRGB）、BT.709、BT.2020、SMPTE ST 2084（PQ）、
BT.2100（HLG）、ARRI LogC3（SUP 3.x，EI 800）。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rgbspace as R

plt = H.plt

L = np.logspace(-4, 0, 900)
CURVES = [
    ("纯 gamma 2.2", R.gamma_oetf(L, 2.2), H.GRAY, (0, (5, 3))),
    ("sRGB 分段", R.srgb_oetf(L), H.NAVY, "-"),
    ("BT.709 OETF", R.rec709_oetf(L), H.ORANGE, "-"),
    ("BT.2020 OETF", R.rec2020_oetf(L), H.TEAL, (0, (6, 2, 1, 2))),
    ("PQ（0 到 10000 nit）", R.pq_oetf(L * 10000), H.RED, "-"),
    ("HLG OETF", R.hlg_oetf(L), H.PURPLE, "-"),
    ("LogC3（EI 800）", R.logc3_oetf(L), H.GREEN, "-"),
]

fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.0), gridspec_kw={"wspace": 0.26})

ax = axes[0]
for name, v, col, ls in CURVES:
    ax.plot(L, v, color=col, ls=ls, lw=1.8, label=name)
ax.set_xscale("log")
ax.set_xlim(1e-4, 1.0)
TICKS = [1e-4, 1e-3, 1e-2, 1e-1, 1.0]
ax.set_xticks(TICKS)
ax.set_xticklabels(["0.0001", "0.001", "0.01", "0.1", "1"])
ax.set_ylim(0, 1.02)
ax.set_xlabel("线性光（相对值）")
ax.set_ylabel("编码值")
ax.set_title("(a) 编码曲线的形状", fontsize=10.5, pad=6)
ax.legend(loc="upper left", fontsize=7.4, handlelength=1.9, labelspacing=0.3,
          borderaxespad=0.2)

# ---------- (b) 局部伽马 ----------
ax = axes[1]
BREAKS = {"sRGB 分段": 0.0031308, "BT.709 OETF": 0.018, "BT.2020 OETF": 0.0181}
for name, v, col, ls in CURVES:
    y = np.asarray(v)
    ok = y > 2e-4
    if name in BREAKS:
        # 分段点两侧斜率不同，附近点会让数值微分出现假尖峰，跳过
        ok &= np.abs(np.log10(L / BREAKS[name])) > 0.04
    slope = np.gradient(np.log10(y[ok]), np.log10(L[ok]))
    ax.plot(L[ok], slope, color=col, ls=ls, lw=1.7)
ax.set_xscale("log")
ax.set_xlim(1e-4, 1.0)
TICKS = [1e-4, 1e-3, 1e-2, 1e-1, 1.0]
ax.set_xticks(TICKS)
ax.set_xticklabels(["0.0001", "0.001", "0.01", "0.1", "1"])
ax.set_ylim(0, 1.42)
ax.axhline(1.0, color="#9aa6b2", lw=0.9, ls=(0, (2, 2)))
ax.text(0.0105, 1.10, "斜率 1：码值与光成正比", fontsize=7.6, color="#7f8c8d",
        va="bottom", ha="left")
ax.set_xlabel("线性光（相对值）")
ax.set_ylabel("局部伽马  d log(码值) / d log(线性)")
ax.set_title("(b) 曲线把码值分给哪一段亮度", fontsize=10.5, pad=6)

H.save(fig, 7, "f3_transfer_curves")
