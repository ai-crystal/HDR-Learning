# -*- coding: utf-8 -*-
"""第 07 章 图 f2：HLG（BT.2100）OETF 曲线 —— 两段拼接，标出 1/12 拐点。

左图：OETF 全貌（场景线性 E → 信号 V），低段 γ≈0.5 平方根，高段对数，E=1/12 处拼接。
右图：同一曲线的对数横轴版本，突出高光段的对数压缩能力。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
from matplotlib.ticker import FuncFormatter

E = np.linspace(0, 1, 2000)
with np.errstate(invalid="ignore", divide="ignore"):
    V = H.hlg_oetf(E)          # E→0 时未采用的对数分支会产生 nan，属正常
Ejo = 1.0 / 12.0                     # 1/12 拐点
Vjo = 0.5                            # 对应信号 0.5

Esq = np.linspace(0, Ejo, 400)
Vsq = np.sqrt(3.0 * Esq)             # 低段：平方根
Elog = np.linspace(Ejo, 1.0, 1200)
a, b, c = 0.17883277, 0.28466892, 0.55991073
Vlog = a * np.log(12.0 * Elog - b) + c

fig, (ax1, ax2) = H.plt.subplots(1, 2, figsize=(7.2, 4.3))

# ---------------- 左：线性横轴 ----------------
ax1.fill_between(E, 0, V, color=H.TEAL, alpha=0.07)
ax1.plot(E, V, color=H.DARK, lw=1.4, alpha=0.5, label="HLG OETF（分段函数）")
ax1.plot(Esq, Vsq, color=H.TEAL, lw=2.6, label="低段：√(3E)　γ ≈ 0.5")
ax1.plot(Elog, Vlog, color=H.ORANGE, lw=2.6, label="高段：a·ln(12E-b)+c　对数")
ax1.plot([Ejo], [Vjo], "o", color=H.RED, ms=8, mec="white", mew=1.5, zorder=6)
ax1.axvline(Ejo, color=H.RED, ls=":", lw=1.2)
ax1.axhline(Vjo, color=H.RED, ls=":", lw=1.2)
ax1.annotate("拐点 E = 1/12 ≈ 0.0833\n对应信号 V = 0.5\n（10bit 码值 512）",
             xy=(Ejo, Vjo), xytext=(0.17, 0.245), fontsize=9, color=H.RED, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.3,
                             connectionstyle="arc3,rad=0.25"))
ax1.text(0.03, 0.99, "低段：接近 Gamma 家族（兼容 SDR）",
         fontsize=8.5, color=H.TEAL, va="top")
ax1.annotate("高段：对数曲线\n容纳极宽的高光范围", xy=(0.86, 0.962), xytext=(0.40, 0.42),
             fontsize=8.5, color=H.ORANGE, fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=1.2,
                             connectionstyle="arc3,rad=-0.2"))
ax1.set_xlabel("场景线性亮度 E（相对值 0 – 1）")
ax1.set_ylabel("HLG 信号 V（0 – 1）")
ax1.set_title("HLG OETF：平方根 + 对数两段拼接", fontweight="bold")
ax1.set_xlim(0, 1.02)
ax1.set_ylim(0, 1.05)
ax1.legend(loc="lower right", fontsize=8.5)

# ---------------- 右：对数横轴看高光压缩 ----------------
Ex = np.logspace(-4, 0, 1500)
with np.errstate(invalid="ignore", divide="ignore"):
    Vx = H.hlg_oetf(np.clip(Ex, 0, 1))
ax2.semilogx(Ex, Vx, color=H.ORANGE, lw=2.6, label="HLG OETF（对数横轴）")
ax2.semilogx(Ex, np.clip(H.gamma_oetf(np.clip(Ex, 1e-4, 1), 2.2), 0, 1.05),
             color=H.GRAY, ls="--", lw=1.8, label="Gamma 2.2 OETF（对比）")
ax2.axhline(0.5, color=H.RED, ls=":", lw=1.1)
ax2.plot([Ejo], [Vjo], "o", color=H.RED, ms=7, mec="white", mew=1.3, zorder=6)
ax2.annotate("1/12", xy=(Ejo, Vjo), xytext=(0.0016, 0.62), fontsize=9, color=H.RED,
             fontweight="bold",
             arrowprops=dict(arrowstyle="-", color=H.RED, lw=1.0))
ax2.text(1.5e-4, 0.80, "高光段：4 个数量级的场景亮度\n只换来约 0.1 的信号增量",
         fontsize=8.5, color=H.DARK,
         bbox=dict(boxstyle="round,pad=0.32", fc="white", ec=H.LGRAY, lw=0.8, alpha=0.95))
ax2.set_xlabel("场景线性亮度 E（对数刻度，相对值）")
ax2.set_ylabel("HLG 信号 V")
ax2.set_title("对数横轴：高光段的对数压缩", fontweight="bold")
ax2.set_xlim(1e-4, 1.0)
ax2.set_ylim(0, 1.12)
ax2.xaxis.set_major_formatter(FuncFormatter(lambda v_, p: ("%g" % v_)))
ax2.legend(loc="center left", fontsize=8.5)

fig.tight_layout()
H.save(fig, 7, "f2_hlg_curve")
