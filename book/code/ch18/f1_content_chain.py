# -*- coding: utf-8 -*-
"""第 18 章 图 1：HDR 内容链路图（内容 → 编解码 → 播放器 → 显示）。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(7.2, 5.5))
ax.set_xlim(0, 100); ax.set_ylim(0, 100)
ax.axis("off"); ax.grid(False)


def rbox(x, y, w, h, fc, ec=None, lw=1.4, z=2, alpha=1.0):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.35,rounding_size=1.5",
                       linewidth=lw, edgecolor=ec if ec else fc, facecolor=fc,
                       alpha=alpha, zorder=z)
    ax.add_patch(p)
    return p


def arrow(x1, y1, x2, y2, color=H.GRAY, lw=1.8, ms=9, rad=0.0, z=3):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=ms, linewidth=lw, color=color,
                                 connectionstyle="arc3,rad=%s" % rad, zorder=z))


# ---------------- 左侧：① 内容（三条供给线） ----------------
rbox(1.5, 40.0, 29.0, 56.5, "#f5f8fb", ec=H.LGRAY, lw=1.2, z=1)
ax.text(16.0, 92.6, "① 内容　HDR 从哪来", ha="center", va="center",
        fontsize=9.8, fontweight="bold", color=H.DARK)

srcs = [
    (78.5, "游戏", ["实时渲染 · 帧未压缩", "显卡直接输出 HDR 信号"], H.ORANGE),
    (62.5, "影视", ["母版调色 → 压缩码流", "UHD 蓝光 / 流媒体"], H.NAVY),
    (46.5, "创作", ["后期导出的 HDR 文件", "调色 / 修图 / 参考监看"], H.TEAL),
]
for y, name, lines, c in srcs:
    rbox(3.0, y, 25.5, 11.6, "white", ec=c, lw=1.6, z=2)
    ax.text(4.4, y + 6.2, name, ha="left", va="center", fontsize=9.5,
            fontweight="bold", color=c)
    ax.text(4.4, y + 3.0, lines[0], ha="left", va="center", fontsize=6.8, color="#333")
    ax.text(4.4, y + 1.0, lines[1], ha="left", va="center", fontsize=6.8, color="#333")
    arrow(28.7, y + 5.8, 32.7, 70.0, color=c, lw=1.5, ms=8, rad=0.06)

# ---------------- 右侧：②③④ 链路主体 ----------------
stages = [
    (33.0, "② 编解码 / 封装", H.PURPLE,
     ["HEVC · VP9 · AV1",
      "10bit / 4:2:0 压缩",
      "元数据打包进码流",
      "静态：HDR10",
      "动态：DV / HDR10+",
      "流媒体 15–25 Mbps",
      "蓝光：数十 Mbps"]),
    (56.3, "③ 解码 / 播放器", H.BLUE,
     ["解码还原 PQ 码值",
      "读取 HDR 元数据",
      "按屏幕能力做映射",
      "madVR / mpv / 主机",
      "映射好坏决定观感",
      "相当于映射引擎",
      "（见第 17 章）"]),
    (79.6, "④ 显示", H.TEAL,
     ["PQ / HLG 反变换",
      "输出绝对亮度",
      "峰值 / 黑位受硬件限",
      "BT.2020 色域覆盖",
      "缺元数据 → 退回 SDR",
      "被眼睛真正看到",
      "（见第 11–13 章）"]),
]
for x, title, c, lines in stages:
    rbox(x, 50.0, 20.3, 40.0, c, z=2)
    ax.text(x + 10.15, 87.5, title, ha="center", va="center", fontsize=9.0,
            fontweight="bold", color="white")
    ax.plot([x + 2, x + 18.3], [85.3, 85.3], color="white", lw=0.9, alpha=0.6, zorder=3)
    for i, ln in enumerate(lines):
        ax.text(x + 1.4, 81.6 - i * 4.4, "· " + ln, ha="left", va="center",
                fontsize=6.6, color="white", zorder=3)

# 链路箭头
arrow(53.3, 70.0, 56.3, 70.0, color=H.DARK, lw=2.2, ms=10)
arrow(76.6, 70.0, 79.6, 70.0, color=H.DARK, lw=2.2, ms=10)
ax.text(31.75, 47.0, "母版\nPQ / HLG", ha="center", va="top", fontsize=6.4,
        color=H.NAVY, linespacing=1.35, fontweight="bold")
ax.text(54.8, 47.0, "码流\n+ 元数据\n随流传输", ha="center", va="top", fontsize=6.4,
        color=H.PURPLE, linespacing=1.35)
ax.text(78.1, 47.0, "HDMI / DP\n带宽 + HDCP\n（第 14–15 章）", ha="center", va="top",
        fontsize=6.4, color=H.TEAL, linespacing=1.35)

# ---------------- 底部：关键约束 ----------------
rbox(1.5, 24.0, 97.0, 12.0, "#fdf4e8", ec=H.ORANGE, lw=1.3, z=1)
ax.text(50.0, 32.3, "元数据必须跟着码流一起走：静态元数据（MaxCLL / MaxFALL）＋ 动态元数据（逐场景映射参数）",
        ha="center", va="center", fontsize=7.6, color="#8a4b00", fontweight="bold")
ax.text(50.0, 27.6, "解码器 / 播放器负责读取并交给色调映射 —— 元数据丢了，画面是 HDR 也没有 HDR 的灵魂",
        ha="center", va="center", fontsize=7.0, color="#8a4b00")

chips = [(1.5, "10bit 起步", H.NAVY), (26.0, "PQ 或 HLG", H.BLUE),
         (50.5, "BT.2020 容器", H.PURPLE), (75.0, "元数据随流传输", H.TEAL)]
for x, t, c in chips:
    rbox(x, 13.5, 23.5, 8.0, "white", ec=c, lw=1.5, z=2)
    ax.text(x + 11.75, 17.5, t, ha="center", va="center", fontsize=8.2,
            fontweight="bold", color=c)

rbox(1.5, 2.0, 97.0, 9.0, "#fdeceb", ec=H.RED, lw=1.3, z=1)
ax.text(50.0, 6.5, "链路效应：任一环掉链子（编解码不带元数据 / 播放器不映射 / 显示不支持 / 带宽或 HDCP 不足）\n"
                   "→ 画面发灰、过曝，甚至整条链路退回 SDR。",
        ha="center", va="center", fontsize=7.4, color="#8f2b20", fontweight="bold",
        linespacing=1.5)

ax.set_title("HDR 内容链路：从创作者的光，到你眼前的光", fontsize=12.5, fontweight="bold",
             color=H.DARK, pad=8)
H.save(fig, 18, "f1_content_chain")
