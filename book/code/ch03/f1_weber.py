# -*- coding: utf-8 -*-
"""第 03 章 图 1　韦伯定律：刚可辨亮度差 ΔL 与背景亮度 L 近似成正比。

左图：双对数坐标下的 ΔL–L 关系——韦伯区是一条 45° 直线，
      极暗处退化为恒定阈值（绝对阈值主导）。
右图：同样的物理增量 ΔL，在不同背景亮度下占背景的比例天差地别。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import numpy as np
import hdrfig as H
from matplotlib.ticker import NullFormatter
plt = H.plt

W = 0.015      # 典型韦伯比（1.5%）
DL0 = 0.01     # 绝对阈值地板（nit）


def logticks(ax, which, ticks):
    """log 轴刻度用 mathtext 写好，避免中文字体缺 U+2212 显示成方框。"""
    lab = [r"$10^{%d}$" % int(round(np.log10(t))) for t in ticks]
    if which == "x":
        ax.set_xticks(ticks); ax.set_xticklabels(lab)
        ax.xaxis.set_minor_formatter(NullFormatter())
    else:
        ax.set_yticks(ticks); ax.set_yticklabels(lab)
        ax.yaxis.set_minor_formatter(NullFormatter())


fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(7.2, 3.9),
    gridspec_kw=dict(width_ratios=[1.25, 1.0], wspace=0.33))

# ---------------- 左：ΔL 与 L 的关系 ----------------
L = np.logspace(-3, 4, 600)
weber = W * L
real = np.sqrt(DL0 ** 2 + weber ** 2)

ax1.fill_between(L, 0.01 * L, 0.02 * L, color=H.GOLD, alpha=0.30, lw=0, zorder=1,
                 label="典型韦伯比区间 1%–2%")
ax1.plot(L, weber, "--", color=H.NAVY, lw=1.6, zorder=3,
         label="纯韦伯预测 ΔL = 1.5% × L")
ax1.plot(L, real, color=H.RED, lw=2.6, zorder=4,
         label="真实可辨阈值（叠加绝对阈值）")
ax1.axvline(1.0, color=H.GRAY, ls=":", lw=1.1, zorder=2)

ax1.set_xscale("log"); ax1.set_yscale("log")
ax1.set_xlim(1e-3, 1.2e4); ax1.set_ylim(4e-3, 400)
logticks(ax1, "x", [1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e4])
logticks(ax1, "y", [1e-2, 1e-1, 1, 1e1, 1e2])
ax1.set_xlabel("背景亮度 L（nit，对数轴）")
ax1.set_ylabel("刚可辨的亮度差 ΔL（nit，对数轴）")
ax1.set_title("ΔL 与 L 近似成正比（双对数上的一条 45° 直线）", fontsize=10)
ax1.legend(loc="upper left", fontsize=7.6)

ax1.annotate("韦伯区（L > 1 nit）：\nΔL 随 L 等比放大",
             xy=(300, 4.5), xytext=(1.6, 12), fontsize=8.5, color=H.NAVY,
             arrowprops=dict(arrowstyle="->", color=H.NAVY, lw=1.0))
ax1.annotate("极暗处退化为恒定阈值：\n约 1 nit 以下不再成比例",
             xy=(0.004, 0.0105), xytext=(0.0013, 0.11), fontsize=8.5, color=H.TEAL,
             arrowprops=dict(arrowstyle="->", color=H.TEAL, lw=1.0))

for Lv, dx, dy, ha in ((1, 10, -16, "left"), (100, 9, -14, "left"),
                       (10000, -9, -26, "right")):
    dv = float(np.sqrt(DL0 ** 2 + (W * Lv) ** 2))
    ax1.plot([Lv], [dv], "o", color=H.RED, ms=5.5, zorder=6, mec="white", mew=0.9)
    ax1.annotate(f"L = {Lv:,} nit　ΔL ≈ {dv:.3g} nit", xy=(Lv, dv),
                 xytext=(dx, dy), textcoords="offset points",
                 fontsize=8, color=H.RED, ha=ha, zorder=7)

# ---------------- 右：同样的 ΔL，不同背景下差别巨大 ----------------
L2 = np.logspace(0, 4, 500)
ax2.fill_between(L2, 1.5, 400, color=H.GREEN, alpha=0.10, lw=0)
ax2.plot(L2, 100.0 / L2, color=H.RED, lw=2.4, label="增量 ΔL = 1 nit")
ax2.plot(L2, 10.0 / L2, color=H.BLUE, lw=1.9, ls="-.", label="增量 ΔL = 0.1 nit")
ax2.axhline(1.5, color=H.GREEN, lw=1.5, ls="--", label="韦伯比门槛 ≈ 1.5%")

ax2.set_xscale("log"); ax2.set_yscale("log")
ax2.set_xlim(1, 1.2e4); ax2.set_ylim(6e-3, 400)
logticks(ax2, "x", [1, 1e1, 1e2, 1e3, 1e4])
logticks(ax2, "y", [1e-2, 1e-1, 1, 1e1, 1e2])
ax2.set_xlabel("背景亮度 L（nit，对数轴）")
ax2.set_ylabel("该增量占背景的比例 ΔL/L（%，对数轴）")
ax2.set_title("同样的增量，背景越亮越看不出", fontsize=10)
ax2.legend(loc="lower left", fontsize=7.8)

ax2.text(1.06, 260, "同样的 1 nit 增量：\n"
                     "　背景 2 nit → 占 50%，极明显\n"
                     "　背景 60 nit → 占 1.7%，勉强\n"
                     "　背景 900 nit → 占 0.11%，看不出",
         fontsize=7.9, color="#333333", ha="left", va="top",
         bbox=dict(fc="white", ec=H.LGRAY, lw=0.8, pad=2.4))

for Lv, txt, dx, dy, ha in ((2, "50%", 7, 4, "left"),
                            (60, "1.7%", 7, 4, "left"),
                            (900, "0.11%", 8, -3, "left")):
    ax2.plot([Lv], [100.0 / Lv], "o", color=H.RED, ms=5.5, mec="white", mew=0.9, zorder=6)
    ax2.annotate(txt, xy=(Lv, 100.0 / Lv), xytext=(dx, dy), textcoords="offset points",
                 fontsize=8.2, color=H.RED, ha=ha, zorder=7)

ax2.text(1.06, 1.75, "门槛以上才分辨得出", fontsize=8, color=H.GREEN,
         ha="left", va="bottom")

fig.suptitle("图 03-1　韦伯定律：能分辨的“差别”取决于“背景”",
             fontsize=12.5, fontweight="bold", y=1.02)
H.save(fig, 3, "f1_weber")
