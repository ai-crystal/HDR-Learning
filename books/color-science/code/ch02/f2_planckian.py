# -*- coding: utf-8 -*-
"""第 02 章 图 2：黑体轨迹与相关色温。

左：由普朗克公式逐温度计算黑体光谱，再用 CIE 1931 2° 观察者积分得到 xy 轨迹，
    等色温线按 CIE 1960 uv 中垂直于轨迹的方向绘制。
右：四个温度下的黑体相对光谱功率（在可见光范围内各自归一）。
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

C2 = 1.4388e-2                       # 第二辐射常数，m·K
LAM = np.linspace(360.0, 830.0, 941)
XB = PchipInterpolator(C.LAM, C.XBAR)(LAM)
YB = PchipInterpolator(C.LAM, C.YBAR)(LAM)
ZB = PchipInterpolator(C.LAM, C.ZBAR)(LAM)


def planck(T, lam_nm=LAM):
    l = lam_nm * 1e-9
    return 1.0 / (l ** 5 * (np.exp(C2 / (l * T)) - 1.0))


def planck_xy(T):
    X = np.trapezoid(planck(T) * XB, LAM)
    Y = np.trapezoid(planck(T) * YB, LAM)
    Z = np.trapezoid(planck(T) * ZB, LAM)
    s = X + Y + Z
    return X / s, Y / s


def xy_to_uv(x, y):
    d = -2 * x + 12 * y + 3
    return 4 * x / d, 6 * y / d


def uv_to_xy(u, v):
    d = 6 * u - 16 * v + 12
    return 9 * u / d, 4 * v / d


def isotherm_normal(T):
    """在 1960 uv 中取轨迹切向的法向，返回单位向量。"""
    u1, v1 = xy_to_uv(*planck_xy(T * 1.02))
    u2, v2 = xy_to_uv(*planck_xy(T * 0.98))
    du, dv = u1 - u2, v1 - v2
    n = np.hypot(du, dv)
    return -dv / n, du / n


fig = plt.figure(figsize=(7.2, 4.5))
gs = fig.add_gridspec(1, 2, width_ratios=[1.25, 1.0], wspace=0.26)

# ==================== 左：轨迹与等色温线 ====================
ax = fig.add_subplot(gs[0])

T_GRID = np.concatenate([np.linspace(1700, 4000, 120), np.linspace(4000, 20000, 160)])
locus = np.array([planck_xy(t) for t in T_GRID])
ax.plot(locus[:, 0], locus[:, 1], color="#1b1f26", lw=2.2, zorder=6)

# 光谱轨迹做参照
lam_d = np.linspace(380, 780, 600)
sx = PchipInterpolator(C.LAM, C.XBAR)(lam_d)
sy = PchipInterpolator(C.LAM, C.YBAR)(lam_d)
sz = PchipInterpolator(C.LAM, C.ZBAR)(lam_d)
tt = sx + sy + sz
ax.plot(sx / tt, sy / tt, color="#b8c2cc", lw=1.2, zorder=2)

# ---- 温度点、等色温线与沿轨迹的标注 ----
MARKS = [2000, 3000, 6500, 10000]
for T in MARKS:
    x0, y0 = planck_xy(T)
    u0, v0 = xy_to_uv(x0, y0)
    nu, nv = isotherm_normal(T)
    ts = np.linspace(-0.030, 0.030, 2)
    px, py = uv_to_xy(u0 + ts * nu, v0 + ts * nv)
    ax.plot(px, py, color="#8d99a6", lw=1.1, ls=(0, (2.5, 2)), zorder=4)
    ax.plot([x0], [y0], "o", ms=6.0, mfc="white", mec="#1b1f26", mew=1.5, zorder=8)

    # 沿轨迹法向放置文字，避免引线横穿曲线
    xa, ya = planck_xy(T * 1.04)
    xb, yb = planck_xy(T * 0.96)
    tx, ty = xa - xb, ya - yb
    norm = np.hypot(tx, ty)
    tx, ty = tx / norm, ty / norm
    mx, my = -ty, tx
    if my < 0:
        mx, my = -mx, -my
    ax.plot([x0, x0 + 0.013 * mx], [y0, y0 + 0.013 * my], color="#1b1f26",
            lw=1.0, zorder=7)
    ang = np.degrees(np.arctan2(ty, tx))
    if ang > 90:
        ang -= 180
    if ang < -90:
        ang += 180
    ax.text(x0 + 0.027 * mx, y0 + 0.027 * my, f"{T} K", fontsize=7.8,
            color="#1b1f26", rotation=ang, rotation_mode="anchor",
            ha="center", va="center", zorder=9,
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="none", pad=0.8))

ax.set_xlim(0.232, 0.578)
ax.set_ylim(0.248, 0.462)
ax.set_aspect("equal")
ax.set_xlabel("色度坐标 x")
ax.set_ylabel("色度坐标 y")
ax.set_xticks([0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55])
ax.set_yticks([0.25, 0.30, 0.35, 0.40, 0.45])

# ==================== 右：四个温度的光谱 ====================
ax2 = fig.add_subplot(gs[1])
COLORS = {2000: H.RED, 3000: H.ORANGE, 6500: "#c8a24a", 10000: H.BLUE}
for T in (2000, 3000, 6500, 10000):
    spd = planck(T)
    m = (LAM >= 380) & (LAM <= 780)
    spd = spd / spd[m].max()
    ax2.plot(LAM[m], spd[m], color=COLORS[T], lw=2.0, label=f"{T} K")
    lam_max = 2.8978e6 / T
    if 380 <= lam_max <= 780:
        i = int(np.argmin(np.abs(LAM - lam_max)))
        ax2.plot([lam_max], [spd[i]], "o", ms=4.5, color=COLORS[T], zorder=6)

ax2.set_xlim(380, 780)
ax2.set_ylim(0, 1.16)
ax2.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
ax2.set_xlabel("波长 λ（nm）")
ax2.set_ylabel("相对光谱功率（各自归一）")
ax2.legend(fontsize=8.2, loc="lower center", bbox_to_anchor=(0.5, 1.0),
           ncol=4, columnspacing=1.2, handlelength=1.3, frameon=False)
H.save(fig, 2, "f2_planckian")
print("2000K xy", np.round(planck_xy(2000), 4))
print("3000K xy", np.round(planck_xy(3000), 4))
print("6500K xy", np.round(planck_xy(6500), 4))
print("10000K xy", np.round(planck_xy(10000), 4))
