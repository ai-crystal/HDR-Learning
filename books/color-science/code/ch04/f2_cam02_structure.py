# -*- coding: utf-8 -*-
"""第 04 章 图 2：CIECAM02 的正向计算流程（方框流程图，matplotlib 绘制）。"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt = H.plt

fig = plt.figure(figsize=(7.0, 6.5))
ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
ax.set_xlim(0, 7.0)
ax.set_ylim(0, 6.5)
ax.axis("off")

STYLE = {
    "in":  dict(fc="#e9eff6", ec="#7d94ad"),
    "cat": dict(fc="#dae6f2", ec=H.NAVY),
    "nl":  dict(fc="#e4f0ea", ec=H.TEAL),
    "out": dict(fc="#fbe9dc", ec=H.ORANGE),
}


def box(x0, y0, w, h, title, formulas, style="in", fs_t=9.2, fs_f=8.4, lh=0.26):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h,
                                boxstyle="round,pad=0.015,rounding_size=0.09",
                                linewidth=1.15, facecolor=STYLE[style]["fc"],
                                edgecolor=STYLE[style]["ec"], zorder=2))
    ax.text(x0 + w / 2, y0 + h - 0.20, title, ha="center", va="center",
            fontsize=fs_t, color="#16232f", zorder=3)
    for i, f in enumerate(formulas):
        ax.text(x0 + w / 2, y0 + h - 0.20 - lh * (i + 1) - 0.02, f,
                ha="center", va="center", fontsize=fs_f, color="#1b2b3a", zorder=3)


def arrow(p0, p1, ls="-", color="#39485a", lw=1.2):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=11,
                                 linewidth=lw, color=color, zorder=1,
                                 linestyle=ls, shrinkA=1.5, shrinkB=1.0))


box(0.35, 5.60, 2.55, 0.62, "刺激三刺激值", [r"$X,\;Y,\;Z$"], "in")
box(3.85, 5.60, 2.80, 0.62, "参考白（适应白）", [r"$X_w,\;Y_w,\;Z_w$"], "in")

box(1.15, 4.42, 4.70, 1.00, "① CAT02 色适应（含适应程度 D）",
    [r"$D=F\,[\,1-e^{(-L_A-42)/92}/3.6\,]$",
     r"$R_c=(D\,Y_w/R_w+1-D)\,R$"], "cat", fs_f=8.6)

box(1.15, 3.52, 4.70, 0.78, "② 转入 Hunt-Pointer-Estevez 锥空间",
    [r"$L'M'S'=M_{HPE}\,M_{CAT02}^{-1}\,(R_cG_cB_c)^{\mathsf{T}}$"], "cat", fs_f=8.6)

box(1.15, 2.50, 4.70, 0.98, "③ 锥响应非线性压缩（$L_A$ 决定 $F_L$）",
    [r"$F_L=0.2k^4(5L_A)+0.1(1-k^4)^2(5L_A)^{1/3},\;\;k=1/(5L_A+1)$",
     r"$R_a=400\,\dfrac{(F_L R'/100)^{0.42}}{(F_L R'/100)^{0.42}+27.13}+0.1$"],
    "nl", fs_f=8.4, lh=0.26)

box(0.30, 1.36, 2.85, 0.92, "④ 消色差响应",
    [r"$A=(2R_a+G_a+B_a/20-0.305)\,N_{bb}$",
     r"$N_{bb}=N_{cb}=0.725\,(Y_w/Y_b)^{0.2}$"], "nl", fs_t=9.0, fs_f=8.2)

box(3.85, 1.42, 2.85, 1.06, "⑤ 对立色坐标与色相",
    [r"$a=R_a-12G_a/11+B_a/11$",
     r"$b=(R_a+G_a-2B_a)/9$",
     r"$h=\arctan(b/a),\;\;e_t=\frac{1}{4}[\cos(h+2)+3.8]$"], "nl",
    fs_t=9.0, fs_f=7.7, lh=0.235)

box(0.30, 0.28, 2.85, 1.02, "⑥ 明度 J 与亮度 Q",
    [r"$J=100\,(A/A_w)^{cz},\;\;z=1.48+\sqrt{n}$",
     r"$Q=\dfrac{4}{c}\sqrt{J/100}\,(A_w+4)\,F_L^{1/4}$"],
    "out", fs_t=9.0, fs_f=8.2)

box(3.85, 0.26, 2.85, 1.08, "⑦ 彩度 C、色彩量 M、饱和度 s",
    [r"$t=\dfrac{50000}{13}N_cN_{cb}e_t\dfrac{\sqrt{a^2+b^2}}{R_a+G_a+21B_a/20}$",
     r"$C=t^{0.9}\sqrt{J/100}\,(1.64-0.29^n)^{0.73}$"],
    "out", fs_t=9.0, fs_f=7.8, lh=0.28)

arrow((1.62, 5.60), (2.30, 5.44))
arrow((5.25, 5.60), (4.70, 5.44))
arrow((3.50, 4.42), (3.50, 4.30))
arrow((3.50, 3.52), (3.50, 3.48))
arrow((2.35, 2.50), (1.72, 2.30))
arrow((4.70, 2.50), (5.28, 2.46))
arrow((1.72, 1.36), (1.72, 1.30))
arrow((5.28, 1.42), (5.28, 1.34))
arrow((3.15, 0.80), (3.85, 0.80), ls=(0, (4, 2.5)), color=H.RED, lw=1.1)
ax.text(3.50, 0.89, "J 参与", ha="center", va="bottom", fontsize=7.6, color=H.RED)

ax.text(3.50, 0.09,
        "视环境参数：适应亮度 $L_A$（cd/m$^2$）、背景亮度因数 $Y_b$、环绕因子 $F$、$c$、$N_c$；"
        "$n=Y_b/Y_w$，$M=CF_L^{1/4}$，$s=100\\sqrt{M/Q}$",
        ha="center", va="center", fontsize=7.6, color="#39485a")

H.save(fig, 4, "f2_cam02_structure")
