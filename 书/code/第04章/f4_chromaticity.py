# -*- coding: utf-8 -*-
"""第 04 章 图 4：CIE 1931 马蹄形色度图（光谱轨迹、白点、普朗克轨迹、标色点）。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.path as mpath
from matplotlib.lines import Line2D
import hdrfig as H
import cie1931 as C

plt = H.plt


def planckian(T):
    """黑体（普朗克）轨迹 (x,y) 近似：Kim et al. 分段拟合，T 单位 K。"""
    x = np.where(
        T < 4000,
        -0.2661239e9 / T ** 3 - 0.2343589e6 / T ** 2 + 0.8776956e3 / T + 0.179910,
        -3.0258469e9 / T ** 3 + 2.1070379e6 / T ** 2 + 0.2226347e3 / T + 0.240390)
    y = np.where(
        T < 2222,
        -1.1063814 * x ** 3 - 1.34811020 * x ** 2 + 2.18555832 * x - 0.20219683,
        np.where(T < 4000,
                 -0.9549476 * x ** 3 - 1.37418593 * x ** 2 + 2.09137015 * x - 0.16748867,
                 3.0817580 * x ** 3 - 5.87338670 * x ** 2 + 3.75112997 * x - 0.37001483))
    return x, y


fig = plt.figure(figsize=(7.2, 5.8))
ax = fig.add_axes([0.08, 0.14, 0.88, 0.80])
ax.set_title("CIE 1931 色度图：一张“颜色地图”", pad=12)

# ---------- 1. 用真实颜色填充马蹄形内部 ----------
nx, ny = 760, 820
gx = np.linspace(-0.09, 0.90, nx)
gy = np.linspace(-0.07, 0.98, ny)
GX, GY = np.meshgrid(gx, gy)
valid = GY > 0.015
Xs = np.where(valid, GX / np.where(valid, GY, 1), 0.0)
Zs = np.where(valid, (1 - GX - GY) / np.where(valid, GY, 1), 0.0)
RGB = C.xyz_to_srgb01(Xs, np.where(valid, 1.0, 0.0), Zs)

poly_x, poly_y = C.horseshoe_outline()
poly = mpath.Path(np.column_stack([poly_x, poly_y]))
inside = poly.contains_points(np.column_stack([GX.ravel(), GY.ravel()])).reshape(GX.shape)
img = np.where((inside & valid)[..., None], RGB, np.nan)
ax.imshow(img, extent=[gx[0], gx[-1], gy[0], gy[-1]], origin="lower",
          interpolation="nearest", aspect="auto", zorder=1)

# ---------- 2. 光谱轨迹与波长刻度 ----------
lam, sx, sy = C.spectral_locus()
ax.plot(sx, sy, color="#20242b", lw=2.6, zorder=4, solid_capstyle="round")
ax.plot([sx[0], sx[-1]], [sy[0], sy[-1]], color="#20242b", lw=1.8,
        ls=(0, (5, 3)), zorder=4)

TICKS = [380, 460, 500, 520, 540, 560, 580, 600, 620, 700]
for wl in [380, 420, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570,
           580, 590, 600, 610, 620, 650, 700, 780]:
    i = int(np.argmin(np.abs(lam - wl)))
    px, py = sx[i], sy[i]
    vx, vy = px - 1 / 3, py - 1 / 3
    n = np.hypot(vx, vy)
    vx, vy = vx / n, vy / n
    ax.plot([px, px + vx * 0.020], [py, py + vy * 0.020], color="#20242b",
            lw=1.0, zorder=5)
    if wl in TICKS:
        ax.text(px + vx * 0.048, py + vy * 0.048, str(wl), fontsize=7.2,
                color="#20242b", ha="center", va="center", zorder=6,
                bbox=dict(facecolor="white", alpha=0.6, edgecolor="none", pad=0.6))
for wl in (460, 520, 580, 700):
    i = int(np.argmin(np.abs(lam - wl)))
    ax.plot([sx[i]], [sy[i]], "o", ms=3.4, mfc="white", mec="#20242b", mew=1.0, zorder=6)

# ---------- 3. 黑体（普朗克）轨迹 ----------
T = np.concatenate([np.linspace(1667, 4000, 260), np.linspace(4000, 25000, 320)])
bx, by = planckian(T)
ax.plot(bx, by, color="#20242b", lw=1.3, ls=":", zorder=5)
for Tt, tag, xyt in ((2000, "2000 K", (0.560, 0.356)),
                     (3000, "3000 K", (0.448, 0.345)),
                     (10000, "10000 K", (0.232, 0.232))):
    i = int(np.argmin(np.abs(T - Tt)))
    ax.plot([bx[i]], [by[i]], ".", ms=4.5, color="#20242b", zorder=6)
    ax.annotate(tag, xy=(bx[i], by[i]), xytext=xyt, fontsize=7.0, color="#20242b",
                ha="center", va="center", zorder=7,
                arrowprops=dict(arrowstyle="-", color="#20242b", lw=0.8),
                bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=0.8))

# ---------- 4. 白点 ----------
ax.plot(*C.WHITE_POINTS["D65"], marker="o", ms=9.5, mfc="white", mec="#111111",
        mew=2.0, zorder=8)
ax.annotate("白点 D65：x = 0.3127, y = 0.3290\n（A / D50 / DCI 等其他白点位置各不相同）",
            xy=C.WHITE_POINTS["D65"], xytext=(0.630, 0.128), fontsize=7.8,
            color="#111111", fontweight="bold", ha="center", va="center", zorder=9,
            arrowprops=dict(arrowstyle="->", color="#111111", lw=1.2,
                            connectionstyle="arc3,rad=0.12"),
            bbox=dict(facecolor="white", alpha=0.9, edgecolor=H.LGRAY,
                      boxstyle="round,pad=0.32"))
for name in ("A", "D50", "DCI"):
    px, py = C.WHITE_POINTS[name]
    ax.plot([px], [py], marker="s", ms=5, mfc="#ffe9a8", mec="#6b5a20", mew=1.0, zorder=7)
ax.text(0.630, 0.042, "注意：色度图不含量度（亮度）\nx、y 也不是感知均匀坐标",
        fontsize=7.4, color=H.NAVY, ha="center", va="center", zorder=9,
        bbox=dict(facecolor="white", alpha=0.88, edgecolor="none", pad=0.7))

# ---------- 5. sRGB 三角形与标色点 ----------
prim = [(0.6400, 0.3300, "红 R"), (0.3000, 0.6000, "绿 G"), (0.1500, 0.0600, "蓝 B")]
pxs = [p[0] for p in prim] + [prim[0][0]]
pys = [p[1] for p in prim] + [prim[0][1]]
ax.plot(pxs, pys, color=H.NAVY, lw=1.7, ls="--", zorder=7)
laboff = {0: (0.0, -0.055), 1: (0.0, 0.052), 2: (0.0, 0.052)}
for k, (x0, y0, lab) in enumerate(prim):
    ax.plot([x0], [y0], marker="o", ms=6.5, mfc="white", mec=H.NAVY, mew=1.8, zorder=8)
    ax.text(x0 + laboff[k][0], y0 + laboff[k][1], "sRGB " + lab, fontsize=7.0,
            color=H.NAVY, fontweight="bold", ha="center", va="center", zorder=8,
            bbox=dict(facecolor="white", alpha=0.75, edgecolor="none", pad=0.5))

for wl, col in ((620, "#8e1a10"), (545, "#0f7a34"), (465, "#123f8c")):
    i = int(np.argmin(np.abs(lam - wl)))
    ax.plot([sx[i]], [sy[i]], marker="^", ms=6.5, mfc="white", mec=col, mew=1.7, zorder=8)

# ---------- 6. 读图提示（都放在马蹄之外，不遮颜色） ----------
ax.annotate("光谱轨迹：单波长纯色，最饱和", xy=(0.230, 0.754), xytext=(0.60, 0.845),
            fontsize=8.0, color="#20242b", fontweight="bold", ha="center", zorder=9,
            arrowprops=dict(arrowstyle="->", color="#20242b", lw=1.1),
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=0.8))
ax.text(0.68, 0.700, "马蹄之外\n不存在颜色\n（没有对应的光）", fontsize=8.0,
        color=H.RED, fontweight="bold", ha="center", va="center", zorder=9,
        bbox=dict(facecolor="white", alpha=0.88, edgecolor=H.RED,
                  boxstyle="round,pad=0.34", lw=0.9))
ax.annotate("越靠边沿越饱和\n越靠中间越接近白", xy=(0.512, 0.487), xytext=(0.655, 0.505),
            fontsize=8.0, color="#20242b", fontweight="bold", ha="center", va="center",
            zorder=9, arrowprops=dict(arrowstyle="->", color="#20242b", lw=1.1),
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=0.8))
ax.text(0.345, 0.058, "紫线：红紫混合\n（非单波长）", fontsize=7.4, color="#20242b",
        ha="center", va="center", rotation=13, zorder=9,
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="none", pad=0.6))
ax.annotate("其他白点：A（白炽灯）/ D50（印刷）/ DCI",
            xy=(0.3457, 0.3585), xytext=(0.400, 0.432), fontsize=7.0, color="#5a4a10",
            fontweight="bold", ha="center", va="center", zorder=9,
            arrowprops=dict(arrowstyle="->", color="#8a7333", lw=0.9),
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="none", pad=0.6))

# 图例放到坐标区外下方，避免遮挡
handles = [
    Line2D([], [], color="#20242b", lw=2.4, label="光谱轨迹（单波长）"),
    Line2D([], [], color="#20242b", lw=1.8, ls=(0, (5, 3)), label="紫线"),
    Line2D([], [], color="#20242b", lw=1.3, ls=":", label="黑体（普朗克）轨迹"),
    Line2D([], [], color=H.NAVY, lw=1.7, ls="--", label="sRGB 三角形"),
    Line2D([], [], marker="o", color="none", mfc="white", mec="#111111", ms=8, label="白点 D65"),
    Line2D([], [], marker="s", color="none", mfc="#ffe9a8", mec="#6b5a20", ms=6, label="其他白点"),
    Line2D([], [], marker="^", color="none", mfc="white", mec="#8e1a10", ms=6, label="单波长标色点"),
    Line2D([], [], marker="o", color="none", mfc="white", mec=H.NAVY, ms=6, label="sRGB 基色"),
]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.115),
          ncol=4, fontsize=7.4, frameon=False, columnspacing=1.1, handlelength=1.6)

ax.set_xlim(-0.06, 0.82)
ax.set_ylim(-0.06, 0.92)
ax.set_aspect("equal")
ax.set_xlabel("色度坐标 x", fontsize=10.5)
ax.set_ylabel("色度坐标 y", fontsize=10.5)
ax.set_xticks(np.arange(0, 0.9, 0.1))
ax.set_yticks(np.arange(0, 1.0, 0.1))
ax.grid(color="#dde3ea", lw=0.6, zorder=0)

H.save(fig, 4, "f4_chromaticity")
