# -*- coding: utf-8 -*-
"""第 06 章 图 3：HDR 波形图（对合成画面逐列统计生成，示例用途）。

做法与波形监视器相同：把画面按列切开，统计每一列中落在各 PQ 码值区间的像素数，
得到"横轴=画面位置、纵轴=码值、亮度=该码值的像素密度"的二维图。
合成画面含天空渐变（约 0.05–8 nit）、太阳（约 5000 nit）、左侧亮窗（约 800 nit）、
地面（约 0.8 nit）与暗部剪影（约 0.01 nit）。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
from matplotlib.colors import LinearSegmentedColormap, PowerNorm

H.set_book("hdr-tech")
plt = H.plt

Hh, Ww = 216, 384
yy, xx = np.mgrid[0:1:Hh * 1j, 0:1:Ww * 1j]

img = 0.05 + 8.0 * (1 - yy) ** 2
img = np.maximum(img, 5000.0 * np.exp(-(((xx - 0.62) ** 2 + (yy - 0.14) ** 2) / (2 * 0.016 ** 2))))
img = np.where((yy > 0.42) & (yy < 0.62), 2.5 * (1 - yy) + 0.35, img)          # 远山
img = np.where(yy > 0.62, 0.8 + 0.4 * xx, img)                                 # 地面
img = np.where((xx > 0.04) & (xx < 0.20) & (yy > 0.30) & (yy < 0.58), 800.0, img)  # 亮窗
img = np.where((xx > 0.82) & (xx < 0.92) & (yy > 0.20), 0.012, img)            # 暗剪影

code = H.pq_oetf(img) * 1023.0
nb = 256
bins = np.clip((code / 1024.0 * nb).astype(int), 0, nb - 1)

wf = np.zeros((nb, Ww))
for c in range(Ww):
    np.add.at(wf[:, c], bins[:, c], 1)

cmap = LinearSegmentedColormap.from_list(
    "scope", ["#000000", "#0b3a12", "#1f9e3d", "#7bf27f", "#ffffff"])

fig, ax = plt.subplots(figsize=(7.6, 4.4))
ax.imshow(wf, origin="lower", aspect="auto", cmap=cmap,
          extent=[0, 1920, 0, 1023],
          norm=PowerNorm(gamma=0.45, vmin=0, vmax=wf.max()),
          interpolation="nearest")

ax.set_xlabel("画面水平位置（像素）")
ax.set_ylabel("PQ 码值（10 位）")
ax.set_xticks([0, 480, 960, 1440, 1920])
ax.set_yticks([0, 256, 512, 768, 1023])
ax.set_yticklabels(["0", "256", "512", "768", "1023"])
ax.grid(False)

axr = ax.twinx()
axr.set_ylim(ax.get_ylim())
axr.set_yticks([float(H.pq_oetf(v)) * 1023 for v in (1, 10, 100, 1000, 10000)])
axr.set_yticklabels(["1", "10", "100", "1000", "10000"], fontsize=8.5)
axr.minorticks_off()
axr.set_ylabel("对应的绝对亮度（nit）", fontsize=9.5)
axr.grid(False)

H.save(fig, 6, "f3_waveform")
