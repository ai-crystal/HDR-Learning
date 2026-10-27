# -*- coding: utf-8 -*-
"""第 20 章 f3_roadmap：HDR 精通路线图（入门 → 进阶 → 专家）。
五级台阶：会用 → 读标准 → 懂数学 → 会调色 → 会测量，底部按三大阶段分带。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

# (台阶标题, [要点行], 台阶面颜色, 阶段)
STEPS = [
    ("① 入门·会用", ["懂“动态范围”", "看懂 nit / 峰值 / 黑位", "会开 HDR、调设置"],
     "#3d7bb8", "入门"),
    ("② 进阶·读标准", ["BT.2100 总纲", "ST 2084（PQ）", "CTA-861 / BT.2390"],
     H.TEAL, "进阶"),
    ("③ 进阶·懂数学", ["CIE XYZ、色度坐标", "白点换算、函数推导", "自算色域覆盖率"],
     H.GREEN, "进阶"),
    ("④ 专家·会调色", ["Resolve 调色实战", "波形 / 矢量示波器", "定峰值与黑位"],
     H.PURPLE, "专家"),
    ("⑤ 专家·会测量", ["校色仪 / 分光计", "DisplayCAL / Calman", "验峰值·色域·灰阶"],
     H.NAVY, "专家"),
]

fig, ax = plt.subplots(figsize=(7.2, 4.9))
ax.set_xlim(0, 10); ax.set_ylim(0, 7.5)
ax.axis("off"); ax.grid(False)

Y0 = 1.50            # 基线
W, PITCH = 1.80, 1.95
HEIGHTS = [1.65, 2.25, 3.00, 3.80, 4.60]

# 顶部注释
ax.text(5.0, 7.22, "HDR 精通路线图：从“会用”到“能辨真伪”",
        fontsize=13, fontweight="bold", color=H.NAVY, ha="center", va="center")
ax.text(5.0, 6.94, "越往上，越接近全链路工程思维 —— 每一层都能让你更懂“为什么”",
        fontsize=8, color=H.GRAY, ha="center", va="center")
ax.add_patch(FancyArrowPatch((0.35, 6.45), (9.85, 6.45), arrowstyle="-|>",
                             mutation_scale=12, color=H.ORANGE, linewidth=1.4,
                             linestyle=(0, (5, 3)), zorder=4))
ax.text(5.0, 6.45, "持续精进：会用 → 读标准 → 懂数学 → 会调色 → 会测量",
        fontsize=7.6, fontweight="bold", color=H.ORANGE, ha="center", va="center",
        zorder=5, bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                            edgecolor="none"))

# 坐标轴：深度箭头 + 基线
ax.add_patch(FancyArrowPatch((0.14, Y0), (0.14, 6.10), arrowstyle="-|>",
                             mutation_scale=11, color=H.GRAY, linewidth=1.2))
ax.text(0.03, 3.8, "深度", rotation=90, fontsize=8.4, fontweight="bold",
        color=H.GRAY, ha="center", va="center")
ax.plot([0.14, 9.92], [Y0, Y0], color=H.GRAY, linewidth=1.2)

for i, (title, bullets, color, tier) in enumerate(STEPS):
    x = 0.28 + i * PITCH
    h = HEIGHTS[i]
    top = Y0 + h
    # 台阶（带阴影底）
    ax.add_patch(Rectangle((x + 0.04, Y0 - 0.04), W, h, facecolor="#c9d2db",
                           edgecolor="none", zorder=1))
    ax.add_patch(Rectangle((x, Y0), W, h, facecolor=color, edgecolor="white",
                           linewidth=1.2, zorder=2))
    # 台阶标题（白色加粗）
    ax.text(x + W / 2, top - 0.25, title, fontsize=8.0, fontweight="bold",
            color="white", ha="center", va="center", zorder=3)
    ax.plot([x + 0.18, x + W - 0.18], [top - 0.42, top - 0.42],
            color="#ffffff", alpha=0.55, linewidth=0.9, zorder=3)
    # 要点
    for j, b in enumerate(bullets):
        ax.text(x + W / 2, top - 0.70 - j * 0.32, b, fontsize=6.3,
                color="white", ha="center", va="center", zorder=3)

# 阶段分带（底部）
BANDS = [(0.28, 2.08, "#dbe8f5", H.BLUE, "入门：会用"),
         (2.23, 5.93, "#d8f0ea", H.TEAL, "进阶：读标准 + 懂数学"),
         (6.08, 9.83, "#e5dff2", H.PURPLE, "专家：会调色 + 会测量")]
for x0, x1, bg, ec, label in BANDS:
    ax.add_patch(FancyBboxPatch((x0, 0.70), x1 - x0, 0.56,
                                boxstyle="round,pad=0,rounding_size=0.10",
                                facecolor=bg, edgecolor=ec, linewidth=1.1))
    ax.text((x0 + x1) / 2, 0.98, label, fontsize=7.8, fontweight="bold",
            color=ec, ha="center", va="center")

# 底部一句话
ax.text(5.0, 0.26, "理解得越完整，越不会被营销词牵着走；能一眼看出“这个参数是真的、那个是凑数的”，就算真的精通了。",
        fontsize=8.0, color=H.NAVY, ha="center", va="center")

H.save(fig, 20, "f3_roadmap")
