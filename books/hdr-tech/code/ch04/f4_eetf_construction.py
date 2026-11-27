# -*- coding: utf-8 -*-
"""第 04 章 图 5：BT.2390 EETF 的分段构造（按推荐书公式计算）。

上：PQ 码值域里的映射曲线。K_S 以下为恒等段，K_S 以上为三次 Hermite 段。
    两条切线段分别标出拐点处斜率 1、峰值处斜率 0 的边界条件。
下：同一映射的导数 dE3/dE1。拐点处导数连续（值为 1），终点处为 0，即整条曲线 C1 连续。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt


def eetf_code(e1, max_lum):
    ks = 1.5 * max_lum - 0.5
    t = np.clip((e1 - ks) / (1.0 - ks), 0.0, 1.0)
    h = (ks * (2 * t ** 3 - 3 * t ** 2 + 1)
         + (1.0 - ks) * (t ** 3 - 2 * t ** 2 + t)
         + max_lum * (-2 * t ** 3 + 3 * t ** 2))
    return np.where(e1 < ks, e1, h)


E1 = np.linspace(0.0, 1.0, 2000)
MAXLUM = float(H.pq_oetf(1000))          # 1000 nit 对应的 PQ 码值
KS = 1.5 * MAXLUM - 0.5
E3 = eetf_code(E1, MAXLUM)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 6.0), sharex=True,
                               gridspec_kw=dict(hspace=0.16, height_ratios=[1.25, 1.0]))

# ---------------- (a) 曲线 ----------------
ax1.plot(E1, E1, color=H.LGRAY, lw=1.5, ls=(0, (4, 2)), label="恒等（不压缩）")
ax1.plot(E1, E3, color=H.NAVY, lw=2.4, label="EETF，目标峰值 1000 nit")

ax1.axvspan(KS, 1.0, color="#eaf0f6", lw=0, zorder=0)
ax1.text(0.80, 0.16, "Hermite 压\n缩段", fontsize=8.5, color="#5b6b7c", ha="center")
ax1.text(0.30, 0.10, "恒等段", fontsize=8.5, color="#5b6b7c", ha="center")

ax1.axvline(KS, color=H.RED, lw=0.9, ls=":")
ax1.plot([KS], [KS], marker="o", ms=6, color=H.RED, mec="white", mew=1.1, zorder=6)
ax1.annotate("$K_S$ = 0.628\n（316 nit）", xy=(KS, KS), xytext=(KS - 0.26, 0.74),
             fontsize=8.4, color=H.RED,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.0,
                             connectionstyle="arc3,rad=-0.25"))

# 拐点切线（斜率 1）与峰值切线（斜率 0）
tg = np.array([-0.075, 0.075])
ax1.plot(KS + tg, KS + tg, color=H.TEAL, lw=1.6, ls="-")
ax1.text(KS + 0.105, KS - 0.075, "切线斜率 1", fontsize=8.2, color=H.TEAL)
ax1.plot([0.90, 1.0], [MAXLUM, MAXLUM], color=H.ORANGE, lw=1.6, ls="-")
ax1.text(0.985, MAXLUM + 0.030, "切线斜率 0", fontsize=8.2, color=H.ORANGE, ha="right")

ax1.set_ylabel("输出码值 $E_3$")
ax1.set_xlim(0, 1.0)
ax1.set_ylim(0, 1.0)
ax1.legend(loc="upper left", fontsize=8.2)

# ---------------- (b) 导数 ----------------
for tgt, color in [(300, H.TEAL), (600, H.ORANGE), (1000, H.NAVY)]:
    m = float(H.pq_oetf(tgt))
    y = eetf_code(E1, m)
    d = np.gradient(y, E1)
    ax2.plot(E1, d, color=color, lw=1.8, label=f"目标 {tgt} nit")
    ax2.plot([1.5 * m - 0.5], [1.0], marker="o", ms=4.5, color=color,
             mec="white", mew=0.9, zorder=5)

ax2.axhline(1.0, color=H.GRAY, lw=0.9, ls=":")
ax2.text(0.02, 1.03, "斜率 1：局部对比不变", fontsize=8.2, color=H.GRAY, va="bottom")
ax2.set_xlabel("输入码值 $E_1$（PQ 0–1，满量程 10000 nit）")
ax2.set_ylabel("导数 $\\mathrm{d}E_3 / \\mathrm{d}E_1$")
ax2.set_xlim(0, 1.0)
ax2.set_ylim(0, 1.18)
ax2.legend(loc="lower left", fontsize=8.2, ncol=1, handlelength=1.6,
           labelspacing=0.3, borderpad=0.4)

H.save(fig, 4, "f4_eetf_construction")
