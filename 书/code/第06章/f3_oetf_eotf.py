# -*- coding: utf-8 -*-
"""图 06-3：OETF 打包 → 传输 → EOTF 解包 的采集-显示链路。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig = H.plt.figure(figsize=(7.2, 5.0))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.25], hspace=0.30)
ax = fig.add_subplot(gs[0]); ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 3.0)

xs = [0.05, 1.95, 3.85, 5.75, 7.65]
w = 1.75
cols = [H.GRAY, H.NAVY, H.PURPLE, H.TEAL, H.GREEN]
titles = ["场景的光", "OETF 打包", "码值 / 信号", "EOTF 解包", "屏幕的光"]
subs = ["（原场景）\nL = 0.180\n（18% 灰）",
        "（采集/编码端）\nV = L$^{1/2.2}$\n= 0.459",
        "（传输、存储）\n8bit → 117\n（0.459×255）",
        "（显示端）\nL = V$^{2.2}$\n= 0.180",
        "（重现）\nL = 0.180\n与原场景一致 √"]

for x, c, t, s in zip(xs, cols, titles, subs):
    ax.add_patch(FancyBboxPatch((x, 0.95), w, 1.60, boxstyle="round,pad=0.06",
                                fc="white", ec=c, lw=1.6))
    ax.text(x + w / 2, 2.34, t, ha="center", va="center", fontsize=9.4,
            color=c, fontweight="bold")
    ax.text(x + w / 2, 1.55, s, ha="center", va="center", fontsize=8.4, color=H.DARK)

for i in range(4):
    x0, x1 = xs[i] + w + 0.03, xs[i + 1] - 0.03
    ax.add_patch(FancyArrowPatch((x0, 1.75), (x1, 1.75), arrowstyle="-|>",
                                 mutation_scale=13, lw=1.6, color=H.GRAY))

ax.text(0.05, 2.76, "① 链路：场景的光 → 码值 → 屏幕的光，两头必须互逆",
        fontsize=10.2, fontweight="bold", color=H.DARK)
ax.text(0.05, 0.58,
        "只要 EOTF 正好是 OETF 的逆运算，屏幕重现的光就与原场景一致；两者错位 → 画面发灰或发暗（见 6.9 节）。",
        fontsize=8.5, color=H.RED)
ax.text(0.05, 0.16,
        "链路上实际的写法：BT.709 的 OETF 用指数 0.45（≈1/2.2）再加一段直线脚；sRGB 的 EOTF 用 2.4 次方再加直线脚。",
        fontsize=8.5, color=H.DARK)

# ---------------- 下：两条曲线互为镜像 ----------------
ax2 = fig.add_subplot(gs[1])
L = np.linspace(0, 1, 600)
oetf = H.gamma_oetf(L, 2.2)          # 光 -> 码值
eotf = H.gamma_eotf(L, 2.2)          # 码值 -> 光

ax2.plot(L, oetf, color=H.NAVY, lw=2.6, label="OETF（打包）：V = L$^{1/2.2}$")
ax2.plot(L, eotf, color=H.TEAL, lw=2.6, ls="--", label="EOTF（解包）：L = V$^{2.2}$")
ax2.plot([0, 1], [0, 1], color=H.LGRAY, lw=1.2, ls=":", label="对角参考线")

# 互逆示意：0.18 --打包--> 0.459 --解包--> 0.18
ax2.plot([0.18, 0.459], [0.459, 0.459], color=H.ORANGE, lw=1.2, ls="-.")
ax2.plot([0.459, 0.459], [0.459, 0.18], color=H.ORANGE, lw=1.2, ls="-.")
ax2.plot([0.18, 0.18], [0.18, 0.459], color=H.ORANGE, lw=1.2, ls="-.")
ax2.plot(0.18, 0.459, "o", color=H.ORANGE, ms=6)
ax2.plot(0.459, 0.18, "o", color=H.ORANGE, ms=6)

ax2.text(0.035, 0.975,
         "同一个点的一对坐标\n(L, V) 与 (V, L)：关于对角线镜像\n"
         "→ 打包再解包，光回到原值",
         fontsize=8.2, color=H.ORANGE, va="top", ha="left",
         bbox=dict(boxstyle="round,pad=0.35", fc="#fff8f0", ec=H.ORANGE, lw=0.9))

ax2.set_xlim(0, 1); ax2.set_ylim(0, 1.02)
ax2.set_xlabel("横轴：左半轴读“线性光 L”，右半轴读“码值 V”（0–1）")
ax2.set_ylabel("码值 V / 线性光 L")
ax2.set_title("② 曲线：OETF 与 EOTF 互为逆运算（理想 2.2 对）", fontsize=11)
ax2.legend(loc="lower right", fontsize=8.5)

H.save(fig, 6, "f3_oetf_eotf")
