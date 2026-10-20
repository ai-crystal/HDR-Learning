# -*- coding: utf-8 -*-
"""第 05 章 图 1：sRGB / Adobe RGB / DCI-P3 / BT.2020 在 CIE 1931 色度图上的叠加。

重点图：一眼看出"三角形"是怎么一层层变大的。
数据：CIE 1931 2° 标准观察者（第 04 章 cie1931.py 提供色匹配函数）。
"""
import sys
sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
sys.path.insert(0, "E:/Study/HDR-Learning/书/code/第04章")
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import Patch
import hdrfig as H
import cie1931 as C

plt = H.plt

# ---------------- 常用矩阵 ----------------
# XYZ -> 线性 sRGB（D65），精确值
SRGB_FROM_XYZ = np.array([
    [3.2409699419045226, -1.5373831775700940, -0.4986107602930034],
    [-0.9692436362808796, 1.8759675015077202, 0.0415550574071756],
    [0.0556300796969937, -0.2039769588889765, 1.0569715142428786]])

WHITE_D65 = (0.3127, 0.3290)
WHITE_DCI = (0.3140, 0.3510)


# ---------------- 色域定义：基色 (x, y) ----------------
GAMUTS = [
    ("BT.2020", H.RED, [(0.708, 0.292), (0.170, 0.797), (0.131, 0.046)]),
    ("DCI-P3", H.ORANGE, [(0.680, 0.320), (0.265, 0.690), (0.150, 0.060)]),
    ("Adobe RGB (1998)", H.TEAL, [(0.640, 0.330), (0.210, 0.710), (0.150, 0.060)]),
    ("sRGB / BT.709", H.NAVY, [(0.640, 0.330), (0.300, 0.600), (0.150, 0.060)]),
]


def tri_area(p):
    x = np.array([q[0] for q in p])
    y = np.array([q[1] for q in p])
    return 0.5 * abs(x[0] * (y[1] - y[2]) + x[1] * (y[2] - y[0]) + x[2] * (y[0] - y[1]))


LAM, LX, LY = C.spectral_locus()
VIS_AREA = 0.5 * abs(np.dot(LX, np.roll(LY, 1)) - np.dot(LY, np.roll(LX, 1)))


def draw_chroma_bg(ax, xlim, ylim, n=820, bg=0.955):
    """在给定坐标范围内画 CIE 1931 色度图的近似彩色底图。"""
    xs = np.linspace(xlim[0], xlim[1], n)
    ys = np.linspace(ylim[0], ylim[1], n)
    XX, YY = np.meshgrid(xs, ys)
    Yp = np.maximum(YY, 1e-6)
    XYZ = np.stack([XX / Yp, np.ones_like(XX), (1.0 - XX - YY) / Yp], axis=-1)
    with np.errstate(invalid="ignore", divide="ignore"):
        lin = XYZ @ SRGB_FROM_XYZ.T
    lin = np.clip(np.nan_to_num(lin), 0.0, 1.0)
    img = H.srgb_oetf(lin)
    img = img * 0.82 + 0.18          # 轻微淡入白，避免过于刺眼
    pts = np.column_stack([XX.ravel(), YY.ravel()])
    path = Path(np.column_stack([np.append(LX, LX[0]), np.append(LY, LY[0])]))
    inside = path.contains_points(pts).reshape(XX.shape) & (YY > 1e-4)
    img = np.dstack([img, np.where(inside, 1.0, 0.0)])   # 轨迹外透明，网格可见
    ax.imshow(img, extent=[xlim[0], xlim[1], ylim[0], ylim[1]], origin="lower",
              aspect="auto", zorder=-1, interpolation="bilinear")
    return inside


fig = plt.figure(figsize=(7.2, 6.2))
ax = fig.add_axes([0.075, 0.215, 0.90, 0.745])

XLIM, YLIM = (-0.02, 0.82), (-0.02, 0.90)
ax.set_axisbelow(True)
for gl in ax.get_xgridlines() + ax.get_ygridlines():
    gl.set_zorder(-5)
draw_chroma_bg(ax, XLIM, YLIM)

# 光谱轨迹（马蹄形边界）与紫线
ax.plot(LX, LY, color="#3b4450", lw=1.1, zorder=3)
ax.plot([LX[0], LX[-1]], [LY[0], LY[-1]], color="#9aa3ad", lw=1.0, ls="--", zorder=3)

# 波长刻度
WL_OFFSET = {380: (-0.045, -0.018), 460: (0.030, 0.014), 620: (0.026, 0.010),
             700: (0.028, 0.014)}
for w in [380, 460, 480, 500, 520, 540, 560, 580, 600, 620, 700]:
    x = float(np.interp(w, LAM, LX))
    y = float(np.interp(w, LAM, LY))
    if w in WL_OFFSET:
        dx, dy = WL_OFFSET[w]
    else:
        d = np.array([x - 0.33, y - 0.33])
        d = d / np.linalg.norm(d)
        dx, dy = d * 0.032
    ax.plot([x], [y], "o", ms=2.6, color="#3b4450", zorder=6)
    ax.text(x + dx, y + dy, str(w), fontsize=7.2,
            color="#3b4450", ha="center", va="center", zorder=7)

