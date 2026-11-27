# -*- coding: utf-8 -*-
"""第 08 章 图 2：ICC 文件的字节布局与两类 profile 的数据通道。

左：头部 128 字节、tag 表、标签数据区三层结构
右：matrix/TRC 型与 mAB（CLUT）型的处理链
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt = H.plt

fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.8),
                         gridspec_kw={"width_ratios": [1.0, 1.18], "wspace": 0.12})

# ---------------- (a) 文件布局 ----------------
ax = axes[0]
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
ax.grid(False)

ax.text(0, 99, "(a) 一个 ICC 文件的字节布局", fontsize=8.4, color=H.DARK,
        ha="left", va="top")


def frame(x, y, w, h, fc="#f8fafc", ec=H.LGRAY, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.0,rounding_size=1.2",
                                fc=fc, ec=ec, lw=1.0, ls=ls, zorder=2))


frame(1, 60, 98, 32, fc="#eef4fa", ec=H.NAVY)
ax.text(4, 88.0, "头　128 字节", fontsize=7.0, color=H.NAVY, ha="left",
        va="center", zorder=4)
fields = ["0　文件总长度", "8　版本 4.3", "12　设备类 mntr",
          "16　数据色彩空间 RGB", "20　PCS 为 XYZ 或 Lab",
          "68　PCS 白点 0.9642, 1, 0.8249", "84　profile ID（MD5）"]
for i, f in enumerate(fields):
    ax.text(4, 82.0 - i * 3.4, f, fontsize=6.0, color=H.DARK, ha="left",
            va="center", zorder=4)

frame(1, 31, 98, 25, fc="#f4f8fc", ec=H.BLUE)
ax.text(4, 53.0, "tag 表　数量 + 每项 12 字节", fontsize=7.0, color=H.BLUE,
        ha="left", va="center", zorder=4)
ax.text(4, 48.0, "签名　　偏移　　长度", fontsize=5.8, color=H.GRAY, ha="left",
        va="center", zorder=4)
for i, (sig, off, ln) in enumerate([("A2B0", "356", "668"),
                                   ("B2A0", "1024", "1126"),
                                   ("wtpt", "2150", "20")]):
    yy = 43.0 - i * 3.9
    ax.text(4, yy, sig, fontsize=6.0, color=H.BLUE, ha="left", va="center",
            zorder=4)
    ax.text(24, yy, off, fontsize=6.0, color=H.DARK, ha="left", va="center",
            zorder=4)
    ax.text(46, yy, ln, fontsize=6.0, color=H.DARK, ha="left", va="center",
            zorder=4)
    ax.text(66, yy, "→ 数据区", fontsize=5.4, color=H.GRAY, ha="left",
            va="center", zorder=4)

frame(1, 3, 98, 25)
ax.text(4, 25.0, "标签数据区（每段 4 字节对齐）", fontsize=6.8, color=H.GRAY,
        ha="left", va="center", zorder=4)
for i, (t, fc, ec, tc) in enumerate([("A2B0\nmAB", "#dcebf7", H.BLUE, H.NAVY),
                                    ("B2A0\nmAB", "#dcebf7", H.BLUE, H.NAVY),
                                    ("wtpt\nrXYZ", "#fdf0e2", H.GOLD, "#8a6a20")]):
    x = 6 + i * 31
    ax.add_patch(FancyBboxPatch((x, 6), 26, 14,
                                boxstyle="round,pad=0,rounding_size=1.0",
                                fc=fc, ec=ec, lw=0.9, zorder=3))
    ax.text(x + 13, 13, t, fontsize=6.2, color=tc, ha="center", va="center",
            zorder=4, linespacing=1.3)

# ---------------- (b) 两类 profile ----------------
ax = axes[1]
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
ax.grid(False)

ax.text(0, 99, "(b) 两类 profile 的数据通道", fontsize=8.4, color=H.DARK,
        ha="left", va="top")


def chain(stages, y, col, h=13.0):
    n = len(stages)
    gap = 2.6
    w = (100.0 - gap * (n - 1)) / n
    for i, (t, dim) in enumerate(stages):
        x = i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0,rounding_size=1.0",
                                    fc="white" if not dim else "#fbfbfc",
                                    ec=col if not dim else H.LGRAY,
                                    lw=1.0, ls="-" if not dim else (0, (2, 2)),
                                    zorder=3))
        ax.text(x + w / 2, y + h / 2, t, fontsize=6.3,
                color=H.DARK if not dim else "#b9c2cc", ha="center",
                va="center", zorder=4, linespacing=1.3)
        if i < n - 1:
            ax.add_patch(FancyArrowPatch((x + w, y + h / 2),
                                         (x + w + gap, y + h / 2),
                                         arrowstyle="-|>", mutation_scale=8,
                                         color=col if not dim else H.LGRAY,
                                         lw=0.9, zorder=4))


ax.text(0, 84, "matrix / TRC", fontsize=7.2, color=H.NAVY, ha="left",
        va="center")
ax.text(27, 84, "显示器 profile 的常见形式，解析式没有格点误差", fontsize=6.2,
        color=H.GRAY, ha="left", va="center")
chain([("输入\n编码", False), ("3 条\nTRC", False), ("$3\\times3$\n矩阵", False),
       ("PCS\nXYZ", False)], 66, H.NAVY)

ax.text(0, 52, "mAB（A2B0）", fontsize=7.2, color=H.ORANGE, ha="left",
        va="center")
ax.text(27, 52, "扫描仪与打样常用，能装下任意非线性", fontsize=6.2,
        color=H.GRAY, ha="left", va="center")
chain([("输入\n编码", False), ("3 条\nA 曲线", False), ("$N^3$\nCLUT", False),
       ("$3\\times3$\n矩阵", False), ("3 条\nB 曲线", False), ("PCS\nXYZ", False)],
      34, H.ORANGE)

ax.text(0, 24, "mAB 的执行顺序是 A 曲线 → CLUT → 矩阵 → B 曲线，矩阵排在 CLUT 之后。",
        fontsize=6.5, color=H.DARK, ha="left", va="center")
ax.text(0, 17.5, "v2 的 mft2 相反，输入表 → 矩阵 → CLUT → 输出表，矩阵在前。",
        fontsize=6.5, color=H.DARK, ha="left", va="center")
ax.text(0, 11, "两者字段顺序不同，解析器要按类型分开处理；\n"
              "matrix/TRC 型没有 CLUT，陡峭的非线性只能靠 TRC 逼近。",
        fontsize=6.3, color=H.GRAY, ha="left", va="center", linespacing=1.5)

H.save(fig, 8, "f2_icc_tags")
