# -*- coding: utf-8 -*-
"""图 7-4：色度子采样对图形边缘的影响。

构造一幅带高饱和色块的合成图，按 BT.709 非恒定亮度矩阵转成 Y'CbCr，
再做 4:2:2 / 4:2:0 下采样和双线性上采样，看色度往亮度边缘外扩散了几像素。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt

Hh, Ww = 36, 48
img = np.zeros((Hh, Ww, 3))
img[:, :] = [0.62, 0.62, 0.62]
img[6:30, 18:31] = [0.82, 0.12, 0.10]        # 高饱和红块
img[3:5, 4:44] = [0.05, 0.12, 0.55]         # 一条细蓝线
img[26:30, 34:44] = [0.10, 0.45, 0.20]      # 小块绿色

M = np.array([[0.2126, 0.7152, 0.0722],
              [-0.1146, -0.3854, 0.5000],
              [0.5000, -0.4542, -0.0458]])
Mi = np.linalg.inv(M)


def to_ycc(a):
    return a @ M.T


def from_ycc(a):
    return a @ Mi.T


def downsample(c, kx, ky):
    h, w = c.shape
    c = c[:h - h % ky, :w - w % kx]
    c = c.reshape(h // ky, ky, w // kx, kx).mean(axis=(1, 3))
    return c


def upsampled(c, kx, ky):
    h, w = c.shape
    xi = (np.arange(w * kx) + 0.5) / kx - 0.5
    yi = (np.arange(h * ky) + 0.5) / ky - 0.5
    rows = np.array([np.interp(xi, np.arange(w), r) for r in c])
    cols = np.array([np.interp(yi, np.arange(h), r) for r in rows.T]).T
    return cols


def subsample(a, kx, ky):
    y = a[:, :, 0]
    cb = downsample(a[:, :, 1], kx, ky)
    cr = downsample(a[:, :, 2], kx, ky)
    cb = upsampled(cb, kx, ky)
    cr = upsampled(cr, kx, ky)
    cb = cb[:y.shape[0], :y.shape[1]]
    cr = cr[:y.shape[0], :y.shape[1]]
    return np.dstack([y, cb, cr])


ycc = to_ycc(img)
panels = [("4:4:4", img),
          ("4:2:2", from_ycc(subsample(ycc, 2, 1))),
          ("4:2:0", from_ycc(subsample(ycc, 2, 2)))]

fig, axes = plt.subplots(1, 3, figsize=(8.4, 3.3),
                         gridspec_kw={"wspace": 0.10})
fig.subplots_adjust(left=0.02, right=0.98, bottom=0.17, top=0.90)

for ax, (name, a) in zip(axes, panels):
    ax.imshow(np.clip(a, 0, 1), interpolation="nearest")
    ax.set_title(name, fontsize=10, pad=5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for s in ax.spines.values():
        s.set_edgecolor("#9aa7b4")

notes = ["色度与亮度同分辨率\n边缘保持锐利",
         "水平方向两像素共用一个\n色度样点，左右各渗一像素",
         "两个方向都降一半\n色度块覆盖四像素，边缘更糊"]
for ax, t in zip(axes, notes):
    ax.set_xlabel(t, fontsize=7.8, labelpad=4, linespacing=1.5)

H.save(fig, 7, "f4_chroma_subsample")
