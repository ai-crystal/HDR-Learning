# -*- coding: utf-8 -*-
"""第 05 章 图 6：色域映射的评价——色差统计与色相偏移分布。

源色域 BT.2020，目标 Display P3，样本为 BT.2020 立方体中落在 P3 之外的颜色
（26 格网格，L* > 10，共 7049 个）。
左图：三种映射的 ΔE00 统计量；右图：色相偏移绝对值的累积分布。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import gamut as G

plt = H.plt

DST = "P3"


def clamp_map(lab, dst=DST):
    return G.rgb_to_lab(np.clip(G.lab_to_rgb(lab, dst), 0.0, 1.0), dst)


def lch_clip(lab, dst=DST):
    L, C, h = G.lab_to_lch(lab)
    Cm = np.array([G.max_chroma(Li, hi, dst) for Li, hi in zip(L, h)])
    return G.lch_to_lab(L, np.minimum(C, Cm), h)


def knee_lab(lab, dst=DST, k=0.85):
    L, C, h = G.lab_to_lch(lab)
    out = []
    for Li, hi, ci in zip(L, h, C):
        Cm = G.max_chroma(Li, hi, dst)
        out.append(float(G.knee_map(np.array([ci]), k * Cm, Cm)[0]))
    return G.lch_to_lab(L, np.array(out), h)


g = np.linspace(0, 1, 26)
R, Gg, B = np.meshgrid(g, g, g, indexing="ij")
lab = G.rgb_to_lab(np.stack([R.ravel(), Gg.ravel(), B.ravel()], axis=-1), "BT2020")
mask = (~G.in_gamut(G.lab_to_rgb(lab, DST), 1e-4)) & (lab[:, 0] > 10)
src = lab[mask]

METHODS = [("逐通道裁剪", clamp_map, H.RED), ("等色相裁剪", lch_clip, H.TEAL),
           ("膝形压缩", knee_lab, H.ORANGE)]

stats = []
for name, fn, col in METHODS:
    out = fn(src)
    de = G.dE2000(src, out)
    _, _, h1 = G.lab_to_lch(src)
    _, _, h2 = G.lab_to_lch(out)
    dh = np.abs((h2 - h1 + 180) % 360 - 180)
    stats.append(dict(name=name, col=col, de=de, dh=dh))

fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.7),
                         gridspec_kw=dict(width_ratios=[1.0, 1.05], wspace=0.29))
fig.subplots_adjust(left=0.085, right=0.985, top=0.90, bottom=0.16)

# ---------------- (a) ΔE00 统计 ----------------
ax = axes[0]
xs = np.arange(3)
q = [("均值", [s["de"].mean() for s in stats], 0.55),
     ("95 分位", [np.percentile(s["de"], 95) for s in stats], 0.72),
     ("最大", [s["de"].max() for s in stats], 0.86)]
for i, (lab_q, vals, alpha) in enumerate(q):
    ax.bar(xs + (i - 1) * 0.26, vals, width=0.24,
           color=[s["col"] for s in stats], alpha=alpha, edgecolor="#3b4653",
           linewidth=0.5, label=lab_q)
ax.set_xticks(xs)
ax.set_xticklabels([s["name"] for s in stats], fontsize=8.6)
ax.set_ylabel("$\\Delta E_{00}$", fontsize=9.8)
ax.set_ylim(0, 30)
ax.legend(loc="upper left", fontsize=7.8, ncol=3, columnspacing=0.9,
          handletextpad=0.4, borderpad=0.35)
ax.grid(axis="x", visible=False)
for i, s in enumerate(stats):
    ax.text(i, 1.2, f"{s['de'].mean():.2f}", ha="center", fontsize=7.2, color="white")

# ---------------- (b) 色相偏移的累积分布 ----------------
ax2 = axes[1]
grid_x = np.linspace(0, 16, 400)
LW = {H.RED: 2.1, H.TEAL: 3.6, H.ORANGE: 1.7}
LS = {H.RED: "-", H.TEAL: "-", H.ORANGE: (0, (5, 2.5))}
for s in stats:
    cdf = np.array([(s["dh"] <= x).mean() for x in grid_x]) * 100.0
    ax2.plot(grid_x, cdf, color=s["col"], lw=LW[s["col"]], ls=LS[s["col"]],
             label=s["name"])
ax2.text(9.0, 96.5, "等色相裁剪与膝形压缩全为 0", fontsize=7.2, color="#39485a",
         ha="center", va="top")
ax2.axvline(2.0, color="#6b7886", lw=1.0, ls=(0, (4, 2.5)))
ax2.text(2.35, 8, "2°", fontsize=7.8, color="#6b7886")
ax2.set_xlim(0, 16)
ax2.set_ylim(0, 108)
ax2.set_xlabel("色相偏移的绝对值 $|\\Delta h_{ab}|$（°）", fontsize=9.5)
ax2.set_ylabel("样本累积比例（%）", fontsize=9.5)
ax2.legend(loc="center right", fontsize=7.8, handletextpad=0.6, borderpad=0.35)
ax2.annotate(f"{100 * (stats[0]['dh'] > 2).mean():.0f}% 的样本超过 2°",
             xy=(2.2, 53), xytext=(5.2, 30), fontsize=7.6, color=H.RED,
             arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=0.9,
                             shrinkA=2, shrinkB=3))

H.save(fig, 5, "f6_mapping_metrics")
