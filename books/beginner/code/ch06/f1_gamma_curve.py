# -*- coding: utf-8 -*-
"""图 06-1：Gamma 2.2 曲线 vs 线性 —— 码值 → 光。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

fig, ax = H.plt.subplots(figsize=(7.2, 4.3))

v = np.linspace(0, 1, 600)
lin = v                       # 线性：码值 = 光
g22 = H.gamma_eotf(v, 2.2)    # 显示端 Gamma 2.2：码值 -> 光
g18 = H.gamma_eotf(v, 1.8)
g26 = H.gamma_eotf(v, 2.6)

# 线性（参照）
ax.plot(v, lin, color=H.GRAY, lw=2.0, ls="--", label="线性（认为码值=光）")
# 其它 gamma 作为背景参考
ax.plot(v, g18, color=H.LGRAY, lw=1.4, label="Gamma 1.8（画面发灰）")
ax.plot(v, g26, color="#e8d9b0", lw=1.4, label="Gamma 2.6（画面发暗）")
# 主角
ax.plot(v, g22, color=H.NAVY, lw=2.8, label="Gamma 2.2（SDR 约定值）")

# 填充"暗部被抬亮 / 亮部被压暗"的差异区
ax.fill_between(v, g22, lin, where=(lin > g22), color=H.NAVY, alpha=0.10, lw=0)
ax.fill_between(v, g22, lin, where=(lin <= g22), color=H.ORANGE, alpha=0.12, lw=0)

# 关键点：码值 128（0.5）
ax.plot([0.5, 0.5], [0, 0.5 ** 2.2], color=H.RED, lw=1.1, ls=":")
ax.plot([0, 0.5], [0.5 ** 2.2, 0.5 ** 2.2], color=H.RED, lw=1.1, ls=":")
ax.plot(0.5, 0.5, "o", color=H.GRAY, ms=6, zorder=5)
ax.plot(0.5, 0.5 ** 2.2, "o", color=H.RED, ms=7, zorder=6)
ax.annotate("码值 128（50%）：\n线性“以为”是 0.50 的光\n实际只有 0.5$^{2.2}$≈0.218（两成多）",
            xy=(0.5, 0.218), xytext=(0.545, 0.40),
            fontsize=9, color=H.RED,
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.2))

# 暗部放大强调（用箭头指向三条曲线的低段差异）
ax.annotate("暗部：非线性编码把曲线抬起来\n→ 同样的光对应更大的码值",
            xy=(0.10, 0.10 ** 2.2), xytext=(0.14, 0.055),
            fontsize=9, color=H.NAVY,
            arrowprops=dict(arrowstyle="->", color=H.NAVY, lw=1.2))

ax.text(0.82, 0.695, "亮部被压暗\n（浪费码值少）", fontsize=8.5, color=H.ORANGE,
        ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=H.ORANGE, lw=0.7, alpha=0.95))

# 关键点小表
pts = [0.25, 0.5, 0.75]
for p in pts:
    ax.plot(p, p ** 2.2, "o", color=H.NAVY, ms=4.5, zorder=6)
rows = "\n".join([f"码值 {int(round(p*255)):>3d} → 光 {p**2.2:.3f}" for p in pts])
ax.text(0.015, 0.955, "Gamma 2.2 采样\n" + rows, transform=ax.transAxes,
        fontsize=8.5, va="top", ha="left", color=H.DARK,
        bbox=dict(boxstyle="round,pad=0.4", fc="#f4f7fa", ec=H.LGRAY, lw=0.8))

ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
ax.set_xticks(np.arange(0, 1.01, 0.125))
ax.set_xticklabels([f"{int(x*255)}" for x in np.arange(0, 1.01, 0.125)])
ax.set_xlabel("输入码值（0–255，按比例）")
ax.set_ylabel("归一化输出光（0 = 黑，1 = 白）")
ax.set_title("Gamma 2.2 曲线 vs 线性：码值 128 只有约两成多的光", fontweight="bold")
ax.legend(loc="lower right", fontsize=8.5)

fig.tight_layout()
H.save(fig, 6, "f1_gamma_curve")
