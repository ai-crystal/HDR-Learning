# -*- coding: utf-8 -*-
"""第 01 章 图 7：从 RGB 颜色匹配函数到 CIE XYZ —— 一次线性变换，消掉负值。

上：CIE RGB 匹配函数（红色有负值）；
中：一个 3×3 线性变换；
下：变换后的 CIE XYZ 匹配函数 x̄、ȳ、z̄ —— 全部非负，且 ȳ 恰等于亮度。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
sys.path.insert(0, "E:/Study/HDR技术/书/code/第04章")
import numpy as np
import hdrfig as H
import cie1931 as C

M = np.array([[2.7689, 1.7517, 1.1302],
              [1.0000, 4.5907, 0.0601],
              [0.0000, 0.0565, 5.5943]])
Minv = np.linalg.inv(M)
lam = C.LAM
r, g, b = Minv @ np.stack([C.XBAR, C.YBAR, C.ZBAR])

fig = H.plt.figure(figsize=(7.2, 6.0))
gs = fig.add_gridspec(3, 1, height_ratios=[1.0, 0.34, 1.0], hspace=0.62,
                      left=0.11, right=0.97, top=0.895, bottom=0.09)

# ---- 上：RGB 匹配函数 ----
ax1 = fig.add_subplot(gs[0])
ax1.axhline(0, color="#333", lw=0.8)
ax1.plot(lam, r, color=H.RED, lw=2.2, label=r"$\bar r$ (R)")
ax1.plot(lam, g, color=H.GREEN, lw=2.2, label=r"$\bar g$ (G)")
ax1.plot(lam, b, color=H.BLUE, lw=2.2, label=r"$\bar b$ (B)")
neg = r < -1e-4
ax1.fill_between(lam, r, 0, where=neg, color=H.RED, alpha=0.16, lw=0)
ax1.text(520, -0.10, "负值", color=H.RED, fontsize=7.8, fontweight="bold")
ax1.set_ylim(-0.13, 0.40); ax1.set_xlim(380, 780)
ax1.set_ylabel("匹配函数值")
ax1.set_title("① CIE RGB 颜色匹配函数（红原色有负值）", fontsize=10.5,
              fontweight="bold", color=H.NAVY)
ax1.legend(loc="upper left", fontsize=7.6, ncol=3)
ax1.grid(True, color="#e6ebf0", lw=0.6)

# ---- 中：变换箭头 ----
axm = fig.add_subplot(gs[1]); axm.axis("off")
axm.set_xlim(0, 1); axm.set_ylim(0, 1)
axm.annotate("", xy=(0.5, 0.05), xytext=(0.5, 0.95),
             arrowprops=dict(arrowstyle="-|>", color=H.PURPLE, lw=2.0,
                             mutation_scale=16))
axm.text(0.54, 0.55, "线性变换（3×3 矩阵）\n把 RGB 换成新的三条曲线",
         fontsize=8.6, color=H.PURPLE, ha="left", va="center", linespacing=1.5)
axm.text(0.10, 0.55, "选择 X：全为非负\n选择 Y：就等于亮度\n选择 Z：约等于蓝",
         fontsize=8.0, color=H.DARK, ha="left", va="center", linespacing=1.5)

# ---- 下：XYZ 匹配函数 ----
ax2 = fig.add_subplot(gs[2])
ax2.axhline(0, color="#333", lw=0.8)
ax2.plot(lam, C.XBAR, color=H.RED, lw=2.2, label=r"$\bar x(\lambda)$")
ax2.plot(lam, C.YBAR, color=H.GREEN, lw=2.2, label=r"$\bar y(\lambda)$ = 亮度 V(λ)")
ax2.plot(lam, C.ZBAR, color=H.BLUE, lw=2.2, label=r"$\bar z(\lambda)$")
for arr, col, txt in [(C.XBAR, H.RED, "x̄"), (C.YBAR, H.GREEN, "ȳ"), (C.ZBAR, H.BLUE, "z̄")]:
    i = int(np.argmax(arr))
    ax2.plot(lam[i], arr[i], "o", color=col, ms=4.5, zorder=6,
             markeredgecolor="white", markeredgewidth=0.8)
ax2.set_ylim(-0.05, 2.1); ax2.set_xlim(380, 780)
ax2.set_xlabel("波长 λ（nm）")
ax2.set_ylabel("匹配函数值")
ax2.set_title("② CIE XYZ 颜色匹配函数（全部 ≥ 0，且 $\\bar y$ 即亮度）", fontsize=10.5,
              fontweight="bold", color=H.NAVY)
ax2.legend(loc="upper left", fontsize=7.8)
ax2.grid(True, color="#e6ebf0", lw=0.6)
ax2.annotate("负值被彻底消除", xy=(0.72, 0.55), xycoords="axes fraction",
             fontsize=8.2, color=H.PURPLE, fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=H.PURPLE, lw=0.8))

fig.suptitle("从 RGB 到 XYZ：为什么 CIE 要另造一套三刺激值", fontsize=12.8,
             fontweight="bold", y=0.975)
H.save(fig, 1, "f7_xyz_transform")
