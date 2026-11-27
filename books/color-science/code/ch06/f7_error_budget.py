# -*- coding: utf-8 -*-
"""第 06 章 图 7：色度子采样的误差随亮度的变化（误差预算的一环）。

场景：一个满饱和的 BT.2020 红像素与等亮度灰像素相邻，色度取平均后重建，
比较 YCbCr 与 ICtCp 两种编码。左图为总色差，右图为其中落在亮度轴上的那部分。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import ictcp as I

plt = H.plt

P = 10000.0
YS = np.logspace(np.log10(0.1), np.log10(500), 80)

tot_y, tot_i, lum_y, lum_i = [], [], [], []
for Y in YS:
    red = np.array([Y / 0.2627 / P, 0.0, 0.0])
    gray = np.array([Y / P] * 3)
    both = np.stack([red, gray], axis=0)

    yuv = I.rgb_lin_to_ycbcr(both, peak=P)
    cb = yuv[0, 1] * 0.5 + yuv[1, 1] * 0.5
    cr = yuv[0, 2] * 0.5 + yuv[1, 2] * 0.5
    yuv2 = np.stack([yuv[:, 0], np.full(2, cb), np.full(2, cr)], axis=-1)
    rec_y = I.ycbcr_to_rgb_lin(yuv2, peak=P)

    ict = I.rgb_lin_to_ictcp(both, peak=P)
    ict2 = ict.copy()
    ict2[:, 1] = ict[0, 1] * 0.5 + ict[1, 1] * 0.5
    ict2[:, 2] = ict[0, 2] * 0.5 + ict[1, 2] * 0.5
    rec_i = I.ictcp_to_rgb_lin(ict2, peak=P)

    e_y = I.rgb_lin_to_ictcp(rec_y, peak=P)
    e_i = I.rgb_lin_to_ictcp(rec_i, peak=P)
    tot_y.append(float(I.deltaE_ITP(e_y, ict).max()))
    tot_i.append(float(I.deltaE_ITP(e_i, ict).max()))
    lum_y.append(float(720 * np.abs(e_y[:, 0] - ict[:, 0]).max()))
    lum_i.append(float(720 * np.abs(e_i[:, 0] - ict[:, 0]).max()))

tot_y, tot_i = np.array(tot_y), np.array(tot_i)
lum_y, lum_i = np.array(lum_y), np.array(lum_i)

fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.7),
                         gridspec_kw=dict(width_ratios=[1.05, 1.0], wspace=0.30))
fig.subplots_adjust(left=0.085, right=0.985, top=0.90, bottom=0.16)

ax = axes[0]
ax.plot(YS, tot_y, color=H.RED, lw=2.0, label="YCbCr（BT.2020 NCL）")
ax.plot(YS, tot_i, color=H.NAVY, lw=2.0, ls=(0, (5, 2.5)), label="ICtCp（BT.2100）")
ax.set_xscale("log")
ax.set_xlim(0.1, 520)
ax.set_ylim(0, 400)
ax.set_xticks([0.1, 1, 10, 100, 500])
ax.set_xticklabels(["0.1", "1", "10", "100", "500"])
ax.set_xlabel("像素的绝对亮度（cd/m$^2$）", fontsize=9.5)
ax.set_ylabel("重建后的 $\\Delta E_{ITP}$", fontsize=9.5)
ax.legend(loc="upper left", fontsize=7.8, handletextpad=0.6, borderpad=0.35)
ax.text(1.3, 300, "同一块彩边，亮度越高错得越多", fontsize=7.4, color="#39485a")

ax2 = axes[1]
ax2.plot(YS, lum_y, color=H.RED, lw=2.0, label="YCbCr")
ax2.plot(YS, lum_i, color=H.NAVY, lw=2.0, ls=(0, (5, 2.5)), label="ICtCp")
ax2.set_xscale("log")
ax2.set_xlim(0.1, 520)
ax2.set_ylim(-0.6, 12)
ax2.set_xticks([0.1, 1, 10, 100, 500])
ax2.set_xticklabels(["0.1", "1", "10", "100", "500"])
ax2.set_xlabel("像素的绝对亮度（cd/m$^2$）", fontsize=9.5)
ax2.set_ylabel("落在亮度轴上的误差 $720\\,|\\Delta I|$", fontsize=9.5)
ax2.legend(loc="upper left", fontsize=7.8, handletextpad=0.6, borderpad=0.35)
ax2.text(1.3, 0.35, "$I$ 不含 $S$，色度取样不碰亮度轴，ICtCp 恒为 0", fontsize=7.4,
         color="#1f4e79", va="bottom")
ax2.annotate("YCbCr 的亮度项随亮度增大", xy=(400, 7.9), xytext=(3.0, 10.6),
             fontsize=7.4, color=H.RED,
             arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=0.9,
                             shrinkA=2, shrinkB=3))

H.save(fig, 6, "f7_error_budget")
print("total at 1,100,1000:", tot_y[20], tot_y[55], tot_y[-1])
print("lum at 1,100,1000:", lum_y[20], lum_y[55], lum_y[-1])
