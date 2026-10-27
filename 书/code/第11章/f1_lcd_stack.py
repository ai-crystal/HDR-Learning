# -*- coding: utf-8 -*-
"""第 11 章 · 图 11-1：LCD 结构剖面（背光 + 液晶闸门 + 彩色滤光片）。

从观众的眼睛往里看：一片恒亮的背光，夹在两片偏光片之间的液晶"百叶窗"，
以及把每个像素拆成 R/G/B 三个子像素的彩色滤光片。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import numpy as np
import hdrfig as H
import matplotlib.patches as mpatch

X0, X1 = 2.45, 6.25          # 屏体横向范围
fig, ax = H.plt.subplots(figsize=(7.2, 5.6))
ax.set_xlim(0, 16); ax.set_ylim(-1.3, 9.0)
ax.axis("off"); ax.grid(False)

def layer(y0, y1, fc, ec="#4a5666", lw=1.0, z=2, alpha=1.0):
    r = mpatch.Rectangle((X0, y0), X1 - X0, y1 - y0, facecolor=fc,
                         edgecolor=ec, linewidth=lw, alpha=alpha, zorder=z)
    ax.add_patch(r)
    return r

# ---------------- 各层 ----------------
# 背光模组（含 LED 灯珠 + 导光板 + 扩散板）
layer(0.30, 1.75, "#e8eef6")
for i in range(11):                                   # LED 灯珠
    cx = X0 + 0.28 + i * (X1 - X0 - 0.56) / 10.0
    ax.add_patch(mpatch.Rectangle((cx - 0.09, 0.48), 0.18, 0.34, facecolor=H.GOLD,
                                  edgecolor="#8a6d1f", linewidth=0.6, zorder=3))
ax.plot([X0, X1], [1.18, 1.18], color="#9db3cc", lw=1.0, zorder=3)
ax.text((X0 + X1) / 2, 1.44, "导光板 / 扩散板", ha="center", va="center",
        fontsize=8, color="#33475f", zorder=4)
ax.text((X0 + X1) / 2, 0.83, "LED 灯珠（恒亮）", ha="center", va="center",
        fontsize=8, color="#6b5410", zorder=4)

# 后偏光片 / TFT 基板 / 液晶层 / 彩色滤光片 / 前偏光片
layer(1.75, 2.35, "#b9c6d6")
layer(2.35, 3.05, "#dfe6ee")
for i in range(12):                                   # TFT 开关
    cx = X0 + (i + 0.5) * (X1 - X0) / 12.0
    ax.add_patch(mpatch.Rectangle((cx - 0.07, 2.62), 0.14, 0.16, facecolor=H.NAVY,
                                  edgecolor="none", zorder=3))
layer(3.05, 4.55, "#cfe3f5", alpha=0.95)
rng = np.random.default_rng(3)
for i in range(11):                                   # 液晶分子（示意）
    cx = X0 + (i + 0.5) * (X1 - X0) / 11.0
    ang = np.deg2rad(58 if i % 2 == 0 else 122)
    dx, dy = 0.16 * np.cos(ang), 0.42 * np.sin(ang)
    ax.plot([cx - dx, cx + dx], [3.80 - dy, 3.80 + dy], color=H.PURPLE,
            lw=1.4, zorder=3, solid_capstyle="round")
ax.text((X0 + X1) / 2, 4.34, "液晶分子通电转向", ha="center", va="center",
        fontsize=7.6, color="#5b3a86", zorder=4)

# 彩色滤光片：R/G/B 子像素
for i in range(12):
    cx0 = X0 + i * (X1 - X0) / 12.0
    c = [("#e74c3c", "R"), ("#27ae60", "G"), ("#2980b9", "B")][i % 3]
    ax.add_patch(mpatch.Rectangle((cx0, 4.55), (X1 - X0) / 12.0, 0.80,
                                  facecolor=c[0], edgecolor="white",
                                  linewidth=0.6, alpha=0.62, zorder=3))
ax.text((X0 + X1) / 2, 5.15, "R  G  B  R  G  B  …", ha="center", va="center",
        fontsize=7.6, color="#12314f", zorder=5)
layer(5.35, 5.95, "#b9c6d6")

# ---------------- 光路：亮场 / 黑场 ----------------
ax.annotate("", xy=(3.05, 5.95), xytext=(3.05, 0.25),
            arrowprops=dict(arrowstyle="-|>", color=H.GOLD, lw=5.0,
                            mutation_scale=14, alpha=0.9), zorder=6)
ax.annotate("", xy=(5.65, 3.80), xytext=(5.65, 0.25),
            arrowprops=dict(arrowstyle="-|>", color="#59667a", lw=5.0,
                            mutation_scale=14, alpha=0.9), zorder=6)
ax.annotate("", xy=(5.65, 5.95), xytext=(5.65, 3.86),
            arrowprops=dict(arrowstyle="-|>", color="#59667a", lw=1.6,
                            mutation_scale=10, alpha=0.55), zorder=6)
ax.text(3.05, 6.30, "亮场：液晶开\n光几乎全通过", ha="center", va="bottom",
        fontsize=8, color="#8a6d1f", fontweight="bold", linespacing=1.35)
ax.text(5.65, 6.30, "黑场：液晶关\n仍漏出一点光", ha="center", va="bottom",
        fontsize=8, color="#3d4a5c", fontweight="bold", linespacing=1.35)
ax.annotate("", xy=(4.35, 7.95), xytext=(4.35, 6.35),
            arrowprops=dict(arrowstyle="-|>", color=H.NAVY, lw=1.8,
                            mutation_scale=12), zorder=6)
ax.text(4.35, 8.20, "观众的眼睛", ha="center", va="bottom", fontsize=9,
        color=H.NAVY, fontweight="bold")

# ---------------- 右侧标注 ----------------
labels = [
    (5.65, 6.35, "前偏光片", "只让某一个振动方向的光通过"),
    (4.95, 5.40, "彩色滤光片（R / G / B 子像素）", "1 个像素 = 红绿蓝三块小格子"),
    (3.80, 4.45, "液晶层（光阀 / 百叶窗）", "通电时分子转向，决定挡多少光"),
    (2.70, 3.50, "TFT 玻璃基板", "每个子像素一个独立开关"),
    (2.05, 2.55, "后偏光片", "与前面一片配合，把液晶变成闸门"),
    (1.02, 1.60, "背光模组（恒亮）", "真正发光的只有它，整块共用"),
]
LX = 6.62
for yc, yt, name, desc in labels:
    ax.plot([X1 + 0.03, LX], [yc, yc], ls=(0, (1.6, 1.6)), color="#9aa7b6",
            lw=0.9, zorder=1)
    ax.plot([LX, LX], [yc, yt], ls=(0, (1.6, 1.6)), color="#9aa7b6", lw=0.9,
            zorder=1)
    ax.add_patch(mpatch.Rectangle((LX, yt - 0.09), 0.18, 0.18,
                                  facecolor=H.ORANGE, edgecolor="none"))
    ax.text(LX + 0.33, yt + 0.20, name, ha="left", va="center", fontsize=9,
            color=H.NAVY, fontweight="bold")
    ax.text(LX + 0.33, yt - 0.24, desc, ha="left", va="center", fontsize=8,
            color=H.GRAY)

notes = ("液晶控制的是「挡多少光」，不是「发多少光」——LCD 自己完全不发光。\n"
         "黑位由背光泄露锁定在 0.1–0.5 nit：峰值 400 nit 的屏，同时对比度也只有 ≈1000:1。")
ax.text(5.9, -0.72, notes, ha="center", va="center", fontsize=8.4, color="#243b55",
        linespacing=1.6, zorder=5,
        bbox=dict(boxstyle="round,pad=0.42", facecolor="#f3f6fa",
                  edgecolor="#c3ceda", linewidth=0.9))
ax.set_title("LCD 结构剖面：恒亮的背光 + 液晶闸门 + 彩色滤光片", fontsize=12.5,
             pad=8, loc="center")

H.save(fig, 11, "f1_lcd_stack")
