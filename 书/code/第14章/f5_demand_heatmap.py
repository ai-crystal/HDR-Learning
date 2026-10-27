# -*- coding: utf-8 -*-
"""第 14 章 图 14-4：带宽需求热图（分辨率 × 帧率），叠加各接口的有效带宽能力线。
三个面板分别是 8bit 4:4:4 / 10bit 4:4:4 / 10bit 4:2:0 三种每像素位数。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

OVH = 1.25

RES = [("1080p", 1920 * 1080), ("1440p", 2560 * 1440), ("4K UHD", 3840 * 2160),
       ("5K", 5120 * 2880), ("8K", 7680 * 4320)]
panel_bpp = [("（a）8bit 4:4:4", 24), ("（b）10bit 4:4:4", 30), ("（c）10bit 4:2:0", 15)]

fps = np.linspace(20, 150, 320)
mp = np.linspace(1.8, 34.0, 320)
F, M = np.meshgrid(fps, mp)

# 接口有效带宽能力线（Gbps）
caps = [(14.4, "HDMI 2.0"), (25.9, "DP 1.4"), (42.7, "HDMI 2.1"), (77.4, "DP 2.x")]
XLAB = 145.0        # 能力线数字标签所在的帧率位置

fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.8), sharey=True)
mesh = None
for ax, (title, bpp) in zip(axes, panel_bpp):
    Z = M * 1e6 * F * bpp * OVH / 1e9
    mesh = ax.pcolormesh(fps, mp, Z, cmap="viridis", norm=LogNorm(vmin=1, vmax=150),
                         shading="auto", rasterized=True)
    ax.contour(fps, mp, Z, levels=[c[0] for c in caps],
               colors="white", linewidths=1.15, linestyles="--")
    # 能力线数字标签（沿 x=144 处与该曲线的交点，解析求出）
    for lv, _ in caps:
        yy = lv * 1e3 / (XLAB * bpp * OVH)
        if 2.0 <= yy <= 32.0:
            ax.text(XLAB, yy, f"{lv:g}", fontsize=6.0, color="white", ha="right",
                    va="center", fontweight="bold", zorder=7,
                    bbox=dict(boxstyle="square,pad=0.12", fc="#2b3a4a",
                              ec="white", lw=0.5, alpha=0.75))
    # 键工况点
    for fp, mpv, name in [(60, 8.29, "4K60"), (120, 8.29, "4K120"), (60, 33.18, "8K60")]:
        v = mpv * 1e6 * fp * bpp * OVH / 1e9
        ax.plot(fp, mpv, "o", ms=4.2, mfc="white", mec="#12233b", mew=1.0, zorder=6)
        ax.text(fp - 3.5, mpv + 1.3, f"{name} {v:.1f}", fontsize=6.0, color="white",
                fontweight="bold", zorder=7, ha="right", va="bottom")
    ax.set_title(title, fontsize=9.6, color=H.NAVY, pad=6)
    ax.set_xlabel("帧率（Hz）", fontsize=9.5)
    ax.set_xticks([30, 60, 120, 144])
    ax.set_xlim(20, 150)
    ax.set_ylim(1.8, 34)
    ax.grid(False)

axes[0].set_yscale("log")
axes[0].set_yticks([r[1] / 1e6 for r in RES])
axes[0].set_yticklabels([f"{r[0]}\n{r[1]/1e6:.1f} MP" for r in RES], fontsize=7.0)
axes[0].set_ylabel("分辨率（像素总数）", fontsize=9.5)

fig.subplots_adjust(top=0.845, bottom=0.19, left=0.088, right=0.90, wspace=0.13)
cax = fig.add_axes([0.925, 0.19, 0.017, 0.655])
cb = fig.colorbar(mesh, cax=cax)
cb.set_label("所需带宽（Gbps，含 1.25 开销）", fontsize=8.2)
cb.ax.tick_params(labelsize=7.4)
for i, a in enumerate(axes):
    print(i, a.get_position().bounds, cax.get_position().bounds)

fig.suptitle("图 14-4　带宽需求热图：白虚线是各接口的有效带宽“能力线”，越过就装不下",
             fontsize=12.2, fontweight="bold", y=1.02)
fig.text(0.5, 0.005,
         "白虚线自下而上：14.4 = HDMI 2.0　25.9 = DP 1.4　42.7 = HDMI 2.1　77.4 = DP 2.x（均为有效带宽 Gbps）；"
         "圆点为 4K60 / 4K120 / 8K60 工况，数字为所需带宽",
         ha="center", va="bottom", fontsize=7.0, color=H.GRAY)
fig.subplots_adjust(top=0.845, bottom=0.19, left=0.088, right=0.90, wspace=0.13)
H.save(fig, 14, "f5_demand_heatmap")
