# -*- coding: utf-8 -*-
"""第 20 章 f1_myths：十大 HDR 常见误区对照信息图（误区 × / 真相 √）。
左红右绿：每格上半是"常见说法"，下半是"实际真相"。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

RED_BG = "#fdecea"
RED_TX = "#9b2c1f"
GRN_BG = "#eafaf1"
GRN_TX = "#1e6b3a"

# (误区短句, [真相行1, 真相行2])
MYTHS = [
    ("峰值亮度越高，HDR 就越好",
     ["峰值只是“上限”，不是充分条件；",
      "黑位、对比度与映射同样决定观感"]),
    ("HDR 就是“颜色更艳”",
     ["HDR 的本职是扩大亮度动态范围；",
      "广色域是另一维度，别混为一谈"]),
    ("DisplayHDR 400 完全是废物",
     ["门槛低，但有实测下限保证；",
      "比无认证的“假 HDR”更可靠"]),
    ("8bit+FRC 就是真 10bit",
     ["FRC 靠抖动两帧模拟中间色阶，",
      "能改善色带，但不等于原生 10bit"]),
    ("摄影的 HDR 合成＝HDR 显示",
     ["HDR 合成是后期技巧，输出 SDR 图；",
      "HDR 显示是编码+传输+发光体系"]),
    ("HDR 一直开着最好",
     ["SDR 内容会被错误映射而发灰；",
      "日常 SDR，看片/玩游戏再开"]),
    ("有 Dolby Vision 标就一定更好看",
     ["元数据有优势，但观感取决于母片质量、",
      "设备映射，以及是否真的用上元数据"]),
    ("显示器标了“HDR”就真支持 HDR",
     ["要看认证等级与实测峰值/黑位参数，",
      "不能只看宣传字样"]),
    ("亮度越高越伤眼",
     ["高光只在局部、瞬时出现；",
      "伤眼的是过暗环境+长时间近距离用眼"]),
    ("开 HDR 一定大幅耗电、还伤屏",
     ["有自动亮度限制（ABL）在保护；",
      "烧屏与长期固定高亮静态画面相关"]),
]

fig, ax = plt.subplots(figsize=(7.2, 6.3))
ax.set_xlim(0, 2); ax.set_ylim(0, 6.25)
ax.axis("off"); ax.grid(False)

ax.text(1.0, 6.12, "十大 HDR 常见误区：错在哪 · 对在哪",
        fontsize=13.5, fontweight="bold", color=H.NAVY, ha="center", va="center")
ax.text(1.0, 5.94, "× 常见说法（不成立或不完整）　√ 正确认知　—— 十条都能自己指出来，才算真的懂 HDR",
        fontsize=7.8, color=H.GRAY, ha="center", va="center")

CW = 0.94          # 单元格宽
CH = 0.96          # 单元格高
COLX = [0.03, 1.03]

for i, (claim, truth) in enumerate(MYTHS):
    col = i // 5
    row = i % 5
    x0 = COLX[col]
    y_top = 5.56 - row * 1.02
    y_bot = y_top - CH

    # 上半：误区（淡红）
    ax.add_patch(FancyBboxPatch(
        (x0, y_top - 0.46), CW, 0.44,
        boxstyle="round,pad=0,rounding_size=0.03",
        facecolor=RED_BG, edgecolor="#e8b4ac", linewidth=0.8, clip_on=False))
    # 下半：真相（淡绿）
    ax.add_patch(FancyBboxPatch(
        (x0, y_bot + 0.01), CW, 0.52,
        boxstyle="round,pad=0,rounding_size=0.03",
        facecolor=GRN_BG, edgecolor="#a9dcc1", linewidth=0.8, clip_on=False))

    # 误区行
    ax.text(x0 + 0.045, y_top - 0.16, "×", color=H.RED, fontsize=13,
            fontweight="bold", va="center", ha="left")
    ax.text(x0 + 0.115, y_top - 0.15, f"误区 {i+1}", color=RED_TX, fontsize=7.6,
            fontweight="bold", va="center", ha="left")
    ax.text(x0 + 0.30, y_top - 0.15, claim, color="#5c2018", fontsize=7.9,
            fontweight="bold", va="center", ha="left")
    ax.plot([x0 + 0.03, x0 + CW - 0.03], [y_top - 0.24, y_top - 0.24],
            color="#e8b4ac", linewidth=0.8, clip_on=False)

    # 真相行
    ax.text(x0 + 0.045, y_top - 0.60, "√", color=H.GREEN, fontsize=12,
            fontweight="bold", va="center", ha="left")
    ax.text(x0 + 0.115, y_top - 0.59, "真相", color=GRN_TX, fontsize=7.6,
            fontweight="bold", va="center", ha="left")
    ax.text(x0 + 0.045, y_top - 0.78, truth[0], color="#12502c", fontsize=7.2,
            va="center", ha="left")
    ax.text(x0 + 0.045, y_top - 0.92, truth[1], color="#12502c", fontsize=7.2,
            va="center", ha="left")

# 底部提示条
ax.add_patch(FancyBboxPatch((0.03, 0.10), 1.94, 0.26,
                            boxstyle="round,pad=0,rounding_size=0.06",
                            facecolor="#eef4fb", edgecolor="#b9cde4",
                            linewidth=0.8, clip_on=False))
ax.text(1.0, 0.23, "一句话记法：HDR = 更亮的高光 + 更深的黑位 + 更大的动态范围，"
                   "而不是“更艳”；参数只是必要条件，观感由全链路决定。",
        fontsize=8, color=H.NAVY, ha="center", va="center")

H.save(fig, 20, "f1_myths")
