# -*- coding: utf-8 -*-
"""第 07 章 图 5：在编码域做运算的代价。

(a) 黑白边缘做同样宽度的模糊，线性域与 gamma 域的亮度剖面对比
(b) 把画面亮度乘一个系数，在编码域直接缩放带来的亮度误差
(c) 三对灰按 50% 混合，正确亮度与 gamma 域平均后显示的亮度
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rgbspace as R

plt = H.plt

fig, axes = plt.subplots(1, 3, figsize=(7.5, 3.2),
                         gridspec_kw={"wspace": 0.42})

# ---------- (a) 边缘模糊 ----------
ax = axes[0]
n = 400
step = np.zeros(n)
step[n // 2:] = 1.0
k_sigma = 9.0
kx = np.arange(-4 * k_sigma, 4 * k_sigma + 1)
kernel = np.exp(-0.5 * (kx / k_sigma) ** 2)
kernel /= kernel.sum()


def blur(a):
    return np.convolve(a, kernel, mode="same")


prof_lin = blur(step)
prof_code = R.gamma_eotf(blur(R.gamma_oetf(step)))
xx = (np.arange(n) - n // 2) / (4 * k_sigma)

ax.plot(xx, prof_lin, color=H.NAVY, lw=2.0, label="线性域模糊（正确）")
ax.plot(xx, prof_code, color=H.RED, lw=1.8, ls="--", label="编码域模糊")
ax.fill_between(xx, prof_code, prof_lin, where=prof_lin > prof_code,
                color=H.RED, alpha=0.10, lw=0)
ax.plot([0, 0], [0.2176, 0.5], "o", ms=4.0, color=H.DARK, mec="white", mew=0.7,
        zorder=6)
ax.plot([0, 0], [0.2176, 0.5], color=H.GRAY, lw=0.9, ls=(0, (2, 2)), zorder=5)
ax.annotate("过渡中点\n0.50 变 0.22", (0.07, 0.33), xytext=(0.55, 0.15),
            fontsize=7.4, color=H.DARK, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=H.GRAY, lw=0.8))
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(0, 1.0)
ax.set_xlabel("像素位置（以模糊半径为单位）")
ax.set_ylabel("显示亮度（归一化）")
ax.set_title("(a) 边缘过渡处的亮度剖面", fontsize=9.8, pad=6)
ax.legend(loc="upper left", fontsize=7.0, handlelength=1.8, borderaxespad=0.2,
          labelspacing=0.25)

# ---------- (b) 亮度缩放的误差 ----------
ax = axes[1]
alpha = np.linspace(0.04, 1.0, 400)
for name, g, col, ls in (("gamma 2.2", 2.2, H.ORANGE, "-"),
                         ("sRGB 分段", None, H.GREEN, (0, (5, 2)))):
    if g is None:
        ratio = R.srgb_eotf(alpha) / np.maximum(R.srgb_eotf(1.0) * alpha, 1e-9)
    else:
        ratio = alpha ** g / alpha
    ax.plot(alpha, (ratio - 1) * 100, color=col, lw=1.8, ls=ls, label=name)
ax.axhline(0, color="#4a5666", lw=0.9)
ax.set_xlim(0, 1.0)
ax.set_ylim(-90, 6)
ax.set_xlabel("期望的亮度系数")
ax.set_ylabel("实际亮度相对期望的误差  %")
ax.set_title("(b) 编码域直接缩放亮度", fontsize=9.8, pad=6)
ax.legend(loc="lower right", fontsize=7.4, handlelength=2.0, borderaxespad=0.2,
          labelspacing=0.25)

# ---------- (c) 50% 混合 ----------
ax = axes[2]
pairs = [(0.0, 1.0), (0.2, 0.8), (0.1, 0.9)]
labels = ["0 与 1", "0.2 与 0.8", "0.1 与 0.9"]
xp = np.arange(len(pairs))
w = 0.34
right, wrong = [], []
for a, b in pairs:
    la, lb = R.gamma_eotf(a, 2.2), R.gamma_eotf(b, 2.2)
    right.append((la + lb) / 2)
    wrong.append(R.gamma_eotf((a + b) / 2, 2.2))
b1 = ax.bar(xp - w / 2, right, width=w, color=H.NAVY, alpha=0.88,
            label="线性域混合")
b2 = ax.bar(xp + w / 2, wrong, width=w, color=H.RED, alpha=0.85,
            label="编码域混合")
for bars in (b1, b2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.015,
                f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=6.9,
                color=H.DARK)
ax.set_xticks(xp)
ax.set_xticklabels(labels, fontsize=7.6)
ax.set_xlabel("参与混合的两个灰阶")
ax.set_ylabel("混合后的显示亮度")
ax.set_ylim(0, 0.65)
ax.set_title("(c) 两个灰各取一半", fontsize=9.8, pad=6)
ax.legend(loc="upper right", fontsize=7.2, handlelength=1.2, borderaxespad=0.2,
          labelspacing=0.25)
ax.grid(axis="x", visible=False)

H.save(fig, 7, "f5_linearize_ops")
