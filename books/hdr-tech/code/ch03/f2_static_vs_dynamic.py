# -*- coding: utf-8 -*-
"""图 3-2：静态元数据与动态元数据对逐帧亮度的处理差异（示意，合成数据）。

上曲线为每帧最亮像素，下曲线为帧平均亮度，均按人工构造的三段场景生成
（内景 320、窗口逆光 400、夜景 180，中段含一次 4000 cd/m² 的镜面闪光）。
MaxCLL / MaxFALL 按 CTA-861.3 的定义在整段序列上取极值；
动态元数据按逐帧滑动窗口峰值生成，仅用于说明"逐帧跟随"的行为。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import FuncFormatter, NullFormatter
plt.rcParams["mathtext.fontset"] = "dejavusans"

rng = np.random.default_rng(7)
N = 144
f = np.arange(N)
peak = np.zeros(N)
avg = np.zeros(N)

# 场景 1：内景（0–47）
peak[0:48] = 320 + 25 * np.sin(f[0:48] / 9.0)
avg[0:48] = 52 + 6 * np.sin(f[0:48] / 11.0)
# 场景 2：窗边逆光（48–95），第 61–63 帧为镜面闪光
peak[48:96] = 400 + 40 * np.sin(f[48:96] / 7.0)
avg[48:96] = 118 + 12 * np.sin(f[48:96] / 9.0)
peak[61:64] = 4000.0
avg[61:64] = 260.0
# 场景 3：夜景（96–143）
peak[96:] = 185 + 18 * np.sin(f[96:] / 8.0)
avg[96:] = 20 + 4 * np.sin(f[96:] / 10.0)

peak *= 1.0 + 0.02 * rng.standard_normal(N)
avg *= 1.0 + 0.02 * rng.standard_normal(N)

maxcll = peak.max()
maxfall = avg.max()
# 动态元数据：逐帧滑动窗口峰值（窗宽 6 帧）
win = 6
dyn = np.array([peak[max(0, i - win + 1):i + 1].max() for i in range(N)])

fig, ax = plt.subplots(figsize=(9.0, 4.5))
fig.subplots_adjust(left=0.085, right=0.975, bottom=0.285, top=0.95)

ax.semilogy(f, peak, color=H.RED, lw=1.1, alpha=0.55, label="每帧最亮像素")
ax.semilogy(f, avg, color=H.GRAY, lw=1.1, alpha=0.6, label="每帧平均亮度")
ax.axhline(maxcll, color=H.RED, lw=1.6, ls=(0, (5, 3)),
           label=f"MaxCLL = {maxcll:.0f}")
ax.axhline(maxfall, color=H.GRAY, lw=1.4, ls=(0, (5, 3)),
           label=f"MaxFALL = {maxfall:.0f}")
ax.step(f, dyn, where="post", color=H.NAVY, lw=2.0,
        label="动态元数据（逐帧）")

ax.set_xlim(0, N)
ax.set_ylim(8, 2.2e4)
ax.set_xlabel("帧序号（24 fps）")
ax.set_ylabel("亮度（cd/m$^2$，对数）")
ax.set_xticks([0, 24, 48, 72, 96, 120, 143])
ax.set_yticks([10, 100, 1000, 4000, 10000])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
ax.yaxis.set_minor_formatter(NullFormatter())
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), fontsize=8.4,
          ncol=3, handlelength=1.8, columnspacing=1.4, frameon=False)

for x0, x1, lab in [(0, 48, "内景"), (48, 96, "窗边逆光"), (96, 144, "夜景")]:
    ax.text((x0 + x1) / 2, 1.35e4, lab, ha="center", va="center",
            fontsize=8.6, color=H.GRAY)
    if x0:
        ax.axvline(x0, color=H.LGRAY, lw=0.9, zorder=0)

ax.annotate("三帧镜面闪光决定整片的 MaxCLL", xy=(65, 4000), xytext=(72, 9000),
            fontsize=8.4, color=H.DARK, ha="left",
            arrowprops=dict(arrowstyle="->", color=H.DARK, lw=0.9,
                            shrinkA=2, shrinkB=2))
ax.annotate("", xy=(126, maxcll), xytext=(126, dyn[-1]),
            arrowprops=dict(arrowstyle="<->", color=H.RED, lw=1.0))
ax.text(119, 1300, "静态映射多压的\n四个数量级", fontsize=8.0, color=H.RED,
        ha="right", va="center")

H.save(fig, 3, "f2_static_vs_dynamic")
