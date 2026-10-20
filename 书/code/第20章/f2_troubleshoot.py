# -*- coding: utf-8 -*-
"""第 20 章 f2_troubleshoot：HDR 排查流程图。
顺序：内容 → 显卡 → 线材 → 接口 → HDCP → 显示器 → 设置与映射；
每一环左边是"检查点"，右边是"不通过时的修复动作"。"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

CHK_BG, CHK_EC = "#eef4fb", H.NAVY
FIX_BG, FIX_EC = "#fdf3e7", H.ORANGE

# (序号, 环节名, [问题行], [修复行])
STEPS = [
    ("①", "内容源", ["片源 / 游戏 / 流媒体", "本身是 HDR 吗？"],
     ["换 HDR 片源；游戏里开 HDR /", "Auto HDR / RTX HDR"]),
    ("②", "显卡与系统", ["显卡支持 HDR，且系统里", "已经打开了 HDR 开关？"],
     ["更新显卡驱动；在系统显示设置", "里打开 HDR 开关"]),
    ("③", "线材", ["线材带宽够吗？", "是认证的高速线吗？"],
     ["换 HDMI 2.1 / DP 1.4 及以上", "的高速认证线"]),
    ("④", "接口", ["接口版本够吗？", "需要 DSC 压缩吗？"],
     ["换 2.0b / 2.1 接口，或降低", "分辨率 / 帧率 / 色深"]),
    ("⑤", "HDCP", ["HDCP 版本", "全链路匹配（2.2 / 2.3）吗？"],
     ["换 HDCP 2.2 / 2.3 全链路设备，", "避免过老的功放 / 切换器"]),
    ("⑥", "显示器", ["显示器 / 电视真的支持 HDR？", "（不是“假 HDR”）"],
     ["换真正达标（有认证 + 实测", "参数）的显示设备"]),
    ("⑦", "设置与映射", ["系统 + 播放器 / 游戏设置对吗？", "（模式、自动映射、HGiG）"],
     ["开 HDR、关自动映射、按需", "开 HGiG、检查校准"]),
]

fig, ax = plt.subplots(figsize=(7.2, 7.5))
ax.set_xlim(0, 10); ax.set_ylim(0, 15.1)
ax.axis("off"); ax.grid(False)

# ---------- 标题区 ----------
ax.text(5.0, 14.86, "HDR 排查流程图：从源头到眼睛，一环一环排除",
        fontsize=13, fontweight="bold", color=H.NAVY, ha="center", va="center")
ax.text(5.0, 14.56, "蓝色 = 检查点　　橙色 = 不通过时的修复动作　　"
                    "口诀：内容 → 显卡 → 线 → 接口 → HDCP → 显示器 → 设置",
        fontsize=7.4, color=H.GRAY, ha="center", va="center")

MX0, MX1 = 0.55, 4.75      # 检查点列
RX0, RX1 = 5.45, 9.80      # 修复列
BH = 1.28                  # 环节框高
XC = (MX0 + MX1) / 2

for i, (num, name, qlines, fixlines) in enumerate(STEPS):
    y_top = 13.90 - i * 1.72
    yb = y_top - BH
    # 检查点框
    ax.add_patch(FancyBboxPatch((MX0, yb), MX1 - MX0, BH,
                                boxstyle="round,pad=0,rounding_size=0.10",
                                facecolor=CHK_BG, edgecolor=CHK_EC, linewidth=1.3))
    ax.text(MX0 + 0.20, y_top - 0.30, f"{num} {name}", fontsize=9.4,
            fontweight="bold", color=H.NAVY, va="center", ha="left")
    ax.text(MX0 + 0.22, y_top - 0.70, qlines[0], fontsize=8.0, color=H.DARK,
            va="center", ha="left")
    ax.text(MX0 + 0.22, y_top - 1.02, qlines[1], fontsize=8.0, color=H.DARK,
            va="center", ha="left")

    # 修复动作框
    ax.add_patch(FancyBboxPatch((RX0, yb), RX1 - RX0, BH,
                                boxstyle="round,pad=0,rounding_size=0.10",
                                facecolor=FIX_BG, edgecolor=FIX_EC, linewidth=1.3))
    ax.text(RX0 + 0.18, y_top - 0.30, "否  →  这样修", fontsize=8.4,
            fontweight="bold", color=H.ORANGE, va="center", ha="left")
    ax.text(RX0 + 0.18, y_top - 0.70, fixlines[0], fontsize=7.7, color="#7a4a12",
            va="center", ha="left")
    ax.text(RX0 + 0.18, y_top - 1.02, fixlines[1], fontsize=7.7, color="#7a4a12",
            va="center", ha="left")

    # 横向箭头：否
    ax.add_patch(FancyArrowPatch((MX1 + 0.02, yb + BH / 2), (RX0 - 0.03, yb + BH / 2),
                                 arrowstyle="-|>", mutation_scale=11,
                                 color=H.ORANGE, linewidth=1.4))
    ax.text((MX1 + RX0) / 2, yb + BH / 2 + 0.20, "否", fontsize=8.5,
            fontweight="bold", color=H.ORANGE, ha="center", va="bottom")

    # 纵向箭头：是，进入下一环
    if i < len(STEPS) - 1:
        ax.add_patch(FancyArrowPatch((XC, yb), (XC, yb - 0.44),
                                     arrowstyle="-|>", mutation_scale=11,
                                     color=H.NAVY, linewidth=1.4))
        ax.text(XC + 0.14, yb - 0.22, "是", fontsize=8.5, fontweight="bold",
                color=H.NAVY, ha="left", va="center")

# 最后一环到底部结论
yb_last = 13.90 - 6 * 1.72 - BH
ax.add_patch(FancyArrowPatch((XC, yb_last), (XC, 2.02),
                             arrowstyle="-|>", mutation_scale=11,
                             color=H.NAVY, linewidth=1.4))
ax.text(XC + 0.14, (yb_last + 2.02) / 2, "是", fontsize=8.5, fontweight="bold",
        color=H.NAVY, ha="left", va="center")

# 结论框
ax.add_patch(FancyBboxPatch((MX0, 1.34), RX1 - MX0, 0.62,
                            boxstyle="round,pad=0,rounding_size=0.12",
                            facecolor="#eafaf1", edgecolor=H.GREEN, linewidth=1.5))
ax.text(5.0, 1.65, "全链路通畅 →  HDR 正常显示；若仍发灰/偏暗，多半是最后的映射与校准问题（§20.2）",
        fontsize=8.4, fontweight="bold", color="#1e6b3a", ha="center", va="center")

# 症状速查条
ax.add_patch(FancyBboxPatch((MX0, 0.24), RX1 - MX0, 0.90,
                            boxstyle="round,pad=0,rounding_size=0.10",
                            facecolor="#f4f6f8", edgecolor=H.LGRAY, linewidth=1.0))
ax.text(MX0 + 0.20, 1.00, "按症状定位（对症下药）", fontsize=8.2,
        fontweight="bold", color=H.NAVY, va="center", ha="left")
ax.text(MX0 + 0.20, 0.72, "画面发灰 → 映射/设置（⑥⑦）　　完全没有 HDR 提示 → 内容或系统开关（①②）　　"
                          "黑屏 / 闪屏 → HDCP 或线材（③⑤）",
        fontsize=7.4, color=H.DARK, va="center", ha="left")
ax.text(MX0 + 0.20, 0.46, "高光一片死白 → 映射过激，开 HGiG 或换映射方案（⑦）　　"
                          "暗部糊成黑块 → 黑位/校准或环境光太亮（⑥⑦）",
        fontsize=7.4, color=H.DARK, va="center", ha="left")

# 左侧竖向提示
ax.text(0.22, 8.0, "从源头（内容）到眼睛（屏幕）", rotation=90, fontsize=8.4,
        fontweight="bold", color=H.GRAY, ha="center", va="center")

H.save(fig, 20, "f2_troubleshoot")
