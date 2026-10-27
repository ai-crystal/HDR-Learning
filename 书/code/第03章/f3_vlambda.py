# -*- coding: utf-8 -*-
"""第 03 章 图 3　明视觉 V(λ) 与暗视觉 V'(λ) 灵敏度曲线。

上：两条光谱光视效率函数（峰 555 nm / 507 nm），下方附可见光谱色带。
下：两者之比（暗视觉/明视觉），交点在约 526 nm，说明“浦肯野漂移”。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import numpy as np
import hdrfig as H
from scipy.interpolate import PchipInterpolator
from matplotlib.ticker import NullFormatter
plt = H.plt

# ---------- CIE 1924 明视觉 V(λ)（10 nm 表 + 555 nm 峰） ----------
WL = np.arange(380, 781, 10, dtype=float)
V = np.array([
    0.000039, 0.000120, 0.000396, 0.001210, 0.004000, 0.011600, 0.023000,
    0.038000, 0.060000, 0.090980, 0.139020, 0.208020, 0.323000, 0.503000,
    0.710000, 0.862000, 0.954000, 0.994950, 0.995000, 0.952000, 0.870000,
    0.757000, 0.631000, 0.503000, 0.381000, 0.265000, 0.175000, 0.107000,
    0.061000, 0.032000, 0.017000, 0.008210, 0.004102, 0.002091, 0.001047,
    0.000520, 0.000249, 0.000120, 0.000060, 0.000030, 0.000015])
WL = np.append(WL, 555.0); V = np.append(V, 1.0)
o = np.argsort(WL); WL, V = WL[o], V[o]

lam = np.arange(380, 781, 1.0)
phot = np.clip(PchipInterpolator(WL, V)(lam), 0, None)

# ---------- CIE 1951 暗视觉 V'(λ)：峰 507 nm 的平滑拟合 ----------
scot = np.exp(-0.5 * ((lam - 507.0) / 35.0) ** 2)


def wl2rgb(w):
    """波长 → 近似 RGB（用于绘制可见光谱色带）。"""
    if 380 <= w < 440:    r, g, b = -(w - 440) / 60.0, 0.0, 1.0
    elif 440 <= w < 490:  r, g, b = 0.0, (w - 440) / 50.0, 1.0
    elif 490 <= w < 510:  r, g, b = 0.0, 1.0, -(w - 510) / 20.0
    elif 510 <= w < 580:  r, g, b = (w - 510) / 70.0, 1.0, 0.0
    elif 580 <= w < 645:  r, g, b = 1.0, -(w - 645) / 65.0, 0.0
    elif 645 <= w <= 780: r, g, b = 1.0, 0.0, 0.0
    else:                 r = g = b = 0.0
    if 380 <= w < 420:    f = 0.28 + 0.72 * (w - 380) / 40.0
    elif 420 <= w < 700:  f = 1.0
    elif 700 <= w <= 780: f = 0.28 + 0.72 * (780 - w) / 80.0
    else:                 f = 0.0
    return r * f, g * f, b * f


band = np.array([[wl2rgb(w) for w in lam]])

# 交点（只在 500–570 nm 内找，避免远红端两者都趋零造成误判）
sel = (lam >= 500) & (lam <= 570)
xc = float(lam[sel][np.argmin(np.abs(scot[sel] - phot[sel]))])
yc = float(phot[sel][np.argmin(np.abs(scot[sel] - phot[sel]))])

fig = plt.figure(figsize=(7.2, 5.05))
gs = fig.add_gridspec(3, 1, height_ratios=[3.4, 0.38, 1.30], hspace=0.30)
ax = fig.add_subplot(gs[0])
axb = fig.add_subplot(gs[1])
axr = fig.add_subplot(gs[2])

# ---------------- 主图 ----------------
ax.plot(lam, phot, color=H.NAVY, lw=2.6, label="明视觉 V(λ)（峰 555 nm）")
ax.plot(lam, scot, color=H.ORANGE, lw=2.6, label="暗视觉 V′(λ)（峰 507 nm）")
ax.fill_between(lam, 0, phot, color=H.NAVY, alpha=0.07, lw=0)

ax.axvline(555, color=H.NAVY, ls="--", lw=1.1, alpha=0.85)
ax.axvline(507, color=H.ORANGE, ls="--", lw=1.1, alpha=0.85)
ax.plot([555], [1.0], "o", color=H.NAVY, ms=6, mec="white", mew=1.0, zorder=6)
ax.plot([507], [1.0], "o", color=H.ORANGE, ms=6, mec="white", mew=1.0, zorder=6)
ax.text(555, 1.045, "555 nm", fontsize=8.4, color=H.NAVY, ha="center", va="bottom")
ax.text(507, 1.045, "507 nm", fontsize=8.4, color=H.ORANGE, ha="center", va="bottom")

ax.plot([xc], [yc], "o", color=H.PURPLE, ms=6, mec="white", mew=1.0, zorder=7)
ax.annotate("两曲线交于约 %.0f nm\n（浦肯野漂移的分界）" % xc,
            xy=(xc, yc), xytext=(596, 0.60), fontsize=8.4, color=H.PURPLE,
            arrowprops=dict(arrowstyle="->", color=H.PURPLE, lw=1.0))

ax.annotate("450 nm：暗视觉相对更灵敏\n夜里蓝绿最亮", xy=(450, 0.235), xytext=(386, 0.52),
            fontsize=8.2, color=H.TEAL,
            arrowprops=dict(arrowstyle="->", color=H.TEAL, lw=1.0))
ax.annotate("650 nm：暗视觉几乎归零\n夜里红色看不清", xy=(650, 0.110), xytext=(612, 0.24),
            fontsize=8.2, color="#8a6d1f",
            arrowprops=dict(arrowstyle="->", color="#8a6d1f", lw=1.0))

ax.text(676, 0.60,
        "浦肯野漂移（Purkinje shift）\n暗环境下峰值蓝移 48 nm，\n世界偏冷、偏蓝",
        fontsize=8.0, color="#444444", ha="left", va="top",
        bbox=dict(fc="white", ec=H.LGRAY, lw=0.8, pad=2.6))

ax.set_xlim(380, 780); ax.set_ylim(0, 1.10)
ax.set_xticks(np.arange(400, 781, 50))
ax.set_xlabel("")
ax.set_ylabel("相对灵敏度（归一化）")
ax.set_title("明视觉与暗视觉：两条曲线、两个峰值（视锥 / 视杆）", fontsize=10.5)
ax.legend(loc="upper right", fontsize=8.4)

# ---------------- 光谱色带 ----------------
axb.imshow(band, extent=[380, 780, 0, 1], aspect="auto", origin="lower")
axb.set_xlim(380, 780); axb.set_yticks([]); axb.set_xticks([])
axb.grid(False)
for s in axb.spines.values():
    s.set_visible(False)

# ---------------- 比值 ----------------
m = (lam >= 400) & (lam <= 700)
ratio = scot[m] / np.maximum(phot[m], 1e-12)
axr.axhline(1.0, color=H.GRAY, lw=1.2, ls=":")
axr.fill_between(lam[m], 1.0, ratio, where=ratio > 1, color=H.ORANGE, alpha=0.16, lw=0)
axr.fill_between(lam[m], 1.0, ratio, where=ratio < 1, color=H.NAVY, alpha=0.12, lw=0)
axr.plot(lam[m], ratio, color=H.PURPLE, lw=2.2, zorder=5)
axr.plot([xc], [1.0], "o", color=H.PURPLE, ms=6, mec="white", mew=1.0, zorder=6)
axr.annotate("%.0f nm" % xc, xy=(xc, 1.0), xytext=(5, 7), textcoords="offset points",
             fontsize=8.4, color=H.PURPLE)

axr.set_xlim(400, 700); axr.set_ylim(3e-3, 3e2)
axr.set_yscale("log")
axr.set_xticks(np.arange(400, 701, 50))
axr.set_yticks([1e-2, 1e-1, 1, 1e1, 1e2])
axr.set_yticklabels([r"$10^{-2}$", r"$10^{-1}$", r"$10^{0}$", r"$10^{1}$", r"$10^{2}$"])
axr.yaxis.set_minor_formatter(NullFormatter())
axr.set_xlabel("波长（nm）")
axr.set_ylabel("V′ / V")
axr.set_title("V′/V 比值：蓝端暗视觉更强，红端几乎归零", fontsize=9.5)
axr.text(408, 1.35, "暗视觉更灵敏", fontsize=8, color=H.ORANGE, va="bottom")
axr.text(696, 0.72, "明视觉更灵敏", fontsize=8, color=H.NAVY, ha="right", va="top")

fig.suptitle("图 03-3　明视觉 V(λ) 与暗视觉 V′(λ)：峰值从 555 nm 漂移到 507 nm",
             fontsize=12.5, fontweight="bold", y=0.995)
H.save(fig, 3, "f3_vlambda")
