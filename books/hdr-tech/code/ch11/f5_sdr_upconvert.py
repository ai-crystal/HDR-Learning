# -*- coding: utf-8 -*-
"""第 11 章 图 5：把 SDR 抬到 HDR 时，量化台阶被一起放大。

SDR 按 BT.1886 解码（白场 100 cd/m2），整体放大 10 倍到 1000 nit 峰值，再编成 10 bit PQ。
(a) 输入码值每跨一级，输出跨多少个 10 bit PQ 码值。8 bit 源在中暗部就有两三个码值的跨度。
(b) 输入码值与输出码值的关系，8 bit 是一条台阶很宽的楼梯，10 bit 基本连续。
放大倍数与峰值只取 1000 nit 一种，用于比较位深带来的差别。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

GAIN = 10.0          # 100 cd/m2 -> 1000 nit


def sdr_lum(v, bits):
    return 100.0 * (v / (2 ** bits - 1)) ** 2.4


def pq10(lum):
    return 1023.0 * H.pq_oetf(lum)


v8 = np.arange(256)
v10 = np.arange(1024)
q8 = pq10(sdr_lum(v8, 8) * GAIN)
q10 = pq10(sdr_lum(v10, 10) * GAIN)

d8 = np.diff(q8)
d10 = np.diff(q10)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.9),
                               gridspec_kw={"width_ratios": [1.06, 1.0]})
fig.subplots_adjust(left=0.085, right=0.985, bottom=0.145, top=0.945, wspace=0.29)

ax1.plot(v8[1:] / 255, d8, color=H.RED, lw=1.9, label="8 bit 源")
ax1.plot(v10[1:] / 1023, d10, color=H.NAVY, lw=1.9, label="10 bit 源")
ax1.axhline(1.0, color="#8a97a6", lw=0.9, ls=(0, (4, 2)))
ax1.text(0.55, 1.25, "一个量化级", fontsize=7.4, color="#5b6b7c", va="bottom")
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 13.8)
ax1.set_xlabel("输入码值（归一化）", fontsize=9.5)
ax1.set_ylabel("每级跨过的 10 bit PQ 码值", fontsize=9.0)
ax1.legend(loc="upper right", fontsize=8.2)
ax1.text(0.02, 12.6, "(a)", fontsize=10, fontweight="bold", color=H.DARK)

i8 = int(np.argmax(d8))
ax1.annotate(f"最大 {d8.max():.1f} 级\n出现在码值 {v8[1:][i8]}",
             xy=(v8[1:][i8] / 255, d8[i8]), xytext=(0.28, 10.6),
             fontsize=7.4, color=H.RED, ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                             connectionstyle="arc3,rad=0.25"))

BINS = [0, 1, 2, 3, 4, 6, 20]
LAB = ["< 1", "1–2", "2–3", "3–4", "4–6", "> 6"]
h8, _ = np.histogram(d8, BINS)
h10, _ = np.histogram(d10, BINS)
p8 = 100.0 * h8 / len(d8)
p10 = 100.0 * h10 / len(d10)

xp = np.arange(len(LAB))
ax2.bar(xp - 0.20, p8, width=0.38, color=H.RED, alpha=0.88,
        edgecolor="white", lw=0.6, label="8 bit 源")
ax2.bar(xp + 0.20, p10, width=0.38, color=H.NAVY, alpha=0.88,
        edgecolor="white", lw=0.6, label="10 bit 源")
for x, a, b in zip(xp, p8, p10):
    if a > 2:
        ax2.text(x - 0.20, a + 1.2, f"{a:.0f}", fontsize=7.2, color=H.RED,
                 ha="center", va="bottom")
    if b > 2:
        ax2.text(x + 0.20, b + 1.2, f"{b:.0f}", fontsize=7.2, color=H.NAVY,
                 ha="center", va="bottom")

ax2.set_xticks(xp)
ax2.set_xticklabels(LAB, fontsize=8.4)
ax2.set_ylim(0, 88)
ax2.set_xlabel("每级跨过的 10 bit PQ 码值（区间）", fontsize=9.5)
ax2.set_ylabel("占总级数的百分比（%）", fontsize=9.0)
ax2.legend(loc="upper right", fontsize=8.2)
ax2.text(-0.45, 83, "(b)", fontsize=10, fontweight="bold", color=H.DARK)
ax2.text(1.55, 40, "8 bit 有三成码值\n跨过 3 级以上", fontsize=7.4, color=H.RED,
         ha="left", va="center", linespacing=1.5)

print("share >=3", round(100*(d8>=3).mean(),1), round(100*(d10>=3).mean(),1))
print("d8 max", d8.max(), "at", v8[1:][i8], "d10 max", round(float(d10.max()), 2))
print("d8 mean first 64", round(float(d8[:64].mean()), 2))
print("q8 range", q8[0], q8[-1])

H.save(fig, 11, "f5_sdr_upconvert")
