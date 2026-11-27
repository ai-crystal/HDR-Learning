# -*- coding: utf-8 -*-
"""第 09 章 图 3：增益图的三个组成部分（合成场景，非实拍）。

场景为程序生成：墙面基础亮度、一扇过曝的窗、一盏灯。
基础层按 SDR 白 203 nit 裁切，增益图记录每像素需要的 log2 倍率，
右图按增益图重建后再压到 1000 nit 峰值。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

rng = np.random.default_rng(7)
Hh, Ww = 240, 340
yy, xx = np.mgrid[0:Hh, 0:Ww]
u = xx / Ww
v = yy / Hh

# 线性亮度场景（nit）
L = 9.0 + 10.0 * (1.0 - v)
win = (u > 0.60) & (u < 0.90) & (v > 0.12) & (v < 0.52)
L[win] = 1500.0 - 700.0 * (v[win] - 0.12) / 0.40
lamp = 260.0 * np.exp(-(((u - 0.24) ** 2) / 0.004 + ((v - 0.30) ** 2) / 0.004))
L = L + lamp
L = L * (1.0 + 0.03 * rng.standard_normal((Hh, Ww)))
L = np.clip(L, 0.05, 4000.0)

WHITE_SDR = 203.0
base_lin = np.clip(L / WHITE_SDR, 0, 1)
sdr = np.round((base_lin ** (1 / 2.2)) * 255) / 255

rec_lin = (sdr ** 2.2) * WHITE_SDR
gain = np.log2(np.maximum(L, 1e-3) / np.maximum(rec_lin, 1e-3))
gain = np.clip(gain, 0, 3.0)

full = np.clip(rec_lin * 2 ** gain, 0, 1000.0) / 1000.0
full = full ** (1 / 2.2)

fig, axes = plt.subplots(1, 3, figsize=(7.8, 3.15),
                         gridspec_kw=dict(wspace=0.30))
for ax in axes:
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

axes[0].imshow(sdr, cmap="gray", vmin=0, vmax=1)
axes[0].set_title("(a) 基础层，SDR 8 bit", fontsize=9.5, pad=6)

im = axes[1].imshow(gain, cmap="magma", vmin=0, vmax=3)
axes[1].set_title("(b) 增益图，单位 stop", fontsize=9.5, pad=6)
cb = fig.colorbar(im, ax=axes[1], fraction=0.042, pad=0.04)
cb.ax.tick_params(labelsize=7.5)

axes[2].imshow(full, cmap="gray", vmin=0, vmax=1)
axes[2].set_title("(c) 重建后压到 1000 nit", fontsize=9.5, pad=6)

H.save(fig, 9, "f3_gainmap_parts")
