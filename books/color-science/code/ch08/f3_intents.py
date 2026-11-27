# -*- coding: utf-8 -*-
"""第 08 章 图 4：四种渲染意图的映射差异（示意）。

(a) 明度 $L^*$ 的映射：相对比色、相对比色加 BPC、感知、绝对比色
(b) 同一色相上的彩度映射：硬裁剪、平滑压缩、保饱和
目标介质取黑 $L^*=4$、白 $L^*=96$，源取 $0$ 到 $100$。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cms_util as C

plt = H.plt
plt.rcParams["mathtext.fontset"] = "dejavusans"

fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2),
                         gridspec_kw={"wspace": 0.30})

BLK_D, WHT_D = 8.0, 94.0

# ---------------- (a) L* 映射 ----------------
ax = axes[0]
L = np.linspace(0, 100, 600)

rel = np.clip(L, BLK_D, WHT_D)
bpc = BLK_D + (WHT_D - BLK_D) * L / 100.0
# 感知：暗部略抬、亮部略压，整体对比度收缩
x = L / 100.0
s_curve = 0.5 * x + 0.5 * (3 * x ** 2 - 2 * x ** 3)
perc = BLK_D + (WHT_D - BLK_D) * s_curve
# 绝对比色：源白 100 cd/m2、目标介质白 160 cd/m2，按绝对亮度折算
Y = np.where(L > 8, ((L + 16) / 116.0) ** 3, L / 903.3)
Y_abs = Y * (100.0 / 160.0)
L_abs = np.where(Y_abs > 0.008856, 116 * np.cbrt(Y_abs) - 16, 903.3 * Y_abs)
L_abs = np.clip(L_abs, BLK_D, WHT_D)

ax.plot(L, rel, color=H.NAVY, lw=1.8, label="相对比色")
ax.plot(L, bpc, color=H.TEAL, lw=1.8, ls=(0, (5, 2)), label="相对比色 + BPC")
ax.plot(L, perc, color=H.ORANGE, lw=1.8, label="感知")
ax.plot(L, L_abs, color=H.RED, lw=1.6, ls=(0, (1.5, 2)), label="绝对比色")
ax.plot([0, 100], [0, 100], color=H.LGRAY, lw=1.0, ls=":", zorder=1)

ax.axhspan(0, BLK_D, color="#f2f2f2", zorder=0)
ax.axhspan(WHT_D, 100, color="#f2f2f2", zorder=0)



ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_xlabel("源 $L^*$", fontsize=8.5)
ax.set_ylabel("目标 $L^*$", fontsize=8.5)
ax.set_title("(a) 明度映射", fontsize=8.4, pad=5)
ax.legend(loc="lower right", fontsize=6.2, handlelength=2.0,
          labelspacing=0.22, borderaxespad=0.3)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_yticks([0, 25, 50, 75, 100])

ins = ax.inset_axes([0.13, 0.52, 0.34, 0.34])
ins.plot(L, rel, color=H.NAVY, lw=1.4)
ins.plot(L, bpc, color=H.TEAL, lw=1.4, ls=(0, (5, 2)))
ins.plot(L, perc, color=H.ORANGE, lw=1.4)
ins.plot(L, L_abs, color=H.RED, lw=1.2, ls=(0, (1.5, 2)))
ins.plot([0, 100], [0, 100], color=H.LGRAY, lw=0.8, ls=":")
ins.set_xlim(0, 30)
ins.set_ylim(0, 30)
ins.tick_params(labelsize=5.6, length=2)
ins.set_title("暗部放大", fontsize=5.8, pad=2)
ins.grid(True, color="#e8edf2", lw=0.5)

# ---------------- (b) 彩度映射 ----------------
ax = axes[1]
Cin = np.linspace(0, 110, 600)
CMAX = 62.0
start = 0.72 * CMAX

rel_c = np.minimum(Cin, CMAX)

over = Cin > start
perc_c = np.where(over,
                  start + (CMAX - start)
                  * (1 - np.exp(-(Cin - start) / (CMAX - start) * 1.2)),
                  Cin)
sat_c = np.minimum(Cin * 1.08, CMAX)

ax.plot(Cin, rel_c, color=H.NAVY, lw=1.8, label="相对比色：到边界就裁")
ax.plot(Cin, perc_c, color=H.ORANGE, lw=1.8, label="感知：提前起压")
ax.plot(Cin, sat_c, color=H.TEAL, lw=1.8, ls=(0, (5, 2)), label="饱和度：先抬后裁")
ax.axvline(CMAX, color=H.GRAY, lw=0.9, ls=(0, (3, 3)))
ax.text(CMAX + 1.5, 8, "目标色域\n彩度上限", fontsize=5.8, color=H.GRAY,
        va="bottom", linespacing=1.4)
ax.plot([0, 110], [0, 110], color=H.LGRAY, lw=1.0, ls=":", zorder=1)
ax.text(66, 44, "超出色域的部分\n只能压回来", fontsize=5.8, color=H.GRAY,
        ha="left", va="center", linespacing=1.4)

ax.set_xlim(0, 110)
ax.set_ylim(0, 110)
ax.set_xlabel("源 $C^*_{ab}$", fontsize=8.5)
ax.set_ylabel("目标 $C^*_{ab}$", fontsize=8.5)
ax.set_title("(b) 彩度映射", fontsize=8.4, pad=5)
ax.legend(loc="lower right", fontsize=6.2, handlelength=2.0,
          labelspacing=0.22, borderaxespad=0.3)

H.save(fig, 8, "f3_intents")
