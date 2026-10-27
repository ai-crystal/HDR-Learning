# -*- coding: utf-8 -*-
"""图 08-3：MaxCLL 与 MaxFALL —— 逐帧亮度曲线上的两条统计线。

上：逐帧峰值 / 平均亮度 + 两条水平统计线。
下：两种极端画面的示意帧，说明为什么需要两个数字。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import numpy as np
import hdrfig as H
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm

FPS = 24
DUR = 6000.0
N = int(FPS * DUR)

SCENES = [
    (0, 600, "烛光晚餐（暗场）", 150, 10),
    (600, 1800, "夜晚街头（点光源闪烁）", 700, 25),
    (1800, 2700, "室内对话（中亮）", 320, 110),
    (2700, 3300, "正午雪原（大面积亮场）", 2100, 900),
    (3300, 3390, "爆炸高光（一闪而过）", 4000, 380),
    (3390, 4400, "海边日落", 1400, 420),
    (4400, 6000, "夜景收尾（暗场）", 350, 20),
]


def build_content():
    rng = np.random.default_rng(8)
    peak = np.zeros(N); avg = np.zeros(N)
    for s, e, name, pk, av in SCENES:
        i0, i1 = int(s * FPS), int(e * FPS)
        n = i1 - i0
        t = np.linspace(0, 1, n)
        f = 1.0 + 0.6 * np.sin(2.0 * np.pi * 0.7 * t) + 0.25 * np.sin(2.0 * np.pi * 3.1 * t)
        peak[i0:i1] = pk * (0.75 + 0.25 * f) * (1.0 + 0.02 * rng.standard_normal(n))
        avg[i0:i1] = av * (0.85 + 0.15 * f) * (1.0 + 0.02 * rng.standard_normal(n))
        if "点光源" in name:
            blk = (rng.random(n) < 0.004)
            peak[i0:i1] = np.where(blk, peak[i0:i1] * 1.8, peak[i0:i1])
    peak = np.clip(peak, 1.31, 4000)
    avg = np.clip(avg, 1.31, peak * 0.95)
    return peak, avg


peak, avg = build_content()
maxcll, i_cll = float(peak.max()), int(np.argmax(peak))
maxfall, i_fall = float(avg.max()), int(np.argmax(avg))

fig = plt.figure(figsize=(7.2, 5.8))
gs = fig.add_gridspec(2, 2, height_ratios=[1.6, 0.95], hspace=0.52, wspace=0.18)

# ---------------- 上：逐帧曲线 + 两条统计线 ----------------
ax = fig.add_subplot(gs[0, :])
tt = np.arange(N) / FPS / 60.0
ax.fill_between(tt, 1.3, peak, color=H.ORANGE, alpha=0.14, lw=0, zorder=2)
ax.plot(tt, peak, color=H.ORANGE, lw=0.6, zorder=3, label="逐帧峰值亮度（该帧最亮像素）")
ax.plot(tt, avg, color=H.TEAL, lw=0.8, zorder=3, label="逐帧平均亮度（该帧全画面平均）")
ax.axhline(maxcll, color=H.RED, ls="--", lw=1.6, zorder=4,
           label=f"MaxCLL = {maxcll:.0f} nit（峰值曲线的最高点）")
ax.axhline(maxfall, color=H.BLUE, ls="-.", lw=1.6, zorder=4,
           label=f"MaxFALL = {maxfall:.0f} nit（平均曲线的最高点）")

for s, e, name, pk, av in SCENES:
    ax.axvline(s / 60.0, color=H.LGRAY, lw=0.8, zorder=1)
ax.axvline(DUR / 60.0, color=H.LGRAY, lw=0.8, zorder=1)

ax.plot([i_cll / FPS / 60.0], [maxcll], marker="v", ms=6, color=H.RED, zorder=6)
ax.annotate("MaxCLL 来自“最亮的那一帧”\n（极小面积、瞬间 4000 nit 高光）",
            xy=(i_cll / FPS / 60.0, maxcll), xytext=(57.5, 5200),
            fontsize=7.2, color=H.RED, ha="left", va="bottom",
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=H.RED, lw=0.7, alpha=0.95))
ax.plot([i_fall / FPS / 60.0], [maxfall], marker="v", ms=6, color=H.BLUE, zorder=6)
ax.annotate("MaxFALL 来自“平均最亮的那一帧”\n（大面积亮场：雪原）",
            xy=(i_fall / FPS / 60.0, maxfall * 0.95), xytext=(56, 150),
            fontsize=7.2, color=H.BLUE, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=H.BLUE, lw=0.9),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=H.BLUE, lw=0.7, alpha=0.95))

ax.set_yscale("log")
ax.set_ylim(1.3, 40000)
ax.set_xlim(0, DUR / 60.0)
ax.set_xlabel("影片时间（分钟，逐帧 24 fps 采样）")
ax.set_ylabel("亮度（nit，对数轴）")
ax.set_title("MaxCLL / MaxFALL：从逐帧亮度里各取一条“统计线”",
             fontsize=11, color=H.NAVY, pad=8)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"{v:g}"))
ax.yaxis.set_minor_formatter(mticker.NullFormatter())
ax.grid(True, which="both", alpha=0.45)
ax.legend(loc="lower left", fontsize=7.0, ncol=2, handlelength=1.8,
          columnspacing=1.0, labelspacing=0.3)

# ---------------- 下：两种极端画面示意 ----------------
h, w = 180, 320
# A：暗场 + 极小面积高光  → 峰值很高、平均很低
A = np.full((h, w), 4.0)
A[72:80, 208:215] = 4000.0            # 一个小小的高光点
A[120:126, 60:66] = 90.0              # 一盏暗灯
A[100:112, 250:262] = 25.0
A += 0.6 * np.random.default_rng(1).random((h, w))
# B：大面积亮场 → 平均很高
B = np.full((h, w), 760.0)
B[0:62, :] = 1000.0                   # 天空
B[130:180, 30:110] = 120.0            # 一小片暗部（岩石）
B += 12.0 * np.random.default_rng(2).random((h, w))

norm = LogNorm(vmin=1.0, vmax=4500.0)
for k, (img, name, col, cap) in enumerate([
        (A, "① 小面积高光帧", H.RED, "峰值 4000 nit，平均只有 %.0f nit" % A.mean()),
        (B, "② 大面积亮场帧", H.BLUE, "峰值 1000 nit，平均高达 %.0f nit" % B.mean())]):
    axf = fig.add_subplot(gs[1, k])
    im = axf.imshow(img, cmap="gray", norm=norm, interpolation="nearest",
                    aspect="auto")
    axf.set_xticks([]); axf.set_yticks([])
    axf.grid(False)
    for sp in axf.spines.values():
        sp.set_color(col); sp.set_linewidth(1.6)
    axf.set_title(f"{name}　{cap}", fontsize=9.0, color=col, pad=5)
    if k == 0:
        axf.annotate("这一个像素\n4000 nit", xy=(211, 76), xytext=(150, 30),
                     fontsize=6.8, color="white", ha="center",
                     arrowprops=dict(arrowstyle="->", color="white", lw=0.9))
        axf.text(0.02, 0.06, "平均亮度低：屏幕整体负担小", transform=axf.transAxes,
                 fontsize=6.8, color="white")
    else:
        axf.text(0.02, 0.06, "平均亮度高：背光 / ABL 被迫降亮度",
                 transform=axf.transAxes, fontsize=6.8, color="black")
        axf.annotate("这一小片暗部\n被亮场“拖累”", xy=(70, 155), xytext=(150, 30),
                     fontsize=6.8, color="black", ha="center",
                     arrowprops=dict(arrowstyle="->", color="black", lw=0.9))

fig.text(0.5, 0.055,
         "同一个亮度标尺（对数）：MaxCLL 描述“最响的一声尖叫”，MaxFALL 描述“最吵的那一分钟”——"
         "小亮点冲得高，和整屏都亮，是两回事。",
         ha="center", va="center", fontsize=7.4, color=H.DARK)

H.save(fig, 8, "f3_maxcll_maxfall")
