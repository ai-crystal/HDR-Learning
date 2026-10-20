# -*- coding: utf-8 -*-
"""第 07 章 图 f5：HLG 系统 gamma（OOTF，≈1.2）显示调整示意。

左图：系统 gamma 随显示峰值亮度变化（γ = 1.2 + 0.42·log10(Lw/1000)），标出 1000 nit → 1.2。
右图：同一条 HLG 信号在不同峰值屏幕上的 OOTF 曲线 —— 整体提亮/压暗，但相对关系保留。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np

fig, (ax1, ax2) = H.plt.subplots(1, 2, figsize=(7.2, 4.3))

# ---------------- 左：系统 gamma vs 显示峰值 ----------------
Lw = np.logspace(np.log10(100), np.log10(10000), 400)
gamma_sys = 1.2 + 0.42 * np.log10(Lw / 1000.0)
ax1.semilogx(Lw, gamma_sys, color=H.NAVY, lw=2.6, label="γ = 1.2 + 0.42·log₁₀(Lw / 1000)")
ax1.axhline(1.2, color=H.GRAY, ls=":", lw=1.1)
ann = [(100, H.PURPLE, (1.06e2, 0.87)), (1000, H.RED, (1.45e3, 1.02)),
       (4000, H.ORANGE, (1.7e3, 1.60))]
for lw_, col, xytext in ann:
    g = 1.2 + 0.42 * np.log10(lw_ / 1000.0)
    ax1.plot([lw_], [g], "o", color=col, ms=7, mec="white", mew=1.3, zorder=6)
    ax1.annotate("%g nit\nγ ≈ %.2f" % (lw_, g), xy=(lw_, g), xytext=xytext,
                 fontsize=8.5, color=col, fontweight="bold",
                 arrowprops=dict(arrowstyle="-", color=col, lw=0.9))
ax1.set_xlabel("显示端峰值亮度 Lw（nit，对数刻度）")
ax1.set_ylabel("系统 gamma（OOTF 指数 γ）")
ax1.set_title("系统 gamma 随屏幕亮度自适应", fontweight="bold")
ax1.set_ylim(0.6, 1.8)
ax1.text(2.6e3, 0.70, "屏幕越亮 → γ 越大\n（1000 nit 参考点 = 1.2）",
         fontsize=8.5, color=H.DARK, ha="left", va="bottom")

# ---------------- 右：OOTF 在信号上的效果 ----------------
E = np.linspace(0, 1, 600)
for g, col, name in [(0.78, H.PURPLE, "暗屏 100 nit，γ≈0.78"),
                     (1.20, H.RED, "参考屏 1000 nit，γ=1.20"),
                     (1.45, H.ORANGE, "亮屏 4000 nit，γ≈1.45"),
                     (1.00, H.GRAY, "无调整 γ=1.00")]:
    ax2.plot(E, E ** g, color=col, lw=2.4, ls="--" if abs(g - 1) < 1e-9 else "-", label=name)

p1, p2 = 0.2, 0.6
for p in (p1, p2):
    ax2.plot([p, p], [p ** 0.78, p ** 1.45], color=H.DARK, lw=1.6, alpha=0.55)
ax2.annotate("同一信号：γ 越大整体越亮，\n但亮度之间的相对关系不变",
             xy=(p2, p2 ** 1.45), xytext=(0.06, 0.86), fontsize=8.5, color=H.DARK,
             arrowprops=dict(arrowstyle="->", color=H.DARK, lw=1.1,
                             connectionstyle="arc3,rad=-0.2"))
ax2.set_xlabel("场景线性亮度 E（HLG 信号解出的相对值）")
ax2.set_ylabel("显示端相对光输出（OOTF 之后）")
ax2.set_title("OOTF：把相对关系适配到屏幕能力", fontweight="bold")
ax2.set_xlim(0, 1.0); ax2.set_ylim(0, 1.05)
ax2.legend(loc="lower right", fontsize=8.5)

fig.tight_layout()
H.save(fig, 7, "f5_system_gamma")
