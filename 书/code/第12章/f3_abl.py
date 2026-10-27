# -*- coding: utf-8 -*-
"""第12章 f3：ABL（自动亮度限制）——亮白场面积越大，峰值亮度越低。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig = plt.figure(figsize=(7.2, 5.4))
gs = fig.add_gridspec(2, 3, height_ratios=[1.75, 1.0], hspace=0.80, wspace=0.30)

# ---------------- 上：ABL 曲线 ----------------
ax = fig.add_subplot(gs[0, :])
area = np.linspace(1, 100, 400)          # 白色窗口面积占比 %
def abl(peak, floor, k):
    return floor + (peak - floor) * (1.0 / (1.0 + (area / k) ** 1.35))

curves = [
    ("OLED 电视（标称峰值 1000 nit @2%）", abl(1000, 150, 6.0), H.RED),
    ("OLED 显示器（标称峰值 600 nit @3%）", abl(600, 130, 8.0), H.NAVY),
    ("Mini-LED LCD（亮度几乎不随面积变化）", 1800 - 500 * (area / 100) ** 1.6, H.TEAL),
]
for lab, y, c in curves:
    ax.plot(area, y, color=c, lw=2.4, label=lab)
ax.set_xlim(0, 100); ax.set_ylim(0, 2700)
ax.set_xlabel("白色窗口占屏幕面积（%）——亮场越大，面积越大\n（曲线为示意，真实 ABL 策略由厂商标定；峰值务必看窗口面积条件）")
ax.set_ylabel("可达峰值亮度 (nit)")
ax.set_title("ABL：画面越\"白\"，峰值被压得越低", fontsize=12, pad=6)
ax.legend(loc="upper right", fontsize=8.4)
ax.axvspan(1, 10, color=H.GOLD, alpha=0.16)
ax.text(6.0, 2320, "HDR 高光区\n（小而亮）", ha="center", fontsize=8.0, color="#8a6a1a", fontweight="bold")
ax.axvspan(60, 100, color=H.GRAY, alpha=0.10)
ax.text(80, 1760, "大面积亮场（体育/文档/雪景）", ha="center", fontsize=8.0, color=H.GRAY)

# 关键点标注
y_tv = abl(1000, 150, 6.0)
pts = [(2, y_tv[1]), (10, y_tv[9]), (100, y_tv[-1])]
labs_pt = ["2% 窗口 ≈1000 nit", f"10% 窗口 ≈{round(y_tv[9])} nit", f"全屏白 ≈{round(y_tv[-1])} nit"]
for (px, py), lab in zip(pts, labs_pt):
    ax.plot([px], [py], "o", color=H.RED, ms=6, zorder=5)
    ax.annotate(lab, xy=(px, py), xytext=(px + 6, py + 105), fontsize=8.2, color=H.RED,
                arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=1.1))
ax.annotate("从 1000 nit 掉到约 150 nit\n（掉 ~2.7 挡）", xy=(90, 190), xytext=(44, 620),
            fontsize=8.6, color=H.RED, fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=1.3))

# ---------------- 下：三种窗口面积示意 ----------------
windows = [(2, "2% 窗口", "≈1000 nit", 1.0), (10, "10% 窗口", "≈750 nit", 0.72),
           (100, "全屏白", "≈150 nit", 0.30)]
for i, (pct, name, nit, alpha) in enumerate(windows):
    a = fig.add_subplot(gs[1, i])
    a.grid(False)
    a.set_xlim(0, 10); a.set_ylim(0, 10); a.axis("off")
    a.add_patch(Rectangle((0.1, 0.1), 9.8, 9.8, fc="#0d1420", ec="#4a5666", lw=0.9))
    side = 9.6 * (pct / 100.0) ** 0.5
    a.add_patch(Rectangle((5 - side / 2, 5 - side / 2), side, side, fc="white", ec="none", alpha=alpha))
    a.set_title(f"{name} → {nit}", fontsize=9.4, color=H.NAVY, fontweight="bold")
    a.text(0.55, 0.62, f"占屏面积 {pct}%", ha="left", fontsize=8.0,
           color="#333c48" if pct == 100 else "#9aa6b3", fontweight="bold")

fig.suptitle("OLED 的必修课：ABL 自动亮度限制", fontsize=14, fontweight="bold", color=H.NAVY, y=0.99)
H.save(fig, 12, "f3_abl")
