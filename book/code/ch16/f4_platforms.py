# -*- coding: utf-8 -*-
"""图 16-4　四平台 HDR 速查图：Windows / macOS / 主机 / 手机与流媒体

2×2 卡片，每张卡含「关键机制 / 你要做的事 / 心法」，
底部给出三条共通心法。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(7.2, 5.2))
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.axis("off"); ax.grid(False)
ax.set_title("图 16-4　四大平台 HDR 速查：谁在管、你要做什么", pad=8)

cards = [
    dict(x=0.25, y=5.30, w=4.55, h=4.15, c=H.NAVY,
         name="Windows", sub="双语频道：手动调平衡",
         rows=[("关键机制", "HDR 开关 + SDR 亮度滑块 +\nHDR 校准应用"),
               ("你要做的事", "调滑块对齐 SDR 白点；\n跑一遍校准应用"),
               ("额外功能", "Auto HDR 为老 SDR 游戏补光")],
         mantra="平时 SDR，用 HDR 时再开"),
    dict(x=5.20, y=5.30, w=4.55, h=4.15, c=H.TEAL,
         name="macOS", sub="EDR：局部 HDR",
         rows=[("关键机制", "EDR 局部开 HDR + 自动 HDR"),
               ("你要做的事", "日常几乎无需手动设置"),
               ("专业场景", "参考模式锁定色域 / 白点 / EOTF")],
         mantra="让它自动管，需要时锁标准"),
    dict(x=0.25, y=0.95, w=4.55, h=4.15, c=H.ORANGE,
         name="PS5 / Xbox", sub="主机校准 + HGiG",
         rows=[("关键机制", "主机校准界面 + HGiG 模式"),
               ("你要做的事", "认真跑校准，别一路跳过"),
               ("换屏之后", "换电视 / 换接口后重校")],
         mantra="认真校一次，换屏重校"),
    dict(x=5.20, y=0.95, w=4.55, h=4.15, c=H.PURPLE,
         name="手机 / 流媒体", sub="厂商替你调好了",
         rows=[("关键机制", "厂商预设 + App 识别 HDR"),
               ("你要做的事", "保证带宽；按需 App 开关"),
               ("注意点", "带宽不足会自动降级 SDR")],
         mantra="厂商已调好，注意网络"),
]

for d in cards:
    ax.add_patch(FancyBboxPatch((d["x"], d["y"]), d["w"], d["h"],
                                boxstyle="round,pad=0.04,rounding_size=0.16",
                                facecolor="#fbfcfe", edgecolor=d["c"], lw=1.5,
                                zorder=1))
    # 头部色条
    ax.add_patch(FancyBboxPatch((d["x"] + 0.10, d["y"] + d["h"] - 0.86),
                                d["w"] - 0.20, 0.78,
                                boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor=d["c"], edgecolor=d["c"], lw=1.0,
                                zorder=2))
    ax.text(d["x"] + 0.30, d["y"] + d["h"] - 0.58, d["name"], fontsize=11.0,
            color="white", fontweight="bold", ha="left", va="center", zorder=3)
    ax.text(d["x"] + d["w"] - 0.30, d["y"] + d["h"] - 0.58, d["sub"],
            fontsize=7.2, color="#e9eef5", ha="right", va="center", zorder=3)

    yy = d["y"] + d["h"] - 1.32
    for k, v in d["rows"]:
        ax.text(d["x"] + 0.28, yy, k, fontsize=7.7, fontweight="bold",
                color=d["c"], ha="left", va="center", zorder=3)
        ax.text(d["x"] + 1.38, yy, v, fontsize=6.9, color=H.DARK,
                ha="left", va="center", zorder=3, linespacing=1.45)
        yy -= 1.00
    # 心法条
    ax.add_patch(FancyBboxPatch((d["x"] + 0.20, d["y"] + 0.20),
                                d["w"] - 0.40, 0.58,
                                boxstyle="round,pad=0.02,rounding_size=0.10",
                                facecolor="#eef1f5", edgecolor="none", zorder=2))
    ax.text(d["x"] + d["w"] / 2, d["y"] + 0.49, "心法：" + d["mantra"],
            fontsize=7.8, color=d["c"], fontweight="bold", ha="center",
            va="center", zorder=3)

# 底部共通心法
ax.text(5.0, 0.60, "共通三条：　① 校准优先于开关　② SDR 桌面与 HDR 正片分开对待"
                   "　③ 换屏 / 换接口 / 重装驱动后重校一次",
        ha="center", va="center", fontsize=7.4, color=H.NAVY,
        fontweight="bold")

H.save(fig, 16, "f4_platforms")
