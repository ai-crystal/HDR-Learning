# -*- coding: utf-8 -*-
"""图 16-3　HDR 校准应用的三种测试图案示意

2×2：
  左上 最小亮度 —— 暗部近黑阶梯，校黑位 / 暗部起始点
  右上 最大亮度 —— 小窗口白块，校峰值 / 高光上限
  左下 最大帧平均亮度 —— 大面积亮场，校大片亮场的容忍度
  右下 校准结果 → ICC 配置文件（含 HGiG 建议）
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig = plt.figure(figsize=(7.2, 4.9))
gs = fig.add_gridspec(2, 2, left=0.04, right=0.97, top=0.86, bottom=0.055,
                      hspace=0.42, wspace=0.16)
fig.suptitle("图 16-3　Windows HDR 校准应用的三种测试图案（都用眼睛看）",
             fontsize=12.5, fontweight="bold", y=0.975)

axes = [fig.add_subplot(gs[r, c]) for r in range(2) for c in range(2)]


def caption(ax, txt):
    ax.text(0.5, -0.05, txt, transform=ax.transAxes, ha="center", va="top",
            fontsize=7.4, color=H.DARK)


# ---------- 左上：最小亮度 ----------
axA = axes[0]
base = 0.020
Hh, Ww = 128, 160
imgA = np.full((Hh, Ww), base)
vals = np.geomspace(0.035, 0.34, 8)
for i, v in enumerate(vals):
    r, c = divmod(i, 4)
    y0 = 12 + r * 54
    x0 = 10 + c * 37
    imgA[y0:y0 + 34, x0:x0 + 30] = v
axA.imshow(imgA, cmap="gray", vmin=0.0, vmax=1.0, interpolation="nearest",
           aspect="auto")
axA.set_title("① 最小亮度（黑位 / 暗部起始点）", fontsize=10.2, color=H.NAVY)
axA.axis("off")
for i in range(8):
    r, c = divmod(i, 4)
    x0 = 10 + c * 37
    axA.annotate(str(i + 1), xy=(x0 + 15, 50 + r * 54), ha="center", va="center",
                 fontsize=7.2, color="#ffe9a8")
caption(axA, "调到「暗部细节刚好能看见、黑底又足够黑」")

# ---------- 右上：最大亮度 ----------
axB = axes[1]
imgB = np.zeros((Hh, Ww))
imgB[30:86, 52:100] = 0.92            # 约 10% 面积的小窗口白块
axB.imshow(imgB, cmap="gray", vmin=0.0, vmax=1.0, interpolation="nearest",
           aspect="auto")
axB.set_title("② 最大亮度（峰值 / 高光上限）", fontsize=10.2, color=H.ORANGE)
axB.axis("off")
axB.annotate("小窗口白块\n约 10% 面积\n≈ 屏幕峰值亮度", xy=(76, 58),
             xytext=(6, 108), fontsize=7.0, color="#ffe9a8",
             arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=1.2),
             ha="left", va="center", linespacing=1.35)
caption(axB, "调到「最亮处明亮清晰、又不糊成一片」")

# ---------- 左下：最大帧平均亮度 ----------
axC = axes[2]
imgC = np.full((Hh, Ww), 0.93)       # 大面积亮场
imgC[14:52, 12:52] = 0.78
imgC[14:52, 60:100] = 0.86
imgC[66:104, 12:52] = 0.86
imgC[66:104, 60:100] = 0.70
imgC[66:104, 110:148] = 0.88
axC.imshow(imgC, cmap="gray", vmin=0.0, vmax=1.0, interpolation="nearest",
           aspect="auto")
axC.set_title("③ 最大帧平均亮度（大面积亮场）", fontsize=10.2, color=H.TEAL)
axC.axis("off")
axC.text(8, 116, "近全屏白（大面积亮场）", ha="left", va="center",
         fontsize=7.0, color="#5a6a7a")
caption(axC, "调到「整片亮场长时间看着舒服、不刺眼」")

# ---------- 右下：ICC 配置文件 ----------
axD = axes[3]
axD.set_xlim(0, 10); axD.set_ylim(0, 10)
axD.axis("off"); axD.grid(False)
axD.set_title("校准完成 → 生成 ICC 配置文件", fontsize=10.2, color=H.GREEN)

axD.add_patch(FancyBboxPatch((0.35, 0.30), 9.3, 8.55,
                             boxstyle="round,pad=0.05,rounding_size=0.25",
                             facecolor="#f4f7fb", edgecolor=H.NAVY, lw=1.4))
axD.text(5.0, 8.45, "ICC 配置文件（这块屏的「档案」）", ha="center", va="center",
         fontsize=8.6, fontweight="bold", color=H.NAVY)

items = [
    ("白点", "D65（6504K）"),
    ("原色", "红 / 绿 / 蓝 色度坐标"),
    ("亮度", "最小亮度 & 最大亮度"),
    ("EOTF", "PQ / Gamma 特性曲线"),
    ("目标", "让系统准确渲染 HDR 与 SDR"),
]
for i, (k, v) in enumerate(items):
    y = 7.55 - i * 0.92
    axD.text(1.05, y, k, fontsize=7.8, fontweight="bold", color=H.BLUE,
             ha="left", va="center")
    axD.text(3.10, y, v, fontsize=7.6, color=H.DARK, ha="left", va="center")

axD.text(5.0, 1.70, "配合 HGiG：在显示器上关掉「动态增强 / 自动亮度」，\n"
                    "让校准结果真正生效（详见第 17 章）",
         ha="center", va="center", fontsize=6.9, color="#8a5a12",
         linespacing=1.4,
         bbox=dict(boxstyle="round,pad=0.35", fc="#fdf3e3",
                   ec=H.ORANGE, lw=1.0))

H.save(fig, 16, "f3_calib_patterns")
