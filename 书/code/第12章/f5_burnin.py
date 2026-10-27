# -*- coding: utf-8 -*-
"""第12章 f5：烧屏（burn-in）示意见图：长时间静态高亮 → 残影 + 老化曲线。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig = plt.figure(figsize=(7.2, 5.6))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.95], hspace=0.45, wspace=0.24)

# ---------------- 合成两帧画面 ----------------
NH, NW = 126, 210
base = np.zeros((NH, NW, 3)) + np.array([0.16, 0.20, 0.26])

elements = np.zeros((NH, NW, 3))
mask = np.zeros((NH, NW), dtype=bool)

# 台标（右上角静态标志）
logo = np.zeros((NH, NW), dtype=bool); logo[10:30, 148:194] = True
elements[logo] = [0.90, 0.16, 0.13]
mask |= logo
logo_txt = np.zeros((NH, NW), dtype=bool); logo_txt[16:24, 154:172] = True
elements[logo_txt] = [1.0, 0.95, 0.95]

# 底部状态条 / 任务栏
bar = np.zeros((NH, NW), dtype=bool); bar[106:120, 8:202] = True
elements[bar] = [0.88, 0.89, 0.92]
mask |= bar
for cx in range(20, 200, 26):
    elements[110:116, cx:cx + 14] = [0.25, 0.30, 0.36]

# 游戏 HUD / 界面元素
hud = np.zeros((NH, NW), dtype=bool); hud[44:74, 18:52] = True
elements[hud] = [0.22, 0.88, 0.52]
mask |= hud

frame_old = np.clip(base + elements, 0, 1)

# 新内容（浅灰画面）+ 老化残影
new_content = np.zeros((NH, NW, 3)) + np.array([0.46, 0.46, 0.47])
aged_factors = np.array([0.80, 0.78, 0.62])       # 蓝光材料退化更快 → 残影偏暖
frame_new = new_content.copy()
frame_new[mask] = new_content[mask] * aged_factors

# ---------------- 上排：老化时 vs 之后 ----------------
axA = fig.add_subplot(gs[0, 0])
axA.grid(False)
axA.imshow(frame_old, vmin=0, vmax=1)
axA.set_xticks([]); axA.set_yticks([])
axA.set_title("① 长期显示同一静态界面", fontsize=9.8, color=H.NAVY, fontweight="bold")
axA.set_xlabel("台标 / 任务栏 / HUD 长期高亮 → 这些像素老化更快", fontsize=7.8, color="#4a5666")
for (xy, xyt, t) in [((171, 20), (100, 48), "台标"), ((100, 112), (96, 88), "任务栏 / 状态条"),
                     ((35, 59), (60, 40), "HUD 血条")]:
    axA.annotate(t, xy=xy, xytext=xyt, fontsize=7.4, color="#ffe9a8", fontweight="bold",
                 arrowprops=dict(arrowstyle="-|>", color="#ffe9a8", lw=1.0))

axB = fig.add_subplot(gs[0, 1])
axB.grid(False)
axB.imshow(frame_new, vmin=0, vmax=1)
axB.set_xticks([]); axB.set_yticks([])
axB.set_title("② 换成新内容后：留下淡淡残影", fontsize=9.8, color=H.RED, fontweight="bold")
axB.set_xlabel("同样驱动电流下，老化像素更暗、偏色 → 残影可见", fontsize=7.8, color="#4a5666")
axB.annotate("残影：台标形状", xy=(172, 20), xytext=(96, 60), fontsize=7.4, color=H.RED,
             fontweight="bold", arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=1.1))
axB.annotate("残影：状态条形状", xy=(100, 113), xytext=(40, 84), fontsize=7.4, color=H.RED,
             fontweight="bold", arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=1.1))

# ---------------- 下排左：老化曲线 ----------------
ax1 = fig.add_subplot(gs[1, 0])
t = np.linspace(0, 10000, 300)
stress = 100 - 15.5 * (1 - np.exp(-t / 2600))      # 长期高亮像素
normal = 100 - 7.5 * (1 - np.exp(-t / 4200))       # 普通内容像素
ax1.plot(t, stress, color=H.RED, lw=2.3, label="长期高亮像素（台标/任务栏）")
ax1.plot(t, normal, color=H.NAVY, lw=2.3, label="普通内容像素")
ax1.fill_between(t, stress, normal, color=H.ORANGE, alpha=0.18)
ax1.set_xlabel("累计点亮时间 (小时)")
ax1.set_ylabel("相对发光效率 (%)")
ax1.set_ylim(80, 101)
ax1.set_xlim(0, 10000)
ax1.set_title("老化速度不同 → 效率差 → 残影", fontsize=10.2, pad=5)
ax1.legend(loc="lower left", fontsize=8.0)
ax1.annotate("", xy=(5200, stress[156] - 0.25), xytext=(5200, normal[156] + 0.25),
             arrowprops=dict(arrowstyle="<|-|>", color=H.ORANGE, lw=1.4))
ax1.text(5400, (stress[156] + normal[156]) / 2, "Δ ≈ 5%\n（肉眼已可辨）", fontsize=7.8,
         color="#a06a12", va="center", fontweight="bold")
ax1.axhline(97, color=H.GRAY, ls="--", lw=1.0)
ax1.text(6350, 97.9, "约 2%~3% 亮度差开始可辨", fontsize=7.4, color=H.GRAY)
ax1.grid(axis="x", visible=False)

# ---------------- 下排右：缓解手段 ----------------
ax2 = fig.add_subplot(gs[1, 1])
ax2.grid(False); ax2.axis("off")
ax2.set_title("厂商如何缓解", fontsize=10.2, pad=5)
tips = [
    ("像素位移", "整个画面在小范围内缓慢平移，让高亮元素不总打在同样像素上"),
    ("标志检测", "识别台标/任务栏等静态元素，自动降低其亮度"),
    ("像素刷新 / 补偿", "定期测量每颗像素老化程度并补偿"),
    ("使用习惯", "降低默认亮度、用暗色主题；避免长时间固定高亮静态界面"),
]
y0 = 0.94
for i, (k, v) in enumerate(tips):
    y = y0 - i * 0.235
    ax2.add_patch(Rectangle((0.02, y - 0.16), 0.96, 0.19, fc="#f2f6fa",
                            ec="#d5dbe2", lw=0.8, transform=ax2.transAxes))
    ax2.add_patch(Rectangle((0.048, y - 0.048), 0.018, 0.026,
                            fc=H.PALETTE[i % len(H.PALETTE)], ec="none", transform=ax2.transAxes))
    ax2.text(0.085, y - 0.005, k, fontsize=8.8, color=H.NAVY, fontweight="bold",
             transform=ax2.transAxes, va="top")
    ax2.text(0.085, y - 0.082, v, fontsize=7.6, color="#4a5666", transform=ax2.transAxes, va="top")
ax2.text(0.5, 0.015, "经常变化的画面（看片、打游戏）几乎不用担心烧屏",
         fontsize=7.8, color=H.GREEN, transform=ax2.transAxes, ha="center", fontweight="bold")

fig.suptitle("烧屏（burn-in）：有机材料老化留下的\"残影\"", fontsize=13.5,
             fontweight="bold", color=H.NAVY, y=0.985)
H.save(fig, 12, "f5_burnin")