# 四个色域三角形（由大到小叠画，最里面最清楚）
handles = []
for name, col, prim in GAMUTS:
    p = np.array(prim + [prim[0]])
    a = tri_area(prim)
    ax.fill(p[:, 0], p[:, 1], color=col, alpha=0.11, zorder=4)
    ax.plot(p[:, 0], p[:, 1], color=col, lw=2.3, zorder=5,
            solid_capstyle="round")
    handles.append(Patch(facecolor=col, alpha=0.30, edgecolor=col,
                         label=f"{name}　{a / VIS_AREA * 100:.1f}% 可见色域"))

# BT.2020 的三个顶点标注
for lab, (vx, vy), tx, ty, ha in [("R (0.708, 0.292)", (0.708, 0.292), 0.660, 0.150, "center"),
                                  ("G (0.170, 0.797)", (0.170, 0.797), 0.152, 0.842, "right"),
                                  ("B (0.131, 0.046)", (0.131, 0.046), 0.215, 0.004, "left")]:
    ax.plot([vx], [vy], "o", ms=5, color=H.RED, mec="white", mew=1.0, zorder=8)
    ax.text(tx, ty, lab, fontsize=7.4, color=H.RED, ha=ha, va="center", zorder=8,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.72))

# sRGB 三基色点
for (vx, vy) in [(0.640, 0.330), (0.300, 0.600), (0.150, 0.060)]:
    ax.plot([vx], [vy], "o", ms=4, color=H.NAVY, mec="white", mew=0.9, zorder=8)

# 白点
ax.plot([WHITE_D65[0]], [WHITE_D65[1]], marker="*", ms=15, color="white",
        mec="#2b2b2b", mew=0.9, zorder=9, label="D65 白点 (0.3127, 0.3290)")
ax.plot([WHITE_DCI[0]], [WHITE_DCI[1]], marker="*", ms=12, color=H.GOLD,
        mec="#2b2b2b", mew=0.8, zorder=9, label="DCI 影院白点 (0.3140, 0.3510)")
ax.text(0.3127 - 0.030, 0.3290 + 0.022, "D65", fontsize=8.5, color="#2b2b2b",
        fontweight="bold", zorder=9)
ax.text(0.3140 + 0.014, 0.3510 + 0.016, "DCI 白点（偏暖）", fontsize=7.6,
        color="#6b5a20", zorder=9)

# 说明性注释
ax.annotate("sRGB 只覆盖可见色域的约 1/3\n（网页 / SDR 电视的最小公约数）",
            xy=(0.33, 0.36), xytext=(0.055, 0.62), fontsize=8.0, color=H.NAVY,
            ha="left", va="center", zorder=10,
            arrowprops=dict(arrowstyle="->", color=H.NAVY, lw=1.1,
                            connectionstyle="arc3,rad=-0.25"),
            bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=H.NAVY,
                      alpha=0.88, lw=0.8))
ax.annotate("BT.2020：HDR 的“大画布”\n三角形几乎贴到马蹄形外缘",
            xy=(0.35, 0.72), xytext=(0.415, 0.845), fontsize=8.0, color=H.RED,
            ha="left", va="center", zorder=10,
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.1,
                            connectionstyle="arc3,rad=0.20"),
            bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=H.RED,
                      alpha=0.88, lw=0.8))

ax.set_xlim(*XLIM)
ax.set_ylim(*YLIM)
ax.set_xlabel("色度坐标 x")
ax.set_ylabel("色度坐标 y")
ax.set_title("四大色域在 CIE 1931 色度图上的叠加：三角形越大 = 能显示的颜色越多",
             pad=9)
leg = ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.105),
                ncol=3, fontsize=8.4, handlelength=1.6, columnspacing=1.2)
leg.set_zorder(20)

fig.text(0.5, 0.016,
         "注：百分比 = 色域三角形面积 ÷ CIE 1931 可见色域（马蹄形）面积，按 xy 坐标严格计算；"
         "不同文献口径略有出入。",
         ha="center", fontsize=7.6, color=H.GRAY)

H.save(fig, 5, "f1_gamuts")

print("BT.2020   面积 %.5f  %.1f%%" % (tri_area(GAMUTS[0][2]), tri_area(GAMUTS[0][2]) / VIS_AREA * 100))
print("DCI-P3    面积 %.5f  %.1f%%" % (tri_area(GAMUTS[1][2]), tri_area(GAMUTS[1][2]) / VIS_AREA * 100))
print("AdobeRGB  面积 %.5f  %.1f%%" % (tri_area(GAMUTS[2][2]), tri_area(GAMUTS[2][2]) / VIS_AREA * 100))
print("sRGB/709  面积 %.5f  %.1f%%" % (tri_area(GAMUTS[3][2]), tri_area(GAMUTS[3][2]) / VIS_AREA * 100))
