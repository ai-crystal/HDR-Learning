# -*- coding: utf-8 -*-
"""图 19-1　HDR 显示器选购要点信息图（七件事，优先级从高到低）。

把 19.2 的选购清单做成一张信息图：每行给出「看什么 / 为什么重要 / 怎么看」，
右侧给出关键量化目标徽章。左侧色条与序号圆点按优先级档着色
（P1 先看 → P2 再看 → P3 最后看），徽章边框用各条目的主题色区分。
底部是记忆口诀与按用途选屏的提醒。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(7.2, 5.9))
ax.set_xlim(0, 10); ax.set_ylim(0.2, 11.2)
ax.axis("off"); ax.grid(False)
ax.set_title("图 19-1　HDR 显示器选购七件事（优先级从高到低）", pad=12)

# 优先级档颜色（与顶部图例一致）
TIER = {"P1": H.NAVY, "P2": H.TEAL, "P3": H.GOLD}


def box(x, y, w, h, fc, ec, radius=0.10, lw=1.3, alpha=1.0, z=3):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0.02,rounding_size={radius}",
                       linewidth=lw, edgecolor=ec, facecolor=fc, alpha=alpha,
                       zorder=z)
    ax.add_patch(p)
    return p


# 序号, 标题, 为什么重要, 怎么看, 关键目标徽章, 主题色, 优先级档
rows = [
    (1, "峰值亮度", "决定高光冲击力，是 HDR 的“上限”",
     "看认证等级或实测，别只看标称值", "目标 ≥ 600–1000 nit", H.BLUE, "P1"),
    (2, "分区调光 / 黑位", "决定暗部纯净度与对比度",
     "LCD 看分区数与 FALD；OLED 逐像素天然好", "数百–数千 分区 / OLED", H.ORANGE, "P1"),
    (3, "原生对比度", "黑得下去，亮才有意义",
     "别信“动态对比度”的百万比一", "看原生对比度", H.RED, "P1"),
    (4, "色域覆盖", "决定颜色能有多“艳”",
     "看“DCI-P3 覆盖率”，且必须注明参照", "DCI-P3 ≥ 90%", H.PURPLE, "P2"),
    (5, "色深", "10bit 起步，避免色带",
     "看清是真 10bit 还是 8bit+FRC", "≥ 10bit（真）", H.GREEN, "P2"),
    (6, "认证", "一份可信的“下限保证”",
     "DisplayHDR 等级 / True Black（见第 13 章）", "认准认证等级", H.TEAL, "P3"),
    (7, "面板类型", "决定对比、可视角度与响应",
     "IPS / VA / OLED 各有取舍（见第 11、12 章）", "按用途取舍", H.GRAY, "P3"),
]

RH, GAP, top = 1.02, 0.18, 10.05
for i, (n, title, why, how, badge, c, tier) in enumerate(rows):
    y = top - (i + 1) * RH - i * GAP
    tc = TIER[tier]
    box(0.35, y, 9.30, RH, "#f7f9fb", "#e3e9ef", radius=0.09, lw=1.0)
    box(0.35, y, 0.16, RH, tc, tc, radius=0.05, lw=0)          # 优先级色条
    ax.add_patch(plt.Circle((0.90, y + RH / 2), 0.26, color=tc, zorder=4))
    ax.text(0.90, y + RH / 2, str(n), ha="center", va="center", color="white",
            fontsize=11, fontweight="bold", zorder=5)
    ax.text(1.34, y + RH - 0.30, title, ha="left", va="center",
            fontsize=11, fontweight="bold", color="#22303f")
    ax.text(1.34, y + 0.44, why, ha="left", va="center", fontsize=8.1,
            color="#3d4856")
    ax.text(1.34, y + 0.18, "怎么看：" + how, ha="left", va="center",
            fontsize=7.8, color=H.GRAY)
    box(6.75, y + 0.24, 2.85, 0.56, "white", c, radius=0.08, lw=1.2)
    ax.text(8.17, y + 0.52, badge, ha="center", va="center", fontsize=8.5,
            color=c, fontweight="bold")

# ---------------- 顶部优先级图例 ----------------
ax.text(0.35, 10.62, "优先级：", ha="left", va="center", fontsize=8.6,
        color=H.NAVY, fontweight="bold")
lx = 1.55
for lab, c, txt in [("P1", H.NAVY, "先看"), ("P2", H.TEAL, "再看"),
                    ("P3", H.GOLD, "最后看")]:
    ax.add_patch(plt.Rectangle((lx, 10.47), 0.30, 0.30, color=c, zorder=4))
    ax.text(lx + 0.42, 10.62, f"{lab} {txt}", ha="left", va="center",
            fontsize=8.4, color="#3d4856")
    lx += 1.55

# ---------------- 底部口诀与提醒 ----------------
box(0.35, 0.45, 6.05, 0.86, "#eef3f9", H.NAVY, radius=0.10, lw=1.1)
ax.text(3.37, 0.88, "口诀：先看黑位和峰值，再看色域和色深，最后看认证",
        ha="center", va="center", fontsize=8.0, color=H.NAVY,
        fontweight="bold")
ax.text(3.37, 0.62, "峰值亮度孤立地看没有意义——黑不下去的屏，HDR 观感未必好",
        ha="center", va="center", fontsize=7.5, color=H.GRAY)
box(6.60, 0.45, 3.05, 0.86, "#fdf3e3", H.ORANGE, radius=0.10, lw=1.1)
ax.text(8.12, 0.88, "按用途选", ha="center", va="center", fontsize=8.6,
        color="#8a5a12", fontweight="bold")
ax.text(8.12, 0.62, "游戏看响应 · 影视看黑位\n创作看色准 · 办公未必需要 HDR",
        ha="center", va="center", fontsize=7.3, color="#8a5a12",
        linespacing=1.4)

H.save(fig, 19, "f1_buy_checklist")
