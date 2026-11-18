# -*- coding: utf-8 -*-
"""第 06 章 图 1：ICtCp 的编码流程（BT.2100），横向流水线框图。"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt = H.plt

fig = plt.figure(figsize=(8.8, 3.4))
ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
ax.set_xlim(0, 10.0)
ax.set_ylim(0, 4.0)
ax.axis("off")

STYLE = {
    "io":  dict(fc="#e9eff6", ec="#7d94ad"),
    "enc": dict(fc="#dae6f2", ec=H.NAVY),
    "mix": dict(fc="#e4f0ea", ec=H.TEAL),
    "out": dict(fc="#fbe9dc", ec=H.ORANGE),
}

Hh = 1.26
SPEC = [(0.15, 1.66, "线性 RGB", [r"$R,\;G,\;B$", "峰值归一化"], "io", 8.4, 8.0),
        (1.99, 1.66, "PQ 编码", [r"$R'=\mathrm{PQ}(R\,L_p)$", r"$L_p$：峰值 cd/m$^2$"],
         "enc", 8.4, 7.6),
        (3.83, 1.90, "转入 LMS 锥空间",
         [r"$(L\,M\,S)^{\mathsf{T}}=M_1(R'G'B')^{\mathsf{T}}$", r"$M_1$：BT.2100 定点矩阵"],
         "enc", 8.2, 7.2),
        (5.93, 2.10, "三轴组合",
         [r"$I=0.5L+0.5M$", r"$C_t=(6610L-13613M+7003S)/4096$"], "mix", 8.4, 6.5),
        (8.23, 1.62, "量化与子采样", ["I 保持全分辨率", "Ct、Cp 可降至 4:2:0"], "out", 8.4, 7.6)]

Y = 1.42
for x, w, title, forms, style, fs_t, fs_f in SPEC:
    ax.add_patch(FancyBboxPatch((x, Y), w, Hh,
                                boxstyle="round,pad=0.015,rounding_size=0.08",
                                linewidth=1.15, facecolor=STYLE[style]["fc"],
                                edgecolor=STYLE[style]["ec"], zorder=2))
    ax.text(x + w / 2, Y + Hh - 0.22, title, ha="center", va="center",
            fontsize=fs_t, color="#16232f", zorder=3)
    for i, f in enumerate(forms):
        ax.text(x + w / 2, Y + Hh - 0.56 - 0.28 * i, f, ha="center", va="center",
                fontsize=fs_f, color="#1b2b3a", zorder=3)

for i in range(len(SPEC) - 1):
    x0 = SPEC[i][0] + SPEC[i][1] + 0.03
    x1 = SPEC[i + 1][0] - 0.03
    ax.add_patch(FancyArrowPatch((x0, Y + Hh / 2), (x1, Y + Hh / 2), arrowstyle="-|>",
                                 mutation_scale=11, linewidth=1.2, color="#39485a",
                                 zorder=1, shrinkA=1, shrinkB=1))

ax.text(5.0, 3.45,
        "PQ 先把绝对亮度压成近似均匀的码值，再做线性矩阵，$I$ 因此近似正比于编码亮度；"
        "$C_t$、$C_p$ 的取值范围约为 $[-0.5,\\,0.5]$",
        fontsize=8.0, color="#39485a", ha="center", va="center")

ax.text(6.98, Y - 0.30, "$S$ 只进入 $C_t$、$C_p$，亮度轴不吸收色度",
        fontsize=7.6, color="#0f5f50", ha="center", va="center")

ax.text(5.0, 0.42,
        "解码：由 $I$、$C_t$、$C_p$ 反解 $L\\,M\\,S$，乘 $M_1^{-1}$ 得 $R'G'B'$，再经 PQ EOTF 回到线性光",
        fontsize=8.0, color="#39485a", ha="center", va="center")

H.save(fig, 6, "f1_ictcp_pipeline")
