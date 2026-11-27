# -*- coding: utf-8 -*-
"""第 04 章 图 6：SDR→HDR 逆映射的两条曲线，以及直方图的变化（公式计算）。

左：两条逆映射曲线。保守的全局曲线只把 SDR 白 100 nit 抬到参考白 203 nit，
    峰值停在 203 nit；要让高光冲到 1000 nit，必须在 30 nit 以上加一段快速滚降。
右：同一幅合成 SDR 画面在两种映射下的 PQ 码值分布。保守映射整体平移，
    高光扩张映射把 30 nit 以上的像素拉开，直方图右端出现长尾。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

GAMMA = 1.15
KNEE, KNEE_OUT = 30.0, 203.0 * (30.0 / 100.0) ** GAMMA


def conservative(x):
    return 203.0 * (np.maximum(x, 1e-5) / 100.0) ** GAMMA


def aggressive(x):
    lx = np.log10(np.maximum(x, 1e-5))
    ly = np.log10(np.maximum(conservative(x), 1e-5))
    a, b = np.log10(KNEE), np.log10(100.0)
    c, d = np.log10(KNEE_OUT), np.log10(1000.0)
    u = np.clip((lx - a) / (b - a), 0.0, 1.0)
    t0 = GAMMA * (b - a) / (d - c)
    her = (t0 * (u ** 3 - 2 * u ** 2 + u) + 1.0 * (-2 * u ** 3 + 3 * u ** 2))
    out = 10 ** (ly + her * (d - c))
    return np.where(lx >= a, out, conservative(x))


x = np.logspace(np.log10(0.02), 2.0, 600)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 4.1))
fig.subplots_adjust(wspace=0.30)

ax1.plot(x, x * 2.03, color=H.LGRAY, lw=1.5, ls=(0, (4, 2)), label="等比例放大 2.03 倍")
ax1.plot(x, conservative(x), color=H.BLUE, lw=2.1, label="保守全局曲线（峰值 203 nit）")
ax1.plot(x, aggressive(x), color=H.RED, lw=2.1, label="含高光扩张（峰值 1000 nit）")
ax1.plot([100], [203], marker="o", ms=6, color=H.BLUE, mec="white", mew=1.0, zorder=5)
ax1.plot([100], [1000], marker="o", ms=6, color=H.RED, mec="white", mew=1.0, zorder=5)

ax1.text(0.023, 900, "SDR 白 100 nit 的两种去处\n保守映射 → 203 nit\n高光扩张 → 1000 nit",
         fontsize=8.3, color="#3a4a5c", va="top", linespacing=1.5)

ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlim(0.02, 105)
ax1.set_ylim(0.01, 3000)
ax1.set_xticks([0.02, 0.1, 1, 10, 100])
ax1.set_xticklabels(["0.02", "0.1", "1", "10", "100"])
ax1.set_yticks([0.01, 0.1, 1, 10, 100, 1000])
ax1.set_yticklabels(["0.01", "0.1", "1", "10", "100", "1000"])
ax1.minorticks_off()
ax1.set_xlabel("SDR 输入的绝对亮度（nit，对数刻度）")
ax1.set_ylabel("映射后的 HDR 亮度（nit）")
ax1.set_title("(a) 两条逆映射曲线", fontsize=10, pad=4)
ax1.legend(loc="lower right", fontsize=7.8, labelspacing=0.3, borderpad=0.4)

# ---------------- (b) 直方图 ----------------
Hh, Ww = 216, 384
yy, xx = np.mgrid[0:1:Hh * 1j, 0:1:Ww * 1j]
img = 8.0 + 37.0 * (1 - yy) ** 2
wall = (xx > 0.06) & (xx < 0.32) & (yy > 0.52) & (yy < 0.96)
img = np.where(wall, 3.0, img)
for wx in (0.10, 0.16, 0.22, 0.28):
    for wy in (0.58, 0.68, 0.78, 0.88):
        img = np.where((np.abs(xx - wx) < 0.012) & (np.abs(yy - wy) < 0.02), 85.0, img)
img = np.where(yy > 0.93, 12.0, img)
img = np.where((xx > 0.82) & (xx < 0.92) & (yy > 0.20), 0.4, img)
img = np.where((np.abs(xx - 0.62) < 0.01) & (np.abs(yy - 0.18) < 0.02), 99.0, img)

bins = np.linspace(0, 1023, 65)
for arr, color, lab, lw in [(conservative(img), H.BLUE, "保守全局曲线", 2.2),
                            (aggressive(img), H.RED, "含高光扩张", 1.6)]:
    ax2.hist((H.pq_oetf(arr) * 1023.0).ravel(), bins=bins, histtype="step",
             color=color, lw=lw, label=lab, density=True)

for val, lab in [(203, "203 nit"), (1000, "1000 nit")]:
    xv = float(H.pq_oetf(val)) * 1023
    ax2.axvline(xv, color=H.GRAY if val == 203 else H.DARK, lw=0.9, ls=":")
    ax2.text(xv + 10, 0.0084, lab, fontsize=8.0,
             color=H.GRAY if val == 203 else H.DARK, ha="left", va="top")

ax2.set_xlim(0, 1023)
ax2.set_ylim(0, 0.0086)
ax2.set_xlabel("输出 PQ 码值（10 位）")
ax2.set_ylabel("像素占比（归一化密度）")
ax2.set_title("(b) 同一画面在两种映射下的分布", fontsize=10, pad=4)
ax2.legend(loc="center right", fontsize=8.0, labelspacing=0.3, borderpad=0.4)

H.save(fig, 4, "f6_inverse_hist")
