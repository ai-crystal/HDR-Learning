# -*- coding: utf-8 -*-
"""第 05 章 图 3：裁剪与压缩两种彩度映射策略的映射曲线与局部斜率。

三条曲线都是解析式，参数取目标色域边界 C_l = 100、源色域最大彩度 C_s = 140、
膝点 C_k = 0.8 C_l = 80。斜率为数值微分（中心差分）。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
import numpy as np

plt = H.plt

CL, CS, CK = 100.0, 140.0, 80.0
Ci = np.linspace(0, 160, 801)


def clip(c):
    return np.minimum(c, CL)


def linear(c):
    return c * CL / CS


def knee(c):
    over = np.maximum(c - CK, 0.0)
    return np.where(c <= CK, c, CK + (CL - CK) * (1 - np.exp(-over / (CL - CK))))


fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.9))
fig.subplots_adjust(left=0.085, right=0.985, top=0.94, bottom=0.19, wspace=0.28)

# ---------- (a) 映射曲线 ----------
ax = axes[0]
ax.axvspan(CL, 160, color="#f6e7e3", zorder=0, lw=0)
ax.axvline(CL, color="#b9a29b", lw=1.0, ls=(0, (5, 3)), zorder=1)
ax.plot([0, 160], [0, 160], color="#b7c0ca", lw=1.0, ls=":", zorder=1)
ax.plot(Ci, clip(Ci), color=H.NAVY, lw=2.3, label="硬裁剪 clipping")
ax.plot(Ci, linear(Ci), color=H.ORANGE, lw=2.1, ls=(0, (6, 3)), label="全局线性压缩")
ax.plot(Ci, knee(Ci), color=H.TEAL, lw=2.3, label="膝形软压缩")
ax.plot([CK], [CK], "o", ms=5.5, mfc="white", mec=H.TEAL, mew=1.5, zorder=5)

ax.set_xlim(0, 160)
ax.set_ylim(0, 160)
ax.set_xlabel("源彩度 $C_{in}$", fontsize=10)
ax.set_ylabel("映射后彩度 $C_{out}$", fontsize=10)
ax.text(CL + 5, 22, "目标色域之外\n$C_{in}>C_l$", fontsize=8.0, color="#8a5a50",
        va="center")
ax.annotate("膝点 $C_k=80$", xy=(CK + 1.5, CK - 1.5), xytext=(90, 58), fontsize=8.0,
            color=H.TEAL, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=H.TEAL, lw=0.8,
                            shrinkA=2, shrinkB=3))
ax.text(6, 156, "点线为理想恒等映射", fontsize=7.8, color="#69747f", va="top")
ax.legend(loc="upper left", fontsize=8.2, frameon=False, bbox_to_anchor=(0.02, 0.76))

# ---------- (b) 局部斜率 ----------
ax = axes[1]
for f, col, ls, lab in ((clip, H.NAVY, "-", "硬裁剪"),
                        (linear, H.ORANGE, (0, (6, 3)), "全局线性压缩"),
                        (knee, H.TEAL, "-", "膝形软压缩")):
    d = np.gradient(f(Ci), Ci)
    ax.plot(Ci, d, color=col, lw=2.1, ls=ls, label=lab)

ax.axhline(0, color="#4a5666", lw=0.9, zorder=2)
ax.axvline(CL, color="#b9a29b", lw=1.0, ls=(0, (5, 3)))
ax.axvspan(CL, 160, color="#f6e7e3", zorder=0, lw=0)
ax.text(CL + 4, 0.90, "多对一\n细节丢失", fontsize=7.8, color=H.NAVY, va="top")
ax.text(6, 1.06, "斜率为 1：完全保留彩度细节", fontsize=7.8, color="#39485a")

ax.set_xlim(0, 160)
ax.set_ylim(-0.05, 1.15)
ax.set_xlabel("源彩度 $C_{in}$", fontsize=10)
ax.set_ylabel("局部斜率 $\\mathrm{d}C_{out}/\\mathrm{d}C_{in}$", fontsize=10)
ax.legend(loc="lower left", fontsize=8.4, frameon=False, bbox_to_anchor=(0.01, 0.02))

H.save(fig, 5, "f3_mapping_curves")
