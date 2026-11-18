# -*- coding: utf-8 -*-
"""图 1-2：Barten 对比敏感度模型（1999 版，闭式公式计算）。

左：不同适应亮度下的 CSF 曲线；右：峰值对比敏感度随适应亮度的变化。
所有曲线由模型公式直接算出，不含任何实测或拟合数据。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import FuncFormatter, NullFormatter
plt.rcParams["mathtext.fontset"] = "dejavusans"


def plain_log(ax, which="xy"):
    """对数坐标用十进制数字标注，避免 mathtext 缺字。"""
    for a in which:
        axis = ax.xaxis if a == "x" else ax.yaxis
        axis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
        axis.set_minor_formatter(NullFormatter())


def barten_csf(u, L, X0=2.0, Xmax=12.0, Nmax=15.0, k=3.0, T=0.1,
               eta=0.03, p=1.2274e6, phi0=3e-8, u0=7.0,
               sigma0=0.5, Cab=0.08):
    """Barten(1999) 对比敏感度 S(u) = 1/m_t。

    u 空间频率（cpd），L 适应亮度（cd/m^2）。
    X0 目标角尺寸（度），Xmax 最大积分面积（度），Nmax 最大周期数，
    k 信噪比，T 积分时间(s)，eta 量子效率，p 瞳孔照度换算因子，
    phi0 神经噪声谱密度，u0 侧抑制峰值频率(cpd)，
    sigma0 光学点扩散（角分），Cab 色差系数（角分/mm）。
    """
    d = 5.0 - 3.0 * np.tanh(0.4 * np.log10(L / 40.0))        # 瞳孔直径 mm
    E = L * np.pi * d ** 2 / 4.0                              # 视网膜照度 td
    sigma = np.sqrt(sigma0 ** 2 + (Cab * d) ** 2) / 60.0      # 度
    M_opt = np.exp(-2.0 * np.pi ** 2 * sigma ** 2 * u ** 2)   # 光学 MTF
    spat = 1.0 / X0 ** 2 + 1.0 / Xmax ** 2 + u ** 2 / Nmax ** 2
    noise = 1.0 / (eta * p * E) + phi0 / (1.0 - np.exp(-(u / u0) ** 2))
    return M_opt / (k * np.sqrt(2.0 / T * spat * noise))


u = np.logspace(np.log10(0.6), np.log10(70.0), 500)
levels = [0.1, 1.0, 10.0, 100.0, 1000.0]
colors = [H.GRAY, H.TEAL, H.BLUE, H.NAVY, H.ORANGE]

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(8.6, 3.7), gridspec_kw={"width_ratios": [1.6, 1.0]})
fig.subplots_adjust(left=0.085, right=0.98, bottom=0.16, top=0.95, wspace=0.30)

for L, c in zip(levels, colors):
    ax1.loglog(u, barten_csf(u, L), color=c, lw=2.0,
               label=f"{L:g} cd/m$^2$")
ax1.set_xlim(0.6, 70)
ax1.set_ylim(0.2, 900)
ax1.set_xlabel("空间频率（周期/度，cpd）")
ax1.set_ylabel("对比敏感度  S = 1/m$_t$")
ax1.set_xticks([1, 2, 5, 10, 20, 50])
plain_log(ax1)
ax1.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
ax1.legend(loc="lower left", ncol=2, fontsize=8.2,
           handlelength=1.5, columnspacing=1.0, borderpad=0.5)
ax1.text(0.97, 0.94, "(a)", transform=ax1.transAxes,
         ha="right", va="top", fontsize=10, color=H.DARK)

Lg = np.logspace(-2, 4, 300)
peak = np.array([barten_csf(u, Lv).max() for Lv in Lg])
ax2.semilogx(Lg, peak, color=H.RED, lw=2.2)
ax2.set_xlim(1e-2, 1e4)
ax2.set_ylim(0, 560)
ax2.set_xlabel("适应亮度（cd/m$^2$）")
ax2.set_ylabel("峰值对比敏感度  $S_{max}$")
ax2.set_xticks([0.01, 0.1, 1, 10, 100, 1000, 10000])
plain_log(ax2, "x")
for Lv, c in zip(levels, colors):
    ax2.plot([Lv], [barten_csf(u, Lv).max()], "o", ms=5.5, color=c,
             mec="white", mew=0.8, zorder=5)
ax2.annotate("暗视觉区\n模型偏离实测", xy=(0.012, 40), xytext=(0.03, 300),
             fontsize=8.2, color=H.GRAY, ha="left",
             arrowprops=dict(arrowstyle="-", color=H.GRAY, lw=0.8))
ax2.text(0.97, 0.94, "(b)", transform=ax2.transAxes,
         ha="right", va="top", fontsize=10, color=H.DARK)

H.save(fig, 1, "f2_barten_csf")
