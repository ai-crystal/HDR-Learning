# -*- coding: utf-8 -*-
"""第 01 章 图 4：CIE 1931 2° 标准观察者色匹配函数（真实数据，5 nm 间隔）。

数据来源：CIE 1931 2° standard observer，见同目录 cie1931.py。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C

plt = H.plt

lam = C.LAM
X, Y, Z = C.XBAR, C.YBAR, C.ZBAR

fig = plt.figure(figsize=(7.2, 4.5))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 0.085], hspace=0.10)
ax = fig.add_subplot(gs[0])
axb = fig.add_subplot(gs[1])

# ---------------- 色匹配函数 ----------------
ax.fill_between(lam, 0, X, color=H.RED, alpha=0.07)
ax.fill_between(lam, 0, Z, color=H.BLUE, alpha=0.07)
ax.plot(lam, X, color=H.RED, lw=2.3, label=r"$\bar{x}(\lambda)$")
ax.plot(lam, Y, color=H.GREEN, lw=2.3, label=r"$\bar{y}(\lambda)$")
ax.plot(lam, Z, color=H.BLUE, lw=2.3, label=r"$\bar{z}(\lambda)$")

# 峰值标记
peak_annot = [
    (Z, H.BLUE, (560, 1.95), r"$\bar{z}$ 峰 445 nm，1.782"),
    (Y, H.GREEN, (614, 1.40), r"$\bar{y}$ 峰 555 nm，1.000"),
    (X, H.RED, (668, 0.90), r"$\bar{x}$ 峰 600 nm，1.062"),
]
for curve, col, txt, tag in peak_annot:
    wl, h = C.peak_wavelength(curve)
    ax.plot([wl], [h], "o", ms=5.5, color=col, zorder=6)
    ax.annotate(tag, xy=(wl, h), xytext=txt, fontsize=8.2, color=col,
                fontweight="bold", ha="center", va="center", zorder=7,
                arrowprops=dict(arrowstyle="->", color=col, lw=1.0,
                                shrinkB=4, connectionstyle="arc3,rad=0.12"),
                bbox=dict(facecolor="white", alpha=0.9, edgecolor="none", pad=1.4))

ax.text(700, 0.30, "三条曲线处处非负\n$X=\\int L_\\lambda\\bar{x}\\,d\\lambda$ 等",
        fontsize=7.8, color=H.DARK, ha="center", va="center", zorder=7,
        bbox=dict(facecolor="#f3f6fa", edgecolor=H.LGRAY,
                  boxstyle="round,pad=0.35", lw=0.8))

ax.axhline(0, color="#4a5666", lw=0.9)
ax.set_xlim(380, 780)
ax.set_ylim(-0.05, 2.12)
ax.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
ax.tick_params(labelbottom=False)
ax.set_ylabel("色匹配函数值（无量纲）")
ax.set_xlabel("")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.005), ncol=3,
          fontsize=9, frameon=False, columnspacing=2.4, handlelength=1.6)

# ---------------- 底部光谱色带（同一横轴，帮助读波长） ----------------
wl_dense = np.linspace(380, 780, 1200)
rgb = C.wavelength_to_srgb01(wl_dense, normalized=True)
strip = rgb.reshape(1, -1, 3)
axb.imshow(strip, extent=[380, 780, 0, 1], origin="lower", aspect="auto")
axb.set_xlim(380, 780)
axb.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
axb.set_yticks([])
axb.grid(False)
axb.set_xlabel("波长 λ（nm）")
for s in axb.spines.values():
    s.set_color("#9aa7b4")

H.save(fig, 1, "f4_cmf_1931")
