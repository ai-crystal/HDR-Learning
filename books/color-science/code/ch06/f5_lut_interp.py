# -*- coding: utf-8 -*-
"""第 06 章 图 5：3D LUT 的网格、插值方式与误差。

左图：一个 CLUT 单元与四面体剖分（插值只用 4 个顶点）。
右图：同一个非线性"显示器模型"下，三线性与四面体插值的误差随网格密度的变化。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import ictcp as I

plt = H.plt
from matplotlib.patches import Polygon

M = np.array([[0.41, 0.36, 0.18], [0.21, 0.72, 0.07], [0.02, 0.12, 0.95]])


def device(rgb):
    """合成器件模型：逐通道伽马 + 通道间串扰，输出归一化 XYZ。"""
    lin = np.clip(rgb, 0, 1) ** 2.2
    cross = lin * (1.0 + 0.12 * np.roll(lin, 1, axis=-1))
    return cross @ M.T


def build_lut(n):
    g = np.linspace(0, 1, n)
    R, G, B = np.meshgrid(g, g, g, indexing="ij")
    rgb = np.stack([R, G, B], axis=-1)
    return device(rgb)


def trilinear(lut, q):
    n = lut.shape[0]
    p = np.clip(q, 0, 1) * (n - 1)
    i0 = np.minimum(np.floor(p).astype(int), n - 2)
    f = p - i0
    i1 = i0 + 1
    out = np.zeros(q.shape)
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = ((f[..., 0] if dx else 1 - f[..., 0]) *
                     (f[..., 1] if dy else 1 - f[..., 1]) *
                     (f[..., 2] if dz else 1 - f[..., 2]))
                out += w[..., None] * lut[i0[:, 0] + dx, i0[:, 1] + dy, i0[:, 2] + dz]
    return out


def tetrahedral(lut, q):
    n = lut.shape[0]
    p = np.clip(q, 0, 1) * (n - 1)
    i0 = np.minimum(np.floor(p).astype(int), n - 2)
    f = p - i0
    fx, fy, fz = f[..., 0], f[..., 1], f[..., 2]
    i0x, i0y, i0z = i0[:, 0], i0[:, 1], i0[:, 2]
    c000 = lut[i0x, i0y, i0z]
    c100 = lut[i0x + 1, i0y, i0z]
    c010 = lut[i0x, i0y + 1, i0z]
    c001 = lut[i0x, i0y, i0z + 1]
    c110 = lut[i0x + 1, i0y + 1, i0z]
    c101 = lut[i0x + 1, i0y, i0z + 1]
    c011 = lut[i0x, i0y + 1, i0z + 1]
    c111 = lut[i0x + 1, i0y + 1, i0z + 1]
    out = np.zeros(q.shape)
    # 按 fx/fy/fz 的大小关系分六种情况
    m0 = (fx > fy) & (fy > fz)
    m1 = (fx > fy) & (fy <= fz) & (fx > fz)
    m2 = (fx > fy) & (fx <= fz)
    m3 = (fx <= fy) & (fy > fz) & (fx > fz)
    m4 = (fx <= fy) & (fy > fz) & (fx <= fz)
    m5 = (fx <= fy) & (fy <= fz)
    cases = [
        (m0, lambda: c000 + fx[..., None] * (c100 - c000) + fy[..., None] * (c110 - c100)
         + fz[..., None] * (c111 - c110)),
        (m1, lambda: c000 + fz[..., None] * (c001 - c000) + fx[..., None] * (c101 - c001)
         + fy[..., None] * (c111 - c101)),
        (m2, lambda: c000 + fz[..., None] * (c001 - c000) + fy[..., None] * (c011 - c001)
         + fx[..., None] * (c111 - c011)),
        (m3, lambda: c000 + fy[..., None] * (c010 - c000) + fx[..., None] * (c110 - c010)
         + fz[..., None] * (c111 - c110)),
        (m4, lambda: c000 + fy[..., None] * (c010 - c000) + fz[..., None] * (c011 - c010)
         + fx[..., None] * (c111 - c011)),
        (m5, lambda: c000 + fz[..., None] * (c001 - c000) + fy[..., None] * (c011 - c001)
         + fx[..., None] * (c111 - c011)),
    ]
    for mask, fn in cases:
        val = fn()
        out[mask] = val[mask]
    return out


rng = np.random.default_rng(7)
Q = rng.uniform(0, 1, size=(4000, 3))
truth = device(Q)

fig = plt.figure(figsize=(7.6, 3.9))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.06], wspace=0.28,
                      left=0.055, right=0.985, top=0.90, bottom=0.16)

# ---------------- (a) 单元与四面体 ----------------
ax = fig.add_subplot(gs[0])
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)

# 简易等轴投影：x 向右，y 向上，z 向右上
o = np.array([1.0, 1.2])


def P(x, y, z):
    return o + np.array([x * 3.4 + z * 2.0, y * 3.4 + z * 1.5])


V = {k: P(*v) for k, v in {
    "000": (0, 0, 0), "100": (1, 0, 0), "010": (0, 1, 0), "001": (0, 0, 1),
    "110": (1, 1, 0), "101": (1, 0, 1), "011": (0, 1, 1), "111": (1, 1, 1)}.items()}

for a, b, ls, col in [("000", "100", "-", "#8a97a6"), ("100", "110", "-", "#8a97a6"),
                      ("110", "010", "-", "#8a97a6"), ("010", "000", "-", "#8a97a6"),
                      ("001", "101", "-", "#8a97a6"), ("101", "111", "-", "#8a97a6"),
                      ("111", "011", "-", "#8a97a6"), ("011", "001", "-", "#8a97a6"),
                      ("000", "001", "-", "#8a97a6"), ("100", "101", "-", "#8a97a6"),
                      ("010", "011", "-", "#8a97a6"), ("110", "111", "-", "#8a97a6")]:
    ax.plot([V[a][0], V[b][0]], [V[a][1], V[b][1]], ls, color=col, lw=1.1, zorder=1)

# 四面体 000-100-110-111 高亮（两个可见三角面）
for tri, al in [(["000", "100", "110"], 0.30), (["000", "110", "111"], 0.18)]:
    ax.add_patch(Polygon([V[k] for k in tri], closed=True, facecolor=H.TEAL,
                         alpha=al, edgecolor=H.TEAL, lw=1.3, zorder=2))

TET = ["000", "100", "110", "111"]
for k, v in V.items():
    col = H.TEAL if k in TET else "#3b4653"
    ax.plot(v[0], v[1], "o", ms=5.6, mfc="white", mec=col, mew=1.6, zorder=4)

sp = P(0.62, 0.75, 0.2)
ax.plot(sp[0], sp[1], "*", ms=12, mfc=H.ORANGE, mec="#8a5a12", mew=0.8, zorder=5)
ax.annotate("输入落在格点之间", xy=(sp[0], sp[1]), xytext=(sp[0] - 0.3, sp[1] + 1.55),
            fontsize=7.6, color="#8a5a12", ha="center",
            arrowprops=dict(arrowstyle="-|>", color="#8a5a12", lw=0.9,
                            shrinkA=2, shrinkB=4))
ax.text(V["000"][0] - 0.10, V["000"][1] - 0.80, "立方体共 8 个顶点，三线性 8 个都要用",
        fontsize=7.2, color="#4a5666", ha="left")
ax.text(2.55, 7.15, "四面体只取其中 4 个（青色实心边）", fontsize=7.2, color="#0f5f50",
        ha="left")

# ---------------- (b) 误差随网格密度 ----------------
ax2 = fig.add_subplot(gs[1])
NS = [9, 17, 33, 65]
err_tri, err_tet = [], []
for n in NS:
    lut = build_lut(n)
    e1 = device(Q) - trilinear(lut, Q)
    e2 = device(Q) - tetrahedral(lut, Q)
    lab0 = I.xyz_to_lab(truth / 1.0, white=(0.95047, 1.0, 1.08883))
    err_tri.append(float(np.mean(I.deltaE_2000(
        lab0, I.xyz_to_lab(np.clip(trilinear(lut, Q), 1e-4, None), white=(0.95047, 1.0, 1.08883))))))
    err_tet.append(float(np.mean(I.deltaE_2000(
        lab0, I.xyz_to_lab(np.clip(tetrahedral(lut, Q), 1e-4, None), white=(0.95047, 1.0, 1.08883))))))

ax2.plot(NS, err_tri, "-o", color=H.RED, lw=2.0, ms=5, label="三线性插值")
ax2.plot(NS, err_tet, "-s", color=H.TEAL, lw=2.0, ms=4.6, label="四面体插值")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xticks(NS)
ax2.set_xticklabels([str(n) for n in NS])
ax2.xaxis.set_minor_formatter(plt.NullFormatter())
ax2.set_ylim(0.003, 1.15)
ax2.set_xlabel("每维格点数 $N$（共 $N^3$ 个格点）", fontsize=9.5)
ax2.set_ylabel("平均 $\\Delta E_{00}$", fontsize=9.5)
ax2.legend(loc="lower left", fontsize=8.0, handletextpad=0.6, borderpad=0.35)
for n, v in zip(NS, err_tet):
    ax2.annotate(f"{v:.3f}", xy=(n, v), xytext=(0, 10), textcoords="offset points",
                 fontsize=7.0, color="#0f5f50", ha="center")
for n, v in zip(NS, err_tri):
    ax2.annotate(f"{v:.3f}", xy=(n, v), xytext=(0, -15), textcoords="offset points",
                 fontsize=7.0, color="#8a3a2e", ha="center")

H.save(fig, 6, "f5_lut_interp")
