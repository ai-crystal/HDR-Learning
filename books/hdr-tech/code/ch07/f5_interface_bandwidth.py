# -*- coding: utf-8 -*-
"""图 7-5：常见 HDR 信号格式的净数据率与三条接口上限。

数据率按有效像素计算：宽 × 高 × 每像素字节数 × 帧率，不含消隐区，
实际链路还要多出几个百分点。接口数值取 HDMI 2.1 FRL 的 48 Gbps 总带宽、
DisplayPort 2.0 UHBR20 的 77.4 Gbps 有效带宽、HDMI 2.0 的 18 Gbps。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt

FMT = [
    ("1080p60　8 bit 4:2:0", 1920, 1080, 1.5, 8, 60),
    ("4K60　10 bit 4:2:0", 3840, 2160, 1.5, 10, 60),
    ("4K120　10 bit 4:2:0", 3840, 2160, 1.5, 10, 120),
    ("4K60　12 bit 4:4:4", 3840, 2160, 3.0, 12, 60),
    ("8K60　10 bit 4:2:0", 7680, 4320, 1.5, 10, 60),
    ("4K120　12 bit 4:4:4", 3840, 2160, 3.0, 12, 120),
    ("8K60　12 bit 4:4:4", 7680, 4320, 3.0, 12, 60),
]

HDMI21 = 48.0
rows = []
for name, w, h, spp, bit, fps in FMT:
    gbps = w * h * spp * bit * fps / 1e9
    rows.append((name, gbps))

fig, ax = plt.subplots(figsize=(7.9, 4.3))
fig.subplots_adjust(left=0.235, right=0.975, bottom=0.175, top=0.845)

ypos = np.arange(len(rows))[::-1]
for (name, v), y in zip(rows, ypos):
    c = H.BLUE if v <= HDMI21 else H.ORANGE
    ax.barh(y, v, height=0.58, color=c, edgecolor="none", zorder=3)
    ax.text(v + 0.9, y, f"{v:.1f}", va="center", ha="left", fontsize=8.2,
            color=H.DARK, zorder=4)

ax.set_yticks(ypos)
ax.set_yticklabels([n for n, _ in rows], fontsize=8.6)
ax.set_xlim(0, 86)
ax.set_ylim(-0.75, len(rows) - 0.15)
ax.set_xlabel("净数据率（Gbps）")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)

for xv, lab, c in [(18.0, "HDMI 2.0\n18", H.GRAY),
                   (48.0, "HDMI 2.1 FRL\n48", H.NAVY),
                   (77.4, "DP 2.0 UHBR20\n77.4", H.TEAL)]:
    ax.axvline(xv, color=c, lw=1.1, ls=(0, (4, 3)), zorder=2)
    ax.text(xv, len(rows) - 0.05, lab, fontsize=7.6, color=c,
            ha="center", va="bottom", linespacing=1.4)

fig.text(0.02, 0.035,
         "蓝色格式可直接走 HDMI 2.1，橙色格式需要 DSC 或降到 4:2:0、降帧率",
         fontsize=7.8, color=H.GRAY, ha="left", va="center")

H.save(fig, 7, "f5_interface_bandwidth")
