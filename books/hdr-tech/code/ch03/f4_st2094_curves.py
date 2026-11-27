# -*- coding: utf-8 -*-
"""图 3-4：ST 2094-40 风格的逐帧映射曲线族。

2094-40 用“拐点 + 贝塞尔锚点”描述映射：拐点以下按 1:1 直通，拐点以上用
一段单调压缩曲线压到目标峰值。这里用一双参数的简化形式画出曲线形状，
横轴是内容归一化亮度，纵轴是显示归一化亮度，压缩段写成
    y = k + (1-k)·(1-(1-t)^p)，  t = (u-k)/(1-k)
k 为拐点，p 为压缩强度。参数是为说明形状而选的合成值，不对应任何真实片源。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
plt.rcParams["mathtext.fontset"] = "dejavusans"


def curve(u, k, p):
    u = np.asarray(u, dtype=float)
    t = np.clip((u - k) / (1 - k), 0, 1)
    y = np.where(u <= k, u, k + (1 - k) * (1 - (1 - t) ** p))
    return y


u = np.linspace(0, 1, 600)

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(8.8, 4.0), gridspec_kw={"width_ratios": [1.1, 1.0]})
fig.subplots_adjust(left=0.085, right=0.975, bottom=0.155, top=0.935, wspace=0.28)

ax1.plot(u, u, color=H.GRAY, lw=1.1, ls=(0, (4, 3)), zorder=1,
         label="1:1 参考")

fams = [(0.35, 1.00, H.NAVY, "直通，目标 1000 nit"),
        (0.35, 1.60, H.BLUE, "目标 600 nit"),
        (0.35, 2.40, H.TEAL, "目标 300 nit"),
        (0.35, 3.60, H.ORANGE, "目标 100 nit")]
for k, p, c, lab in fams:
    ax1.plot(u, curve(u, k, p), color=c, lw=2.2, label=lab)

ax1.plot([0.35], [0.35], "o", ms=6, color=H.RED, mec="white", mew=0.9, zorder=6)
ax1.annotate("拐点以下按 1:1 直通\n拐点以上才开始压缩",
             xy=(0.35, 0.35), xytext=(0.03, 0.10),
             fontsize=8.2, color=H.RED, ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                             shrinkA=4, shrinkB=5,
                             connectionstyle="arc3,rad=-0.25"))
ax1.text(0.045, 0.93, "(a) 同一帧、不同目标峰值", fontsize=8.8, color=H.DARK)

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1.02)
ax1.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax1.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax1.set_xlabel("内容亮度（相对当前帧峰值）")
ax1.set_ylabel("显示亮度（相对目标峰值）")
ax1.legend(loc="lower right", fontsize=7.6, handlelength=2.0,
           borderpad=0.45, labelspacing=0.30)

# ---- (b) 静态映射与逐帧映射对同一段内容的影响 ----
x = np.linspace(0, 1, 600)
static = curve(x, 0.80, 3.2)          # 按全片 MaxCLL 定的静态曲线
adap = np.where(x < 0.45, x, 0.45 + (1 - 0.45) *
                (1 - (1 - np.clip((x - 0.45) / 0.55, 0, 1)) ** 1.5))
ax2.plot(x, static, color=H.GRAY, lw=2.2, ls=(0, (5, 2)),
         label="静态映射（按全片 4010 nit）")
ax2.plot(x, adap, color=H.TEAL, lw=2.2, label="逐帧映射（当前帧 400 nit）")
ax2.fill_between(x, static, adap, where=(adap > static), color=H.ORANGE,
                 alpha=0.18, lw=0)
ax2.annotate("这一段被静态曲线压暗", xy=(0.62, 0.45), xytext=(0.46, 0.08),
             fontsize=8.2, color=H.ORANGE,
             arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=0.9,
                             shrinkA=3, shrinkB=4))
ax2.text(0.045, 0.93, "(b) 同一帧、两种映射策略", fontsize=8.8, color=H.DARK)

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1.02)
ax2.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax2.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax2.set_xlabel("内容亮度（相对当前帧峰值）")
ax2.set_ylabel("显示亮度（相对目标峰值）")
ax2.legend(loc="upper left", bbox_to_anchor=(0.02, 0.90), fontsize=7.6,
           handlelength=2.2, borderpad=0.45, labelspacing=0.30)

H.save(fig, 3, "f4_st2094_curves")
