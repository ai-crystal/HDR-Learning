# -*- coding: utf-8 -*-
"""图 06-5：非线性编码为什么省位深 —— 暗部台阶更密。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt

Lw = 100.0      # 峰值白 100 nit
N = 8           # 8bit
nmax = 255

fig = H.plt.figure(figsize=(7.2, 5.2))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.4], hspace=0.42)

# ---------------- 上：整条码值范围，对数轴 ----------------
ax0 = fig.add_subplot(gs[0])
k = np.arange(nmax + 1)
Llin = Lw * k / nmax
Lgam = Lw * (k / nmax) ** 2.2

ax0.semilogy(k, np.maximum(Llin, 1e-3), color=H.ORANGE, lw=2.2, label="线性编码")
ax0.semilogy(k, np.maximum(Lgam, 1e-3), color=H.NAVY, lw=2.2, label="Gamma 2.2 编码")
ax0.axhspan(0.03, 1.0, color=H.RED, alpha=0.10, lw=0)
ax0.text(250, 0.115, "暗部区间 0–1 nit", fontsize=8.6, color=H.RED, ha="right")

n_lin = int(np.sum(Llin <= 1.0))
n_gam = int(np.sum(Lgam <= 1.0))
n_lin10 = int(np.sum(Llin <= 10.0))
n_gam10 = int(np.sum(Lgam <= 10.0))
ax0.annotate("线性：0–1 nit 只分到 3 个码值",
             xy=(3, 1.0), xytext=(105, 3.4), fontsize=8.5, color=H.ORANGE,
             arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=1.1))
ax0.annotate("Gamma：0–1 nit 分到 32 个码值",
             xy=(31, 0.9), xytext=(75, 1.12), fontsize=8.5, color=H.NAVY,
             arrowprops=dict(arrowstyle="->", color=H.NAVY, lw=1.1))
ax0.text(0.012, 0.035,
         "8bit 在 0–10 nit 内的可用级数\n线性 26 级　|　Gamma 90 级",
         transform=ax0.transAxes, fontsize=8.6, va="bottom", ha="left",
         color=H.DARK,
         bbox=dict(boxstyle="round,pad=0.35", fc="#f4f7fa", ec=H.LGRAY, lw=0.8))

ax0.set_xlim(0, nmax); ax0.set_ylim(1e-3, 200)
# 手写刻度标签，避开 mathtext 里 U+2212 缺字导致的方块
ax0.set_yticks([1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2])
ax0.set_yticklabels(["0.001", "0.01", "0.1", "1", "10", "100"])
ax0.minorticks_off()
ax0.set_xlabel("8bit 码值")
ax0.set_ylabel("输出亮度（nit，对数）")
ax0.set_title("① 全码值范围：Gamma 把码值向暗部倾斜", fontsize=11)
ax0.legend(loc="lower right", fontsize=8.5)

# ---------------- 下：前 32 级放大，看台阶高度 ----------------
ax1 = fig.add_subplot(gs[1])
kk = np.arange(0, 33)
ax1.step(kk, Lw * kk / nmax, where="post", color=H.ORANGE, lw=1.8,
         label=f"线性：每级≈{Lw/nmax:.2f} nit，台阶粗")
ax1.step(kk, Lw * (kk / nmax) ** 2.2, where="post", color=H.NAVY, lw=2.2,
         label="Gamma 2.2：暗部台阶“贴地”密排")

ax1.fill_between(kk, 0, Lw * (kk / nmax) ** 2.2, step="post",
                 color=H.NAVY, alpha=0.12, lw=0)
ax1.fill_between(kk, Lw * (kk / nmax) ** 2.2, Lw * kk / nmax, step="post",
                 color=H.ORANGE, alpha=0.13, lw=0)

for kx in [1, 4, 8, 16, 32]:
    ax1.plot([kx, kx], [Lw * (kx / nmax) ** 2.2, Lw * kx / nmax],
             color=H.GRAY, lw=0.7, ls=":")
ax1.annotate("码值 16：线性已 6.27 nit\nGamma 仅 0.23 nit",
             xy=(16, 0.23), xytext=(17.6, 3.0), fontsize=8.6, color=H.DARK,
             arrowprops=dict(arrowstyle="->", color=H.GRAY, lw=1.1))

ax1.set_xlim(0, 32.5); ax1.set_ylim(0, 13)
ax1.set_xlabel("8bit 码值（只取 0–32，暗部放大）")
ax1.set_ylabel("输出亮度（nit）")
ax1.set_title("② 暗部放大：同样的 8bit，Gamma 在暗部挤进了更多级", fontsize=11)
ax1.legend(loc="upper left", fontsize=8.5)

fig.suptitle("非线性编码为何省位深：把码值优先分给人眼敏感的暗部",
             fontweight="bold", y=0.995)
H.save(fig, 6, "f5_why_nonlinear")
