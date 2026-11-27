# -*- coding: utf-8 -*-
"""第 06 章 图 5：测量光斑与测试窗口的尺寸匹配（几何计算）。

(a) 亮度计的测量光斑直径 = 2·D·tan(θ/2)，θ 取 1° 与 2°；
    水平虚线是 65 英寸 16:9 屏幕上 1%、2%、10% 面积窗口的边长（厘米）。
    光斑必须完整落在窗口内部，否则读数被黑背景拉低。
(b) 16:9 屏幕上三种面积窗口的边长随对角线长度的变化。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt


def win_side_cm(diag_in, area_pct):
    w = diag_in * 0.8716
    h = diag_in * 0.4903
    return np.sqrt(area_pct / 100.0 * w * h) * 2.54


D = np.linspace(0.4, 4.0, 300)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 4.0))
fig.subplots_adjust(wspace=0.30)

for fov, color in [(2.0, H.NAVY), (1.0, H.TEAL)]:
    d_cm = 2 * D * 100 * np.tan(np.radians(fov / 2))
    ax1.plot(D, d_cm, color=color, lw=2.1, label=f"{fov:.0f}° 视场")

for area, y, lab in [(10, win_side_cm(65, 10), "10% 窗口"),
                     (2, win_side_cm(65, 2), "2% 窗口"),
                     (1, win_side_cm(65, 1), "1% 窗口")]:
    ax1.axhline(y, color=H.GRAY, lw=1.0, ls=":")
    ax1.text(2.55, y + 0.6, f"{lab} {y:.0f} cm", fontsize=8.0, color=H.GRAY, va="bottom")

ax1.set_xlim(0.4, 4.0)
ax1.set_ylim(0, 38)
ax1.set_xlabel("测量距离（米）")
ax1.set_ylabel("测量光斑直径（厘米）")
ax1.legend(loc="upper left", fontsize=8.2)
ax1.set_title("(a) 光斑与 65 英寸屏的窗口", fontsize=10, pad=4)

diag = np.linspace(50, 90, 200)
for area, color in [(10, H.ORANGE), (2, H.PURPLE), (1, H.RED)]:
    ax2.plot(diag, win_side_cm(diag, area), color=color, lw=2.1, label=f"{area}% 面积")

ax2.axvline(65, color=H.GRAY, lw=0.9, ls=":")
ax2.text(65.8, 1.4, "65 英寸", fontsize=8.0, color=H.GRAY)
ax2.set_xlim(50, 90)
ax2.set_ylim(0, 42)
ax2.set_xlabel("屏幕对角线（英寸）")
ax2.set_ylabel("窗口边长（厘米）")
ax2.legend(loc="upper left", fontsize=8.2)
ax2.set_title("(b) 窗口边长随屏幕尺寸", fontsize=10, pad=4)

H.save(fig, 6, "f5_measure_geometry")
