# -*- coding: utf-8 -*-
"""第 01 章 图 8：反射率测量的两种几何，以及定标与杂散光带来的系统误差。

(a) 45/0 环带几何与 d/8 积分球几何示意（几何示意，非实测装置图）。
(b) 白板标定误差 2% 与 0.5% 杂散光对 L* 的影响，横轴为真实反射率。
    白板误差等价于把全部反射率乘一个固定系数，误差在暗端按比例缩小；
    杂散光等价于加一个固定偏移，误差在暗端反而放大。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Wedge, Polygon

plt = H.plt

fig = plt.figure(figsize=(7.2, 4.3))
gs = fig.add_gridspec(1, 2, width_ratios=[1.30, 1.0], wspace=0.28)

# ==================== (a) 两种几何 ====================
ax = fig.add_subplot(gs[0])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
for s in ax.spines.values():
    s.set_visible(False)

# ---- 左：45/0 ----
ax.text(0.235, 0.955, "45/0 环形照明", fontsize=8.4, color=H.NAVY,
        fontweight="bold", ha="center", va="center")
# 样品
ax.add_patch(Rectangle((0.06, 0.16), 0.34, 0.045, facecolor="#cbb89a",
                       edgecolor="#7a6a52", lw=1.1, zorder=4))
ax.text(0.23, 0.115, "样品", fontsize=7.4, color="#5c4d38", ha="center",
        va="center")
# 45° 入射
for x0, col in ((0.055, H.GOLD), (0.345, H.GOLD)):
    ax.add_patch(FancyArrowPatch((x0 + (0.075 if x0 < 0.2 else -0.075), 0.50),
                                 (x0 + (0.02 if x0 < 0.2 else -0.02), 0.215),
                                 arrowstyle="-|>", mutation_scale=9,
                                 color=col, lw=1.6, zorder=3))
ax.add_patch(Rectangle((0.115, 0.485), 0.13, 0.075, facecolor="#fdf2d8",
                       edgecolor=H.GOLD, lw=1.1, zorder=5))
ax.text(0.18, 0.522, "光源", fontsize=7.0, color="#8a6a12", ha="center",
        va="center", zorder=6)
ax.text(0.065, 0.36, "45°", fontsize=7.4, color="#8a6a12", ha="center",
        va="center")
ax.text(0.395, 0.36, "45°", fontsize=7.4, color="#8a6a12", ha="center",
        va="center")
# 0° 接收
ax.add_patch(FancyArrowPatch((0.23, 0.215), (0.23, 0.70), arrowstyle="-|>",
                             mutation_scale=10, color=H.NAVY, lw=1.7, zorder=3))
ax.add_patch(Rectangle((0.19, 0.70), 0.085, 0.075, facecolor="#dfe8f2",
                       edgecolor=H.NAVY, lw=1.1, zorder=5))
ax.text(0.232, 0.737, "接收", fontsize=7.0, color=H.NAVY, ha="center",
        va="center", zorder=6)
ax.text(0.248, 0.60, "法线 0°", fontsize=7.0, color=H.NAVY, ha="left",
        va="center")
ax.text(0.235, 0.035, "镜面反射不进接收器", fontsize=6.9, color="#4a5666",
        ha="center", va="center")

# ---- 右：d/8 积分球 ----
ax.text(0.735, 0.955, "d/8 积分球", fontsize=8.4, color=H.TEAL,
        fontweight="bold", ha="center", va="center")
ax.add_patch(Circle((0.72, 0.50), 0.185, facecolor="#eef4f3",
                    edgecolor=H.TEAL, lw=1.3, zorder=2))
ax.add_patch(Circle((0.72, 0.50), 0.185, facecolor="none",
                    edgecolor="#b9d6d2", lw=0.8, ls=":", zorder=5))
ax.text(0.72, 0.60, "积分球内壁\n（高反射涂层）", fontsize=6.8, color="#2f6f66",
        ha="center", va="center", zorder=6)
# 样品口
ax.add_patch(Rectangle((0.665, 0.30), 0.11, 0.038, facecolor="#cbb89a",
                       edgecolor="#7a6a52", lw=1.1, zorder=6))
ax.text(0.72, 0.255, "样品口", fontsize=7.0, color="#5c4d38", ha="center",
        va="center", zorder=6)
# 8° 接收
ax.add_patch(FancyArrowPatch((0.79, 0.62), (0.90, 0.735), arrowstyle="-|>",
                             mutation_scale=9, color=H.TEAL, lw=1.6, zorder=3))
ax.text(0.905, 0.755, "8° 接收", fontsize=7.0, color=H.TEAL, ha="left",
        va="center")
# 光源与光陷阱
ax.add_patch(Polygon([[0.545, 0.60], [0.60, 0.66], [0.60, 0.52]],
                     closed=True, facecolor="#fdf2d8", edgecolor=H.GOLD,
                     lw=1.0, zorder=5))
ax.text(0.545, 0.545, "光源", fontsize=6.9, color="#8a6a12", ha="center",
        va="center", zorder=6)
ax.add_patch(Rectangle((0.80, 0.29), 0.10, 0.045, facecolor="#3b3b3b",
                       edgecolor="#222", lw=1.0, zorder=6))
ax.text(0.905, 0.312, "光陷阱", fontsize=6.9, color="#222", ha="left",
        va="center", zorder=6)
ax.text(0.735, 0.115, "含镜面分量（SCI）或排除（SCE）", fontsize=6.9,
        color="#4a5666", ha="center", va="center")

# ==================== (b) 系统误差 ====================
ax2 = fig.add_subplot(gs[1])


def lstar(y):
    d = 6.0 / 29.0
    t = np.asarray(y, dtype=float)
    f = np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4.0 / 29.0)
    return 116 * f - 16


rho = np.logspace(np.log10(0.004), np.log10(0.95), 400)
dL_white = lstar(rho * 0.99 / 0.97) - lstar(rho)
dL_stray = lstar(rho + 0.005) - lstar(rho)

ax2.semilogx(rho, dL_white, color=H.NAVY, lw=2.1,
             label="白板标定偏差 2%（0.99 对 0.97）")
ax2.semilogx(rho, dL_stray, color=H.RED, lw=2.1, label="杂散光 0.5%")
ax2.axhline(1.0, color=H.GRAY, lw=0.9, ls=":")
ax2.text(0.0042, 1.12, "ΔE = 1", fontsize=7.0, color=H.GRAY, ha="left",
         va="bottom")
ax2.set_xlim(0.004, 1.0)
ax2.set_ylim(0, 8.5)
ax2.set_xlabel("真实反射率 ρ")
ax2.set_ylabel("$L^*$ 的偏差")
ax2.set_title("(b) 两类系统误差的分布", fontsize=9.5, pad=6)
ax2.legend(loc="upper right", fontsize=7.0, frameon=True, handlelength=1.6,
           labelspacing=0.25)
ax2.annotate("暗端误差被放大", xy=(0.0105, 3.75), xytext=(0.0052, 6.3),
             fontsize=7.2, color=H.RED, ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                             connectionstyle="arc3,rad=0.18"))
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
ax2.xaxis.set_major_locator(FixedLocator([0.01, 0.03, 0.1, 0.3, 1.0]))
ax2.xaxis.set_minor_locator(NullLocator())
ax2.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))

H.save(fig, 1, "f8_measurement_geometry")

for r in (0.01, 0.05, 0.2, 0.5, 0.9):
    print(f"rho={r:.2f}  dL_white={lstar(r*0.99/0.97)-lstar(r):.3f}  "
          f"dL_stray={lstar(r+0.005)-lstar(r):.3f}")
