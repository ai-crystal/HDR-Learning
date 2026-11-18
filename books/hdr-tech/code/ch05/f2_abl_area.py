# -*- coding: utf-8 -*-
"""第 05 章 图 2：峰值亮度随亮场面积变化的示意曲线（模型计算，非厂商实测数据）。

模型：P(A) = clip(K / A, P_full, P_peak)，A 为亮场面积占比，K 为面板可分配的
总光通量常数（单位 nit），P_full 为全屏白亮度，P_peak 为小面积峰值。
该式只描述"总能量守恒 + 两个端点上限"这一最简关系，不包含热与时间因素。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

A = np.logspace(np.log10(1.0), 2.0, 600)          # 亮场面积占比 %
F = A / 100.0


def abl(peak, k, full):
    return np.clip(k / F, full, peak)


oled = abl(1000.0, 70.0, 140.0)      # 自发光：峰值 1000 nit，全屏白 140 nit
miniled = abl(2000.0, 200.0, 700.0)  # 分区背光：峰值 2000 nit，全屏白 700 nit

fig, ax = plt.subplots(figsize=(7.2, 4.3))
ax.plot(A, oled, color=H.PURPLE, lw=2.3, label="自发光面板（峰值 1000 nit，全屏白 140 nit）")
ax.plot(A, miniled, color=H.TEAL, lw=2.3, label="分区背光液晶（峰值 2000 nit，全屏白 700 nit）")

ax.axvline(10.0, color=H.GRAY, lw=1.0, ls=":")

ax.set_xscale("log")
ax.set_xlim(1, 100)
ax.set_ylim(0, 2650)
ax.set_xticks([1, 2, 5, 10, 20, 50, 100])
ax.set_xticklabels(["1", "2", "5", "10", "20", "50", "100"])
ax.minorticks_off()
ax.set_xlabel("亮场面积占全屏的比例（%，对数刻度）")
ax.set_ylabel("可维持的峰值亮度（nit）")
ax.legend(loc="upper right", fontsize=8.5)
H.save(fig, 5, "f2_abl_area")
