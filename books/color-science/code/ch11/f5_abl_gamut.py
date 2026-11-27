# -*- coding: utf-8 -*-
"""第 11 章 图 5：平均图像电平（APL）对峰值亮度与可达色度的压缩。

左图：恒功率预算下的峰值亮度模型 L(APL) = L_peak / (1 + c·APL^p)，
      c 由"全屏白只有小窗口峰值 22%"定出，p 取 0.8。
右图：把绝对亮度钉在 200 cd/m² 时，不同 APL 下还能达到哪些色度。
      亮度够不着的色度点就是显示不出来的颜色，红蓝两个角先塌。

基色用 BT.2020，矩阵由本册第 7 章的方法解出；模型参数是假设值，只用于示意趋势。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.ndimage import gaussian_filter
import primaries11 as P

plt = H.plt

prim = [P.PRIMARIES["BT2020"][k] for k in "RGB"]
M, S = P.covering_matrix(prim, P.WHITE["D65"], 1.0)
Minv = np.linalg.inv(M)

LP, C0, PP = 1000.0, 1.0 / 0.22 - 1.0, 0.8


def peak_lum(apl):
    return LP / (1.0 + C0 * apl ** PP)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.7),
                               gridspec_kw=dict(wspace=0.30, left=0.085,
                                                right=0.975, top=0.925, bottom=0.145))

# ---------------- 左图 ----------------
apl = np.linspace(0.002, 1.0, 500)
ax1.plot(apl * 100, peak_lum(apl), color=H.NAVY, lw=2.2)
ax1.axhline(LP * 0.22, color="#9aa6b2", lw=0.9, ls=(0, (3, 3)))

marks = [0.03, 0.10, 0.25, 0.50, 1.00]
for a in marks:
    L = peak_lum(a)
    ax1.plot([a * 100], [L], marker="o", ms=5.4, mfc="white", mec=H.ORANGE, mew=1.6,
             zorder=6)
ax1.text(5.0, 858, f"3% 窗口\n{peak_lum(0.03):.0f} nit", fontsize=7.4,
         color=H.ORANGE, ha="left", va="bottom")
ax1.text(14.5, 700, f"10%  APL\n{peak_lum(0.10):.0f} nit", fontsize=7.4,
         color=H.ORANGE, ha="left", va="center")
ax1.text(31, 545, f"25%  APL\n{peak_lum(0.25):.0f} nit", fontsize=7.4,
         color=H.ORANGE, ha="left", va="center")
ax1.text(53, 440, f"50%  APL\n{peak_lum(0.5):.0f} nit", fontsize=7.4,
         color=H.ORANGE, ha="left", va="center")
ax1.text(97, 172, f"全屏白\n{peak_lum(1.0):.0f} nit", fontsize=7.4,
         color=H.ORANGE, ha="right", va="center")
ax1.text(38, 140, "恒功率预算的底：峰值的两成", fontsize=7.2,
         color="#697580", ha="center", va="bottom")
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 1080)
ax1.set_xlabel("平均图像电平 APL（%）")
ax1.set_ylabel(r"可达峰值亮度（cd/m$^2$）")
ax1.set_title("(a) 峰值亮度随 APL 下降", fontsize=9.2, pad=6)

# ---------------- 右图 ----------------
Y_FIX = 200.0
xs = np.linspace(0.02, 0.78, 620)
ys = np.linspace(0.02, 0.88, 620)
XX, YY = np.meshgrid(xs, ys)
den = XX + YY + (1 - XX - YY)
XYZ = np.stack([XX * Y_FIX / YY, np.full_like(XX, Y_FIX),
                (1 - XX - YY) * Y_FIX / YY], axis=0)
RGBv = np.tensordot(Minv, XYZ, axes=1)
ok = np.all(RGBv <= 1.0 + 1e-9, axis=0) & np.all(RGBv >= -1e-9, axis=0)
fin = np.isfinite(ok)
mask = np.where(fin, ok.astype(float), 0.0)
sm = gaussian_filter(mask, 1.6)

U, V = P.xy_to_uv76(XX, YY)

colors = {1.0: H.RED, 0.75: "#3d7ab5", 0.5: "#1f4e79", 0.25: "#12233b"}
label_done = {}
for a in (1.0, 0.75, 0.5, 0.25):
    Lp = peak_lum(a)
    okA = np.all(np.tensordot(Minv, XYZ / Lp, axes=1) <= 1.0 + 1e-9, axis=0) & np.all(RGBv >= -1e-9, axis=0)
    smA = gaussian_filter(np.where(np.isfinite(okA), okA.astype(float), 0.0), 1.6)
    ax2.contour(U, V, smA, levels=[0.5], colors=[colors[a]], linewidths=2.0,
                zorder=5)

for a, col in colors.items():
    ax2.plot([], [], color=col, lw=2.0,
             label=f"APL {int(round(a * 100))}%，峰值 {peak_lum(a):.0f} nit")

uv = np.array([P.xy_to_uv76(*q) for q in prim])
ax2.plot(np.append(uv[:, 0], uv[0, 0]), np.append(uv[:, 1], uv[0, 1]),
         color=H.GRAY, lw=1.2, ls=(0, (4, 3)), zorder=4, label="BT.2020 三角形")
ax2.plot([0.1978], [0.4683], marker="+", ms=7, color="#38424e", mew=1.3, zorder=6)

ax2.set_xlim(0.02, 0.62)
ax2.set_ylim(0.05, 0.625)
ax2.set_aspect("equal")
ax2.set_xlabel("u′")
ax2.set_ylabel("v′")
ax2.set_title(r"(b) 200 cd/m$^2$ 时可达到的色度范围", fontsize=9.2, pad=6)
ax2.legend(loc="lower right", fontsize=6.9, handlelength=1.7, borderpad=0.45,
           labelspacing=0.3)

H.save(fig, 11, "f5_abl_gamut")
for a in (0.03, 0.10, 0.25, 0.50, 1.00):
    print(f"APL {a*100:4.0f}% -> {peak_lum(a):.0f} nit")
print(f"red   max at APL100: {S[0]*peak_lum(1.0):.0f} nit")
print(f"green max at APL100: {S[1]*peak_lum(1.0):.0f} nit")
print(f"blue  max at APL100: {S[2]*peak_lum(1.0):.0f} nit")
print(f"ratio APL100/APL25: {peak_lum(1.0)/peak_lum(0.25):.3f}")
