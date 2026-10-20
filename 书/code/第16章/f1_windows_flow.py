# -*- coding: utf-8 -*-
"""图 16-1　Windows HDR 设置流程：开关 → SDR 亮度滑块 → 校准

画一张纵向流程图，说明 Windows 上开启 HDR 的完整步骤链，
并在右侧给出每一步的注意事项，底部给出务实建议。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(7.2, 5.4))
ax.set_xlim(0, 10.6); ax.set_ylim(0, 10.9)
ax.axis("off"); ax.grid(False)
ax.set_title("图 16-1　Windows HDR 设置四步流程：开关 → SDR 亮度滑块 → 校准",
             pad=10)


def box(x, y, w, h, fc, ec, radius=0.10, lw=1.5):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0.02,rounding_size={radius}",
                       linewidth=lw, edgecolor=ec, facecolor=fc, zorder=3)
    ax.add_patch(p)
    return p


def arrow(x0, y0, x1, y1, color=H.DARK, lw=1.8):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1),
                                 arrowstyle="-|>", mutation_scale=15,
                                 linewidth=lw, color=color, zorder=2))


# ---------------- 左侧主流程 ----------------
LX, BW = 0.35, 4.10
CX = LX + BW / 2
RX = LX + BW

steps = [
    (8.35, 1.20, H.NAVY, "① 设置 → 系统 → 显示 → HDR",
     "前提：显卡 / 线 / 接口 /\n显示器全链路支持 HDR\n（见第 14、15 章）"),
    (6.85, 1.20, H.BLUE, "② 打开 HDR 总开关",
     "开关灰掉＝链路不支持，\n先排查线缆与接口"),
    (5.15, 1.45, H.ORANGE, "③ 拖动「SDR 内容亮度」滑块",
     "决定 SDR 桌面白点落在\nHDR 屏上的亮度位置；\n目标：和以前开 SDR 时\n「差不多舒服」"),
    (3.35, 1.45, H.TEAL, "④ 运行 Windows HDR 校准应用",
     "三个测试图案：最小亮度 /\n最大亮度 / 最大帧平均亮度"),
    (1.55, 1.30, H.GREEN, "⑤ 生成 ICC → 系统准确渲染",
     "建议同时在显示器上关掉\n「动态增强 / 自动亮度」，\n让校准结果生效（呼应 HGiG）"),
]

for y, h, c, title, note in steps:
    box(LX, y, BW, h, c, c, radius=0.12)
    ax.text(CX, y + h / 2, title, ha="center", va="center", color="white",
            fontsize=9.9, fontweight="bold", zorder=4)

for i in range(len(steps) - 1):
    ytop = steps[i][0]
    ybot = steps[i + 1][0] + steps[i + 1][1]
    arrow(CX, ytop, CX, ybot)

# ---------------- 右侧注意事项 ----------------
NX = RX + 0.25
ax.text(NX, 10.05, "每步的要点", ha="left", va="center", fontsize=8.8,
        fontweight="bold", color=H.NAVY)
for (y, h, c, title, note) in steps:
    ax.plot([RX + 0.02, NX - 0.10], [y + h / 2, y + h / 2],
            color=H.LGRAY, lw=1.0, zorder=1)
    ax.text(NX, y + h / 2, note, ha="left", va="center", fontsize=7.4,
            color=H.DARK, linespacing=1.5, zorder=4)

# ---------------- 顶部核心提示 ----------------
box(3.30, 9.78, 6.95, 0.62, "#eef3f9", H.NAVY, radius=0.10, lw=1.1)
ax.text(6.77, 10.09, "核心：HDR 不是「开了就好」，而是要把 SDR / HDR 调平衡",
        ha="center", va="center", fontsize=8.4, color=H.NAVY,
        fontweight="bold")

# ---------------- 底部两条结论 ----------------
box(0.35, 0.42, 4.10, 0.66, "#fdf3e3", H.ORANGE, radius=0.10, lw=1.2)
ax.text(2.40, 0.75, "滑块低＝SDR 发灰发暗　高＝刺眼发白",
        ha="center", va="center", fontsize=7.5, color="#8a5a12")

box(4.70, 0.42, 5.55, 0.66, "#eaf4ef", H.GREEN, radius=0.10, lw=1.2)
ax.text(7.47, 0.75, "务实建议：平时用 SDR，看 HDR 影视 / 玩 HDR 游戏时再开",
        ha="center", va="center", fontsize=7.5, color="#1d6b45",
        fontweight="bold")

H.save(fig, 16, "f1_windows_flow")
