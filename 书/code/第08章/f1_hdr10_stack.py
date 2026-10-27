# -*- coding: utf-8 -*-
"""图 08-1：HDR10 的三件套 —— PQ（亮度）+ 10bit（精度）+ BT.2020（色彩容器）。

一句话：HDR10 不是一个技术，而是三样东西的组合，缺一样都不完整。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import numpy as np
import hdrfig as H
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ---------------- 数据 ----------------
# CIE 1931 光谱轨迹（10 nm 取样，xy 坐标，近似标准值，用于画马蹄形轮廓）
LOCUS = np.array([
    (0.1741, 0.0050), (0.1738, 0.0049), (0.1733, 0.0048), (0.1726, 0.0048),
    (0.1714, 0.0051), (0.1689, 0.0069), (0.1644, 0.0109), (0.1566, 0.0177),
    (0.1440, 0.0297), (0.1241, 0.0578), (0.0913, 0.1327), (0.0454, 0.2950),
    (0.0082, 0.5384), (0.0139, 0.7502), (0.0743, 0.8338), (0.1547, 0.8059),
    (0.2296, 0.7543), (0.3016, 0.6923), (0.3731, 0.6245), (0.4441, 0.5547),
    (0.5125, 0.4866), (0.5752, 0.4242), (0.6270, 0.3725), (0.6658, 0.3340),
    (0.6915, 0.3083), (0.7079, 0.2920), (0.7190, 0.2809), (0.7260, 0.2740),
    (0.7300, 0.2700), (0.7320, 0.2680), (0.7334, 0.2666), (0.7344, 0.2656),
    (0.7347, 0.2653),
])
SRGB = [(0.640, 0.330), (0.300, 0.600), (0.150, 0.060)]      # BT.709 / sRGB 基色
P3 = [(0.680, 0.320), (0.265, 0.690), (0.150, 0.060)]        # DCI-P3 基色
BT2020 = [(0.708, 0.292), (0.170, 0.797), (0.131, 0.046)]    # BT.2020 基色
D65 = (0.3127, 0.3290)


def plain_log(ax, which="y"):
    """对数轴用普通数字标签，避免 ASCII 字体缺字形。"""
    a = ax.yaxis if which == "y" else ax.xaxis
    a.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"{v:g}"))
    a.set_minor_formatter(mticker.NullFormatter())


fig = plt.figure(figsize=(7.2, 5.0))
gs = fig.add_gridspec(2, 3, height_ratios=[0.5, 2.6], hspace=0.40, wspace=0.34)

# ---------------- 顶部：公式条 ----------------
axf = fig.add_subplot(gs[0, :]); axf.axis("off")
axf.set_xlim(0, 1); axf.set_ylim(0, 1)


def chip(ax, x, y, text, fc, fs=8.4):
    ax.text(x, y, text, ha="center", va="center", color="white", fontsize=fs,
            fontweight="bold", zorder=3, linespacing=1.6,
            bbox=dict(boxstyle="round,pad=0.42", fc=fc, ec=fc, lw=1.0))


axf.text(0.045, 0.72, "HDR10\n＝", ha="center", va="center", fontsize=10,
         fontweight="bold", color=H.DARK, linespacing=1.7)
chip(axf, 0.290, 0.70, "PQ（ST 2084）\n亮度编码：码值 → 绝对亮度", H.NAVY)
axf.text(0.487, 0.70, "＋", ha="center", va="center", fontsize=12,
         fontweight="bold", color=H.DARK)
chip(axf, 0.640, 0.70, "10bit\n每通道 1024 级", H.ORANGE)
axf.text(0.793, 0.70, "＋", ha="center", va="center", fontsize=12,
         fontweight="bold", color=H.DARK)
chip(axf, 0.885, 0.70, "BT.2020\n色彩容器", H.TEAL)
axf.text(0.5, 0.13,
         "三件缺一不可：没有 PQ 就表达不出 10000 nit 的绝对亮度；没有 10bit，PQ 的陡峭暗部会出现色带；"
         "没有 BT.2020，颜色就没有足够大的“画布”。",
         ha="center", va="center", fontsize=8.0, color=H.DARK)

# ---------------- ① PQ 曲线 ----------------
ax1 = fig.add_subplot(gs[1, 0])
code = np.linspace(0.0, 1.0, 800)
nit = H.pq_eotf(code)
ax1.semilogy(code * 1023, nit, color=H.NAVY, lw=2.2, zorder=3)
for v, c, lab in [(100, H.GREEN, "100 nit  SDR 白点"), (1000, H.GOLD, "1000 nit 常见 HDR 屏"),
                  (10000, H.RED, "10000 nit  PQ 上限")]:
    ax1.axhline(v, color=c, ls=":", lw=1.1, zorder=2)
    ax1.text(30, v * 1.3, lab, color=c, fontsize=7.2, va="bottom")
ax1.set_xlim(0, 1023)
ax1.set_ylim(0.005, 40000)
ax1.set_xlabel("10bit 码值（0 – 1023）")
ax1.set_ylabel("绝对亮度（nit，对数轴）")
ax1.set_title("① PQ：每个码值多少 nit", fontsize=10, color=H.NAVY, pad=7)
ax1.grid(True, which="both", alpha=0.55)
plain_log(ax1, "y")
ax1.annotate("暗部陡、亮部平：\n码值大量让给暗部",
             xy=(150, 1.2), xytext=(330, 0.02), fontsize=7.2, color=H.GRAY,
             arrowprops=dict(arrowstyle="->", color=H.GRAY, lw=0.9))

# ---------------- ② 10bit 台阶 ----------------
ax2 = fig.add_subplot(gs[1, 1])
c8 = np.arange(26, 37) / 255.0             # 8bit 码值 26–36（暗部一小段）
c10 = np.arange(103, 144) / 1023.0         # 10bit 码值 103–143（同一亮度区段）
ax2.step(c8 * 1023, H.pq_eotf(c8), where="post", color=H.ORANGE, lw=2.0,
         label="8bit：10 级粗台阶")
ax2.step(c10 * 1023, H.pq_eotf(c10), where="post", color=H.TEAL, lw=1.6,
         label="10bit：40 级细台阶")
ax2.set_yscale("log")
ax2.set_xlim(102, 144)
ax2.set_ylim(0.30, 1.6)
ax2.legend(loc="upper left", fontsize=7.4, handlelength=1.6)
ax2.set_xlabel("码值（同一段暗部亮度）")
ax2.set_ylabel("亮度（nit，对数轴）")
ax2.set_title("② 10bit：暗部台阶细 4 倍", fontsize=10, color=H.ORANGE, pad=7)
ax2.grid(True, which="both", alpha=0.55)
plain_log(ax2, "y")
ax2.annotate("8bit 的台阶\n肉眼可见\n→ 暗部色带",
             xy=(138, 1.02), xytext=(124.5, 0.325), fontsize=7.2, color=H.ORANGE,
             ha="left", va="bottom",
             arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=0.9))

# ---------------- ③ BT.2020 容器 ----------------
ax3 = fig.add_subplot(gs[1, 2])
clip = np.r_[LOCUS[:, 0], LOCUS[0, 0]], np.r_[LOCUS[:, 1], LOCUS[0, 1]]
ax3.fill(clip[0], clip[1], color="#f5f8fb", zorder=1)
ax3.plot(clip[0], clip[1], color=H.GRAY, lw=1.1, zorder=2)


def tri(pts, color, ls, lw, label=None, fill=None, z=3):
    p = np.array(pts + [pts[0]])
    if fill:
        ax3.fill(p[:, 0], p[:, 1], color=fill, alpha=0.18, zorder=z - 1)
    ax3.plot(p[:, 0], p[:, 1], color=color, ls=ls, lw=lw, label=label, zorder=z)


tri(BT2020, H.TEAL, "-", 2.0, "BT.2020（标准规定的容器）", fill=H.TEAL)
tri(P3, H.ORANGE, "--", 1.5, "DCI-P3（多数设备实际水平）")
tri(SRGB, H.NAVY, "-", 1.3, "sRGB / BT.709（SDR 老画布）")
ax3.plot(*D65, marker="o", ms=4.5, color=H.RED, zorder=5)
ax3.text(D65[0] + 0.015, D65[1] + 0.028, "D65 白点", fontsize=7.2, color=H.RED)
ax3.set_xlim(0.0, 0.80); ax3.set_ylim(0.0, 0.90)
ax3.set_xlabel("色度 x"); ax3.set_ylabel("色度 y")
ax3.set_title("③ BT.2020：更大的色彩容器", fontsize=10, color=H.TEAL, pad=7)
ax3.legend(loc="lower right", fontsize=6.6, handlelength=1.5,
           borderaxespad=0.25, labelspacing=0.3)
fig.text(0.5, 0.005,
         "容器 ≠ 能力：标准只规定 HDR10 用 BT.2020 这套坐标描述颜色，不代表屏幕真能显示全部 BT.2020；"
         "绝大多数设备实际只覆盖到 DCI-P3 附近，剩余部分靠显示端映射。",
         ha="center", va="bottom", fontsize=7.2, color=H.DARK)

H.save(fig, 8, "f1_hdr10_stack")
