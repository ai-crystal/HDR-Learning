# -*- coding: utf-8 -*-
"""第 04 章 图 4：局部算子的光晕（一维信号演示，公式计算）。

做法与 Durand & Dorsey 的双边分解相同：
    L = L_base × L_detail,  L_base = exp( G_sigma * log L )
只压缩基础层：L_disp = L_base^alpha × L_detail = L × L_base^(alpha-1)。
亮区附近的暗部会因为 base 被亮区"泄漏"抬高而变暗（暗晕），
亮区内侧则因为 base 被暗区拉低而变亮（亮边）；压缩越强，两种越界越深。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

W = 1200
x = np.arange(W)
BG, FG = 0.6, 300.0
EDGE0, EDGE1 = 430, 700

L = np.full(W, BG)
L[EDGE0:EDGE1] = FG
tex = 1.0 + 0.20 * np.sin(2 * np.pi * x / 34.0)
L = L * np.where((x < EDGE0) | (x > EDGE1), tex, 1.0)


def gauss_blur(sig, sigma):
    n = int(max(3, np.ceil(5 * sigma)))
    k = np.exp(-np.arange(-n, n + 1) ** 2 / (2 * sigma ** 2))
    k /= k.sum()
    return np.convolve(np.pad(sig, n, mode="edge"), k, mode="same")[n:-n]


def local_op(sig, sigma, alpha):
    base = np.exp(gauss_blur(np.log(np.maximum(sig, 1e-6)), sigma))
    return sig * base ** (alpha - 1.0)


disp_small = local_op(L, 12.0, 0.70)
disp_large = local_op(L, 70.0, 0.70)
disp_hard = local_op(L, 70.0, 0.45)

fig, ax = plt.subplots(figsize=(7.4, 4.4))
ax.plot(x, L, color=H.DARK, lw=2.2, ls=(0, (5, 2)), label="原画面（理想显示）")
ax.plot(x, disp_small, color=H.TEAL, lw=1.8, label="基础层半径小（12 像素），指数 0.70")
ax.plot(x, disp_large, color=H.ORANGE, lw=1.8, label="基础层半径大（70 像素），指数 0.70")
ax.plot(x, disp_hard, color=H.RED, lw=1.8, label="基础层半径大，指数 0.45")

ax.annotate("暗晕：紧邻亮区的暗部\n被压暗；压缩越强，\n暗晕越深、边界越明显",
            xy=(712, disp_hard[712]), xytext=(726, 7.0), fontsize=8.2, color=H.RED,
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.0,
                            connectionstyle="arc3,rad=0.2"))
ax.annotate("亮边：亮区内侧被抬亮", xy=(688, disp_large[688]), xytext=(750, 235),
            fontsize=8.5, color=H.TEAL,
            arrowprops=dict(arrowstyle="->", color=H.TEAL, lw=1.0,
                            connectionstyle="arc3,rad=-0.15"))
ax.annotate("暗部小纹理的起伏保留", xy=(316, disp_small[316]), xytext=(150, 9.0),
            fontsize=8.4, color=H.GRAY,
            arrowprops=dict(arrowstyle="->", color=H.GRAY, lw=0.9,
                            connectionstyle="arc3,rad=-0.22"))

ax.set_yscale("log")
ax.set_xlim(0, 1000)
ax.set_ylim(0.05, 1400)
ax.set_yticks([0.1, 1, 10, 100])
ax.set_yticklabels(["0.1", "1", "10", "100"])
ax.minorticks_off()
ax.set_xlabel("屏幕水平位置（像素）")
ax.set_ylabel("显示亮度（nit，对数刻度）")
ax.legend(loc="upper left", fontsize=8.0, labelspacing=0.35, borderpad=0.45)

H.save(fig, 4, "f5_halo_local")
