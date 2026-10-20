# -*- coding: utf-8 -*-
"""第 18 章 图 3：游戏 HDR 三条路线（原生 / Auto HDR / RTX HDR）。"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig = plt.figure(figsize=(7.2, 6.4))
gs = fig.add_gridspec(2, 1, height_ratios=[3.05, 1.75], hspace=0.30)
ax = fig.add_subplot(gs[0])
axb = fig.add_subplot(gs[1])

ax.set_xlim(0, 100); ax.set_ylim(0, 100)
ax.axis("off"); ax.grid(False)


def rbox(a, x, y, w, h, fc, ec=None, lw=1.4, z=2):
    a.add_patch(FancyBboxPatch((x, y), w, h,
                               boxstyle="round,pad=0.3,rounding_size=1.4",
                               linewidth=lw, edgecolor=ec if ec else fc,
                               facecolor=fc, zorder=z))


def arrow(a, x1, y1, x2, y2, color=H.GRAY, lw=1.9, ms=9):
    a.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                mutation_scale=ms, linewidth=lw, color=color, zorder=3))


lanes = [
    (74, "原生 HDR", "开发者设计 · 效果最好", H.ORANGE,
     [("引擎内部 HDR 光照", "线性、高动态范围计算"),
      ("开发者调色 + 定标", "峰值 / 纸白 / 高光冲击力"),
      ("PQ 编码输出（10bit）", "HDR 信号直接送显示器")]),
    (41, "Auto HDR", "Windows 算法 · 覆盖面广", H.BLUE,
     [("SDR 游戏画面", "已被 tonemap、8bit 起步"),
      ("Windows 算法推断", "猜亮度差别、自动拉开"),
      ("重编码为 PQ 输出", "效果随机：过曝或偏色")]),
    (8, "RTX HDR", "驱动级 + AI · 可调参数多", H.GREEN,
     [("SDR 游戏画面", "以没有原生 HDR 的游戏为主"),
      ("驱动级转换 + AI 增强", "参数可调、覆盖面广"),
      ("PQ 输出", "需新显卡，有性能开销")]),
]

xs = [15.5, 44.5, 73.5]
w = 26.0
for base, name, tag, c, stages in lanes:
    yb, hb = base + 3.0, 16.0
    # 路线标签
    rbox(ax, 0.5, yb, 13.5, hb, c, z=2)
    ax.text(7.25, yb + hb * 0.66, name, ha="center", va="center", fontsize=9.6,
            fontweight="bold", color="white", zorder=3)
    ax.text(7.25, yb + hb * 0.26, tag.replace(" · ", "\n"), ha="center", va="center",
            fontsize=6.3, color="white", zorder=3, linespacing=1.4)
    # 三个环节
    for i, (t1, t2) in enumerate(stages):
        x = xs[i]
        light = i == 0
        rbox(ax, x, yb, w, hb, "white" if light else c, ec=c, lw=1.5, z=2)
        ax.text(x + w / 2, yb + hb * 0.66, t1, ha="center", va="center", fontsize=7.8,
                fontweight="bold", color=c if light else "white", zorder=3)
        ax.text(x + w / 2, yb + hb * 0.28, t2, ha="center", va="center", fontsize=6.3,
                color="#3a3a3a" if light else "white", zorder=3)
    ym = yb + hb / 2
    arrow(ax, xs[0] + w, ym, xs[1], ym, color=H.GRAY, lw=1.9, ms=9)
    arrow(ax, xs[1] + w, ym, xs[2], ym, color=c, lw=1.9, ms=9)

# 三条线的共同点 / 差异注释（放在最上方）
ax.text(50, 98.5, "共同点：源端都做过 HDR 处理；差异在“谁决定的亮度”——开发者、系统算法，还是驱动 + AI",
        ha="center", va="center", fontsize=7.4, color=H.DARK, fontweight="bold")

ax.set_title("游戏 HDR 三条路线：渲染 → 输出 → 送显", fontsize=12.2,
             fontweight="bold", color=H.DARK, pad=20)

# ---------------- 下半：四个维度评分 ----------------
metrics = ["画质 / 准确性", "老游戏覆盖", "可调参数", "性能效率\n（高 = 开销小）"]
data = {
    "原生 HDR": ([5.0, 2.0, 4.0, 5.0], H.ORANGE),
    "Auto HDR": ([3.0, 5.0, 1.5, 3.5], H.BLUE),
    "RTX HDR":  ([3.5, 4.5, 4.0, 2.5], H.GREEN),
}
n = len(metrics)
x = np.arange(n)
bw = 0.26
for k, (name, (vals, c)) in enumerate(data.items()):
    off = (k - 1) * bw
    b = axb.bar(x + off, vals, bw, label=name, color=c, zorder=3)
    for rect, v in zip(b, vals):
        axb.text(rect.get_x() + rect.get_width() / 2, v + 0.09, f"{v:g}",
                 ha="center", va="bottom", fontsize=6.6, color="#444")
axb.set_xticks(x)
axb.set_xticklabels(metrics, fontsize=8.6, color="#333")
axb.set_ylim(0, 6.2)
axb.set_yticks([0, 1, 2, 3, 4, 5])
axb.set_ylabel("评分（5 = 最好）", fontsize=9)
axb.grid(axis="x", visible=False)
axb.legend(fontsize=8.4, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.02))
axb.set_title("四个维度对比：算法补的 HDR 覆盖面大，画质上限不如原生",
              fontsize=9.6, fontweight="bold", color=H.DARK, pad=22)

axb.text(0.005, -0.30,
         "游戏内校准三项：最大亮度（纸白）· 黑位 / 黑场 · 峰值亮度 —— 调到“图案刚好不糊、细节刚好可见”为止。\n"
         "提醒：Auto HDR / RTX HDR 属于算法补出来的 HDR，与原生 HDR 是两码事；原生也要靠游戏内校准才好看。",
         transform=axb.transAxes, ha="left", va="top", fontsize=7.2, color="#555",
         linespacing=1.6)

H.save(fig, 18, "f3_game_hdr")
