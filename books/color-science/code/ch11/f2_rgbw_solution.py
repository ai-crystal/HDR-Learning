# -*- coding: utf-8 -*-
"""第 11 章 图 2：RGBW 映射的欠定解与选择依据。

左图：给定一个目标色，W 子像素从关到开的整个解族（R、G、B 三条曲线），
解在 w 超过某一点后消失，这一点由"某个通道先归零"决定。
右图：不同色相的目标色在 L* = 70 时最多能用多少 W 份额，彩度越高越用不上。

数值按 Display P3 基色 + D65 白点计算，RGB→XYZ 矩阵由基色坐标解出。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import primaries11 as P

plt = H.plt

M, S = P.covering_matrix([P.PRIMARIES["DisplayP3"][k] for k in "RGB"],
                         P.WHITE["D65"], 1.0)
Minv = np.linalg.inv(M)
Wxyz = P.xy_to_XYZ(*P.WHITE["D65"], 1.0)          # 白子像素满驱动时的 XYZ
Wn = P.xy_to_XYZ(*P.WHITE["D65"], 1.0)


def feasible(rgb):
    return np.all(rgb >= -1e-9) and np.all(rgb <= 1 + 1e-9)


def max_w_xyz(XYZ):
    if not feasible(Minv @ XYZ):
        return np.nan
    if feasible(Minv @ (XYZ - Wxyz)):
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if feasible(Minv @ (XYZ - mid * Wxyz)):
            lo = mid
        else:
            hi = mid
    return lo


def lab_to_xyz(L, a, b):
    fy = (L + 16) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0
    d = 6.0 / 29.0

    def finv(t):
        return np.where(t > d, t ** 3, 3 * d * d * (t - 4.0 / 29.0))

    return np.array([finv(fx), finv(fy), finv(fz)]) * Wn


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.9),
                               gridspec_kw=dict(wspace=0.30, left=0.078,
                                                right=0.975, top=0.925, bottom=0.155))

# ---------------- 左图：解族 ----------------
xy_t = (0.340, 0.370)
Yt = 0.70
XYZt = P.xy_to_XYZ(*xy_t, Yt)
wmax = max_w_xyz(XYZt)

ws = np.linspace(0, 1, 600)
sols = np.array([Minv @ (XYZt - w * Wxyz) for w in ws])
sols[ws > wmax + 1e-9] = np.nan

ax1.axvspan(wmax, 1.0, color="#f6e2d8", alpha=0.8, zorder=0)
ax1.axvline(wmax, color=H.RED, lw=1.0, ls=":", zorder=1)

ax1.plot(ws, sols[:, 0], color=H.RED, lw=2.0, label="R 通道")
ax1.plot(ws, sols[:, 1], color=H.GREEN, lw=2.0, label="G 通道")
ax1.plot(ws, sols[:, 2], color=H.BLUE, lw=2.0, label="B 通道")
ax1.plot(ws, ws, color="#3b3b3b", lw=1.4, ls=(0, (4, 3)), label="W 通道")

for wsel, col in ((0.0, H.NAVY), (wmax, H.ORANGE)):
    rgb = np.clip(Minv @ (XYZt - wsel * Wxyz), 0, 1)
    ax1.plot([wsel] * 3, rgb, ls="none", marker="o", ms=5.6, mfc="white",
             mec=col, mew=1.6, zorder=6)

ax1.annotate("B 先归零", xy=(wmax, 0.0), xytext=(wmax + 0.10, 0.13),
             fontsize=7.6, color=H.BLUE, ha="left", va="center", zorder=8,
             arrowprops=dict(arrowstyle="->", color=H.BLUE, lw=1.0, shrinkB=2),
             bbox=dict(facecolor="white", alpha=0.88, edgecolor="none", pad=1.6))
ax1.text(0.945, 0.50, "虚线右侧无解，w 上限 0.49", fontsize=7.6, color=H.RED, rotation=90,
         ha="center", va="center", zorder=8)
ax1.text(0.015, 0.06, "w = 0 全用彩色子像素\n最费电，色度余量最大", fontsize=7.2,
         color=H.NAVY, ha="left", va="bottom", zorder=8,
         bbox=dict(facecolor="white", alpha=0.86, edgecolor="none", pad=1.6))

ax1.set_xlim(-0.01, 1.0)
ax1.set_ylim(0, 1.05)
ax1.set_xlabel("白子像素的驱动值 $w$", labelpad=1)
ax1.set_ylabel("各通道驱动值")
ax1.legend(loc="upper right", fontsize=7.4, handlelength=1.7, borderpad=0.45,
           labelspacing=0.35)
ax1.set_title("(a) 目标色 (0.340, 0.370)，Y = 0.70 时的解族", fontsize=9.2, pad=6)

# ---------------- 右图：W 份额与彩度 ----------------
Cvals = np.linspace(0, 120, 80)
for hue, name, col in ((0, "红方向 0°", H.RED), (40, "橙 40°", H.ORANGE),
                       (120, "绿 120°", H.GREEN), (270, "蓝 270°", H.BLUE)):
    th = np.radians(hue)
    vals = [max_w_xyz(lab_to_xyz(70.0, C * np.cos(th), C * np.sin(th)))
            for C in Cvals]
    vals = np.array(vals, dtype=float)
    ax2.plot(Cvals, vals, color=col, lw=2.0, label=name)
    if np.all(np.isnan(vals)):
        continue
    i = np.where(np.isnan(vals))[0]
    if len(i) and i[0] > 1:
        ax2.plot(Cvals[i[0] - 1], vals[i[0] - 1], marker="x", ms=6, color=col,
                 mew=1.8, zorder=6)

ax2.axhline(1.0, color="#9aa6b2", lw=0.9, ls=(0, (3, 3)))
ax2.text(117, 1.03, "全部交给白子像素", fontsize=7.2, color="#697580", ha="right")
ax2.set_xlim(0, 120)
ax2.set_ylim(0, 1.16)
ax2.set_xlabel("目标色的 CIELAB 彩度 $C^*_{ab}$（L* = 70）")
ax2.set_ylabel("可用白子像素份额 $w_{\\max}$")
ax2.legend(loc="lower left", fontsize=7.4, handlelength=1.7, borderpad=0.45,
           labelspacing=0.32)
ax2.set_title("(b) 彩度升高后白子像素能承担多少", fontsize=9.2, pad=6)

H.save(fig, 11, "f2_rgbw_solution")
print("wmax = %.3f" % wmax)
print("w=0  :", np.round(Minv @ XYZt, 3), " sum %.3f" % (Minv @ XYZt).sum())
print("w=max:", np.round(np.clip(Minv @ (XYZt - wmax * Wxyz), 0, 1), 3),
      " sum %.3f" % np.clip(Minv @ (XYZt - wmax * Wxyz), 0, 1).sum())
for C in (0, 20, 40, 60, 80):
    print("  C=%.0f: red %.3f  120deg %.3f" % (
        C, max_w_xyz(lab_to_xyz(70, C, 0)), max_w_xyz(lab_to_xyz(70, -0.5 * C, 0.866 * C))))
