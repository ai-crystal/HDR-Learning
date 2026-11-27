# -*- coding: utf-8 -*-
"""第 02 章 图 4：黑体轨迹与色温。

(a) 由普朗克公式逐温度积分得到的 xy 轨迹（1700 K 到 25000 K），叠加在 CIE 1931
    色度图上。灰色虚线是等色温线，方向为 CIE 1960 uv 中垂直于轨迹的法向，
    因此它们在 xy 里并不垂直于曲线本身的切线。
(b) 四个温度的黑体相对光谱，圆点标出维恩位移律给出的峰值波长。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C

plt = H.plt

C2 = 1.4388e-2                       # 第二辐射常数 m·K
LAM = C.LAM


def planck(T, lam_nm=LAM):
    l = lam_nm * 1e-9
    return 1.0 / (l ** 5 * (np.exp(C2 / (l * T)) - 1.0))


def planck_xy(T):
    sp = planck(T)
    X = np.trapezoid(sp * C.XBAR, LAM)
    Y = np.trapezoid(sp * C.YBAR, LAM)
    Z = np.trapezoid(sp * C.ZBAR, LAM)
    s = X + Y + Z
    return X / s, Y / s


def xy_to_uv(x, y):
    d = -2 * x + 12 * y + 3
    return 4 * x / d, 6 * y / d


def uv_to_xy(u, v):
    """CIE 1960 uv 的逆变换。"""
    d = 2 * u - 8 * v + 4
    return 3 * u / d, 2 * v / d


def isotherm_normal(T):
    u1, v1 = xy_to_uv(*planck_xy(T * 1.02))
    u2, v2 = xy_to_uv(*planck_xy(T * 0.98))
    du, dv = u1 - u2, v1 - v2
    n = np.hypot(du, dv)
    return -dv / n, du / n


fig = plt.figure(figsize=(7.2, 4.5))
gs = fig.add_gridspec(1, 2, width_ratios=[1.18, 1.0], wspace=0.26)

# ==================== (a) 轨迹与等色温线 ====================
ax = fig.add_subplot(gs[0])

# 光谱轨迹做背景参照
lam_d = np.linspace(380, 780, 600)
sx = np.interp(lam_d, C.LAM, C.XBAR)
sy = np.interp(lam_d, C.LAM, C.YBAR)
sz = np.interp(lam_d, C.LAM, C.ZBAR)
tt = sx + sy + sz
ax.plot(sx / tt, sy / tt, color="#c8d0d8", lw=1.3, zorder=1)
ax.plot([sx[0] / tt[0], sx[-1] / tt[-1]], [sy[0] / tt[0], sy[-1] / tt[-1]],
        color="#e0d3e8", lw=1.1, ls=(0, (3, 2)), zorder=1)

T_GRID = np.concatenate([np.linspace(1700, 4000, 140),
                         np.linspace(4000, 25000, 200)])
loc = np.array([planck_xy(t) for t in T_GRID])
ax.plot(loc[:, 0], loc[:, 1], color="#1b1f26", lw=2.2, zorder=6)

MARKS = [2000, 2856, 6500, 10000]
LAB = {2000: (0.006, 0.012, "left", "bottom"),
       2856: (-0.010, 0.014, "right", "bottom"),
       6500: (-0.014, 0.018, "right", "bottom"),
       10000: (0.006, -0.020, "left", "top")}
XMIN, XMAX, YMIN, YMAX = 0.245, 0.545, 0.225, 0.475
for T in MARKS:
    x0, y0 = planck_xy(T)
    u0, v0 = xy_to_uv(x0, y0)
    nu, nv = isotherm_normal(T)
    ts = np.linspace(-0.045, 0.045, 301)
    px, py = uv_to_xy(u0 + ts * nu, v0 + ts * nv)
    inside = (px > XMIN + 0.002) & (px < XMAX - 0.002) &              (py > YMIN + 0.002) & (py < YMAX - 0.002)
    ax.plot(px, py, color="#7f8d9b", lw=1.1, ls=(0, (3.0, 2.2)), zorder=4)
    ax.plot([x0], [y0], "o", ms=5.5, mfc="white", mec="#1b1f26", mew=1.4,
            zorder=8)
    dx, dy, ha, va = LAB[T]
    ax.text(x0 + dx, y0 + dy, f"{T} K", fontsize=7.2, color="#3d4a57",
            ha=ha, va=va, zorder=9,
            bbox=dict(facecolor="white", alpha=0.80, edgecolor="none", pad=0.5))

ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_aspect("equal")
ax.set_xlabel("色度坐标 x")
ax.set_ylabel("色度坐标 y")
ax.set_xticks([0.25, 0.30, 0.35, 0.40, 0.45, 0.50])
ax.set_yticks([0.25, 0.30, 0.35, 0.40, 0.45])
ax.text(0.352, 0.452, "普朗克轨迹", fontsize=7.6, color="#1b1f26", ha="left",
        va="center")

# ==================== (b) 四个温度的光谱 ====================
ax2 = fig.add_subplot(gs[1])
COLORS = {2000: H.RED, 3000: H.ORANGE, 6500: "#b8912f", 10000: H.BLUE}
m = (LAM >= 380) & (LAM <= 780)
for T in (2000, 3000, 6500, 10000):
    spd = planck(T)[m]
    spd = spd / spd.max()
    ax2.plot(LAM[m], spd, color=COLORS[T], lw=2.0, label=f"{T} K")
    lam_max = 2.8978e6 / T
    if 380 <= lam_max <= 780:
        i = int(np.argmin(np.abs(LAM[m] - lam_max)))
        ax2.plot([lam_max], [spd[i]], "o", ms=4.5, mfc="white",
                 mec=COLORS[T], mew=1.4, zorder=6)

ax2.annotate("峰值：维恩位移律\n$\\lambda_{max}=2.8978\\times10^6/T$",
             xy=(447, 1.0), xytext=(486, 1.10), fontsize=7.2, color="#8a6a12",
             ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color="#a8842a", lw=0.9,
                             connectionstyle="arc3,rad=0.2"))
ax2.set_xlim(380, 780)
ax2.set_ylim(0, 1.22)
ax2.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
ax2.set_xlabel("波长 λ（nm）")
ax2.set_ylabel("相对光谱功率（各自归一）")
ax2.legend(fontsize=8.0, loc="lower center", bbox_to_anchor=(0.5, 1.0),
           ncol=4, columnspacing=1.1, handlelength=1.3, frameon=False)

H.save(fig, 2, "f4_planckian")

for T in (2000, 3000, 6500, 10000):
    x_, y_ = planck_xy(T)
    print(f"{T} K: xy=({x_:.4f}, {y_:.4f})  peak={2.8978e6/T:.0f} nm")
print("2856 K:", np.round(planck_xy(2856), 4))
