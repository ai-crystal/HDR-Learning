# -*- coding: utf-8 -*-
"""f4_ycbcr：RGB → YCbCr 分离示意（Y / Cb / Cr 三通道图像化）。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np
import matplotlib.colors as mcolors

# ---------- 构造一张彩色测试图 ----------
Hh, W = 160, 240
hue = np.linspace(0, 1, W)[None, :] * np.ones((Hh, 1))
sat = np.linspace(0.05, 1.0, Hh)[:, None] * np.ones((1, W))
val = np.linspace(0.95, 0.75, Hh)[:, None] * np.ones((1, W))
hsv = np.dstack([hue, sat, val])
rgb = mcolors.hsv_to_rgb(hsv).astype(float)          # 0..1，色相横向渐变

# 左侧加一条灰度阶梯，便于看 Y
gray = np.linspace(0.0, 1.0, 40)[None, :] * np.ones((Hh, 1))
rgb[:, :40, :] = np.dstack([gray, gray, gray])

R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]

# ---------- BT.709 RGB → YCbCr ----------
Y = 0.2126 * R + 0.7152 * G + 0.0722 * B
Cb = (B - Y) / 1.8556
Cr = (R - Y) / 1.5748

fig, axes = H.plt.subplots(2, 2, figsize=(7.2, 5.2))

panels = [
    (axes[0, 0], rgb, None, "① 原始 RGB：红/绿/蓝三个通道都在表达颜色", H.NAVY),
    (axes[0, 1], Y, "gray", "② Y 亮度：明暗信息单独拎出（只看它就是黑白）", H.DARK),
    (axes[1, 0], 0.5 + Cb, "coolwarm", "③ Cb 色差：蓝-黄方向，偏离灰多少", H.BLUE),
    (axes[1, 1], 0.5 + Cr, "coolwarm", "④ Cr 色差：红-绿方向，偏离灰多少", H.RED),
]
for ax, img, cmap, title, col in panels:
    if cmap == "coolwarm":
        ax.imshow(img, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    elif cmap == "gray":
        ax.imshow(np.clip(img, 0, 1), cmap="gray", vmin=0, vmax=1, aspect="auto")
    else:
        ax.imshow(np.clip(img, 0, 1), aspect="auto")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_edgecolor(col); s.set_linewidth(1.6)
    ax.set_title(title, fontsize=9.5, color=col, loc="left", pad=5)

# 公式说明
fig.text(0.5, 0.985,
         "Y = 0.2126 R + 0.7152 G + 0.0722 B　　Cb = (B - Y) / 1.8556　　Cr = (R - Y) / 1.5748",
         ha="center", va="center", fontsize=9, color=H.GRAY)
fig.text(0.5, 0.955,
         "亮度独立成 Y，色度成为两个色差 → 才能对 Cb/Cr 单独降采样（色度采样）",
         ha="center", va="center", fontsize=9.5, color=H.ORANGE, fontweight="bold")

fig.suptitle("图 10-4　RGB → YCbCr：把亮度与色度拆开",
             fontsize=13, fontweight="bold", y=1.06)
fig.tight_layout(rect=[0, 0, 1, 0.93])
H.save(fig, 10, "f4_ycbcr")
