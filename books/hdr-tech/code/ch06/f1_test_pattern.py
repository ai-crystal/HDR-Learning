# -*- coding: utf-8 -*-
"""第 06 章 图 1：HDR 测试图案（代码生成）。

四个子图：
  (a) 灰阶阶梯：11 级，标注 10 位码值与对应绝对亮度；
  (b) 近黑阶梯：码值 0–64，检查黑位裁切与暗部层次；
  (c) 窗口图案：面积 1%、2%、10% 的白块，用于测峰值亮度与 ABL（按比例绘制）；
  (d) 色块：白、灰与六个饱和色（以 sRGB 近似显示，实际图案应在 Rec.2020 / PQ 域生成）。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt


def code_to_nit(code):
    return float(H.pq_eotf(np.array([code / 1023.0]))[0])


fig = plt.figure(figsize=(7.4, 6.2))
gs = fig.add_gridspec(2, 2, hspace=0.46, wspace=0.18,
                      left=0.05, right=0.98, top=0.92, bottom=0.05)

# ---------- (a) 灰阶阶梯 ----------
axa = fig.add_subplot(gs[0, 0])
codes_a = np.linspace(0, 1023, 11).astype(int)
for i, c in enumerate(codes_a):
    n = code_to_nit(c)
    axa.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=str(c / 1023.0),
                                edgecolor="#4a5666", lw=0.7))
    axa.text(i + 0.5, -0.12, str(c), ha="center", va="top", fontsize=7.2)
    axa.text(i + 0.5, 1.07, ("0" if n < 1 else f"{n:.0f}"), ha="center",
             va="bottom", fontsize=6.8, color=H.NAVY)
axa.set_xlim(0, 11)
axa.set_ylim(-0.58, 1.42)
axa.set_axis_off()
axa.text(0, -0.44, "下排为 10 位码值，上排为对应亮度（nit）", fontsize=7.8, color=H.GRAY)
axa.set_title("(a) 灰阶阶梯", fontsize=10, pad=2)

# ---------- (b) 近黑阶梯 ----------
axb = fig.add_subplot(gs[0, 1])
codes_b = np.arange(0, 65, 8)
for i, c in enumerate(codes_b):
    n = code_to_nit(c)
    axb.add_patch(plt.Rectangle((i, 0), 1, 1, facecolor=str(c / 1023.0),
                                edgecolor="#4a5666", lw=0.7))
    axb.text(i + 0.5, -0.12, str(c), ha="center", va="top", fontsize=7.2)
    axb.text(i + 0.5, -0.46, f"{n:.3f}", ha="center", va="top", fontsize=6.4,
             color=H.NAVY)
axb.set_xlim(0, len(codes_b))
axb.set_ylim(-0.78, 1.42)
axb.set_axis_off()
axb.text(0, -0.66, "码值 0–64（下排为亮度，nit）；这些层次只有在正确校准的显示器上才能分开",
         fontsize=7.2, color=H.GRAY)
axb.set_title("(b) 近黑阶梯", fontsize=10, pad=2)

# ---------- (c) 窗口图案 ----------
axc = fig.add_subplot(gs[1, 0])
axc.set_xlim(0, 1)
axc.set_ylim(0, 1)
axc.set_aspect("equal")
axc.set_axis_off()
for i, area in enumerate([1, 2, 10]):
    x0 = 0.03 + i * 0.34
    side = 0.26
    axc.add_patch(plt.Rectangle((x0, 0.40), side, side, facecolor="#111111",
                                edgecolor="#4a5666", lw=0.8))
    s = side * np.sqrt(area / 100.0)
    axc.add_patch(plt.Rectangle((x0 + side / 2 - s / 2, 0.40 + side / 2 - s / 2),
                                s, s, facecolor="white", edgecolor="none"))
    axc.text(x0 + side / 2, 0.33, f"{area}%", ha="center", va="top", fontsize=8)
axc.text(0.03, 0.90, "白块面积与整屏面积之比 1%、2%、10%，按比例绘制",
         fontsize=7.8, color=H.GRAY)
axc.set_title("(c) 窗口图案", fontsize=10, pad=2)

# ---------- (d) 色块 ----------
axd = fig.add_subplot(gs[1, 1])
patches = [("白", (1, 1, 1)), ("灰 50%", (0.5, 0.5, 0.5)),
           ("R", (1, 0, 0)), ("G", (0, 1, 0)),
           ("B", (0, 0, 1)), ("C", (0, 1, 1)),
           ("M", (1, 0, 1)), ("Y", (1, 1, 0))]
for i, (name, rgb) in enumerate(patches):
    r, c = divmod(i, 4)
    x0 = c * 0.25
    y0 = 0.58 - r * 0.50
    axd.add_patch(plt.Rectangle((x0 + 0.012, y0), 0.226, 0.34, facecolor=rgb,
                                edgecolor="#4a5666", lw=0.7))
    axd.text(x0 + 0.125, y0 - 0.05, name, ha="center", va="top", fontsize=7.8)
axd.set_xlim(0, 1)
axd.set_ylim(0, 1)
axd.set_axis_off()
axd.set_title("(d) 色块（饱和度检查）", fontsize=10, pad=2)

H.save(fig, 6, "f1_test_pattern")
