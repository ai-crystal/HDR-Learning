# -*- coding: utf-8 -*-
"""第 12 章 图 1：四种 HDR 色差度量在亮度-彩度平面上的等值线对比。

做法：固定色相角 h_ab，在 (L*, C*_ab) 平面取网格，把每个网格点转成绝对 XYZ，
再用四种度量相对中心色求值。四条等值线的水平各自取"该度量在中心色沿 +L*
方向 10 个 L* 处的读数"，于是四条曲线都在 (0, 10) 处交汇，往其他方向散开，
剩下的差别就是各向异性本身：沿彩度方向能走多远，四种度量给出 9 到 31 不等的
答案。
"""
import os
import sys
import numpy as np

sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metrics as M

plt = H.plt

WHITE_LUM = 203.0
mm = M.Metrics(white_lum=WHITE_LUM)
REF_DL = 10.0

CASES = [
    dict(tag="(a) 红橙色相  $h_{ab}=40^\\circ$\n$L^*=70$，$C^*_{ab}=45$",
         L=70.0, C=45.0, h=40.0),
    dict(tag="(b) 蓝紫色相  $h_{ab}=295^\\circ$\n$L^*=40$，$C^*_{ab}=35$",
         L=40.0, C=35.0, h=295.0),
]

STYLE = [
    ("$\\Delta E_{00}$", H.NAVY, "-"),
    ("$\\Delta E_{ITP}$", H.ORANGE, "-"),
    ("$\\Delta E_z$", H.TEAL, "-"),
    ("$\\Delta E'_{CAM16}$", H.PURPLE, "-"),
]

DC_MAX = 34.0
DL_MAX = 14.0
DL_TOP = 17.0


def fields(L, C, h, dLs, dCs):
    dL, dC = np.meshgrid(dLs, dCs, indexing="ij")
    Cg = np.where(C + dC < 0.5, np.nan, C + dC)
    xyz = M.lab_to_xyz(M.lch_to_lab(L + dL, Cg, h), white_ref=WHITE_LUM)
    x0 = M.lab_to_xyz(M.lch_to_lab(L, np.array(C), np.array(h)), white_ref=WHITE_LUM)
    lab0 = mm.lab(x0)
    d00 = M.I.deltaE_2000(mm.lab(xyz), lab0)
    ditp = M.I.deltaE_ITP(M.xyz_to_ictcp(xyz), M.xyz_to_ictcp(x0))
    dez = M.I.deltaE_z(M.xyz_to_jz(xyz), M.xyz_to_jz(x0))
    dec = M.deltaE_CAM16UCS(xyz, x0, mm.cam)
    return [d00, ditp, dez, dec]


fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.5),
                         gridspec_kw=dict(wspace=0.24))
for ax, case in zip(axes, CASES):
    L, C, h = case["L"], case["C"], case["h"]
    dLs = np.arange(-DL_MAX, DL_MAX + 0.01, 0.1)
    dCs = np.arange(-DC_MAX, DC_MAX + 0.01, 0.1)
    fl = fields(L, C, h, dLs, dCs)
    levels = [np.interp(REF_DL, dLs, f[:, np.argmin(np.abs(dCs + 0.5))]) for f in fl]
    for (txt, col, ls), f, lv in zip(STYLE, fl, levels):
        z = np.ma.masked_invalid(f)
        ax.contour(dCs, dLs, z, levels=[lv], colors=[col], linewidths=1.9)
        ax.plot([], [], color=col, lw=1.9, label=txt)
    ax.axhline(0, color=H.LGRAY, lw=0.8, zorder=0)
    ax.axvline(0, color=H.LGRAY, lw=0.8, zorder=0)
    ax.plot([0], [0], marker="+", ms=8, color=H.DARK, mew=1.5)
    ax.plot([0], [REF_DL], marker="o", ms=4.0, mfc="white", mec=H.DARK, mew=1.1)
    ax.set_xlabel("$\\Delta C^*_{ab}$")
    ax.set_ylabel("$\\Delta L^*$")
    ax.set_xlim(-DC_MAX, DC_MAX)
    ax.set_ylim(-DL_MAX, DL_TOP)
    ax.text(0.035, 0.955, case["tag"], transform=ax.transAxes, fontsize=9.0,
            va="top", ha="left", linespacing=1.35,
            bbox=dict(fc="white", ec=H.LGRAY, lw=0.7, alpha=0.92, pad=2.5))
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=8.8,
           handlelength=1.7, columnspacing=1.8, frameon=False,
           bbox_to_anchor=(0.5, -0.115))

H.save(fig, 12, "f1_contours_lc")
