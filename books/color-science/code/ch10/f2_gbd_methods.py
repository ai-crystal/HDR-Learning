# -*- coding: utf-8 -*-
"""第 10 章 图 2：色域边界描述的两种构造（凸包与 α-shape）与等亮度切片族。

(a) 在 L* = 50 的切片上，用 24 个带 2.0 C 单位噪声的边界采样点分别求凸包与 α-shape，
    与连续求解的真实边界比较面积。噪声模拟实测 GBD 点云的离群点。
(b) 把 sRGB 色域切成 9 层等亮度切片，叠出边界族与尖点轨迹。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cslib as C
from scipy.spatial import ConvexHull

plt = H.plt
rng = np.random.default_rng(7)


def sha_area(pts):
    x, y = pts[:, 0], pts[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def walk_cycle(edges, pts):
    adj = {}
    for i, j in edges:
        adj.setdefault(i, []).append(j)
        adj.setdefault(j, []).append(i)
    start = min(adj)
    cyc, prev, cur = [start], None, start
    while True:
        nxt = [k for k in adj[cur] if k != prev]
        if not nxt:
            break
        prev, cur = cur, nxt[0]
        if cur == start:
            break
        cyc.append(cur)
    return pts[cyc]


fig = plt.figure(figsize=(7.8, 3.9))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.0], wspace=0.24,
                      left=0.07, right=0.985, top=0.95, bottom=0.15)

# ---------- (a) 凸包 vs α-shape ----------
ax = fig.add_subplot(gs[0])
L0, G = 50.0, "sRGB"
hs_d = np.linspace(0, 360, 721)
cs_d = np.array([C.cmax(L0, h, G) for h in hs_d])
bd = C.lch_to_lab(np.stack([np.full_like(hs_d, L0), cs_d, hs_d], axis=-1))[:, 1:]
area_true = sha_area(bd)

n = 24
hs_s = np.linspace(0, 360, n, endpoint=False)
cs_s = np.array([C.cmax(L0, h, G) for h in hs_s])
pts = C.lch_to_lab(np.stack([np.full(n, L0), cs_s, hs_s], axis=-1))[:, 1:]
pts_n = pts + rng.normal(0, 2.0, pts.shape)
hull = ConvexHull(pts_n)
hp = pts_n[hull.vertices]
area_hull = sha_area(hp)

edges, _ = C.alpha_shape(pts_n, alpha=0.015)
cyc = walk_cycle(edges, pts_n)
area_alpha = sha_area(cyc)

ax.plot(np.r_[bd[:, 0], bd[0, 0]], np.r_[bd[:, 1], bd[0, 1]], color=H.NAVY, lw=2.2,
        label="连续求解的边界", zorder=3)
ax.plot(np.r_[hp[:, 0], hp[0, 0]], np.r_[hp[:, 1], hp[0, 1]], color=H.ORANGE, lw=1.6,
        ls=(0, (5, 2.5)), label="24 点凸包", zorder=4)
ax.plot(np.r_[cyc[:, 0], cyc[0, 0]], np.r_[cyc[:, 1], cyc[0, 1]], color=H.TEAL,
        lw=1.5, ls=(0, (1.6, 1.6)), label="24 点 α-shape", zorder=5)
ax.plot(pts_n[:, 0], pts_n[:, 1], "o", ms=3.2, mfc="#9aa6b2", mec="none",
        label="采样点（噪声 2.0）", zorder=6)
ax.plot([0], [0], "+", ms=7, color="#6b7885", mew=1.4)
ax.set_xlim(-105, 110)
ax.set_ylim(-115, 112)
ax.set_xlabel("$a^*$", fontsize=10)
ax.set_ylabel("$b^*$", fontsize=10)
ax.set_aspect("equal")
txt = (f"真实面积 {area_true:,.0f}\n凸包 {area_hull:,.0f}"
       f"（{100*(area_hull/area_true-1):+.1f}%）　α-shape {area_alpha:,.0f}"
       f"（{100*(area_alpha/area_true-1):+.1f}%）")
ax.text(0.5, 0.055, txt, fontsize=7.6, ha="center",
        va="bottom", color="#39424e", transform=ax.transAxes,
        bbox=dict(fc="white", ec="#d5dbe2", lw=0.7, pad=3.0, alpha=0.92))
ax.legend(loc="upper left", fontsize=7.0, frameon=True, framealpha=0.95,
          borderpad=0.4, handlelength=2.0, labelspacing=0.35)
ax.text(104, 104, "(a)", fontsize=9.4, color=H.DARK, va="top", ha="right")

# ---------- (b) 等亮度切片族 ----------
ax = fig.add_subplot(gs[1])
levels = [10, 20, 30, 40, 50, 60, 70, 80, 90]
cmap = plt.get_cmap("Blues")
for k, L in enumerate(levels):
    hs_ = np.linspace(0, 360, 361)
    cs_ = np.array([C.cmax(L, h, G) for h in hs_])
    lab = C.lch_to_lab(np.stack([np.full_like(hs_, L), cs_, hs_], axis=-1))[:, 1:]
    if L == 50:
        ax.plot(np.r_[lab[:, 0], lab[0, 0]], np.r_[lab[:, 1], lab[0, 1]],
                color=H.ORANGE, lw=2.0, label="$L^*=50$ 切片", zorder=5)
    else:
        col = cmap(0.30 + 0.60 * k / (len(levels) - 1))
        ax.plot(np.r_[lab[:, 0], lab[0, 0]], np.r_[lab[:, 1], lab[0, 1]],
                color=col, lw=1.2)

hs_c = np.linspace(0, 360, 73)
lcs = np.array([C.cusp(h, G, nL=41) for h in hs_c])
ax.plot(lcs[:, 1] * np.cos(np.radians(hs_c)), lcs[:, 1] * np.sin(np.radians(hs_c)),
        color=H.RED, lw=1.5, ls=(0, (5, 2)), label="尖点轨迹")
ax.plot([0], [0], "+", ms=7, color="#6b7885", mew=1.4)
ax.set_xlim(-110, 125)
ax.set_ylim(-120, 118)
ax.set_xlabel("$a^*$", fontsize=10)
ax.set_ylabel("$b^*$", fontsize=10)
ax.set_aspect("equal")
ax.legend(loc="lower right", fontsize=7.6, frameon=True, framealpha=0.95)
ax.text(120, 110, "(b)", fontsize=9.4, color=H.DARK, va="top", ha="right")
ax.text(-105, -114, "由内向外 $L^*$ 从 10 增到 90，每层 10", fontsize=7.4,
        color="#6b7885", va="bottom")

H.save(fig, 10, "f2_gbd_methods")
print(f"area_true={area_true:.1f} area_hull={area_hull:.1f} area_alpha={area_alpha:.1f}")
