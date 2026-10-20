# -*- coding: utf-8 -*-
"""第 01 章 图 3：颜色/亮度标准的时间线（NTSC → BT.601 → BT.709 → sRGB → BT.2020 → BT.2100）。

要点：分辨率涨了近百倍，但"红绿蓝是什么颜色""白有多亮"几十年基本没变 —— 一路继承。
版式：单条主轴上/下方分两条"泳道"放事件标签，说明文字一律放在远离主轴的一侧，避免连线压字。
运行：D:/DevTools/Anaconda3/python.exe f3_history_timeline.py
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle

CAT = {
    "模拟广播": H.GOLD,
    "ITU 数字标准": H.NAVY,
    "PC / 桌面": H.TEAL,
    "数字电影": H.PURPLE,
    "HDR": H.RED,
}

# (年份, 名称, 说明, 类别, 泳道)  A1/A2 = 轴上方两条泳道，B1 = 轴下方一条泳道
EV = [
    (1953, "NTSC", "彩色电视开山（美国）\n首个 RGB 色域定义", "模拟广播", "A1"),
    (1967, "PAL / SECAM", "欧洲 / 中国采用的\n模拟制式", "模拟广播", "A2"),
    (1982, "BT.601", "数字标清（SD）规范\nYCbCr 与 SD 色域", "ITU 数字标准", "A1"),
    (1990, "BT.709", "高清（HD）规范：\nHD / 蓝光 / 网络视频", "ITU 数字标准", "A2"),
    (1996, "sRGB", "惠普 + 微软\nPC 的“最小公约数”\n同期还有 Adobe RGB（1998）\n（印刷 / 摄影用）", "PC / 桌面", "B1"),
    (2007, "DCI-P3", "数字电影放映色域", "数字电影", "A1"),
    (2012, "BT.2020", "UHD 大容器：\n色域远大于 sRGB", "ITU 数字标准", "B1"),
    (2016, "BT.2100", "HDR 规范：\nPQ / HLG + BT.2020", "HDR", "A2"),
]

LANE = {"A1": 1.15, "A2": 2.55, "B1": -1.15}
UP = {"A1", "A2"}

fig, ax = plt.subplots(figsize=(7.2, 5.0))
ax.set_xlim(1946, 2024)
ax.set_ylim(-3.95, 4.35)
ax.set_yticks([])
for sp in ("left", "right", "top"):
    ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.grid(False)

# ---------------- 时代分带（时代名放在底部） ----------------
eras = [(1946, 1982, "#f6edd9", "模拟时代", "黑白 → 彩色（只有亮度，后加颜色）"),
        (1982, 2010, "#e6edf5", "数字 SD / HD 时代", "分辨率 ↑，颜色与亮度约定不变"),
        (2010, 2024, "#fbe9e6", "UHD / HDR 时代", "4K / 8K + 宽色域 + HDR")]
for x0, x1, fc, name, sub in eras:
    ax.add_patch(Rectangle((x0, -3.95), x1 - x0, 7.80, facecolor=fc,
                           edgecolor="none", zorder=0))
    ax.text((x0 + x1) / 2, -3.28, name, ha="center", va="center", fontsize=9.0,
            color="#6b7784", fontweight="bold", zorder=1)
    ax.text((x0 + x1) / 2, -3.58, sub, ha="center", va="center", fontsize=7.0,
            color="#8a95a1", zorder=1)

# ---------------- 主轴 ----------------
ax.annotate("", xy=(2023.5, 0), xytext=(1946.5, 0),
            arrowprops=dict(arrowstyle="-|>", color="#4a5666", lw=1.8), zorder=2)

# ---------------- 事件 ----------------
for year, name, desc, cat, lane in EV:
    c = CAT[cat]
    y = LANE[lane]
    up = lane in UP
    ax.plot([year, year], [0, y - 0.05 if up else y + 0.05], color=c, lw=1.1, zorder=3)
    ax.plot([year], [0], marker="o", ms=6.5, color=c, zorder=4,
            markeredgecolor="white", markeredgewidth=1.0)
    ax.text(year, y, f"{year}  {name}", ha="center", va=("bottom" if up else "top"),
            fontsize=8.2, color=c, fontweight="bold", zorder=5,
            bbox=dict(boxstyle="round,pad=0.22", fc="white", ec=c, lw=0.8, alpha=0.96))
    ax.text(year, y + (0.42 if up else -0.42), desc, ha="center",
            va=("bottom" if up else "top"), fontsize=6.8, color="#4a5666",
            linespacing=1.35, zorder=5)

# ---------------- 顶部两条"括线" ----------------
def bracket(x0, x1, y, tick=0.12, color="#93a0ad"):
    ax.plot([x0, x1], [y, y], color=color, lw=1.2, zorder=6)
    for xx in (x0, x1):
        ax.plot([xx, xx], [y, y - tick], color=color, lw=1.2, zorder=6)


bracket(1953, 2016, 3.98)
ax.text(1984.5, 4.06, "颜色定义一路继承：红绿蓝是什么颜色、白有多亮，70 年基本没变",
        ha="center", va="bottom", fontsize=7.4, color="#6b7784", zorder=6)
bracket(1996, 2016, 3.52, tick=0.10, color=H.RED)
ax.text(2006, 3.58, "20 年后 HDR 才再次“松绑”", ha="center", va="bottom",
        fontsize=7.0, color=H.RED, zorder=6)

ax.set_xticks([1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020])
ax.set_xticklabels(["1950", "1960", "1970", "1980", "1990", "2000", "2010", "2020"],
                   fontsize=8.5)
ax.set_xlabel("年份", fontsize=10)

handles = [Patch(fc=CAT[k], label=k) for k in CAT]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.115),
          ncol=5, fontsize=7.8, frameon=False, handlelength=1.3, columnspacing=1.5)

ax.set_title("从 NTSC 到 BT.2100：颜色与亮度标准的时间线", fontsize=13,
             fontweight="bold", pad=10)

H.save(fig, 1, "f3_history_timeline")
