# -*- coding: utf-8 -*-
"""图 19-2　校准流程：校色仪 → 软件 → ICC/LUT → 系统应用。

左图用纵向流程给出权威校准的六个步骤（测量 → 计算 → 应用）；
右图用曲线说明「校准在做什么」：实测的显示 EOTF 偏离目标 γ2.2，
软件据此算出一条修正系数曲线（LUT），把屏幕拉回标准。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, (axL, axR) = plt.subplots(
    1, 2, figsize=(7.2, 4.8), gridspec_kw={"width_ratios": [1.05, 1.0]})

# ================= 左：校准流程 =================
axL.set_xlim(0, 6); axL.set_ylim(0, 10.4)
axL.axis("off"); axL.grid(False)
axL.set_title("校准流程：把屏幕拉回标准", pad=8, fontsize=11.5)

steps = [
    (H.NAVY,   "① 校色仪贴在屏幕上", "把标准的“尺子”架上"),
    (H.BLUE,   "② 校准软件投放测试图案", "灰阶 + 色块"),
    (H.TEAL,   "③ 仪器测量实际输出", "读亮度 / 色度"),
    (H.ORANGE, "④ 软件算出偏差曲线", "目标 vs 实测"),
    (H.PURPLE, "⑤ 生成 ICC 配置文件 / 3D LUT", "得到修正“处方”"),
    (H.GREEN,  "⑥ 系统 / 显示器加载并应用", "屏幕颜色被修正"),
]
BW, BH, GAP, CX = 5.0, 1.14, 0.46, 3.0
top = 9.9


def box(ax, x, y, w, h, fc, ec, radius=0.10, lw=1.3, z=3):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0.02,rounding_size={radius}",
                       linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z)
    ax.add_patch(p)
    return p


for i, (c, title, note) in enumerate(steps):
    y = top - (i + 1) * BH - i * GAP
    box(axL, CX - BW / 2, y, BW, BH, c, c, radius=0.12)
    axL.text(CX, y + BH * 0.63, title, ha="center", va="center", color="white",
             fontsize=9.6, fontweight="bold", zorder=4)
    axL.text(CX, y + BH * 0.26, note, ha="center", va="center", color="white",
             fontsize=8.0, alpha=0.9, zorder=4)
    if i < len(steps) - 1:
        axL.add_patch(FancyArrowPatch(
            (CX, y), (CX, y - GAP), arrowstyle="-|>", mutation_scale=14,
            linewidth=1.8, color=H.DARK, zorder=2))

axL.text(CX, 0.34, "工具：校色仪（X-Rite / Calibrite / Datacolor）\n软件：DisplayCAL · Calman",
         ha="center", va="center", fontsize=6.8, color=H.GRAY,
         linespacing=1.5)

# ================= 右：校准在做什么 =================
code = np.linspace(0, 1, 256)
target = code ** 2.2                                  # 目标 EOTF（γ2.2）
measured = 0.020 + 0.980 * code ** 2.34               # 实测：偏暗 + 抬黑
corr = target / np.maximum(measured, 1e-6)            # 修正系数（LUT）

axR.plot(code, target, "--", color=H.NAVY, lw=1.8, label="目标 EOTF（γ2.2）")
axR.plot(code, measured, "-", color=H.ORANGE, lw=2.2, label="实测（γ≈2.34）")
axR.fill_between(code, target, measured, color=H.ORANGE, alpha=0.12, zorder=1)
axR.annotate("偏差", xy=(0.72, (0.72 ** 2.2 + 0.02 + 0.98 * 0.72 ** 2.34) / 2),
             xytext=(0.60, 0.42), fontsize=8.5, color=H.ORANGE,
             fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=1.1))

ax2 = axR.twinx()
ax2.plot(code, corr, "-", color=H.GREEN, lw=2.0, label="修正系数（→ LUT）")
ax2.set_ylabel("修正系数", color=H.GREEN, fontsize=9.5)
ax2.tick_params(axis="y", colors=H.GREEN)
ax2.grid(False)
ax2.set_ylim(0, 1.6)

axR.set_xlim(0, 1); axR.set_ylim(0, 1.05)
axR.set_xlabel("输入码值")
axR.set_ylabel("相对输出亮度")
axR.set_title("校准在做什么：测偏差 → 生成修正曲线", pad=8, fontsize=11.5)

h1, l1 = axR.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
axR.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8)

fig.suptitle("没有尺子就只能靠眼睛——校准必须“仪器测量 + 软件修正”", fontsize=12,
             fontweight="bold", y=1.035)
H.save(fig, 19, "f2_calib_flow")
