# -*- coding: utf-8 -*-
"""第 11 章 · 图 11-5：分区数 vs 像素数——光晕的根本原因。

左：4K/1080p 的像素数与各类背光的分区数（对数条形）；
右：一块 4K 屏上"每个分区要罩住多少像素"，与像素级控光差了多少。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import numpy as np
import hdrfig as H
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker

PX_4K = 3840 * 2160          # 8,294,400
PX_1080 = 1920 * 1080        # 2,073,600

def cnnum(v, _=None):
    """对数轴的友好刻度：1 万以上用「万」。"""
    if v >= 1e8:
        return "%g亿" % (v / 1e8)
    if v >= 1e4:
        return "%g万" % (v / 1e4)
    return "%g" % v

fig = H.plt.figure(figsize=(7.2, 4.4))
gs = gridspec.GridSpec(1, 2, width_ratios=[1.0, 1.05], wspace=0.30,
                       left=0.085, right=0.975, top=0.855, bottom=0.175)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

# ================= 左：对数条形 =================
names = ["4K", "1080p", "Mini-LED", "FALD", "入门", "侧入式"]
vals = [PX_4K, PX_1080, 1024, 288, 64, 16]
cols = [H.NAVY, H.BLUE, H.ORANGE, "#e8a33d", H.GOLD, H.GRAY]
days = ["829 万", "207 万", "1024", "288", "64", "16"]
xs = np.arange(len(vals))
ax1.bar(xs, vals, color=cols, width=0.68, zorder=3)
ax1.set_yscale("log")
ax1.set_ylim(8, 3e8)
ax1.set_xticks(xs)
ax1.set_xticklabels(names, fontsize=7.4)
ax1.set_ylabel("数量（个，对数轴）")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(cnnum))
ax1.yaxis.set_minor_formatter(mticker.NullFormatter())
for x, v, t in zip(xs, vals, days):
    ax1.text(x, v * 1.5, t, ha="center", va="bottom", fontsize=7.6,
             color="#243b55", fontweight="bold", zorder=4)
ax1.axhline(1e6, color=H.RED, lw=0.9, ls="--", zorder=2)
ax1.text(5.42, 1.3e6, "100 万", fontsize=7.0, color=H.RED, ha="right",
         va="bottom")
ax1.set_title("像素数 vs 分区数（4K 屏：3840×2160）", fontsize=10.2, pad=6)
ax1.annotate("", xy=(0.0, 1.5e7), xytext=(2.6, 1.5e7),
             arrowprops=dict(arrowstyle="<|-|>", color=H.PURPLE, lw=1.2,
                             mutation_scale=9), zorder=5)
ax1.text(1.3, 2.1e7, "相差约 8100 倍", ha="center", va="bottom", fontsize=8.2,
         color=H.PURPLE, fontweight="bold", zorder=5)
leg = [H.plt.Rectangle((0, 0), 1, 1, facecolor=H.NAVY),
       H.plt.Rectangle((0, 0), 1, 1, facecolor=H.ORANGE)]
ax1.legend(leg, ["像素：每个都能单独控光", "背光分区：一组像素共用一个值"],
           loc="upper right", fontsize=6.8, bbox_to_anchor=(1.0, 0.60))

# ================= 右：每个分区罩住多少像素 =================
cfg = [("侧入式 16 分区", 16), ("入门 FALD 64 分区", 64), ("FALD 288 分区", 288),
       ("Mini-LED 1024 分区", 1024), ("高端 Mini-LED 4096 分区", 4096)]
ys = np.arange(len(cfg))
ppz = [PX_4K / z for _, z in cfg]
ax2.barh(ys, ppz, color=[H.GRAY, H.GOLD, "#e8a33d", H.ORANGE, "#d35400"],
         height=0.62, zorder=3)
ax2.set_xscale("log")
ax2.set_xlim(1, 2.5e7)
ax2.set_yticks(ys)
ax2.set_yticklabels([n for n, _ in cfg], fontsize=7.6)
ax2.invert_yaxis()
ax2.set_xlabel("每个分区要罩住的像素数（对数轴）")
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(cnnum))
ax2.xaxis.set_minor_formatter(mticker.NullFormatter())
for y, v in zip(ys, ppz):
    k = int(round(np.sqrt(v)))
    ax2.text(v * 1.35, y, "%s 像素/区（%d×%d）" % (format(int(v), ","), k, k),
             va="center", ha="left", fontsize=7.4, color="#243b55", zorder=4)
ax2.axvline(1, color=H.GREEN, lw=1.2, ls="--", zorder=2)
ax2.text(1.12, -0.62, "1 像素 = 1 分区\n（自发光，无光晕）", fontsize=7.0,
         color=H.GREEN, ha="left", va="bottom")
ax2.set_title("一块 4K 屏上，每个分区要罩住多少像素", fontsize=10.2, pad=6)
ax2.annotate("", xy=(1.0, 4.72), xytext=(2025.0, 4.72),
             arrowprops=dict(arrowstyle="<|-|>", color=H.PURPLE, lw=1.2,
                             mutation_scale=9), zorder=5)
ax2.text(45, 4.50, "还差约 2000 倍", ha="center", va="bottom", fontsize=8.0,
         color=H.PURPLE, fontweight="bold", zorder=5)
ax2.set_ylim(4.95, -1.15)

fig.suptitle("分区数 vs 像素数：几百个分区，要覆盖八百多万个像素", fontsize=12.5,
             fontweight="bold", y=0.968)
fig.text(0.5, 0.035,
         "分区数（几十 ~ 几千）比像素数（几百万）小 3~5 个数量级 —— 一个分区只能给一个亮度，这就是光晕（blooming）的根本原因。",
         ha="center", va="center", fontsize=8.4, color="#243b55",
         bbox=dict(boxstyle="round,pad=0.45", facecolor="#f3f6fa",
                   edgecolor="#c3ceda", linewidth=0.9))
H.save(fig, 11, "f5_zones_vs_pixels")
