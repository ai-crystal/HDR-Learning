# -*- coding: utf-8 -*-
"""第 04 章 图 3：BT.2390 EETF 的高光压缩曲线（按推荐书公式计算）。

EETF 单通道形式（PQ 码值域 0..1）：
    KS = 1.5 * maxLum - 0.5
    t  = (E1 - KS) / (1 - KS)                       E1 >= KS
    E3 = P0(2t^3-3t^2+1) + T0(t^3-2t^2+t)
         + P1(-2t^3+3t^2) + T1(t^3-t^2)
    P0 = KS, T0 = 1-KS（与线性段斜率连续）, P1 = maxLum, T1 = 0（峰值处斜率收敛）
    E1 < KS 时 E3 = E1（黑位到拐点不做处理）
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt


def eetf_code(e1, max_lum):
    """e1、max_lum 均为 PQ 码值 0..1，返回压缩后的 PQ 码值。"""
    e1 = np.asarray(e1, dtype=float)
    ks = 1.5 * max_lum - 0.5
    t = np.clip((e1 - ks) / (1.0 - ks), 0.0, 1.0)
    p0, t0, p1, t1 = ks, 1.0 - ks, max_lum, 0.0
    h = (p0 * (2 * t ** 3 - 3 * t ** 2 + 1)
         + t0 * (t ** 3 - 2 * t ** 2 + t)
         + p1 * (-2 * t ** 3 + 3 * t ** 2)
         + t1 * (t ** 3 - t ** 2))
    return np.where(e1 < ks, e1, h)


def eetf_nit(nit_in, target_nit):
    return H.pq_eotf(eetf_code(H.pq_oetf(nit_in), H.pq_oetf(target_nit)))


nit = np.logspace(np.log10(0.005), 4.0, 1200)

fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.plot(nit, nit, color=H.LGRAY, lw=1.6, ls=(0, (4, 2)), label="恒等（不做映射）")

colors = [H.NAVY, H.TEAL, H.ORANGE, H.RED]
targets = [100, 300, 600, 1000]
for c, tgt in zip(colors, targets):
    ax.plot(nit, eetf_nit(nit, tgt), color=c, lw=2.1, label=f"目标峰值 {tgt} nit")

# 标注 1000 nit 曲线的拐点
ks = 1.5 * float(H.pq_oetf(1000)) - 0.5
ks_nit = float(H.pq_eotf(ks))
ax.plot([ks_nit], [ks_nit], marker="o", ms=5.5, color=H.RED, mec="white", mew=1.0, zorder=5)
ax.annotate("拐点 $K_S$（316 nit）\n此处曲率开始下降", xy=(ks_nit, ks_nit),
            xytext=(1.5, 950), fontsize=8.5, color=H.RED,
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.0,
                            connectionstyle="arc3,rad=0.28"))

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.005, 1.2e4)
ax.set_ylim(0.005, 1.2e4)
ax.set_xlabel("输入亮度（nit，对数刻度）")
ax.set_ylabel("输出亮度（nit，对数刻度）")
ax.legend(loc="upper left", fontsize=8.5)
tick = [0.01, 0.1, 1, 10, 100, 1000, 10000]
lab = ["0.01", "0.1", "1", "10", "100", "1000", "10000"]
ax.set_xticks(tick); ax.set_xticklabels(lab)
ax.set_yticks(tick); ax.set_yticklabels(lab)
ax.minorticks_off()
H.save(fig, 4, "f3_bt2390_eetf")
