# -*- coding: utf-8 -*-
"""第 11 章 图 1：多原色色域多边形与三原色三角形的叠加（CIE 1976 u'v'）。

原色取真实谱线波长（638/590/532/490/465 nm），坐标由 CIE 1931 标准观察者
对单色光积分得到；BT.2020 三角形用标准坐标。多边形为原色点在 u'v' 中的凸包，
面积为鞋带公式，覆盖率以 BT.2020 三角形为分母、用多边形裁剪求交后计算。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import primaries11 as P

plt = H.plt

LAM_R, LAM_Y, LAM_G, LAM_C, LAM_B = 638, 590, 532, 490, 465
p3 = [P.xy_of_wavelength(LAM_R), P.xy_of_wavelength(LAM_G), P.xy_of_wavelength(LAM_B)]
p4 = [P.xy_of_wavelength(LAM_R), P.xy_of_wavelength(LAM_G),
      P.xy_of_wavelength(LAM_C), P.xy_of_wavelength(LAM_B)]
p5 = [P.xy_of_wavelength(LAM_R), P.xy_of_wavelength(LAM_Y), P.xy_of_wavelength(LAM_G),
      P.xy_of_wavelength(LAM_C), P.xy_of_wavelength(LAM_B)]
bt2020 = [P.PRIMARIES["BT2020"][k] for k in "RGB"]


def hull_uv(prims):
    return np.array([P.xy_to_uv76(*q) for q in P.convex_hull_2d(prims)])


def draw(ax, poly, col, lw, fill=None, ls="-", z=5):
    xs = np.append(poly[:, 0], poly[0, 0])
    ys = np.append(poly[:, 1], poly[0, 1])
    if fill:
        ax.fill(xs, ys, color=fill, alpha=0.14, zorder=1, edgecolor="none")
    ax.plot(xs, ys, color=col, lw=lw, ls=ls, zorder=z, solid_capstyle="round")


fig = plt.figure(figsize=(7.4, 5.2))
ax = fig.add_axes([0.075, 0.105, 0.585, 0.865])

lam, sx, sy = P.C.spectral_locus(1600)
su, sv = P.xy_to_uv76(sx, sy)
ax.fill(np.append(su, su[0]), np.append(sv, sv[0]), color="#f4f6f9",
        zorder=0, edgecolor="none")
ax.plot(su, sv, color="#8a97a6", lw=1.4, zorder=2)
ax.plot([su[0], su[-1]], [sv[0], sv[-1]], color="#8a97a6", lw=1.0,
        ls=(0, (4, 3)), zorder=2)

for wl, dx, dy, ha in ((460, 0.016, -0.014, "left"), (580, 0.002, 0.026, "center")):
    i = int(np.argmin(np.abs(lam - wl)))
    ax.text(su[i] + dx, sv[i] + dy, f"{wl} nm", fontsize=7.0, color="#6d7885",
            ha=ha, va="center", zorder=3)

draw(ax, hull_uv(bt2020), H.NAVY, 1.8, ls=(0, (5, 3)), z=5)
draw(ax, hull_uv(p4), H.ORANGE, 2.0, fill=H.ORANGE, z=6)
draw(ax, hull_uv(p3), H.TEAL, 1.8, ls=(0, (7, 3)), z=7)
draw(ax, hull_uv(p5), H.PURPLE, 1.5, ls=(0, (2, 2)), z=8)

mark = [("R 638", p3[0], H.RED, (-0.014, -0.028), "right"),
        ("G 532", p3[1], H.GREEN, (0.020, 0.004), "left"),
        ("B 465", p3[2], H.BLUE, (0.014, -0.020), "left"),
        ("C 490", p4[2], H.ORANGE, (0.012, -0.028), "left"),
        ("Y 590", p5[1], H.PURPLE, (-0.016, -0.026), "right")]
for name, xy, col, (dx, dy), ha in mark:
    u, v = P.xy_to_uv76(*xy)
    ax.plot([u], [v], marker="o", ms=6.6, mfc="white", mec=col, mew=1.7, zorder=9)
    ax.text(u + dx, v + dy, f"{name} nm", fontsize=7.8, color=col, ha=ha,
            va="center", zorder=10,
            bbox=dict(facecolor="white", alpha=0.88, edgecolor="none", pad=0.9))

ax.plot([0.1978], [0.4683], marker="+", ms=8, color="#38424e", mew=1.4, zorder=9)

ax.text(0.203, 0.486, "D65", fontsize=7.4, color="#38424e", va="center", zorder=9)

ax.text(0.103, 0.448, "青色原色只换来\n左侧窄窄一条", fontsize=7.4, color=H.ORANGE,
        ha="left", va="center", zorder=11,
        bbox=dict(facecolor="white", alpha=0.9, edgecolor=H.ORANGE, lw=0.6, pad=2.0))
ax.text(0.296, 0.474, "黄色原色只换来\n顶上一个小角", fontsize=7.4, color=H.PURPLE,
        ha="left", va="center", zorder=11,
        bbox=dict(facecolor="white", alpha=0.9, edgecolor=H.PURPLE, lw=0.6, pad=2.0))

ax.set_xlim(0.00, 0.62)
ax.set_ylim(0.00, 0.628)
ax.set_xlabel("u′")
ax.set_ylabel("v′")
ax.set_aspect("equal")

# ---------- 右侧说明 ----------
rows = [("BT.2020 标准三角形", "面积 0.1118，顶点在光谱轨迹内侧", H.NAVY, (0, (5, 3))),
        ("三原色 638 / 532 / 465", "面积 0.1197，覆盖 BT.2020 的 98.6%", H.TEAL, (0, (7, 3))),
        ("四原色 加 490 nm 青", "面积 0.1362，覆盖 99.9%", H.ORANGE, "-"),
        ("五原色 加 590 nm 黄", "面积 0.1367，覆盖 100.0%", H.PURPLE, (0, (2, 2)))]
x0, x1, x2 = 0.700, 0.735, 0.745
ytop, step = 0.855, 0.083
for k, (name, note, col, ls) in enumerate(rows):
    yy = ytop - k * step
    ax.plot([x0, x1], [yy, yy], color=col, lw=2.4, ls=ls, transform=fig.transFigure,
            clip_on=False)
    fig.text(x2, yy + 0.018, name, fontsize=8.4, color=col, va="center")
    fig.text(x2, yy - 0.019, note, fontsize=7.6, color="#59636f", va="center")

fig.text(x0, ytop - 4 * step, "面积为鞋带公式；覆盖率为与 BT.2020\n三角形求交后的面积比。",
         fontsize=7.2, color="#59636f", va="top")

# ---------- 右下角：面积柱状 ----------
axb = fig.add_axes([0.745, 0.115, 0.215, 0.255])
names = ["2020", "3P", "4P", "5P"]
vals = [0.1118, 0.1197, 0.1362, 0.1367]
cols = [H.NAVY, H.TEAL, H.ORANGE, H.PURPLE]
axb.bar(range(4), vals, color=cols, width=0.62, alpha=0.9)
for i, v in enumerate(vals):
    axb.text(i, v - 0.004, f"{v:.4f}", ha="center", va="top", fontsize=6.6, color="white")
axb.set_xticks(range(4))
axb.set_xticklabels(names, fontsize=7.6)
axb.set_ylim(0.10, 0.152)
axb.set_ylabel("u′v′ 面积", fontsize=7.6)
axb.tick_params(axis="y", labelsize=6.8)
axb.grid(axis="x", visible=False)

H.save(fig, 11, "f1_multiprimary_polygon")
