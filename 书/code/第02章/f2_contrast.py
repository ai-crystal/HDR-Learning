# -*- coding: utf-8 -*-
"""图 02-2 对比度 = 峰值 ÷ 黑位

用「峰值条 + 黑位条」两个亮度水平 + 比值标注，
说明同一台显示器在不同「口径」下能算出天差地别的对比度。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
from matplotlib.patches import Patch

plt = H.plt
YBOT = 1e-5

# (名称, 副题, 峰值 nit, 黑位 nit, 颜色, 备注)
cases = [
    ("LCD 原生", "（同一帧黑白块）", 400.0, 0.4, H.NAVY, "同一画面同时测量，可信"),
    ("OLED 原生", "（同一帧黑白块）", 800.0, 0.0005, H.TEAL, "黑位极低，可标称无限"),
    ("动态对比度", "（两帧之间调背光）", 1000.0, 0.001, H.RED, "两帧不可同时，营销数字"),
]

fig, ax = plt.subplots(figsize=(7.2, 4.9))
x = np.arange(len(cases))
w = 0.30

for i, (name, sub, peak, black, c, note) in enumerate(cases):
    ax.bar(x[i] - w * 0.60, peak - YBOT, bottom=YBOT, width=w,
           color=c, edgecolor="white", linewidth=1.2, zorder=3)
    ax.bar(x[i] + w * 0.60, black - YBOT, bottom=YBOT, width=w,
           color=c, alpha=0.40, edgecolor=c, linewidth=1.5,
           hatch="//", zorder=3)
    ratio = peak / black
    stops = np.log2(ratio)
    ax.text(x[i] - w * 0.60, peak * 1.45, f"峰值 {peak:g}", ha="center",
            va="bottom", fontsize=8.8, color=c, fontweight="bold")
    ax.text(x[i] + w * 0.60, black * 1.45, f"黑位 {black:g}", ha="center",
            va="bottom", fontsize=8.8, color=c)
    ax.text(x[i], 2.5e5,
            f"{ratio:,.0f}:1".replace(",", " ") + f"\n≈ {stops:.1f} 档",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color=c, zorder=6, linespacing=1.3)
    ax.text(x[i], 1.1e4, note, ha="center", va="center", fontsize=8.2,
            color=H.GRAY, zorder=6)

ax.set_yscale("log")
ax.set_ylim(YBOT, 1e7)
ax.set_xlim(-0.62, len(cases) - 0.38)
ax.set_xticks(x)
ax.set_xticklabels([f"{c[0]}\n{c[1]}" for c in cases], fontsize=9)
ax.set_ylabel("亮度（nit，对数轴）")
ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1000, 1e4])
ax.set_yticklabels([r"$10^{-4}$", r"$10^{-3}$", r"$10^{-2}$", r"$10^{-1}$",
                    "1", "10", "100", "1000", r"$10^{4}$"])
ax.xaxis.grid(False)

leg = [Patch(facecolor=H.GRAY, edgecolor="white", label="峰值亮度（最亮）"),
       Patch(facecolor=H.GRAY, alpha=0.40, hatch="//", edgecolor=H.GRAY,
             label="黑位亮度（最暗）")]
ax.legend(handles=leg, loc="upper center", bbox_to_anchor=(0.5, -0.13),
          ncol=2, fontsize=9)

ax.set_title("对比度 = 峰值 ÷ 黑位：口径不同，数字能差出上千倍")
fig.subplots_adjust(left=0.10, right=0.97, top=0.92, bottom=0.31)
fig.text(0.5, 0.025,
         "关键：只有「同一帧画面里」同时出现的峰值与黑位才算数——"
         "动态对比度靠两帧之间自动调背光，几乎只是营销数字。",
         ha="center", va="bottom", fontsize=8.8, color=H.DARK)
H.save(fig, 2, "f2_contrast")
