# -*- coding: utf-8 -*-
"""图 2-1：SMPTE ST 2084 (PQ) 的 EOTF 与 10/12 bit 量化台阶。

左：PQ EOTF（码值 -> 绝对亮度，纵轴对数），标注 BT.2408 的参考白与常见峰值；
右：相邻码值之间的相对亮度差 = L(n+1)/L(n) - 1，按公式计算，并与 Weber 阈值 1% 比较。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import FuncFormatter, NullFormatter
plt.rcParams["mathtext.fontset"] = "dejavusans"


def dec(v):
    s = f"{v:.0e}"
    return s.replace("e+0", "e").replace("e+", "e").replace("e-0", "e-")


code = np.linspace(0, 1, 2000)
nit = H.pq_eotf(code)

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(8.8, 4.3), gridspec_kw={"width_ratios": [1.0, 1.05]})
fig.subplots_adjust(left=0.09, right=0.975, bottom=0.145, top=0.95, wspace=0.32)

# ---------- (a) EOTF ----------
ax1.semilogy(code, np.maximum(nit, 1e-6), color=H.NAVY, lw=2.4, zorder=4)
for ref, lab, c, side in [(100, "100", H.GRAY, "right"),
                          (203, "203　BT.2408 参考白", H.TEAL, "left"),
                          (1000, "1000", H.ORANGE, "left"),
                          (4000, "4000", H.RED, "left")]:
    ax1.axhline(ref, color=c, lw=0.9, ls=(0, (4, 3)), zorder=1)
    bb = dict(facecolor="white", edgecolor="none", pad=1.0)
    if side == "left":
        ax1.text(0.015, ref * 1.10, lab, fontsize=8.0, color=c, va="bottom",
                 bbox=bb, zorder=6)
    else:
        ax1.text(0.985, ref * 1.10, lab, fontsize=8.0, color=c,
                 va="bottom", ha="right", bbox=bb, zorder=6)
    c01 = float(H.pq_oetf(ref)) if ref > 0 else 0.0
    ax1.plot([c01], [ref], "o", ms=5, color=c, mec="white", mew=0.8, zorder=6)

ax1.set_xlim(0, 1)
ax1.set_ylim(1e-4, 3e4)
ax1.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax1.set_xticklabels(["0", "0.25", "0.50", "0.75", "1.0"])
ax1.set_yticks([1e-4, 1e-2, 1, 1e2, 1e4])
ax1.yaxis.set_major_formatter(FuncFormatter(lambda v, p: dec(v) if v < 0.01 else f"{v:g}"))
ax1.yaxis.set_minor_formatter(NullFormatter())
ax1.set_xlabel("PQ 码值（归一化，$E' = \\mathrm{code}/1023$）")
ax1.set_ylabel("显示亮度（cd/m$^2$）")
ax1.annotate("0.58 → 203 cd/m$^2$", xy=(0.5807, 203), xytext=(0.30, 3.2),
             fontsize=8.4, color=H.TEAL,
             arrowprops=dict(arrowstyle="->", color=H.TEAL, lw=0.9,
                             shrinkA=2, shrinkB=4))
ax1.text(0.97, 0.06, "(a)", transform=ax1.transAxes,
         ha="right", va="bottom", fontsize=10, color=H.DARK)

# ---------- (b) 量化台阶 ----------
for bits, c, lw in [(10, H.RED, 2.2), (12, H.BLUE, 2.2)]:
    n = 2 ** bits - 1
    L = H.pq_eotf(np.arange(1, n + 1) / n)
    step = L[1:] / np.maximum(L[:-1], 1e-12) - 1.0
    ax2.loglog(L[1:], step * 100, color=c, lw=lw, label=f"{bits} bit")
ax2.axhline(1.0, color=H.GRAY, lw=1.0, ls=(0, (4, 3)))
ax2.text(1.3e-4, 1.25, "Weber 阈值 1%", fontsize=8.2, color=H.GRAY)
ax2.set_xlim(1e-4, 1.2e4)
ax2.set_ylim(0.03, 400)
ax2.set_xlabel("该码值对应的亮度（cd/m$^2$）")
ax2.set_ylabel("相邻码值的相对亮度差（%）")
ax2.set_xticks([1e-4, 1e-2, 1, 1e2, 1e4])
ax2.set_xticklabels(["1e-4", "1e-2", "1", "100", "1e4"])
ax2.xaxis.set_minor_formatter(NullFormatter())
ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
ax2.yaxis.set_minor_formatter(NullFormatter())
ax2.legend(loc="upper right", fontsize=8.6, handlelength=1.6)
ax2.annotate("100 cd/m$^2$ 附近台阶约 1%，\n正压在可见性边缘",
             xy=(100, 1.02), xytext=(0.02, 0.12),
             fontsize=8.2, color=H.DARK,
             arrowprops=dict(arrowstyle="->", color=H.DARK, lw=0.9,
                             shrinkA=2, shrinkB=4))
ax2.text(0.97, 0.94, "(b)", transform=ax2.transAxes,
         ha="right", va="top", fontsize=10, color=H.DARK)

H.save(fig, 2, "f1_pq_curve")
