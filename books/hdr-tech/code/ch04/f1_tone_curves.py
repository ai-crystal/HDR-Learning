# -*- coding: utf-8 -*-
"""第 04 章 图 1：四种色调映射算子的曲线形状（全部按公式计算）。

归一化约定：
  输入为绝对亮度（nit），输出为归一化显示值；
  各曲线均按"输入 400 nit 时输出 1.0"标定，便于比较曲线形状差异。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

# ---------------- 算子定义 ----------------
def reinhard(L, Lw=4.0):
    """Reinhard 扩展式（2002）：L 以参考白 100 nit 为单位，Lw 为映射到白点的亮度单位。"""
    return L * (1.0 + L / Lw ** 2) / (1.0 + L)


def hable(x, A=0.15, B=0.50, C=0.10, D=0.20, E=0.02, F=0.30):
    """Hable / Uncharted 2 影调曲线（GDC 2010）。"""
    return (x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F) - E / F


def aces_fit(x):
    """Narkowicz 2015 对 ACES RRT+ODT 的解析拟合。"""
    x = np.clip(x, 0.0, None)
    return np.clip(x * (2.51 * x + 0.03) / (x * (2.43 * x + 0.59) + 0.14), 0.0, 1.0)


# ---------------- 采样 ----------------
nit = np.logspace(np.log10(0.2), np.log10(400.0), 800)
PEAK = 400.0

y_rein = reinhard(nit / 100.0, Lw=PEAK / 100.0)
y_hable = hable(nit / 100.0) / hable(PEAK / 100.0)
y_aces = aces_fit((nit / 100.0) / (PEAK / 100.0)) / aces_fit(1.0)
y_lin = np.clip(nit / PEAK, 0.0, 1.0)

fig, ax = plt.subplots(figsize=(7.2, 4.4))

ax.plot(nit, y_lin, color=H.LGRAY, lw=1.6, ls=(0, (4, 2)), label="线性截断（无映射）")
ax.plot(nit, y_rein, color=H.BLUE, lw=2.2, label="Reinhard 扩展式（白点 400 nit）")
ax.plot(nit, y_hable, color=H.ORANGE, lw=2.2, label="Hable / Uncharted 2")
ax.plot(nit, y_aces, color=H.RED, lw=2.2, label="ACES 拟合（Narkowicz 2015）")

ax.axvline(100.0, color=H.GRAY, lw=1.0, ls=":")
ax.axvline(PEAK, color=H.DARK, lw=1.0, ls=":")
ax.text(94, 0.055, "参考白 100 nit", fontsize=8.5,
        color=H.GRAY, ha="right", va="bottom")
ax.text(392, 0.055, "峰值 400 nit", fontsize=8.5,
        color=H.DARK, ha="right", va="bottom")

ax.set_xscale("log")
ax.set_xlim(0.2, 420)
ax.set_ylim(0.0, 1.05)
ax.set_xlabel("输入亮度（nit，对数刻度）")
ax.set_ylabel("输出（归一化显示值）")
ax.set_yticks(np.arange(0, 1.01, 0.2))
ax.legend(loc="upper left", fontsize=8.5)
ax.grid(True, which="major", axis="both", color="#dde3ea", lw=0.7)
ax.grid(True, which="minor", axis="x", color="#eef2f6", lw=0.5)

H.save(fig, 4, "f1_tone_curves")
