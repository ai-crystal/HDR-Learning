# -*- coding: utf-8 -*-
"""图 9-2　四组 CAT 矩阵的光谱选择性：长波行响应曲线与 450 nm 处的通道响应。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import observer_model as OM
plt = H.plt

lam = OM.LAM
cats = [("Bradford", OM.M_BFD, H.NAVY), ("CAT02", OM.M_CAT02, H.ORANGE),
        ("CAT16", OM.M_CAT16, H.RED), ("CMCCAT2000", OM.M_CMCCAT2000, H.TEAL)]
resp = {n: OM.CMF_STD @ M.T for n, M, _ in cats}


def fwhm(x, y):
    y = y / y.max()
    i = int(np.argmax(y))
    xl = xr = np.nan
    for j in range(i, 0, -1):
        if y[j - 1] <= 0.5:
            xl = np.interp(0.5, [y[j - 1], y[j]], [x[j - 1], x[j]])
            break
    for j in range(i, len(y) - 1):
        if y[j + 1] <= 0.5:
            xr = np.interp(0.5, [y[j], y[j + 1]], [x[j], x[j + 1]])
            break
    return xr - xl

fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.1),
                         gridspec_kw=dict(wspace=0.30, width_ratios=[1.22, 1.0]))
fig.subplots_adjust(bottom=0.28)

ax = axes[0]
for name, M, c in cats:
    y = resp[name][:, 0] / resp[name][:, 0].max()
    w = fwhm(lam, resp[name][:, 0])
    print(f"{name:12s} L row: peak {lam[np.argmax(y)]:.0f} nm, FWHM {w:.0f} nm")
    ax.plot(lam, y, color=c, lw=1.6, label=f"{name}，{w:.0f} nm")
ax.axhline(0.5, color=H.GRAY, ls=":", lw=1.0)
ax.text(700, 0.52, "半高", fontsize=8, color=H.GRAY, ha="right")
ax.set_xlim(380, 720)
ax.set_ylim(0, 1.34)
ax.set_xlabel("波长（nm）")
ax.set_ylabel("归一化的长波行响应")
ax.legend(loc="upper center", fontsize=8, ncol=2, labelspacing=0.35,
          title="长波行的半高宽", title_fontsize=8, columnspacing=1.0)

ax = axes[1]
i450 = int(np.where(lam == 450.0)[0][0])
names = [n for n, _, _ in cats]
xl = np.arange(len(names))
wbar = 0.36
vL = [resp[n][i450, 0] for n in names]
vM = [resp[n][i450, 1] for n in names]
b1 = ax.bar(xl - wbar / 2, vL, wbar, color=H.BLUE, label="长波通道 $L$")
b2 = ax.bar(xl + wbar / 2, vM, wbar, color=H.GOLD, label="中波通道 $M$")
ax.axhline(0, color="#4a5666", lw=0.9)
ax.set_xticks(xl)
ax.set_xticklabels(names, fontsize=8.5)
ax.set_ylim(-0.21, 0.15)
ax.set_ylabel("450 nm 单色光的通道响应")
for i, n in enumerate(names):
    ax.annotate(f"{vL[i]:+.3f}", (i - wbar / 2, vL[i]), ha="center",
                va="bottom" if vL[i] > 0 else "top", fontsize=7.2,
                color=H.DARK, xytext=(0, 2 if vL[i] > 0 else -2),
                textcoords="offset points")
    ax.annotate(f"{vM[i]:+.3f}", (i + wbar / 2, vM[i]), ha="center",
                va="bottom" if vM[i] > 0 else "top", fontsize=7.2,
                color=H.DARK, xytext=(0, 2 if vM[i] > 0 else -2),
                textcoords="offset points")
svals = "、".join(f"{resp[n][i450, 2]:.2f}" for n in names)
ax.annotate("短波通道 $S$ 未画\n" + svals, (0.02, 0.985), xycoords="axes fraction",
            va="top", fontsize=7.4, color="#5a6779", linespacing=1.4)

fig.legend(handles=[b1, b2], loc="lower center", ncol=2, fontsize=8.5,
           bbox_to_anchor=(0.755, 0.005), frameon=False)
H.save(fig, 9, "f2_cat_matrix_response")
