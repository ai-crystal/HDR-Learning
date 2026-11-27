# -*- coding: utf-8 -*-
"""第 10 章 图 7：两个常见失败模式的量化。

(a) 传输特性标错。同一码值在 PQ 与 HLG 两种解释下对应的亮度不同：
    PQ 走 ST 2084 的 EOTF；HLG 走 BT.2100 的 OOTF（显示峰值 1000 nit，
    系统 gamma 1.2）。两条曲线在参考白附近交叉，越往高光差得越多。
(b) 白点不一致。DCI 放映白与 D65 在 CIE 1976 u'v' 上的距离，并画出
    BT.709、DCI-P3、BT.2020 三个色域三角形作为参照。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt


def xy_to_upvp(x, y):
    d = -2 * x + 12 * y + 3
    return 4 * x / d, 9 * y / d


fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(9.0, 4.4), gridspec_kw={"width_ratios": [1.05, 1.0]})
fig.subplots_adjust(left=0.09, right=0.975, bottom=0.145, top=0.945, wspace=0.26)

# ---------------- (a) ----------------
code = np.linspace(0.02, 1.0, 800)
L_pq = H.pq_eotf(code)
L_hlg = 1000.0 * H.hlg_eotf(code) ** 1.2
ax1.semilogy(code, L_pq, color=H.NAVY, lw=2.5, label="按 PQ 解释", zorder=4)
ax1.semilogy(code, L_hlg, color=H.ORANGE, lw=2.5, label="按 HLG 解释", zorder=4)
ax1.fill_between(code, L_pq, L_hlg, where=(code > 0.30), color=H.RED, alpha=0.09, zorder=1)

ax1.plot([0.58], [float(H.pq_eotf(0.58))], "o", ms=5.5, color=H.TEAL, mec="white",
         mew=1.0, zorder=6)
ax1.annotate("码值 0.58 附近两条线相交\n参考白在此对齐", xy=(0.58, 200), xytext=(0.10, 2300),
             fontsize=8.0, color=H.TEAL,
             arrowprops=dict(arrowstyle="->", color=H.TEAL, lw=0.9,
                             connectionstyle="arc3,rad=0.2"), zorder=7)

ax1.annotate("", xy=(0.75, float(H.pq_eotf(0.75))), xytext=(0.75, float(1000 * H.hlg_eotf(0.75) ** 1.2)),
             arrowprops=dict(arrowstyle="<->", color=H.RED, lw=1.2))
ax1.text(0.765, 420, "同一码值 0.75\n差 4.8 倍", fontsize=8.2, color=H.RED)

ax1.set_xlim(0, 1.02)
ax1.set_ylim(0.05, 1.2e4)
ax1.set_xlabel("归一化码值")
ax1.set_ylabel("显示亮度（cd/m$^2$）")
ax1.set_xticks([0, 0.25, 0.5, 0.58, 0.75, 1.0])
ax1.set_xticklabels(["0", "0.25", "0.50", "0.58", "0.75", "1.0"])
ax1.set_yticks([0.1, 1, 10, 100, 1000, 10000])
ax1.set_yticklabels(["0.1", "1", "10", "100", "1000", "10000"])
ax1.minorticks_off()
ax1.legend(loc="lower right", fontsize=8.2)
ax1.set_title("(a) 传输特性标错", fontsize=10.5, pad=6)

# ---------------- (b) ----------------
gamuts = [
    ("BT.709", (0.640, 0.330), (0.300, 0.600), (0.150, 0.060), H.GRAY, 0.0),
    ("DCI-P3", (0.680, 0.320), (0.265, 0.690), (0.150, 0.060), H.TEAL, 14.0),
    ("BT.2020", (0.708, 0.292), (0.170, 0.797), (0.131, 0.046), H.NAVY, 30.0),
]
for name, r, g, b, c, dy in gamuts:
    pr, pg, pb = xy_to_upvp(*r), xy_to_upvp(*g), xy_to_upvp(*b)
    ax2.plot([pr[0], pg[0], pb[0], pr[0]], [pr[1], pg[1], pb[1], pr[1]],
             color=c, lw=1.7, zorder=3)
    ax2.annotate(name, xy=pr, xytext=(pr[0] + 0.012, pr[1] + dy / 1000.0 + 0.008),
                 fontsize=8.2, color=c, ha="left", va="bottom")

wx1, wy1 = xy_to_upvp(0.3127, 0.3290)
wx2, wy2 = xy_to_upvp(0.314, 0.351)
d = np.hypot(wx1 - wx2, wy1 - wy2)
ax2.plot([wx1, wx2], [wy1, wy2], color=H.RED, lw=1.4, ls=(0, (2, 2)), zorder=5)
ax2.plot([wx1], [wy1], "o", ms=6.5, color=H.ORANGE, mec="white", mew=1.0, zorder=6)
ax2.plot([wx2], [wy2], "o", ms=6.5, color=H.RED, mec="white", mew=1.0, zorder=6)
ax2.annotate("D65", xy=(wx1, wy1), xytext=(wx1 - 0.075, wy1 - 0.030), fontsize=8.4,
             color=H.ORANGE,
             arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=0.8))
ax2.annotate("DCI 放映白", xy=(wx2, wy2), xytext=(wx2 + 0.035, wy2 + 0.045), fontsize=8.4,
             color=H.RED,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.8))
ax2.text(0.033, 0.315, "两点相距 $\\Delta u'v'$ = %.3f\n约为刚可觉察的 3 至 4 倍" % d,
         fontsize=8.0, color=H.RED)

ax2.set_xlim(0.02, 0.60)
ax2.set_ylim(0.14, 0.62)
ax2.set_xlabel("$u'$")
ax2.set_ylabel("$v'$")
ax2.set_xticks([0.1, 0.2, 0.3, 0.4, 0.5])
ax2.set_yticks([0.2, 0.3, 0.4, 0.5, 0.6])
ax2.set_title("(b) 白点不一致", fontsize=10.5, pad=6)

H.save(fig, 10, "f7_failure_modes")
print("du'v' = %.4f" % d)
