# -*- coding: utf-8 -*-
"""图 1-7：位深与传递函数共同决定的亮度台阶。

纵轴是相邻两个码值之间的相对亮度差 (L(n+1)-L(n))/L(n)。对 gamma 曲线，
这个比值只取决于码值序号，与白场无关；对 PQ 曲线，比值随亮度下降而放大。
水平虚线是 Weber 分数的常用下限 1%，越过这条线，台阶在大面积缓变区域
就有被看成色带的可能。
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


def gamma_steps(bits, g=2.2, white=100.0):
    n = np.arange(1, 2 ** bits)
    L = white * (n / (2 ** bits - 1)) ** g
    return L[:-1], (np.diff(L) / L[:-1]) * 100.0


def pq_steps(bits):
    n = np.arange(2 ** bits)
    L = H.pq_eotf(n / (2 ** bits - 1))
    L[0] = L[1] * 1e-3
    return L[:-1], (np.diff(L) / L[:-1]) * 100.0


fig, ax = plt.subplots(figsize=(7.6, 4.3))
fig.subplots_adjust(left=0.098, right=0.975, bottom=0.145, top=0.955)

ax.axhspan(1.0, 60, color=H.LGRAY, alpha=0.5, lw=0, zorder=0)
ax.axhline(1.0, color=H.RED, lw=1.0, ls=(0, (4, 3)), zorder=2)
ax.text(2.7e-4, 1.07, "Weber 分数 1%", fontsize=8.0, color=H.RED,
        ha="left", va="bottom")
ax.text(9500, 1.55, "台阶可能被看见的一侧", fontsize=8.0, color=H.GRAY,
        ha="right", va="bottom")

L, s = gamma_steps(8)
m = (L > 2.5e-4) & (L < 1.1e4)
ax.loglog(L[m], s[m], color=H.GRAY, lw=2.0, ls=(0, (5, 2)),
          label="8 bit，gamma 2.2")

for bits, c, lab in [(10, H.BLUE, "10 bit，PQ"), (12, H.NAVY, "12 bit，PQ")]:
    L, s = pq_steps(bits)
    m = (L > 2.5e-4) & (L < 1.1e4)
    ax.loglog(L[m], s[m], color=c, lw=2.3, label=lab)

L10, s10 = pq_steps(10)
i1 = np.argmin(np.abs(L10 - 0.01))
ax.plot([L10[i1]], [s10[i1]], "o", ms=5.5, color=H.BLUE, mec="white", mew=0.9,
        zorder=5)
ax.annotate("0.01 cd/m$^2$ 处为 9.3%\n暗部色带由此而来",
            xy=(L10[i1], s10[i1] + 0.4), xytext=(3.2e-4, 30), fontsize=8.0,
            color=H.BLUE, va="top",
            arrowprops=dict(arrowstyle="->", color=H.BLUE, lw=0.9,
                            shrinkA=2, shrinkB=5))

ax.text(30, 0.155, "12 bit 在 1 cd/m$^2$ 以上小于 0.5%", fontsize=8.0,
        color=H.NAVY, ha="left", va="center")

ax.set_xlim(2.5e-4, 1.1e4)
ax.set_ylim(0.08, 40)
ax.set_xticks([1e-3, 1e-2, 1e-1, 1, 10, 100, 1000, 10000])
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: dec(v) if v < 1
                                           else f"{v:g}".replace("e+", "e")))
ax.xaxis.set_minor_formatter(NullFormatter())
ax.set_yticks([0.1, 0.3, 1, 3, 10, 30])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
ax.yaxis.set_minor_formatter(NullFormatter())
ax.set_xlabel("该码值对应的亮度（cd/m$^2$，gamma 曲线按白场 100 cd/m$^2$ 折算）")
ax.set_ylabel("相邻码值的相对亮度差（%）")
ax.legend(loc="upper right", fontsize=8.2, handlelength=2.6,
          borderpad=0.5, labelspacing=0.4)

H.save(fig, 1, "f7_step_visibility")
