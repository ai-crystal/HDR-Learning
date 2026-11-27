# -*- coding: utf-8 -*-
"""图 2-7：同一条暗部渐变在 8 bit gamma、10 bit PQ、12 bit PQ 下的台阶。

取 0.005 至 0.5 cd/m² 的亮度斜坡，分别按三条曲线量化，再把码值线性拉伸到
0 至 255 显示。三条横条共用同一段亮度范围，只是量化精度不同，因此看到的
条带数就是码值数。下方的剖面图把同一段数据的亮度画出来，台阶高度一目了然。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import FuncFormatter, NullFormatter
plt.rcParams["mathtext.fontset"] = "dejavusans"

W = 900
L0, L1 = 0.005, 0.5
x = np.linspace(0, 1, W)
L = L0 * (L1 / L0) ** x          # 对数均匀的亮度斜坡

cases = []

# 8 bit gamma 2.2
code = np.round(255 * (L / 100.0) ** (1 / 2.2))
cases.append(("8 bit，gamma 2.2", code, H.GRAY))

# 10 bit / 12 bit PQ
for bits, c in [(10, H.BLUE), (12, H.NAVY)]:
    code = np.round((2 ** bits - 1) * H.pq_oetf(L))
    cases.append((f"{bits} bit，PQ", code, c))

fig = plt.figure(figsize=(7.6, 4.6))
gs = fig.add_gridspec(4, 1, height_ratios=[1.0, 1.0, 1.0, 1.9], hspace=0.30,
                      left=0.175, right=0.975, bottom=0.115, top=0.955)

axes = []
for i, (lab, code, c) in enumerate(cases):
    ax = fig.add_subplot(gs[i])
    axes.append(ax)
    lo, hi = code.min(), code.max()
    strip = ((code - lo) / max(hi - lo, 1) * 255.0).astype(np.uint8)
    ax.imshow(strip.reshape(1, -1), cmap="gray", aspect="auto", vmin=0,
              vmax=255, extent=(0, 1, 0, 1))
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_color("#8a97a6")
    ax.text(-0.02, 0.5, lab, transform=ax.transAxes, ha="right", va="center",
            fontsize=8.4, color=H.DARK)
    ax.text(1.012, 0.5, f"{int(hi - lo + 1)} 级", transform=ax.transAxes,
            ha="left", va="center", fontsize=7.8, color=c)

axp = fig.add_subplot(gs[3])
for lab, code, c in cases:
    lvl = (code - code.min()) / max(code.max() - code.min(), 1)
    axp.plot(x, lvl, color=c, lw=1.7, drawstyle="steps-post", label=lab)

axp.set_xlim(0, 1)
axp.set_ylim(-0.05, 1.12)
axp.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
axp.set_xticklabels(["暗", "", "中间", "", "亮"])
axp.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
axp.set_xlabel("渐变条上的位置（亮度从 0.005 到 0.5 cd/m$^2$ 对数变化）")
axp.set_ylabel("归一化码值")
axp.legend(loc="upper left", fontsize=7.9, handlelength=1.8,
           borderpad=0.45, labelspacing=0.3)
axp.annotate("同一段亮度，8 bit 只有 21 级台阶", xy=(0.44, 0.055),
             xytext=(0.33, 0.72), fontsize=7.9, color=H.GRAY,
             arrowprops=dict(arrowstyle="->", color=H.GRAY, lw=0.9,
                             shrinkA=2, shrinkB=4))

H.save(fig, 2, "f7_banding")
