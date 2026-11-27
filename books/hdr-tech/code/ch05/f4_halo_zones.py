# -*- coding: utf-8 -*-
"""第 05 章 图 4：光晕幅度与宽度随分区数的变化（一维面板模型计算，非厂商数据）。

沿用图 5-1 的模型：目标画面为 0.1 nit 暗背景中央 60 px 宽、1000 nit 的高光条；
背光取分区内最大值，经扩散片高斯平滑（sigma = 0.45 个分区宽）；
液晶透射率被限制在 [1/2000, 1]；显示亮度 = 背光 × 透射率。

高光条落在分区里的位置会影响光晕强度，因此把高光条在一个分区宽度内平移 8 个相位，
取平均，得到"内容位置任意"时的典型值：
  光晕幅度 = 暗区靠近高光一侧的最大显示亮度（背景 0.1 nit）；
  光晕宽度 = 从高光边缘到显示亮度回落到背景 1.1 倍处的距离。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

W, OBJ = 1920, 60
BG, PEAK = 0.1, 1000.0


def gauss_kernel(sigma):
    n = int(max(3, np.ceil(6 * sigma)))
    x = np.arange(-n, n + 1)
    g = np.exp(-x ** 2 / (2 * sigma ** 2))
    return g / g.sum()


def simulate(zones, shift=0.0, cr=2000.0, psf=0.45):
    target = np.full(W, BG)
    c = W // 2 + shift
    target[int(c - OBJ / 2): int(c + OBJ / 2)] = PEAK
    zw = W / zones
    idx = np.minimum((np.arange(W) / zw).astype(int), zones - 1)
    zmax = np.zeros(zones)
    np.maximum.at(zmax, idx, target)
    bl = zmax[idx]
    g = gauss_kernel(psf * zw)
    pad = len(g) // 2
    bl = np.convolve(np.pad(bl, pad, mode="edge"), g, mode="same")[pad:-pad]
    lc = np.clip(target / np.maximum(bl, 1e-9), 1.0 / cr, 1.0)
    return bl, bl * lc


zones = np.unique(np.round(np.logspace(np.log10(8), np.log10(1024), 21)).astype(int))
peak_avg, width_avg, zone_px = [], [], []

for z in zones:
    zw = W / z
    peaks, widths = [], []
    for k in range(8):
        _, disp = simulate(z, shift=k * zw / 8.0)
        right = int(W // 2 + OBJ / 2 + k * zw / 8.0)
        seg = disp[right: W // 2 + 600]
        peaks.append(seg.max())
        over = np.where(seg > BG * 1.1)[0]
        widths.append(over.max() if len(over) else np.nan)
    peak_avg.append(np.mean(peaks))
    width_avg.append(np.nanmean(widths) if np.any(~np.isnan(widths)) else 1.0)
    zone_px.append(zw)

peak_avg = np.array(peak_avg)
width_avg = np.array(width_avg, dtype=float)
zone_px = np.array(zone_px)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 4.0))
fig.subplots_adjust(wspace=0.30)

ax1.plot(zones, peak_avg, "o-", color=H.ORANGE, lw=2.0, ms=4.0)
ax1.axhline(BG, color=H.GRAY, lw=1.0, ls=":")
ax1.text(8.6, BG * 1.06, "背景 0.1 nit", fontsize=8.2, color=H.GRAY, va="bottom")
ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlim(7, 1400)
ax1.set_ylim(0.08, 1.6)
ax1.set_yticks([0.1, 0.2, 0.5, 1])
ax1.set_yticklabels(["0.1", "0.2", "0.5", "1"])
ax1.set_xticks([8, 32, 128, 512, 1024])
ax1.set_xticklabels(["8", "32", "128", "512", "1024"])
ax1.minorticks_off()
ax1.set_xlabel("分区数（个，对数刻度）")
ax1.set_ylabel("暗区最高亮度（nit，对数刻度）")
ax1.set_title("(a) 光晕的幅度", fontsize=10, pad=4)

ax2.plot(zones, width_avg, "o-", color=H.NAVY, lw=2.0, ms=4.0, label="光晕宽度")
ax2.plot(zones, zone_px, "--", color=H.LGRAY, lw=1.7, label="一个分区的宽度")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlim(7, 1400)
ax2.set_ylim(2, 500)
ax2.set_xticks([8, 32, 128, 512, 1024])
ax2.set_xticklabels(["8", "32", "128", "512", "1024"])
ax2.minorticks_off()
ax2.set_xlabel("分区数（个，对数刻度）")
ax2.set_ylabel("光晕宽度（像素，对数刻度）")
ax2.legend(loc="lower left", fontsize=8.4)
ax2.set_title("(b) 光晕的宽度", fontsize=10, pad=4)

H.save(fig, 5, "f4_halo_zones")
print("peak", np.round(peak_avg, 3))
print("width", np.round(width_avg, 1))
