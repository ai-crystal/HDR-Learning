# -*- coding: utf-8 -*-
"""图 1-5：人眼的绝对范围、瞬时窗口与感光细胞的分工。

(a) 视杆、视锥与中间视觉的工作区间取自 CIE 191:2010 对中间视觉的界定
    （0.005 至 5 cd/m²），其余为常用量级。三段的“瞬时窗口”按 4 个数量级
    的可用跨度画在不同适应点上。
(b) 一幅合成场景的亮度剖面（对数亮度沿水平位置变化，跨约 7 个数量级）
    与一个 4 个数量级的瞬时窗口叠在一起，窗外的部分在单次注视里无法分辨。
    剖面是人为构造的示意数据，只用于说明裁剪关系。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import FuncFormatter, NullFormatter
plt.rcParams["mathtext.fontset"] = "dejavusans"


def dec(v):
    s = f"{v:.0e}"
    return s.replace("e+0", "e").replace("e+", "e").replace("e-0", "e-")


fig = plt.figure(figsize=(8.8, 4.5))
gs = fig.add_gridspec(2, 1, height_ratios=[1.15, 1.0], hspace=0.62,
                      left=0.235, right=0.975, bottom=0.115, top=0.955)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# ---------- (a) ----------
rows, groups = [], []
y = 0.0
CELLS = [("视杆（暗视觉）", 1e-6, 1e-2, H.PURPLE),
         ("中间视觉（混合）", 5e-3, 5.0, H.GOLD),
         ("视锥（明视觉）", 3.0, 1e8, H.TEAL)]
WINS = [("暗适应之后 · 4 个数量级", 1e-5, 1e-1),
        ("室内观影 · 4 个数量级", 0.3, 3e3),
        ("晴天室外 · 4 个数量级", 30.0, 3e5)]
for name, lo, hi, c in CELLS:
    rows.append((name, lo, hi, c, y, "bar"))
    y -= 1
y -= 0.45
for name, lo, hi in WINS:
    rows.append((name, lo, hi, H.NAVY, y, "win"))
    y -= 1

for name, lo, hi, c, yy, kind in rows:
    if kind == "bar":
        ax1.plot([lo, hi], [yy, yy], color=c, lw=6.0, alpha=0.5,
                 solid_capstyle="round", zorder=3)
    else:
        ax1.annotate("", xy=(lo, yy), xytext=(hi, yy),
                     arrowprops=dict(arrowstyle="<->", color=c, lw=1.6,
                                     shrinkA=0, shrinkB=0))
        ax1.plot([lo, lo], [yy - 0.2, yy + 0.2], color=c, lw=1.4, zorder=3)
        ax1.plot([hi, hi], [yy - 0.2, yy + 0.2], color=c, lw=1.4, zorder=3)

# 组标题
ax1.text(1.4e-7, 0.62, "感光细胞的工作区间", fontsize=9.2, color=H.DARK,
         ha="left", va="center")
ax1.text(1.4e-7, -2.85, "同一时刻可用的亮度跨度",
         fontsize=9.2, color=H.DARK, ha="left", va="center")

ax1.axvline(1e4, color=H.ORANGE, lw=1.0, ls=(0, (4, 3)), zorder=2)
ax1.text(1.3e4, -6.48, "不适眩光起点", fontsize=8.0, color=H.ORANGE,
         ha="left", va="center")
ax1.plot([1.6e9], [-6.48], "o", ms=6.5, color=H.RED, mec="white", mew=1.0,
         zorder=4)
ax1.text(1.6e9 / 3.0, -6.48, "直视太阳 1.6e9", fontsize=8.0, color=H.RED,
         ha="right", va="center")

ax1.set_xscale("log")
ax1.set_xlim(1.4e-7, 2e10)
ax1.set_ylim(-7.55, 1.05)
ax1.set_yticks([r[4] for r in rows])
ax1.set_yticklabels([r[0] for r in rows])
ax1.tick_params(axis="y", length=0, pad=6)
ax1.set_xticks([1e-6, 1e-4, 1e-2, 1, 1e2, 1e4, 1e6, 1e8, 1e10])
ax1.xaxis.set_major_formatter(FuncFormatter(lambda v, p: dec(v) if v < 1e-1
                                            else f"{v:g}".replace("e+", "e")))
ax1.xaxis.set_minor_formatter(NullFormatter())
ax1.grid(axis="y", visible=False)
ax1.set_xlabel("亮度（cd/m$^2$，对数刻度）")
ax1.text(0.995, 0.93, "(a)", transform=ax1.transAxes, ha="right", va="top",
         fontsize=10, color=H.DARK)

# ---------- (b) ----------
x = np.linspace(0, 1, 900)


def bump(xc, w, h):
    return h * np.exp(-((x - xc) / w) ** 2)


logL = (1.35 + bump(0.19, 0.055, 2.6) + bump(0.63, 0.045, 3.35)
        + bump(0.67, 0.03, 0.6) - bump(0.40, 0.06, 1.7)
        + bump(0.86, 0.018, 0.9) - bump(0.42, 0.03, 0.3))
L = 10 ** logL

lo_w, hi_w = 1.0, 1e4
ins = (L >= lo_w) & (L <= hi_w)
ax2.semilogy(x, L, color=H.LGRAY, lw=3.2, zorder=2)
ax2.semilogy(x[ins], L[ins], color=H.NAVY, lw=2.2, zorder=3)
ax2.axhspan(lo_w, hi_w, color=H.NAVY, alpha=0.07, zorder=1)
ax2.axhline(lo_w, color=H.NAVY, lw=0.8, ls=(0, (3, 3)))
ax2.axhline(hi_w, color=H.NAVY, lw=0.8, ls=(0, (3, 3)))
ax2.text(0.012, hi_w * 1.5, "窗口上沿 10000", fontsize=7.8, color=H.NAVY,
         ha="left", va="bottom")
ax2.text(0.012, lo_w * 0.62, "窗口下沿 1", fontsize=7.8, color=H.NAVY,
         ha="left", va="top")

ax2.annotate("窗外的高光被裁掉", xy=(0.635, 3.4e4), xytext=(0.30, 1.0e5),
             fontsize=8.0, color=H.RED,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                             shrinkA=2, shrinkB=3))
ax2.annotate("窗外的暗部糊成一片", xy=(0.42, 0.42), xytext=(0.20, 0.055),
             fontsize=8.0, color=H.PURPLE,
             arrowprops=dict(arrowstyle="->", color=H.PURPLE, lw=0.9,
                             shrinkA=2, shrinkB=3))
ax2.text(0.985, 0.93, "(b)", transform=ax2.transAxes, ha="right", va="top",
         fontsize=10, color=H.DARK)

ax2.set_xlim(0, 1)
ax2.set_ylim(1e-2, 5e5)
ax2.set_yticks([1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e4, 1e5])
ax2.yaxis.set_major_formatter(FuncFormatter(lambda v, p: dec(v)))
ax2.yaxis.set_minor_formatter(NullFormatter())
ax2.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax2.set_xticklabels(["左", "", "", "", "", "右"])
ax2.set_xlabel("画面上的水平位置")
ax2.set_ylabel("亮度（cd/m$^2$）")

H.save(fig, 1, "f5_instant_range")
