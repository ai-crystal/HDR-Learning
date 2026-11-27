# -*- coding: utf-8 -*-
"""图 8-3 自动曝光的适应曲线：引擎的一阶近似与人眼真实的时间尺度。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("hdr-tech")
import numpy as np
from matplotlib.ticker import FuncFormatter

plt = H.plt

fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.2))
ax1, ax2 = axes

# ---------- 左：亮度阶跃后曝光增益的收敛 ----------
step_ev = np.log2(1000.0 / 100.0)
t = np.linspace(0, 7, 600)
for rate, col in [(1.0, H.BLUE), (2.0, H.TEAL), (4.0, H.ORANGE)]:
    tau = step_ev / rate
    gain_ev = -step_ev * (1 - np.exp(-t / tau))
    ax1.plot(t, gain_ev, color=col, lw=2.0, label=f"{rate:g} EV/s")
    t95 = tau * np.log(20.0)
    if t95 < 7:
        ax1.plot([t95], [-step_ev * 0.95], "o", ms=4.5, color=col, zorder=5)

ax1.axhline(-step_ev, color=H.GRAY, lw=0.9, ls=":")
ax1.text(0.15, -step_ev + 0.10, f"目标 {step_ev:.2f} EV", ha="left", va="bottom",
         fontsize=7.8, color=H.GRAY)
ax1.set_xlim(0, 7)
ax1.set_ylim(-4.2, 0.85)
ax1.set_xlabel("阶跃后的时间（s）")
ax1.set_ylabel("曝光增益的变化（EV）")
ax1.set_title("(a) 场景由 100 nit 跳到 1000 nit 之后的收敛", fontsize=9.6, pad=8)
ax1.legend(loc="upper right", fontsize=8, title="引擎里设的速率",
           title_fontsize=8, ncol=3, columnspacing=1.0, handlelength=1.6)
ax1.text(0.03, 0.06, "圆点为 95% 收敛时刻", transform=ax1.transAxes,
         fontsize=7.6, color=H.GRAY)

# ---------- 右：人眼暗适应的时间尺度 ----------
tt = np.logspace(0, 3.5, 900)            # 1 s 到约 3160 s
cone = -2.6 * (1 - np.exp(-tt / 95.0))
rod = -3.4 * (1 - np.exp(-np.maximum(tt - 210.0, 0) / 420.0))
total = cone + rod

ax2.semilogx(tt, cone, color=H.TEAL, lw=1.5, ls="--", label="锥体主导")
ax2.semilogx(tt, rod + cone[0], color=H.NAVY, lw=1.5, ls="--", label="杆体接续的增量")
ax2.semilogx(tt, total, color=H.RED, lw=2.3, label="阈值合计")
ax2.set_xlim(1, 3300)
ax2.set_ylim(-6.6, 0.5)
ax2.set_xlabel("进入暗环境后的时间（s）")
ax2.set_ylabel("阈值相对明适应状态的变化（log 单位）")
ax2.set_title("(b) 人眼暗适应的两个阶段", fontsize=9.6, pad=8)

for xv, lab in ((300, "5 min"), (1500, "25 min")):
    ax2.axvline(xv, color="#ccd5de", lw=0.9, ls=":")
    ax2.text(xv, -6.48, lab, ha="center", va="bottom", fontsize=7.6, color=H.GRAY)
ax2.annotate("锥体平台", xy=(260, -2.45), xytext=(40, -1.55),
             fontsize=7.8, color=H.TEAL,
             arrowprops=dict(arrowstyle="-|>", color=H.TEAL, lw=1.0))
ax2.annotate("杆体平台", xy=(2300, -5.85), xytext=(700, -4.55),
             fontsize=7.8, color=H.NAVY,
             arrowprops=dict(arrowstyle="-|>", color=H.NAVY, lw=1.0))
ax2.legend(loc="lower left", fontsize=7.8)
ax2.text(0.025, 0.30, "曲线形状为示意", transform=ax2.transAxes,
         fontsize=7.4, color=H.GRAY)
ax2.xaxis.set_major_formatter(FuncFormatter(
    lambda v, p: f"{v:g}" if v < 1000 else f"{v/1000:g}k"))

fig.subplots_adjust(wspace=0.32)
H.save(fig, 8, "f3_adaptation")
