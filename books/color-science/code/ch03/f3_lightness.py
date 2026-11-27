# -*- coding: utf-8 -*-
"""第 03 章 图 3：CIELAB 的明度函数。

左图把 f(t) 与纯立方根 t^(1/3) 画在一起，横轴取对数以看清暗段的线性段。
右图画 L* 随 Y/Yn 的变化，并标出几个常用反射率对应的 L*。
数据全部由 CIE 15 的公式直接算得。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

plt = H.plt
D = 6.0 / 29.0
T0 = D ** 3
NL = chr(10)


def f(t):
    t = np.asarray(t, float)
    return np.where(t > T0, np.cbrt(t), t / (3 * D * D) + 4.0 / 29.0)


def Lstar(y):
    return 116 * f(y) - 16


fig = plt.figure(figsize=(7.2, 3.7))
ax = fig.add_axes([0.085, 0.175, 0.395, 0.700])
ax2 = fig.add_axes([0.607, 0.175, 0.363, 0.700])

# ---------- 左：f(t) 与立方根 ----------
t = np.logspace(-6, 0, 700)
ax.semilogx(t, t ** (1.0 / 3.0), color=H.ORANGE, lw=2.6, alpha=0.55,
            ls=(0, (4, 2)), zorder=4, label="纯立方根 $t^{1/3}$")
ax.semilogx(t, f(t), color=H.NAVY, lw=2.0, zorder=6,
            label="$f(t)$，CIELAB 的分段函数")
ax.axvline(T0, color=H.RED, lw=1.0, ls=(0, (2, 3)), zorder=3)
ax.axvspan(1e-6, T0, color="#eef2f7", zorder=1)

ax.annotate("拐点 $t=(6/29)^3=0.0089$", xy=(T0, 0.207), xytext=(1.1e-6, 0.94),
            fontsize=7.3, color=H.RED, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                            connectionstyle="arc3,rad=-0.25"),
            bbox=dict(facecolor="white", alpha=0.94, edgecolor="none", pad=1.4))
ax.annotate("暗段换成直线" + NL + "避开无穷导数", xy=(8.0e-6, 0.137),
            xytext=(1.6e-6, 0.50), fontsize=7.2, color="#2c3e50", ha="left",
            va="center", linespacing=1.55,
            arrowprops=dict(arrowstyle="->", color=H.GRAY, lw=0.9),
            bbox=dict(facecolor="white", alpha=0.94, edgecolor="none", pad=1.3))
ax.text(0.00035, 0.30, "拐点右侧两条曲线" + NL + "完全重合", fontsize=7.0,
        color="#4a5666", ha="left", va="center", linespacing=1.5,
        bbox=dict(facecolor="white", alpha=0.9, edgecolor="none", pad=0.9))

ax.set_xlim(1e-6, 1.0)
ax.set_ylim(0.0, 1.08)
ax.set_xticks([1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0])
ax.set_xticklabels(["$10^{-6}$", "$10^{-5}$", "$10^{-4}$", "$10^{-3}$",
                    "$10^{-2}$", "$10^{-1}$", "$10^{0}$"])
ax.set_xlabel("$t=Y/Y_n$（对数轴）", labelpad=2)
ax.set_ylabel("$f(t)$", labelpad=2)
ax.legend(loc="lower left", fontsize=7.0, frameon=True, handlelength=1.8,
          borderpad=0.40, labelspacing=0.30, ncol=2,
          bbox_to_anchor=(0.0, 1.005, 1.0, 0.1), mode="expand")

# ---------- 右：L* 随 Y/Yn ----------
y = np.linspace(0.0, 1.0, 800)
ax2.plot(y, Lstar(y), color=H.NAVY, lw=2.1, zorder=5)
ax2.plot([0, 1], [0, 100], color=H.GRAY, lw=1.0, ls=(0, (4, 3)), zorder=3)

for yv, lab, tx, ty, ha in [(0.18, "18% 灰卡  $L^*$=49.5", 0.255, 36.0, "left"),
                            (0.50, "50%  $L^*$=76.1", 0.575, 58.0, "left"),
                            (0.90, "90%  $L^*$=96.0", 0.905, 80.0, "right")]:
    ax2.plot([yv], [Lstar(yv)], "o", ms=5.0, mfc="white", mec=H.RED, mew=1.5,
             zorder=7)
    ax2.annotate(lab, xy=(yv, Lstar(yv)), xytext=(tx, ty), fontsize=7.2,
                 color="#2c3e50", ha=ha, va="center",
                 arrowprops=dict(arrowstyle="->", color=H.GRAY, lw=0.9),
                 bbox=dict(facecolor="white", alpha=0.9, edgecolor="none", pad=1.2))

ax2.text(0.46, 18, "灰虚线为线性参照", fontsize=7.0, color="#4a5666",
         ha="left", va="center",
         bbox=dict(facecolor="white", alpha=0.86, edgecolor="none", pad=1.0))
ax2.set_xlim(0.0, 1.0)
ax2.set_ylim(0, 104)
ax2.set_xlabel("$Y/Y_n$", labelpad=2)
ax2.set_ylabel("$L^*$", labelpad=2)
ax2.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax2.set_yticks([0, 20, 40, 60, 80, 100])

H.save(fig, 3, "f3_lightness")
print("L*(0.18)=%.2f  L*(0.5)=%.2f  L*(0.9)=%.2f  L*(T0)=%.2f"
      % (Lstar(0.18), Lstar(0.5), Lstar(0.9), Lstar(T0)))
