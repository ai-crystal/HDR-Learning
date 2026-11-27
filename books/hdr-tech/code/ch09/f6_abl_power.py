# -*- coding: utf-8 -*-
"""第 09 章 图 6：峰值亮度与屏幕功耗随平均图像电平的变化（模型示意）。

峰值模型：P(APL) = clip(K / APL, P_full, P_peak)，K 为可分配的总光通量常数。
功耗模型：W(APL) = 0.3 + 0.7 * APL/100，即与发光面积近似线性，不含驱动与散热的非线性。
两个端点取值参照公开评测的常见量级，不是任何一台具体机型的数据。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

APL = np.linspace(1, 100, 500)
P_PEAK, P_FULL, K = 1400.0, 450.0, 14000.0

peak = np.clip(K / APL, P_FULL, P_PEAK)
power = 0.30 + 0.70 * APL / 100.0

fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.plot(APL, peak, color=H.ORANGE, lw=2.4, label="可维持的峰值亮度")
ax.set_xlabel("平均图像电平 APL（%，全黑为 0，全白为 100）")
ax.set_ylabel("峰值亮度（nit）", color=H.ORANGE)
ax.tick_params(axis="y", colors=H.ORANGE)
ax.set_ylim(0, 1600)
ax.set_xlim(0, 100)

ax2 = ax.twinx()
ax2.plot(APL, power, color=H.NAVY, lw=2.0, ls="--", label="屏幕相对功耗")
ax2.set_ylabel("屏幕功耗（相对全白功耗）", color=H.NAVY)
ax2.tick_params(axis="y", colors=H.NAVY)
ax2.set_ylim(0, 1.15)
ax2.grid(False)

ax.axvline(10, color=H.GRAY, lw=1.0, ls=":")
ax.text(11.5, 640, "拐点 10%", fontsize=8.2, color=H.GRAY)
ax.axvline(31, color=H.GRAY, lw=1.0, ls=":")
ax.text(36, 290, "全屏白托底 450 nit", fontsize=8.2, color=H.GRAY)

lines = ax.get_lines()[:1] + ax2.get_lines()[:1]
ax.legend(lines, [l.get_label() for l in lines], loc="upper right",
          fontsize=8.6)

H.save(fig, 9, "f6_abl_power")
