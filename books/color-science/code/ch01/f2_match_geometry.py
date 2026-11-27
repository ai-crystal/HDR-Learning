# -*- coding: utf-8 -*-
"""第 01 章 图 2：色匹配实验的装置示意（左）与三刺激值的坐标含义（右）。

左图为几何示意，不是实测装置图；右图把三原色当作基向量，
任意色的三刺激值就是该向量在这组基下的坐标。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C
from matplotlib.patches import (Rectangle, Circle, Polygon, FancyArrowPatch,
                                Ellipse)

plt = H.plt

fig = plt.figure(figsize=(7.2, 4.0))
gs = fig.add_gridspec(1, 2, width_ratios=[1.55, 1.0], wspace=0.04)

# ==================== 左：双视场目视匹配装置 ====================
ax = fig.add_subplot(gs[0])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
for s in ax.spines.values():
    s.set_visible(False)

FX0, FX1, FY0, FY1 = 0.44, 0.90, 0.60, 0.92
ax.add_patch(Rectangle((FX0, FY0), FX1 - FX0, FY1 - FY0, facecolor="white",
                       edgecolor="#2c3e50", lw=1.4, zorder=4))
mid = 0.5 * (FY0 + FY1)

grad = np.linspace(0, 1, 256).reshape(1, -1)
ax.imshow(grad, extent=[FX0, FX1, mid + 0.004, FY1 - 0.004], origin="lower",
          aspect="auto", cmap="YlOrBr", alpha=0.85, zorder=5, vmin=-0.4, vmax=1.2)
ax.add_patch(Rectangle((FX0 + 0.004, FY0 + 0.004), FX1 - FX0 - 0.008,
                       mid - FY0 - 0.008, facecolor="#e0b184",
                       edgecolor="none", zorder=5))
ax.plot([FX0, FX1], [mid, mid], color="#2c3e50", lw=1.6, zorder=6)
ax.text(FX0 + 0.012, FY1 - 0.032, "待测光", fontsize=8.4, color="#5a3c10",
        fontweight="bold", va="center", zorder=7)
ax.text(FX0 + 0.012, mid - 0.032, "R + G + B 混合", fontsize=8.4, color="#4a3020",
        fontweight="bold", va="center", zorder=7)

# ---- 待测光来源：单色仪（棱镜） ----
ax.add_patch(Polygon([[0.06, 0.86], [0.19, 0.86], [0.125, 0.72]], closed=True,
                     facecolor="#dcecf7", edgecolor="#3f6f92", lw=1.2, zorder=4))
for yy in np.linspace(0.85, 0.73, 5):
    ax.add_patch(FancyArrowPatch((0.015, yy), (0.06, yy + 0.005),
                                 arrowstyle="-|>", mutation_scale=7,
                                 color="#7a5fb0", lw=0.9, zorder=4))
ax.text(0.105, 0.655, "单色仪\n（连续谱分光）", fontsize=7.2, color="#3f6f92",
        ha="center", va="center", zorder=6)
ax.add_patch(FancyArrowPatch((0.135, 0.755), (FX0 - 0.012, 0.82),
                            arrowstyle="-|>", mutation_scale=9, color="#7a5fb0",
                            lw=1.3, zorder=3,
                            connectionstyle="arc3,rad=-0.20"))

# ---- 三原色灯：灯 + 滑轨 + 光束 ----
lamp_y = [0.47, 0.36, 0.25]
lamp_info = [("R 650 nm", H.RED, 0.62), ("G 530 nm", H.GREEN, 0.44),
             ("B 460 nm", H.BLUE, 0.28)]
LX = 0.285
for (name, col, frac), yy in zip(lamp_info, lamp_y):
    ax.add_patch(FancyArrowPatch((0.015, yy), (LX - 0.038, yy), arrowstyle="-",
                                 color=col, lw=1.8, alpha=0.65, zorder=3))
    ax.add_patch(Circle((LX, yy), 0.032, facecolor=col, alpha=0.72,
                        edgecolor="#2c3e50", lw=1.0, zorder=5))
    # 滑轨与滑块：滑块位置即该原色用量
    ax.plot([LX + 0.055, LX + 0.165], [yy, yy], color="#8d99a6", lw=3.4,
            solid_capstyle="round", zorder=3)
    ax.plot([LX + 0.055 + 0.11 * frac], [yy], marker="s", ms=8.5,
            mfc="white", mec=col, mew=1.8, zorder=6)
    ax.text(LX + 0.185, yy, name, fontsize=7.2, color=col, fontweight="bold",
            ha="left", va="center", zorder=6)
    # 光束汇入下半视场
    ax.add_patch(FancyArrowPatch((LX + 0.036, yy + 0.018), (FX0 + 0.002, 0.646),
                                 arrowstyle="-|>", mutation_scale=8, color=col,
                                 lw=1.0, alpha=0.65, zorder=3,
                                 connectionstyle="arc3,rad=-0.16"))

ax.text(0.44, 0.115, "三路原色按比例加光：\n滑块位置即该原色的三刺激值",
        fontsize=7.4, color="#2c3e50", ha="center", va="center",
        bbox=dict(facecolor="#f4f7fa", edgecolor=H.LGRAY, boxstyle="round,pad=0.32"))
ax.text(0.44, 0.028, "负值情形：把某盏原色灯改照到上半视场，等效于负刺激值",
        fontsize=6.9, color=H.RED, ha="center", va="center")

# ---- 观察者 ----
ex, ey = 0.815, 0.475
ax.add_patch(Ellipse((ex, ey), 0.068, 0.098, facecolor="white",
                     edgecolor="#2c3e50", lw=1.2, zorder=6))
ax.add_patch(Circle((ex - 0.009, ey), 0.021, facecolor="#2c3e50", zorder=7))
ax.add_patch(Circle((ex - 0.016, ey + 0.006), 0.0058, facecolor="white", zorder=8))
ax.text(ex - 0.045, ey, "观察者", fontsize=7.6, color="#2c3e50", ha="right",
        va="center")
ax.add_patch(FancyArrowPatch((0.862, FY0 - 0.008), (ex + 0.030, ey + 0.042),
                             arrowstyle="-|>", mutation_scale=9, color=H.NAVY,
                             lw=1.3, ls=(0, (4, 2)), zorder=5,
                             connectionstyle="arc3,rad=-0.28"))

# ==================== 右：三刺激值 = 基向量坐标 ====================
ax2 = fig.add_subplot(gs[1])
ax2.set_xlim(-0.50, 1.10)
ax2.set_ylim(-0.30, 1.18)
ax2.set_aspect("equal")
ax2.set_xticks([]); ax2.set_yticks([]); ax2.grid(False)
for s in ax2.spines.values():
    s.set_visible(False)


def proj(x, y, z):
    """轴测投影：X 向右上、Y 向上、Z 向左上。"""
    return 0.80 * x - 0.62 * z, y + 0.26 * x + 0.18 * z


o = proj(0, 0, 0)
AX = 0.80
axes_def = [(proj(AX, 0, 0), r"$X$", H.RED, "right"),
            (proj(0, AX, 0), r"$Y$", H.GREEN, "up"),
            (proj(0, 0, AX), r"$Z$", H.BLUE, "left")]
for (ux, uy), lab, col, side in axes_def:
    ax2.annotate("", xy=(ux, uy), xytext=o,
                 arrowprops=dict(arrowstyle="-|>", color=col, lw=2.0,
                                 mutation_scale=12))
    if side == "right":
        ax2.text(ux + 0.07, uy - 0.01, lab, fontsize=10.5, color=col,
                 fontweight="bold", ha="left", va="center")
    elif side == "up":
        ax2.text(ux, uy + 0.09, lab, fontsize=10.5, color=col,
                 fontweight="bold", ha="center", va="bottom")
    else:
        ax2.text(ux - 0.07, uy - 0.01, lab, fontsize=10.5, color=col,
                 fontweight="bold", ha="right", va="center")

# 刺激向量 P
P = (0.56, 0.66, 0.34)
px, py = proj(*P)
ax2.annotate("", xy=(px, py), xytext=o,
             arrowprops=dict(arrowstyle="-|>", color=H.DARK, lw=2.2,
                             mutation_scale=13))
ax2.plot([px], [py], "o", ms=6, mfc="white", mec=H.DARK, mew=1.8, zorder=6)
ax2.text(px + 0.055, py + 0.055, r"$\mathbf{P}=(X,Y,Z)$", fontsize=9.2,
         color=H.DARK, fontweight="bold", ha="left", va="bottom")

# 三条投影虚线，标出三个坐标值
for k, col in ((0, H.RED), (1, H.GREEN), (2, H.BLUE)):
    q = list(P); q[k] = 0.0
    ax2.plot([px, proj(*q)[0]], [py, proj(*q)[1]], color=col, lw=1.1,
             ls=(0, (3, 2)), alpha=0.9, zorder=4)
    r = [0.0, 0.0, 0.0]; r[k] = P[k]
    ax2.plot([proj(*r)[0]], [proj(*r)[1]], "s", ms=5, mfc="white", mec=col,
             mew=1.5, zorder=6)

ax2.text(o[0] - 0.012, o[1] - 0.105, "O", fontsize=8.6, color="#4a5666",
         ha="center", va="center")
ax2.text(0.34, -0.235, "同一种光换一组原色基向量，\n坐标数值改变，颜色不变",
         fontsize=7.2, color=H.NAVY, ha="center", va="center")

H.save(fig, 1, "f2_match_geometry")
