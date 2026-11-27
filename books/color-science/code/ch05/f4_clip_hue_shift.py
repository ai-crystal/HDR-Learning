# -*- coding: utf-8 -*-
"""第 05 章 图 4：逐通道裁剪的映射轨迹与色相偏移。

源色域 BT.2020，目标色域 Display P3，取 L* = 50 的 a*b* 平面。
左图：两条色域边界与该平面上的映射轨迹（逐通道裁剪、等色相裁剪、膝形压缩）。
右图：逐通道裁剪在 12 个色相方向上造成的色相偏移（取超出边界 20% 的颜色）。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import gamut as G

plt = H.plt

SRC, DST = "BT2020", "P3"
L0 = 50.0


def boundary(name, L, n=360):
    h = np.linspace(0, 360, n)
    C = np.array([G.max_chroma(L, hi, name) for hi in h])
    return G.lch_to_lab(np.full(n, L), C, h)


def clamp_map(lab):
    rgb = np.clip(G.lab_to_rgb(lab, DST), 0.0, 1.0)
    return G.rgb_to_lab(rgb, DST)


def clip_hue(lab):
    L, C, h = G.lab_to_lch(lab)
    Cm = np.array([G.max_chroma(Li, hi, DST) for Li, hi in zip(np.atleast_1d(L), np.atleast_1d(h))])
    return G.lch_to_lab(np.atleast_1d(L), np.minimum(np.atleast_1d(C), Cm), h)


def knee_lab(lab):
    L, C, h = G.lab_to_lch(lab)
    out = []
    for Li, hi, ci in zip(np.atleast_1d(L), np.atleast_1d(h), np.atleast_1d(C)):
        Cm = G.max_chroma(Li, hi, DST)
        out.append(float(G.knee_map(np.array([ci]), 0.85 * Cm, Cm)[0]))
    return G.lch_to_lab(np.atleast_1d(L), np.array(out), h)


fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.1),
                         gridspec_kw=dict(width_ratios=[1.22, 1.0], wspace=0.26))
fig.subplots_adjust(left=0.085, right=0.985, top=0.90, bottom=0.155)

# ---------------- (a) 映射轨迹 ----------------
ax = axes[0]
b_src = boundary(SRC, L0)
b_dst = boundary(DST, L0)
ax.plot(b_src[:, 1], b_src[:, 2], color="#9aa7b5", lw=1.4, ls=(0, (5, 2.5)))
ax.plot(np.append(b_dst[:, 1], b_dst[0, 1]), np.append(b_dst[:, 2], b_dst[0, 2]),
        color=H.NAVY, lw=1.8)


for h in (35.0, 145.0, 262.0):
    Cmax = G.max_chroma(L0, h, SRC)
    ax.plot([0, Cmax * np.cos(np.radians(h))], [0, Cmax * np.sin(np.radians(h))],
            color="#c2cad4", lw=0.9, ls=(0, (3, 3)), zorder=1)
    ax.text(0.22 * Cmax * np.cos(np.radians(h)), 0.22 * Cmax * np.sin(np.radians(h)),
            f"{h:.0f}°", fontsize=7.6, color="#6b7886", ha="center", va="center",
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="none", pad=1.0))
    Csrc = np.linspace(0.42 * Cmax, Cmax, 7)
    src = G.lch_to_lab(np.full(7, L0), Csrc, np.full(7, h))
    out_clamp = clamp_map(src)
    out_clip = clip_hue(src)
    out_knee = knee_lab(src)
    ax.plot(src[:, 1], src[:, 2], "o", ms=5.0, mfc="white", mec="#7f8c8d", mew=1.3,
            zorder=4)
    for i in range(7):
        ax.annotate("", xy=(out_clamp[i, 1], out_clamp[i, 2]),
                    xytext=(src[i, 1], src[i, 2]),
                    arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=1.0,
                                    shrinkA=3.0, shrinkB=3.0), zorder=3)
    ax.plot(out_clip[:, 1], out_clip[:, 2], "s", ms=4.2, mfc=H.TEAL,
            mec="#0f5f50", mew=0.5, zorder=5)
    ax.plot(out_knee[:, 1], out_knee[:, 2], "^", ms=4.6, mfc=H.ORANGE,
            mec="#8a5a12", mew=0.5, zorder=5)

ax.plot([], [], "-", color="#9aa7b5", lw=1.4, ls=(0, (5, 2.5)), label="BT.2020 边界")
ax.plot([], [], "-", color=H.NAVY, lw=1.8, label="Display P3 边界")
ax.plot([], [], "o", ms=5.0, mfc="white", mec="#7f8c8d", mew=1.3, label="源色（BT.2020）")
ax.plot([], [], "o", ms=4.6, mfc=H.RED, label="逐通道裁剪")
ax.plot([], [], "s", ms=4.2, mfc=H.TEAL, label="等色相裁剪")
ax.plot([], [], "^", ms=4.6, mfc=H.ORANGE, label="膝形压缩")
ax.legend(loc="lower right", fontsize=7.0, handletextpad=0.5, borderpad=0.35)
ax.set_xlim(-118, 120)
ax.set_ylim(-96, 104)
ax.set_aspect("equal")
ax.set_xlabel("$a^*$（$L^*=50$）", fontsize=9.5)
ax.set_ylabel("$b^*$", fontsize=9.5)

# ---------------- (b) 色相偏移 ----------------
ax2 = axes[1]
HUE = np.arange(0, 360, 30)
dh = []
for h in HUE:
    Cm = G.max_chroma(L0, h, DST)
    lab = G.lch_to_lab(np.array([L0]), np.array([1.20 * Cm]), np.array([h]))
    out = clamp_map(lab)
    _, _, h2 = G.lab_to_lch(out)
    dh.append(((h2[0] - h + 180) % 360) - 180)
dh = np.array(dh)
cols = [H.RED if abs(v) > 2 else H.GRAY for v in dh]
ax2.bar(np.arange(len(HUE)), dh, color=cols, width=0.66, edgecolor="#3b4653",
        linewidth=0.6)
ax2.axhline(0, color="#4a5666", lw=1.0)
for y in (2, -2):
    ax2.axhline(y, color=H.RED, lw=0.9, ls=(0, (4, 2.5)))
ax2.text(len(HUE) - 0.6, 2.5, "±2° 可察觉线", fontsize=7.2, color=H.RED, ha="right")
ax2.set_xticks(np.arange(len(HUE)))
ax2.set_xticklabels([str(h) for h in HUE], fontsize=7.4)
ax2.set_xlabel("源色的 CIELAB 色相角（°）", fontsize=9.5)
ax2.set_ylabel("裁剪后的色相偏移 $\\Delta h$（°）", fontsize=9.5)
ax2.set_ylim(-17, 12)
ax2.grid(axis="x", visible=False)

H.save(fig, 5, "f4_clip_hue_shift")
