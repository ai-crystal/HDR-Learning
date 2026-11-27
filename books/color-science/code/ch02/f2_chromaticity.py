# -*- coding: utf-8 -*-
"""第 02 章 图 2：CIE 1931 色度图（真实光谱轨迹 + 三种色域三角 + 五个白点）。

光谱轨迹由 CIE 1931 2° 色匹配函数逐波长计算；内部颜色按 sRGB 归一化渲染，
仅用于示意色相走势，不代表该点在实际显示设备上的准确外观。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.path as mpath
from matplotlib.lines import Line2D
import cie1931 as C
from scipy.interpolate import PchipInterpolator

plt = H.plt


def dense_locus(n=1200):
    """用单调三次插值把 5 nm 色匹配函数加密，得到平滑的光谱轨迹。"""
    lam_d = np.linspace(380.0, 780.0, n)
    xb = PchipInterpolator(C.LAM, C.XBAR)(lam_d)
    yb = PchipInterpolator(C.LAM, C.YBAR)(lam_d)
    zb = PchipInterpolator(C.LAM, C.ZBAR)(lam_d)
    tot = xb + yb + zb
    return lam_d, xb / tot, yb / tot

fig = plt.figure(figsize=(7.2, 5.6))
ax = fig.add_axes([0.085, 0.145, 0.88, 0.82])

# ---------- 1. 用 sRGB 渲染马蹄形内部 ----------
nx, ny = 1200, 1350
gx = np.linspace(-0.08, 0.85, nx)
gy = np.linspace(-0.05, 0.92, ny)
GX, GY = np.meshgrid(gx, gy)
valid = GY > 0.004
s = np.where(valid, GY, 1.0)
Xs = np.where(valid, GX / s, 0.0)
Zs = np.where(valid, (1.0 - GX - GY) / s, 0.0)
lin = C.xyz_to_linear_srgb(Xs, np.where(valid, 1.0, 0.0), Zs)
lin = np.clip(lin, 0.0, None)
m = lin.max(axis=-1, keepdims=True)
m[m < 1e-9] = 1.0
lin = lin / m
rgb = np.where(lin <= 0.0031308, 12.92 * lin,
               1.055 * np.power(lin, 1 / 2.4) - 0.055)

_ld, _lx, _ly = dense_locus()
poly = mpath.Path(np.column_stack([np.concatenate([_lx, [_lx[0]]]),
                                   np.concatenate([_ly, [_ly[0]]])]))
inside = poly.contains_points(np.column_stack([GX.ravel(), GY.ravel()])).reshape(GX.shape)
img = np.where((inside & valid)[..., None], rgb, np.nan)
ax.imshow(img, extent=[gx[0], gx[-1], gy[0], gy[-1]], origin="lower",
          interpolation="nearest", aspect="auto", zorder=1)

# ---------- 2. 光谱轨迹与紫线 ----------
lam, sx, sy = dense_locus()
ax.plot(sx, sy, color="#1b1f26", lw=2.6, zorder=5, solid_capstyle="round")
ax.plot([sx[0], sx[-1]], [sy[0], sy[-1]], color="#1b1f26", lw=1.9,
        ls=(0, (5, 3)), zorder=5)

LAB_TICKS = [460, 500, 540, 580, 620, 700]
for wl in range(400, 701, 10):
    i = int(np.argmin(np.abs(lam - wl)))
    px, py = sx[i], sy[i]
    vx, vy = px - 1 / 3.0, py - 1 / 3.0
    n = np.hypot(vx, vy)
    vx, vy = vx / n, vy / n
    long_tick = wl in LAB_TICKS
    ax.plot([px, px + vx * (0.026 if long_tick else 0.015)],
            [py, py + vy * (0.026 if long_tick else 0.015)],
            color="#1b1f26", lw=1.0, zorder=6)
    if long_tick:
        ax.text(px + vx * 0.062, py + vy * 0.062, str(wl), fontsize=7.2,
                color="#1b1f26", ha="center", va="center", zorder=7,
                bbox=dict(facecolor="white", alpha=0.62, edgecolor="none", pad=0.6))

# ---------- 3. 色域三角 ----------
GAMUTS = [
    ("sRGB / BT.709", [(0.640, 0.330), (0.300, 0.600), (0.150, 0.060)], H.NAVY, "-"),
    ("DCI-P3", [(0.680, 0.320), (0.265, 0.690), (0.150, 0.060)], H.TEAL, "--"),
    ("BT.2020", [(0.708, 0.292), (0.170, 0.797), (0.131, 0.046)], H.PURPLE, "-."),
]
for name, pts, col, ls in GAMUTS:
    xs = [p[0] for p in pts] + [pts[0][0]]
    ys = [p[1] for p in pts] + [pts[0][1]]
    ax.plot(xs, ys, color=col, lw=1.8, ls=ls, zorder=8)

# ---------- 4. 白点（形状区分，坐标见正文） ----------
WPS = [("D65", 0.3127, 0.3290, "*", 13, "#f7d774"),
       ("A", 0.4476, 0.4074, "o", 7.0, "white"),
       ("D50", 0.3457, 0.3585, "s", 6.5, "white"),
       ("E", 0.3333, 0.3333, "D", 6.0, "white"),
       ("DCI", 0.3140, 0.3510, "v", 7.0, "white")]
for name, x0, y0, mk, ms, fc in WPS:
    ax.plot([x0], [y0], marker=mk, ms=ms, mfc=fc, mec="#111111", mew=1.1, zorder=10)

# ---------- 5. 读图提示（全部放在马蹄之外） ----------
ax.text(0.560, 0.815, "马蹄之外" + chr(10) + "没有对应的光", fontsize=7.8, color=H.RED,
        ha="center", va="center", zorder=11, linespacing=1.4,
        bbox=dict(facecolor="white", alpha=0.85, edgecolor=H.RED,
                  boxstyle="round,pad=0.34", lw=0.9))
ax.annotate("", xy=(0.480, 0.560), xytext=(0.545, 0.760),
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.1), zorder=11)
ax.annotate("越靠边沿越饱和", xy=(0.598, 0.392), xytext=(0.700, 0.545),
            fontsize=7.8, color="#111111", ha="center", va="center", zorder=11,
            arrowprops=dict(arrowstyle="->", color="#111111", lw=1.0),
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="none", pad=1.0))
ax.text(0.268, 0.028, "紫线（非单波长）", fontsize=7.2, color="#111111",
        rotation=15, ha="center", va="center", zorder=11,
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="none", pad=0.6))

handles = [
    Line2D([], [], color="#1b1f26", lw=2.4, label="光谱轨迹"),
    Line2D([], [], color="#1b1f26", lw=1.8, ls=(0, (5, 3)), label="紫线"),
] + [Line2D([], [], color=col, lw=1.8, ls=ls, label="色域三角形：" + name)
     for name, _, col, ls in GAMUTS] + [
    Line2D([], [], marker="*", color="none", mfc="#f7d774", mec="#111111", ms=11,
           label="白点 D65"),
    Line2D([], [], marker="o", color="none", mfc="white", mec="#111111", ms=7,
           label="白点 A"),
    Line2D([], [], marker="s", color="none", mfc="white", mec="#111111", ms=6,
           label="白点 D50"),
    Line2D([], [], marker="D", color="none", mfc="white", mec="#111111", ms=6,
           label="白点 E"),
    Line2D([], [], marker="v", color="none", mfc="white", mec="#111111", ms=7,
           label="白点 DCI"),
]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.075),
          ncol=4, fontsize=7.4, frameon=False, columnspacing=1.3, handlelength=1.8)

ax.set_xlim(-0.06, 0.80)
ax.set_ylim(-0.04, 0.90)
ax.set_aspect("equal")
ax.set_xlabel("色度坐标 x")
ax.set_ylabel("色度坐标 y")
ax.set_xticks(np.arange(0, 0.85, 0.1))
ax.set_yticks(np.arange(0, 0.95, 0.1))
ax.grid(color="#e2e8ee", lw=0.6, zorder=0)

H.save(fig, 2, "f2_chromaticity")
