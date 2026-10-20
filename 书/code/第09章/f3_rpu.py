# -*- coding: utf-8 -*-
"""图 09-3：Dolby Vision 的 RPU —— 画面 + 参考处理单元，按设备能力逐级适配。"""
import sys
sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.patches as mp

fig, ax = H.plt.subplots(figsize=(7.2, 4.4))
ax.set_xlim(0, 100); ax.set_ylim(0, 64); ax.axis("off"); ax.grid(False)

def box(x, y, w, h, text, fc, ec, tc="white", fs=9):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.4",
                                   fc=fc, ec=ec, lw=1.2))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", color=tc,
            fontsize=fs, fontweight="bold", linespacing=1.5)

box(3, 34, 26, 20, "PQ 画面数据\n（逐帧、0–10000 nit）", "#eaf0f6", H.NAVY, H.DARK, 9.5)
ax.text(16, 30.5, "画面只管「长什么样」", ha="center", fontsize=8.2, color=H.GRAY)

box(33, 34, 31, 20, "RPU　参考处理单元\n（动态元数据／逐帧）\n每帧附带：目标亮度、\n映射曲线锚点……", "#fdf2e4", H.ORANGE, "#7a4a10", 9)
ax.text(48.5, 30.5, "RPU 说「怎么放给这块屏看」", ha="center", fontsize=8.2, color=H.GRAY)

for y0 in (44, 40):
    ax.annotate("", xy=(75.0, 44), xytext=(64.5, y0),
                arrowprops=dict(arrowstyle="-|>", color=H.NAVY, lw=1.4))

disp = [("600 nit 显示器\n高光压得更狠", H.TEAL, 46),
        ("1000 nit 显示器\n折中", H.GREEN, 32),
        ("4000 nit 显示器\n高光保留最多", H.PURPLE, 18)]
for name, col, y in disp:
    box(77, y, 21, 12, name, col, col, "white", 8.6)

ax2 = fig.add_axes([0.12, 0.085, 0.78, 0.20])
L = np.linspace(0, 1, 200)
ax2.plot(L, L, color=H.GRAY, lw=1.2, ls="--", label="理想（不映射）")
for tgt, col, lab in [(0.62, H.TEAL, "→600 nit"), (0.80, H.GREEN, "→1000 nit"), (0.95, H.PURPLE, "→4000 nit")]:
    y = np.where(L <= tgt, L, tgt + (L - tgt) * 0.15)
    ax2.plot(L, y, color=col, lw=2.0, label=lab)
ax2.set_xlabel("输入亮度（归一化）", fontsize=8.5)
ax2.set_ylabel("显示亮度", fontsize=8.5)
ax2.set_title("同一帧，按 RPU 映射到不同能力的屏幕", fontsize=9.5, fontweight="bold")
ax2.legend(fontsize=7.4, ncol=4, loc="lower right")
ax2.tick_params(labelsize=7.5)

ax.set_title("Dolby Vision：画面 + RPU，逐帧告诉你「怎么放」", fontsize=13, fontweight="bold", pad=8)
H.save(fig, 9, "f3_rpu")
