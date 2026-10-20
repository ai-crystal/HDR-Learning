# -*- coding: utf-8 -*-
"""f2_frc：8bit + FRC 抖动示意——时间上交替显示相邻两级，平均出中间灰。"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np

A_CODE, B_CODE = 100.0, 101.0        # 8bit 相邻两级
A_GRAY, B_GRAY = 80, 175             # 示意放大后的灰度（实际级差仅 1/255）
AVG_GRAY = int(round((A_GRAY + B_GRAY) / 2))

fig = H.plt.figure(figsize=(7.2, 4.3))
gs = fig.add_gridspec(2, 6, height_ratios=[0.9, 1.4], hspace=0.85, wspace=0.62,
                      left=0.05, right=0.97, top=0.86, bottom=0.10)

# ---- 上排：连续 6 帧，蓝/橙交替 ----
nframes = 6
for i in range(nframes):
    ax = fig.add_subplot(gs[0, i])
    isA = (i % 2 == 0)
    g = A_GRAY if isA else B_GRAY
    col = H.BLUE if isA else H.ORANGE
    code = int(A_CODE) if isA else int(B_CODE)
    ax.imshow(np.full((4, 4), g), cmap="gray", vmin=0, vmax=255,
              extent=[0, 1, 0, 1], interpolation="nearest")
    for s in ax.spines.values():
        s.set_edgecolor(col); s.set_linewidth(2.2)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"第{i+1}帧", fontsize=8.5, color=col, pad=2)
    ax.text(0.5, -0.22, f"码值 {code}", transform=ax.transAxes, ha="center",
            va="top", fontsize=8.5, color=col, fontweight="bold")

fig.text(0.5, 0.925,
         "8bit 只有相邻两级 → 每帧在两级间快速轮流刷新（FRC）",
         ha="center", va="center", fontsize=9.5, color=H.NAVY, fontweight="bold")
fig.text(0.5, 0.885, "（示意：灰度差已放大，实际相邻级差仅 1/256）",
         ha="center", va="center", fontsize=8, color=H.GRAY)

# ---- 左下：码值刻度示意 ----
axl = fig.add_subplot(gs[1, 0:3])
axl.set_xlim(0, 1); axl.set_ylim(99.4, 101.6)
axl.axhline(A_CODE, color=H.BLUE, lw=2.5)
axl.axhline(B_CODE, color=H.ORANGE, lw=2.5)
axl.axhline(100.5, color=H.GREEN, lw=2.2, ls="--")
axl.text(1.03, A_CODE, " 8bit 级 100", color=H.BLUE, fontsize=8.5, va="center")
axl.text(1.03, B_CODE, " 8bit 级 101", color=H.ORANGE, fontsize=8.5, va="center")
axl.text(1.03, 100.5, " 10bit 级\n 100.5", color=H.GREEN, fontsize=8.5,
         va="center", fontweight="bold")
axl.set_xlim(0, 1); axl.set_xticks([])
axl.set_ylabel("码值", fontsize=9.5)
axl.set_title("真 10bit 有中间级；8bit 没有", fontsize=10, color=H.NAVY, loc="left", pad=6)
axl.grid(False)

# ---- 右下：人眼平均后的观感 ----
axr = fig.add_subplot(gs[1, 3:6])
axr.imshow(np.full((4, 4), AVG_GRAY), cmap="gray", vmin=0, vmax=255,
           extent=[0, 1, 0, 1], interpolation="nearest")
for s in axr.spines.values():
    s.set_edgecolor(H.GREEN); s.set_linewidth(2.4)
axr.set_xticks([]); axr.set_yticks([])
axr.set_title("人眼视觉暂留 → 平均观感", fontsize=10, color=H.GREEN,
              loc="left", pad=6)
axr.text(0.5, -0.16, "≈ 码值 100.5 的中间灰", transform=axr.transAxes,
         ha="center", va="top", fontsize=9.5, color=H.GREEN, fontweight="bold")
axr.text(0.5, -0.34, "8bit+FRC ≠ 真 10bit：中间色是「骗」出来的",
         transform=axr.transAxes, ha="center", va="top", fontsize=8.8, color=H.RED)

fig.suptitle("图 10-2　8bit + FRC：靠时间交替「拼」出中间灰",
             fontsize=13, fontweight="bold", y=1.0)
H.save(fig, 10, "f2_frc")
