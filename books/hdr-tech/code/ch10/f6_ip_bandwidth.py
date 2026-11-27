# -*- coding: utf-8 -*-
"""第 10 章 图 6：4K HDR 信号在 IP 链路上的带宽账。

按 3840×2160、50 帧、4:2:2、10 bit 计算，未压缩净荷为
3840×2160×50×20 bit = 8.29 Gb/s。JPEG XS 的 2:1、3:1、6:1 在此基线上折算。
参考线是 10GbE、25GbE、100GbE 端口的可用带宽（按 0.95 折算）。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

raw = 3840 * 2160 * 50 * 20 / 1e9
items = [
    ("HEVC 贡献编码", 0.035, H.GREEN),
    ("JPEG XS 6:1", raw / 6, H.TEAL),
    ("JPEG XS 3:1", raw / 3, H.BLUE),
    ("JPEG XS 2:1", raw / 2, H.ORANGE),
    ("ST 2110-20 未压缩", raw * 1.03, H.NAVY),
]

fig, ax = plt.subplots(figsize=(8.2, 4.1))
fig.subplots_adjust(left=0.225, right=0.965, bottom=0.145, top=0.935)

ypos = np.arange(len(items))
for y, (name, val, c) in zip(ypos, items):
    ax.barh(y, val, height=0.56, color=c, alpha=0.88, zorder=3)
    if val > 0.3:
        ax.text(val * 0.93, y, f"{val:.2f}", va="center", ha="right", fontsize=9.0,
                color="white", fontweight="bold", zorder=5)
    else:
        ax.text(val * 1.25, y, f"{val:.3f}", va="center", ha="left", fontsize=8.6,
                color=c, fontweight="bold", zorder=5)

for cap, lab in [(10 * 0.95, "10GbE"), (25 * 0.95, "25GbE"), (100 * 0.95, "100GbE")]:
    ax.axvline(cap, color=H.RED, lw=1.0, ls=(0, (5, 3)), zorder=2)
    ax.text(cap, 4.52, lab, fontsize=8.0, color=H.RED, ha="center", va="bottom",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.4))

ax.set_yticks(ypos)
ax.set_yticklabels([i[0] for i in items], fontsize=9.2)
ax.set_xscale("log")
ax.set_xlim(0.01, 320)
ax.set_ylim(-0.55, 5.05)
ax.set_xlabel("单路信号的带宽（Gb/s，对数刻度）")
ax.set_xticks([0.01, 0.1, 1, 10, 100])
ax.set_xticklabels(["0.01", "0.1", "1", "10", "100"])
ax.minorticks_off()
ax.grid(axis="y", visible=False)

H.save(fig, 10, "f6_ip_bandwidth")
print("raw %.2f Gb/s" % raw)
