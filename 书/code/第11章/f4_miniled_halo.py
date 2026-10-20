# -*- coding: utf-8 -*-
"""第 11 章 · 图 11-4：Mini-LED 的分区与光晕（泛光 blooming）。

关键事实：一个分区只有一个亮度。亮点所在的分区必须为亮点开满背光，
于是同一分区里的"暗处"也被一起照亮 —— 这就是光晕。
下排给出不同分区数下的亮度剖面：分区越少，光晕越宽。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import numpy as np
import hdrfig as H
from scipy.ndimage import gaussian_filter
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker

PEAK = 1000.0            # Mini-LED 峰值亮度 nit
LEAK = 1.0 / 3000.0      # 面板泄露率（≈3000:1 原生对比度）
BL_FLOOR = 0.02          # 背光最低档位（暗区）→ 远处黑位 = PEAK*LEAK*BL_FLOOR
LIFT, LO, HI = 0.60, 0.001, 1200.0

# ---------------- 画面：一个亮点 + 一根细亮条，其余全黑 ----------------
W, Hh = 384, 216
yy, xx = np.mgrid[0:Hh, 0:W].astype(float)
scene = np.zeros((Hh, W))
scene[((xx - 150) ** 2 + (yy - 108) ** 2) <= 6 ** 2] = 1.0        # 亮"点"
scene[(np.abs(yy - 108) <= 1.2) & (xx >= 282) & (xx <= 294)] = 1.0  # 细亮条
scene[((xx - 340) ** 2 + (yy - 55) ** 2) <= 3.0 ** 2] = 0.85      # 小亮点
scene = np.clip(scene, 0, 1)

def zone_backlight(scene, nx, blur=2.0):
    """把画面按 nx 个横向分区切块，每块取最大亮度，再升采样回全分辨率。"""
    ny = max(1, int(round(nx * scene.shape[0] / scene.shape[1])))
    zsx, zsy = W // nx, Hh // ny
    bl = scene[:ny * zsy, :nx * zsx].reshape(ny, zsy, nx, zsx).max(axis=(1, 3))
    bl = np.maximum(bl, BL_FLOOR)
    up = np.kron(bl, np.ones((zsy, zsx)))
    up = np.pad(up, ((0, max(0, Hh - up.shape[0])), (0, max(0, W - up.shape[1]))),
                mode="edge")[:Hh, :W]
    return bl, gaussian_filter(up, blur)

def logdisp(nit, lo=LO, hi=HI, lift=LIFT):
    n = np.clip(np.asarray(nit, float), lo, hi)
    v = (np.log10(n) - np.log10(lo)) / (np.log10(hi) - np.log10(lo))
    return v ** lift

# 展示用的分区：10×6（≈60 个分区，示意）
bl_demo, bl_up_demo = zone_backlight(scene, 10, blur=2.0)
disp_demo = (LEAK + (1 - LEAK) * scene) * bl_up_demo * PEAK
halo = PEAK * LEAK * 1.0                 # 亮区所在分区内的暗处亮度（光晕）
blk_far = PEAK * LEAK * BL_FLOOR         # 远处暗区的黑位
NZ_DEMO = bl_demo.size

# ---------------- 画布 ----------------
fig = H.plt.figure(figsize=(7.2, 5.8))
gs = gridspec.GridSpec(2, 3, height_ratios=[1.0, 1.5], hspace=0.60, wspace=0.14,
                       left=0.045, right=0.985, top=0.865, bottom=0.10)
ax0, ax1, ax2 = [fig.add_subplot(gs[0, i]) for i in range(3)]
axp = fig.add_subplot(gs[1, :])

def imshow(ax, img, cmap="gray", title="", sub=""):
    ax.imshow(img, cmap=cmap, vmin=0, vmax=1, interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for s in ax.spines.values():
        s.set_edgecolor("#4a5666"); s.set_linewidth(1.0)
    ax.set_title(title, fontsize=9.3, pad=4)
    if sub:
        ax.text(0.5, 0.028, sub, transform=ax.transAxes, fontsize=7.3,
                color="#f2f2f2", ha="center", va="bottom", zorder=6,
                bbox=dict(boxstyle="round,pad=0.24", facecolor="#1b2b3d",
                          edgecolor="none", alpha=0.86))

imshow(ax0, logdisp(np.maximum(scene * PEAK, 0.0008)),
       title="① 画面内容（亮点 + 全黑背景）", sub="理想：亮就是亮，黑就是黑")
zsx, zsy = W // 10, Hh // 6
for i in range(1, 10):
    ax0.axvline(i * zsx - 0.5, color="#ffb454", lw=0.6, alpha=0.85)
for j in range(1, 6):
    ax0.axhline(j * zsy - 0.5, color="#ffb454", lw=0.6, alpha=0.85)
ax0.text(0.03, 0.95, "橙色网格 = 背光分区（10×6）", transform=ax0.transAxes,
         fontsize=6.8, color="#ffe0b0", ha="left", va="top", zorder=6,
         bbox=dict(boxstyle="round,pad=0.22", facecolor="#1b2b3d", edgecolor="none",
                   alpha=0.86))

imshow(ax1, bl_demo, cmap="inferno", title="② 分区背光的实际亮度分布",
       sub="一个分区只有一个值：亮区必须开满")
ax1.annotate("含亮点的分区只能取一个亮度\n→ 整块都开满（含其中的暗处）",
             xy=(150, 108), xytext=(206, 190), fontsize=6.9, color="#ffd9a0",
             ha="left", va="center",
             arrowprops=dict(arrowstyle="-|>", color="#ffd9a0", lw=0.9,
                             mutation_scale=7), zorder=7)

imshow(ax2, logdisp(disp_demo), title="③ 实际显示：亮区把暗区「抬亮」＝光晕",
       sub="光晕 %.2f nit" % halo)
ax2.annotate("光晕 / 泛光（blooming）", xy=(126, 108), xytext=(176, 26),
             fontsize=7.0, color="#ffd9a0", ha="left", va="center",
             arrowprops=dict(arrowstyle="-|>", color="#ffd9a0", lw=0.9,
                             mutation_scale=7), zorder=7)

# ---------------- 亮度剖面：不同分区数 ----------------
row = 108
xs = np.arange(W)
axp.semilogy(xs, np.maximum(scene[row] * PEAK, 0.0008), color=H.GRAY, lw=1.5,
             ls="--", label="理想（像素级控光）")
for nx, col, lab in ((42, "#f39c12", "≈1024 分区"), (21, H.TEAL, "≈256 分区"),
                     (10, H.PURPLE, "≈64 分区")):
    _, up = zone_backlight(scene, nx, blur=2.0)
    d = (LEAK + (1 - LEAK) * scene) * up * PEAK
    axp.semilogy(xs, d[row], color=col, lw=1.9,
                 label="%s（分区宽 %d px）" % (lab, W // nx))
axp.set_ylim(0.0005, 20000); axp.set_xlim(0, W - 1)
axp.set_xlabel("水平像素位置（穿过亮点的切线）")
axp.set_ylabel("显示亮度（nit，对数轴）")
axp.set_title("分区越少，光晕越宽（Mini-LED）：亮点周围被背光「糊」出一片灰雾",
              fontsize=10.2, pad=8)
axp.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda v, p: ("%g" % v) if v >= 0.001 else ("%.4f" % v)))
axp.legend(loc="upper left", fontsize=7.6, handlelength=1.7, labelspacing=0.35)
axp.axhline(halo, color=H.RED, lw=0.9, ls=":")
axp.axhline(blk_far, color=H.GRAY, lw=0.9, ls=":")
axp.text(205, halo * 2.8, "光晕台阶 %.2f nit（亮区所在分区的暗处）" % halo,
         fontsize=7.4, color=H.RED, ha="left", va="bottom",
         bbox=dict(boxstyle="round,pad=0.18", fc="white", ec=H.RED, lw=0.6, alpha=0.95))
axp.text(205, blk_far * 0.45, "远处暗区黑位 %.4f nit" % blk_far, fontsize=7.4,
         color="#4a5666", ha="left", va="center",
         bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#9fb0c2", lw=0.6, alpha=0.95))
axp.annotate("光晕把暗区的亮度抬高约 %.0f 倍（%.4f → %.2f nit）" % (halo / blk_far, blk_far, halo),
             xy=(200, halo * 0.85), xytext=(24, 0.0011), fontsize=7.6, color="#8a4b0f",
             arrowprops=dict(arrowstyle="-|>", color="#8a4b0f", lw=0.9,
                             mutation_scale=8),
             bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#8a4b0f", lw=0.6, alpha=0.95))
axp.text(0.985, 0.975,
         "4K 屏：1024 分区 ≈ 每分区 90×90 像素，光晕可从亮区外扩约 45 像素",
         transform=axp.transAxes, ha="right", va="top", fontsize=8.0,
         color="#243b55",
         bbox=dict(boxstyle="round,pad=0.34", facecolor="#f3f6fa",
                   edgecolor="#c3ceda", linewidth=0.9))

fig.suptitle("Mini-LED 的分区与光晕：一个分区只有一个亮度", fontsize=12.5,
             fontweight="bold", y=0.963)
H.save(fig, 11, "f4_miniled_halo")