# -*- coding: utf-8 -*-
"""第 11 章 · 图 11-3：侧入式（Edge-lit）vs 直下式（Direct-lit / FALD）背光。

上排：两种背光的结构剖面（灯珠在哪里、光怎么走、机身多厚）；
下排：两种方案能做出的"分区形态"——条状 vs 二维网格。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import numpy as np
import hdrfig as H
import matplotlib.patches as mpatch
import matplotlib.gridspec as gridspec

fig = H.plt.figure(figsize=(7.2, 5.3))
gs = gridspec.GridSpec(2, 2, height_ratios=[1.75, 1.0], hspace=0.36, wspace=0.10,
                       left=0.02, right=0.98, top=0.855, bottom=0.045)
axL, axR = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
axl, axr = fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])

for ax in (axL, axR):
    ax.set_xlim(0, 11.2); ax.set_ylim(-0.15, 7.65)
    ax.axis("off"); ax.grid(False)

def box(ax, x0, y0, x1, y1, fc, ec="#4a5666", ls="-", lw=0.9, z=2, alpha=1.0):
    ax.add_patch(mpatch.Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=fc,
                                  edgecolor=ec, linestyle=ls, linewidth=lw,
                                  zorder=z, alpha=alpha))

# =============== 左：侧入式 ===============
axL.set_title("侧入式（Edge-lit）：灯在边上，光靠导光板铺开", fontsize=10.2, pad=6)
box(axL, 0.8, 6.05, 9.2, 6.75, "#c6d5e5")
axL.text(5.0, 6.42, "液晶面板（像素只管挡光）", ha="center", va="center",
         fontsize=8, color="#12314f")
box(axL, 0.8, 5.55, 9.2, 6.05, "#e4edf6")
axL.text(5.0, 5.80, "扩散片", ha="center", va="center", fontsize=7.6, color="#41556b")
box(axL, 0.8, 3.05, 9.2, 5.55, "#f6fafe", ec="#8fa6bd", ls=(0, (4, 2.5)))
axL.text(5.0, 5.28, "导光板：光在里面横向铺开", ha="center", va="center",
         fontsize=7.6, color="#41556b")
# 亮度随距离衰减的光线
for i, y in enumerate(np.linspace(3.35, 4.95, 6)):
    for j in range(9):
        x0 = 1.05 + j * 0.92
        a = 0.85 * (1.0 - j / 9.0) ** 1.2
        axL.annotate("", xy=(x0 + 0.6, y), xytext=(x0, y),
                     arrowprops=dict(arrowstyle="-|>", color=H.GOLD, lw=1.1,
                                     alpha=max(a, 0.06), mutation_scale=6), zorder=3)
box(axL, 0.55, 3.20, 0.80, 5.40, "#3c4857", ec="#22303f")
for y in np.linspace(3.38, 5.22, 6):
    axL.add_patch(mpatch.Rectangle((0.57, y - 0.06), 0.21, 0.12,
                                   facecolor=H.GOLD, edgecolor="none", zorder=4))
axL.text(0.68, 5.72, "LED 灯条", ha="center", va="center", fontsize=7.4,
         color="#6b5410", fontweight="bold")
box(axL, 9.20, 3.20, 9.45, 5.40, "#3c4857", ec="#22303f")
for y in np.linspace(3.38, 5.22, 6):
    axL.add_patch(mpatch.Rectangle((9.22, y - 0.06), 0.21, 0.12,
                                   facecolor=H.GOLD, edgecolor="none", zorder=4))
box(axL, 0.8, 2.62, 9.2, 3.05, "#dde5ee")
axL.text(5.0, 2.84, "反射片（把漏下去的光折回来）", ha="center", va="center",
         fontsize=7.4, color="#41556b")
box(axL, 0.35, 2.15, 9.65, 2.62, "#59667a")
axL.text(5.0, 2.38, "背板", ha="center", va="center", fontsize=7.4, color="white")
axL.annotate("", xy=(10.45, 2.15), xytext=(10.45, 6.75),
             arrowprops=dict(arrowstyle="<|-|>", color=H.RED, lw=1.3,
                             mutation_scale=9))
axL.text(10.25, 4.45, "薄\n≈10–15 mm", ha="center", va="center", fontsize=7.4,
         color=H.RED, rotation=90)
axL.annotate("光要「跑」很远，控光必然粗糙\n→ 分区只能做成条状", xy=(4.2, 4.3),
             xytext=(1.9, 0.85), fontsize=7.6, color="#8a4b0f", ha="left",
             arrowprops=dict(arrowstyle="-|>", color="#8a4b0f", lw=0.9,
                             mutation_scale=8))

# =============== 右：直下式 ===============
axR.set_title("直下式（Direct-lit / FALD）：灯珠就在屏幕正后方", fontsize=10.2, pad=6)
box(axR, 0.8, 6.05, 9.2, 6.75, "#c6d5e5")
axR.text(5.0, 6.42, "液晶面板（像素只管挡光）", ha="center", va="center",
         fontsize=8, color="#12314f")
box(axR, 0.8, 5.50, 9.2, 6.05, "#e4edf6")
axR.text(5.0, 5.78, "扩散板（把点光抹匀）", ha="center", va="center",
         fontsize=7.6, color="#41556b")
box(axR, 0.8, 2.60, 9.2, 5.50, "#fbfdff", ec="#8fa6bd", ls=(0, (4, 2.5)))
# 分区网格（每格一个独立驱动）
NZC, NZR = 6, 4
for i in range(1, NZC):
    axR.plot([0.8 + i * 8.4 / NZC] * 2, [2.60, 5.50], color=H.ORANGE, lw=0.7,
             alpha=0.55, zorder=3)
for j in range(1, NZR):
    axR.plot([0.8, 9.2], [2.60 + j * 2.90 / NZR] * 2, color=H.ORANGE, lw=0.7,
             alpha=0.55, zorder=3)
axR.text(5.0, 5.25, "每个格子 = 一个可独立调亮度的分区", ha="center", va="center",
         fontsize=7.6, color="#8a4b0f")
for i in range(NZC):
    for j in range(2):
        cx = 0.8 + (i + 0.5) * 8.4 / NZC
        cy = 2.85 + j * 1.15
        axR.add_patch(mpatch.Rectangle((cx - 0.20, cy - 0.14), 0.40, 0.28,
                                       facecolor=H.GOLD, edgecolor="#8a6d1f",
                                       linewidth=0.5, zorder=4))
axR.text(0.95, 3.45, "LED 灯珠阵列（一个分区一组）", ha="left", va="center",
         fontsize=7.0, color="#6b5410")
box(axR, 0.35, 1.90, 9.65, 2.42, "#59667a")
axR.text(5.0, 2.15, "背板 / 驱动电路", ha="center", va="center", fontsize=7.4,
         color="white")
axR.annotate("", xy=(10.45, 1.90), xytext=(10.45, 6.75),
             arrowprops=dict(arrowstyle="<|-|>", color=H.RED, lw=1.3,
                             mutation_scale=9))
axR.text(10.25, 4.33, "厚\n≈30–40 mm", ha="center", va="center", fontsize=7.4,
         color=H.RED, rotation=90)
axR.annotate("灯就在每个分区背后\n→ 控光精细、分区可以很多", xy=(6.0, 4.6),
             xytext=(1.9, 0.75), fontsize=7.6, color="#8a4b0f", ha="left",
             arrowprops=dict(arrowstyle="-|>", color="#8a4b0f", lw=0.9,
                             mutation_scale=8))

# =============== 下排：分区形态 ===============
edge_zones = np.array([[0.12, 0.18, 0.32, 0.62, 1.00, 0.85, 0.40, 0.14]])
axl.imshow(np.repeat(edge_zones, 40, axis=0), cmap="YlOrRd", vmin=0, vmax=1,
           aspect="auto")
axl.set_xticks(range(len(edge_zones[0])))
axl.set_xticklabels([str(i + 1) for i in range(len(edge_zones[0]))], fontsize=7)
axl.set_yticks([]); axl.grid(False)
axl.set_xlabel("分区编号（只有横向）", fontsize=8, labelpad=1)
axl.set_title("侧入式的分区：条状，几条 ~ 十几条", fontsize=9.4, pad=4)
for i in range(1, 8):
    axl.axvline(i - 0.5, color="white", lw=1.0)

nz = np.zeros((7, 12))
yy, xx = np.mgrid[0:7, 0:12].astype(float)
nz += 0.92 * np.exp(-(((xx - 4.0) ** 2) / 6.0 + ((yy - 3.0) ** 2) / 3.0))
nz += 0.45 * np.exp(-(((xx - 9.5) ** 2) / 3.0 + ((yy - 1.6) ** 2) / 1.6))
nz = np.clip(nz, 0.06, 1.0)
axr.imshow(nz, cmap="YlOrRd", vmin=0, vmax=1, aspect="auto",
           interpolation="nearest")
axr.set_xticks([]); axr.set_yticks([]); axr.grid(False)
axr.set_title("直下式（FALD）的分区：二维网格，几十 ~ 几千个", fontsize=9.4, pad=4)
for i in range(1, 12):
    axr.axvline(i - 0.5, color="white", lw=0.7, alpha=0.8)
for j in range(1, 7):
    axr.axhline(j - 0.5, color="white", lw=0.7, alpha=0.8)
axr.text(0.02, 0.04, "同一画面下背光的亮度分布示意（越亮 = 该分区背光开得越大）",
         transform=axr.transAxes, fontsize=7.2, color="#3a2a10", ha="left",
         va="bottom",
         bbox=dict(boxstyle="round,pad=0.25", facecolor="#fff6e6",
                   edgecolor="#e0c9a0", linewidth=0.7))

fig.suptitle("侧入式 vs 直下式：灯放在哪里，决定了分区能做多细", fontsize=12.5,
             fontweight="bold", y=0.978)
H.save(fig, 11, "f3_edge_direct")
