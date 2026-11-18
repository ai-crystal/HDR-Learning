# -*- coding: utf-8 -*-
"""图 1-1：典型场景亮度与人眼 / 显示设备的能力区间（对数横轴）。

数值取公开文献与标准的数量级（CIE 视觉亮度范围、ITU-R BT.2408 参考白、
SMPTE 影院银幕 48 cd/m² 等），只用于比较量级，不作为精确测量值。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import NullFormatter
plt.rcParams["mathtext.fontset"] = "dejavusans"


def num(v):
    if v >= 1e5:
        return f"{v:.1e}".replace("e+0", "e").replace("e+", "e")
    if v < 1e-4:
        return f"{v:.0e}".replace("e-0", "e-")
    return f"{v:g}"


# (标签, 起点, 终点, 数值标注放左侧?)
SCENE = [
    ("无月星空下的地面", 1e-4, 1e-3, False),
    ("满月照明的夜景", 2e-2, 2e-1, False),
    ("室内灯光下的白纸", 10, 100, False),
    ("阴天室外景物", 2e2, 2e3, False),
    ("晴天室外景物", 2e3, 2e4, False),
    ("阳光下的白云", 1e4, 3e4, False),
    ("太阳表面（直视）", 1.6e9, 1.6e9, False),
]
DISP = [
    ("影院银幕（SDR 白）", 48, 48, True),
    ("SDR 电视 / 显示器", 100, 350, False),
    ("HDR 电视（峰值）", 1000, 4000, False),
    ("手机屏（峰值）", 1000, 2000, False),
]
EYE = [
    ("视杆绝对阈值", 1e-6, 1e-6, False),
    ("明视觉下限", 3, 3, False),
    ("不适眩光起始", 1e4, 1e4, True),
]

rows, groups = [], []
y = 0.0
for title, items, color in [("自然与人造场景", SCENE, H.TEAL),
                            ("显示与观看条件", DISP, H.ORANGE),
                            ("人眼的工作边界", EYE, H.PURPLE)]:
    groups.append((title, y))
    y -= 1
    for name, lo, hi, left in items:
        rows.append((name, lo, hi, color, y, left))
        y -= 1
    y -= 0.55

fig, ax = plt.subplots(figsize=(8.4, 5.6))
fig.subplots_adjust(left=0.235, right=0.975, bottom=0.135, top=0.925)

ax.set_xscale("log")
ax.set_xlim(3e-7, 6e10)
ax.set_ylim(y + 0.7, 1.5)
ax.set_yticks([r[4] for r in rows])
ax.set_yticklabels([r[0] for r in rows])
ax.tick_params(axis="y", length=0, pad=6)

for name, lo, hi, color, yy, left in rows:
    if lo == hi:
        ax.plot([lo], [yy], "o", ms=7, color=color, mec="white", mew=1.0, zorder=4)
        if left:
            ax.text(lo / 2.2, yy, num(lo), va="center", ha="right",
                    fontsize=8.2, color=color)
        else:
            ax.text(lo * 2.0, yy, num(lo), va="center", ha="left",
                    fontsize=8.2, color=color)
    else:
        ax.plot([lo, hi], [yy, yy], color=color, lw=5.5, alpha=0.55,
                solid_capstyle="round", zorder=3)
        ax.text(hi * 2.4, yy, f"{num(lo)} – {num(hi)}", va="center", ha="left",
                fontsize=8.2, color=color)

for title, yy in groups:
    ax.text(3.2e-7, yy + 0.42, title, va="center", ha="left",
            fontsize=9.6, color=H.DARK)
    ax.plot([3e-7, 6e10], [yy + 0.9, yy + 0.9], color=H.LGRAY, lw=1.0, zorder=1)

ax.axvline(100, color=H.NAVY, lw=1.0, ls=(0, (4, 3)), zorder=2,
           label="SDR 参考白 100 cd/m$^2$")
ax.axvline(203, color=H.RED, lw=1.0, ls=(0, (4, 3)), zorder=2,
           label="HDR 参考白 203 cd/m$^2$")
ax.legend(loc="lower right", fontsize=8.2, bbox_to_anchor=(1.0, 0.02))

ax.set_xlabel("亮度（cd/m$^2$，对数刻度）")
ax.set_xticks([1e-6, 1e-4, 1e-2, 1, 1e2, 1e4, 1e6, 1e8, 1e10])
ax.set_xticklabels(["1e-6", "1e-4", "1e-2", "1", "100", "1e4", "1e6",
                    "1e8", "1e10"])
ax.xaxis.set_minor_formatter(NullFormatter())
ax.grid(axis="y", visible=False)

H.save(fig, 1, "f1_scene_luminance")
