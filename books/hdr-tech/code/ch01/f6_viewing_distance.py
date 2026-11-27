# -*- coding: utf-8 -*-
"""图 1-6：显示分辨率、观看距离与对比敏感度的关系。

(a) 把屏幕的奈奎斯特频率换算成视角空间频率 cpd。设画面高度为 H、观看距离为 kH，
    则画面的张角为 2·arctan(1/2k)，垂直方向 N 行的奈奎斯特频率为 (N/2)/张角。
(b) 把 3H 距离下三种分辨率对应的空间频率画在 Barten CSF（100 cd/m²）上，
    1080p 的上限还落在敏感度尚可的一段，4K 已接近截止频率，8K 完全越界。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import FuncFormatter, NullFormatter
plt.rcParams["mathtext.fontset"] = "dejavusans"


def plain(ax, which="xy"):
    for a in which:
        ax_ = ax.xaxis if a == "x" else ax.yaxis
        ax_.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
        ax_.set_minor_formatter(NullFormatter())


def barten_csf(u, L, X0=2.0, Xmax=12.0, Nmax=15.0, k=3.0, T=0.1,
               eta=0.03, p=1.2274e6, phi0=3e-8, u0=7.0,
               sigma0=0.5, Cab=0.08):
    d = 5.0 - 3.0 * np.tanh(0.4 * np.log10(L / 40.0))
    E = L * np.pi * d ** 2 / 4.0
    sigma = np.sqrt(sigma0 ** 2 + (Cab * d) ** 2) / 60.0
    M_opt = np.exp(-2.0 * np.pi ** 2 * sigma ** 2 * u ** 2)
    spat = 1.0 / X0 ** 2 + 1.0 / Xmax ** 2 + u ** 2 / Nmax ** 2
    noise = 1.0 / (eta * p * E) + phi0 / (1.0 - np.exp(-(u / u0) ** 2))
    return M_opt / (k * np.sqrt(2.0 / T * spat * noise))


def nyquist(rows, k):
    ang = 2.0 * np.degrees(np.arctan(1.0 / (2.0 * k)))
    return (rows / 2.0) / ang


fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(8.8, 3.9), gridspec_kw={"width_ratios": [1.15, 1.0]})
fig.subplots_adjust(left=0.085, right=0.985, bottom=0.155, top=0.94, wspace=0.28)

k = np.linspace(0.8, 8.0, 400)
sets = [(1080, "1080p（1920×1080）", H.GRAY),
        (2160, "4K（3840×2160）", H.BLUE),
        (4320, "8K（7680×4320）", H.ORANGE)]
for rows, lab, c in sets:
    ax1.semilogy(k, nyquist(rows, k), color=c, lw=2.2, label=lab)

ax1.axhspan(60, 400, color=H.LGRAY, alpha=0.55, lw=0, zorder=0)
ax1.axhline(60, color=H.RED, lw=1.0, ls=(0, (4, 3)), zorder=2)
ax1.axhline(30, color=H.NAVY, lw=0.9, ls=(0, (2, 2)), zorder=2)
ax1.text(4.6, 32, "30 cpd", fontsize=7.9, color=H.NAVY,
         ha="left", va="bottom")

ax1.axvline(3.0, color=H.DARK, lw=0.8, ls=":", zorder=2)
ax1.text(3.12, 6.2, "3H", fontsize=8.4, color=H.DARK, ha="left", va="bottom")
for rows, lab, c in sets:
    ax1.plot([3.0], [nyquist(rows, 3.0)], "o", ms=6.0, color=c,
             mec="white", mew=1.0, zorder=5)

ax1.text(1.50, 300, "灰色区在 60 cpd 以上\n屏幕分辨力已超出人眼极限", fontsize=7.9,
         color=H.GRAY, ha="left", va="center")

ax1.set_xlim(0.8, 8.0)
ax1.set_ylim(5, 400)
ax1.set_xticks([1, 2, 3, 4, 5, 6, 7, 8])
ax1.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
ax1.yaxis.set_minor_formatter(NullFormatter())
ax1.set_xlabel("观看距离（以画面高度 H 为单位）")
ax1.set_ylabel("屏幕能呈现的空间频率（cpd）")
ax1.legend(loc="lower right", fontsize=8.0, handlelength=1.8,
           borderpad=0.45, labelspacing=0.35)
ax1.text(0.035, 0.06, "(a)", transform=ax1.transAxes, ha="left", va="bottom",
         fontsize=10, color=H.DARK)

# ---------- (b) ----------
u = np.logspace(np.log10(0.6), np.log10(200), 700)
ax2.loglog(u, barten_csf(u, 100.0), color=H.NAVY, lw=2.4)
marks = [(nyquist(1080, 3.0), "1080p  29", H.GRAY, 600),
         (nyquist(2160, 3.0), "4K  57", H.BLUE, 320),
         (nyquist(4320, 3.0), "8K  114", H.ORANGE, 600)]
for xv, lab, c, ly in marks:
    ax2.axvline(xv, color=c, lw=1.1, ls=(0, (3, 2)))
    yv = float(barten_csf(np.array([xv]), 100.0)[0])
    ax2.plot([xv], [yv], "o", ms=5.5, color=c, mec="white", mew=0.9, zorder=5)
    ax2.text(xv * (0.90 if xv < 40 else 1.10), ly, lab, fontsize=7.8, color=c,
             ha="right" if xv < 40 else "left", va="bottom")

ax2.text(0.66, 640, "CSF（100 cd/m$^2$）", fontsize=8.2, color=H.NAVY,
         ha="left", va="center")
ax2.text(0.72, 0.52, "1080p 的上限还能分辨出\nS 约 30 的条纹；4K 的上限\n已经贴住敏感度曲线的尾巴",
         fontsize=7.8, color=H.DARK, ha="left", va="bottom")

ax2.set_xlim(0.6, 300)
ax2.set_ylim(0.4, 1400)
ax2.set_xticks([1, 2, 5, 10, 20, 50, 100, 200])
plain(ax2, "x")
ax2.set_yticks([1, 10, 100, 1000])
ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
ax2.yaxis.set_minor_formatter(NullFormatter())
ax2.set_xlabel("空间频率（cpd）")
ax2.set_ylabel("对比敏感度  S = 1/m$_t$")
ax2.text(0.975, 0.035, "(b)", transform=ax2.transAxes, ha="right",
         va="bottom", fontsize=10, color=H.DARK)

H.save(fig, 1, "f6_viewing_distance")
