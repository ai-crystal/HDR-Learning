# -*- coding: utf-8 -*-
"""第 04 章 图 3：CIE 1931 色匹配函数 x̄ ȳ z̄（并对照真实 RGB 响应）。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import hdrfig as H
import cie1931 as C

plt = H.plt

lam = C.LAM
X, Y, Z = C.XBAR, C.YBAR, C.ZBAR

# 真实 CIE RGB 色匹配函数（由 XYZ 反变换得到，会出现负值）
_RGB2XYZ = np.array([[2.7689, 1.7517, 1.1302],
                     [1.0000, 4.5907, 0.0601],
                     [0.0000, 0.0565, 5.5943]])
M = np.linalg.inv(_RGB2XYZ)   # XYZ -> RGB
Rr = M[0, 0] * X + M[0, 1] * Y + M[0, 2] * Z
Gg = M[1, 0] * X + M[1, 1] * Y + M[1, 2] * Z
Bb = M[2, 0] * X + M[2, 1] * Y + M[2, 2] * Z

fig = plt.figure(figsize=(7.2, 4.4))
gs = fig.add_gridspec(1, 2, width_ratios=[2.15, 1.15], wspace=0.28)

# ================= 左：CIE 1931 XYZ 色匹配函数 =================
ax = fig.add_subplot(gs[0])
ax.set_title("CIE 1931 色匹配函数（永远非负）", pad=8)

ax.fill_between(lam, 0, X, color=H.RED, alpha=0.10)
ax.fill_between(lam, 0, Z, color=H.BLUE, alpha=0.10)
ax.plot(lam, X, color=H.RED, lw=2.3, label=r"$\bar{x}(\lambda)$")
ax.plot(lam, Y, color=H.GREEN, lw=2.3, label=r"$\bar{y}(\lambda)$（= V(λ)）")
ax.plot(lam, Z, color=H.BLUE, lw=2.3, label=r"$\bar{z}(\lambda)$")
ax.axhline(0, color="#4a5666", lw=0.9)

for curve, tag, col, xyt in ((Z, r"$\bar{z}$ 峰 445 nm = 1.78", H.BLUE, (503, 1.84)),
                             (Y, r"$\bar{y}$ 峰 555 nm = 1.00", H.GREEN, (497, 1.26)),
                             (X, r"$\bar{x}$ 峰 600 nm = 1.06", H.RED, (662, 1.58))):
    wl, h = C.peak_wavelength(curve)
    ax.plot([wl], [h], "o", ms=6, color=col, zorder=5)
    ax.annotate(tag, xy=(wl, h), xytext=xyt, fontsize=8.3, color=col,
                fontweight="bold", ha="center", va="center",
                arrowprops=dict(arrowstyle="->", color=col, lw=1.1,
                                connectionstyle="arc3,rad=-0.15"),
                bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=1.2))

ax.text(700, 0.62, "X + Y + Z\n= 三刺激值", fontsize=8.4, color=H.NAVY,
        ha="center", va="center", fontweight="bold",
        bbox=dict(facecolor="#f2f6fa", edgecolor=H.LGRAY, boxstyle="round,pad=0.35"))
ax.set_xlim(380, 780)
ax.set_ylim(-0.06, 2.25)
ax.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
ax.set_xlabel("波长 λ（nm）")
ax.set_ylabel("色匹配函数值")
ax.legend(loc="upper center", fontsize=8.2, ncol=3, columnspacing=1.1,
          handlelength=1.3)

# ================= 右：真实 RGB 响应会出现负值 =================
ax2 = fig.add_subplot(gs[1])
ax2.set_title("真实的红绿蓝响应：有负值", pad=8)
ax2.axhspan(-0.20, 0, color=H.RED, alpha=0.07)
ax2.axhline(0, color="#4a5666", lw=1.1)
ax2.plot(lam, Rr, color=H.RED, lw=2.0, label=r"$\bar{r}(\lambda)$")
ax2.plot(lam, Gg, color=H.GREEN, lw=2.0, label=r"$\bar{g}(\lambda)$")
ax2.plot(lam, Bb, color=H.BLUE, lw=2.0, label=r"$\bar{b}(\lambda)$")
ax2.set_xlim(380, 780)
ax2.set_ylim(-0.20, 0.52)
ax2.set_xticks([400, 500, 600, 700])
ax2.set_xlabel("波长 λ（nm）")
ax2.set_ylabel("响应值")
ax2.legend(fontsize=8, loc="upper right", ncol=3, columnspacing=0.8,
           handlelength=1.0)
ax2.annotate("红基色响应在 450–560 nm\n区间为负 → “减光”", xy=(500, -0.081),
             xytext=(560, -0.155), fontsize=7.6, color=H.RED, ha="center",
             va="center", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.1),
             bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=1.2))

H.save(fig, 4, "f3_cmf")
