# -*- coding: utf-8 -*-
"""图 7-3：HDR 的码率代价，以及抖动对量化台阶的掩盖作用。

左图是两条率失真曲线，只表示形状关系，标出的倍数取自公开测试报告
的常见区间，不是某一条序列的实测值。
右图取同一段渐变（亮度 0.30 至 0.35）用三种方式量化，再按 8 bit 输出，
用来说明 8 bit 抖动与 10 bit 在观感上的差距。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import NullFormatter
plt.rcParams["mathtext.fontset"] = "dejavusans"

rng = np.random.default_rng(20261127)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.9),
                               gridspec_kw={"width_ratios": [1.15, 1.0],
                                            "wspace": 0.26})
fig.subplots_adjust(left=0.085, right=0.985, bottom=0.155, top=0.95)

# ---------- (a) 率失真曲线示意 ----------
def rd(rate, sat, k=0.55):
    return 100.0 * sat * rate ** k / (1.0 + sat * rate ** k)

R = np.logspace(-0.45, 0.55, 400)
q_sdr = rd(R, 1.55)
q_hdr = rd(R / 1.28, 1.62)

ax1.semilogx(R, q_sdr, color=H.NAVY, lw=2.3, label="SDR，10 bit 4:2:0")
ax1.semilogx(R, q_hdr, color=H.ORANGE, lw=2.3, label="HDR10，10 bit 4:2:0")

QT = 72.0
r1 = (QT / (100 - QT) / 1.55) ** (1 / 0.55)
r2 = (QT / (100 - QT) / 1.62) ** (1 / 0.55) * 1.28
ax1.axhline(QT, color=H.GRAY, lw=0.9, ls=(0, (4, 3)), zorder=1)
ax1.plot([r1, r2], [QT, QT], color=H.RED, lw=1.4, zorder=4)
for xv in (r1, r2):
    ax1.plot([xv], [QT], "o", ms=5.2, color=H.RED, mec="white", mew=0.8, zorder=5)
ax1.annotate("", xy=(r2, QT - 7.5), xytext=(r1, QT - 7.5),
             arrowprops=dict(arrowstyle="<->", color=H.RED, lw=1.0))
ax1.text((r1 + r2) / 2, QT - 10.0, "同一质量档\n码率差 1.2 至 1.4 倍",
         fontsize=8.0, color=H.RED, ha="center", va="top", linespacing=1.5)
ax1.text(0.36, QT + 1.6, "同质量参考线", fontsize=7.4, color=H.GRAY,
         ha="left", va="bottom")

ax1.set_xlim(0.35, 3.6)
ax1.set_ylim(25, 92)
ax1.set_xticks([0.4, 0.6, 1.0, 1.5, 2.0, 3.0])
ax1.set_xticklabels(["0.4", "0.6", "1.0", "1.5", "2.0", "3.0"])
ax1.xaxis.set_minor_formatter(NullFormatter())
ax1.set_xlabel("相对码率（以 SDR 编码为 1.0）")
ax1.set_ylabel("主观质量（示意刻度）")
ax1.legend(loc="lower right", fontsize=8.0, handlelength=2.4)

# ---------- (b) 抖动与位深 ----------
W, HH, GAPY = 620, 44, 16
lo, hi = 0.30, 0.35
x = np.linspace(lo, hi, W)

def q8(v, dither=0.0):
    return np.round((v + dither) * 255.0) / 255.0

undithered = np.tile(q8(x), (HH, 1))
noise = rng.triangular(-0.5, 0.0, 0.5, (HH, W)) / 255.0
dithered = np.tile(x, (HH, 1)) + noise
dithered = np.round(dithered * 255.0) / 255.0
ten = np.tile(np.round(x * 1023.0) / 1023.0, (HH, 1))

rows = [undithered, dithered, ten]
blocks = []
for i, r in enumerate(rows):
    blocks.append(r)
    if i < 2:
        blocks.append(np.full((GAPY, W), np.nan))
img = np.vstack(blocks)
nH = img.shape[0]

cm = plt.get_cmap("gray").copy()
cm.set_bad("white")
ax2.imshow(img, cmap=cm, vmin=lo, vmax=hi, aspect="auto",
           interpolation="nearest", extent=(0, 1, nH, 0))

centers = []
y = 0
for i in range(3):
    centers.append(y + HH / 2)
    y += HH + GAPY
ax2.set_yticks(centers)
ax2.set_yticklabels(["8 bit\n无抖动", "8 bit\n加抖动", "10 bit"], fontsize=8.2)
ax2.set_xticks([])
ax2.grid(False)
ax2.set_xlabel("同一段渐变的局部放大（亮度 0.30 至 0.35）")
for s in ax2.spines.values():
    s.set_visible(False)

H.save(fig, 7, "f3_rate_dither")
