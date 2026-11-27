# -*- coding: utf-8 -*-
"""第 06 章 图 4：三种色差公式在 HDR 亮度范围内的表现。

左图：固定 5% 的相对亮度差，三种公式的读数相对 203 cd/m² 处归一化后的变化。
右图：CIEDE2000 的明度权重函数 S_L 随 L* 的增长，L* > 100 处超出其拟合数据范围。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import ictcp as I

plt = H.plt

W = np.array([0.95047, 1.0, 1.08883])
WHITE_REF = 203.0


def gray(Y):
    return W * Y


YS = np.logspace(0, np.log10(4000), 160)


def readings(ratio=1.05):
    de00, ditp, dez = [], [], []
    for Y in YS:
        Y2 = Y * ratio
        lab1 = I.xyz_to_lab(gray(Y) / WHITE_REF, white=(0.95047, 1.0, 1.08883))
        lab2 = I.xyz_to_lab(gray(Y2) / WHITE_REF, white=(0.95047, 1.0, 1.08883))
        de00.append(float(I.deltaE_2000(lab1, lab2)))
        it1 = I.rgb_lin_to_ictcp(np.array([Y / 4000.0] * 3), peak=4000.0)
        it2 = I.rgb_lin_to_ictcp(np.array([Y2 / 4000.0] * 3), peak=4000.0)
        ditp.append(float(I.deltaE_ITP(it1, it2)))
        dez.append(float(I.deltaE_z(I.xyz_to_jzazbz(gray(Y)),
                                    I.xyz_to_jzazbz(gray(Y2)))))
    return np.array(de00), np.array(ditp), np.array(dez)


de00, ditp, dez = readings()
i0 = int(np.argmin(np.abs(YS - 203.0)))
rel = lambda a: a / a[i0]

fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.8),
                         gridspec_kw=dict(width_ratios=[1.12, 1.0], wspace=0.29))
fig.subplots_adjust(left=0.085, right=0.985, top=0.90, bottom=0.16)

ax = axes[0]
ax.plot(YS, rel(de00), color=H.RED, lw=2.0, label="$\\Delta E_{00}$（参考白 203）")
ax.plot(YS, rel(ditp), color=H.NAVY, lw=2.0, label="$\\Delta E_{ITP}$（BT.2124）")
ax.plot(YS, rel(dez), color=H.TEAL, lw=2.0, label="$\\Delta E_z$（Jzazbz）")
ax.axvline(203, color="#8a97a6", lw=1.0, ls=(0, (5, 3)))
ax.set_xscale("log")
ax.set_xlim(1, 4000)
ax.set_ylim(0.3, 3.4)
ax.set_xlabel("绝对亮度（cd/m$^2$）", fontsize=9.5)
ax.set_ylabel("相对 203 cd/m$^2$ 处的读数（倍）", fontsize=9.5)
ax.legend(loc="upper left", fontsize=7.6, handletextpad=0.6, borderpad=0.35)
ax.annotate("$\\Delta E_z$ 涨了约 3 倍", xy=(2600, 2.55), xytext=(120, 2.95),
            fontsize=7.4, color=H.TEAL,
            arrowprops=dict(arrowstyle="-|>", color=H.TEAL, lw=0.9,
                            shrinkA=2, shrinkB=3))
ax.annotate("$\\Delta E_{00}$ 在参考白以上基本不再变化", xy=(900, 1.02),
            xytext=(26, 0.40), fontsize=7.4, color=H.RED,
            arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=0.9,
                            shrinkA=2, shrinkB=3))

# ---------------- (b) S_L 与实验范围 ----------------
ax2 = axes[1]
L = np.linspace(0, 300, 400)
SL = 1 + 0.015 * (L - 50) ** 2 / np.sqrt(20 + (L - 50) ** 2)
SC = 1 + 0.045 * np.linspace(0, 0, 1) if False else None
ax2.axvspan(100, 300, color="#f3d9d4", alpha=0.55, lw=0)
ax2.plot(L, SL, color=H.RED, lw=2.0, label="$S_L(L^*)$")
for C, col in [(20, H.BLUE), (50, H.TEAL), (80, H.GREEN)]:
    ax2.plot(L, 1 + 0.015 * (L - 50) ** 2 / np.sqrt(20 + (L - 50) ** 2), alpha=0)
ax2.set_xlim(0, 300)
ax2.set_ylim(0, 6.0)
ax2.set_xlabel("$L^*$（CIEDE2000 的明度坐标）", fontsize=9.5)
ax2.set_ylabel("明度权重 $S_L$", fontsize=9.5)
ax2.text(252, 1.75, "$L^*>100$" + "\n" + "无实验数据", fontsize=7.8, color="#8a3a2e",
         ha="center", va="center")
ax2.text(8, 5.7, "$S_L$ 随 $L^*$ 二次增长，" + "\n" + "高亮度端的明度差被大幅折扣",
         fontsize=7.4, color="#39485a", va="top")
ax2.legend(loc="upper left", bbox_to_anchor=(0.02, 0.72), fontsize=7.6,
           handletextpad=0.6, borderpad=0.35)

H.save(fig, 6, "f4_deltaE_high_luminance")
