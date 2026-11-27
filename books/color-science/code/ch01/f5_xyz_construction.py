# -*- coding: utf-8 -*-
"""第 01 章 图 5：从 CIE RGB 到 XYZ 的线性变换，以及数值积分的采样误差。

(a) 700/546.1/435.8 nm 原色下的色匹配函数，r̄ 在 436–546 nm 为负。
(b) 变换后的 x̄ ȳ z̄，处处非负，ȳ 与 V(λ) 重合。
(c) x̄ 由三项线性组合而成：负的 r̄ 项被 ḡ 项抵消，所以合成的 x̄ 不为负。
    三项按 XYZ = M·RGB 的系数加权，和为 x̄（数值上与 x̄ 逐点相差 < 1e-12）。
(d) 用不同采样间隔对同一 SPD 做梯形积分得到的 Y 相对误差：
    窄带源（460 nm，FWHM 20 nm）与宽带源（6500 K 黑体）对比。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C
from scipy.interpolate import PchipInterpolator

plt = H.plt

FX = PchipInterpolator(C.LAM, C.XBAR)
FY = PchipInterpolator(C.LAM, C.YBAR)
FZ = PchipInterpolator(C.LAM, C.ZBAR)

M = np.array([[2.7689, 1.7517, 1.1302],
              [1.0000, 4.5907, 0.0601],
              [0.0000, 0.0565, 5.5943]])
MI = np.linalg.inv(M)

lam = np.linspace(380.0, 780.0, 4001)
XYZ = np.stack([FX(lam), FY(lam), FZ(lam)])
RGB = MI @ XYZ

fig = plt.figure(figsize=(7.2, 5.9))
gs = fig.add_gridspec(2, 2, hspace=0.46, wspace=0.34)

# ==================== (a) RGB 色匹配函数 ====================
ax = fig.add_subplot(gs[0, 0])
ax.axhline(0, color="#4a5666", lw=0.9)
for k, (col, lab) in enumerate(zip((H.RED, H.GREEN, H.BLUE),
                                   (r"$\bar{r}$", r"$\bar{g}$", r"$\bar{b}$"))):
    ax.plot(lam, RGB[k] / 0.35, color=col, lw=1.9, label=lab)
ax.fill_between(lam, 0, np.minimum(RGB[0] / 0.35, 0), color=H.RED, alpha=0.30,
                lw=0)
ax.annotate("负值区 436–546 nm", xy=(516, -0.075), xytext=(625, -0.225),
            fontsize=7.2, color=H.RED, ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                            connectionstyle="arc3,rad=0.18"))
ax.set_xlim(380, 780)
ax.set_ylim(-0.32, 1.10)
ax.set_xticks([400, 500, 600, 700])
ax.set_xlabel("波长 λ（nm）")
ax.set_ylabel("色匹配函数（未归一）")
ax.set_title("(a) CIE RGB 原色下", fontsize=9.5, pad=5)
ax.legend(loc="upper right", fontsize=8, ncol=3, frameon=False,
          handlelength=1.2, columnspacing=1.4, bbox_to_anchor=(1.0, 1.0))

# ==================== (b) XYZ 色匹配函数 ====================
ax2 = fig.add_subplot(gs[0, 1])
for k, (col, lab) in enumerate(zip((H.RED, H.GREEN, H.BLUE),
                                   (r"$\bar{x}$", r"$\bar{y}$", r"$\bar{z}$"))):
    ax2.plot(lam, XYZ[k], color=col, lw=1.9, label=lab)
ax2.axhline(0, color="#4a5666", lw=0.9)
ax2.text(690, 0.55, "处处非负", fontsize=7.6, color=H.DARK, ha="center",
         va="center")
ax2.annotate(r"$\bar{y}=V(\lambda)$", xy=(556, 1.0), xytext=(608, 1.30),
             fontsize=7.4, color=H.GREEN, ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=H.GREEN, lw=0.9,
                             connectionstyle="arc3,rad=0.15"))
ax2.set_xlim(380, 780)
ax2.set_ylim(-0.05, 1.95)
ax2.set_xticks([400, 500, 600, 700])
ax2.set_xlabel("波长 λ（nm）")
ax2.set_ylabel("色匹配函数（未归一）")
ax2.set_title("(b) 变换后 XYZ", fontsize=9.5, pad=5)
ax2.legend(loc="upper right", fontsize=8, ncol=3, frameon=False,
           handlelength=1.2, columnspacing=1.4, bbox_to_anchor=(1.0, 1.0))

# ==================== (c) x̄ 的三项分解 ====================
ax3 = fig.add_subplot(gs[1, 0])
terms = M[0][:, None] * RGB
ax3.axhline(0, color="#4a5666", lw=0.9)
ax3.plot(lam, terms[0], color=H.RED, lw=1.5, ls=(0, (4, 2)),
         label=r"$2.7689\,\bar{r}$")
ax3.plot(lam, terms[1], color=H.GREEN, lw=1.5, ls=(0, (4, 2)),
         label=r"$1.7517\,\bar{g}$")
ax3.plot(lam, terms[2], color=H.BLUE, lw=1.5, ls=(0, (4, 2)),
         label=r"$1.1302\,\bar{b}$")
ax3.plot(lam, XYZ[0], color=H.DARK, lw=2.3, label=r"$\bar{x}$（三项之和）")
ax3.fill_between(lam, 0, np.minimum(terms[0], 0), color=H.RED, alpha=0.25,
                 lw=0)
ax3.annotate("$\\bar r$ 项为负", xy=(497, -0.02), xytext=(425, -0.24),
             fontsize=7.2, color=H.RED, ha="center", va="center",
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                             connectionstyle="arc3,rad=-0.15"))
ax3.text(690, 0.72, "$\\bar g$ 项在绿区补上\n缺口，和不为负", fontsize=7.0,
         color="#2c5d3f", ha="center", va="center")
ax3.set_xlim(380, 780)
ax3.set_ylim(-0.35, 1.15)
ax3.set_xticks([400, 500, 600, 700])
ax3.set_xlabel("波长 λ（nm）")
ax3.set_ylabel("对 $\\bar{x}$ 的贡献")
ax3.set_title("(c) $\\bar{x}$ 按三项加权组合", fontsize=9.5, pad=5)
ax3.legend(loc="upper left", fontsize=7.0, frameon=False, handlelength=1.4,
           labelspacing=0.2)

# ==================== (d) 采样间隔与积分误差 ====================
ax4 = fig.add_subplot(gs[1, 1])
lam_ref = np.linspace(380.0, 780.0, 8001)
C2 = 1.4388e-2


def planck(T, lam_nm):
    l = lam_nm * 1e-9
    return 1.0 / (l ** 5 * (np.exp(C2 / (l * T)) - 1.0))


def gauss(cen, fwhm, l):
    s = fwhm / 2.3548
    return np.exp(-0.5 * ((l - cen) / s) ** 2)


def y_of(spd, l):
    return np.trapezoid(spd * FY(l), l)


REF_NARROW = y_of(gauss(460.0, 20.0, lam_ref), lam_ref)
REF_WIDE = y_of(planck(6500.0, lam_ref), lam_ref)

steps = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0])
err_n, err_w = [], []
for s in steps:
    l = np.arange(380.0, 780.0 + 1e-9, s)
    if l[-1] < 780.0:
        l = np.append(l, 780.0)
    err_n.append(abs(y_of(gauss(460.0, 20.0, l), l) / REF_NARROW - 1.0) * 100)
    err_w.append(abs(y_of(planck(6500.0, l), l) / REF_WIDE - 1.0) * 100)

ax4.semilogy(steps, err_n, "o-", color=H.RED, lw=1.9, ms=4.5,
             label="窄带源 460 nm，FWHM 20 nm")
ax4.semilogy(steps, err_w, "s-", color=H.NAVY, lw=1.9, ms=4.5,
             label="宽带源 6500 K 黑体")
ax4.axvline(5, color=H.GRAY, lw=0.9, ls=":")
ax4.axvline(10, color=H.GRAY, lw=0.9, ls=":")
ax4.text(5.4, 30, "5 nm", fontsize=7.0, color=H.GRAY, ha="left", va="top")
ax4.text(10.4, 30, "10 nm", fontsize=7.0, color=H.GRAY, ha="left", va="top")
ax4.set_xlim(0, 21)
ax4.set_ylim(1e-3, 60)
ax4.set_xticks([0, 5, 10, 15, 20])
ax4.set_xlabel("采样间隔（nm）")
ax4.set_ylabel("$Y$ 的相对误差（%）")
ax4.set_title("(d) 梯形积分的采样误差", fontsize=9.5, pad=5)
ax4.legend(loc="upper left", fontsize=7.0, frameon=True, handlelength=1.6,
           labelspacing=0.2, bbox_to_anchor=(0.02, 0.99))
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
ax4.yaxis.set_major_locator(FixedLocator([0.001, 0.01, 0.1, 1.0, 10.0]))
ax4.yaxis.set_minor_locator(NullLocator())
ax4.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}%"))

H.save(fig, 1, "f5_xyz_construction")

print("max |xbar - sum(terms)| =", np.abs(XYZ[0] - terms.sum(0)).max())
for s, en, ew in zip(steps, err_n, err_w):
    print(f"step {s:4.0f} nm  narrow {en:8.4f}%  wide {ew:8.4f}%")

# 仪器带宽（三角狭缝函数）造成的误差，采样固定 1 nm
def tri_kernel(fwhm):
    k = np.arange(-int(3 * fwhm), int(3 * fwhm) + 1, 1.0)
    return np.maximum(0.0, 1 - np.abs(k) / fwhm)


for b in (5.0, 10.0, 20.0):
    kk = tri_kernel(b)
    kk = kk / kk.sum()
    sm = np.convolve(gauss(460.0, 20.0, lam_ref), kk, mode="same")
    print(f"bandwidth {b:.0f} nm: Y error {abs(y_of(sm, lam_ref) / REF_NARROW - 1) * 100:.3f}%")
