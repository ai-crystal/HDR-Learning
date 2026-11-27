# -*- coding: utf-8 -*-
"""第 02 章 图 3：色域三角形、面积比与沿色相方向的边界距离。

(a) CIE 1931 色度图上叠加 sRGB、DCI-P3、BT.2020 三个色域三角形，马蹄形面积按
    光谱轨迹多边形算得 0.3351，各三角形面积以它为单位换算成百分比。
(b) 以 D65 白点为原点，沿 CIE 1976 u'v' 的色相角画到色域边界的距离。距离
    反映的是"这个方向上还能走多远"，与三角形面积不是一回事：BT.2020 的优势
    集中在绿区，蓝区与 sRGB 差得不多。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C

plt = H.plt

GAMUTS = {
    "sRGB": ([(0.640, 0.330), (0.300, 0.600), (0.150, 0.060)], H.BLUE, "-"),
    "DCI-P3": ([(0.680, 0.320), (0.265, 0.690), (0.150, 0.060)], H.ORANGE, "-"),
    "BT.2020": ([(0.708, 0.292), (0.170, 0.797), (0.131, 0.046)], H.TEAL, "-"),
}
W = (0.3127, 0.3290)


def uv(x, y):
    """CIE 1976 u'v'：v' 是 1960 v 的 1.5 倍。"""
    d = -2 * x + 12 * y + 3
    return 4 * x / d, 9 * y / d


def uv_to_xy(u, v):
    d = 6 * u - 16 * v + 12
    return 9 * u / d, 4 * v / d


def poly_area(px, py):
    return 0.5 * abs(np.dot(px, np.roll(py, -1)) - np.dot(py, np.roll(px, -1)))


lam = np.linspace(380, 780, 2001)
sx = np.interp(lam, C.LAM, C.XBAR)
sy = np.interp(lam, C.LAM, C.YBAR)
sz = np.interp(lam, C.LAM, C.ZBAR)
tt = sx + sy + sz
lx, ly = sx / tt, sy / tt
AREA_LOCUS = poly_area(lx, ly)

fig = plt.figure(figsize=(7.2, 4.2))
gs = fig.add_gridspec(1, 2, width_ratios=[1.12, 1.0], wspace=0.28)

# ==================== (a) 色度图上的三角形 ====================
ax = fig.add_subplot(gs[0])
ax.plot(lx, ly, color="#8d99a6", lw=1.5, zorder=3)
ax.plot([lx[0], lx[-1]], [ly[0], ly[-1]], color="#8d99a6", lw=1.0,
        ls=(0, (3, 2)), zorder=3)

for name, (pts, col, ls) in GAMUTS.items():
    px = [p[0] for p in pts] + [pts[0][0]]
    py = [p[1] for p in pts] + [pts[0][1]]
    ax.plot(px, py, color=col, lw=1.7, ls=ls, zorder=5, label=name)
    ax.fill(px, py, color=col, alpha=0.05, lw=0)

ax.plot([W[0]], [W[1]], "+", ms=9, color=H.DARK, mew=1.8, zorder=7)
ax.text(W[0] + 0.012, W[1] - 0.030, "D65", fontsize=7.6, color=H.DARK,
        ha="left", va="center")

ax.annotate("520 nm\n$y=0.834$", xy=(0.074, 0.834), xytext=(0.185, 0.855),
            fontsize=7.0, color="#5b6b7a", ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color="#5b6b7a", lw=0.8,
                            connectionstyle="arc3,rad=0.15"))
ax.annotate("700 nm\n$(0.7347,\\ 0.2653)$", xy=(0.7347, 0.2653),
            xytext=(0.520, 0.150), fontsize=7.0, color="#5b6b7a", ha="left",
            va="center",
            arrowprops=dict(arrowstyle="->", color="#5b6b7a", lw=0.8,
                            connectionstyle="arc3,rad=-0.2"))
ax.text(0.395, 0.098, "紫线", fontsize=7.0, color="#8e44ad", rotation=21,
        ha="left", va="bottom")

ax.set_xlim(0.0, 0.82)
ax.set_ylim(0.0, 0.90)
ax.set_aspect("equal")
ax.set_xlabel("色度坐标 x")
ax.set_ylabel("色度坐标 y")
ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8])
ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8])
ax.legend(loc="upper right", fontsize=7.6, frameon=True, handlelength=1.6,
          labelspacing=0.25, bbox_to_anchor=(1.0, 1.0))

# ==================== (b) 沿色相方向的边界距离 ====================
ax2 = fig.add_subplot(gs[1])
u0, v0 = uv(*W)


def boundary_dist(pts, ang):
    """从白点沿 ang 方向走到三角形边界的距离（u'v' 单位）。"""
    dx, dy = np.cos(ang), np.sin(ang)
    px = np.array([p[0] for p in pts])
    py = np.array([p[1] for p in pts])
    qu, qv = uv(px, py)
    best = None
    for i in range(3):
        ax_, ay_ = qu[i], qv[i]
        bx_, by_ = qu[(i + 1) % 3], qv[(i + 1) % 3]
        ex, ey = bx_ - ax_, by_ - ay_
        det = dx * ey - dy * ex
        if abs(det) < 1e-12:
            continue
        t = ((ax_ - u0) * ey - (ay_ - v0) * ex) / det
        s = ((ax_ - u0) * dy - (ay_ - v0) * dx) / det
        if t > 0 and -1e-9 <= s <= 1 + 1e-9:
            if best is None or t < best:
                best = t
    return best if best is not None else np.nan


ANG = np.linspace(0, 2 * np.pi, 361)
for name, (pts, col, ls) in GAMUTS.items():
    d = np.array([boundary_dist(pts, a) for a in ANG])
    ax2.plot(np.degrees(ANG), d, color=col, lw=1.9, label=name)

ax2.set_xlim(0, 360)
ax2.set_ylim(0, 0.40)
ax2.set_xticks([0, 60, 120, 180, 240, 300, 360])
ax2.set_xlabel("色相角（°，u'v' 平面，从 +u' 轴起算）")
ax2.set_ylabel("到色域边界的距离（u'v'）")
ax2.legend(loc="upper right", fontsize=7.6, frameon=True, handlelength=1.6,
           labelspacing=0.25, bbox_to_anchor=(1.0, 1.0), ncol=3,
           columnspacing=1.0)
ax2.annotate("绿区", xy=(140, 0.196), xytext=(158, 0.268), fontsize=7.4,
             color=H.GREEN, ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=H.GREEN, lw=0.9,
                             connectionstyle="arc3,rad=-0.2"))
ax2.annotate("蓝区", xy=(266, 0.336), xytext=(226, 0.300), fontsize=7.4,
             color=H.BLUE, ha="center", va="center",
             arrowprops=dict(arrowstyle="->", color=H.BLUE, lw=0.9,
                             connectionstyle="arc3,rad=0.2"))
ax2.annotate("红区", xy=(4, 0.352), xytext=(26, 0.290), fontsize=7.4,
             color=H.RED, ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                             connectionstyle="arc3,rad=-0.2"))

H.save(fig, 2, "f3_gamut_coverage")

print("locus area", round(AREA_LOCUS, 4))
for name, (pts, col, ls) in GAMUTS.items():
    px = np.array([p[0] for p in pts])
    py = np.array([p[1] for p in pts])
    a = poly_area(px, py)
    d = np.array([boundary_dist(pts, t) for t in ANG])
    print(f"{name}: area={a:.4f} rel={a / AREA_LOCUS * 100:.1f}% "
          f"rmin={np.nanmin(d):.4f} rmax={np.nanmax(d):.4f}")
