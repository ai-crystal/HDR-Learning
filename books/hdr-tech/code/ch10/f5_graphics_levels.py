# -*- coding: utf-8 -*-
"""第 10 章 图 5：图形与字幕的三种亮度策略。

(a) 图形亮度与所在场景平均亮度之比。三条线对应：固定 203 cd/m2（BT.2408 的
    图形白）、固定 100 cd/m2（沿用 SDR 观感）、按场景比例跟随（比值恒为 2.03，
    即 SDR 里 235 码值对 100 cd/m2 场景白的关系）。浅色带是比值 1 至 4 的
    常用可接受区。
(b) 一个体育画面的亮度直方图（对数正态合成，仅作示意），标出三条策略给出的
    图形亮度落在分布里的什么位置。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(9.0, 4.2), gridspec_kw={"width_ratios": [1.08, 1.0]})
fig.subplots_adjust(left=0.085, right=0.975, bottom=0.145, top=0.955, wspace=0.28)

# ---------------- (a) ----------------
Lsc = np.logspace(np.log10(8), np.log10(600), 500)
ax1.axhspan(1.0, 4.0, color=H.GREEN, alpha=0.10, zorder=0)
ax1.text(9.0, 4.3, "比值 1 到 4 的常用区", fontsize=8.0, color=H.GREEN, va="bottom")

ax1.loglog(Lsc, 203.0 / Lsc, color=H.NAVY, lw=2.4, label="固定 203")
ax1.loglog(Lsc, 100.0 / Lsc, color=H.ORANGE, lw=2.0, label="固定 100")
ax1.axhline(2.03, color=H.TEAL, lw=2.2, ls=(0, (5, 2)), label="按场景跟随")

ax1.plot([203.0], [1.0], "o", ms=5.5, color=H.NAVY, mec="white", mew=1.0, zorder=6)
ax1.plot([49.0], [2.03], "o", ms=5.5, color=H.TEAL, mec="white", mew=1.0, zorder=6)

ax1.annotate("场景平均亮度到 203 时\n图形与画面等亮", xy=(203, 1.0), xytext=(575, 1.60),
             fontsize=7.8, color=H.NAVY,
             ha="right", va="center",
             arrowprops=dict(arrowstyle="->", color=H.NAVY, lw=0.8,
                             connectionstyle="arc3,rad=0.2"))
ax1.text(11.5, 2.45, "两条线在 49 处相交", fontsize=7.8, color=H.TEAL)

ax1.set_xlim(8, 600)
ax1.set_ylim(0.15, 12)
ax1.set_xlabel("场景平均亮度（cd/m$^2$）")
ax1.set_ylabel("图形亮度 / 场景亮度")
ax1.set_xticks([10, 30, 100, 300])
ax1.set_xticklabels(["10", "30", "100", "300"])
ax1.set_yticks([0.2, 0.5, 1, 2, 5, 10])
ax1.set_yticklabels(["0.2", "0.5", "1", "2", "5", "10"])
ax1.minorticks_off()
ax1.legend(loc="upper right", fontsize=8.2)
ax1.set_title("(a) 图形与画面的相对亮度", fontsize=10.5, pad=6)

# ---------------- (b) 直方图（示意） ----------------
rng = np.random.default_rng(7)
samples = rng.lognormal(mean=np.log(85.0), sigma=0.62, size=40000)
samples = samples[(samples > 1) & (samples < 1200)]
bins = np.logspace(0, 3.1, 120)
w, edges = np.histogram(samples, bins=bins, density=True)
centers = 0.5 * (edges[1:] + edges[:-1])
ax2.fill_between(centers, 0, w, color=H.LGRAY, alpha=0.85, zorder=2, lw=0)
ax2.plot(centers, w, color=H.GRAY, lw=1.2, zorder=3)

for x, c, lab, ls in [(100, H.ORANGE, "固定 100", "-"),
                      (203, H.NAVY, "固定 203", "-"),
                      (172, H.TEAL, "跟随（场景 85）", (0, (5, 2)))]:
    ax2.axvline(x, color=c, lw=1.8, zorder=4, ls=ls, label=lab)

ax2.set_xscale("log")
ax2.set_xlim(1, 1200)
ax2.set_ylim(0, w.max() * 1.30)
ax2.legend(loc="upper left", fontsize=8.0, bbox_to_anchor=(-0.01, 1.02))
ax2.set_xlabel("画面亮度（cd/m$^2$）")
ax2.set_ylabel("相对像素数")
ax2.set_yticks([])
ax2.set_xticks([1, 10, 100, 1000])
ax2.set_xticklabels(["1", "10", "100", "1000"])
ax2.minorticks_off()
ax2.set_title("(b) 一个画面里的亮度分布（示意）", fontsize=10.5, pad=6)

H.save(fig, 10, "f5_graphics_levels")
