# -*- coding: utf-8 -*-
"""第 20 章 f4_glossary_map：HDR 术语关系地图。
中心是 HDR，六大门类（基础 / 色彩 / 标准 / 硬件 / 传输 / 软件）环绕，
每个门类列出代表术语并标注对应章节，一张图串起全书词汇。"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import to_rgb


def tint(color, t=0.12):
    """把颜色与白色混合，得到不透明的浅色底（避免透出连接线）。"""
    r, g, b = to_rgb(color)
    return (1 - t + t * r, 1 - t + t * g, 1 - t + t * b)

# (门类标题, [术语行], 主色, (中心 x, 中心 y))
CLUSTERS = [
    ("基础 · 概念（§1–2）",
     ["动态范围（DR）", "nit / cd·m2", "峰值 · 黑位 · 对比度", "stop（档）", "SDR vs HDR"],
     H.NAVY, (0.500, 0.855)),
    ("色彩 · 色度（§4–5）",
     ["色域 / 覆盖率", "BT.2020 大容器", "CIE XYZ · 色度坐标", "白点 D65", "10bit 位深"],
     H.PURPLE, (0.185, 0.675)),
    ("软件 · 流程（§16–19）",
     ["色调映射 Tone Mapping", "HGiG", "ICC · 3D LUT", "HDR 开关 · Auto HDR", "校准 · 色彩管理"],
     H.GREEN, (0.815, 0.675)),
    ("标准 · 编码（§7–9）",
     ["BT.2100 总纲", "PQ（ST 2084）", "HLG", "HDR10 / HDR10+ / DV", "DisplayHDR 认证"],
     H.RED, (0.185, 0.285)),
    ("传输 · 链路（§14–15）",
     ["HDMI 2.1 / DP 1.4", "带宽（Gbps）", "DSC 视觉无损压缩", "HDCP 2.2 / 2.3", "EDID · 元数据"],
     H.TEAL, (0.815, 0.285)),
    ("硬件 · 显示（§11–13）",
     ["LCD · Mini-LED · FALD", "OLED · QD-OLED", "分区调光", "ABL 亮度限制", "峰值亮度 nit"],
     H.ORANGE, (0.500, 0.135)),
]

BW, BH = 0.300, 0.265      # 门类框尺寸（axes 比例）
CX, CY = 0.50, 0.50        # 中心

fig, ax = plt.subplots(figsize=(7.2, 6.2))
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.axis("off"); ax.grid(False)

# 标题
ax.text(0.5, 1.045, "HDR 术语关系地图：六大门类，一张图串起全书",
        fontsize=13, fontweight="bold", color=H.NAVY, ha="center", va="center")
ax.text(0.5, 1.005, "中心：HDR（高动态范围）　—— 把知识按“基础 / 色彩 / 标准 / 硬件 / 传输 / 软件”归类，就不容易记混",
        fontsize=7.8, color=H.GRAY, ha="center", va="center")

# 连接线（先画，被框遮住中段）
for _, _, color, (cx, cy) in CLUSTERS:
    ax.plot([CX, cx], [CY, cy], color=color, linewidth=1.8, alpha=0.55, zorder=1)

# 中心节点
ax.add_patch(FancyBboxPatch((CX - 0.085, CY - 0.075), 0.170, 0.150,
                            boxstyle="round,pad=0,rounding_size=0.05",
                            facecolor=H.DARK, edgecolor=H.GOLD, linewidth=1.8,
                            zorder=3))
ax.text(CX, CY + 0.035, "HDR", fontsize=15, fontweight="bold", color="white",
        ha="center", va="center", zorder=4)
ax.text(CX, CY - 0.035, "高动态范围", fontsize=7.6, color="#d8e2ee",
        ha="center", va="center", zorder=4)

# 六个门类
for title, terms, color, (cx, cy) in CLUSTERS:
    x0, y0 = cx - BW / 2, cy - BH / 2
    ax.add_patch(FancyBboxPatch((x0, y0), BW, BH,
                                boxstyle="round,pad=0,rounding_size=0.035",
                                facecolor=tint(color), edgecolor="none",
                                zorder=2))
    ax.add_patch(FancyBboxPatch((x0, y0), BW, BH,
                                boxstyle="round,pad=0,rounding_size=0.035",
                                facecolor="none", edgecolor=color, linewidth=1.5,
                                zorder=3))
    ax.text(cx, cy + BH / 2 - 0.030, title, fontsize=8.0, fontweight="bold",
            color=color, ha="center", va="center", zorder=4)
    ax.plot([x0 + 0.020, x0 + BW - 0.020], [cy + BH / 2 - 0.052, cy + BH / 2 - 0.052],
            color=color, linewidth=0.9, alpha=0.6, zorder=4)
    for j, t in enumerate(terms):
        ax.text(cx, cy + BH / 2 - 0.083 - j * 0.034, t, fontsize=6.6,
                color=H.DARK, ha="center", va="center", zorder=4)

# 底部提示
ax.text(0.5, 0.0, "记忆路径：概念（为什么）→ 色彩与标准（怎么定义）→ 硬件与传输（能不能送到）→ 软件与流程（好不好看）。",
        fontsize=7.8, color=H.GRAY, ha="center", va="top")

H.save(fig, 20, "f4_glossary_map")
