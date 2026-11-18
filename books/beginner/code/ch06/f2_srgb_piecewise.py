# -*- coding: utf-8 -*-
"""图 06-2：sRGB 分段 EOTF —— 暗部直线 + 亮部 2.4 次方，并放大低段。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt

fig, (axL, axR) = H.plt.subplots(1, 2, figsize=(7.2, 4.0),
                                 gridspec_kw=dict(width_ratios=[1.15, 1.0]))

v = np.linspace(0, 1, 1200)
srgb = H.srgb_eotf(v)
p24 = v ** 2.4
p22 = v ** 2.2
Vt, Lt = 0.04045, 0.0031308

# ---------------- 左：整条曲线 ----------------
axL.plot(v, p22, color=H.LGRAY, lw=1.6, label="纯 Gamma 2.2")
axL.plot(v, p24, color=H.TEAL, lw=1.6, ls="--", label="纯 Gamma 2.4")
axL.plot(v, srgb, color=H.NAVY, lw=2.8, label="sRGB 分段 EOTF")
axL.plot(v, v, color=H.GRAY, lw=1.3, ls=":", label="线性（参照）")

axL.plot(Vt, Lt, "o", color=H.RED, ms=7, zorder=6)
axL.annotate(f"接缝点 V={Vt:.5f}\nL={Lt:.7f}", xy=(Vt, Lt), xytext=(0.17, 0.075),
             fontsize=8.5, color=H.RED,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.1))
axL.axvline(Vt, color=H.RED, lw=0.9, ls=":")
axL.axhline(Lt, color=H.RED, lw=0.9, ls=":")

axL.set_xlim(0, 1); axL.set_ylim(0, 1.02)
axL.set_xlabel("码值 V（0–1）")
axL.set_ylabel("线性亮度 L（0–1）")
axL.set_title("sRGB EOTF：整条曲线（整体≈2.2）", fontsize=11)
axL.legend(loc="upper left", fontsize=8)
axL.text(0.50, 0.135, "码值 0.5 → L=0.2140\n（比 2.2 略低，比 2.4 略高）",
         fontsize=8.5, color=H.DARK,
         bbox=dict(boxstyle="round,pad=0.35", fc="#f4f7fa", ec=H.LGRAY, lw=0.8))
axL.text(0.50, 0.020,
         "V ≤ 0.04045：L = V/12.92（直线）\nV > 0.04045：L = ((V+0.055)/1.055)$^{2.4}$",
         fontsize=8.3, color=H.RED, va="bottom", ha="left")
axL.plot(0.5, H.srgb_eotf(0.5), "o", color=H.NAVY, ms=5, zorder=6)

# ---------------- 右：放大低段 ----------------
vz = np.linspace(0, 0.12, 800)
axR.plot(vz, H.srgb_eotf(vz), color=H.NAVY, lw=2.8, label="sRGB 分段 EOTF")
axR.plot(vz, vz ** 2.4, color=H.TEAL, lw=1.6, ls="--", label="纯 Gamma 2.4（暗部太陡）")
# 线性段延长线
xe = np.linspace(0, 0.09, 10)
axR.plot(xe, xe / 12.92, color=H.RED, lw=1.5, ls="-.", label=r"直线段 $L=V/12.92$")

axR.set_xlim(0, 0.09)
axR.set_ylim(0, 0.0075)
axR.axvline(Vt, color=H.RED, lw=0.9, ls=":")
axR.axhline(Lt, color=H.RED, lw=0.9, ls=":")
axR.plot(Vt, Lt, "o", color=H.RED, ms=7, zorder=6)
axR.annotate("接缝点\n（两段斜率连续）", xy=(Vt, Lt),
             xytext=(0.008, 0.0042), fontsize=8.2, color=H.RED, va="bottom",
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.1))

axR.set_xlabel("码值 V（低段放大 0–0.09）")
axR.set_ylabel("线性亮度 L")
axR.set_title("放大暗部：为什么需要“掰直”", fontsize=11)
axR.legend(loc="upper left", fontsize=8)

fig.suptitle("sRGB 的分段 EOTF：暗部走直线、亮部约 2.4 次方", fontweight="bold", y=1.0)
fig.tight_layout()
H.save(fig, 6, "f2_srgb_piecewise")
