# -*- coding: utf-8 -*-
"""第 07 章 图 f3：PQ / HLG / Gamma 2.2 三条传递函数归一化对比。

左图：线性纵轴（输出归一化到各自 0–1），看三条曲线形状差异。
右图：对数纵轴，暗部差异被放大 —— PQ 明显比 HLG、Gamma 更"陡"。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np
from matplotlib.ticker import FuncFormatter

v = np.linspace(0, 1, 2000)
pq = H.pq_eotf(v) / 10000.0          # 归一化：10000 nit → 1.0
hlg = H.hlg_eotf(v)                  # 场景线性 0–1
gam = H.gamma_eotf(v, 2.2)           # Gamma 2.2

fig, (ax1, ax2) = H.plt.subplots(1, 2, figsize=(7.2, 4.3))

# ---------------- 左：线性刻度 ----------------
ax1.plot(v, gam, color=H.GRAY, lw=2.4, ls="--", label="Gamma 2.2（SDR 相对）")
ax1.plot(v, hlg, color=H.ORANGE, lw=2.6, label="HLG EOTF（场景参考）")
ax1.plot(v, pq, color=H.NAVY, lw=2.6, label="PQ EOTF（显示参考，/10000）")
ax1.plot([0, 1], [0, 1], color=H.LGRAY, lw=1.0, ls=":", label="线性参考")

ax1.axvline(0.5, color=H.RED, ls=":", lw=1.0, alpha=0.8)
for y, col in [(0.5 ** 2.2, H.GRAY), (0.5 * 0.5 / 3.0, H.ORANGE),
               (float(H.pq_eotf(0.5)) / 10000.0, H.NAVY)]:
    ax1.plot([0.5], [y], "o", color=col, ms=5.5, mec="white", mew=1.0, zorder=6)
ax1.annotate("同一信号 0.5（10bit 码值 512）：\nPQ 输出仅约 1%，Gamma 约 22%",
             xy=(0.5, 0.012), xytext=(0.075, 0.50), fontsize=8.5, color=H.DARK,
             arrowprops=dict(arrowstyle="->", color=H.DARK, lw=1.1,
                             connectionstyle="arc3,rad=-0.25"))
ax1.set_xlabel("归一化输入信号（码值 / 最大值）")
ax1.set_ylabel("归一化输出光")
ax1.set_title("三条曲线归一化对比", fontweight="bold")
ax1.set_xlim(0, 1.0); ax1.set_ylim(0, 1.05)
ax1.legend(loc="upper left", fontsize=8.5)

# ---------------- 右：对数刻度看暗部 ----------------
ax2.semilogy(v[1:], np.maximum(pq[1:], 1e-7), color=H.NAVY, lw=2.6, label="PQ EOTF")
ax2.semilogy(v[1:], np.maximum(hlg[1:], 1e-7), color=H.ORANGE, lw=2.6, label="HLG EOTF")
ax2.semilogy(v[1:], np.maximum(gam[1:], 1e-7), color=H.GRAY, lw=2.4, ls="--", label="Gamma 2.2")
ax2.axvspan(0.0, 0.2, color=H.PURPLE, alpha=0.08)
ax2.text(0.015, 0.96, "暗部（信号最低 20%）", transform=ax2.transAxes, va="top",
         fontsize=8.5, color=H.PURPLE, fontweight="bold")
ax2.annotate("PQ 在此处比 Gamma 低 1 个数量级以上\n→ 同样的暗部细节需要更多码值支撑",
             xy=(0.17, 2.0e-5), xytext=(0.28, 1.6e-6), fontsize=8.5, color=H.NAVY,
             arrowprops=dict(arrowstyle="->", color=H.NAVY, lw=1.1,
                             connectionstyle="arc3,rad=0.22"))
ax2.set_xlabel("归一化输入信号（码值 / 最大值）")
ax2.set_ylabel("归一化输出光（对数刻度）")
ax2.set_title("对数刻度：暗部差异被放大", fontweight="bold")
ax2.set_xlim(0, 1.0); ax2.set_ylim(1e-7, 1.4)
ax2.yaxis.set_major_formatter(FuncFormatter(lambda v_, p: ("%g" % v_)))
ax2.legend(loc="lower right", fontsize=8.5)

fig.tight_layout()
H.save(fig, 7, "f3_pq_hlg_gamma")
