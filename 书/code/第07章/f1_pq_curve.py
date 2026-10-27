# -*- coding: utf-8 -*-
"""第 07 章 图 f1：PQ（SMPTE ST 2084）曲线 —— 10bit 码值 0–1023 → 绝对亮度（nit，对数轴）。

要点：
  * 用 H.pq_eotf 逐码值计算绝对亮度，纵轴取对数，直观呈现约 7 个数量级的跨度。
  * 标注 100 / 1000 / 10000 nit 三个关键点及其对应码值。
  * 说明暗部（0–100 nit）就占用了一半码值。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
from matplotlib.ticker import FuncFormatter

fig, ax = H.plt.subplots(figsize=(7.2, 4.8))

# ---------- 主线：PQ EOTF ----------
code = np.arange(0, 1024)
nit = H.pq_eotf(code / 1023.0)
YLO = 3e-4
nit_plot = np.maximum(nit, YLO)          # 0 nit 无法在对数轴上显示，做下限截断

ax.fill_between(code, YLO, nit_plot, color=H.NAVY, alpha=0.06)
ax.semilogy(code, nit_plot, color=H.NAVY, lw=2.8, zorder=5)

# ---------- 暗部区间（0–100 nit 占一半码值） ----------
c100 = float(H.pq_oetf(100.0)) * 1023.0
ax.axvspan(0, c100, color=H.GOLD, alpha=0.12, zorder=0)
ax.text(0.015, 0.975,
        "暗部区间 0 – 100 nit\n已占 0 – %.0f 共 %.0f%% 的码值" % (c100, c100 / 1023 * 100),
        transform=ax.transAxes, va="top", ha="left", fontsize=9,
        color="#8a6f22", fontweight="bold")

# ---------- 关键亮度点 ----------
for lv, col, lab in [(100.0, H.ORANGE, "100 nit（SDR 白点）"),
                     (1000.0, H.TEAL, "1000 nit（常见 HDR 峰值）"),
                     (10000.0, H.RED, "10000 nit（PQ 上限）")]:
    c = float(H.pq_oetf(lv)) * 1023.0
    ax.axhline(lv, color=col, ls="--", lw=1.1, alpha=0.85)
    ax.plot([c], [lv], "o", color=col, ms=7, mec="white", mew=1.3, zorder=6)
    ax.text(c - 14, lv * 1.35, "%s → 码值 %.0f" % (lab, c), color=col, fontsize=9,
            fontweight="bold", ha="right", va="bottom")

# ---------- 曲线形态说明 ----------
ax.text(0.025, 0.235,
        "暗部极陡：一半码值只换来 0–100 nit 的细微变化\n"
        "亮部平缓：1000 nit 以上只用掉约 1/4 码值",
        transform=ax.transAxes, fontsize=9, color=H.DARK, va="top")
ax.text(0.42, 0.72, "PQ EOTF（ST 2084）", transform=ax.transAxes, color=H.NAVY,
        fontsize=9.5, fontweight="bold")

ax.set_xlabel("10bit PQ 码值（0 – 1023）")
ax.set_ylabel("绝对亮度（nit，对数刻度）")
ax.set_title("PQ（ST 2084）曲线：码值到绝对亮度", fontweight="bold")
ax.set_xlim(0, 1060)
ax.set_ylim(YLO, 1.2e5)
ax.set_xticks([0, 128, 256, 384, 512, 640, 768, 896, 1023])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: ("%g" % v)))

fig.tight_layout()
H.save(fig, 7, "f1_pq_curve")
