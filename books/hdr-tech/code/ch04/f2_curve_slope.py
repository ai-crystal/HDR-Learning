# -*- coding: utf-8 -*-
"""第 04 章 图 2：各算子的对数斜率与剩余对比度。

(a) 斜率 s = d(log L_out) / d(log L_in)。s = 1 表示该亮度附近的明暗比例被原样保留；
(b) 把 s 换成可以直接读的物理量：一对相差一档（2 倍）的输入，经过映射后还剩多少倍。
    输出比值 = f(2L) / f(L)，s = 1 时等于 2，s = 0.5 时约等于 1.41，s = 0 时等于 1。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

PEAK = 400.0


def reinhard(L, Lw=4.0):
    return L * (1.0 + L / Lw ** 2) / (1.0 + L)


def hable(x, A=0.15, B=0.50, C=0.10, D=0.20, E=0.02, F=0.30):
    return (x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F) - E / F


def aces_fit(x):
    x = np.clip(x, 0.0, None)
    return np.clip(x * (2.51 * x + 0.03) / (x * (2.43 * x + 0.59) + 0.14), 0.0, 1.0)


def power_shoulder(nit, gamma=2.2):
    x = np.clip(nit / PEAK, 0.0, 1.0)
    return 1.0 - (1.0 - x) ** gamma


nit = np.logspace(np.log10(0.2), np.log10(399.0), 2400)

curves = {
    "幂次肩部": power_shoulder(nit),
    "Reinhard 扩展式": np.clip(reinhard(nit / 100.0, Lw=PEAK / 100.0), 0, 1),
    "Hable / Uncharted 2": hable(nit / 100.0) / hable(PEAK / 100.0),
    "ACES 拟合": aces_fit((nit / 100.0) / (PEAK / 100.0)) / aces_fit(1.0),
    "线性截断": np.clip(nit / PEAK, 0.0, 1.0),
}
colors = {"幂次肩部": H.PURPLE, "Reinhard 扩展式": H.BLUE,
          "Hable / Uncharted 2": H.ORANGE, "ACES 拟合": H.RED,
          "线性截断": H.LGRAY}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 4.0))
fig.subplots_adjust(wspace=0.28)

for name, y in curves.items():
    y = np.clip(y, 1e-7, None)
    slope = np.gradient(np.log10(y), np.log10(nit))
    kw = dict(lw=1.5, ls=(0, (4, 2))) if name == "线性截断" else dict(lw=2.0)
    ax1.plot(nit, np.clip(slope, 0.0, 1.75), color=colors[name], label=name, **kw)

ax1.axhline(1.0, color=H.GRAY, lw=0.9, ls=":")
ax1.axvspan(1.0, 50.0, color="#e8eef5", lw=0, zorder=0)
ax1.text(7.0, 1.66, "中间调", fontsize=8.5, color="#5b6b7c", ha="center", va="center")
ax1.set_xscale("log")
ax1.set_xlim(0.2, 420)
ax1.set_ylim(0.0, 1.75)
ax1.set_xlabel("输入亮度（nit，对数刻度）")
ax1.set_ylabel("斜率 d(log $L_{out}$) / d(log $L_{in}$)")
ax1.legend(loc="lower left", fontsize=7.8, labelspacing=0.3, borderpad=0.4)
ax1.set_title("(a) 对数斜率", fontsize=10, pad=4)

# ---- (b) 一档输入在映射后剩下多少 ----
for name, y in curves.items():
    if name == "线性截断":
        continue
    x2 = nit[:-1] * 2.0
    idx = np.searchsorted(nit, x2, side="right") - 1
    idx = np.clip(idx, 0, len(nit) - 2)
    y1 = np.clip(y[:-1], 1e-7, None)
    y2 = np.clip(y[idx + 1], 1e-7, None)
    ratio = y2 / y1
    kw = dict(lw=2.0)
    ax2.plot(nit[:-1], np.clip(ratio, 1.0, 3.0), color=colors[name], label=name, **kw)

ax2.axhline(2.0, color=H.GRAY, lw=0.9, ls=":")
ax2.axhline(1.0, color=H.GRAY, lw=0.9, ls=":")
ax2.text(195, 2.03, "2×：对比原样保留", fontsize=7.8, color=H.GRAY, va="bottom", ha="right")
ax2.text(195, 1.03, "1×：对比完全丢失", fontsize=7.8, color=H.GRAY, va="bottom", ha="right")
ax2.set_xscale("log")
ax2.set_xlim(0.2, 200)
ax2.set_ylim(0.95, 3.05)
ax2.set_xlabel("输入亮度（nit，对数刻度）")
ax2.set_ylabel("一对相差一档的输入，输出还剩多少倍")
ax2.set_title("(b) 剩余对比度", fontsize=10, pad=4)

H.save(fig, 4, "f2_curve_slope")
