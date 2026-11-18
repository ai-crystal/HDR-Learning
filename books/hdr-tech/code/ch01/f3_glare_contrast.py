# -*- coding: utf-8 -*-
"""图 1-3：眼内杂散光对可用对比度的限制（模型计算）。

左：设高光亮度 Lw、原生黑位 Lb = Lw/CR_native，杂散光按 s·Lw 抬升整个视野
（Stiles–Holladay 遮蔽光的一阶近似），有效对比度
    CR_eff = (1 + s) / (1/CR_native + s)
右：取 Lw = 1000 cd/m²、CR_native = 10^6、s = 1% 的具体算例。
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


s = np.logspace(np.log10(5e-4), np.log10(0.2), 400)
natives = [10.0 ** 3, 10.0 ** 4, 10.0 ** 5, 10.0 ** 6]
colors = [H.GRAY, H.TEAL, H.BLUE, H.NAVY]

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(8.6, 4.2), gridspec_kw={"width_ratios": [1.35, 1.0]})
fig.subplots_adjust(left=0.085, right=0.975, bottom=0.16, top=0.95, wspace=0.42)

ax1.axvspan(0.03, 0.2, color=H.LGRAY, alpha=0.55, zorder=0, lw=0)
for cr, c in zip(natives, colors):
    cr_eff = (1.0 + s) / (1.0 / cr + s)
    ax1.loglog(s, cr_eff, color=c, lw=2.1,
               label=r"原生对比度 $10^{%d}$:1" % int(round(np.log10(cr))))

ax1.set_xlim(5e-4, 0.2)
ax1.set_ylim(5, 2e6)
ax1.set_xlabel("杂散光占比 s（相对高光亮度）")
ax1.set_ylabel("有效对比度  $CR_{eff}$")
ax1.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
ax1.xaxis.set_minor_formatter(NullFormatter())
ax1.yaxis.set_major_formatter(FuncFormatter(lambda v, p: dec(v)))
ax1.yaxis.set_minor_formatter(NullFormatter())
ax1.set_xticks([0.001, 0.003, 0.01, 0.03, 0.1])

ax1.axvline(0.01, color=H.RED, lw=0.9, ls=(0, (3, 3)), zorder=1)
ax1.annotate("s ≈ 1%，有效对比度\n落到 100:1 量级",
             xy=(0.01, 101), xytext=(0.0012, 7.5),
             fontsize=8.4, color=H.DARK,
             arrowprops=dict(arrowstyle="->", color=H.DARK, lw=0.9,
                             shrinkA=2, shrinkB=3))
ax1.text(0.037, 8e5, "强眩光区", fontsize=8.4, color=H.GRAY,
         ha="left", va="center")
ax1.legend(loc="upper left", fontsize=8.0, handlelength=1.5,
           borderpad=0.45, labelspacing=0.35, bbox_to_anchor=(0.0, 1.0))
ax1.text(0.97, 0.94, "(a)", transform=ax1.transAxes,
         ha="right", va="top", fontsize=10, color=H.DARK)

# ---- (b) 具体算例：1000 cd/m² 高光、原生 10^6、1% 杂散光 ----
Lw, cr_native, sv = 1000.0, 1e6, 0.01
Lb = Lw / cr_native
floor = sv * Lw
items = [("器件原生黑位", Lb, H.GRAY),
         ("杂散光抬升后的黑位", floor, H.RED),
         ("HDR 参考白", 203.0, H.TEAL),
         ("场景高光", Lw, H.ORANGE)]
for i, (name, val, c) in enumerate(items):
    ax2.hlines(i, 1e-3, val, color=c, lw=1.2, ls=":", zorder=2)
    ax2.plot([val], [i], "o", ms=8, color=c, mec="white", mew=1.0, zorder=4)
    ax2.text(val * 1.7, i, f"{val:g}", va="center", ha="left",
             fontsize=8.6, color=c)
ax2.set_xscale("log")
ax2.set_xlim(1e-3, 3e5)
ax2.set_ylim(-0.7, 3.7)
ax2.set_yticks(range(len(items)))
ax2.set_yticklabels([it[0] for it in items])
ax2.tick_params(axis="y", length=0, pad=4)
ax2.set_xlabel("亮度（cd/m$^2$）")
ax2.xaxis.set_major_formatter(FuncFormatter(lambda v, p: dec(v) if v >= 1e4
                                            else f"{v:g}"))
ax2.xaxis.set_minor_formatter(NullFormatter())
ax2.set_xticks([1e-3, 1e-1, 10, 1e3])
ax2.annotate("", xy=(10, 0.94), xytext=(10, 0.06),
             arrowprops=dict(arrowstyle="<->", color=H.DARK, lw=1.0))
ax2.text(0.0085, 0.5, "遮蔽光吃掉\n4 个数量级的暗部", fontsize=8.2,
         color=H.DARK, ha="right", va="center")
ax2.text(0.97, 0.94, "(b)", transform=ax2.transAxes,
         ha="right", va="top", fontsize=10, color=H.DARK)

H.save(fig, 1, "f3_glare_contrast")
