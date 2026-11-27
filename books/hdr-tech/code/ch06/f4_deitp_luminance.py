# -*- coding: utf-8 -*-
"""第 06 章 图 4：1 个 ΔE_ITP 在不同亮度上对应多大的亮度差（按 PQ 公式计算）。

BT.2124 的 ΔE_ITP 定义在 ICtCp 上，只考虑亮度分量时
    ΔE_ITP = 720 · ΔI,  I 为 PQ 码值（0..1）
所以 1 个 ΔE_ITP 对应 ΔI = 1/720，在 10 位下约 1.42 个码值，与亮度无关。
但同样的码值差换算成绝对亮度差和相对亮度差，两者都随亮度剧烈变化。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

L = np.logspace(np.log10(0.005), np.log10(5000.0), 800)
I = H.pq_oetf(L)
dI = 1.0 / 720.0
dL = H.pq_eotf(np.minimum(I + dI, 1.0)) - L
rel = dL / L * 100.0

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 4.0))
fig.subplots_adjust(wspace=0.30)

ax1.plot(L, dL, color=H.NAVY, lw=2.2)
ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlim(0.005, 5000)
ax1.set_ylim(1e-5, 100)
ax1.set_xticks([0.01, 0.1, 1, 10, 100, 1000, 5000])
ax1.set_xticklabels(["0.01", "0.1", "1", "10", "100", "1000", "5000"])
ax1.set_yticks([1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100])
ax1.set_yticklabels(["0.0001", "0.001", "0.01", "0.1", "1", "10", "100"])
ax1.minorticks_off()
ax1.set_xlabel("画面亮度（nit，对数刻度）")
ax1.set_ylabel("1 个 ΔE_ITP 对应的亮度差（nit）")

for xv, txt in [(100, "100 nit"), (1000, "1000 nit")]:
    yv = np.interp(xv, L, dL)
    ax1.plot([xv], [yv], "o", ms=5, color=H.ORANGE, mec="white", mew=1.0, zorder=5)
    ax1.annotate(f"{txt}：{yv:.1f} nit", xy=(xv, yv), xytext=(0.03, yv * 4.2),
                 fontsize=8.2, color=H.ORANGE,
                 arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=0.9,
                                 connectionstyle="arc3,rad=0.2"))

ax1.set_title("(a) 绝对亮度差", fontsize=10, pad=4)

ax2.plot(L, rel, color=H.TEAL, lw=2.2)
ax2.set_xscale("log")
ax2.set_xlim(0.005, 5000)
ax2.set_ylim(0, 6)
ax2.set_xticks([0.01, 0.1, 1, 10, 100, 1000, 5000])
ax2.set_xticklabels(["0.01", "0.1", "1", "10", "100", "1000", "5000"])
ax2.minorticks_off()
ax2.set_xlabel("画面亮度（nit，对数刻度）")
ax2.set_ylabel("1 个 ΔE_ITP 对应的相对亮度差（%）")
ax2.axhline(1.0, color=H.GRAY, lw=0.9, ls=":")
ax2.text(0.006, 1.08, "1%：中间调的视觉分辨力", fontsize=8.0, color=H.GRAY)
ax2.set_title("(b) 相对亮度差", fontsize=10, pad=4)

H.save(fig, 6, "f4_deitp_luminance")
print("100nit", np.interp(100, L, dL), "rel", np.interp(100, L, rel))
print("1000nit", np.interp(1000, L, dL), "rel", np.interp(1000, L, rel))
print("0.1nit", np.interp(0.1, L, dL), "rel", np.interp(0.1, L, rel))
