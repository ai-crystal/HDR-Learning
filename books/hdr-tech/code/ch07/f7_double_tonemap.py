# -*- coding: utf-8 -*-
"""图 7-7：两极色调映射串联造成的中间调塌陷。

映射在 PQ 码值域里做，滚降起点取源码值的 60%，这是 BT.2390 类 EETF 的
常见选择。源峰值 4000 nit，面板 800 nit。正确做法只映射一次；若播放器
已经映射过、元数据却仍写着 4000，显示端会按同一曲线再压一遍。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import FuncFormatter, NullFormatter

SRC, PANEL = 4000.0, 800.0
KNEE = 0.60
CS = float(H.pq_oetf(SRC))
CP = float(H.pq_oetf(PANEL))


def roll(u):
    u = np.clip(u, 0, None)
    return np.where(u <= KNEE, u,
                    KNEE + (1 - KNEE) * np.tanh((u - KNEE) / (1 - KNEE)) / np.tanh(1.0))


def once(L):
    c = H.pq_oetf(L)
    return H.pq_eotf(roll(c / CS) * CP)


L = np.logspace(np.log10(0.5), np.log10(4000), 900)
y1 = once(L)
y2 = once(y1)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.6, 5.5), sharex=True,
                               gridspec_kw={"height_ratios": [1.45, 1.0],
                                            "hspace": 0.12})
fig.subplots_adjust(left=0.105, right=0.975, bottom=0.125, top=0.955)

ax1.loglog(L, L, color="#c3ccd6", lw=1.3, ls=(0, (1, 2)),
           label="一比一参照")
ax1.loglog(L, y1, color=H.TEAL, lw=2.3, label="映射一次：4000 到 800")
ax1.loglog(L, y2, color=H.RED, lw=2.3, label="映射两次：再按 4000 压一遍")
ax1.set_xlim(0.5, 4600)
ax1.set_ylim(0.5, 4500)
ax1.set_yticks([1, 3, 10, 30, 100, 300, 1000])
ax1.set_ylabel("显示亮度（cd/m$^2$）")
ax1.legend(loc="upper left", fontsize=8.0, handlelength=2.6,
           borderpad=0.5, labelspacing=0.35)

L18 = 14.0
a, b = float(once(np.array(L18))), float(once(once(np.array(L18))))
ax1.plot([L18, L18], [b, a], color=H.GRAY, lw=0.9, ls=(0, (3, 2)))
ax1.plot([L18], [a], "o", ms=5, color=H.TEAL, mec="white", mew=0.8, zorder=5)
ax1.plot([L18], [b], "o", ms=5, color=H.RED, mec="white", mew=0.8, zorder=5)
ax1.annotate(f"18% 灰 {a:.1f} → {b:.1f} nit", xy=(L18 * 1.1, b),
             xytext=(0.9, 60), fontsize=7.8, color=H.RED,
             ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                             shrinkA=3, shrinkB=5,
                             connectionstyle="arc3,rad=0.25"))
ax1.text(0.62, 1400, "高光段两级压缩后\n只剩 200 nit 上下",
         fontsize=7.6, color=H.GRAY, ha="left", va="center", linespacing=1.6)

for y, c, lab in [(y1, H.TEAL, "映射一次"), (y2, H.RED, "映射两次")]:
    s = np.gradient(np.log(y), np.log(L))
    ax2.semilogx(L, s, color=c, lw=2.2, label=lab)
ax2.semilogx(L, np.ones_like(L), color="#c3ccd6", lw=1.2, ls=(0, (1, 2)))
ax2.set_ylim(0.35, 1.12)
ax2.set_yticks([0.4, 0.6, 0.8, 1.0])
ax2.set_ylabel("对数斜率")
ax2.set_xlabel("输入亮度（cd/m$^2$）")
ax2.legend(loc="lower right", fontsize=8.0, handlelength=2.6,
           borderpad=0.5, labelspacing=0.35)
ax2.text(0.55, 0.62, "斜率小于 1 的一段\n明暗差被按比例削掉",
         fontsize=7.6, color=H.GRAY, ha="left", va="center", linespacing=1.6)

for ax in (ax1, ax2):
    ax.set_xlim(0.5, 4600)
    ax.set_xticks([1, 3, 10, 30, 100, 300, 1000, 3000])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
    ax.xaxis.set_minor_formatter(NullFormatter())
ax1.tick_params(labelbottom=False)

H.save(fig, 7, "f7_double_tonemap")
