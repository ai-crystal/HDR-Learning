# -*- coding: utf-8 -*-
"""第 17 章 f3：显示端映射 vs 源端映射

左列：示意图（谁来决定怎么压）。
右列：映射曲线的区别——显示端映射时两台屏各走各的曲线；源端映射时两台屏重合。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle


def eetf_nit(x_nit, cmax_nit, dmax_nit, offset=0.5):
    """BT.2390 EETF，输入/输出均为 nit。"""
    pq_c = float(H.pq_oetf(cmax_nit))
    pq_d = float(H.pq_oetf(dmax_nit))
    maxLum = pq_d / pq_c
    ks = float(np.clip((1.0 + offset) * maxLum - offset, 0.0, 0.95))
    u = H.pq_oetf(np.clip(x_nit, 0.0, cmax_nit)) / pq_c
    t = np.clip((u - ks) / (1.0 - ks), 0.0, 1.0)
    pb = ((2 * t**3 - 3 * t**2 + 1) * ks
          + (t**3 - 2 * t**2 + t) * (1.0 - ks)
          + (-2 * t**3 + 3 * t**2) * maxLum)
    out = np.where(u < ks, u, pb)
    return H.pq_eotf(np.clip(out * pq_c, 0.0, 1.0))


def box(ax, x, y, w, h, text, fc, ec, fs=8.4, tc="#12233b"):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.010,rounding_size=0.018",
                                transform=ax.transAxes, fc=fc, ec=ec, lw=1.1, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, transform=ax.transAxes, ha="center",
            va="center", fontsize=fs, color=tc, zorder=4, linespacing=1.6)


def bar(ax, x, y, w, label, col):
    ax.add_patch(Rectangle((x, y), 0.44, 0.052, transform=ax.transAxes,
                           fc="#eef2f6", ec="#c3ccd6", lw=0.9, zorder=2))
    ax.add_patch(Rectangle((x, y), w, 0.052, transform=ax.transAxes,
                           fc=col, ec="none", zorder=3))
    ax.text(x + 0.22, y - 0.022, label, transform=ax.transAxes, ha="center",
            va="top", fontsize=7.6, color=col, zorder=4)


def arrow(ax, x0, y0, x1, y1, col="#7f8c8d"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), xycoords="axes fraction",
                textcoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.2,
                                shrinkA=0, shrinkB=0), zorder=2)


def schematic(ax, title, content_text, mid_text, mid_col, bar_labels, bar_frac,
              result_text, result_col, caveat):
    """画一张“内容 → 两台屏 → 输出峰值条”的示意。"""
    ax.set_axis_off()
    ax.set_title(title, fontsize=10.5, loc="left")
    box(ax, 0.18, 0.815, 0.64, 0.16, content_text, "#eef4fa", H.NAVY)
    arrow(ax, 0.42, 0.810, 0.25, 0.700, mid_col)
    arrow(ax, 0.58, 0.810, 0.75, 0.700, mid_col)
    ax.text(0.50, 0.752, mid_text, transform=ax.transAxes, ha="center",
            va="center", fontsize=7.8, color=mid_col,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.9))
    box(ax, 0.03, 0.505, 0.42, 0.165, "峰值 400 nit 的屏", "#fdf3e8", H.ORANGE)
    box(ax, 0.55, 0.505, 0.42, 0.165, "峰值 1000 nit 的屏", "#e8f6f3", H.TEAL)
    bar(ax, 0.03, 0.365, 0.44 * bar_frac[0], bar_labels[0], bar_frac[2])
    bar(ax, 0.55, 0.365, 0.44 * bar_frac[1], bar_labels[1], bar_frac[2])
    ax.text(0.50, 0.205, result_text, transform=ax.transAxes, ha="center",
            va="center", fontsize=8.4, color=result_col)
    ax.text(0.50, 0.075, caveat, transform=ax.transAxes, ha="center",
            va="center", fontsize=8.2, color="#4a5666")


fig = H.plt.figure(figsize=(7.2, 5.0))
gs = fig.add_gridspec(2, 2, width_ratios=[1.14, 1.0], hspace=0.52, wspace=0.26)
a0 = fig.add_subplot(gs[0, 0]); a1 = fig.add_subplot(gs[0, 1])
b0 = fig.add_subplot(gs[1, 0]); b1 = fig.add_subplot(gs[1, 1])
fig.subplots_adjust(left=0.065, right=0.975, top=0.86, bottom=0.07)

C400, C1000 = H.BLUE, H.TEAL
xq = np.logspace(np.log10(10), np.log10(4000), 900)
y400 = eetf_nit(xq, 4000.0, 400.0)
y1000 = eetf_nit(xq, 4000.0, 1000.0)
LEG = dict(fontsize=7.7, handlelength=1.8, frameon=True, facecolor="white",
           edgecolor="#c3ccd6", framealpha=0.9)

# ======================= (a) 显示端映射 =======================
schematic(a0, "(a) 显示端映射：谁在放，就谁自己压",
          "HDR 内容（同一份）\n峰值 4000 nit",
          "各设备按自身能力决定曲线", H.RED,
          ("输出峰值 400 nit", "输出峰值 1000 nit"), (0.40, 1.0, C400),
          "同一份内容 → 两种观感：高光压缩程度不同", H.RED,
          "缺点：各家算法不同，观感难以统一")

a1.plot(xq, y400 / 400.0, color=C400, lw=2.3, label="400 nit 屏的曲线")
a1.plot(xq, y1000 / 1000.0, color=C1000, lw=2.3, label="1000 nit 屏的曲线")
a1.plot(xq, xq / 4000.0, color=H.LGRAY, ls=(0, (1, 2)), lw=1.5, label="输入 = 输出")
gap = y1000 / 1000.0 - y400 / 400.0
k = int(np.argmax(gap))
xa = xq[k]
ka = int(np.argmin(np.abs(xq - 150)))
a1.annotate("", xy=(xq[ka], y1000[ka] / 1000.0), xytext=(xq[ka], y400[ka] / 400.0),
            arrowprops=dict(arrowstyle="<->", color="#33475b", lw=1.1))
a1.set_xscale("log")
a1.set_xlim(10, 4000); a1.set_ylim(0, 1.10)
a1.set_xlabel("输入亮度 / nit（内容峰值 4000 nit）", fontsize=9)
a1.set_ylabel("输出亮度\n（归一化到各屏峰值）", fontsize=9)
a1.set_title("两台屏：曲线不一样（同一输入，输出差一截）", fontsize=9.8, loc="left")
a1.legend(loc="lower right", **LEG)

# ======================= (b) 源端映射 =======================
schematic(b0, "(b) 源端映射：内容里就写好怎么压",
          "HDR 内容 + 逐场景元数据\n“这一帧就该这么压”",
          "设备照做，用同一条曲线", H.GREEN,
          ("按内容指定曲线输出", "按内容指定曲线输出"), (1.0, 1.0, H.GREEN),
          "同一份内容 → 观感一致（忠于创作意图）", H.GREEN,
          "前提：内容带元数据 + 设备愿意照办")

yref = eetf_nit(xq, 4000.0, 800.0)
b1.plot(xq, y400 / 400.0, color="#c3ccd6", lw=1.5, ls="--",
        label="（对照）显示端映射的两条曲线")
b1.plot(xq, y1000 / 1000.0, color="#c3ccd6", lw=1.5, ls="--")
b1.plot(xq, yref / 800.0, color=H.GREEN, lw=2.6, label="内容指定的曲线（两台屏都照做）")
b1.plot(xq, xq / 4000.0, color=H.LGRAY, ls=(0, (1, 2)), lw=1.5, label="输入 = 输出")
b1.set_xscale("log")
b1.set_xlim(10, 4000); b1.set_ylim(0, 1.10)
b1.set_xlabel("输入亮度 / nit（内容峰值 4000 nit）", fontsize=9)
b1.set_ylabel("输出亮度\n（归一化到各屏峰值）", fontsize=9)
b1.set_title("两台屏：曲线重合", fontsize=10, loc="left")
b1.legend(loc="lower right", **LEG)
b1.annotate("两台屏都走这条曲线 → 观感一致", xy=(900, 0.70), xytext=(12, 0.97),
            fontsize=7.9, color=H.GREEN, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=H.GREEN, lw=1.0))

fig.suptitle("谁来压缩高光：显示端映射 vs 源端映射", fontsize=12.5,
             fontweight="bold", y=0.965)

H.save(fig, 17, "f3_display_vs_source")
