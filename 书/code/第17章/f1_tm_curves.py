# -*- coding: utf-8 -*-
"""第 17 章 f1：Reinhard / Hable / ACES / 硬裁剪 四种色调映射曲线对比

坐标约定
    横轴：输入亮度，以"显示峰值"为单位（显示峰值 = 1，即屏幕能显示的最亮值）。
    纵轴：输出亮度，同样归一化到显示峰值（1 = 屏幕最亮）。
    本例假设 内容峰值 = 8 × 显示峰值（例如 4800 nit 内容 / 600 nit 屏幕）。

这样归一化后，"45° 直线"就代表"照搬不压缩"，各条曲线谁贴得近、谁压得狠一目了然。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np

PK = 8.0        # 内容峰值 / 显示峰值
DMAX = 600.0    # 显示峰值 nit（仅用于副坐标轴刻度与 BT.2390 换算）


# ---------------------------------------------------------------- 各种映射算子
def hard_clip(x):
    """硬裁剪：不超过上限就照搬，超了直接砍平。"""
    return np.minimum(x, 1.0)


def linear_dim(x, peak=PK):
    """等比压缩（整体调暗）：把整个输入范围线性缩进显示范围。"""
    return x / peak


def reinhard(x, w=PK):
    """扩展 Reinhard：输出 1.0 对应输入白点 w。"""
    return x * (1.0 + x / (w * w)) / (1.0 + x)


def hable(x, A=0.15, B=0.50, C=0.10, D=0.20, E=0.02, F=0.30):
    """Hable / Uncharted 2 曲线（原始形式）。"""
    return ((x * (A * x + C * B) + D * E) / (x * (A * x + B) + D * F)) - E / F


def hable_norm(x, peak=PK, expo=2.0):
    """Hable 曲线按"输入峰值→显示峰值"归一化（对应 Uncharted 2 的曝光偏置 + 白点标定）。"""
    return hable(expo * x) / hable(expo * peak)


def aces(x, a=2.51, b=0.03, c=2.43, d=0.59, e=0.14):
    """ACES 近似（Narkowicz 拟合），本身已收敛到 1.0。"""
    return np.clip((x * (a * x + b)) / (x * (c * x + d) + e), 0.0, 1.0)


def bt2390(x, cmax_nit=PK * DMAX, dmax_nit=DMAX, offset=0.5):
    """BT.2390 EETF：PQ 域里的分段 Hermite 样条（KS = 1.5*maxLum - 0.5）。

    输入输出都是"显示峰值单位"的线性亮度，内部转到 PQ 码值域做映射。
    offset=0.5 时 KS = (1+offset)*maxLum - offset = 1.5*maxLum - 0.5。
    """
    pq_c = float(H.pq_oetf(cmax_nit))
    pq_d = float(H.pq_oetf(dmax_nit))
    maxLum = pq_d / pq_c
    ks = (1.0 + offset) * maxLum - offset
    ks = float(np.clip(ks, 0.0, 0.95))
    u = H.pq_oetf(np.clip(x * DMAX, 0.0, cmax_nit)) / pq_c
    out = u.copy()
    if ks < 1.0:
        t = np.clip((u - ks) / (1.0 - ks), 0.0, 1.0)
        pb = ((2 * t**3 - 3 * t**2 + 1) * ks
              + (t**3 - 2 * t**2 + t) * (1.0 - ks)
              + (-2 * t**3 + 3 * t**2) * maxLum)
        out = np.where(u < ks, u, pb)
    return H.pq_eotf(np.clip(out * pq_c, 0.0, 1.0)) / DMAX


# ---------------------------------------------------------------- 绘制
fig = H.plt.figure(figsize=(7.2, 4.5))
gs = fig.add_gridspec(1, 2, wspace=0.22, width_ratios=[1.05, 1.0])
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
fig.subplots_adjust(left=0.085, right=0.985, top=0.80, bottom=0.185)

x1 = np.linspace(0, PK, 3000)
x2 = np.linspace(0, 1.6, 1600)

CURVES = [
    ("硬裁剪", H.RED, hard_clip, "-", 2.4),
    ("等比压缩（整体调暗）", H.GRAY, lambda t, p=PK: linear_dim(t, p), "--", 2.0),
    ("Reinhard", H.NAVY, reinhard, "-", 2.2),
    ("Hable / Uncharted 2", H.ORANGE, hable_norm, "-", 2.2),
    ("ACES", H.TEAL, aces, "-", 2.4),
    ("BT.2390 EETF（第 17.4 节，参考）", H.GREEN, bt2390, ":", 2.2),
]

for ax, xv in ((ax1, x1), (ax2, x2)):
    for name, col, fn, ls, lw in CURVES:
        ax.plot(xv, fn(xv), color=col, ls=ls, lw=lw, label=name, zorder=3)
    ax.plot(xv, xv, color=H.LGRAY, lw=1.6, ls=(0, (1, 2)), zorder=1,
            label="理想照搬（输入 = 输出）" if ax is ax1 else None)
    ax.axhline(1.0, color=H.DARK, lw=1.1, alpha=0.6, zorder=2)
    ax.axhline(0.1667, color=H.GOLD, lw=1.0, ls="-.", alpha=0.9, zorder=2)
    ax.axvspan(0, 0.1667, color=H.GOLD, alpha=0.10, zorder=0)
    ax.set_ylim(0, 1.12)
    ax.set_xlabel("输入亮度（显示峰值 = 1）")
    ax.set_ylabel("输出亮度\n（显示峰值 = 1）")

# ---- 左：全景 ----
ax1.set_xlim(0, PK)
ax1.set_title("(a) 全景：输入亮度可达显示峰值的 8 倍", fontsize=10.5)
ax1.text(0.10, 1.045, "显示上限：屏幕只能显示到这里", fontsize=8, color=H.DARK,
         va="bottom", ha="left")
ax1.annotate("硬裁剪\n中间调最忠实，\n高光一刀切", xy=(6.0, 1.0), xytext=(3.55, 0.34),
             fontsize=8.2, color=H.RED, ha="left",
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.1))
ax1.annotate("等比压缩\n不爆白，但整幅显暗", xy=(6.6, 0.822), xytext=(4.35, 0.055),
             fontsize=8.2, color="#6c7a89", ha="left",
             arrowprops=dict(arrowstyle="->", color=H.GRAY, lw=1.1))
ax1.text(0.16, 0.63, "中低段贴近 45° 虚线\n= 保留中间调明暗关系", fontsize=8.2,
         color="#4a5666", ha="left", zorder=6,
         bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="#c3ccd6", lw=0.7,
                   alpha=0.95))
sec1 = ax1.secondary_xaxis("top", functions=(lambda v: v * DMAX, lambda n: n / DMAX))
sec1.set_xlabel("输入亮度 / nit（设显示峰值 600 nit）", fontsize=8.5, labelpad=3)
sec1.tick_params(labelsize=7.5)

# ---- 右：放大暗部 / 中间调 ----
ax2.set_xlim(0, 1.6)
ax2.set_title("(b) 放大：暗部与中间调（0–1.6）", fontsize=10.5)
ax2.text(0.085, 0.52, "SDR 参考白\n100 nit 以下", fontsize=7.2, color="#a07d1f",
         rotation=90, va="center", ha="center")
ax2.text(0.055, 0.975,
         "同一输入下更亮：\n等比压缩 < Hable\n< Reinhard < 硬裁剪\n< ACES",
         fontsize=7.6, color="#33475b", ha="left", va="top",
         bbox=dict(boxstyle="round,pad=0.30", fc="#f7f9fb", ec="#c3ccd6", lw=0.8))
sec2 = ax2.secondary_xaxis("top", functions=(lambda v: v * DMAX, lambda n: n / DMAX))
sec2.set_xlabel("输入亮度 / nit", fontsize=8.5, labelpad=3)
sec2.tick_params(labelsize=7.5)

h, l = ax1.get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3, fontsize=8.0,
           bbox_to_anchor=(0.5, -0.045), handlelength=2.1, columnspacing=1.0,
           labelspacing=0.35)
fig.suptitle("四种色调映射曲线：谁把高光压得最巧、谁把中间调保得最好",
             fontsize=12.5, fontweight="bold", y=0.975)

H.save(fig, 17, "f1_tm_curves")
