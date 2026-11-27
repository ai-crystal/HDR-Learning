# -*- coding: utf-8 -*-
"""第 02 章 图 5：相关色温的度量与 McCamy 近似的适用范围。

(a) CIE 1960 uv 平面：普朗克轨迹、在其上垂直于轨迹的等温线，以及同一点沿法向
    偏移 ±0.006 得到的两条"同 CCT 不同 Duv"的色。Duv > 0 偏向绿侧，
    Duv < 0 偏向品红侧，这个符号约定来自轨迹上方为绿。
(b) McCamy 多项式近似的误差：把黑体轨迹上的点代入多项式，与轨迹本身的温度比较。
    2856 K 到 7000 K 之间误差在 3 K 以内，10000 K 处偏 126 K，20000 K 处偏 2900 K。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C

plt = H.plt

C2 = 1.4388e-2


def planck(T, lam_nm=C.LAM):
    l = lam_nm * 1e-9
    return 1.0 / (l ** 5 * (np.exp(C2 / (l * T)) - 1.0))


def planck_xy(T):
    sp = planck(T)
    X = np.trapezoid(sp * C.XBAR, C.LAM)
    Y = np.trapezoid(sp * C.YBAR, C.LAM)
    Z = np.trapezoid(sp * C.ZBAR, C.LAM)
    s = X + Y + Z
    return X / s, Y / s


def xy_to_uv(x, y):
    d = -2 * x + 12 * y + 3
    return 4 * x / d, 6 * y / d


def uv_to_xy(u, v):
    d = 2 * u - 8 * v + 4
    return 3 * u / d, 2 * v / d


def normal(T):
    u1, v1 = xy_to_uv(*planck_xy(T * 1.03))
    u2, v2 = xy_to_uv(*planck_xy(T * 0.97))
    du, dv = u1 - u2, v1 - v2
    n = np.hypot(du, dv)
    nu, nv = -dv / n, du / n
    if nv < 0:                     # 约定：法向取 v 增大的一侧，即偏绿方向
        nu, nv = -nu, -nv
    return nu, nv


def mccamy(x, y):
    n = (x - 0.3320) / (0.1858 - y)
    return 449 * n ** 3 + 3525 * n ** 2 + 6823.3 * n + 5520.33


fig = plt.figure(figsize=(7.2, 4.3))
gs = fig.add_gridspec(1, 2, width_ratios=[1.02, 1.0], wspace=0.36)

# ==================== (a) uv 平面里的等温线 ====================
ax = fig.add_subplot(gs[0])
Tg = np.concatenate([np.linspace(1500, 4000, 120), np.linspace(4000, 25000, 200)])
uv = np.array([xy_to_uv(*planck_xy(t)) for t in Tg])
ax.plot(uv[:, 0], uv[:, 1], color="#1b1f26", lw=2.2, zorder=6)

for T in (2000, 3000, 6500, 10000):
    u0, v0 = xy_to_uv(*planck_xy(T))
    nu, nv = normal(T)
    ts = np.array([-0.030, 0.030])
    ax.plot(u0 + ts * nu, v0 + ts * nv, color="#93a1af", lw=1.1,
            ls=(0, (3, 2)), zorder=4)
    ax.plot([u0], [v0], "o", ms=5, mfc="white", mec="#1b1f26", mew=1.3,
            zorder=7)
    cands = [(u0 + 0.030 * nu, v0 + 0.030 * nv),
             (u0 - 0.030 * nu, v0 - 0.030 * nv)]
    tx, ty = next(((a, b) for a, b in cands
                   if 0.180 < a < 0.286 and 0.280 < b < 0.368), cands[0])
    ax.text(tx, ty, f"{T} K", fontsize=6.8, color="#3d4a57", ha="center",
            va="center", zorder=8,
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="none", pad=0.4))

# 同一点上的 ±Duv（沿法向偏移）
T0 = 4500
u0, v0 = xy_to_uv(*planck_xy(T0))
nu, nv = normal(T0)
for dv_, col, lab, tx, ty, ha in (
        (0.006, H.GREEN, r"$D_{uv}=+0.006$  偏绿", 0.1805, 0.3555, "left"),
        (-0.006, H.PURPLE, r"$D_{uv}=-0.006$  偏品红", 0.1995, 0.2985, "left")):
    qu, qv = u0 + dv_ * nu, v0 + dv_ * nv
    ax.plot([qu], [qv], "s", ms=6.5, color=col, mec="white", mew=1.0,
            zorder=9)
    ax.annotate(lab, xy=(qu, qv), xytext=(tx, ty),
                fontsize=6.8, color=col, ha=ha, va="center",
                arrowprops=dict(arrowstyle="->", color=col, lw=0.8,
                                connectionstyle="arc3,rad=-0.15"))
ax.annotate("", xy=(u0 - 0.030 * nu, v0 - 0.030 * nv),
            xytext=(u0 + 0.025 * nu, v0 + 0.025 * nv),
            arrowprops=dict(arrowstyle="<->", color=H.DARK, lw=0.9))

ax.set_xlim(0.176, 0.290)
ax.set_ylim(0.276, 0.372)
ax.set_aspect("equal")
ax.set_xlabel("$u$（CIE 1960 UCS）")
ax.set_ylabel("$v$（CIE 1960 UCS）")
ax.set_xticks([0.18, 0.20, 0.22, 0.24, 0.26, 0.28])
ax.set_yticks([0.28, 0.30, 0.32, 0.34, 0.36])

# ==================== (b) McCamy 误差 ====================
ax2 = fig.add_subplot(gs[1])
Ts = np.linspace(1800, 20000, 400)
err = np.array([mccamy(*planck_xy(t)) - t for t in Ts])
ax2.axhline(0, color="#4a5666", lw=0.9)
ax2.semilogx(Ts, err, color=H.RED, lw=2.0)
ax2.axvspan(2856, 7000, color=H.NAVY, alpha=0.05, lw=0)
ax2.annotate("2856 到 7000 K：偏差在 10 K 以内", xy=(4200, 8.7),
             xytext=(1900, -1250), fontsize=7.2, color=H.NAVY, ha="left",
             va="center",
             arrowprops=dict(arrowstyle="->", color=H.NAVY, lw=0.9,
                             connectionstyle="arc3,rad=-0.25"))
ax2.annotate("10000 K：-126 K", xy=(10000, -126), xytext=(5600, -780),
             fontsize=7.2, color=H.RED, ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                             connectionstyle="arc3,rad=0.15"))
ax2.annotate("20000 K：-2900 K", xy=(19600, -2900), xytext=(6200, -2450),
             fontsize=7.2, color=H.RED, ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                             connectionstyle="arc3,rad=-0.2"))

ax2.set_xlim(1800, 22000)
ax2.set_ylim(-3300, 120)
ax2.set_xlabel("色温 $T$（K）")
ax2.set_ylabel("CCT 偏差（K）", labelpad=20, fontsize=9.5)
ax2.set_xticks([2000, 3000, 5000, 10000, 20000])
ax2.set_xticklabels(["2000", "3000", "5000", "10000", "20000"])
ax2.tick_params(axis="y", labelsize=8.5)
ax2.set_yticks([-3000, -2000, -1000, 0])

H.save(fig, 2, "f5_cct_duv")

for T in (2000, 2856, 4500, 6500, 6504, 10000, 20000):
    print(f"{T}: McCamy err {mccamy(*planck_xy(T)) - T:+.1f} K")
