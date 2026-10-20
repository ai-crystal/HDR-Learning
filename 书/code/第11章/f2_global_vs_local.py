# -*- coding: utf-8 -*-
"""第 11 章 · 图 11-2：全局调光 vs 分区调光（FALD）——同一画面、同一个背光模组。

同一个"亮太阳 + 暗星空"的画面：
  全局调光：整块背光一起给 → 暗区被整体照亮，黑位抬到 0.43 nit，画面发灰；
  分区调光：只有亮区所在分区的背光给足 → 远处暗区只有 0.03 nit，但亮区所在
            分区内的暗处被一起照亮，渗出"光晕"。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import numpy as np
import hdrfig as H
from scipy.ndimage import gaussian_filter
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker

PEAK = 600.0                 # 屏幕峰值亮度 nit
LEAK = 1.0 / 830.0           # 面板泄露率（原生对比度 ≈830:1）
BL_GLOBAL = 0.60             # 全局调光时背光的统一档位
BL_FLOOR = 0.04              # 分区调光时背光的最低档位
NZ_X, NZ_Y = 16, 9           # 分区数：16×9 = 144

# ---------------- 场景 ----------------
W, Hh = 320, 180
yy, xx = np.mgrid[0:Hh, 0:W].astype(float)
scene = np.zeros((Hh, W))
scene[((xx - 72) ** 2 + (yy - 62) ** 2) <= 21 ** 2] = 1.00      # 明亮的"太阳"
scene[((xx - 252) ** 2 + (yy - 34) ** 2) <= 6 ** 2] = 0.45      # 远处亮星
rng = np.random.default_rng(11)
for _ in range(24):
    cx, cy = rng.uniform(0, W), rng.uniform(0, Hh * 0.8)
    scene += 0.07 * np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * 1.3 ** 2)))
scene[yy > Hh - 24] += 0.035                                    # 微亮的"地面"
scene = np.clip(scene, 0, 1)

# 分区背光：每个分区取区块内最大亮度（这就是"分区只能取一个值"的物理限制）
zsx, zsy = W // NZ_X, Hh // NZ_Y
bl = scene[:NZ_Y * zsy, :NZ_X * zsx].reshape(NZ_Y, zsy, NZ_X, zsx).max(axis=(1, 3))
bl = np.maximum(bl, BL_FLOOR)
bl_map = gaussian_filter(np.kron(bl, np.ones((zsy, zsx)))[:Hh, :W], 2.0)

# 实际显示亮度（nit）
disp_g = (LEAK + (1 - LEAK) * scene) * BL_GLOBAL * PEAK
disp_l = (LEAK + (1 - LEAK) * scene) * bl_map * PEAK

blk_g = PEAK * LEAK * BL_GLOBAL          # 全局调光的黑位
blk_l = PEAK * LEAK * BL_FLOOR           # 分区调光在"远处暗区"的黑位
halo = PEAK * LEAK                       # 亮区所在分区内的暗处（光晕）亮度

def logdisp(nit, lo=0.01, hi=1000.0, lift=0.62):
    """对数显示映射（0.01–1000 nit），再做暗部抬升，便于肉眼看出黑位差异。"""
    n = np.clip(np.asarray(nit, float), lo, hi)
    v = (np.log10(n) - np.log10(lo)) / (np.log10(hi) - np.log10(lo))
    return v ** lift

# ---------------- 画布 ----------------
fig = H.plt.figure(figsize=(7.2, 5.9))
gs = gridspec.GridSpec(2, 3, height_ratios=[1.0, 1.45], hspace=0.68, wspace=0.14,
                       left=0.045, right=0.985, top=0.875, bottom=0.10)
ax0, ax1, ax2 = [fig.add_subplot(gs[0, i]) for i in range(3)]
axp = fig.add_subplot(gs[1, :])

def show(ax, img, title, sub=""):
    ax.imshow(img, cmap="gray", vmin=0, vmax=1, interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for s in ax.spines.values():
        s.set_edgecolor("#4a5666"); s.set_linewidth(1.0)
    ax.set_title(title, fontsize=9.3, pad=4)
    if sub:
        ax.text(0.5, 0.028, sub, transform=ax.transAxes, fontsize=7.4,
                color="#f2f2f2", ha="center", va="bottom", zorder=6,
                bbox=dict(boxstyle="round,pad=0.24", facecolor="#1b2b3d",
                          edgecolor="none", alpha=0.85))

show(ax0, logdisp(scene * PEAK), "① 画面内容（理想显示）",
     "真黑 0 nit，高光锐利（600 nit）")
ax0.text(0.035, 0.965, "对数显示\n0.01–1000 nit", transform=ax0.transAxes,
         fontsize=6.8, color="#f2f2f2", ha="left", va="top", zorder=6,
         bbox=dict(boxstyle="round,pad=0.22", facecolor="#1b2b3d",
                   edgecolor="none", alpha=0.85))

show(ax1, logdisp(disp_g), "② 全局调光：整块一起亮暗",
     "背光 60%%　黑位 %.2f nit" % (blk_g,))
show(ax2, logdisp(disp_l), "③ 分区调光：144 分区各自调",
     "背光 4–100%%　黑位 %.3f nit" % (blk_l,))
for i in range(1, NZ_X):
    ax2.axvline(i * zsx - 0.5, color="#ffb454", lw=0.55, alpha=0.7)
for j in range(1, NZ_Y):
    ax2.axhline(j * zsy - 0.5, color="#ffb454", lw=0.55, alpha=0.7)
ax2.annotate("太阳所在的分区背光必须开满\n→ 同分区内的暗处被一起照亮",
             xy=(79, 62), xytext=(92, 30), fontsize=6.8, color="#ffe0b0",
             ha="left", va="center",
             arrowprops=dict(arrowstyle="-|>", color="#ffe0b0", lw=0.9,
                             mutation_scale=7), zorder=7)

# ---------------- 亮度剖面 ----------------
row = 62
xs = np.arange(W)
axp.semilogy(xs, np.maximum(scene[row] * PEAK, 0.012), color=H.GRAY, lw=1.5,
             ls="--", label="画面内容（理想：真黑）")
axp.semilogy(xs, disp_g[row], color=H.NAVY, lw=2.0, label="全局调光后的实际显示")
axp.semilogy(xs, disp_l[row], color=H.ORANGE, lw=2.0, label="分区调光后的实际显示")
axp.set_ylim(0.004, 3000); axp.set_xlim(0, W - 1)
axp.set_xlabel("水平像素位置（穿过亮区的切线）")
axp.set_ylabel("显示亮度（nit，对数轴）")
axp.set_title("同一行像素的亮度剖面：分区调光把远处暗区压得更黑，峰值也更高",
              fontsize=10.0, pad=24)
axp.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda v, p: ("%g" % v) if v >= 0.01 else ("%.3f" % v)))
axp.legend(loc="lower center", bbox_to_anchor=(0.5, 1.005), ncol=3,
           fontsize=8.0, handlelength=1.7, columnspacing=1.2)

axp.axhline(blk_g, color=H.NAVY, lw=1.0, ls=":")
axp.axhline(blk_l, color=H.ORANGE, lw=1.0, ls=":")
for yv, xa, txt, col, ty in ((blk_g, 205, "全局调光黑位 %.2f nit（整屏发灰）" % blk_g, H.NAVY, None),
                             (blk_l, 228, "分区调光远处黑位 %.3f nit（更黑）" % blk_l, H.ORANGE, 0.085)):
    axp.plot([xa, xa], [yv, yv * 8.0], ls=":", color=col, lw=0.9)
    axp.text(xa + 3, ty if ty else yv * 9.6, txt, fontsize=7.4, color=col,
             ha="left", va="bottom")
axp.annotate("光晕：亮区所在分区里的暗处被抬到 %.2f nit" % halo, xy=(70, halo),
             xytext=(96, 60), fontsize=7.4, color="#9a5b12",
             arrowprops=dict(arrowstyle="-|>", color="#9a5b12", lw=0.9,
                             mutation_scale=7),
             bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#9a5b12", lw=0.6, alpha=0.95))
axp.text(0.985, 0.975,
         "同时对比度：全局 %.0f:1　→　分区 %.0f:1" % (PEAK * BL_GLOBAL / blk_g, PEAK / blk_l),
         transform=axp.transAxes, ha="right", va="top", fontsize=8.2,
         color="#243b55",
         bbox=dict(boxstyle="round,pad=0.36", facecolor="#f3f6fa",
                   edgecolor="#c3ceda", linewidth=0.9))

fig.suptitle("全局调光 vs 分区调光：同一画面、同一个背光模组", fontsize=12.5,
             fontweight="bold", y=0.968)
H.save(fig, 11, "f2_global_vs_local")
