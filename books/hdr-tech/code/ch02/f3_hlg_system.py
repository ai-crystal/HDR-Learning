# -*- coding: utf-8 -*-
"""图 2-3：BT.2100 HLG 的 OETF 与系统 gamma 端到端特性。

左：HLG OETF（场景线性 -> 信号），标出 1/12 处的拐点；
右：信号 -> 显示亮度，按 OOTF  F_D = L_W · Y_S^(γ-1) · E 计算，γ = 1.2 + 0.42 lg(L_W/1000)，
    分别取 L_W = 400 / 1000 / 2000 cd/m²，并与 BT.1886（SDR，白场 100 cd/m²）对照。
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


v = np.linspace(0, 1, 1000)
E = H.hlg_eotf(v)

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(8.8, 4.3), gridspec_kw={"width_ratios": [1.0, 1.05]})
fig.subplots_adjust(left=0.09, right=0.975, bottom=0.145, top=0.95, wspace=0.32)

# ---------- (a) OETF ----------
e = np.linspace(0, 1, 1000)
e_sq = np.linspace(0, 1 / 12, 200)
e_lg = np.linspace(1 / 12, 1, 600)
ax1.plot(e_sq, np.sqrt(3.0 * e_sq), color=H.ORANGE, lw=3.0, zorder=5,
         label="平方根段 $E'=\sqrt{3E}$")
ax1.plot(e_lg, H.hlg_oetf(e_lg), color=H.NAVY, lw=2.2, zorder=4,
         label="对数段 $E'=a\ln(12E-b)+c$")
ax1.legend(loc="lower right", fontsize=8.0, handlelength=1.8,
           borderpad=0.45, labelspacing=0.4, bbox_to_anchor=(1.0, 0.10))
ax1.axvline(1 / 12, color=H.GRAY, lw=0.9, ls=(0, (4, 3)), zorder=1)
ax1.axhline(0.5, color=H.GRAY, lw=0.9, ls=(0, (4, 3)), zorder=1)
ax1.plot([1 / 12], [0.5], "o", ms=6, color=H.RED, mec="white", mew=1.0, zorder=6)
ax1.annotate("拐点 $E=1/12$，$E'=0.5$",
             xy=(1 / 12, 0.5), xytext=(0.19, 0.63),
             fontsize=8.4, color=H.DARK,
             arrowprops=dict(arrowstyle="->", color=H.DARK, lw=0.9,
                             shrinkA=3, shrinkB=4))
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1.02)
ax1.set_xlabel("场景线性光 $E$（相对漫反射白）")
ax1.set_ylabel("HLG 信号 $E'$")
ax1.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax1.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax1.text(0.97, 0.06, "(a)", transform=ax1.transAxes,
         ha="right", va="bottom", fontsize=10, color=H.DARK)

# ---------- (b) 端到端 ----------
for Lw, c in [(400, H.TEAL), (1000, H.ORANGE), (2000, H.RED)]:
    g = 1.2 + 0.42 * np.log10(Lw / 1000.0)
    Ld = Lw * E ** g
    ax2.semilogy(v, np.maximum(Ld, 1e-3), color=c, lw=2.2,
                 label=f"HLG，$L_W$={Lw} cd/m$^2$（γ={g:.2f}）")
ax2.semilogy(v, np.maximum(100.0 * v ** 2.4, 1e-3), color=H.GRAY, lw=1.6,
             ls=(0, (5, 2)), label="BT.1886（SDR，白场 100）")

ax2.axhline(203, color=H.NAVY, lw=0.9, ls=(0, (4, 3)), zorder=1)
ax2.axvline(0.75, color=H.NAVY, lw=0.9, ls=(0, (4, 3)), zorder=1)
ax2.plot([0.75], [203.2], "o", ms=6, color=H.NAVY, mec="white", mew=1.0, zorder=6)
ax2.annotate("75% 信号 → 203 cd/m$^2$", xy=(0.748, 190), xytext=(0.42, 0.055),
             fontsize=8.4, color=H.NAVY,
             arrowprops=dict(arrowstyle="->", color=H.NAVY, lw=0.9,
                             shrinkA=3, shrinkB=5))
ax2.set_xlim(0, 1)
ax2.set_ylim(0.03, 6e3)
ax2.set_xlabel("HLG 信号 $E'$")
ax2.set_ylabel("显示亮度（cd/m$^2$）")
ax2.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax2.set_yticks([0.1, 1, 10, 100, 1000])
ax2.yaxis.set_major_formatter(FuncFormatter(lambda t, p: f"{t:g}"))
ax2.yaxis.set_minor_formatter(NullFormatter())
ax2.legend(loc="upper left", fontsize=7.8, handlelength=1.7,
           borderpad=0.45, labelspacing=0.35)
ax2.text(0.04, 0.055, "(b)", transform=ax2.transAxes,
         ha="left", va="bottom", fontsize=10, color=H.DARK)

H.save(fig, 2, "f3_hlg_system")
