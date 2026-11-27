# -*- coding: utf-8 -*-
"""第 11 章 图 6：三种转换错误在波形上的样子。

用一张合成的画面（天空、地面、暗处剪影、中间调人物、招牌、高光窗口）算出亮度波形：
横轴是画面水平位置，纵轴是 SDR 信号电平，颜色深浅表示该列落在该电平上的像素密度。
(a) 按 203 nit 参考白定标的正确转换；
(b) 把 260 nit 当成白点，天空与窗口一起贴顶削平；
(c) 把 2 nit 以下直接归零，剪影与地面暗部贴底死黑。
画面是合成的，亮度值按用途给定，不代表实拍素材。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
from matplotlib.colors import LinearSegmentedColormap

H.set_book("hdr-tech")
plt = H.plt

rng = np.random.default_rng(11)
W, Hh = 960, 540
yy, xx = np.mgrid[0:Hh, 0:W].astype(float)

L = np.zeros((Hh, W))
sky = yy < 250
L[sky] = 350.0 - 150.0 * (yy[sky] / 250.0)
ground = ~sky
L[ground] = 18.0 + 7.0 * rng.random((ground.sum(),))

sil = (xx > 110) & (xx < 300) & (yy > 300) & (yy < 480)
L[sil] = 0.8
face = (xx > 430) & (xx < 520) & (yy > 300) & (yy < 430)
L[face] = 120.0
sign = (xx > 780) & (xx < 900) & (yy > 330) & (yy < 450)
L[sign] = 60.0
lamp = (xx > 858) & (xx < 905) & (yy > 95) & (yy < 200)
L[lamp] = 800.0
win = (xx > 610) & (xx < 750) & (yy > 90) & (yy < 250)
L[win] = 3000.0


def ire(lin):
    return 100.0 * np.clip(lin, 0, 1) ** (1 / 2.4)


def tone(t, knee=203.0, k_mid=0.72, gamma=0.80):
    lo = (t / knee) * k_mid
    hi = k_mid + (1 - k_mid) * (np.log10(np.maximum(t, knee) / knee)
                                / np.log10(4000.0 / knee)) ** gamma
    return ire(np.where(t <= knee, lo, hi))


GOOD = tone(L)
OVER = ire(np.clip(L / 260.0, 0, 1))
CRUSH = np.where(L < 2.0, 0.0, GOOD)

CASES = [("(a)", GOOD), ("(b)", OVER), ("(c)", CRUSH)]

cmap = LinearSegmentedColormap.from_list(
    "wv", ["#ffffff", "#cddbe9", "#5b86b0", "#1f4e79", "#0d2740"])

fig, axes = plt.subplots(1, 3, figsize=(7.8, 3.3), sharey=True,
                         gridspec_kw=dict(wspace=0.08))
fig.subplots_adjust(left=0.085, right=0.985, bottom=0.155, top=0.955)

for ax, (label, data) in zip(axes, CASES):
    dens, _, _ = np.histogram2d(
        np.tile(np.arange(W), Hh), data.ravel(),
        bins=[np.linspace(0, W, 121), np.linspace(0, 104, 209)])
    ax.imshow(np.log1p(dens.T), origin="lower", aspect="auto", cmap=cmap,
              extent=(0, W, 0, 104), interpolation="nearest", vmin=0)
    ax.axhline(100, color=H.RED, lw=0.9, ls=(0, (5, 3)))
    ax.axhline(0, color="#8a97a6", lw=0.8, ls=":")
    ax.set_xlim(0, W)
    ax.set_ylim(0, 106)
    ax.set_xticks([])
    ax.set_xlabel("画面水平位置", fontsize=8.6)
    ax.grid(False)
    ax.text(16, 102, label, fontsize=9.0, color=H.DARK, fontweight="bold",
            va="center", ha="left")

axes[0].set_ylabel("SDR 信号电平（IRE）", fontsize=8.8)
axes[0].annotate("天空 200–350 nit", xy=(250, 88), xytext=(26, 74),
                 fontsize=7.2, color="#40505f", ha="left", va="center",
                 arrowprops=dict(arrowstyle="->", color="#7f8c8d", lw=0.8,
                                 connectionstyle="arc3,rad=0.2"))
axes[0].annotate("窗口 3000 nit", xy=(660, 97), xytext=(330, 60),
                 fontsize=7.2, color="#8a6a20", ha="left", va="center",
                 arrowprops=dict(arrowstyle="->", color="#c8a24a", lw=0.9,
                                 connectionstyle="arc3,rad=0.22"))
axes[0].annotate("人物 120 nit", xy=(470, 71), xytext=(240, 46),
                 fontsize=7.2, color="#40505f", ha="left", va="center",
                 arrowprops=dict(arrowstyle="->", color="#7f8c8d", lw=0.8,
                                 connectionstyle="arc3,rad=-0.2"))
axes[0].annotate("剪影 0.8 nit", xy=(200, 6), xytext=(330, 16),
                 fontsize=7.2, color="#40505f", ha="left", va="center",
                 arrowprops=dict(arrowstyle="->", color="#7f8c8d", lw=0.8,
                                 connectionstyle="arc3,rad=0.2"))

axes[1].annotate("天空与窗口一起削平\n31% 的像素贴顶",
                 xy=(400, 100), xytext=(330, 82),
                 fontsize=7.2, color=H.RED, ha="left", va="center",
                 arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                                 connectionstyle="arc3,rad=0.2"))
axes[2].annotate("剪影整块贴底\n暗部层次归零", xy=(205, 1), xytext=(330, 18),
                 fontsize=7.2, color=H.RED, ha="left", va="center",
                 arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                                 connectionstyle="arc3,rad=0.2"))

print("贴顶百分比", [round(100 * float((d >= 99.5).mean()), 1) for _, d in CASES])

H.save(fig, 11, "f6_error_waveforms")
