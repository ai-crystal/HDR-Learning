# -*- coding: utf-8 -*-
"""第15章 图4：DSC 约 3:1 视觉无损压缩的数据量对比。"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

fig, ax = plt.subplots(figsize=(7.2, 5.6))
ax.set_xlim(0, 12)
ax.set_ylim(0, 9.6)
ax.axis("off")


def rbox(x, y, w, h, fc="#ffffff", ec=H.GRAY, lw=1.2, r=0.08, z=3, alpha=1.0):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={r}",
                       fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha)
    ax.add_patch(p)
    return p


def sec(y, txt, color=H.NAVY):
    ax.add_patch(FancyBboxPatch((0.26, y - 0.15), 0.16, 0.3,
                 boxstyle="round,pad=0,rounding_size=0.04",
                 fc=color, ec="none", zorder=4))
    ax.text(0.56, y, txt, ha="left", va="center", fontsize=9.5,
            color=color, fontweight="bold", zorder=4)


ax.set_title("图 15-4　DSC：用约 3:1 的视觉无损压缩，把高规格信号塞进链路",
             fontsize=12.2, fontweight="bold", pad=8)

# ---------------- ① 数据量对比 ----------------
sec(9.45, "① 以 4K120 · 10bit · 4:4:4 为例：原始码流放不下，压完就够用")
ax.text(0.30, 9.14, "算例：3840 × 2160 × 120fps × 30bit ≈ 29.9 Gbps（未含链路开销）",
        ha="left", va="center", fontsize=7.2, color=H.DARK, zorder=5)

X0, K = 3.60, 8.0 / 34.0          # 横轴起点、每 Gbps 对应宽度
LIMIT = X0 + 25.92 * K            # DP 1.4 有效带宽上限


def bar(y, val, label1, label2, color, fc, vcolor="white", lw=1.6):
    w = val * K
    rbox(X0, y, w, 0.52, fc=fc, ec=color, lw=lw, r=0.06)
    ax.text(X0 - 0.15, y + 0.34, label1, ha="right", va="center", fontsize=7.6,
            color=color, fontweight="bold", zorder=5)
    ax.text(X0 - 0.15, y + 0.12, label2, ha="right", va="center", fontsize=6.8,
            color=H.DARK, zorder=5)
    ax.text(min(X0 + w - 0.12, LIMIT - 0.14), y + 0.26, f"{val:.1f} Gbps",
            ha="right", va="center",
            fontsize=7.8, color=vcolor, fontweight="bold", zorder=6)
    return w


bar(8.50, 29.9, "原始码流（未压缩）", "4K120 · 10bit · 4:4:4",
    H.NAVY, H.NAVY)
bar(7.62, 25.92, "DP 1.4 可用有效带宽", "（承载上限）",
    H.GRAY, "#eef1f5", vcolor=H.NAVY)
bar(6.74, 10.0, "开启 DSC 后", "≈3:1 视觉无损压缩",
    H.GREEN, H.GREEN)

# 超限部分标红
ax.add_patch(Rectangle((LIMIT, 8.50), 29.9 * K - 25.92 * K, 0.52,
             fc=H.RED, ec="none", zorder=5))
ax.text(X0 + 29.9 * K, 8.30, "超出 ≈4 Gbps → 原生跑不动", ha="right",
        va="center", fontsize=7.0, color=H.RED, fontweight="bold", zorder=6)
ax.text(X0 + 10.0 * K + 0.25, 7.00, "√ 余量充足，可开高刷", ha="left",
        va="center", fontsize=7.2, color=H.GREEN, fontweight="bold", zorder=6)

# 上限线
ax.plot([LIMIT, LIMIT], [6.45, 9.10], color=H.RED, lw=1.8, ls=(0, (5, 3)),
        zorder=7)
ax.text(LIMIT + 0.12, 9.02, "DP 1.4 上限\n25.9 Gbps", ha="left", va="bottom",
        fontsize=6.8, color=H.RED, fontweight="bold", zorder=7)

# 横轴
ax.plot([X0, 11.6], [6.45, 6.45], color=H.GRAY, lw=1.2, zorder=3)
for val in (0, 10, 20, 30):
    xp = X0 + val * K
    ax.plot([xp, xp], [6.45, 6.33], color=H.GRAY, lw=1.2, zorder=3)
    ax.text(xp, 6.14, f"{val}", ha="center", va="center", fontsize=7.0,
            color=H.GRAY, fontweight="bold", zorder=3)
ax.text(11.6, 6.14, "Gbps", ha="right", va="center", fontsize=7.0,
        color=H.GRAY, fontweight="bold", zorder=3)

# ---------------- ② 压缩比与视觉无损 ----------------
sec(5.80, "② 压缩比 ≈ 3:1：原始 3 份数据，链路上只传 1 份")
# 左：原始 3 份
ax.text(1.12, 5.20, "原始 3 份数据", ha="center", va="center", fontsize=7.6,
        color=H.NAVY, fontweight="bold", zorder=5)
for i, y in enumerate((4.55, 3.95, 3.35)):
    rbox(0.35, y, 1.55, 0.50, fc="#f2f6fb", ec=H.NAVY, lw=1.4, r=0.06)
    ax.text(1.12, y + 0.25, f"原始数据 {i + 1}", ha="center", va="center",
            fontsize=7.0, color=H.NAVY, fontweight="bold", zorder=5)

# 箭头
ax.add_patch(FancyArrowPatch((2.05, 4.20), (3.02, 4.20), arrowstyle="-|>",
             mutation_scale=16, color=H.GREEN, lw=2.2, zorder=4))
ax.text(2.53, 4.42, "≈ 3 : 1", ha="center", va="bottom", fontsize=7.8,
        color=H.GREEN, fontweight="bold", zorder=5)

# 压缩流 1 份
rbox(3.10, 3.91, 1.55, 0.58, fc="#eafaf1", ec=H.GREEN, lw=1.7, r=0.06)
ax.text(3.875, 4.20, "DSC 压缩流", ha="center", va="center", fontsize=7.2,
        color=H.GREEN, fontweight="bold", zorder=5)
ax.text(4.80, 4.20, "（1 份）", ha="left", va="center", fontsize=7.0,
        color=H.GREEN, zorder=5)

# 右：卡片
rbox(6.30, 3.15, 5.50, 2.30, fc="#f7f9fc", ec=H.BLUE, lw=1.7, r=0.09)
ax.text(6.48, 5.16, "为什么敢叫“视觉无损”", ha="left", va="center",
        fontsize=8.4, color=H.BLUE, fontweight="bold", zorder=5)
pts = [
    "逐块预测 + 差量编码：只传变化的部分",
    "固定码率、极低延迟，适合实时链路",
    "目标是让人眼分辨不出：无块状、无条带",
    "≠ 有损视频编码，链路两端实时编解码",
]
for i, t in enumerate(pts):
    ax.text(6.48, 4.72 - i * 0.45, "· " + t, ha="left", va="center",
            fontsize=7.2, color=H.DARK, zorder=5)

# ---------------- ③ 要点 ----------------
rbox(0.2, 0.30, 11.6, 2.15, fc="#f3f6fa", ec=H.LGRAY, lw=1.4, r=0.10)
ax.text(0.46, 2.10, "要点", ha="left", va="center", fontsize=8.6,
        color=H.NAVY, fontweight="bold", zorder=5)
tips = [
    ("DSC 由 VESA 制定，压缩比通常约 3:1，设计目标是“视觉无损”。", H.NAVY),
    ("带宽不够时的三条路：降色深（牺牲暗部）/ 降色度采样（牺牲色彩细节）/ 开 DSC（几乎不牺牲观感）。", H.DARK),
    ("DP 1.4 的“4K120”、HDMI 2.1 高规格模式多半靠 DSC 撑起；偶发闪屏可尝试关 DSC 或换好线。", H.DARK),
]
for i, (t, c) in enumerate(tips):
    ax.text(0.46, 1.62 - i * 0.50, "· " + t, ha="left", va="center",
            fontsize=7.4, color=c, fontweight=("bold" if i == 0 else "normal"))

H.save(fig, 15, "f4_dsc")
