# -*- coding: utf-8 -*-
"""第 03 章 图 4　光适应：眼睛的“工作区间”随环境光整体平移。

上：不同环境光场景下，眼睛的工作区间（约 3.2 个数量级）在 log 亮度轴上的位置。
下：同一块 300 nit 屏幕，落在不同适应曲线上，得到完全不同的主观响应。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import numpy as np
import hdrfig as H
from matplotlib.ticker import NullFormatter
plt = H.plt

SCENES = [
    ("暗夜 / 星光", 1e-3,  H.NAVY,   "屏幕刺眼"),
    ("月光 / 烛光", 0.03,  H.PURPLE, "屏幕发白"),
    ("昏暗室内",    3.0,   H.TEAL,   "屏幕偏亮"),
    ("室内照明",    50.0,  H.GREEN,  "刚刚好"),
    ("阴天户外",    800.0, H.GOLD,   "屏幕偏暗"),
    ("晴天户外",    1e4,   H.ORANGE, "屏幕看不清"),
]
SCREEN = 300.0     # 同一块屏幕的物理亮度（nit）
FAN = 40.0         # 工作区间半宽（共约 3.2 个数量级）


def fmt(v):
    return f"{v:g}"


def logticks(ax, which, ticks):
    lab = [r"$10^{%d}$" % int(round(np.log10(t))) for t in ticks]
    if which == "x":
        ax.set_xticks(ticks); ax.set_xticklabels(lab)
        ax.xaxis.set_minor_formatter(NullFormatter())
    else:
        ax.set_yticks(ticks); ax.set_yticklabels(lab)
        ax.yaxis.set_minor_formatter(NullFormatter())


fig = plt.figure(figsize=(7.2, 5.3))
gs = fig.add_gridspec(2, 1, height_ratios=[1.25, 1.0], hspace=0.42)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# ---------------- 上：工作区间平移 ----------------
for i, (nm, la, c, verdict) in enumerate(SCENES):
    y = len(SCENES) - 1 - i
    ax1.plot([la / FAN, la * FAN], [y, y], lw=10, solid_capstyle="butt",
             color=c, alpha=0.80, zorder=3)
    ax1.plot([la], [y], "D", color="white", ms=4.6, mec=c, mew=1.6, zorder=5)

ax1.plot([1e-6, 1e5], [-0.95, -0.95], lw=6, color=H.LGRAY, solid_capstyle="butt", zorder=2)
ax1.text(1.3e-6, -1.35, "人眼可感范围 0.000001 – 100000 nit（约 11 个数量级）",
         fontsize=8.2, color=H.GRAY, ha="left", va="bottom")

ax1.axvline(SCREEN, color=H.RED, lw=2.2, ls="--", zorder=4)
ax1.text(SCREEN * 1.3, 6.55, "同一块屏幕 300 nit", color=H.RED, fontsize=8.8,
         ha="left", va="center", fontweight="bold")

ax1.set_xscale("log")
ax1.set_xlim(1e-6, 1e6); ax1.set_ylim(-1.9, 7.0)
logticks(ax1, "x", [1e-6, 1e-4, 1e-2, 1, 1e2, 1e4, 1e6])
ax1.set_yticks(range(len(SCENES)))
ax1.set_yticklabels(
    [f"{nm}（适应 ≈ {fmt(la)} nit）→ {v}" for nm, la, c, v in SCENES][::-1], fontsize=8.2)
ax1.tick_params(axis="y", length=0)
ax1.set_xlabel("物理亮度（nit，对数轴）")
ax1.set_title("光适应：眼睛的“工作区间”随环境整体左移 / 右移", fontsize=10.5)

# ---------------- 下：适应曲线平移 ----------------
Ls = np.logspace(-6, 6, 900)
n = 0.7
ax2.axhline(0.5, color=H.GRAY, lw=1.0, ls=":")
ax2.plot([SCREEN, SCREEN], [0, 1.04], color=H.RED, lw=2.2, ls="--", zorder=2)

for nm, la, c, verdict in SCENES:
    ax2.plot(Ls, Ls ** n / (Ls ** n + la ** n), color=c, lw=2.0, zorder=3)

# 结果小表（放在最上方“无机线”的空白带内，颜色对应曲线）
rows = [("暗夜 / 星光", 1e-3, H.NAVY, "刺眼、过曝"),
        ("室内照明", 50.0, H.GREEN, "舒服"),
        ("晴天户外", 1e4, H.ORANGE, "暗弱、看不清")]
ax2.text(1.5e-6, 1.79, "同一块 300 nit 屏幕的响应（对应曲线上的圆点）：",
         fontsize=8.2, color="#333333", ha="left", va="top")
for k, (nm, la, c, note) in enumerate(rows):
    r = SCREEN ** n / (SCREEN ** n + la ** n)
    ax2.text(1.5e-6, 1.635 - 0.155 * k, f"{nm}：{r:.2f}（{note}）",
             fontsize=8.2, color=c, ha="left", va="top")
    ax2.plot([SCREEN], [r], "o", color=c, ms=5.6, mec="white", mew=0.9, zorder=6)

ax2.text(1.5e-6, 1.17, "曲线中点（响应 0.5）＝该场景的适应水平",
         fontsize=8.2, color="#444444", ha="left", va="top")

ax2.set_xscale("log")
ax2.set_xlim(1e-6, 1e6); ax2.set_ylim(0, 1.85)
logticks(ax2, "x", [1e-6, 1e-4, 1e-2, 1, 1e2, 1e4, 1e6])
ax2.set_xlabel("物理亮度（nit，对数轴）")
ax2.set_ylabel("主观响应")
ax2.set_title("同一物理亮度落在不同适应曲线上 → 观感完全不同", fontsize=10.5)

fig.suptitle("图 03-4　光适应：眼睛随时把“零点”搬到当前环境（暗适应慢、明适应快）",
             fontsize=12.5, fontweight="bold", y=0.995)
H.save(fig, 3, "f4_adaptation")
