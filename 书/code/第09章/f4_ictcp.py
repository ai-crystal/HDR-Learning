# -*- coding: utf-8 -*-
"""图 09-4：YCbCr 与 ICtCp —— 两条色彩编码路线的对比（示意）。"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.patches as mp

fig, ax = H.plt.subplots(figsize=(7.2, 4.3))
ax.set_xlim(0, 100); ax.set_ylim(0, 62); ax.axis("off"); ax.grid(False)

def box(x, y, w, h, text, fc, ec, tc, fs=8.4):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                                   fc=fc, ec=ec, lw=1.1))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", color=tc, fontsize=fs,
            fontweight="bold", linespacing=1.4)

def arrow(x0, y0, x1, y1, c=H.NAVY):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=c, lw=1.3))

# 行 A：YCbCr
ax.text(2, 52, "① YCbCr（传统视频）", fontsize=10, fontweight="bold", color=H.RED)
seqA = [("线性/编码\nRGB", "#eaf0f6", H.NAVY, H.DARK),
        ("Y′ = 0.263R′+0.678G′\n+0.059B′（亮度＝luma）", "#fdecea", H.RED, "#7a2018"),
        ("Cb, Cr\n（两个色差）", "#fdecea", H.RED, "#7a2018")]
xs = [3, 33, 66]
for i, (t, fc, ec, tc) in enumerate(seqA):
    box(xs[i], 40, 28, 10, t, fc, ec, tc, 8.2)
    if i < 2:
        arrow(xs[i]+28, 45, xs[i+1], 45)
ax.text(50, 36.5, "非恒定亮度：饱和色下 luma 与真实亮度偏差大；色度子采样时更容易出错",
        ha="center", fontsize=7.8, color=H.GRAY)

# 行 B：ICtCp
ax.text(2, 27, "② ICtCp（HDR/广色域设计）", fontsize=10, fontweight="bold", color=H.TEAL)
seqB = [("线性 RGB", "#e8f6f3", H.TEAL, "#0e5a4d"),
        ("→ LMS\n（长/中/短锥响应）", "#e8f6f3", H.TEAL, "#0e5a4d"),
        ("PQ 编码\nL′M′S′", "#e8f6f3", H.TEAL, "#0e5a4d"),
        ("I + Ct + Cp\n（强度＋色度）", "#e8f6f3", H.TEAL, "#0e5a4d")]
xsB = [3, 26, 49, 72]
for i, (t, fc, ec, tc) in enumerate(seqB):
    box(xsB[i], 14, 20, 10, t, fc, ec, tc, 7.8)
    if i < 3:
        arrow(xsB[i]+20, 19, xsB[i+1], 19, H.TEAL)
ax.text(50, 10.5, "为 HDR 与广色域设计：强度通道更稳、色度子采样更友好，被杜比视界采用",
        ha="center", fontsize=7.8, color=H.GRAY)

# 底部对照带
ax.add_patch(mp.FancyBboxPatch((3, 1.5), 95, 6, boxstyle="round,pad=0.4,rounding_size=1.2",
                               fc="#f3f6fa", ec="#c3ccd6", lw=1.0))
ax.text(50, 4.5, "一句话：YCbCr 是「亮度＋色差」的老办法；ICtCp 换用锥体响应，为 HDR 与宽色域重新设计。",
        ha="center", va="center", fontsize=8.4, color=H.DARK, fontweight="bold")

ax.set_title("两条色彩编码路线：YCbCr vs ICtCp", fontsize=13, fontweight="bold", pad=8)
H.save(fig, 9, "f4_ictcp")
