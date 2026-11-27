# -*- coding: utf-8 -*-
"""第 03 章 图 4：等色差线在 xy 与 a*b* 平面上。

固定 Y=0.5，在六个中心色周围逐点计算 ΔE2000，取 ΔE2000=2 的等值线，
再把同一组等值线映射到 a*b* 平面。左图轮廓的面积相差 7 倍，
右图轮廓接近圆但半径随彩度增大，增速来自 S_C 权重项。
所有数值由 CIEDE2000 公式直接算得，没有拟合。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C
import colordiff as D
from scipy.interpolate import PchipInterpolator

plt = H.plt
Y0 = 0.5
CENTERS = [(0.190, 0.210), (0.280, 0.260), (0.330, 0.330),
           (0.330, 0.450), (0.470, 0.410), (0.520, 0.330)]


def lab_of_xy(x, y):
    X, Y, Z = D.xy_to_XYZ(x, y, Y0)
    return np.array(D.xyz_to_lab(X, Y, Z), dtype=float)


def ring(cx, cy, level=2.0, half=0.135, n=161):
    g = np.linspace(-half, half, n)
    GX, GY = np.meshgrid(cx + g, cy + g)
    ok = (GY > 0.02) & (GX + GY < 0.98)
    lab0 = lab_of_xy(cx, cy)
    de = np.full_like(GX, np.nan)
    for i in range(GX.shape[0]):
        for j in range(GX.shape[1]):
            if ok[i, j]:
                de[i, j] = D.de2000(lab0, lab_of_xy(GX[i, j], GY[i, j]))
            else:
                de[i, j] = np.nan
    ftmp = plt.figure()
    cs = ftmp.add_subplot(111).contour(GX, GY, de, levels=[level])
    plt.close(ftmp)
    return [np.array(s) for s in cs.allsegs[0] if len(s) > 20]


def area(p):
    x, y = p[:, 0], p[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


fig = plt.figure(figsize=(7.4, 4.3))
ax = fig.add_axes([0.072, 0.115, 0.400, 0.855])
ax2 = fig.add_axes([0.622, 0.115, 0.350, 0.855])

lam_d = np.linspace(380, 780, 600)
xb = PchipInterpolator(C.LAM, C.XBAR)(lam_d)
yb = PchipInterpolator(C.LAM, C.YBAR)(lam_d)
zb = PchipInterpolator(C.LAM, C.ZBAR)(lam_d)
tot = xb + yb + zb
ax.plot(xb / tot, yb / tot, color="#c3ccd6", lw=1.3, zorder=2)
ax.plot([xb[0] / tot[0], xb[-1] / tot[-1]], [yb[0] / tot[0], yb[-1] / tot[-1]],
        color="#c3ccd6", lw=1.1, ls=(0, (4, 3)), zorder=2)

rows = []
first = True
for (cx, cy) in CENTERS:
    lab0 = lab_of_xy(cx, cy)
    cstar = float(np.hypot(lab0[1], lab0[2]))
    for s in ring(cx, cy):
        ax.plot(s[:, 0], s[:, 1], color=H.NAVY, lw=1.5,
                label=r"$\Delta E_{2000}=2$ 等值线" if first else None, zorder=6)
        ab = np.array([lab_of_xy(px, py)[1:] for px, py in s])
        ax2.plot(ab[:, 0], ab[:, 1], color=H.NAVY, lw=1.5, zorder=6)
        r = np.sqrt(area(ab) / np.pi)
        rows.append((cstar, area(s), r))
        first = False
    ax.plot([cx], [cy], ".", ms=4.5, color=H.RED, zorder=7)
    ax2.plot([lab0[1]], [lab0[2]], ".", ms=4.5, color=H.RED, zorder=7)
    if cstar < 10:
        ax2.text(lab0[1] + 6, lab0[2] + 3, r"$C^*$=%d" % round(cstar), fontsize=6.8,
                 color=H.RED, ha="left", va="bottom", zorder=8)

ax.set_xlim(0.00, 0.76)
ax.set_ylim(0.00, 0.88)
ax.set_aspect("equal")
ax.set_xlabel("色度坐标 x")
ax.set_ylabel("色度坐标 y")
ax.legend(loc="upper right", fontsize=7.6, frameon=True, handlelength=1.7,
          borderpad=0.42)
axy = [r[1] for r in rows]
ax.text(0.375, 0.735, "轮廓面积最大与最小\n相差 %.1f 倍" % (max(axy) / min(axy)),
        fontsize=7.6, color="#2c3e50", ha="center", va="center", linespacing=1.55,
        bbox=dict(facecolor="white", alpha=0.9, edgecolor=H.LGRAY,
                  boxstyle="round,pad=0.32"))

ax2.set_xlim(-52, 100)
ax2.set_ylim(-74, 86)
ax2.set_aspect("equal")
ax2.axhline(0, color="#9aa7b4", lw=0.9)
ax2.axvline(0, color="#9aa7b4", lw=0.9)
ax2.set_xlabel(r"$a^*$")
ax2.set_ylabel(r"$b^*$")
ax2.text(-48, 79, r"$+b^*$ 偏黄，$-b^*$ 偏蓝", fontsize=7.4, color="#4a5666",
         ha="left", va="top")
ax2.text(52, -64, "轮廓接近圆\n等效半径 %.1f 到 %.1f" % (min(r[2] for r in rows),
                                                  max(r[2] for r in rows)),
         fontsize=7.4, color="#2c3e50", ha="center", va="center", linespacing=1.55,
         bbox=dict(facecolor="white", alpha=0.9, edgecolor=H.LGRAY,
                   boxstyle="round,pad=0.32"))

H.save(fig, 3, "f4_uniformity")
print("C*   面积xy     半径ab")
for c, a, r in rows:
    print("%5.1f %.3e %6.2f" % (c, a, r))
print("xy 面积比值 %.2f；ab 半径比 %.2f" % (max(axy) / min(axy),
                                        max(r[2] for r in rows) / min(r[2] for r in rows)))
