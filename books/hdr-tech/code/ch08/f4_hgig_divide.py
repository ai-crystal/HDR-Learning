# -*- coding: utf-8 -*-
"""图 8-4 HGiG 分工下的三种处理：直通、单次映射、两次映射。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("hdr-tech")
import numpy as np
from matplotlib.ticker import FuncFormatter

plt = H.plt

SRC, DST = 4000.0, 700.0        # 内容峰值与显示器峰值

def eetf(L, src, dst):
    """BT.2390 的 EETF，在 PQ 码值域做，返回绝对亮度。"""
    code = H.pq_oetf(np.clip(L, 0, src))
    E1 = code / H.pq_oetf(src)
    MaxLum = H.pq_oetf(dst) / H.pq_oetf(src)
    KS = 1.5 * MaxLum - 0.5
    t = np.clip((E1 - KS) / (1 - KS), 0, 1)
    P = ((2 * t ** 3 - 3 * t ** 2 + 1) * KS
         + (t ** 3 - 2 * t ** 2 + t) * (1 - KS)
         + (-2 * t ** 3 + 3 * t ** 2) * MaxLum)
    E2 = np.where(E1 < KS, E1, P)
    return H.pq_eotf(E2 * H.pq_oetf(dst))

L = np.logspace(0, 4, 1200)
direct = np.minimum(L, DST)
once = eetf(L, SRC, DST)
twice = eetf(eetf(L, SRC, 1000.0), 1000.0, DST)

fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.3))
ax1, ax2 = axes

ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlim(1, 10000)
ax1.set_ylim(1, 1200)
ax1.plot(L, direct, color=H.GRAY, lw=2.0, ls="--", label="直通后硬裁")
ax1.plot(L, once, color=H.BLUE, lw=2.2, label="单次映射")
ax1.plot(L, twice, color=H.ORANGE, lw=2.2, label="两次映射")

ax1.axvline(203, color="#ccd5de", lw=0.9, ls=":")
ax1.axvline(4000, color="#ccd5de", lw=0.9, ls=":")
ax1.text(212, 2.0, "203 nit\n图卡白", fontsize=7.6, color=H.GRAY, va="bottom")
ax1.text(1200, 2.0, "4000 nit", fontsize=7.6, color=H.GRAY, va="bottom")

ax1.plot([203, 203], [1, 61], color=H.BLUE, lw=0.8, ls=":")
ax1.plot([4000], [172], "o", ms=5, color=H.BLUE, zorder=5,
         markeredgecolor="white")
ax1.plot([4000], [230], "o", ms=5, color=H.ORANGE, zorder=5,
         markeredgecolor="white")
ax1.annotate("172", xy=(4000, 172), xytext=(1500, 118), fontsize=8,
             color=H.BLUE, arrowprops=dict(arrowstyle="-", color=H.BLUE, lw=0.9))
ax1.annotate("230", xy=(4000, 230), xytext=(1500, 330), fontsize=8,
             color=H.ORANGE, arrowprops=dict(arrowstyle="-", color=H.ORANGE, lw=0.9))

ax1.set_xlabel("场景亮度（nit）")
ax1.set_ylabel("屏幕上实际输出（nit）")
ax1.set_title("(a) 三种做法的亮度传递", fontsize=9.8, pad=8)
ax1.legend(loc="upper left", fontsize=7.6, bbox_to_anchor=(0.02, 0.98))
ax1.xaxis.set_major_formatter(FuncFormatter(
    lambda v, p: f"{v:g}" if v >= 1 else f"{v:g}"))

# ---------- 右：局部斜率 ----------
sl_once = np.gradient(np.log10(once), np.log10(L))
sl_twice = np.gradient(np.log10(twice), np.log10(L))
sl_dir = np.gradient(np.log10(direct), np.log10(L))

ax2.set_xscale("log")
ax2.set_xlim(1, 10000)
ax2.set_ylim(0, 1.22)
ax2.plot(L, sl_dir, color=H.GRAY, lw=1.8, ls="--", label="直通后硬裁")
ax2.plot(L, sl_once, color=H.BLUE, lw=2.2, label="单次映射")
ax2.plot(L, sl_twice, color=H.ORANGE, lw=2.2, label="两次映射")
ax2.axhline(1.0, color="#ccd5de", lw=0.9, ls=":")
ax2.text(1.2, 1.035, "斜率 1 表示比例保持", fontsize=7.6, color=H.GRAY)
ax2.set_xlabel("场景亮度（nit）")
ax2.set_ylabel("对数斜率 d log Lout / d log Lin")
ax2.set_title("(b) 高光段的对比保留", fontsize=9.8, pad=8)
ax2.legend(loc="lower left", fontsize=7.8)


fig.subplots_adjust(wspace=0.34)
H.save(fig, 8, "f4_hgig_divide")
