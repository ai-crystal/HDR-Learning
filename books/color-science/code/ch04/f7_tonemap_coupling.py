# -*- coding: utf-8 -*-
"""第 04 章 图 7：纯亮度映射对色貌的连带影响。

母版：峰值 1000 cd/m$^2$，L_A = 200；显示：峰值 203 cd/m$^2$，L_A = 40。
用一条膝形曲线把母版亮度压到显示峰值（保色度、只改亮度），
再用 CAM16 重算色貌坐标，看 J'、M'、C 与色相如何随之变化。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cam02 as C
import cie1931 as S

plt = H.plt

L_M, L_D = 1000.0, 203.0
Wm = C.xy_to_XYZ(0.3127, 0.3290, L_M)
Wd = C.xy_to_XYZ(0.3127, 0.3290, L_D)


def knee(x, p=0.5, m=0.2):
    """归一化膝形曲线：x<=p 恒等，x>p 用三次 Hermite 收到 1（在 p 处一阶连续）。"""
    x = np.asarray(x, dtype=float)
    t = np.clip((x - p) / (1.0 - p), 0.0, 1.0)
    h00 = 2 * t ** 3 - 3 * t ** 2 + 1
    h10 = t ** 3 - 2 * t ** 2 + t
    h01 = -2 * t ** 3 + 3 * t ** 2
    h11 = t ** 3 - t ** 2
    f = h00 * p + h10 * (1 - p) + h01 * 1.0 + h11 * (1 - p) * m
    return np.clip(np.where(x <= p, x, f), 0.0, 1.0)


def xyz(x, y, Y):
    return np.array([x * Y / y, Y, (1.0 - x - y) * Y / y])


HUES = [("肤色", 0.40, 0.36), ("红", 0.55, 0.33), ("绿", 0.28, 0.52), ("蓝", 0.18, 0.16)]
LEVELS = [10.0, 40.0, 160.0, 640.0, 1000.0]

fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.9),
                         gridspec_kw=dict(width_ratios=[1.12, 1.0], wspace=0.29))
fig.subplots_adjust(left=0.085, right=0.985, top=0.90, bottom=0.155)

# ---------------- (a) J'–M' 平面上的位移 ----------------
ax = axes[0]
data = {}
for name, x, y in HUES:
    Jp0, Mp0, Jp1, Mp1, pts = [], [], [], [], []
    for Y in LEVELS:
        a = C.cam16(xyz(x, y, Y), Wm, LA=200.0)
        Y2 = float(knee(Y / L_M) * L_D)
        b = C.cam16(xyz(x, y, Y2), Wd, LA=40.0)
        j0, _, _ = C.cam16_ucs(a)
        j1, _, _ = C.cam16_ucs(b)
        m0 = np.log1p(0.0228 * a["M"]) / 0.0228
        m1 = np.log1p(0.0228 * b["M"]) / 0.0228
        Jp0.append(float(j0)); Mp0.append(float(m0))
        Jp1.append(float(j1)); Mp1.append(float(m1))
        pts.append((float(j0), float(m0), float(j1), float(m1)))
    data[name] = dict(master=np.array(pts), a=a, b=b)
    face = np.clip(S.xyz_to_srgb01(*C.xy_to_XYZ(x, y, 30.0)) * 0.72 + 0.06, 0, 1)
    for (j0, m0, j1, m1) in pts:
        ax.annotate("", xy=(m1, j1), xytext=(m0, j0),
                    arrowprops=dict(arrowstyle="-|>", color="#59687a", lw=0.95,
                                    shrinkA=3.4, shrinkB=3.4), zorder=3)
    ax.plot(Mp0, Jp0, "o", ms=5.6, mfc="white", mec=face, mew=1.5, zorder=4)
    ax.plot(Mp1, Jp1, "o", ms=5.0, mfc=face, mec="#3b4653", mew=0.6, zorder=5)

ax.set_xlabel("$M'$（CAM16-UCS 色彩量）", fontsize=9.5)
ax.set_ylabel("$J'$（CAM16-UCS 明度）", fontsize=9.5)
ax.set_xlim(8, 80)
ax.set_ylim(4, 112)
ax.plot([], [], "o", ms=5.6, mfc="white", mec="#4a5666", mew=1.5, label="母版 1000 cd/m$^2$ 下的色样")
ax.plot([], [], "o", ms=5.0, mfc="#4a5666", mec="#3b4653", label="映射到 203 cd/m$^2$ 后")
ax.legend(loc="upper left", fontsize=7.4, handletextpad=0.45, borderpad=0.35)
ax.annotate("同一色度、只改亮度，\n箭头几乎水平向左", xy=(30, 34), xytext=(38, 20),
            fontsize=7.4, color="#39485a",
            arrowprops=dict(arrowstyle="-|>", color="#39485a", lw=0.9,
                            shrinkA=2, shrinkB=3))

# ---------------- (b) 明度、彩度、色彩量的相对变化 ----------------
ax2 = axes[1]
for name, x, y in [("肤色", 0.40, 0.36), ("绿", 0.28, 0.52)]:
    dC, dM = [], []
    for Y in LEVELS:
        a = C.cam16(xyz(x, y, Y), Wm, LA=200.0)
        Y2 = float(knee(Y / L_M) * L_D)
        b = C.cam16(xyz(x, y, Y2), Wd, LA=40.0)
        dC.append(100.0 * (b["C"] / a["C"] - 1.0))
        dM.append(100.0 * (b["M"] / a["M"] - 1.0))
    col = H.ORANGE if name == "肤色" else H.GREEN
    ax2.plot(LEVELS, dM, "-o", color=col, lw=1.9, ms=4.6, label=f"{name} 的 $M$")
    ax2.plot(LEVELS, dC, "--s", color=col, lw=1.5, ms=4.0, mfc="white",
             label=f"{name} 的 $C$")

ax2.axhline(0, color="#4a5666", lw=1.0)
ax2.set_xscale("log")
ax2.set_xlim(8, 1200)
ax2.set_ylim(-46, 8)
ax2.set_xlabel("母版绝对亮度（cd/m$^2$）", fontsize=9.5)
ax2.set_ylabel("映射后的相对变化（%）", fontsize=9.5)
ax2.legend(loc="upper right", fontsize=7.4, ncol=2, columnspacing=1.0,
           handletextpad=0.5, borderpad=0.35)
ax2.annotate("低亮度段损失最大", xy=(11, -39.5), xytext=(90, -44), fontsize=7.4,
             color="#39485a",
             arrowprops=dict(arrowstyle="-|>", color="#39485a", lw=0.9,
                             shrinkA=2, shrinkB=3))

H.save(fig, 4, "f7_tonemap_coupling")
