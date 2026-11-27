# -*- coding: utf-8 -*-
"""第 04 章 图 4：CAM02 与 CAM16 的锥空间路径对比，以及短波端的负响应。

上图：两条计算路径的方框图（matplotlib 绘制）。
下图：380–780 nm 单色光的 R 通道（长波锥）响应；
      CAT02 在 432–478 nm 之间为负（465 nm 处最低 −0.032），CAT16 全段为正。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cam02 as C
import cie1931 as S

plt = H.plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig = plt.figure(figsize=(7.2, 5.0))
gs = fig.add_gridspec(2, 1, height_ratios=[1.52, 1.0], hspace=0.20,
                      left=0.02, right=0.98, top=0.98, bottom=0.10)

# ================= 上图：路径框图 =================
ax = fig.add_subplot(gs[0])
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.2)
ax.axis("off")

STYLE = {
    "io":  dict(fc="#e9eff6", ec="#7d94ad"),
    "a":   dict(fc="#dae6f2", ec=H.NAVY),
    "b":   dict(fc="#e4f0ea", ec=H.TEAL),
    "out": dict(fc="#fbe9dc", ec=H.ORANGE),
}


def box(x0, y0, w, h, lines, style="io", fs=7.2, title_fs=8.4):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.11",
                                linewidth=1.05, facecolor=STYLE[style]["fc"],
                                edgecolor=STYLE[style]["ec"], zorder=2))
    ax.text(x0 + w / 2, y0 + h - 0.28, lines[0], ha="center", va="center",
            fontsize=title_fs, color="#16232f", zorder=3)
    for i, s in enumerate(lines[1:]):
        ax.text(x0 + w / 2, y0 + h - 0.70 - 0.42 * i, s, ha="center",
                va="center", fontsize=fs, color="#1b2b3a", zorder=3)


def arrow(p0, p1, color="#39485a", ls="-"):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=10,
                                 linewidth=1.1, color=color, zorder=1,
                                 linestyle=ls, shrinkA=1.0, shrinkB=1.0))


ax.text(0.08, 5.85, "CAM02：适应与压缩分处两个锥空间", fontsize=8.6, color=H.NAVY,
        va="center")
box(0.08, 4.28, 1.15, 0.95, ["刺激", r"$X,Y,Z$"], "io")
box(1.60, 4.16, 2.65, 1.55, ["① CAT02 空间内做适应",
                             r"$R,G,B=M_{\mathrm{CAT02}}[X,Y,Z]^{\mathsf{T}}$",
                             r"$R_c=(D\,Y_w/R_w+1-D)\,R$"], "a")
box(4.62, 4.16, 2.65, 1.55, ["② 退回 XYZ，再进 HPE",
                             r"$R'G'B'=M_{\mathrm{HPE}}M_{\mathrm{CAT02}}^{-1}R_cG_cB_c$",
                             r"（多一次矩阵往返）"], "a")
box(7.62, 4.28, 2.05, 1.28, ["③ 锥响应压缩", r"$q=F_LR'/100$",
                             r"$400q^{0.42}/(q^{0.42}+27.13)+0.1$"], "b", fs=6.6)
arrow((1.23, 4.75), (1.58, 4.78))
arrow((4.25, 4.93), (4.60, 4.93))
arrow((7.27, 4.93), (7.60, 4.93))

ax.text(0.08, 3.28, "CAM16：同一个锥空间里做适应与压缩", fontsize=8.6, color=H.TEAL,
        va="center")
box(0.08, 1.42, 1.15, 0.95, ["刺激", r"$X,Y,Z$"], "io")
box(1.60, 1.30, 2.65, 1.55, ["① CAT16 空间内做适应",
                             r"$R,G,B=M_{\mathrm{CAT16}}[X,Y,Z]^{\mathsf{T}}$",
                             r"$R_c=(D\,Y_w/R_w+1-D)\,R$"], "b")
box(4.62, 1.30, 2.65, 1.55, ["② 同一空间内压缩",
                             r"$q=F_LR_c/100$",
                             r"$R_a=400\,q^{0.42}/(q^{0.42}+27.13)+0.1$"], "b")
box(7.62, 1.42, 2.05, 1.28, ["③ 输出", r"$R_a,\;G_a,\;B_a$"], "out", fs=7.6)
arrow((1.23, 1.90), (1.58, 1.93))
arrow((4.25, 2.08), (4.60, 2.08))
arrow((7.27, 2.08), (7.60, 2.08))

ax.add_patch(FancyArrowPatch((3.05, 4.10), (3.05, 3.10), arrowstyle="-|>",
                             mutation_scale=9, linewidth=1.0, color=H.RED,
                             linestyle=(0, (4, 2.5)), zorder=1))
ax.text(3.18, 3.58, "省掉一次矩阵往返，色相不再被第二次变换扭曲", fontsize=7.2,
        color=H.RED, va="center", ha="left")

ax.text(0.08, 0.72,
        r"两段合起来的等效矩阵 $M_{\mathrm{HPE}}M_{\mathrm{CAT02}}^{-1}$ 三行为 "
        r"(0.741, 0.218, 0.041)、(0.285, 0.624, 0.090)、(-0.010, -0.006, 1.015)，"
        r"适应增益 $D$ 只能加在 CAT02 空间；",
        fontsize=7.0, color="#39485a", va="center")
ax.text(0.08, 0.28,
        r"$M_{\mathrm{CAT16}}$ 三行为 (0.401, 0.650, -0.051)、(-0.250, 1.204, 0.046)、"
        r"(-0.002, 0.049, 0.953)，把适应与压缩放在一条直通路径上。",
        fontsize=7.0, color="#39485a", va="center")

# ================= 下图：R 通道的光谱响应 =================
ax2 = fig.add_subplot(gs[1])
lam = S.LAM
XYZ = np.stack([S.XBAR, S.YBAR, S.ZBAR], axis=-1)
r_cat02 = (XYZ @ C.M_CAT02.T)[:, 0]
r_cat16 = (XYZ @ C.M_CAT16.T)[:, 0]
r_hpe = (XYZ @ C.M_HPE.T)[:, 0]

ax2.plot(lam, r_hpe, color=H.GRAY, ls=(0, (4, 2)), lw=1.5, label="HPE 的 R 通道")
ax2.plot(lam, r_cat16, color=H.TEAL, lw=2.0, label="CAT16 的 R 通道")
ax2.plot(lam, r_cat02, color=H.NAVY, lw=2.0, label="CAT02 的 R 通道")
ax2.axhline(0, color="#4a5666", lw=1.0)

zs = np.where(r_cat02 < 0)[0]
ax2.fill_between(lam[zs], r_cat02[zs], 0, color=H.RED, alpha=0.28, lw=0)
ax2.annotate("CAT02 在 432–478 nm 之间为负，\n465 nm 处最低，为 -0.032",
             xy=(462, -0.028), xytext=(390, 0.58), fontsize=7.6, color=H.RED,
             va="center", ha="left",
             arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=1.0,
                             shrinkA=3, shrinkB=3))
ax2.set_xlim(380, 780)
ax2.set_ylim(-0.13, 1.10)
ax2.set_xlabel("波长 (nm)", fontsize=9.5)
ax2.set_ylabel("R 通道响应（同一白点归一）", fontsize=9.5)
ax2.legend(loc="upper right", fontsize=8.0, ncol=1, handlelength=1.9)
ax2.grid(alpha=0.55)

H.save(fig, 4, "f4_cam16_path")
