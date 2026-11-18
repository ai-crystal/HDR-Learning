# -*- coding: utf-8 -*-
"""第 06 章 图 2：一幅合成 HDR 画面的亮度分布直方图（按图计算，示例用途）。

合成画面：天空竖直渐变（0.05–8 nit）+ 太阳（约 5000 nit）+ 建筑墙面（约 0.3 nit）
+ 窗灯（约 800 nit）+ 地面（0.8 nit）。直方图按 PQ 码值统计像素数。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

Hh, Ww = 216, 384
yy, xx = np.mgrid[0:1:Hh * 1j, 0:1:Ww * 1j]

img = 0.05 + 8.0 * (1 - yy) ** 2                       # 天空
img = np.maximum(img, 5000.0 * np.exp(-(((xx - 0.74) ** 2 + (yy - 0.16) ** 2) / (2 * 0.018 ** 2))))
wall = (xx > 0.06) & (xx < 0.32) & (yy > 0.52) & (yy < 0.96)
img = np.where(wall, 0.3, img)
for wx in (0.10, 0.16, 0.22, 0.28):
    for wy in (0.58, 0.68, 0.78, 0.88):
        img = np.where((np.abs(xx - wx) < 0.012) & (np.abs(yy - wy) < 0.02), 800.0, img)
img = np.where(yy > 0.93, 0.8, img)

code = H.pq_oetf(img) * 1023.0
flat = code.ravel()

p50, p99, p999 = np.percentile(flat, [50, 99, 99.9])
max_nit = float(img.max())

fig, ax = plt.subplots(figsize=(7.4, 4.4))
ax.hist(flat, bins=np.linspace(0, 1023, 129), color=H.NAVY, alpha=0.85, lw=0)
ax.set_yscale("log")
ax.set_xlim(0, 1023)
ax.set_ylim(4, 3e5)
ax.set_xlabel("PQ 码值（10 位）")
ax.set_ylabel("像素数（对数刻度）")

for val, color, name in [(p50, H.TEAL, "P50"), (p99, H.ORANGE, "P99"), (p999, H.RED, "P99.9")]:
    ax.axvline(val, color=color, lw=1.3, ls="-")
    ax.text(val + 8, 1.1e4, f"{name} 码 {val:.0f}", color=color, fontsize=8,
            rotation=90, ha="left", va="bottom")

ax.axvline(float(H.pq_oetf(203)) * 1023, color=H.GRAY, lw=1.2, ls="--")
ax.text(float(H.pq_oetf(203)) * 1023 - 10, 1.1e4, "203 nit 参考白",
        color=H.GRAY, fontsize=8, rotation=90, ha="right", va="bottom")

ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim())
ticks_nit = [1, 10, 100, 1000, 10000]
ax2.set_xticks([float(H.pq_oetf(t)) * 1023 for t in ticks_nit])
ax2.set_xticklabels([str(t) for t in ticks_nit], fontsize=8.5)
ax2.minorticks_off()
ax2.set_xlabel("对应的绝对亮度（nit）", fontsize=9.5)

H.save(fig, 6, "f2_lum_hist")
