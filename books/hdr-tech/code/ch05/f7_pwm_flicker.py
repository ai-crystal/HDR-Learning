# -*- coding: utf-8 -*-
"""第 05 章 图 7：PWM 调光的波形与闪烁指标（按定义计算）。

(a) 三种占空比的 PWM 波形，分三行画。周期取 1 ms（对应 1 kHz 调光频率），
    高电平归一化为 1，低电平为 0。占空比越低，亮的时间越短、平均亮度越低，
    但瞬时峰值不变。
(b) 方波的闪烁指数与平均亮度随占空比的变化。闪烁指数（flicker index，
    IES 定义）= 一个周期内高出平均值的面积 / 总面积，方波时等于 1 - d；
    平均亮度等于 d。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

T = 1.0
t = np.linspace(0, 2 * T, 4001)

fig = plt.figure(figsize=(7.6, 4.2))
gs = fig.add_gridspec(3, 2, width_ratios=[1.0, 1.1],
                      hspace=0.30, wspace=0.30,
                      left=0.09, right=0.98, top=0.90, bottom=0.14)

rows = [(0.10, H.RED), (0.25, H.ORANGE), (0.50, H.TEAL)]
axes_a = []
for i, (d, color) in enumerate(rows):
    ax = fig.add_subplot(gs[i, 0])
    y = ((t % T) < d * T).astype(float)
    ax.plot(t, y, color=color, lw=1.8)
    ax.set_xlim(0, 2)
    ax.set_ylim(-0.12, 1.18)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["关", "开"], fontsize=8)
    ax.set_xticks([0, 0.5, 1.0, 1.5, 2.0])
    if i < 2:
        ax.set_xticklabels([])
    else:
        ax.set_xlabel("时间（毫秒，调光频率 1 kHz）")
    ax.text(0.985, 0.72, f"占空比 {int(d*100)}%", fontsize=8.0, color=color,
            va="top", ha="right", transform=ax.transAxes)
    axes_a.append(ax)

fig.text(0.015, 0.52, "瞬时亮度", rotation=90, va="center", fontsize=10)
fig.text(0.30, 0.955, "(a) PWM 波形", ha="center", fontsize=10)

ax2 = fig.add_subplot(gs[:, 1])
d = np.linspace(0.01, 1.0, 400)
ax2.plot(d * 100, 1 - d, color=H.RED, lw=2.1, label="闪烁指数（1 - d）")
ax2.plot(d * 100, d, color=H.NAVY, lw=2.1, label="平均亮度（d × 峰值）")
ax2.axvline(10, color=H.GRAY, lw=0.9, ls=":")
ax2.text(44, 0.035, "10% 占空比：平均亮度只有\n峰值的 1/10，闪烁指数 0.9", fontsize=7.8,
         color=H.GRAY, va="bottom")
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 1.05)
ax2.set_xlabel("占空比（%）")
ax2.set_ylabel("比例")
ax2.legend(loc="upper center", fontsize=8.0, labelspacing=0.3, borderpad=0.4)
ax2.set_title("(b) 闪烁与亮度", fontsize=10, pad=6)

H.save(fig, 5, "f7_pwm_flicker")
