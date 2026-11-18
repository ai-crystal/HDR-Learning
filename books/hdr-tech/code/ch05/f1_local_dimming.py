# -*- coding: utf-8 -*-
"""第 05 章 图 1：局部调光下的显示亮度剖面（一维面板模型计算，非厂商数据）。

模型假设（全部写在脚本里，可按需修改）：
  1. 目标画面为一维切面：0.1 nit 暗背景中央有 60 px 宽、1000 nit 的高光条；
  2. 背光按分区取该区最大值，再经扩散片高斯平滑（sigma = 0.45 个分区宽度）；
  3. 液晶透射率 = 目标亮度 / 背光亮度，被限制在 [液晶黑位, 1]；
  4. 液晶黑位透射率取 1/2000（对应有效对比度 2000:1）；
  5. 显示亮度 = 背光亮度 × 液晶透射率。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

W, OBJ = 1920, 60
BG, PEAK = 0.1, 1000.0

target = np.full(W, BG)
target[W // 2 - OBJ // 2: W // 2 + OBJ // 2] = PEAK


def gauss_kernel(sigma):
    n = int(max(3, np.ceil(6 * sigma)))
    x = np.arange(-n, n + 1)
    g = np.exp(-x ** 2 / (2 * sigma ** 2))
    return g / g.sum()


def simulate(zones, cr=2000.0, psf=0.45):
    zw = W / zones
    idx = np.minimum((np.arange(W) / zw).astype(int), zones - 1)
    zmax = np.zeros(zones)
    np.maximum.at(zmax, idx, target)
    bl = zmax[idx]
    g = gauss_kernel(psf * zw)
    pad = len(g) // 2
    bl = np.convolve(np.pad(bl, pad, mode="edge"), g, mode="same")[pad:-pad]
    lc = np.clip(target / np.maximum(bl, 1e-9), 1.0 / cr, 1.0)
    return bl, bl * lc


x = np.arange(W) - W // 2
fig, ax = plt.subplots(figsize=(7.4, 4.3))
ax.plot(x, target, color=H.DARK, lw=2.4, ls=(0, (5, 2)), label="目标画面（理想显示）")

for zones, color in [(1, H.RED), (32, H.ORANGE), (128, H.TEAL), (512, H.BLUE)]:
    _, disp = simulate(zones)
    label = "全局背光（无分区）" if zones == 1 else f"{zones} 分区"
    ax.plot(x, disp, color=color, lw=1.9, label=label)

_, disp32 = simulate(32)
ax.annotate("光晕：背光溢到暗区，\n液晶最低透射率压不到更黑",
            xy=(66, disp32[W // 2 + 66]), xytext=(84, 11),
            fontsize=8.5, color=H.ORANGE, ha="left", va="bottom",
            arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=1.0,
                            connectionstyle="arc3,rad=0.2"))

ax.set_yscale("log")
ax.set_xlim(-160, 160)
ax.set_ylim(0.05, 3000)
ax.set_xlabel("屏幕水平位置（像素，以高光条中心为原点）")
ax.set_ylabel("显示亮度（nit，对数刻度）")
ax.set_yticks([0.1, 1, 10, 100, 1000])
ax.set_yticklabels(["0.1", "1", "10", "100", "1000"])
ax.minorticks_off()
ax.legend(loc="upper left", fontsize=8.5)
H.save(fig, 5, "f1_local_dimming")
