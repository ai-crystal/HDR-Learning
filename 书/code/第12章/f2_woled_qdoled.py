# -*- coding: utf-8 -*-
"""第12章 f2：WOLED（白光 + 滤光片）vs QD-OLED（蓝光 + 量子点）结构对比。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow, Circle

fig = plt.figure(figsize=(7.2, 5.6))
gs = fig.add_gridspec(2, 2, height_ratios=[1.95, 1.0], hspace=0.34, wspace=0.34)

RED_C, GREEN_C, BLUE_C, WHITE_C = "#d64545", "#3fae6a", "#3f6fd6", "#c9d2dc"


def stack(ax, title, subtitle, emitter_label, emitter_fc, subs, out_note):
    """画一个子像素剖面：emitter 层 + 上方分色层。subs: [(label, color, mode)]"""
    ax.grid(False)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.text(5, 9.72, title, ha="center", fontsize=11.5, color=H.NAVY, fontweight="bold")
    ax.text(5, 9.24, subtitle, ha="center", fontsize=8.4, color=H.GRAY)
    n = len(subs)
    w = 1.95; gap = 0.22
    total = n * w + (n - 1) * gap
    x0 = (10 - total) / 2
    # 基板 + 发光层
    ax.add_patch(Rectangle((0.25, 0.55), 9.5, 1.30, fc=emitter_fc, ec="#7a6a2a", lw=1.0))
    ax.text(5.0, 1.20, emitter_label, ha="center", va="center", fontsize=8.6,
            color="#4b3f0a", fontweight="bold")
    ax.add_patch(Rectangle((0.25, 0.28), 9.5, 0.26, fc=H.GRAY, ec="#4a5666", lw=0.8))
    ax.text(0.40, 0.41, "基板", fontsize=7.2, color="white", va="center")
    # 发光层出光箭头
    for i in range(n):
        cx = x0 + i * (w + gap) + w / 2
        col = WHITE_C if emitter_fc == "#f6e6a8" else BLUE_C
        ax.annotate("", xy=(cx, 2.42), xytext=(cx, 1.86),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.6))
    # 分色层
    ax.add_patch(Rectangle((0.25, 2.55), 9.5, 0.16, fc="#c7d0da", ec="#4a5666", lw=0.7))
    ax.text(9.9, 2.34, "阴极", fontsize=7.0, color=H.GRAY, va="center", ha="right")
    for i, (lab, col, mode) in enumerate(subs):
        x = x0 + i * (w + gap)
        if mode == "filter":
            ax.add_patch(Rectangle((x, 2.85), w, 0.95, fc=col, ec="#4a5666", lw=0.9, alpha=0.75, hatch="///"))
            ax.text(x + w / 2, 3.32, "滤光片", ha="center", va="center", fontsize=7.4, color="white")
        elif mode == "none":
            ax.add_patch(Rectangle((x, 2.85), w, 0.95, fc="white", ec="#4a5666", lw=0.9, ls="--"))
            ax.text(x + w / 2, 3.32, "无滤光片", ha="center", va="center", fontsize=7.4, color=H.GRAY)
        elif mode == "direct":
            ax.add_patch(Rectangle((x, 2.85), w, 0.95, fc="#9fbdf0", ec="#4a5666", lw=0.9, ls="--"))
            ax.text(x + w / 2, 3.32, "蓝光直出", ha="center", va="center", fontsize=7.6,
                    color=H.NAVY, fontweight="bold")
        else:  # qd
            ax.add_patch(Rectangle((x, 2.85), w, 0.95, fc=col, ec="#4a5666", lw=0.9, alpha=0.85))
            ax.text(x + w / 2, 3.32, "量子点", ha="center", va="center", fontsize=7.6,
                    color="white", fontweight="bold")
        # 出光箭头 + 子像素名
        ax.annotate("", xy=(x + w / 2, 4.62), xytext=(x + w / 2, 3.86),
                    arrowprops=dict(arrowstyle="-|>", color=col if mode != "none" else WHITE_C, lw=2.6))
        ax.add_patch(Circle((x + w / 2, 4.9), 0.30, fc=col if mode != "none" else WHITE_C, ec="none", alpha=0.9))
        ax.text(x + w / 2, 5.42, lab, ha="center", fontsize=9.4, color=H.NAVY, fontweight="bold")
    # 顶部说明
    ax.text(5.0, 6.35, out_note, ha="center", fontsize=8.2, color=H.ORANGE)
    # 左下角要点
    ax.text(5.0, 8.55 if False else 7.35, "", ha="center")
    ax.plot([0.25, 9.75], [7.1, 7.1], color="#dde3ea", lw=1.0)
    return ax


# ---- WOLED ----
ax1 = fig.add_subplot(gs[0, 0])
stack(ax1, "WOLED：白光 OLED + 彩色滤光片", "LG 阵营 · 常为 WRGB 四色",
      "白光 OLED 发光层（蓝光材料激发黄光 → 混成白）", "#f6e6a8",
      [("R", RED_C, "filter"), ("G", GREEN_C, "filter"), ("B", BLUE_C, "filter"), ("W", WHITE_C, "none")],
      "白光经滤光片分色；白子像素不滤光直接出光提亮")
ax1.text(5.0, 7.9, "滤光片丢光 → 彩色亮度偏低", ha="center", fontsize=8.2, color=H.RED)
ax1.text(5.0, 7.45, "白子像素\"稀释\"色彩纯度 → 广色域略逊", ha="center", fontsize=8.2, color=H.RED)

# ---- QD-OLED ----
ax2 = fig.add_subplot(gs[0, 1])
stack(ax2, "QD-OLED：蓝光 OLED + 量子点转色", "三星阵营 · RGB 三色",
      "蓝光 OLED 发光层（只发蓝光）", "#bcd2f2",
      [("R", RED_C, "qd"), ("G", GREEN_C, "qd"), ("B", BLUE_C, "direct")],
      "蓝光一部分直出为蓝，其余打到量子点转成纯红/纯绿")
# 蓝色的 "直出" 标注
ax2.text(0.5, 7.0, "", ha="center")
ax2.text(5.0, 7.9, "量子点转色几乎无滤光损失 → 色纯度高", ha="center", fontsize=8.2, color=H.GREEN)
ax2.text(5.0, 7.45, "彩色亮度与广色域更有优势", ha="center", fontsize=8.2, color=H.GREEN)

# ---- 下排：关键指标对比 ----
ax3 = fig.add_subplot(gs[1, 0])
labels = ["色纯度\n/色域", "彩色亮度", "光利用\n效率", "视角", "成本友好"]
wol = [3.4, 3.2, 3.3, 4.2, 4.4]
qdl = [4.6, 4.3, 4.5, 4.7, 3.2]
xx = np.arange(len(labels))
ax3.bar(xx - 0.20, wol, width=0.4, color=H.NAVY, label="WOLED")
ax3.bar(xx + 0.20, qdl, width=0.4, color=H.ORANGE, label="QD-OLED")
ax3.set_xticks(xx); ax3.set_xticklabels(labels, fontsize=8.0)
ax3.set_ylim(0, 5.6); ax3.set_yticks([0, 1, 2, 3, 4, 5])
ax3.set_ylabel("相对表现（5 分制）", labelpad=3)
ax3.set_title("两条路线各有取舍", fontsize=10, pad=4)
ax3.legend(loc="upper center", ncol=2, fontsize=8.4, bbox_to_anchor=(0.5, 1.0))
ax3.grid(axis="x", visible=False)

ax4 = fig.add_subplot(gs[1, 1])
names = ["色域覆盖\n(BT.2020)", "蓝色\n寿命压力", "制造成本\n(早期)"]
wv = [78, 30, 60]
qv = [90, 75, 85]
xx = np.arange(len(names))
ax4.bar(xx - 0.20, wv, width=0.4, color=H.NAVY, label="WOLED")
ax4.bar(xx + 0.20, qv, width=0.4, color=H.ORANGE, label="QD-OLED")
for i, (a, b) in enumerate(zip(wv, qv)):
    ax4.text(i - 0.20, a + 1.5, f"{a}", ha="center", fontsize=7.8, color=H.NAVY)
    ax4.text(i + 0.20, b + 1.5, f"{b}", ha="center", fontsize=7.8, color=H.ORANGE)
ax4.set_xticks(xx); ax4.set_xticklabels(names, fontsize=8.0)
ax4.set_ylim(0, 128)
ax4.set_ylabel("示意数值（%）", labelpad=3)
ax4.set_title("色域 vs 短板（示意，后两项越大越差）", fontsize=9.6, pad=4)
ax4.legend(loc="upper left", fontsize=8.4)
ax4.grid(axis="x", visible=False)

fig.suptitle("同叫 OLED，两条路：WOLED 白光滤色 vs QD-OLED 蓝光转色",
             fontsize=13.5, fontweight="bold", color=H.NAVY, y=0.985)
H.save(fig, 12, "f2_woled_qdoled")
