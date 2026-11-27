# -*- coding: utf-8 -*-
"""第 07 章 图 4：编码曲线与显示曲线不是同一条。

(a) 四条显示端的电光转换曲线（BT.1886 取两组黑位、纯 gamma 2.2、sRGB 显示曲线）
(b) 用错曲线时的亮度相对误差：以 BT.1886（峰值 100、黑位 0.005）为基准
BT.1886 公式：L = a (max(V + b, 0))^2.4，a、b 由 Lw、Lb 定出。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import rgbspace as R

plt = H.plt


def bt1886(V, Lw=100.0, Lb=0.005):
    a = (Lw ** (1 / 2.4) - Lb ** (1 / 2.4)) ** 2.4
    b = Lb ** (1 / 2.4) / (Lw ** (1 / 2.4) - Lb ** (1 / 2.4))
    return a * np.maximum(V + b, 0) ** 2.4


V = np.linspace(0, 1, 1200)

fig, axes = plt.subplots(1, 2, figsize=(7.4, 4.0), gridspec_kw={"wspace": 0.26})

ax = axes[0]
ax.semilogy(V, bt1886(V, 100, 0.005), color=H.NAVY, lw=2.0, label="BT.1886，黑位 0.005")
ax.semilogy(V, bt1886(V, 100, 0.1), color=H.BLUE, lw=1.7, ls=(0, (6, 2)),
            label="BT.1886，黑位 0.1")
ax.semilogy(V, bt1886(V, 100, 0.5), color=H.TEAL, lw=1.7, ls=(0, (2, 2)),
            label="BT.1886，黑位 0.5")
ax.semilogy(V, 100 * R.gamma_eotf(V, 2.2), color=H.ORANGE, lw=1.7,
            label="纯 gamma 2.2，峰值 100")
ax.semilogy(V, 100 * R.srgb_eotf(V), color=H.GREEN, lw=1.5, ls=(0, (5, 2, 1, 2)),
            label="sRGB 显示曲线，峰值 100")
ax.set_ylim(1e-3, 150)
ax.set_yticks([1e-3, 1e-2, 1e-1, 1, 10, 100])
ax.set_yticklabels(["0.001", "0.01", "0.1", "1", "10", "100"])
ax.set_xlim(0, 1)
ax.set_xlabel("输入码值")
ax.set_ylabel("显示亮度（尼特）")
ax.set_title("(a) 显示端 EOTF", fontsize=10.5, pad=6)
ax.legend(loc="lower right", fontsize=7.2, labelspacing=0.28, handlelength=2.0,
          borderaxespad=0.25)

# ---------- (b) 用错曲线的代价 ----------
ax = axes[1]
ref = bt1886(V, 100, 0.005)
for name, curve, col, ls in (
        ("纯 gamma 2.2", 100 * R.gamma_eotf(V, 2.2), H.ORANGE, "-"),
        ("sRGB 显示曲线", 100 * R.srgb_eotf(V), H.GREEN, (0, (5, 2, 1, 2))),
        ("BT.1886 忽略黑位", bt1886(V, 100, 1e-6), H.PURPLE, (0, (6, 2)))):
    ratio = np.log2(np.maximum(curve, 1e-9) / np.maximum(ref, 1e-9))
    ax.plot(V, ratio, color=col, lw=1.8, ls=ls, label=name)

ax.axhline(0, color="#4a5666", lw=0.9)
ax.axhspan(-0.05, 0.05, color="#e8edf2", zorder=0)
ax.set_xlim(0, 1)
ax.set_ylim(-3.2, 2.6)
ax.set_yticks([-3, -2, -1, 0, 1, 2])
ax.set_yticklabels(["1/8", "1/4", "1/2", "1", "2", "4"])
ax.set_xlabel("输入码值")
ax.set_ylabel("显示亮度相对正确值的倍数")
ax.set_title("(b) 用错曲线时的亮度偏差", fontsize=10.5, pad=6)
ax.legend(loc="lower left", fontsize=7.6, labelspacing=0.3, handlelength=2.2,
          borderaxespad=0.25, title="倍数为 1 表示完全正确", title_fontsize=7.4)

H.save(fig, 7, "f4_eotf_compare")
