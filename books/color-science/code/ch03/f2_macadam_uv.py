# -*- coding: utf-8 -*-
"""第 03 章 图 2：xy 到 u'v' 映射的残余失真。

左图沿光谱轨迹取样，逐点计算映射 xy -> u'v' 的雅可比矩阵，
画奇异值之比（圆变椭圆后的长短轴比）与行列式绝对值（面积缩放）。
右图在四个位置取同半径的小圆，映射到 u'v' 后把像归一化到同一中心，
与同尺寸正圆比较，直观看椭圆的方向与轴比。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C
from scipy.interpolate import PchipInterpolator

plt = H.plt
NAVY, ORANGE, TEAL, RED, GRAY = H.NAVY, H.ORANGE, H.TEAL, H.RED, H.GRAY


def xy_to_uvp(x, y):
    d = -2.0 * x + 12.0 * y + 3.0
    return 4.0 * x / d, 9.0 * y / d


def jac_uv(x, y, h=1e-6):
    j = np.zeros((2, 2))
    for i, (dx, dy) in enumerate([(h, 0.0), (0.0, h)]):
        u1, v1 = xy_to_uvp(x + dx, y + dy)
        u0, v0 = xy_to_uvp(x - dx, y - dy)
        j[0, i] = (u1 - u0) / (2 * h)
        j[1, i] = (v1 - v0) / (2 * h)
    return j


# ---------- 左图数据：沿光谱轨迹 ----------
lam = np.arange(380.0, 701.0, 2.0)
xb = PchipInterpolator(C.LAM, C.XBAR)(lam)
yb = PchipInterpolator(C.LAM, C.YBAR)(lam)
zb = PchipInterpolator(C.LAM, C.ZBAR)(lam)
tot = xb + yb + zb
lx, ly = xb / tot, yb / tot

asp, det = [], []
for xi, yi in zip(lx, ly):
    j = jac_uv(xi, yi)
    s = np.linalg.svd(j, compute_uv=False)
    asp.append(s[0] / s[1])
    det.append(abs(np.linalg.det(j)))
asp = np.array(asp)
det = np.array(det)

fig = plt.figure(figsize=(7.8, 3.3))
ax = fig.add_axes([0.072, 0.170, 0.385, 0.790])
axb = ax.twinx()
ax2 = fig.add_axes([0.590, 0.170, 0.235, 0.790])

ax.plot(lam, asp, color=NAVY, lw=2.0, zorder=5)
ax.set_xlabel("波长 (nm)", labelpad=2)
ax.set_ylabel("长短轴比", color=NAVY, labelpad=2)
ax.tick_params(axis="y", labelcolor=NAVY, labelsize=8)
ax.tick_params(axis="x", labelsize=8)
ax.set_ylim(0.9, 4.45)
ax.set_xlim(380, 700)
ax.set_yticks([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])

axb.plot(lam, det, color=ORANGE, lw=1.6, ls=(0, (5, 2)), zorder=4)
axb.set_yscale("log")
axb.set_ylabel("面积缩放（对数轴）", color=ORANGE, labelpad=4, fontsize=9.0)
axb.tick_params(axis="y", labelcolor=ORANGE, labelsize=7.5)
axb.set_ylim(0.03, 16)

ax.axhline(1.0, color=GRAY, lw=0.9, ls=(0, (3, 3)), zorder=2)
ax.text(390, 1.10, "完全均匀时的 1.0", fontsize=7.0, color="#4a5666",
        ha="left", va="bottom")
ax.annotate("绿区轴比\n接近 2", xy=(528, 2.03), xytext=(566, 3.02),
            fontsize=7.2, color=H.DARK, ha="center", va="center", linespacing=1.5,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.9),
            bbox=dict(facecolor="white", alpha=0.9, edgecolor="none", pad=1.4))
ax.annotate("红端轴比\n接近 3.8", xy=(684, 3.78), xytext=(646, 2.38),
            fontsize=7.2, color=H.DARK, ha="center", va="center", linespacing=1.5,
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.9),
            bbox=dict(facecolor="white", alpha=0.9, edgecolor="none", pad=1.4))
ax.text(390, 4.32, "实线 轴比　虚线 面积缩放", fontsize=7.4, color="#2c3e50",
        ha="left", va="center",
        bbox=dict(facecolor="white", alpha=0.9, edgecolor=H.LGRAY,
                  boxstyle="round,pad=0.32"))

# ---------- 右图：四个位置小圆的像 ----------
SITES = [(0.640, 0.330, "红", RED),
         (0.150, 0.060, "蓝", NAVY),
         (0.225, 0.330, "青", TEAL),
         (0.313, 0.329, "白", H.PURPLE)]
R0 = 0.010
RR = 0.0175
th = np.linspace(0, 2 * np.pi, 240)
tx, ty = np.cos(th), np.sin(th)
ax2.plot(RR * tx, RR * ty, color=GRAY, lw=1.1, ls=(0, (3, 3)), zorder=3)

rows = []
for (cx, cy, name, col) in SITES:
    px = cx + R0 * tx
    py = cy + R0 * ty
    u, v = xy_to_uvp(px, py)
    u = u - u.mean()
    v = v - v.mean()
    scale = RR / np.sqrt((u ** 2 + v ** 2).mean())
    u, v = u * scale, v * scale
    ax2.plot(u, v, color=col, lw=1.6, zorder=6)
    j = jac_uv(cx, cy)
    s = np.linalg.svd(j, compute_uv=False)
    rows.append((name, s[0] / s[1], col))

ax2.set_aspect("equal")
ax2.set_xlim(-0.0255, 0.0255)
ax2.set_ylim(-0.0255, 0.0255)
ax2.set_xlabel(r"$\Delta u'$", labelpad=1)
ax2.set_ylabel(r"$\Delta v'$", labelpad=1)
ax2.set_xticks([-0.02, 0.0, 0.02])
ax2.set_yticks([-0.02, 0.0, 0.02])
ax2.set_xticklabels(["-0.02", "0", "0.02"])
ax2.set_yticklabels(["-0.02", "0", "0.02"])
ax2.tick_params(axis="both", labelsize=8)
ax2.text(0.0, 0.0232, "灰虚线为同尺寸正圆", fontsize=6.9, color="#2c3e50",
         ha="center", va="center",
         bbox=dict(facecolor="white", alpha=0.88, edgecolor="none", pad=0.8))

# ---------- 轴比文字块 ----------
fig.text(0.862, 0.880, "小圆在 $u'v'$ 里的像", fontsize=7.6, color="#2c3e50",
         ha="left", va="top")
fig.text(0.862, 0.800, "长短轴比", fontsize=7.6, color="#2c3e50",
         ha="left", va="top")
for i, (nm, av, cc) in enumerate(rows):
    fig.text(0.862, 0.705 - i * 0.115, f"{nm}    {av:.1f} : 1", fontsize=7.6,
             color=cc, ha="left", va="top")

H.save(fig, 3, "f2_macadam_uv")
for name, a, col in rows:
    print(f"{name}: 轴比 {a:.2f}")
print("轴比范围 %.2f - %.2f；面积缩放 %.3f - %.2f"
      % (asp.min(), asp.max(), det.min(), det.max()))
