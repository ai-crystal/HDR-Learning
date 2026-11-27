# -*- coding: utf-8 -*-
"""图 8-2 同一亮度在 scRGB 与 PQ 两套编码里的取值，以及相邻码值的相对步长。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("hdr-tech")
import numpy as np
from matplotlib.ticker import FuncFormatter

plt = H.plt
plt.rcParams["mathtext.fontset"] = "dejavusans"

def plain_log(v, pos):
    """对数轴刻度写成普通十进制，避开 CJK 字体缺少数学负号的问题。"""
    if v >= 1:
        return f"{v:g}"
    if v >= 0.01:
        return f"{v:g}"
    return f"{v:g}"

fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.3))
ax1, ax2 = axes

L = np.logspace(-2, 4, 900)

sc = L / 80.0
pqc = H.pq_oetf(L)

l1, = ax1.plot(L, sc, color=H.ORANGE, lw=2.2, label="scRGB 数值（1.0 记 80 nit）")
ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlim(0.01, 10000)
ax1.set_ylim(3e-5, 600)
ax1.set_xlabel("绝对亮度（nit）")
ax1.set_ylabel("scRGB 数值", color=H.ORANGE)
ax1.tick_params(axis="y", colors=H.ORANGE)
ax1.xaxis.set_major_formatter(FuncFormatter(plain_log))
ax1.yaxis.set_major_formatter(FuncFormatter(plain_log))

ax1b = ax1.twinx()
l2, = ax1b.plot(L, pqc, color=H.NAVY, lw=2.2, label="PQ 码值（0 到 1）")
ax1b.set_ylim(0, 1.10)
ax1b.set_ylabel("PQ 归一化码值", color=H.NAVY)
ax1b.tick_params(axis="y", colors=H.NAVY)
ax1b.grid(False)

for lv in (80, 203, 1000):
    ax1.plot([lv, lv], [3e-5, 600], color="#b8c2cc", lw=0.8, ls="--", zorder=0)

for lv, txt in ((80, "80 nit"), (203, "203 nit"), (1000, "1000 nit")):
    ax1.plot([lv], [lv / 80.0], "o", ms=5, color=H.ORANGE, zorder=6,
             markeredgecolor="white", markeredgewidth=0.8)
    ax1.text(lv * 0.72, lv / 80.0 * 1.6, txt, fontsize=7.8, color="#b8590f",
             ha="right", va="bottom")

ax1.axhline(7.5, color=H.GRAY, lw=1.0, ls=":")
ax1.text(0.012, 9.4, "常用上限 7.5，即 600 nit", fontsize=7.6, color=H.GRAY)
ax1.axhline(1.0, color=H.GRAY, lw=1.0, ls=":")
ax1.text(0.012, 0.62, "参考白 1.0，即 80 nit", fontsize=7.6, color=H.GRAY)

ax1.set_title("(a) 同一亮度的两种写法", fontsize=10, pad=8)
ax1.legend(handles=[l1, l2], loc="lower right", fontsize=7.8)

# ---------- 右：相邻码值的相对步长 ----------
Lg = np.logspace(-2, 3.7, 800)

def rel_step_pq(bits, Lv):
    code = H.pq_oetf(Lv)
    step = 1.0 / (2 ** bits - 1)
    hi = H.pq_eotf(np.clip(code + step / 2, 0, 1))
    lo = H.pq_eotf(np.clip(code - step / 2, 0, 1))
    return (hi - lo) / Lv

v = Lg / 80.0
e = np.floor(np.log2(v))
fp16 = 2.0 ** (e - 10) / v

ax2.semilogx(Lg, fp16 * 100, color=H.ORANGE, lw=1.6, label="scRGB 用 FP16")
ax2.semilogx(Lg, rel_step_pq(10, Lg) * 100, color=H.NAVY, lw=2.0, label="PQ 用 10 bit")
ax2.semilogx(Lg, rel_step_pq(12, Lg) * 100, color=H.TEAL, lw=1.6, ls="--", label="PQ 用 12 bit")
ax2.set_xlim(0.01, 5000)
ax2.set_ylim(0, 10)
ax2.set_xlabel("绝对亮度（nit）")
ax2.set_ylabel("相邻码值的相对亮度差（%）")
ax2.set_title("(b) 同一亮度处的量化细度", fontsize=10, pad=8)
ax2.xaxis.set_major_formatter(FuncFormatter(plain_log))
ax2.legend(loc="upper right", fontsize=8)
ax2.axhline(1.0, color=H.GRAY, lw=0.9, ls=":")
ax2.text(0.011, 1.12, "1% 参考线", fontsize=7.6, color=H.GRAY)

fig.subplots_adjust(wspace=0.46)
H.save(fig, 8, "f2_scrgb_vs_pq")
