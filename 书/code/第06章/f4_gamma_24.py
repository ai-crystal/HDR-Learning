# -*- coding: utf-8 -*-
"""图 06-4：BT.1886（≈2.4）与 Gamma 2.2 对比，含黑位不为 0 的影响。"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt


def bt1886(V, Lw=100.0, Lb=0.0, g=2.4):
    """BT.1886 显示 EOTF：L = a·(max(V+b,0))^γ，由 Lw/Lb 解出 a、b。"""
    V = np.asarray(V, dtype=float)
    a = (Lw ** (1 / g) - Lb ** (1 / g)) ** g
    b = (Lb ** (1 / g)) / (Lw ** (1 / g) - Lb ** (1 / g))
    return a * np.maximum(V + b, 0.0) ** g


fig, (axL, axR) = H.plt.subplots(1, 2, figsize=(7.2, 4.3))

V = np.linspace(0, 1, 1000)
Lw = 100.0
g22 = Lw * V ** 2.2
g24 = bt1886(V, Lw=Lw, Lb=0.0, g=2.4)          # 暗室、黑位 0
g24_b = bt1886(V, Lw=Lw, Lb=0.5, g=2.4)        # 黑位 0.5 nit（非暗室）

# ---------------- 左：线性纵轴 ----------------
axL.plot(V, g22, color=H.NAVY, lw=2.6, label="Gamma 2.2（PC/sRGB 阵营）")
axL.plot(V, g24, color=H.ORANGE, lw=2.6, label="BT.1886 γ=2.4（暗室，L$_{b}$=0）")
axL.plot(V, g24_b, color=H.RED, lw=2.0, ls="--",
         label="BT.1886 γ=2.4（L$_{b}$=0.5 nit）")
axL.fill_between(V, g22, g24, color=H.ORANGE, alpha=0.12, lw=0)

V0 = 0.5
axL.plot([V0, V0], [0, V0 ** 2.2 * Lw], color=H.RED, lw=1.0, ls=":")
axL.annotate(f"码值 128：\n2.2 → {V0**2.2*Lw:.1f} nit\n2.4 → {V0**2.4*Lw:.1f} nit",
             xy=(V0, V0 ** 2.4 * Lw), xytext=(0.30, 45),
             fontsize=8.6, color=H.RED,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.1))

axL.set_xlim(0, 1); axL.set_ylim(0, Lw + 3)
axL.set_xlabel("码值 V（0–1）")
axL.set_ylabel("屏幕亮度（nit）")
axL.set_title("同一条幂函数，指数差 0.2 的后果", fontsize=11)
axL.legend(loc="upper left", fontsize=8)

# ---------------- 右：对数纵轴看暗部 ----------------
axR.semilogy(V[1:], g22[1:], color=H.NAVY, lw=2.6, label="Gamma 2.2")
axR.semilogy(np.clip(V, 1e-3, 1),
             np.maximum(bt1886(np.clip(V, 1e-3, 1), Lw, 0.0, 2.4), 1e-3),
             color=H.ORANGE, lw=2.6, label="BT.1886 γ=2.4（L$_{b}$=0）")
axR.semilogy(V, np.maximum(g24_b, 1e-3), color=H.RED, lw=2.0, ls="--",
             label="BT.1886（L$_{b}$=0.5 nit）")
axR.axhline(0.5, color=H.RED, lw=1.0, ls=":")

axR.set_xlim(0, 1); axR.set_ylim(0.2, 130)
axR.set_xlabel("码值 V（0–1）")
axR.set_ylabel("屏幕亮度（nit，对数）")
axR.set_title("对数轴：暗部差异一目了然", fontsize=11)
axR.legend(loc="upper left", fontsize=8)

fig.suptitle("BT.1886（≈γ 2.4）与 Gamma 2.2：差在“给什么环境看”", fontweight="bold", y=1.0)
fig.subplots_adjust(left=0.09, right=0.985, top=0.855, bottom=0.25, wspace=0.30)
fig.text(0.5, 0.105,
         "右图要点：BT.1886 γ=2.4（橙）比 Gamma 2.2（蓝）更陡 → 暗部压得更黑、对比更强（暗室更“通透”）；"
         "Gamma 2.2 更缓 → 暗部更亮（亮环境不闷）。",
         ha="center", va="center", fontsize=8.0, color=H.DARK)
fig.text(0.5, 0.038,
         "红色虚线：黑位不为 0（这里 0.5 nit）时，暗部被整体“兜底”抬亮。",
         ha="center", va="center", fontsize=8.0, color=H.RED)

H.save(fig, 6, "f4_gamma_24")
