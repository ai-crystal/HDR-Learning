# -*- coding: utf-8 -*-
"""第 01 章 图 1：光谱功率分布与光度量的加权积分。

左：6500 K 黑体光谱（普朗克公式）与 CIE 1924 明视觉函数 V(λ) 相乘，乘积的积分
    就是光度量；两条曲线各自按峰值归一到 1，乘积同样归一到 1 以便观察形状。
右：CIE 1924 明视觉 V(λ) 与 CIE 1951 暗视觉 V'(λ)，各自归一，峰值分别在
    555 nm 与 507 nm，权重常数 Km = 683 lm/W 与 K'm = 1700 lm/W。
暗视觉数据取 CIE 1951 的 10 nm 表格值（380–700 nm，507 nm 处峰值为 1）。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C

plt = H.plt

# ---------------- CIE 1951 暗视觉光谱光视效率（10 nm 间隔） ----------------
_SCOT = """
380 0.000589
390 0.002209
400 0.009290
410 0.034840
420 0.096600
430 0.199800
440 0.328100
450 0.455000
460 0.567000
470 0.676000
480 0.793000
490 0.904000
500 0.982000
507 1.000000
510 0.997000
520 0.935000
530 0.811000
540 0.650000
550 0.481000
560 0.328800
570 0.207600
580 0.121200
590 0.065500
600 0.033150
610 0.015930
620 0.007370
630 0.003335
640 0.001497
650 0.000677
660 0.000313
670 0.000148
680 0.0000715
690 0.0000353
700 0.0000178
"""
_d = np.array([[float(t) for t in l.split()] for l in _SCOT.strip().splitlines()])
SCOT_LAM, SCOT_V = _d[:, 0], _d[:, 1]

lam = np.linspace(380.0, 780.0, 801)
V = np.interp(lam, C.LAM, C.YBAR)          # CIE 1924 明视觉，ȳ 即 V(λ)
Vp = np.interp(lam, SCOT_LAM, SCOT_V, right=0.0)

C2 = 1.4388e-2                              # 第二辐射常数，m·K


def planck(T, lam_nm):
    l = lam_nm * 1e-9
    return 1.0 / (l ** 5 * (np.exp(C2 / (l * T)) - 1.0))


spd = planck(6500.0, lam)
spd = spd / spd.max()
prod = spd * V
prod = prod / prod.max()

fig = plt.figure(figsize=(7.2, 4.2))
gs = fig.add_gridspec(1, 2, width_ratios=[1.42, 1.0], wspace=0.30)

# ==================== 左：加权积分 ====================
ax = fig.add_subplot(gs[0])
ax.fill_between(lam, 0, prod, color=H.ORANGE, alpha=0.30, lw=0,
                label="乘积（已归一）")
ax.plot(lam, spd, color=H.NAVY, lw=2.1, label="6500 K 黑体 SPD")
ax.plot(lam, V, color=H.RED, lw=1.9, ls=(0, (5, 2)), label=r"$V(\lambda)$")

ax.text(404, 0.165,
        "乘积的面积即光度量\n"
        r"$L_v=683\int L_{e,\lambda}V\,\mathrm{d}\lambda$",
        fontsize=7.8, color="#8a4b00", ha="left", va="center",
        bbox=dict(facecolor="white", edgecolor=H.LGRAY,
                  boxstyle="round,pad=0.30", lw=0.8))
ax.annotate("", xy=(540, 0.42), xytext=(497, 0.22),
            arrowprops=dict(arrowstyle="->", color="#a86a20", lw=1.0,
                            connectionstyle="arc3,rad=-0.18"))

ax.set_xlim(380, 780)
ax.set_ylim(0, 1.12)
ax.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
ax.set_xlabel("波长 λ（nm）")
ax.set_ylabel("相对值（各曲线峰值归一到 1）")
ax.legend(loc="upper right", fontsize=7.4, bbox_to_anchor=(1.0, 1.0),
          handlelength=1.8, labelspacing=0.3)

# ==================== 右：明视觉与暗视觉 ====================
ax2 = fig.add_subplot(gs[1])
ax2.fill_between(lam, 0, Vp, color=H.PURPLE, alpha=0.12, lw=0)
ax2.plot(lam, V, color=H.RED, lw=2.2, label=r"$V(\lambda)$ 明视觉")
ax2.plot(lam, Vp, color=H.PURPLE, lw=2.2, label=r"$V'(\lambda)$ 暗视觉")
ax2.plot([555], [1.0], "o", ms=5.5, color=H.RED, zorder=6)
ax2.plot([507], [1.0], "o", ms=5.5, color=H.PURPLE, zorder=6)
ax2.text(560, 1.035, "555 nm", fontsize=7.6, color=H.RED, ha="left",
         va="bottom")
ax2.text(500, 1.035, "507 nm", fontsize=7.6, color=H.PURPLE, ha="right",
         va="bottom")

ax2.annotate("", xy=(507, 0.40), xytext=(555, 0.40),
             arrowprops=dict(arrowstyle="->", color=H.DARK, lw=1.1))
ax2.text(531, 0.315, "浦肯野偏移 48 nm", fontsize=7.4, color=H.DARK,
         ha="center", va="center")

ax2.set_xlim(380, 700)
ax2.set_ylim(0, 1.16)
ax2.set_xticks([400, 450, 500, 550, 600, 650, 700])
ax2.set_xlabel("波长 λ（nm）")
ax2.set_ylabel("光谱光视效率（峰值 = 1）")
ax2.legend(loc="lower center", bbox_to_anchor=(0.5, 0.995), ncol=2,
           fontsize=7.2, frameon=False, columnspacing=1.4,
           handlelength=1.5, handletextpad=0.5)

H.save(fig, 1, "f1_spd_photometry")

# ---------------- 与正文对应的数值 ----------------
l_all = np.linspace(100.0, 4000.0, 8000)


def ler(T):
    s = planck(T, l_all)
    v = np.interp(l_all, C.LAM, C.YBAR, left=0.0, right=0.0)
    return 683.0 * np.trapezoid(s * v, l_all) / np.trapezoid(s, l_all)


for T in (2856.0, 5000.0, 6500.0):
    print(f"T={T:.0f} K  full-band LER={ler(T):.1f} lm/W")
print("V peak", lam[V.argmax()], "Vp peak", lam[Vp.argmax()])
