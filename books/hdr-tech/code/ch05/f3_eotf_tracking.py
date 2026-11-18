# -*- coding: utf-8 -*-
"""第 05 章 图 3：EOTF 跟踪误差（按公式计算的模型对比）。

误差用 BT.2124 的 ΔE_ITP 定义，这里只取亮度分量并保留符号：
    ΔE_ITP(带符号) ≈ 720 × ( PQ(实测亮度) − PQ(目标亮度) )
正值表示画面对应码值偏亮，负值偏暗。三种情形：
  A. 把 PQ 信号按 gamma 2.2 解码，显示峰值 700 nit；
  B. 把 PQ 信号按 BT.1886（gamma 2.4）解码，显示峰值 1000 nit；
  C. 经 3D LUT 校正后残留 ±3% 的平滑亮度误差（校正残差模型，非实测数据）。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

code = np.arange(0, 1024)
v = code / 1023.0
target = H.pq_eotf(v)

L_a = 700.0 * v ** 2.2
L_b = 1000.0 * v ** 2.4
resid = 1.0 + 0.03 * np.sin(2 * np.pi * (1.2 * v + 0.15))
L_c = np.maximum(target * resid, 1e-6)


def de_signed(L_meas):
    return 720.0 * (H.pq_oetf(L_meas) - v)


fig, ax = plt.subplots(figsize=(7.4, 4.4))
ax.axhspan(-1, 1, color="#c8d2dc", alpha=0.45, lw=0, label="±1 ΔE_ITP（可察觉门槛）")
ax.plot(code, de_signed(L_a), color=H.RED, lw=2.0, label="A：按 gamma 2.2 解码（峰值 700 nit）")
ax.plot(code, de_signed(L_b), color=H.ORANGE, lw=2.0, label="B：按 gamma 2.4 解码（峰值 1000 nit）")
ax.plot(code, de_signed(L_c), color=H.TEAL, lw=2.2, label="C：3D LUT 校正后残差 ±3%")

ax.set_yscale("symlog", linthresh=1.0, linscale=0.6)
ax.set_xlim(0, 1023)
ax.set_ylim(-2000, 2000)
ax.set_yticks([-1000, -100, -10, -1, 0, 1, 10, 100, 1000])
ax.set_yticklabels(["-1000", "-100", "-10", "-1", "0", "1", "10", "100", "1000"])
ax.minorticks_off()
ax.set_xlabel("10 位码值")
ax.set_ylabel("亮度码值误差（ΔE_ITP，正值为偏亮）")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2,
          fontsize=8.5, frameon=False)

ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim())
ax2.set_xticks([520, 594, 769])
ax2.set_xticklabels(["100 nit", "203 nit", "1000 nit"], fontsize=8.5)
ax2.minorticks_off()
labs = ax2.get_xticklabels()
for i, ha in enumerate(["right", "center", "left"]):
    labs[i].set_ha(ha)
ax2.set_xlabel("对应的绝对亮度", fontsize=9.5)

H.save(fig, 5, "f3_eotf_tracking")
