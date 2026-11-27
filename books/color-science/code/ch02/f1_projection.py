# -*- coding: utf-8 -*-
"""第 02 章 图 1：色品坐标是 XYZ 空间里的一次中心投影，以及加色混合的杠杆定则。

(a) X Y Z 三轴张成的空间里，等色品面 x+y+z=1 是一个平面。任一刺激向量 P 沿
    过原点的射线投到该平面，落点只由 X:Y:Z 的比例决定，射线上不同的点（不同
    亮度）落在同一处。光谱轨迹就是三条色匹配函数在平面上的投影曲线。
(b) 两个颜色混合后的色品坐标是按 S = X+Y+Z 加权的定点分点，权重不是亮度 Y。
    取亮度相等时，混合点并不在线段中点，因为两者的 y 不同。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C
from matplotlib.patches import Polygon

plt = H.plt

fig = plt.figure(figsize=(7.2, 4.4))
gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.20)

# ==================== (a) 中心投影 ====================
ax = fig.add_subplot(gs[0])
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
for s in ax.spines.values():
    s.set_visible(False)


def proj(x, y, z):
    """等轴测投影，X 向右、Y 向上、Z 向左。"""
    return 0.86 * x - 0.62 * z, y + 0.30 * x + 0.20 * z


# 三个轴
for v, lab, col in (((1.35, 0, 0), r"$X$", H.RED),
                    ((0, 1.30, 0), r"$Y$", H.GREEN),
                    ((0, 0, 1.35), r"$Z$", H.BLUE)):
    p0, p1 = proj(0, 0, 0), proj(*v)
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.6,
                                mutation_scale=11, alpha=0.85))
    ax.text(p1[0] * 1.06, p1[1] * 1.02, lab, fontsize=10.5, color=col,
            fontweight="bold", ha="center", va="center")

# 平面 x+y+z=1
tri = [proj(1, 0, 0), proj(0, 1, 0), proj(0, 0, 1)]
ax.add_patch(Polygon(tri, closed=True, facecolor="#eef2f7",
                     edgecolor="#9aa8b6", lw=1.2, zorder=1))

# 光谱轨迹（投影到平面上），按波长上色
lam = np.linspace(380, 780, 400)
xb = np.interp(lam, C.LAM, C.XBAR)
yb = np.interp(lam, C.LAM, C.YBAR)
zb = np.interp(lam, C.LAM, C.ZBAR)
tot = xb + yb + zb
cx, cy, cz = xb / tot, yb / tot, zb / tot
rgb = C.wavelength_to_srgb01(lam)
pts = np.array([proj(cx[i], cy[i], cz[i]) for i in range(len(lam))])
for i in range(len(lam) - 1):
    ax.plot(pts[i:i + 2, 0], pts[i:i + 2, 1], color=rgb[i], lw=2.6, zorder=3)
# 紫线
ax.plot([pts[0, 0], pts[-1, 0]], [pts[0, 1], pts[-1, 1]], color="#8e44ad",
        lw=1.8, ls=(0, (4, 2)), zorder=3)

# 刺激向量与它的投影
P = np.array([0.62, 0.78, 0.42])
pP = proj(*P)
ax.annotate("", xy=pP, xytext=proj(0, 0, 0),
            arrowprops=dict(arrowstyle="-|>", color=H.DARK, lw=2.0,
                            mutation_scale=12))
for t, mk in ((0.62, "s"), (1.48, "^")):
    q = proj(*(P * t))
    ax.plot([q[0]], [q[1]], mk, ms=5.5, mfc="white", mec=H.DARK, mew=1.3,
            zorder=6)
Pi = P / P.sum()
pPi = proj(*Pi)
ax.plot([proj(0, 0, 0)[0], proj(*(P * 1.62))[0]],
        [proj(0, 0, 0)[1], proj(*(P * 1.62))[1]],
        color=H.DARK, lw=1.0, ls=(0, (4, 3)), alpha=0.75, zorder=5)
ax.plot([pPi[0]], [pPi[1]], "o", ms=7.5, mfc="white", mec=H.ORANGE, mew=2.0,
        zorder=7)
ax.text(pPi[0] - 0.05, pPi[1] - 0.14, "色品点 $(x,y)$", fontsize=7.6,
        color="#a35b13", ha="center", va="center")
ax.text(pP[0] + 0.07, pP[1] + 0.02, r"$\mathbf{P}=(X,Y,Z)$", fontsize=8.6,
        color=H.DARK, ha="left", va="center")
ax.text(proj(*(P * 1.48))[0] + 0.02, proj(*(P * 1.48))[1] + 0.08,
        "同一条射线上\n亮度不同，色品相同", fontsize=7.0, color=H.DARK,
        ha="left", va="center")

ax.text(-0.98, -0.33, "$x+y+z=1$ 平面：射线上的点\n全部投影到同一处，亮度丢失",
        fontsize=7.0, color="#4a5666", ha="left", va="center")

ax.set_xlim(-1.02, 1.28)
ax.set_ylim(-0.50, 1.42)

# ==================== (b) 杠杆定则 ====================
ax2 = fig.add_subplot(gs[1])

C1 = (0.640, 0.330)      # 纯红附近
C2 = (0.150, 0.060)      # 纯蓝附近
Y1 = Y2 = 0.50
S1 = Y1 / C1[1]
S2 = Y2 / C2[1]

# 光谱轨迹轮廓
l2 = np.linspace(380, 780, 600)
sx = np.interp(l2, C.LAM, C.XBAR)
sy = np.interp(l2, C.LAM, C.YBAR)
sz = np.interp(l2, C.LAM, C.ZBAR)
tt = sx + sy + sz
ax2.plot(sx / tt, sy / tt, color="#b8c2cc", lw=1.4, zorder=2)
ax2.plot([sx[0] / tt[0], sx[-1] / tt[-1]], [sy[0] / tt[0], sy[-1] / tt[-1]],
         color="#c9b6d8", lw=1.2, ls=(0, (4, 2)), zorder=2)

ax2.plot([C1[0], C2[0]], [C1[1], C2[1]], color="#5b6b7a", lw=1.4, zorder=3)
ax2.plot(*C1, "o", ms=7, color=H.ORANGE, mec="white", mew=1.0, zorder=6)
ax2.plot(*C2, "o", ms=7, color=H.NAVY, mec="white", mew=1.0, zorder=6)
ax2.annotate("色 1\n$y=0.33$", xy=(C1[0]-0.012, C1[1]+0.012),
             xytext=(0.520, 0.395), fontsize=7.4, color="#a35b13",
             ha="left", va="bottom",
             arrowprops=dict(arrowstyle="->", color="#a35b13", lw=0.8,
                             connectionstyle="arc3,rad=0.2"))
ax2.annotate("色 2\n$y=0.06$", xy=(C2[0]+0.010, C2[1]+0.010),
             xytext=(0.075, 0.135), fontsize=7.4, color=H.NAVY,
             ha="left", va="bottom",
             arrowprops=dict(arrowstyle="->", color=H.NAVY, lw=0.8,
                             connectionstyle="arc3,rad=-0.2"))

mid_Y = ((C1[0] + C2[0]) / 2, (C1[1] + C2[1]) / 2)
w1 = S1 / (S1 + S2)
mix_S = (C1[0] * w1 + C2[0] * (1 - w1), C1[1] * w1 + C2[1] * (1 - w1))
ax2.plot(*mid_Y, "s", ms=7, mfc="white", mec=H.GRAY, mew=1.6, zorder=6)
ax2.plot(*mix_S, "D", ms=7, mfc="white", mec=H.RED, mew=1.6, zorder=6)
ax2.annotate("按亮度等分\n（错误做法）", xy=(mid_Y[0]-0.006, mid_Y[1]+0.010),
             xytext=(0.215, 0.330), fontsize=7.0, color=H.GRAY,
             ha="left", va="bottom",
             arrowprops=dict(arrowstyle="->", color=H.GRAY, lw=0.9,
                             connectionstyle="arc3,rad=-0.25"))
ax2.annotate("按 $S=X+Y+Z$ 加权\n（实际混合点）", xy=(mix_S[0]+0.004, mix_S[1]-0.008),
             xytext=(0.230, 0.235), fontsize=7.0, color=H.RED,
             ha="left", va="bottom",
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                             connectionstyle="arc3,rad=0.3"))

ax2.set_xlim(0.04, 0.72)
ax2.set_ylim(0.00, 0.44)
ax2.set_aspect("equal")
ax2.set_xlabel("色度坐标 x")
ax2.set_ylabel("色度坐标 y")
ax2.set_xticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
ax2.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4])

H.save(fig, 2, "f1_projection")

print("S1, S2 =", round(S1, 4), round(S2, 4), " w1 =", round(w1, 4))
print("mix by S:", np.round(mix_S, 4), " midpoint:", np.round(mid_Y, 4))
print("segment param of mix:", round((mix_S[0] - C2[0]) / (C1[0] - C2[0]), 4))
