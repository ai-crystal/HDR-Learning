# -*- coding: utf-8 -*-
"""图 7-6：8 bit 链路上的 HDR 信号被当成 SDR 解读之后。

左图是同一组码值在三种解读下对应的绝对亮度，右图把各自峰值归一化，
可以看出暗部被整体抬高、亮部被整体压平，也就是常说的“发灰”。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import FuncFormatter, NullFormatter, LogLocator

v = np.linspace(0.0, 1.0, 400)
v2 = v[1:]

pq = H.pq_eotf(v2)
g24 = 100.0 * v2 ** 2.4
g22 = 100.0 * H.srgb_eotf(v2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.9),
                               gridspec_kw={"wspace": 0.26})
fig.subplots_adjust(left=0.09, right=0.98, bottom=0.165, top=0.945)

TICKS1 = [0.1, 1, 10, 100, 1000, 10000]
TICKS2 = [1e-4, 1e-3, 1e-2, 1e-1, 1]


def style(ax, ymin, ymax, ticks):
    ax.set_yscale("log")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.75, 1.0])
    ax.set_xticklabels(["0", "0.2", "0.4", "0.6", "0.75", "1.0"])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_yticks(ticks)
    ax.yaxis.set_major_formatter(FuncFormatter(
        lambda y, p: f"{y:g}" if y >= 0.01 else f"{y:.0e}".replace("e-0", "e-")))
    ax.yaxis.set_minor_locator(LogLocator(subs=(2, 3, 4, 5, 6, 7, 8, 9)))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("归一化码值")


style(ax1, 0.02, 12000, TICKS1)
ax1.semilogy(v2, pq, color=H.ORANGE, lw=2.4, label="按 PQ 解读")
ax1.semilogy(v2, g24, color=H.NAVY, lw=2.2, ls=(0, (5, 2)),
             label="按 BT.1886 解读，白场 100 nit")
ax1.semilogy(v2, g22, color=H.GRAY, lw=1.6, ls=(0, (2, 2)),
             label="按 sRGB 解读，白场 100 nit")
ax1.axvline(0.75, color="#b8c3cf", lw=0.9, zorder=1)
ax1.axhline(100, color=H.GRAY, lw=0.8, ls=(0, (4, 3)), zorder=1)
ax1.set_ylabel("显示亮度（cd/m$^2$）")
ax1.legend(loc="lower right", fontsize=7.4, handlelength=2.4,
           borderpad=0.45, labelspacing=0.35)
ax1.annotate("码值 0.75 处\n1000 nit 只剩 48 nit", xy=(0.758, 42),
             xytext=(0.58, 2.6), fontsize=7.6, color=H.RED,
             ha="center", va="center", linespacing=1.6,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                             shrinkA=4, shrinkB=3,
                             connectionstyle="arc3,rad=-0.22"))
ax1.text(0.03, 2200, "PQ 的高光这一段，\n在 SDR 解读下全部消失",
         fontsize=7.6, color=H.GRAY, ha="left", va="center", linespacing=1.6)

style(ax2, 1e-5, 2.0, TICKS2)
ax2.semilogy(v2, pq / pq[-1], color=H.ORANGE, lw=2.4, label="按 PQ 解读")
ax2.semilogy(v2, g24 / g24[-1], color=H.NAVY, lw=2.2, ls=(0, (5, 2)),
             label="按 BT.1886 解读")
ax2.set_ylabel("相对亮度，以各自峰值为 1")
ax2.legend(loc="lower right", fontsize=7.6, handlelength=2.4,
           borderpad=0.45, labelspacing=0.35)
ax2.annotate("同一处暗部，\n被抬高一个数量级", xy=(0.22, 6.5e-3),
             xytext=(0.46, 2.2e-5), fontsize=7.6, color=H.RED,
             ha="center", va="center", linespacing=1.6,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                             shrinkA=4, shrinkB=3,
                             connectionstyle="arc3,rad=0.25"))

# 对数坐标的刻度文字在曲线绘制之后重设一次，避免回到科学计数法
for ax, tk in ((ax1, TICKS1), (ax2, TICKS2)):
    ax.set_yticks(tk)
    ax.yaxis.set_major_formatter(FuncFormatter(
        lambda y, p: f"{y:g}" if y >= 0.01 else f"{y:.0e}".replace("e-0", "e-")))

H.save(fig, 7, "f6_mistreated_8bit")
