# -*- coding: utf-8 -*-
"""第 10 章 图 3：直播 HDR 的曝光锚点。

横轴是场景反射率（对数），纵轴是 HLG 信号。按 BT.2408 的做法，90% 反射白卡
对准 75% 信号，反解出 HLG OETF 的输入 E = 0.265 对应 90% 反射率，
任何反射率 r 的信号为 hlg_oetf(0.265 r / 0.9)。
(a) 信号与反射率的对应，另画一条收一档曝光的曲线作对照。
(b) 同一信号在 1000 cd/m² 显示上按 OOTF 得到的亮度，标出 203 与削波区。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

E90 = 0.265          # 90% 反射白对应的 OETF 输入（由 75% 信号反解）
LW = 1000.0
GAMMA = 1.2

r = np.logspace(np.log10(0.005), np.log10(30.0), 900)
E = E90 * r / 0.9
sig = H.hlg_oetf(E)
sig_low = H.hlg_oetf(E * 0.5)

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(9.0, 4.3), gridspec_kw={"width_ratios": [1.1, 1.0]})
fig.subplots_adjust(left=0.085, right=0.975, bottom=0.145, top=0.955, wspace=0.30)

# ---------------- (a) ----------------
ax1.axvspan(3.4, 30, color=H.RED, alpha=0.07, zorder=0)
ax1.plot(r, sig * 100, color=H.NAVY, lw=2.6, zorder=4)
ax1.plot(r, sig_low * 100, color=H.TEAL, lw=1.8, ls=(0, (5, 2)), zorder=3)
ax1.axhline(75, color=H.GRAY, lw=0.9, ls=(0, (4, 3)), zorder=1)

marks = [(0.18, "18% 灰　40%", (0.0078, 33), "left"),
         (0.90, "90% 白　75%", (1.07, 63), "left")]
for rr, lab, (tx, ty), ha in marks:
    s = float(H.hlg_oetf(E90 * rr / 0.9)) * 100
    ax1.plot([rr], [s], "o", ms=6, color=H.NAVY, mec="white", mew=1.0, zorder=6)
    ax1.annotate(lab, xy=(rr, s), xytext=(tx, ty), fontsize=8.2, color=H.NAVY,
                 ha=ha, va="center",
                 arrowprops=dict(arrowstyle="->", color=H.NAVY, lw=0.9,
                                 connectionstyle="arc3,rad=0.12"), zorder=7)

ax1.plot([3.4], [100], "o", ms=6, color=H.RED, mec="white", mew=1.0, zorder=6)
ax1.text(3.9, 99, "340% 反射率 = 100% 信号", fontsize=8.0, color=H.RED, va="top")
ax1.text(9.5, 55, "镜面高光\n削波", fontsize=8.4, color=H.RED, ha="center", va="center",
         fontweight="bold")

ax1.text(0.0075, 90, "收一档曝光", fontsize=8.0, color=H.TEAL)
ax1.set_xscale("log")
ax1.set_xlim(0.005, 30)
ax1.set_ylim(0, 105)
ax1.set_xlabel("场景反射率（%，对数刻度）")
ax1.set_ylabel("HLG 信号（%）")
ax1.set_xticks([0.01, 0.1, 1, 10])
ax1.set_xticklabels(["1", "10", "100", "1000"])
ax1.minorticks_off()
ax1.set_title("(a) 反射率到信号", fontsize=10.5, pad=6)

# ---------------- (b) ----------------
Ld = LW * E ** GAMMA
Ld_low = LW * (E * 0.5) ** GAMMA
ax2.axvspan(3.4, 30, color=H.RED, alpha=0.07, zorder=0)
ax2.loglog(r, Ld, color=H.NAVY, lw=2.6, zorder=4)
ax2.loglog(r, Ld_low, color=H.TEAL, lw=1.8, ls=(0, (5, 2)), zorder=3)
ax2.axhline(203, color=H.ORANGE, lw=1.0, ls=(0, (4, 3)), zorder=1)
ax2.axhline(1000, color=H.RED, lw=1.0, ls=(0, (4, 3)), zorder=1)
ax2.text(0.006, 230, "203　参考白", fontsize=8.0, color=H.ORANGE, va="bottom")
ax2.text(0.006, 1090, "1000　参考显示峰值", fontsize=8.0, color=H.RED, va="bottom")

ax2.plot([0.18], [float(LW * (E90 * 0.2) ** GAMMA)], "o", ms=6, color=H.NAVY,
         mec="white", mew=1.0, zorder=6)

ax2.set_xlim(0.005, 30)
ax2.set_ylim(0.3, 3000)
ax2.set_xlabel("场景反射率（%，对数刻度）")
ax2.set_ylabel("1000 cd/m$^2$ 屏上的亮度（cd/m$^2$）")
ax2.set_xticks([0.01, 0.1, 1, 10])
ax2.set_xticklabels(["1", "10", "100", "1000"])
ax2.set_yticks([1, 10, 100, 1000])
ax2.set_yticklabels(["1", "10", "100", "1000"])
ax2.minorticks_off()
ax2.set_title("(b) 信号到显示亮度", fontsize=10.5, pad=6)

H.save(fig, 10, "f3_hlg_exposure")
print("18%% grey signal %.1f%%, %.1f nit on 1000-nit display" % (
    float(H.hlg_oetf(E90 * 0.2)) * 100, float(LW * (E90 * 0.2) ** GAMMA)))
