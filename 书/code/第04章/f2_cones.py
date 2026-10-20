# -*- coding: utf-8 -*-
"""第 04 章 图 2：S / M / L 三种视锥的响应曲线。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import hdrfig as H
import cie1931 as C

plt = H.plt

lam = C.LAM
S = C.S_CONE / C.S_CONE.max()
M = C.M_CONE / C.M_CONE.max()
L = C.L_CONE / C.L_CONE.max()
V = C.YBAR                                   # 明视觉 V(λ)
Vp = 1.019 * np.exp(-285.4 * (lam / 1000.0 - 0.559) ** 2)   # 暗视觉 V'(λ) 近似
Vp = Vp / Vp.max()

fig = plt.figure(figsize=(7.2, 4.3))
gs = fig.add_gridspec(1, 2, width_ratios=[2.45, 1.0], wspace=0.30)

ax = fig.add_subplot(gs[0])
ax.set_title("人眼的三条接收通道：S / M / L 视锥响应", pad=8)

ax.fill_between(lam, 0, S, color=H.PURPLE, alpha=0.13)
ax.fill_between(lam, 0, M, color=H.GREEN, alpha=0.13)
ax.fill_between(lam, 0, L, color=H.RED, alpha=0.13)
ax.plot(lam, S, color=H.PURPLE, lw=2.3, label="S 视锥（短波·蓝）")
ax.plot(lam, M, color=H.GREEN, lw=2.3, label="M 视锥（中波·绿）")
ax.plot(lam, L, color=H.RED, lw=2.3, label="L 视锥（长波·红）")
ax.plot(lam, V, color=H.GRAY, lw=1.4, ls="--", label=r"明视觉 $\bar{y}(\lambda)$（= V(λ)）")
ax.plot(lam, Vp, color=H.NAVY, lw=1.2, ls=":", label="暗视觉 V′(λ)（峰 ≈507 nm）")

# 峰值标注
for curve, tag, col, xyt, ha in ((S, "S 峰 445 nm", H.PURPLE, (416, 0.62), "center"),
                                 (M, "M 峰 545 nm", H.GREEN, (500, 0.32), "center"),
                                 (L, "L 峰 565 nm", H.RED, (676, 0.62), "center")):
    wl, h = C.peak_wavelength(curve)
    ax.plot([wl], [h], "o", ms=6, color=col, zorder=5)
    ax.annotate(tag, xy=(wl, h), xytext=xyt, fontsize=8.4,
                color=col, fontweight="bold", ha=ha, va="center",
                arrowprops=dict(arrowstyle="->", color=col, lw=1.1,
                                connectionstyle="arc3,rad=0.15"),
                bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=1.2))

# 重叠区
ax.axvspan(480, 620, color=H.GOLD, alpha=0.10, zorder=0)
ax.text(550, 0.06, "三条曲线大幅重叠\n每种光都同时刺激三种视锥", fontsize=8.2,
        color="#8a6d1f", ha="center", va="bottom", fontweight="bold")
ax.axhline(0, color="#4a5666", lw=0.9)

ax.set_xlim(380, 780)
ax.set_ylim(0, 1.62)
ax.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
ax.set_xlabel("波长 λ（nm）")
ax.set_ylabel("相对灵敏度（归一化）")
ax.legend(loc="upper right", fontsize=7.8, ncol=1)

# ---------- 右：同一种光刺激出"三个数" ----------
ax2 = fig.add_subplot(gs[1])
ax2.set_title("一个波长 → 三个数", pad=8)
samples = [(450, "450 nm\n(偏蓝)"), (550, "550 nm\n(偏绿)"), (650, "650 nm\n(偏红)")]
tri = []
for wl, _ in samples:
    i = int(np.argmin(np.abs(lam - wl)))
    t = np.array([S[i], M[i], L[i]])
    tri.append(t)
tri = np.array(tri)
x = np.arange(len(samples))
w = 0.26
ax2.bar(x - w, tri[:, 0], w, color=H.PURPLE, label="S")
ax2.bar(x, tri[:, 1], w, color=H.GREEN, label="M")
ax2.bar(x + w, tri[:, 2], w, color=H.RED, label="L")
for i in range(len(samples)):
    for j in range(3):
        if tri[i, j] < 0.02:
            continue
        ax2.text(x[i] + (j - 1) * w, tri[i, j] + 0.03, f"{tri[i,j]:.2f}",
                 ha="center", va="bottom", fontsize=6.6, color=H.GRAY)
ax2.set_xticks(x)
ax2.set_xticklabels([s[1] for s in samples], fontsize=7.6)
ax2.set_ylim(0, 1.45)
ax2.set_ylabel("相对刺激量")
ax2.set_xlabel("单色光波长")
ax2.legend(fontsize=7.6, ncol=3, loc="upper center", columnspacing=0.9,
           handlelength=1.0)
ax2.grid(axis="x", visible=False)

H.save(fig, 4, "f2_cones")
