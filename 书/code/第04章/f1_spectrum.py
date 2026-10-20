# -*- coding: utf-8 -*-
"""第 04 章 图 1：电磁波谱与可见光窗口（380–780 nm）。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.patches as mpatches
import hdrfig as H
import cie1931 as C

plt = H.plt

fig = plt.figure(figsize=(7.2, 4.8))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.0], hspace=0.75)

# ============ 上：全波谱（对数波长轴，单位 m） ============
ax = fig.add_subplot(gs[0])
ax.set_title("电磁波谱：可见光只是极窄的一小段", pad=10)

bands = [
    ("γ 射线",   1e-13, 1e-11,  H.PURPLE, 0.34),
    ("X 射线",   1e-11, 1e-8,   H.NAVY,   0.62),
    ("紫外线",   1e-8,  380e-9, H.GOLD,   0.34),
    ("可见光",   380e-9, 780e-9, H.GREEN, 0.34),
    ("红外线",   780e-9, 1e-3,  H.RED,    0.62),
    ("微波",     1e-3,  1e-1,   H.ORANGE, 0.34),
    ("无线电波", 1e-1,  1e4,    H.TEAL,   0.62),
]
for name, lo, hi, col, ty in bands:
    ax.axvspan(lo, hi, ymin=0.13, ymax=0.74, color=col,
               alpha=0.85 if name == "可见光" else 0.36)
    if name != "可见光":
        ax.text(np.sqrt(lo * hi), ty, name, ha="center", va="center",
                fontsize=9.2, fontweight="bold", color="#2c3e50")
# 可见光窗口高亮
ax.axvspan(380e-9, 780e-9, ymin=0.10, ymax=0.80, facecolor="none",
           edgecolor=H.GREEN, lw=1.8, zorder=5)
ax.annotate("可见光窗口 380–780 nm\n（全谱里不到一个倍频程）",
            xy=(5.5e-7, 0.98), xytext=(2.5e-12, 1.14),
            fontsize=8.6, color=H.GREEN, fontweight="bold", ha="left", va="bottom",
            arrowprops=dict(arrowstyle="->", color=H.GREEN, lw=1.5,
                            connectionstyle="arc3,rad=-0.18"))

ax.set_xscale("log")
ax.set_xlim(1e-13, 1e4)
ax.set_ylim(0.0, 1.42)
ax.set_yticks([])
ax.set_xlabel("波长 λ（米，对数轴）　—— 波长越短：频率越高、光子能量越大", fontsize=9.5)
xt = [1e-12, 1e-9, 1e-6, 1e-3, 1e0, 1e3]
ax.set_xticks(xt)
ax.set_xticklabels(["1 pm", "1 nm", "1 μm", "1 mm", "1 m", "1 km"])
ax.grid(axis="x", color="#dde3ea", lw=0.6)
ax.tick_params(axis="y", length=0)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)

# ============ 下：可见光放大（380–780 nm 彩虹带） ============
ax2 = fig.add_subplot(gs[1])
ax2.set_title("可见光窗口放大：380 nm 紫 → 780 nm 红（下排数字为光子能量 eV）", pad=8)

lam = np.linspace(380, 780, 800)
rgb = C.wavelength_to_srgb01(lam)                     # (800, 3)
strip = np.tile(rgb[None, :, :], (26, 1, 1))          # (26, 800, 3)：行=高度
ax2.imshow(strip, extent=[380, 780, 0.62, 1.02], aspect="auto",
           origin="lower", interpolation="bilinear", zorder=1)

zones = [("紫", 380, 450, "white"), ("蓝", 450, 485, "white"), ("青", 485, 500, "black"),
         ("绿", 500, 565, "black"), ("黄", 565, 590, "black"), ("橙", 590, 625, "black"),
         ("红", 625, 780, "white")]
for name, a, b, tc in zones:
    ax2.text((a + b) / 2, 0.82, name, ha="center", va="center", fontsize=10,
             fontweight="bold", color=tc, zorder=3)
    if a != 380:
        ax2.axvline(a, color="white", lw=1.0, ymin=0.40, ymax=0.90, alpha=0.9, zorder=2)

# 视锥敏感峰
ax2.axhline(0.62, color=H.NAVY, lw=1.0, xmin=0.0, xmax=1.0, zorder=2)
for wl, tag, col, tx in ((445, "S 峰 445", H.PURPLE, 400),
                         (545, "M 峰 545", H.GREEN, 520),
                         (565, "L 峰 565", H.RED, 610)):
    ax2.plot([wl], [0.62], marker="v", ms=7, color=col, zorder=4, clip_on=False)
    ax2.annotate(tag, xy=(wl, 0.62), xytext=(tx, 0.44), fontsize=8,
                 color=col, fontweight="bold", ha="center", va="center",
                 arrowprops=dict(arrowstyle="-", color=col, lw=0.9))

# 光子能量
for wl in (400, 450, 500, 550, 600, 650, 700, 750):
    ax2.text(wl, 0.20, f"{1240/wl:.2f}", ha="center", va="center",
             fontsize=7.4, color=H.GRAY)
ax2.text(378, 0.20, "eV =", ha="right", va="center", fontsize=7.4,
         color=H.GRAY, fontweight="bold")

ax2.set_xlim(360, 800)
ax2.set_ylim(0.05, 1.12)
ax2.set_xticks([380, 450, 500, 550, 600, 650, 700, 750, 780])
ax2.set_yticks([])
ax2.set_xlabel("波长 λ（nm）")
ax2.grid(False)
ax2.tick_params(axis="y", length=0)
for s in ("top", "right", "left"):
    ax2.spines[s].set_visible(False)

H.save(fig, 4, "f1_spectrum")
