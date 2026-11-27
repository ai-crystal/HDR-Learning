# -*- coding: utf-8 -*-
"""第 10 章 图 2：4000 nit 母版映射到 108 cd/m² 银幕的三种做法。

(a) 三条映射曲线，横纵轴均为对数亮度。
    - 恒等：不映射，超过 108 的部分在银幕上不存在。
    - 整体线性缩放：按 108/4000 缩小，白与暗一起掉。
    - 参考白对齐加高光肩部：203 落到 48，肩部用幂函数
      f(L) = 48 (1 + (L-203)/K)^q，K 与 q 由三个条件唯一确定：
      过 (203, 48)、过 (4000, 108)、拐点斜率与线性段连续 (48/203)。
(b) 第三条曲线的局部斜率 dlnL_out/dlnL_in。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

WHITE_SRC, WHITE_DST = 203.0, 48.0
PEAK_SRC, PEAK_DST = 4000.0, 108.0
S = WHITE_DST / WHITE_SRC          # 0.2365，白到白的比例


def solve_k():
    lo, hi = 1.0, 4000.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        q = S * mid / WHITE_DST
        val = WHITE_DST * (1.0 + (PEAK_SRC - WHITE_SRC) / mid) ** q
        if val > PEAK_DST:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


K = solve_k()
Q = S * K / WHITE_DST


def shoulder(l_in):
    l_in = np.asarray(l_in, dtype=float)
    lin = l_in * S
    comp = WHITE_DST * (1.0 + np.maximum(l_in - WHITE_SRC, 0.0) / K) ** Q
    return np.where(l_in <= WHITE_SRC, lin, comp)


L = np.logspace(np.log10(0.005), np.log10(PEAK_SRC), 900)

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(7.4, 5.8), gridspec_kw={"height_ratios": [1.55, 1.0]}, sharex=True)
fig.subplots_adjust(left=0.115, right=0.965, bottom=0.10, top=0.955, hspace=0.10)

ax1.plot(L, np.minimum(L, PEAK_DST), color=H.LGRAY, lw=1.8, ls=(0, (4, 2)),
         label="恒等（超出银幕能力即削平）", zorder=2)
ax1.plot(L, L * S, color=H.ORANGE, lw=2.0, label="整体线性缩放", zorder=3)
Ls = shoulder(L)
ax1.plot(L, Ls, color=H.NAVY, lw=2.6, label="参考白对齐 + 高光肩部", zorder=4)

for x, y, c in [(WHITE_SRC, WHITE_DST, H.NAVY), (PEAK_SRC, PEAK_DST, H.RED)]:
    ax1.plot([x], [y], "o", ms=6, color=c, mec="white", mew=1.0, zorder=6)

ax1.axhline(PEAK_DST, color=H.RED, lw=0.9, ls=(0, (5, 3)), zorder=1)
ax1.text(0.0063, PEAK_DST * 1.35, "银幕峰值 108", fontsize=8.0, color=H.RED, ha="left",
         bbox=dict(facecolor="white", edgecolor="none", pad=1.0), zorder=7)

ax1.annotate("参考白 203 → 48\n低 2.1 档", xy=(WHITE_SRC, WHITE_DST),
             xytext=(2.0, 0.035), fontsize=8.2, color=H.NAVY,
             arrowprops=dict(arrowstyle="->", color=H.NAVY, lw=0.9,
                             connectionstyle="arc3,rad=-0.28"), zorder=7)
ax1.annotate("峰值 4000 → 108\n低 5.2 档", xy=(PEAK_SRC, PEAK_DST),
             xytext=(120, 0.14), fontsize=8.2, color=H.RED,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                             connectionstyle="arc3,rad=0.25"), zorder=7)

ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlim(0.005, 6000)
ax1.set_ylim(1e-4, 1.4e3)
ax1.set_ylabel("银幕亮度（cd/m$^2$）")
ax1.set_yticks([1e-4, 1e-3, 1e-2, 0.1, 1, 10, 100, 1000])
ax1.set_yticklabels(["1e-4", "1e-3", "1e-2", "0.1", "1", "10", "100", "1000"])
ax1.minorticks_off()
ax1.legend(loc="lower right", fontsize=8.2, bbox_to_anchor=(1.0, 0.02))

dl = np.gradient(np.log(Ls), np.log(L))
ax2.plot(L, dl, color=H.NAVY, lw=2.4, zorder=3)
ax2.axhline(1.0, color=H.GRAY, lw=1.0, ls=(0, (4, 3)), zorder=1)
ax2.axvline(WHITE_SRC, color=H.NAVY, lw=0.8, ls=(0, (2, 2)), zorder=1)
ax2.text(WHITE_SRC * 1.12, 0.86, "参考白", fontsize=7.8, color=H.NAVY, va="top")
ax2.text(0.30, 0.62, "拐点以上对数斜率从 1 降到 0.17\n亮度涨 10 倍，银幕只涨 1.5 倍", fontsize=8.0, color=H.NAVY)

ax2.set_xscale("log")
ax2.set_xlim(0.005, 6000)
ax2.set_ylim(0, 1.10)
ax2.set_xlabel("母版亮度（cd/m$^2$）")
ax2.set_ylabel("局部斜率")
ax2.set_xticks([0.01, 0.1, 1, 10, 100, 1000])
ax2.set_xticklabels(["0.01", "0.1", "1", "10", "100", "1000"])
ax2.minorticks_off()

H.save(fig, 10, "f2_master_to_screen")
print("K = %.2f, q = %.4f, f(4000) = %.1f" % (K, Q, WHITE_DST * (1 + (PEAK_SRC - WHITE_SRC) / K) ** Q))
