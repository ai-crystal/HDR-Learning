# -*- coding: utf-8 -*-
"""第 05 章 图 5：局部调光的时序伪影（一维模型计算，非厂商数据）。

(a) 背光响应滞后。高光以 160 像素/秒 横移穿过一个分区，目标背光是一段方波；
    驱动器用一阶滞后跟随（时间常数 40 ms）。滞后让亮区前沿偏暗、后沿偏亮，
    运动中的高光因此拖出一条尾巴。
(b) 分区切换造成的暗部跳变。背景上固定一点（暗区），高光横移经过时，
    该点落到的分区背光随分区取值跳变，即使液晶已经压到最低透过率，
    显示亮度仍然在 0.2 到 1 毫尼特之间反复跳，这正是缓慢移动高光旁边
    "黑底在闪"的来源。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

W = 1920
ZONES = 96
ZW = W / ZONES
BG, PEAK = 0.1, 900.0
CR = 2000.0
TAU = 0.040
V = 160.0


def gauss_kernel(sigma):
    n = int(max(3, np.ceil(6 * sigma)))
    x = np.arange(-n, n + 1)
    g = np.exp(-x ** 2 / (2 * sigma ** 2))
    return g / g.sum()


def target_map(obj_center, width=60.0):
    tgt = np.full(W, BG)
    tgt[int(obj_center - width / 2): int(obj_center + width / 2)] = PEAK
    return tgt


def zone_max(obj_center, width=60.0):
    tgt = target_map(obj_center, width)
    idx = np.minimum((np.arange(W) / ZW).astype(int), ZONES - 1)
    z = np.zeros(ZONES)
    np.maximum.at(z, idx, tgt)
    return z


def zone_light(z, psf=0.45):
    g = gauss_kernel(psf * ZW)
    pad = len(g) // 2
    full = np.repeat(z, int(round(ZW)))
    return np.convolve(np.pad(full, pad, mode="edge"), g, mode="same")[pad:-pad]


# ---------------- (a) 时间响应 ----------------
dt = 0.002
t = np.arange(0, 0.75, dt)
demand = np.array([zone_max(40.0 + V * tt)[4] for tt in t])

actual = np.zeros_like(demand)
x = demand[0]
for i in range(len(t)):
    x += (demand[i] - x) * (1 - np.exp(-dt / TAU))
    actual[i] = x

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 4.0))
fig.subplots_adjust(wspace=0.30)

ax1.plot(t * 1000, demand, color=H.GRAY, lw=1.5, ls=(0, (4, 2)), label="目标背光（分区最大值）")
ax1.plot(t * 1000, actual, color=H.ORANGE, lw=2.2, label="实际背光（一阶滞后 40 ms）")
ax1.fill_between(t * 1000, actual, demand, where=demand > actual,
                 color="#f6d6b8", alpha=0.8, lw=0, label="亮度缺口")
ax1.annotate("前沿偏暗", xy=(102, 690), xytext=(240, 690),
             fontsize=8.4, color=H.ORANGE,
             arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=1.0,
                             connectionstyle="arc3,rad=0.2"))
ax1.annotate("后沿拖尾\n（亮物体后方残留亮度）", xy=(600, 420), xytext=(400, 180),
             fontsize=8.2, color=H.RED,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.0,
                             connectionstyle="arc3,rad=-0.2"))
ax1.set_xlim(0, 750)
ax1.set_ylim(0, 1050)
ax1.set_xlabel("时间（毫秒）")
ax1.set_ylabel("分区背光亮度（nit）")
ax1.legend(loc="upper right", fontsize=7.8, labelspacing=0.3, borderpad=0.4)
ax1.set_title("(a) 背光跟不上运动", fontsize=10, pad=4)

# ---------------- (b) 暗部跳变 ----------------
probe = int(5.4 * ZW)
xs = np.linspace(2.0 * ZW, 8.0 * ZW, 600)
lum = [max(BG, zone_light(zone_max(p))[probe] / CR) for p in xs]

ax2.plot(xs / ZW, lum, color=H.RED, lw=2.0)
ax2.axhline(BG, color=H.GRAY, lw=1.0, ls=":")
ax2.text(5.6, 0.148, "背景 0.1 nit", fontsize=8.2, color=H.GRAY, va="bottom", ha="center")
ax2.set_xlim(2, 8)
ax2.set_ylim(0, 1.0)
ax2.set_xticks(range(2, 9))
ax2.set_xlabel("高光中心位置（单位：分区宽度）")
ax2.set_ylabel("暗部固定点的显示亮度（nit）")
ax2.set_title("(b) 暗部随分区切换跳变", fontsize=10, pad=4)

H.save(fig, 5, "f5_artifact_timing")
