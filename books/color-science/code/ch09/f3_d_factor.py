# -*- coding: utf-8 -*-
"""图 9-5　适应度 D 随适应场亮度的变化，以及 D 对适应结果的影响。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import observer_model as OM
plt = H.plt


def D_of_LA(LA, F=1.0):
    return np.clip(F * (1.0 - (1.0 / 3.6) * np.exp((-np.asarray(LA) + 42.0) / 92.0)),
                   0.0, 1.0)


for LA in (10, 48, 100, 203, 600, 1000):
    print(f"LA={LA:5d}  D(F=1)={D_of_LA(LA,1.0):.3f}  D(F=0.9)={D_of_LA(LA,0.9):.3f}"
          f"  D(F=0.8)={D_of_LA(LA,0.8):.3f}")

fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.9),
                         gridspec_kw=dict(wspace=0.29, width_ratios=[1.0, 1.02]))
fig.subplots_adjust(bottom=0.26)

ax = axes[0]
LA = np.logspace(0, 3.7, 400)
for F, c, nm in [(1.0, H.NAVY, "平均环绕 $F=1.0$"),
                 (0.9, H.ORANGE, "昏暗环绕 $F=0.9$"),
                 (0.8, H.TEAL, "暗环绕 $F=0.8$")]:
    ax.plot(LA, D_of_LA(LA, F), color=c, lw=1.8, label=nm)
for x, txt, ha, dx in [(48, "影院 48", "right", 1.0 / 1.2), (203, "参考白 203", "left", 1.2)]:
    ax.axvline(x, color=H.GRAY, ls=":", lw=1.0)
    ax.annotate(txt, (x * dx, 0.425), fontsize=7.8, color="#6b7887",
                ha=ha, va="bottom")
ax.set_xscale("log")
ax.set_xlim(1, 5000)
ax.set_ylim(0.40, 1.03)
ax.set_xlabel("适应场亮度 $L_A$（$\\mathrm{cd/m^2}$）")
ax.set_ylabel("适应度 $D$")
ax.legend(loc="upper left", fontsize=8.2)

ax = axes[1]
stim = np.array([[0.36, 0.28, 0.14],
                 [0.28, 0.32, 0.12],
                 [0.24, 0.26, 0.30]])
names = ["暖红", "黄绿", "浅蓝"]
cols = [H.RED, H.GREEN, H.NAVY]
Ds = np.linspace(0, 1, 41)
allu, allv = [], []
for k in range(3):
    P = np.array([OM.apply_cat(stim[k], OM.M_BFD, OM.A_WH, OM.D65, D=d)
                  for d in Ds])
    u, v = OM.xyz_to_uv(P[:, 0], P[:, 1], P[:, 2])
    allu.append(u)
    allv.append(v)
    ax.plot(u, v, color=cols[k], lw=1.6, label=names[k])
    for d, mk in [(0.0, "o"), (0.5, "s"), (1.0, "^")]:
        Q = OM.apply_cat(stim[k], OM.M_BFD, OM.A_WH, OM.D65, D=d)
        uu, vv = OM.xyz_to_uv(*Q)
        ax.plot([uu], [vv], mk, color=cols[k], ms=5.5, mfc="white", mew=1.4)
    p0 = OM.apply_cat(stim[k], OM.M_BFD, OM.A_WH, OM.D65, D=0.5)
    p1 = OM.apply_cat(stim[k], OM.M_BFD, OM.A_WH, OM.D65, D=1.0)
    u0, v0 = OM.xyz_to_uv(*p0)
    u1, v1 = OM.xyz_to_uv(*p1)
    print(f"{names[k]}: D=0.5 与 D=1 相差 {np.hypot(u1 - u0, v1 - v0):.4f}")

P = np.array([OM.apply_cat(OM.A_WH, OM.M_BFD, OM.A_WH, OM.D65, D=d) for d in Ds])
u, v = OM.xyz_to_uv(P[:, 0], P[:, 1], P[:, 2])
allu.append(u)
allv.append(v)
ax.plot(u, v, "--", color=H.GRAY, lw=1.3, label="中性轴")
ax.set_xlabel("$u'$")
ax.set_ylabel("$v'$")
leg1 = ax.legend(loc="upper right", fontsize=8.2, handlelength=1.6)
from matplotlib.lines import Line2D
proxies = [Line2D([], [], marker=m, ls="none", color="#5a6779", mfc="white",
                  mew=1.4, ms=5.5, label=t)
           for m, t in [("o", "$D=0$"), ("s", "$D=0.5$"), ("^", "$D=1$")]]
ax.legend(handles=proxies, loc="lower right", fontsize=8.2, ncol=3,
          columnspacing=0.9, handletextpad=0.2)
ax.add_artist(leg1)
us = np.concatenate(allu)
vs = np.concatenate(allv)
ax.set_xlim(us.min() - 0.014, us.max() + 0.020)
ax.set_ylim(vs.min() - 0.012, vs.max() + 0.015)

H.save(fig, 9, "f3_d_factor")
