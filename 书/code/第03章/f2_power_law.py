# -*- coding: utf-8 -*-
"""第 03 章 图 2　史蒂文斯幂律：主观亮度 ≈ 物理亮度的约 1/3 次方。

左图：物理亮度（线性轴）→ 主观亮度，幂律曲线 vs 线性 vs 费希纳对数。
右图：双对数上把“倍数”讲清楚——物理 ×8，主观才 ×2。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import numpy as np
import hdrfig as H
from matplotlib.ticker import NullFormatter
plt = H.plt

LMAX = 1000.0
N = 800


def logticks(ax, which, ticks):
    lab = [r"$10^{%d}$" % int(round(np.log10(t))) for t in ticks]
    if which == "x":
        ax.set_xticks(ticks); ax.set_xticklabels(lab)
        ax.xaxis.set_minor_formatter(NullFormatter())
    else:
        ax.set_yticks(ticks); ax.set_yticklabels(lab)
        ax.yaxis.set_minor_formatter(NullFormatter())


fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(7.2, 3.95), gridspec_kw=dict(width_ratios=[1.05, 1.0], wspace=0.3))

# ---------------- 左：物理亮度 → 主观亮度 ----------------
L = np.linspace(0, LMAX, N)
lin = L / LMAX                              # 线性假设
pw = (L / LMAX) ** (1.0 / 3.0)              # 史蒂文斯幂律 n≈0.33
fe = np.log10(1 + L) / np.log10(1 + LMAX)   # 费希纳对数

ax1.plot(L, lin, color=H.GRAY, lw=2.0, ls="--",
         label="线性假设（错误）：亮度翻倍 = 感觉翻倍")
ax1.plot(L, fe, color=H.TEAL, lw=1.8, ls=":", label=r"费希纳对数 $S = k\ln L$")
ax1.plot(L, pw, color=H.RED, lw=2.8, label=r"史蒂文斯幂律 $S = k\,L^{1/3}$")

ax1.axhline(0.5, color=H.LGRAY, lw=1.0, ls="-")
ax1.axvline(125, color=H.PURPLE, lw=1.2, ls="--")
ax1.plot([125], [0.5], "o", color=H.PURPLE, ms=6, mec="white", mew=1.0, zorder=6)
ax1.annotate("物理 125 nit：主观已过一半\n（线性模型要等到 500 nit）",
             xy=(125, 0.5), xytext=(15, 0.74), fontsize=8.2, color=H.PURPLE,
             arrowprops=dict(arrowstyle="->", color=H.PURPLE, lw=1.0),
             bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.6))

ax1.annotate("物理 8 倍\n→ 主观 2 倍", xy=(8, 0.2), xytext=(190, 0.30),
             fontsize=8.6, color=H.RED,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.0))
ax1.annotate("物理 1000 nit 处\n主观才“满格”", xy=(1000, 1.0), xytext=(590, 0.50),
             fontsize=8.2, color=H.RED,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.0))

ax1.set_xlim(0, LMAX); ax1.set_ylim(0, 1.06)
ax1.set_xlabel("物理亮度 L（nit，线性轴）")
ax1.set_ylabel("主观亮度（以 1000 nit 为参照归一化）")
ax1.set_title("亮度涨 8 倍，感觉才“亮一倍”", fontsize=10)
ax1.legend(loc="lower right", fontsize=7.6)

# ---------------- 右：倍数关系（双对数） ----------------
x = np.logspace(0, 3, 500)
ax2.plot(x, x, color=H.GRAY, lw=1.6, ls="--", label="线性：主观倍数 = 物理倍数")
ax2.plot(x, x ** (1 / 3.0), color=H.RED, lw=2.6, label="幂律：主观倍数 = 物理倍数^(1/3)")
ax2.fill_between(x, x ** (1 / 3.0), x, color=H.RED, alpha=0.06, lw=0)

ax2.axhline(2.0, color=H.GREEN, lw=1.3, ls=":")
ax2.axvline(8.0, color=H.GREEN, lw=1.3, ls=":")

for xv, lab, dx, dy, ha in ((8, "×2 → ×1.26，×8 → ×2.0", 8, 9, "left"),
                            (64, "×64 → ×4.0", -8, 10, "right"),
                            (1000, "×1000 → ×10", -8, 12, "right")):
    yv = xv ** (1 / 3.0)
    ax2.plot([xv], [yv], "o", color=H.RED, ms=6, mec="white", mew=1.0, zorder=6)
    ax2.annotate(lab, xy=(xv, yv), xytext=(dx, dy), textcoords="offset points",
                 fontsize=8.2, color=H.RED, ha=ha)

ax2.annotate("主观“亮一倍”\n需要物理涨约 8 倍", xy=(8, 2.0), xytext=(30, 70),
             fontsize=8.6, color=H.GREEN,
             arrowprops=dict(arrowstyle="->", color=H.GREEN, lw=1.1))

ax2.text(1.06, 900, "其他感觉的幂指数（史蒂文斯）\n"
                    "电击 ≈ 3.5（放大）\n线段长度 ≈ 1.0（线性）\n明度 ≈ 0.33（压缩）",
         fontsize=7.8, color="#444444", ha="left", va="top",
         bbox=dict(fc="white", ec=H.LGRAY, lw=0.8, pad=2.4))

ax2.set_xscale("log"); ax2.set_yscale("log")
ax2.set_xlim(1, 1.2e3); ax2.set_ylim(0.55, 1.3e3)
logticks(ax2, "x", [1, 1e1, 1e2, 1e3])
logticks(ax2, "y", [1, 1e1, 1e2, 1e3])
ax2.set_xlabel("物理亮度倍数（对数轴）")
ax2.set_ylabel("主观亮度倍数（对数轴）")
ax2.set_title("幂律把巨大的物理范围“压扁”了", fontsize=10)
ax2.legend(loc="lower right", fontsize=7.6)
fig.suptitle("图 03-2　史蒂文斯幂律：主观亮度 ≈ 物理亮度的约 1/3 次方",
             fontsize=12.5, fontweight="bold", y=1.02)
H.save(fig, 3, "f2_power_law")
