# -*- coding: utf-8 -*-
"""图 08-4：HDR10 信号链路图。

画面（视频数据）与元数据两条支路，经接口一起送到显示端，在显示端汇合后做色调映射。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import numpy as np
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig = plt.figure(figsize=(7.2, 5.0))
ax = fig.add_axes([0.01, 0.04, 0.98, 0.88])
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.axis("off")

CX = [0.135, 0.375, 0.615, 0.855]
W, Hh = 0.205, 0.155
Y_VID, Y_META = 0.755, 0.455


def node(cx, cy, line1, line2, fc, w=W, h=Hh, tc="white", fs=7.2):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=0.012",
                                fc=fc, ec=fc, lw=1.0, zorder=3,
                                transform=ax.transData))
    ax.text(cx, cy + 0.022, line1, ha="center", va="center", fontsize=fs,
            color=tc, fontweight="bold", zorder=4)
    ax.text(cx, cy - 0.032, line2, ha="center", va="center", fontsize=fs - 0.6,
            color=tc, zorder=4)


def arrow(p0, p1, color=H.DARK, lw=1.6, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=11,
                                 color=color, lw=lw, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=0, shrinkB=0, zorder=2))


# ---- 赛道（lane）标签 ----
ax.text(0.135, 0.880, "画面数据（视频流）", ha="center", va="center",
        fontsize=8.2, color=H.NAVY, fontweight="bold")
ax.text(0.135, 0.590, "元数据（关于画面的信息）", ha="center", va="center",
        fontsize=8.2, color=H.TEAL, fontweight="bold")

# ---- 视频流 ----
node(CX[0], Y_VID, "母版调色定稿", "4000 nit 母版显示器", H.NAVY)
node(CX[1], Y_VID, "PQ + 10bit + BT.2020", "封装为 HEVC / AV1 码流", H.BLUE)
node(CX[2], Y_VID, "HDMI 2.0a / DP 1.4", "视频数据（18 Gbps 内）", H.PURPLE)
node(CX[3], Y_VID, "解析 PQ 码值", "还原为绝对亮度", H.RED)
for k in range(3):
    arrow((CX[k] + W / 2 + 0.004, Y_VID), (CX[k + 1] - W / 2 - 0.004, Y_VID))

# ---- 元数据流 ----
node(CX[0], Y_META, "ST 2086：母版信息", "基色 / 白点 / 亮度范围", H.TEAL)
node(CX[1], Y_META, "MaxCLL / MaxFALL", "全片最亮像素 / 最亮帧均值", H.TEAL)
node(CX[2], Y_META, "静态元数据 InfoFrame", "CTA-861.3 随信号同行", H.TEAL)
node(CX[3], Y_META, "读取元数据", "决定映射策略", H.RED)
for k in range(3):
    arrow((CX[k] + W / 2 + 0.004, Y_META), (CX[k + 1] - W / 2 - 0.004, Y_META),
          color=H.TEAL)

# ---- 接口边界 ----
ax.axvline(0.735, color=H.GRAY, ls="--", lw=1.1, ymin=0.30, ymax=0.855, zorder=1)
ax.text(0.735, 0.885, "HDMI / DP 线缆", fontsize=6.8, color=H.GRAY,
        ha="center", va="center")

# ---- 汇合 ----
arrow((CX[3], Y_VID - Hh / 2 - 0.004), (0.60, 0.205), color=H.RED, rad=-0.18)
arrow((CX[3], Y_META - Hh / 2 - 0.004), (0.64, 0.205), color=H.RED, rad=-0.15)
ax.add_patch(FancyBboxPatch((0.5 - 0.33, 0.105), 0.66, 0.145,
                            boxstyle="round,pad=0,rounding_size=0.012",
                            fc="#fdf1e3", ec=H.ORANGE, lw=1.6, zorder=3))
ax.text(0.5, 0.180, "色调映射（Tone Mapping）", ha="center", va="center",
        fontsize=8.4, color=H.ORANGE, fontweight="bold", zorder=4)
ax.text(0.5, 0.133, "把 4000 nit 的高光压进显示器峰值以内 → 送去驱动面板",
        ha="center", va="center", fontsize=7.0, color=H.DARK, zorder=4)

# ---- 阶段编号 ----
for cx, lab in zip(CX, ["① 内容制作", "② 编码打包", "③ 接口传输", "④ 显示端"]):
    ax.text(cx, 0.960, lab, ha="center", va="center", fontsize=7.4,
            color=H.DARK, fontweight="bold")

# ---- 关键提醒 ----
ax.text(0.015, 0.300,
        "只有 HDMI 2.0a / DP 1.4 及以上才携带 HDR 元数据：\n"
        "老接口只能送画面，元数据这一路是断的 → HDR 开不起来。",
        ha="left", va="center", fontsize=7.0, color=H.RED, linespacing=1.6)

ax.set_title("HDR10 信号链路：画面与元数据两条支路，在显示端汇合",
             fontsize=11, color=H.NAVY, pad=4)

fig.text(0.5, 0.012,
         "注意：InfoFrame 里装的是一组固定数值（一个 MaxCLL、一个 MaxFALL、一套母版信息），"
         "而不是逐帧曲线 —— 这就是“静态元数据”的由来。",
         ha="center", va="bottom", fontsize=7.4, color=H.DARK)

H.save(fig, 8, "f4_hdr10_pipeline")
