# -*- coding: utf-8 -*-
"""第 06 章 图 6：一条 HDR 显示链路的 EOTF 跟踪与校准前后色差。

器件模型：峰值 1000 cd/m²、黑位 0.05 cd/m²、未校准时逐通道伽马 2.2；
目标为 ST 2084 的 PQ EOTF（1000 cd/m² 以下）。校准用一维查找表把输出
拉回 PQ 曲线，再按 21 级灰阶统计 ΔE_ITP。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import ictcp as I

plt = H.plt

PEAK, BLACK = 1000.0, 0.05
CODE_MAX = float(I.pq_oetf(PEAK))


def target(code):
    return I.pq_eotf(np.asarray(code, dtype=float))


def uncal(code):
    return BLACK + (PEAK - BLACK) * np.asarray(code) ** 2.2


def calibrated(code):
    """一维 LUT 校准：输入码值直接驱动到目标亮度。"""
    t = np.clip(np.asarray(code) / CODE_MAX, 0.0, 1.0)
    return BLACK + (target(t * CODE_MAX) - BLACK)


codes = np.linspace(0.0, CODE_MAX, 260)
fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.85),
                         gridspec_kw=dict(width_ratios=[1.10, 1.0], wspace=0.30))
fig.subplots_adjust(left=0.085, right=0.985, top=0.90, bottom=0.165)

ax = axes[0]
ax.plot(codes, target(codes), color="#8a97a6", lw=3.2,
        label="目标：ST 2084 的 PQ")
ax.plot(codes, uncal(codes), color=H.RED, lw=1.9, label="校准前（伽马 2.2）")
ax.plot(codes, calibrated(codes), color=H.TEAL, lw=1.6, ls=(0, (5, 2)),
        label="校准后（一维 LUT）")
ax.axhline(PEAK, color="#c2cad4", lw=0.9, ls=(0, (3, 3)))
ax.text(0.02, PEAK * 1.15, "显示峰值 1000 cd/m$^2$", fontsize=7.4, color="#6b7886")
ax.axhline(203, color="#c2cad4", lw=0.9, ls=(0, (3, 3)))
ax.text(0.02, 203 * 1.15, "漫反射白 203 cd/m$^2$", fontsize=7.4, color="#6b7886")
ax.set_yscale("log")
ax.set_xlim(0, 0.80)
ax.set_ylim(0.02, 2200)
ax.set_xlabel("PQ 输入码值", fontsize=9.5)
ax.set_ylabel("显示亮度（cd/m$^2$）", fontsize=9.5)
ax.legend(loc="lower right", fontsize=7.6, handletextpad=0.6, borderpad=0.35)
ax.annotate("暗部抬起，中段偏高", xy=(0.16, uncal(0.16)), xytext=(0.24, 7.5),
            fontsize=7.4, color=H.RED,
            arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=0.9,
                            shrinkA=2, shrinkB=3))

# ---------------- (b) 21 级灰阶的色差 ----------------
ax2 = axes[1]
lv = np.linspace(0.0, 1.0, 21)
cc = lv * CODE_MAX
meas_before = uncal(cc)
meas_after = calibrated(cc)
tgt = target(cc)


def to_ictcp(Y):
    q = np.asarray(Y) / 10000.0
    code = I.pq_oetf(np.asarray(Y))
    return I.rgb_lin_to_ictcp(np.stack([np.asarray(Y) / 10000.0] * 3, axis=-1), peak=10000.0)


d_before = I.deltaE_ITP(to_ictcp(meas_before), to_ictcp(tgt))
d_after = I.deltaE_ITP(to_ictcp(np.maximum(meas_after, 1e-6)), to_ictcp(tgt))

idx = np.arange(len(lv))
ax2.bar(idx - 0.2, d_before, width=0.38, color=H.RED, label="校准前")
ax2.bar(idx + 0.2, d_after, width=0.38, color=H.TEAL, label="校准后")
ax2.set_yscale("log")
ax2.set_ylim(0.02, 1500)
ax2.set_xticks(idx[::2])
ax2.set_xticklabels([f"{v * 100:.0f}" for v in lv[::2]], fontsize=7.6)
ax2.set_xlabel("灰阶输入（%，满量程 1000 cd/m$^2$）", fontsize=9.5)
ax2.set_ylabel("与目标曲线的 $\\Delta E_{ITP}$", fontsize=9.5)
ax2.legend(loc="lower left", fontsize=7.8, handletextpad=0.5, borderpad=0.35)
ax2.grid(axis="x", visible=False)
ax2.annotate("低灰阶误差最大", xy=(2.4, d_before[2]), xytext=(6.5, 420),
             fontsize=7.4, color=H.RED,
             arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=0.9,
                             shrinkA=2, shrinkB=4))

ax2.text(20.2, 0.45, f"校准后各点均不超过 {d_after.max():.2f}", fontsize=7.4,
         color="#0f5f50", ha="right", va="bottom")
print("before max", d_before.max(), "median", np.median(d_before))
print("after max", d_after.max())
print("luminance at code 0.1, 0.5:", float(target(0.1)), float(target(0.5)))
print("uncal at 0.1,0.5:", float(uncal(0.1)), float(uncal(0.5)))

H.save(fig, 6, "f6_eotf_tracking")
