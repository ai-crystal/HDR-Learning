# -*- coding: utf-8 -*-
"""图 13-4　标称峰值 vs 实测：小窗口（10%）峰值 与 全屏（100%）亮度。

要点：厂商标的“峰值 xxx nit”来自小窗口测量；一旦亮场铺满全屏，
LCD/Mini-LED 会因功耗与散热略降，OLED 则因 ABL 大跌（本图约打到 42%）。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np

dev = ["无认证\n300 nit", "HDR 400", "HDR 600", "HDR1000\nMiniLED",
       "HDR1400\nMiniLED", "TB600\nOLED"]
nominal = np.array([300, 400, 600, 1000, 1400, 600], dtype=float)
small = np.array([280, 400, 610, 1010, 1400, 600], dtype=float)   # 10% 窗口
full = np.array([260, 380, 560, 850, 1100, 250], dtype=float)     # 100% 全屏

x = np.arange(len(dev))
w = 0.25

fig, axes = H.plt.subplots(1, 2, figsize=(7.2, 4.5),
                           gridspec_kw={"width_ratios": [1.62, 1.0]})
fig.subplots_adjust(wspace=0.40)

# ---------- (1) 三组亮度对比 ----------
ax = axes[0]
b1 = ax.bar(x - w, nominal, w, label="标称峰值（宣传值）", color=H.GRAY,
            edgecolor="white", linewidth=0.6)
b2 = ax.bar(x, small, w, label="实测 小窗口 10% 峰值", color=H.ORANGE,
            edgecolor="white", linewidth=0.6)
b3 = ax.bar(x + w, full, w, label="实测 全屏 100% 亮度", color=H.TEAL,
            edgecolor="white", linewidth=0.6)
# 三个标签分别右对齐/居中/左对齐，避免相邻数字挤在一起
for bars, ha in ((b1, "center"), (b2, "center"), (b3, "center")):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 22,
                f"{b.get_height():.0f}", ha="center", va="bottom", fontsize=6.2,
                color="#333333", rotation=90)
ax.axhline(400, color=H.GOLD, ls="--", lw=1.2)
ax.text(0.02, 0.303, "400 nit 门槛", transform=ax.transAxes,
        ha="left", va="bottom", fontsize=7.4, color=H.GOLD, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
ax.set_xticks(x); ax.set_xticklabels(dev, fontsize=6.6)
ax.set_ylabel("亮度 (nit)")
ax.set_ylim(0, 1750)
ax.set_title("同一台机器，三种“亮度”是三个数", pad=8)
ax.grid(axis="x", visible=False)
ax.legend(loc="upper left", fontsize=7.2, ncol=3, columnspacing=0.8,
          handlelength=1.2, handletextpad=0.4)
ax.annotate("ABL", xy=(5.30, 270), xytext=(5.62, 700), fontsize=8,
            color=H.RED, fontweight="bold", ha="center", va="center",
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.1,
                            connectionstyle="arc3,rad=-0.25"))

# ---------- (2) 实测 / 标称 达成率 ----------
ax = axes[1]
r_small = small / nominal * 100
r_full = full / nominal * 100
ax.bar(x - 0.16, r_small, 0.30, color=H.ORANGE, edgecolor="white",
       linewidth=0.6, label="小窗口达成率")
ax.bar(x + 0.16, r_full, 0.30, color=H.TEAL, edgecolor="white",
       linewidth=0.6, label="全屏达成率")
for xi, v in zip(x, r_full):
    ax.text(xi + 0.16, v + 2.5, f"{v:.0f}%", ha="center", va="bottom",
            fontsize=7.2, color="#1b2a3a", fontweight="bold")
ax.axhline(100, color=H.GRAY, ls=":", lw=1.0)
ax.set_xticks(x)
ax.set_xticklabels(["无认证", "400", "600", "1000", "1400", "TB600"], fontsize=8)
ax.set_ylim(0, 132)
ax.set_ylabel("实测 ÷ 标称 (%)")
ax.set_xlabel("DisplayHDR 等级 / 类型")
ax.set_title("“标称峰值”只有小窗口时兑现", pad=8)
ax.grid(axis="x", visible=False)
ax.legend(loc="upper center", fontsize=7.6, ncol=2)

fig.suptitle("认证是及格线，实测才是成绩单", fontsize=12.5,
             fontweight="bold", y=1.04)
fig.text(0.5, -0.11,
         "注：数值为典型示意（同级别不同机型差异很大）；OLED 全屏下跌源于 ABL（见第 12 章），"
         "LCD 小幅下跌源于功耗/散热限流。",
         ha="center", fontsize=8, color=H.GRAY)

H.save(fig, 13, "f4_measured_vs_claim")
