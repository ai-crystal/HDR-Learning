# -*- coding: utf-8 -*-
"""第 03 章 图 1：等感知差轮廓在 CIE 1931 xy 平面上的形状。

图上每个闭合曲线是 CIE 1976 u'v' 平面上一个半径相同的小圆的映射结果，
用于说明 xy 平面严重不均匀：同样大小的感知差，在绿区被拉成长轴很长的椭圆，
在蓝紫区则被压扁。为便于观察，线条在图上放大了 6 倍。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.path as mpath
import cie1931 as C
from scipy.interpolate import PchipInterpolator

plt = H.plt

Y0 = 0.5           # 固定亮度，只比较色度
R0 = 0.0022        # u'v' 平面上的半径
MAG = 6.0          # 图上放大倍数


def uvp_to_xy(up, vp):
    d = 6 * up - 16 * vp + 12
    return 9 * up / d, 4 * vp / d


def xy_to_uvp(x, y):
    d = -2 * x + 12 * y + 3
    return 4 * x / d, 9 * y / d


# ---- 光谱轨迹（平滑） ----
lam_d = np.linspace(380, 780, 700)
xb = PchipInterpolator(C.LAM, C.XBAR)(lam_d)
yb = PchipInterpolator(C.LAM, C.YBAR)(lam_d)
zb = PchipInterpolator(C.LAM, C.ZBAR)(lam_d)
tot = xb + yb + zb
LX, LY = xb / tot, yb / tot
poly = mpath.Path(np.column_stack([np.concatenate([LX, [LX[0]]]),
                                  np.concatenate([LY, [LY[0]]])]))

fig = plt.figure(figsize=(7.0, 5.4))
ax = fig.add_axes([0.10, 0.13, 0.86, 0.80])

ax.plot(LX, LY, color="#9aa7b4", lw=1.6, zorder=3)
ax.plot([LX[0], LX[-1]], [LY[0], LY[-1]], color="#9aa7b4", lw=1.3,
        ls=(0, (4, 3)), zorder=3)

# ---- 中心点网格 ----
centers = []
for yy in (0.12, 0.22, 0.32, 0.42, 0.52, 0.62):
    for xx in (0.10, 0.17, 0.24, 0.31, 0.38, 0.45, 0.52, 0.59):
        if poly.contains_point((xx, yy)):
            centers.append((xx, yy))

th = np.linspace(0, 2 * np.pi, 120)
for (cx, cy) in centers:
    up, vp = xy_to_uvp(cx, cy)
    ux, vy = uvp_to_xy(up + MAG * R0 * np.cos(th), vp + MAG * R0 * np.sin(th))
    ax.plot(ux, vy, color=H.NAVY, lw=1.0, alpha=0.9, zorder=5)
    ax.plot([cx], [cy], ".", ms=2.6, color=H.RED, zorder=6)

# ---- 选两个位置标注 ----
for (cx, cy, lab, tx, ty) in ((0.315, 0.630, "绿区：椭圆倾斜" + chr(10) + "长轴沿绿-黄方向", 0.556, 0.700),
                              (0.100, 0.120, "蓝紫区：椭圆压扁", 0.245, 0.145)):
    ax.annotate(lab, xy=(cx, cy), xytext=(tx, ty),
                fontsize=7.8, color=H.DARK, ha="center", va="center", zorder=8,
                linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=H.GRAY, lw=1.0),
                bbox=dict(facecolor="white", alpha=0.88, edgecolor="none", pad=1.2))

ax.text(0.630, 0.790, "曲线放大 6 倍", fontsize=7.6, color="#4a5666",
        ha="center", va="center", zorder=8,
        bbox=dict(facecolor="white", alpha=0.85, edgecolor=H.LGRAY,
                  boxstyle="round,pad=0.3"))

ax.set_xlim(0.02, 0.76)
ax.set_ylim(0.02, 0.86)
ax.set_aspect("equal")
ax.set_xlabel("色度坐标 x")
ax.set_ylabel("色度坐标 y")
ax.set_xticks(np.arange(0.0, 0.8, 0.1))
ax.set_yticks(np.arange(0.0, 0.9, 0.1))

H.save(fig, 3, "f1_macadam")
