# -*- coding: utf-8 -*-
"""图 8-5 SDR 界面在 HDR 输出里的白点映射，以及文字边缘的混合方式。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("hdr-tech")
import numpy as np
from matplotlib.ticker import FuncFormatter

plt = H.plt

fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.3))
ax1, ax2 = axes

# ---------- 左：SDR 码值到屏幕亮度的三条白点 ----------
code = np.linspace(0, 1, 600)
lin = H.srgb_eotf(code)
for white, col, ls in [(100, H.GRAY, ":"), (203, H.BLUE, "-"), (300, H.ORANGE, "--")]:
    ax1.semilogy(code * 255, lin * white, color=col, lw=2.0, ls=ls,
                 label=f"白点 {white} nit")

ax1.set_xlim(0, 255)
ax1.set_ylim(0.05, 700)
ax1.set_xlabel("SDR 界面里的码值")
ax1.set_ylabel("屏幕上的绝对亮度（nit）")
ax1.set_title("(a) 同一个界面配不同的白点", fontsize=9.8, pad=8)
ax1.legend(loc="lower right", fontsize=8)
ax1.axhline(203, color="#c9d3de", lw=1.0, ls=":")
ax1.text(4, 230, "203 nit 图卡白", fontsize=7.6, color=H.GRAY)
ax1.yaxis.set_major_formatter(FuncFormatter(
    lambda v, p: f"{v:g}"))

# 灰阶 18% 处标一个点，说明中间调的差别
mid = H.srgb_oetf(0.18) * 255
for white, col in [(100, H.GRAY), (203, H.BLUE), (300, H.ORANGE)]:
    ax1.plot([mid], [0.18 * white], "o", ms=4.5, color=col, zorder=5,
             markeredgecolor="white", markeredgewidth=0.7)
ax1.annotate("18% 灰的三个结果\n18 / 36 / 54 nit", xy=(mid, 54), xytext=(138, 4.2),
             fontsize=7.8, color="#2c3e50",
             arrowprops=dict(arrowstyle="-|>", color="#8d99a6", lw=0.9))

# ---------- 右：文字边缘的覆盖率与实际亮度 ----------
a = np.linspace(0, 1, 400)
lin_mix = a * 1.0                       # 线性光里混合
code_mix = a * 1.0                      # 码值域里混合，白与黑都是 1.0 与 0.0
gam_mix = H.srgb_eotf(code_mix)         # 再解码

ax2.plot(a * 100, lin_mix * 203, color=H.BLUE, lw=2.2, label="在线性光里混合")
ax2.plot(a * 100, gam_mix * 203, color=H.ORANGE, lw=2.2, ls="--",
         label="在 sRGB 码值里混合再解码")
ax2.plot([50], [101.5], "o", ms=5, color=H.BLUE, zorder=5,
         markeredgecolor="white")
ax2.plot([50], [43.4], "o", ms=5, color=H.ORANGE, zorder=5,
         markeredgecolor="white")
ax2.annotate("50% 覆盖\n给 101 nit", xy=(50, 101.5), xytext=(6, 140),
             fontsize=7.8, color=H.BLUE, va="center",
             arrowprops=dict(arrowstyle="-|>", color=H.BLUE, lw=0.9))
ax2.annotate("同样的覆盖率\n只有 43 nit", xy=(50, 43.4), xytext=(57, 8),
             fontsize=7.8, color=H.ORANGE, va="bottom",
             arrowprops=dict(arrowstyle="-|>", color=H.ORANGE, lw=0.9))
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 215)
ax2.set_xlabel("像素被文字覆盖的比例（%）")
ax2.set_ylabel("该像素的亮度（nit，白点取 203）")
ax2.set_title("(b) 边缘混合发生在哪个域", fontsize=9.8, pad=8)
ax2.legend(loc="upper left", fontsize=8)


fig.subplots_adjust(wspace=0.34)
H.save(fig, 8, "f5_ui_mapping")
