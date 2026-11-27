# -*- coding: utf-8 -*-
"""第 01 章 图 6：同色异谱对。

左：连续谱（黑体 6500 K）与三窄带光谱经 CIE 1931 2° 观察者积分后三刺激值相同。
右：两组三刺激值的对比，数值由数值积分得到。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C
from matplotlib.patches import Rectangle

plt = H.plt

lam = np.linspace(380, 780, 401)
C2 = 1.4388e-2          # 第二辐射常数，m·K


def planck(T, lam_nm):
    l = lam_nm * 1e-9
    return 1.0 / (l ** 5 * (np.exp(C2 / (l * T)) - 1.0))


def xyz_of(spd):
    return np.array([np.trapezoid(spd * np.interp(lam, C.LAM, c), lam)
                     for c in (C.XBAR, C.YBAR, C.ZBAR)])


def gauss(cen, fwhm=20.0):
    s = fwhm / 2.3548
    return np.exp(-0.5 * ((lam - cen) / s) ** 2)


# ---------- 光谱 A：黑体 6500 K，归一到 Y = 1 ----------
spd_a = planck(6500, lam)
spd_a = spd_a / xyz_of(spd_a)[1]
xyz_a = xyz_of(spd_a)
SCALE = spd_a.max()

# ---------- 光谱 B：三条窄带，权重由 3×3 线性方程组解出 ----------
CENTERS = (460.0, 545.0, 620.0)
Amat = np.column_stack([xyz_of(gauss(c)) for c in CENTERS])
w = np.linalg.solve(Amat, xyz_a)
spd_b = sum(wi * gauss(c) for wi, c in zip(w, CENTERS))
xyz_b = xyz_of(spd_b)

xy_a = xyz_a[:2] / xyz_a.sum()
xy_b = xyz_b[:2] / xyz_b.sum()

fig = plt.figure(figsize=(7.2, 4.1))
gs = fig.add_gridspec(1, 2, width_ratios=[1.62, 1.0], wspace=0.30)

# ==================== 左：两条光谱 ====================
ax = fig.add_subplot(gs[0])
ax.plot(lam, spd_a / SCALE, color=H.GOLD, lw=2.4,
        label="光谱 A：黑体 6500 K（连续谱）")
for wi, c, col in zip(w, CENTERS, (H.BLUE, H.GREEN, H.RED)):
    ax.fill_between(lam, 0, wi * gauss(c) / SCALE, color=col, alpha=0.26, lw=0)
    ax.plot(lam, wi * gauss(c) / SCALE, color=col, lw=1.4)
ax.plot(lam, spd_b / SCALE, color=H.DARK, lw=1.6, ls=(0, (4, 2)),
        label="光谱 B：460 / 545 / 620 nm 三窄带之和")

for c in CENTERS:
    i = int(np.argmin(np.abs(lam - c)))
    ax.annotate(f"{int(c)} nm", xy=(c, spd_b[i] / SCALE + 0.02),
                xytext=(c, spd_b[i] / SCALE + 0.13), fontsize=7.6,
                color="#2c3e50", ha="center", va="bottom",
                arrowprops=dict(arrowstyle="-", color="#7f8c8d", lw=0.8))


ax.set_xlim(380, 780)
ax.set_ylim(0, 3.95)
ax.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
ax.set_xlabel("波长 λ（nm）")
ax.set_ylabel("相对光谱功率（归一到 Y = 1）")
ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.01), fontsize=8.0,
          frameon=False, handlelength=1.9, borderpad=0.2, labelspacing=0.3)
ax.grid(axis="x", color="#e8edf2")

# ==================== 右：三刺激值对比 ====================
ax2 = fig.add_subplot(gs[1])
labels = [r"$X$", r"$Y$", r"$Z$"]
xo = np.arange(3)
bw = 0.34
ax2.bar(xo - bw / 2, xyz_a, bw, color=H.GOLD, edgecolor="#8a6f28", lw=0.8,
        label="光谱 A")
ax2.bar(xo + bw / 2, xyz_b, bw, color=H.NAVY, edgecolor="#12314d", lw=0.8,
        label="光谱 B")
for i in range(3):
    ax2.text(xo[i] - bw / 2, xyz_a[i] * 0.45, f"{xyz_a[i]:.3f}", ha="center",
             va="center", fontsize=7.0, color="white", rotation=90)
    ax2.text(xo[i] + bw / 2, xyz_b[i] * 0.45, f"{xyz_b[i]:.3f}", ha="center",
             va="center", fontsize=7.0, color="white", rotation=90)
ax2.set_xticks(xo)
ax2.set_xticklabels(labels, fontsize=10)
ax2.set_xlim(-0.6, 2.6)
ax2.set_ylim(0, 1.55)
ax2.set_ylabel("三刺激值（Y = 1）")
ax2.grid(axis="x", visible=False)
ax2.legend(loc="upper center", bbox_to_anchor=(0.5, 1.02), ncol=2,
           fontsize=8.0, frameon=False, handlelength=1.4, columnspacing=1.4)

H.save(fig, 1, "f6_metamerism")
print("A XYZ:", np.round(xyz_a, 4), "xy", np.round(xy_a, 4))
print("B XYZ:", np.round(xyz_b, 4), "xy", np.round(xy_b, 4))
print("weights:", np.round(w, 4))
