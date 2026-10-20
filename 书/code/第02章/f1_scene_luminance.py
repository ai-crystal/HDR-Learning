# -*- coding: utf-8 -*-
"""图 02-1 典型场景亮度（对数轴，单位 nit）

把现实世界常见发光 / 反射表面的亮度放到一条对数轴上，
直观展示「从星光到太阳横跨约十亿倍」。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np

plt = H.plt


def fmt(v):
    """亮度数值的中文友好格式化。"""
    if v >= 1000:
        return f"{v:,.0f} nit".replace(",", " ")
    return f"{v:g} nit"


# (名称, 亮度 nit, 颜色)
scenes = [
    ("无月星空（星光）",   0.0005, H.GRAY),
    ("月光下的地面",       0.05,   H.PURPLE),
    ("烛光附近的暗处",     1.0,    H.GOLD),
    ("昏暗室内",           10.0,   H.TEAL),
    ("普通室内照明的白纸", 100.0,  H.GREEN),
    ("明亮办公室 / 商店",  400.0,  H.NAVY),
    ("阴天户外",           2000.0, H.BLUE),
    ("晴天户外白墙",      10000.0, H.ORANGE),
    ("直视太阳附近",     160000.0, H.RED),
]

fig, ax = plt.subplots(figsize=(7.2, 4.8))

XMIN, XMAX = 1e-4, 1e6
n = len(scenes)
ys = np.arange(n)[::-1]

# 背景分区：暗场 / SDR 常见区间 / 高光区
ax.axvspan(XMIN, 1.0, color="#eef2f7", zorder=0)
ax.axvspan(100.0, XMAX, color="#fdf1e3", zorder=0)

# 参考线
ax.axvline(100.0, color=H.GREEN, ls="--", lw=1.4, zorder=2)
ax.axvline(0.001, color=H.GRAY, ls=":", lw=1.2, zorder=2)
ax.text(110.0, -0.28, "SDR 白点 ≈100 nit", color=H.GREEN, fontsize=8.4,
        fontweight="bold", va="top", ha="left", zorder=6)
ax.text(0.0012, -0.28, "夜空中值 ≈0.001 nit", color=H.GRAY, fontsize=7.8,
        va="top", ha="left", zorder=6)

for i, (name, v, c) in enumerate(scenes):
    y = ys[i]
    ax.plot([XMIN, v], [y, y], color=c, lw=2.6, zorder=3,
            solid_capstyle="round")
    ax.plot([v], [y], "o", color=c, ms=9, zorder=4,
            markeredgecolor="white", markeredgewidth=1.2)
    # 数值：大值标在左侧上方，小值标在右侧上方，避免越界
    if v >= 1000:
        ax.text(v, y + 0.16, fmt(v), color=c, fontsize=8.8, va="bottom",
                ha="right", zorder=5, fontweight="bold")
    else:
        ax.text(v * 1.35, y + 0.16, fmt(v), color=c, fontsize=8.8, va="bottom",
                ha="left", zorder=5, fontweight="bold")
    # 右侧名称（单行，避免上下行互相压字）
    ax.text(XMAX * 1.30, y, name, color=c, fontsize=10, va="center",
            ha="left", fontweight="bold")

ax.set_xscale("log")
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(-0.8, n + 0.45)
ax.set_yticks([])
ax.set_xlabel(r"亮度（nit，即 $\mathrm{cd/m^{2}}$，对数轴）", fontsize=10.5)
ax.set_title("现实世界的亮度跨度：从星光到太阳约横跨十亿倍", pad=12)
ax.set_xticks([1e-4, 1e-2, 1, 1e2, 1e4, 1e6])
ax.set_xticklabels([r"$10^{-4}$", r"$10^{-2}$", "1", "100", "10k", "1M"],
                   fontsize=9)
import matplotlib.ticker as mticker
ax.xaxis.set_minor_locator(mticker.LogLocator(base=10, subs=(2, 3, 4, 5, 6, 7, 8, 9), numticks=100))
ax.xaxis.set_minor_formatter(mticker.NullFormatter())
ax.tick_params(axis="x", which="minor", length=2.5)
ax.yaxis.grid(False)
ax.grid(True, axis="x", which="major", color="#dde3ea", lw=0.7)
ax.set_axisbelow(True)
ax.text(XMIN * 1.25, n + 0.20, "暗场", fontsize=8.5, color=H.GRAY,
        ha="left", va="bottom")
ax.text(XMAX * 0.85, n + 0.20, "高光 / 强光", fontsize=8.5, color=H.ORANGE,
        ha="right", va="bottom")

fig.subplots_adjust(left=0.05, right=0.60, top=0.91, bottom=0.16)
fig.text(0.5, 0.025,
         r"从 0.0005 nit（星光）到 160 000 nit（太阳附近）：总跨度 ≈ $3\times10^{8}$ 倍 ≈ 28 档（stop）",
         ha="center", va="bottom", fontsize=9, color=H.DARK, fontweight="bold")
H.save(fig, 2, "f1_scene_luminance")
