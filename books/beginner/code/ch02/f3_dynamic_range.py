# -*- coding: utf-8 -*-
"""图 02-3 SDR 与 HDR 的动态范围（档 / stop）

用横向亮度条对比 SDR、HDR、人眼瞬时与人眼总范围，
在每条上标注「同时可呈现」的最亮 / 最暗与折合的档数。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np
from matplotlib.transforms import blended_transform_factory as btf

plt = H.plt

# (名称, 最暗 nit, 最亮 nit, 颜色, 备注)
bands = [
    ("SDR（BT.709 / 2.2–2.4）",       0.1,    100.0,  H.NAVY,   "上限锁死在 100 nit"),
    ("HDR10（主流）",                  0.005,  1000.0, H.ORANGE, "同时提亮 + 压黑"),
    ("HDR 旗舰（DV / 高亮电视）",      0.0005, 4000.0, H.RED,    "上限更高、黑位更低"),
    ("人眼：同一瞬间（同时对比）",     0.1,    1000.0, H.TEAL,   r"约 $10^{4}$:1"),
    ("人眼：总可感知范围",             0.001,  1e6,    H.PURPLE, "跨约 30 档"),
]

fig, ax = plt.subplots(figsize=(7.2, 4.5))
n = len(bands)
ys = np.arange(n)[::-1]
trans = btf(fig.transFigure, ax.transData)   # x 用图坐标，y 用数据坐标

for i, (name, lo, hi, c, note) in enumerate(bands):
    y = ys[i]
    ax.barh(y, hi - lo, left=lo, height=0.50, color=c, alpha=0.88,
            edgecolor="white", linewidth=1.1, zorder=3)
    stops = np.log2(hi / lo)
    ratio = hi / lo
    # 档数（条内居中）
    ax.text(np.sqrt(lo * hi), y, f"{stops:.1f} 档", ha="center", va="center",
            fontsize=10.5, fontweight="bold", color="white", zorder=5)
    # 两端数值
    ax.text(lo * 0.82, y, f"{lo:g}", ha="right", va="center", fontsize=8.6,
            color=c, fontweight="bold")
    ax.text(hi * 1.35, y, f"{hi:,.0f} nit".replace(",", " "), ha="left",
            va="center", fontsize=8.6, color=c, fontweight="bold")
    # 右侧标签栏（两行）
    ax.text(0.625, y + 0.23, name, transform=trans, ha="left", va="bottom",
            fontsize=9.6, color=c, fontweight="bold")
    ax.text(0.625, y - 0.23,
            f"最暗 {lo:g} → 最亮 {hi:,.0f} nit".replace(",", " ")
            + "　·　比值 ≈ "
            + f"{ratio:,.0f}:1".replace(",", " ")
            + f"　·　{note}",
            transform=trans, ha="left", va="top", fontsize=7.8, color=H.GRAY)

ax.set_xscale("log")
ax.set_xlim(1e-5, 2e6)
ax.set_ylim(-0.75, n - 0.30)
ax.set_yticks([])
ax.set_xlabel("亮度（nit，对数轴）", fontsize=10.5)
ax.set_xticks([1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1e3, 1e4, 1e5, 1e6])
ax.set_xticklabels([r"$10^{-4}$", r"$10^{-3}$", r"$10^{-2}$", r"$10^{-1}$",
                    "1", "10", "100", "1k", "10k", "100k", "1M"])
ax.yaxis.grid(False)
ax.set_title("动态范围（同时可呈现的亮度跨度）：SDR 约 10 档，HDR 十几到二十几档",
             fontsize=12)

fig.subplots_adjust(left=0.07, right=0.60, top=0.90, bottom=0.17)
fig.text(0.5, 0.02,
         r"档数 = $\log_2$(最亮 ÷ 最暗)。SDR 把一切都压在 100 nit 附近，"
         "HDR 则同时抬高上限、压低下限——这正是它表达「这里真的很亮 / 真的很黑」的能力来源。",
         ha="center", va="bottom", fontsize=8.5, color=H.DARK)
H.save(fig, 2, "f3_dynamic_range")
