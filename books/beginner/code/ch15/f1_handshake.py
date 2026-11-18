# -*- coding: utf-8 -*-
"""第 15 章 图 15-1：EDID → 模式协商 → 元数据 → HDCP → 显示 的链路握手时序图。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

fig, ax = plt.subplots(figsize=(7.2, 5.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10.2)
ax.invert_yaxis()
ax.axis("off")

XL, XR = 2.95, 7.05
C_L, C_R = H.NAVY, H.ORANGE


def actor(x, label, color):
    ax.add_patch(FancyBboxPatch((x - 1.85, 0.02), 3.7, 0.78,
                 boxstyle="round,pad=0.02,rounding_size=0.12",
                 fc=color, ec="none", zorder=5))
    ax.text(x, 0.41, label, ha="center", va="center", color="white",
            fontsize=10.0, fontweight="bold", zorder=6)


actor(XL, "主机（显卡 / 播放器）", C_L)
actor(XR, "显示器 / 电视", C_R)

# 生命线
ax.plot([XL, XL], [0.95, 9.05], color=C_L, lw=1.4, ls=(0, (5, 3)), zorder=2)
ax.plot([XR, XR], [0.95, 9.05], color=C_R, lw=1.4, ls=(0, (5, 3)), zorder=2)


def msg(y, x0, x1, text, color, style="->", note=None):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>",
                 mutation_scale=14, color=color, lw=2.0,
                 linestyle="--" if style == "--" else "-", zorder=4,
                 shrinkA=1, shrinkB=1))
    ax.text((x0 + x1) / 2, y - 0.15, text, ha="center", va="bottom",
            fontsize=8.8, color=color, fontweight="bold", zorder=5)
    if note:
        ax.text(max(x0, x1) + 0.12, y + 0.02, note, ha="left", va="center",
                fontsize=7.4, color=H.DARK, zorder=5)


# 阶段：彩色竖条 + 左侧横排短标签（不再用竖排，避免裁切）
phases = [
    (1.15, 1.95, "① 物理连接", H.GRAY, 1.55),
    (2.05, 3.55, "② 能力读取", H.TEAL, 2.45),
    (3.70, 5.35, "③ 模式协商", H.BLUE, 4.10),
    (5.55, 6.85, "④ 许可验证", H.RED, 5.95),
    (7.05, 8.95, "⑤ 画面 / 元数据", H.GREEN, 7.45),
]
for y0, y1, txt, c, ly in phases:
    ax.add_patch(Rectangle((0.05, y0), 0.13, y1 - y0, fc=c, ec="none", alpha=0.9, zorder=3))
    ax.text(0.26, ly, txt, ha="left", va="center", fontsize=7.8, color=c,
            fontweight="bold", zorder=6)

# ① HPD
msg(1.55, XR, XL, "HPD：我插上 / 唤醒啦", H.GRAY,
    note="热插拔检测\n告知主机上线")
# ② EDID
msg(2.45, XL, XR, "请把你的 EDID 给我（DDC 通道）", H.TEAL)
msg(3.25, XR, XL, "EDID：分辨率 / 色深 / 色域 / HDR", H.TEAL, style="--",
    note="扩展块含\nHDR 静态元数据")
# ③ 协商
ax.add_patch(FancyBboxPatch((1.55, 3.72), 2.75, 0.62,
             boxstyle="round,pad=0.02,rounding_size=0.1",
             fc="#eaf2fb", ec=H.BLUE, lw=1.4, zorder=5))
ax.text(2.925, 4.03, "双方取交集 → 选定信号格式", ha="center", va="center",
        fontsize=8.4, color=H.BLUE, fontweight="bold", zorder=6)
msg(4.95, XL, XR, "确认：4K120 / 10bit / 4:4:4 / HDR10", H.BLUE)
# ④ HDCP
msg(5.95, XL, XR, "HDCP 验证请求（版本 2.3）", H.RED)
msg(6.55, XR, XL, "HDCP 就绪 √", H.RED, style="--")
# ⑤ 画面
msg(7.45, XL, XR, "开始传画面 + AVI InfoFrame 元数据", H.GREEN)

# 底部结果
ax.add_patch(FancyBboxPatch((1.15, 8.05), 7.7, 0.72,
             boxstyle="round,pad=0.03,rounding_size=0.12",
             fc="#eafaf1", ec=H.GREEN, lw=1.6, zorder=5))
ax.text(5.0, 8.41, "HDR 稳定显示 √　（任一步失败 → 表现为“HDR 不行”）",
        ha="center", va="center", fontsize=9.0, color=H.GREEN, fontweight="bold", zorder=6)

ax.set_title("图 15-1　从插上线到亮出 HDR：链路握手时序", fontsize=12.5,
             fontweight="bold", pad=10)
H.save(fig, 15, "f1_handshake")
