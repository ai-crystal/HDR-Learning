# -*- coding: utf-8 -*-
"""第 03 章 图 5：同一组颜色对在 ΔE76 / ΔE94 / ΔE2000 下的数值。

Lab 数值为人为设定的色样对（覆盖明度、彩度、色相不同组合），
三个色差全部按 CIE 公式计算（CIEDE2000 实现已用 Sharma 等 2005 的测试数据校验）。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import colordiff as D

plt = H.plt

PAIRS = [
    ("近白", (96.0, 0.0, 2.0), (94.0, 0.0, 1.0)),
    ("中性灰", (60.0, 0.0, 0.0), (57.0, 0.0, 0.0)),
    ("肤色", (66.0, 18.0, 25.0), (63.0, 14.0, 22.0)),
    ("深红", (40.0, 52.0, 30.0), (37.0, 47.0, 27.0)),
    ("叶绿", (70.0, -45.0, 35.0), (68.0, -41.0, 31.0)),
    ("天蓝", (55.0, -12.0, -42.0), (53.0, -9.0, -37.0)),
    ("亮黄", (88.0, -5.0, 80.0), (85.0, -4.0, 74.0)),
    ("暗紫", (25.0, 20.0, -15.0), (23.0, 17.0, -12.0)),
]

names, cstar, e76, e94, e00 = [], [], [], [], []
for name, a, b in PAIRS:
    names.append(name)
    cstar.append(0.5 * (np.hypot(a[1], a[2]) + np.hypot(b[1], b[2])))
    e76.append(D.de76(a, b))
    e94.append(D.de94(a, b))
    e00.append(D.de2000(a, b))

fig = plt.figure(figsize=(7.2, 4.2))
gs = fig.add_gridspec(1, 2, width_ratios=[1.55, 1.0], wspace=0.30)
ax = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

xo = np.arange(len(names))
bw = 0.26
ax.bar(xo - bw, e76, bw, color="#a8b6c4", edgecolor="#6f7d8c", lw=0.7, label=r"$\Delta E_{76}$")
ax.bar(xo, e94, bw, color=H.TEAL, edgecolor="#0d6b58", lw=0.7, label=r"$\Delta E_{94}$")
ax.bar(xo + bw, e00, bw, color=H.NAVY, edgecolor="#12314d", lw=0.7, label=r"$\Delta E_{2000}$")
ax.set_xticks(xo)
ax.set_xticklabels(names, fontsize=8.0)
ax.set_ylim(0, 9.2)
ax.set_ylabel("色差值")
ax.set_xlabel("")
ax.grid(axis="x", visible=False)
ax.legend(loc="upper left", ncol=3, fontsize=8.0, frameon=False, handlelength=1.3,
          columnspacing=1.4)

# ---- 比值随彩度的变化 ----
ax2.plot(cstar, np.array(e94) / np.array(e76), "o", ms=6, mfc="white",
         mec=H.TEAL, mew=1.6, label=r"$\Delta E_{94}/\Delta E_{76}$", zorder=5)
ax2.plot(cstar, np.array(e00) / np.array(e76), "s", ms=5.6, mfc="white",
         mec=H.NAVY, mew=1.6, label=r"$\Delta E_{2000}/\Delta E_{76}$", zorder=5)
ax2.axhline(1.0, color="#8d99a6", lw=0.9, ls=(0, (4, 3)))
ax2.set_xlabel(r"平均彩度 $C^*_{ab}$")
ax2.set_ylabel("相对 ΔE76 的比值")
ax2.set_xlim(0, 90)
ax2.set_ylim(0.35, 1.30)
ax2.legend(fontsize=7.6, loc="lower left", frameon=False, handlelength=1.4)
ax2.text(52, 1.14, "彩度越高，ΔE76 相对高估越多", fontsize=7.4, color="#2c3e50",
         ha="center", va="center",
         bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=1.0))

H.save(fig, 3, "f5_delta_e")
for i in range(len(names)):
    print(f"{names[i]:>4}  C*={cstar[i]:5.1f}  dE76={e76[i]:5.2f}  dE94={e94[i]:5.2f}  dE00={e00[i]:5.2f}")
