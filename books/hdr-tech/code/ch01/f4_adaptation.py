# -*- coding: utf-8 -*-
"""图 1-4：暗适应与明适应的时间过程。

(a) 暗适应按两分支模型计算：视锥分支快速下降后在约 0.05 cd/m² 处形成平台，
    视杆分支以近似恒定的对数斜率继续下降，两者中较低的一支决定任意时刻的阈值
    （即“视杆—视锥转折”）。转折时间、平台高度与最终阈值取自经典暗适应测量
    所描述的形状，属模型近似，不是实测点。
(b) 明适应按两个指数项叠加：快相约 0.3 s，慢相约 10 s，纵轴为相对稳态阈值的倍数。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import FuncFormatter, NullFormatter
plt.rcParams["mathtext.fontset"] = "dejavusans"


def dec(v):
    s = f"{v:.0e}"
    return s.replace("e+0", "e").replace("e+", "e").replace("e-0", "e-")


def plain(ax, which="xy"):
    for a in which:
        ax_ = ax.xaxis if a == "x" else ax.yaxis
        ax_.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
        ax_.set_minor_formatter(NullFormatter())


fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(8.8, 3.9), gridspec_kw={"width_ratios": [1.3, 1.0]})
fig.subplots_adjust(left=0.082, right=0.985, bottom=0.155, top=0.94, wspace=0.30)

# ---------- (a) 暗适应 ----------
t = np.linspace(0, 35, 700)
cone = 10 ** (2.0 - 3.30 * (1.0 - np.exp(-t / 1.3)))
rod = 10 ** (0.41 - 0.214 * t)
thr = np.minimum(cone, rod)

i = np.argmin(np.abs(cone - rod))
t_break = t[i]

ax1.semilogy(t, cone, color=H.TEAL, lw=1.9, ls=(0, (5, 2)),
             label="视锥分支（快，约 6 min 到位）")
ax1.semilogy(t, rod, color=H.PURPLE, lw=1.9, ls=(0, (1.4, 1.6)),
             label="视杆分支（慢，约 30 min 到位）")
ax1.semilogy(t, thr, color=H.NAVY, lw=2.4, label="实际阈值（两支取低）")

ax1.axhline(1e-6, color=H.GRAY, lw=0.9, ls=":")
ax1.text(34.6, 1.6e-6, "视杆绝对阈值 $10^{-6}$", fontsize=7.8, color=H.GRAY,
         ha="right", va="bottom")
ax1.axvline(t_break, color=H.RED, lw=0.9, ls=(0, (3, 3)))
ax1.annotate("视杆—视锥转折\n约 %.0f min" % t_break, xy=(t_break, cone[i]),
             xytext=(4.2, 1.35), fontsize=8.2, color=H.DARK,
             arrowprops=dict(arrowstyle="->", color=H.DARK, lw=0.9,
                             shrinkA=2, shrinkB=3))
ax1.annotate("视锥平台", xy=(11.0, 0.052), xytext=(19.0, 0.005),
             fontsize=8.2, color=H.TEAL,
             arrowprops=dict(arrowstyle="->", color=H.TEAL, lw=0.9,
                             shrinkA=2, shrinkB=3))

ax1.set_xlim(0, 35)
ax1.set_ylim(5e-7, 4e2)
ax1.set_xticks([0, 5, 10, 15, 20, 25, 30, 35])
ax1.set_yticks([1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100])
ax1.yaxis.set_major_formatter(FuncFormatter(lambda v, p: dec(v)))
ax1.yaxis.set_minor_formatter(NullFormatter())
ax1.set_xlabel("进入暗室后的时间（min）")
ax1.set_ylabel("可觉察的阈值亮度（cd/m$^2$）")
ax1.legend(loc="upper right", fontsize=7.8, handlelength=2.4,
           borderpad=0.45, labelspacing=0.35)
ax1.text(0.03, 0.955, "(a)", transform=ax1.transAxes,
         ha="left", va="top", fontsize=10, color=H.DARK)

# ---------- (b) 明适应 ----------
tt = np.logspace(-2, 2, 600)
resp = 1.0 + 150.0 * np.exp(-tt / 0.3) + 15.0 * np.exp(-tt / 10.0)
ax2.loglog(tt, resp, color=H.ORANGE, lw=2.4)
ax2.axhline(1.0, color=H.GRAY, lw=0.9, ls=":")
ax2.text(1.35, 1.06, "稳态阈值", fontsize=7.8, color=H.GRAY,
         ha="left", va="bottom")

ax2.annotate("快相\n瞳孔收缩与光化学复位\n$\\tau\\approx0.3$ s",
             xy=(0.28, 1 + 150 * np.exp(-0.28 / 0.3)),
             xytext=(0.0108, 1.5), fontsize=7.8, color=H.DARK,
             arrowprops=dict(arrowstyle="->", color=H.DARK, lw=0.9,
                             shrinkA=2, shrinkB=3))
ax2.annotate("慢相\n神经增益重设\n$\\tau\\approx10$ s",
             xy=(11.0, 1 + 15 * np.exp(-1.1)), xytext=(1.6, 200),
             fontsize=7.8, color=H.DARK,
             arrowprops=dict(arrowstyle="->", color=H.DARK, lw=0.9,
                             shrinkA=2, shrinkB=3))

ax2.set_xlim(1e-2, 1e2)
ax2.set_ylim(0.9, 800)
ax2.set_xticks([0.01, 0.1, 1, 10, 100])
ax2.set_yticks([1, 3, 10, 30, 100, 300])
plain(ax2)
ax2.set_xlabel("背景亮度阶跃后的时间（s）")
ax2.set_ylabel("阈值相对稳态的倍数")
ax2.text(0.03, 0.955, "(b)", transform=ax2.transAxes,
         ha="left", va="top", fontsize=10, color=H.DARK)

H.save(fig, 1, "f4_adaptation")
