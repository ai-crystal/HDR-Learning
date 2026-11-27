# -*- coding: utf-8 -*-
"""第 03 章 图 6：CIEDE2000 各修正项的形状。

左图沿色相角画 T 与 Δθ。右图画 S_C 与 S_H 随平均彩度的变化，
S_H 取色相角 275°（T 取小值）的最严情形；S_L 只与明度有关，
单独在右上角标出它在 50 与 0/100 处的取值。
数据全部按 CIEDE2000 的定义直接计算。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

plt = H.plt
NL = chr(10)

fig = plt.figure(figsize=(7.2, 3.35))
ax = fig.add_axes([0.072, 0.175, 0.400, 0.715])
ax2 = fig.add_axes([0.590, 0.175, 0.365, 0.715])

# ---------- 左：T 与 Δθ 沿色相 ----------
h = np.linspace(0, 360, 1441)
T = (1 - 0.17 * np.cos(np.radians(h - 30)) + 0.24 * np.cos(np.radians(2 * h))
     + 0.32 * np.cos(np.radians(3 * h + 6)) - 0.20 * np.cos(np.radians(4 * h - 63)))
dth = 30 * np.exp(-(((h - 275.0) / 25.0) ** 2))

ax.axvspan(229, 321, color="#fdf1e3", zorder=1)
ax.plot(h, T, color=H.NAVY, lw=2.2, zorder=6, label="色相权重 $T$")
ax.set_xlabel("平均色相角 $\\bar h'$（度）", labelpad=2)
ax.set_ylabel("$T$", color=H.NAVY, labelpad=2)
ax.tick_params(axis="y", labelcolor=H.NAVY)
ax.set_xlim(0, 360)
ax.set_ylim(0.22, 1.72)
ax.set_xticks([0, 90, 180, 270, 360])

axb = ax.twinx()
axb.plot(h, dth, color=H.ORANGE, lw=2.0, ls=(0, (4, 2)), zorder=5,
         label=r"$\Delta\theta$")
axb.set_ylabel(r"$\Delta\theta$（度）", color=H.ORANGE, labelpad=4)
axb.tick_params(axis="y", labelcolor=H.ORANGE)
axb.set_ylim(-2, 36)

ax.annotate("谷底 290°" + NL + "蓝紫最严", xy=(288, 0.368), xytext=(228, 0.86),
            fontsize=7.0, color=H.DARK, ha="center", va="center", linespacing=1.5,
            arrowprops=dict(arrowstyle="->", color=H.GRAY, lw=0.9),
            bbox=dict(facecolor="white", alpha=0.92, edgecolor="none", pad=1.1))
ax.annotate("峰 234°" + NL + "蓝区最松", xy=(234, 1.575), xytext=(152, 1.60),
            fontsize=7.0, color=H.DARK, ha="center", va="center", linespacing=1.5,
            arrowprops=dict(arrowstyle="->", color=H.GRAY, lw=0.9),
            bbox=dict(facecolor="white", alpha=0.92, edgecolor="none", pad=1.1))
axb.annotate(r"$\Delta\theta$ 只在" + NL + "275°±25° 内显著",
             xy=(262, 29), xytext=(70, 31.0), fontsize=7.0, color=H.ORANGE,
             ha="center", va="center", linespacing=1.5,
             arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=0.9),
             bbox=dict(facecolor="white", alpha=0.92, edgecolor="none", pad=1.1))

lines = [plt.Line2D([], [], color=H.NAVY, lw=2.2),
         plt.Line2D([], [], color=H.ORANGE, lw=2.0, ls=(0, (4, 2)))]
ax.legend(lines, ["$T$（左轴）", r"$\Delta\theta$（右轴）"],
          loc="lower left", fontsize=7.0, frameon=True, handlelength=1.9,
          borderpad=0.40, labelspacing=0.30)

# ---------- 右：S_C 与 S_H ----------
Cb = np.linspace(0, 100, 500)
ax2.plot(Cb, 1 + 0.045 * Cb, color=H.NAVY, lw=2.2, zorder=6, label="$S_C$")
ax2.plot(Cb, 1 + 0.015 * Cb * 0.365, color=H.TEAL, lw=2.1, ls=(0, (5, 2)),
         zorder=5, label="$S_H$（$\\bar h'$=275°）")
ax2.axhline(1.0, color=H.GRAY, lw=1.1, ls=(0, (2, 2)), zorder=3)

ax2.plot([50], [3.25], "o", ms=4.8, mfc="white", mec=H.NAVY, mew=1.4, zorder=8)
ax2.text(53, 3.30, "3.25", fontsize=7.0, color=H.NAVY, ha="left", va="bottom")
ax2.plot([50], [1.274], "o", ms=4.8, mfc="white", mec=H.TEAL, mew=1.4, zorder=8)
ax2.text(53, 1.33, "1.27", fontsize=7.0, color=H.TEAL, ha="left", va="bottom")

ax2.set_xlabel("平均彩度 $\\bar C'$", labelpad=2)
ax2.set_ylabel("权重因子", labelpad=2)
ax2.set_xlim(0, 100)
ax2.set_ylim(0.80, 6.10)
ax2.set_yticks([1, 2, 3, 4, 5, 6])

ax2.legend(loc="upper left", fontsize=7.0, frameon=True, handlelength=1.9,
           borderpad=0.40, labelspacing=0.30)
ax2.text(30, 5.02, "$S_C$ 斜率最大" + NL + "$S_L$ 只随明度变化" + NL
         + "$S_H$ 兼随彩度与色相", fontsize=7.0, color="#2c3e50", ha="left",
         va="top", linespacing=1.75,
         bbox=dict(facecolor="white", alpha=0.92, edgecolor=H.LGRAY,
                   boxstyle="round,pad=0.34"))

H.save(fig, 3, "f6_de2000_terms")
print("T min %.3f @%.0f, T max %.3f @%.0f" % (T.min(), h[T.argmin()],
                                              T.max(), h[T.argmax()]))
