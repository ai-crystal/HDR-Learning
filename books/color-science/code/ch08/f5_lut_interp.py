# -*- coding: utf-8 -*-
"""第 08 章 图 3：3D LUT 的格点几何、四面体权重与格点分配对精度的影响。

(a) 一个 CLUT 单元的八个顶点，被选中的四面体与输入落点
(b) 四面体四个顶点的权重随 $r_z$ 的变化，分段线性
(c) 平均色差随格点数的变化：按码值均分与按线性光均分
    误差来自一个"先串扰、后幂次"的器件模型（示意），不是实测
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import cms_util as C

plt = H.plt
plt.rcParams["mathtext.fontset"] = "dejavusans"

fig = plt.figure(figsize=(7.5, 3.1))
gs = fig.add_gridspec(1, 3, width_ratios=[1.05, 1.0, 1.15], wspace=0.42)

# ---------------- (a) 立方体与四面体 ----------------
ax = fig.add_subplot(gs[0, 0], projection="3d")
ax.set_axis_off()
ax.view_init(elev=20, azim=-62)

corners = [(i, j, k) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
for (i, j, k) in corners:
    for d in range(3):
        n = [i, j, k]
        if n[d] == 0:
            n[d] = 1
            ax.plot([i, n[0]], [j, n[1]], [k, n[2]], color="#c8d0d8", lw=0.8,
                    zorder=1)

tetra = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]
for a in range(4):
    for b in range(a + 1, 4):
        p, q = tetra[a], tetra[b]
        ax.plot([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], color=H.ORANGE,
                lw=1.7, zorder=5)

for (i, j, k) in corners:
    inside = (i, j, k) in tetra
    ax.scatter([i], [j], [k], s=34 if inside else 22,
               color=H.ORANGE if inside else "white",
               edgecolor=H.ORANGE if inside else "#9aa7b4",
               linewidth=0.9, zorder=8 if inside else 4, depthshade=False)
    dx = 0.05 if i == 1 else -0.05
    dy = 0.05 if j == 1 else -0.05
    ax.text(i + dx, j + dy, k + 0.05, f"{i}{j}{k}", fontsize=5.6,
            color=H.DARK if inside else H.GRAY, zorder=9,
            ha="left" if i == 1 else "right")

ax.scatter([0.80], [0.55], [0.35], marker="*", s=48, color=H.NAVY,
           edgecolor="white", linewidth=0.5, zorder=10, depthshade=False)
ax.text(0.82, 0.58, 0.42, "输入落点", fontsize=5.8, color=H.NAVY, zorder=10)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)
ax.set_box_aspect((1, 1, 1))
ax.text2D(0.02, -0.10, "(a) 一个 CLUT 单元", fontsize=7.0, color=H.DARK,
          transform=ax.transAxes)
ax.text2D(0.02, 0.93, "橙色为 $r_x \\geq r_y \\geq r_z$\n时选中的那个四面体",
          fontsize=6.0, color=H.GRAY, transform=ax.transAxes, linespacing=1.4)

# ---------------- (b) 权重随小数部分的变化 ----------------
ax = fig.add_subplot(gs[0, 1])
rx, ry = 0.72, 0.48
rz = np.linspace(0, ry, 200)
w000 = np.full_like(rz, 1 - rx)
w100 = np.full_like(rz, rx - ry)
w110 = ry - rz
w111 = rz

ax.plot(rz, w000, color=H.NAVY, lw=1.6, label="$c_{000}=1-r_x$")
ax.plot(rz, w100, color=H.TEAL, lw=1.6, label="$c_{100}=r_x-r_y$")
ax.plot(rz, w110, color=H.ORANGE, lw=1.8, label="$c_{110}=r_y-r_z$")
ax.plot(rz, w111, color=H.RED, lw=1.8, label="$c_{111}=r_z$")
ax.set_xlim(0, ry)
ax.set_ylim(0, 0.62)
ax.set_xlabel("$r_z$（$r_x=0.72$，$r_y=0.48$）", fontsize=7.6)
ax.set_ylabel("顶点权重", fontsize=8)
ax.set_title("(b) 四面体内的权重", fontsize=7.6, pad=4)
ax.legend(loc="upper right", fontsize=5.4, handlelength=1.3,
          labelspacing=0.16, borderaxespad=0.12)
ax.annotate("$r_z=r_y$\n换到下一个四面体", (ry, 0.012), xytext=(0.04, 0.10),
            fontsize=5.4, color=H.GRAY, ha="left", va="bottom",
            linespacing=1.4,
            arrowprops=dict(arrowstyle="-|>", color=H.GRAY, lw=0.6))

# ---------------- (c) 格点分配与误差 ----------------
ax = fig.add_subplot(gs[0, 2])

A = np.array([[1.00, 0.10, 0.04],
              [0.05, 1.00, 0.09],
              [0.03, 0.07, 1.00]])
A = A / (A @ np.ones(3))[:, None]
rng = np.random.default_rng(8)
u = rng.random((2500, 3))


def want(u):
    return np.clip(A @ C.srgb_eotf(u).T, 0, 1).T


def target(u):
    return C.srgb_oetf(want(u))


def trilinear(vals, f):
    N = vals.shape[0]
    i0 = np.clip(np.floor(f).astype(int), 0, N - 2)
    t = f - i0
    out = np.zeros((len(f), 3))
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = ((t[:, 0] if dx else 1 - t[:, 0])
                     * (t[:, 1] if dy else 1 - t[:, 1])
                     * (t[:, 2] if dz else 1 - t[:, 2]))
                out += w[:, None] * vals[i0[:, 0] + dx, i0[:, 1] + dy,
                                         i0[:, 2] + dz]
    return out


ref = C.xyz_to_lab(want(u) @ C.M_SRGB.T)
Ns = [5, 9, 17, 33, 65]
e_code, e_lin = [], []
for N in Ns:
    g = np.linspace(0, 1, N)
    G = np.array(np.meshgrid(g, g, g, indexing="ij")).reshape(3, -1).T
    tab_code = target(G).reshape(N, N, N, 3)
    tab_lin = target(C.srgb_oetf(G)).reshape(N, N, N, 3)
    out1 = trilinear(tab_code, u * (N - 1))
    out2 = trilinear(tab_lin, C.srgb_eotf(u) * (N - 1))
    e_code.append(C.delta_e00(ref, C.xyz_to_lab(C.srgb_eotf(out1) @ C.M_SRGB.T)).mean())
    e_lin.append(C.delta_e00(ref, C.xyz_to_lab(C.srgb_eotf(out2) @ C.M_SRGB.T)).mean())

ax.loglog(Ns, e_lin, "s--", color=H.RED, ms=4, lw=1.6, label="按线性光均分")
ax.loglog(Ns, e_code, "o-", color=H.NAVY, ms=4, lw=1.7, label="按码值均分")
ref_line = e_code[1] * (np.array(Ns) / Ns[1]) ** -2.0
ax.loglog(Ns, ref_line, ":", color=H.GRAY, lw=1.2, label="斜率参考")
ax.set_xlabel("每维格点数 $N$", fontsize=8)
ax.set_ylabel("平均 $\\Delta E_{00}$", fontsize=8)
ax.set_title("(c) 格点分配对精度的影响", fontsize=7.6, pad=4)
ax.set_xticks(Ns)
ax.set_xticklabels([str(n) for n in Ns])
ax.minorticks_off()
ax.set_yticks([0.002, 0.01, 0.05, 0.2, 1.0])
ax.set_yticklabels(["0.002", "0.01", "0.05", "0.2", "1"])
ax.set_ylim(0.0015, 3.0)
ax.legend(loc="lower left", fontsize=5.6, handlelength=1.5,
          labelspacing=0.2, borderaxespad=0.22)

ax.annotate("0.119", (9, e_code[1]), textcoords="offset points", xytext=(1, 7),
            fontsize=5.2, color=H.NAVY, ha="center")
ax.annotate("1.01", (9, e_lin[1]), textcoords="offset points", xytext=(2, -9),
            fontsize=5.2, color=H.RED, ha="center")

H.save(fig, 8, "f5_lut_interp")
print("code", ["%.4f" % v for v in e_code])
print("lin", ["%.4f" % v for v in e_lin])
