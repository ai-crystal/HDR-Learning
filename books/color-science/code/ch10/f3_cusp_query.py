# -*- coding: utf-8 -*-
"""第 10 章 图 3：沿等色相射线求边界（二分）与尖点参数随色相的变化。

(a) 以 L* = 55、h = 30 为例，画出二分过程中区间的收缩；横轴为彩度，纵轴为迭代序号。
(b)(c) sRGB、Display P3、BT.2020 三个色域的尖点亮度与尖点彩度随色相角的变化。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cslib as C

plt = H.plt

fig = plt.figure(figsize=(7.8, 4.2))
gs = fig.add_gridspec(2, 2, width_ratios=[1.05, 1.0], height_ratios=[1, 1],
                      wspace=0.28, hspace=0.42, left=0.085, right=0.975,
                      top=0.955, bottom=0.135)

# ---------- (a) 二分收缩 ----------
ax = fig.add_subplot(gs[:, 0])
L0, h0, G = 55.0, 30.0, "P3"
Cl = C.cmax(L0, h0, G)
lo, hi = 0.0, 160.0
segs = []
for k in range(9):
    segs.append((lo, hi))
    mid = 0.5 * (lo + hi)
    if C.in_gamut(C.lch_to_lab([L0, mid, h0]), G):
        lo = mid
    else:
        hi = mid
for k, (a, b) in enumerate(segs):
    y = 8.6 - k
    inside = b <= Cl + 1e-9
    ax.plot([a, b], [y, y], color=H.NAVY if k % 2 == 0 else H.BLUE, lw=2.4,
            solid_capstyle="butt", alpha=0.85)
    ax.plot([0.5 * (a + b)], [y], "o", ms=3.4, color=H.ORANGE, zorder=5)
ax.axvline(Cl, color=H.RED, lw=1.4, ls=(0, (5, 2.5)))
ax.text(Cl - 3.0, 5.95, f"边界 $C_l=$ {Cl:.1f}", fontsize=8.4, color=H.RED,
        va="center", ha="right")
ax.set_ylim(-0.7, 10.0)
ax.set_xlim(0, 160)
ax.set_yticks(range(0, 9))
ax.set_yticklabels([f"{9-k}" for k in range(9)])
ax.set_xlabel("彩度 $C$", fontsize=10)
ax.set_ylabel("迭代次数", fontsize=10)
ax.set_title("每一次二分把区间减半", fontsize=9.6, pad=6)
ax.text(4, 9.85, "(a) $L^*=55$，$h=30$ 度，目标 P3", fontsize=8.0, color="#4a5666",
        va="top")
ax.text(6, 4.55, "第 9 次后区间宽\n0.31 个 $C$ 单位", fontsize=7.6, color="#4a5666",
        ha="left", va="top")

# ---------- (b) 尖点亮度 ----------
hs = np.linspace(0, 360, 73)
names = ["sRGB", "P3", "BT2020"]
cols = {"sRGB": H.NAVY, "P3": H.ORANGE, "BT2020": H.TEAL}
res = {}
for g in names:
    res[g] = np.array([C.cusp(h, g, nL=41) for h in hs])

ax = fig.add_subplot(gs[0, 1])
for g in names:
    ax.plot(hs, res[g][:, 0], color=cols[g], lw=1.7, label=g)
ax.set_xlim(0, 360)
ax.set_xticks([0, 60, 120, 180, 240, 300, 360])
ax.set_ylim(35, 100)
ax.set_ylabel("尖点 $L^*$", fontsize=9.5)
ax.legend(loc="lower center", ncol=3, fontsize=7.4, frameon=False,
          bbox_to_anchor=(0.5, 1.02), columnspacing=1.2, handlelength=1.6)
ax.text(200, 41, "(b)", fontsize=9.0, color=H.DARK, va="bottom")

# ---------- (c) 尖点彩度 ----------
ax = fig.add_subplot(gs[1, 1])
for g in names:
    ax.plot(hs, res[g][:, 1], color=cols[g], lw=1.7, label=g)
ax.set_xlim(0, 360)
ax.set_xticks([0, 60, 120, 180, 240, 300, 360])
ax.set_xlabel("色相角 $h_{ab}$", fontsize=10)
ax.set_ylabel("尖点 $C^*$", fontsize=9.5)
ax.text(200, 26, "(c)", fontsize=9.0, color=H.DARK, va="bottom")
ax.set_ylim(20, 215)

for a in fig.axes:
    a.grid(True, alpha=0.6)

H.save(fig, 10, "f3_cusp_query")
print("Cl", Cl)
for g in names:
    i = int(np.argmin(np.abs(hs - 30)))
    print(g, "h=30 cusp", res[g][i], "max C cusp", res[g][:, 1].max(),
          "at h", hs[int(np.argmax(res[g][:, 1]))])
