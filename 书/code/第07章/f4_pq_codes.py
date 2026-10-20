# -*- coding: utf-8 -*-
"""第 07 章 图 f4：PQ 码值分布 —— 暗部占用大量码值。

左图：10bit 1024 个码值按亮度数量级分配统计，0–100 nit 就吃掉约一半码值。
右图：逐码值的亮度间距 ΔL（绝对 nit，对数轴，左轴）与相对间距 ΔL/L（%，右轴），
      说明 PQ 让"每一级台阶的感知差别"在常用亮度区大致相等。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np
from matplotlib.ticker import FuncFormatter

code = np.arange(0, 1024)
nit = H.pq_eotf(code / 1023.0)

fig, (ax1, ax2) = H.plt.subplots(1, 2, figsize=(7.2, 4.4))

# ---------------- 左：码值分配柱状图 ----------------
edges = [0.0, 1.0, 10.0, 100.0, 1000.0, 10001.0]
labels = ["0 – 1", "1 – 10", "10 – 100", "100 – 1000", "1000 – 10000"]
counts = [int(np.sum((nit >= lo) & (nit < hi))) for lo, hi in zip(edges[:-1], edges[1:])]
tot = sum(counts)
colors = [H.PURPLE, H.NAVY, H.TEAL, H.ORANGE, H.RED]
bars = ax1.bar(range(len(counts)), counts, color=colors, edgecolor="white", width=0.68)
for b, cnt, col in zip(bars, counts, colors):
    ax1.text(b.get_x() + b.get_width() / 2, cnt + 12, "%d\n%.0f%%" % (cnt, cnt / tot * 100),
             ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=col)
ax1.axhline(tot / 2, color=H.GOLD, ls="--", lw=1.3)
ax1.text(4.42, tot / 2 + 10, "一半码值（512）落在 100 nit 以下", fontsize=8.5,
         color="#8a6f22", ha="right", va="bottom", fontweight="bold")
ax1.set_xticks(range(len(counts)))
ax1.set_xticklabels(labels, fontsize=8.5)
ax1.set_xlabel("亮度数量级（nit）")
ax1.set_ylabel("分配到的 10bit 码值个数")
ax1.set_title("1024 个码值怎么分？", fontweight="bold")
ax1.set_ylim(0, 560)

# ---------------- 右：码值间距 ----------------
dL = np.diff(nit)
mid = code[:-1] + 0.5
drel = dL / np.maximum(nit[:-1], 1e-12) * 100.0

ax2.semilogy(mid[1:], np.maximum(dL[1:], 1e-8), color=H.NAVY, lw=2.4,
             label="绝对间距 ΔL（nit，左轴）")
ax2.set_xlabel("10bit 码值")
ax2.set_ylabel("相邻码值的亮度间距 ΔL（nit，对数）", color=H.NAVY)
ax2.tick_params(axis="y", labelcolor=H.NAVY)
ax2.set_ylim(1e-5, 2e3)
ax2.set_xlim(0, 1023)
ax2.yaxis.set_major_formatter(FuncFormatter(lambda v_, p: ("%g" % v_)))

ax2b = ax2.twinx()
ax2b.semilogy(mid[1:], drel[1:], color=H.ORANGE, lw=2.0, ls="--",
              label="相对间距 ΔL/L（%，右轴）")
ax2b.set_ylabel("相对间距 ΔL/L（%，对数）", color=H.ORANGE)
ax2b.tick_params(axis="y", labelcolor=H.ORANGE)
ax2b.set_ylim(0.6, 300)
ax2b.grid(False)
ax2b.yaxis.set_major_formatter(FuncFormatter(lambda v_, p: ("%g" % v_)))

c1 = float(H.pq_oetf(1.0)) * 1023.0
ax2.axvline(c1, color=H.PURPLE, ls=":", lw=1.2)
ax2.text(c1 + 14, 300, "1 nit\n（码值 %.0f）" % c1, fontsize=8.5, color=H.PURPLE,
         fontweight="bold", va="top")
ax2.text(110, 2e-4, "暗部每级台阶小到 0.00004 nit", fontsize=8.5, color=H.NAVY,
         fontweight="bold")
ax2.annotate("亮部 ΔL 可达数十 nit",
             xy=(1010, 40), xytext=(420, 700), fontsize=8.5, color=H.RED,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.1))
ax2b.text(770, 3.0, "码值 512（100 nit）以上\n相对间距稳定在 ≈0.9%\n（人眼刚好可辨的量级）",
          fontsize=8.5, color=H.ORANGE, fontweight="bold", ha="right", va="center")
h1, l1 = ax2.get_legend_handles_labels()
h2, l2 = ax2b.get_legend_handles_labels()
ax2.legend(h1 + h2, l1 + l2, loc="center left", fontsize=8.5)
ax2.set_title("绝对间距悬殊，相对间距均匀", fontweight="bold")

fig.tight_layout()
H.save(fig, 7, "f4_pq_codes")
