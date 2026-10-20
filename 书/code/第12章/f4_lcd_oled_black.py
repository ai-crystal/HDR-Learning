# -*- coding: utf-8 -*-
"""第12章 f4：LCD vs OLED 黑位 / 对比度对比（条形 + 暗场画面模拟）。"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

fig = plt.figure(figsize=(7.2, 5.6))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.05], hspace=0.52, wspace=0.30)

devs = ["LCD\n无分区", "Mini-LED\nLCD", "WOLED /\nQD-OLED", "MicroLED"]
black = np.array([0.10, 0.02, 0.0005, 0.0001])   # nit
peak = np.array([600, 1800, 800, 4000])          # nit
contrast = peak / black
cols = [H.GRAY, H.TEAL, H.RED, H.PURPLE]

# ---------------- 左上：黑位（对数） ----------------
ax1 = fig.add_subplot(gs[0, 0])
b = ax1.bar(devs, black, color=cols, edgecolor="#4a5666", lw=0.6)
ax1.set_yscale("log")
ax1.set_ylim(1e-5, 1.0)
ax1.set_yticks([1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0])
ax1.set_yticklabels(["0.00001", "0.0001", "0.001", "0.01", "0.1", "1"])
ax1.set_ylabel("黑位亮度 (nit，对数轴)")
ax1.set_title("黑位：谁能真正关到 0？", fontsize=10.5, pad=5)
for rect, v in zip(b, black):
    ax1.text(rect.get_x() + rect.get_width() / 2, v * 1.35, f"{v:g}",
             ha="center", fontsize=8.2, color=H.NAVY, fontweight="bold")
ax1.tick_params(axis="x", labelsize=8.0)
ax1.grid(axis="x", visible=False)
ax1.axhspan(1e-5, 0.001, color=H.RED, alpha=0.07)
ax1.axhline(0.001, color=H.RED, ls="--", lw=1.0)
ax1.text(1.85, 0.055, "\"真黑\"区（<0.001 nit）", ha="left",
         fontsize=7.6, color=H.RED, fontweight="bold")

# ---------------- 右上：对比度（对数） ----------------
ax2 = fig.add_subplot(gs[0, 1])
devs2 = ["LCD 无分区\n峰值 600 nit", "Mini-LED\n峰值 1800 nit",
         "WOLED / QD-OLED\n峰值 800 nit", "MicroLED\n峰值 4000 nit"]
b2 = ax2.barh(devs2, contrast, color=cols, edgecolor="#4a5666", lw=0.6)
ax2.set_xscale("log")
ax2.set_xlim(1e3, 1e9)
ax2.set_xticks([1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9])
ax2.set_xticklabels(["1千", "1万", "10万", "100万", "1000万", "1亿", "10亿"], fontsize=8.0)
ax2.set_xlabel("对比度 = 峰值 ÷ 黑位（对数轴，:1）")
ax2.set_title("对比度：黑位小才是关键", fontsize=10.5, pad=5)
labels = ["10k:1", "90k:1", "1.6M:1", "40M:1"]
for rect, v, lab in zip(b2, contrast, labels):
    ax2.text(v * 1.5, rect.get_y() + rect.get_height() / 2, lab, va="center",
             fontsize=7.6, color=H.NAVY, fontweight="bold")
ax2.tick_params(axis="y", labelsize=7.6)
ax2.grid(axis="y", visible=False)

# ---------------- 下：暗场画面模拟 ----------------
N = 260
yy, xx = np.mgrid[0:N, 0:N]
stars = np.zeros((N, N))
for (cy, cx, amp, s) in [(95, 120, 1000, 2.2), (55, 205, 300, 1.6), (175, 70, 90, 1.2),
                         (205, 180, 40, 1.0)]:
    stars += amp * np.exp(-(((yy - cy) ** 2 + (xx - cx) ** 2) / (2 * s ** 2)))
halo = gaussian_filter(stars, 11.0)
halo = halo / halo.max()

lcd = 0.10 + stars + 0.15 * halo          # 黑位抬起 + 亮区溢出光晕
oled = 0.0005 + stars                     # 接近 0 的黑位，无光晕

def encode(v):
    return np.clip(v / 0.5, 0, 1)

ax3 = fig.add_subplot(gs[1, 0])
ax3.grid(False)
ax3.imshow(encode(lcd), cmap="gray", vmin=0, vmax=1)
ax3.set_xticks([]); ax3.set_yticks([])
ax3.set_title("LCD：夜空发灰，星星糊一圈光晕", fontsize=9.6, color=H.TEAL, fontweight="bold")
ax3.text(8, 244, "黑位 0.1 nit → 泛灰 + 光晕", fontsize=7.2, color="white")
ax3.set_xlabel("同一幅\"星空\"内容在两种面板上的观感（示意）", fontsize=8.2)

ax4 = fig.add_subplot(gs[1, 1])
ax4.grid(False)
ax4.imshow(encode(oled), cmap="gray", vmin=0, vmax=1)
ax4.set_xticks([]); ax4.set_yticks([])
ax4.set_title("OLED：夜空真黑，高光边缘干净", fontsize=9.6, color=H.RED, fontweight="bold")
ax4.text(8, 244, "黑位 ≈0.0005 nit → 真黑", fontsize=7.2, color="white")
ax4.set_xlabel("同一幅内容：暗部干净 → 立体感来自\"暗中有亮\"", fontsize=8.2)

fig.suptitle("为什么 800 nit 的 OLED 观感胜过更亮的 LCD", fontsize=13.5,
             fontweight="bold", color=H.NAVY, y=0.985)
H.save(fig, 12, "f4_lcd_oled_black")
