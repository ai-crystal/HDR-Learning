# -*- coding: utf-8 -*-
"""第 10 章 图 10-1：位深与色带（banding）。

做法：取一段**很窄的暗部亮度窗口**（ΔV=0.10），再把这个窗口的对比度
拉伸到全黑—全白。这样每级台阶被放大，能清楚区分：
  8bit  → 台阶宽、色带明显；
  10bit → 台阶细 4 倍，仅隐约可见；
  12bit → 台阶再细 4 倍，肉眼已看不出。
（直接并排画整条渐变是看不出区别的——因为输出图片本身只有 8bit。）
"""
import sys
sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import numpy as np
import hdrfig as H

W, Hpx = 1200, 110
V0, V1 = 0.06, 0.16          # 暗部窗口（占满量程的比例）

x = np.linspace(0, 1, W)
V = V0 + x * (V1 - V0)

fig, axs = H.plt.subplots(3, 1, figsize=(7.2, 4.3),
                          gridspec_kw=dict(hspace=0.62))
info = []
for ax, b in zip(axs, (8, 10, 12)):
    L = 2 ** b
    Vq = np.round(V * L) / L                     # 按位深量化
    disp = np.clip((Vq - V0) / (V1 - V0) * 255, 0, 255).astype(np.uint8)
    img = disp[None, :].repeat(Hpx, axis=0)
    ax.imshow(img, cmap="gray", vmin=0, vmax=255, aspect="auto",
              interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values():
        sp.set_color("#4a5666"); sp.set_linewidth(1.0)
    nsteps = int(round((V1 - V0) * L))           # 窗口内的台阶数
    if b == 8:
        col, tag = H.RED, "台阶宽、色带明显"
    elif b == 10:
        col, tag = H.ORANGE, "台阶细 4 倍，仅隐约可见"
    else:
        col, tag = H.GREEN, "台阶再细 4 倍，肉眼已看不出"
    ax.set_title(f"{b}bit　每通道 {L} 级　·　本窗口内约 {nsteps} 级台阶　→　{tag}",
                 fontsize=10.5, color=col, fontweight="bold", loc="left", pad=5)
    info.append((b, L, nsteps))

axs[0].annotate("肉眼可见的“色带（banding）”",
                xy=(0.14, 0.5), xycoords="axes fraction",
                xytext=(0.30, 0.5), textcoords="axes fraction",
                fontsize=8.4, color="white", va="center", ha="left",
                arrowprops=dict(arrowstyle="->", color="white", lw=1.2))
axs[0].text(0.995, 0.5, "同样一段暗部窗口（ΔV=0.10）\n对比度已拉伸到全黑—全白",
            transform=axs[0].transAxes, ha="right", va="center",
            fontsize=7.6, color="white",
            bbox=dict(boxstyle="round,pad=0.28", fc="#00000055", ec="none"))

fig.suptitle("位深与色带：同一段暗部渐变，8 / 10 / 12bit 的台阶粗细对比",
             fontsize=12.5, fontweight="bold", y=1.0)
fig.text(0.5, -0.02,
         "说明：三张用的是同一段渐变，只是位深不同；输出图片本身也是 8bit，"
         "所以这里靠“窄窗口 + 对比度拉伸”把台阶放大——8bit 最粗，12bit 最细。",
         ha="center", fontsize=8.2, color=H.GRAY)
fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.13)

H.save(fig, 10, "f1_banding_bits")
