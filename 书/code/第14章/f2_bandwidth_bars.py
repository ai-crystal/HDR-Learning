# -*- coding: utf-8 -*-
"""第 14 章 图 14-1：各接口版本的带宽条形图（原始带宽 vs 有效带宽）。
HDMI 1.4 / 2.0 / 2.1，DP 1.2 / 1.4 / 2.x；虚线标出常见 HDR 组合的需求线。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt

# ---------------- 数据（Gbps） ----------------
# (显示名, 原始带宽, 有效带宽, 家族颜色, 有效带宽占比说明)
data = [
    ("HDMI 1.4",        10.2, 8.16,  H.BLUE,   "8b/10b"),
    ("HDMI 2.0 / 2.0b", 18.0, 14.40, H.BLUE,   "8b/10b"),
    ("HDMI 2.1 / 2.1a", 48.0, 42.67, H.NAVY,   "FRL 16b/18b"),
    ("DP 1.2",          21.6, 17.28, H.TEAL,   "8b/10b"),
    ("DP 1.4",          32.4, 25.92, H.TEAL,   "8b/10b"),
    ("DP 2.0 / 2.1",    80.0, 77.37, H.GREEN,  "UHBR20 128b/132b"),
]

names  = [d[0] for d in data]
raw    = np.array([d[1] for d in data])
eff    = np.array([d[2] for d in data])
colors = [d[3] for d in data]
notes  = [d[4] for d in data]

y = np.arange(len(data))[::-1]      # 从上到下：HDMI 家族，再 DP 家族

fig, ax = plt.subplots(figsize=(7.2, 4.4))

# 家族底色分区
ax.axhspan(-0.6, 2.6, color=H.TEAL, alpha=0.05, zorder=0)
ax.axhspan(2.6, 5.6, color=H.BLUE, alpha=0.05, zorder=0)
ax.text(0.985, 0.615, "HDMI 家族", transform=ax.transAxes, fontsize=8.6,
        color=H.NAVY, ha="right", va="center", style="italic", alpha=0.85)
ax.text(0.985, 0.20, "DisplayPort 家族", transform=ax.transAxes, fontsize=8.6,
        color=H.TEAL, ha="right", va="center", style="italic", alpha=0.85)

ax.barh(y + 0.19, raw, height=0.34, color="#dbe3ec", edgecolor="#9fb0c4",
        linewidth=0.8, label="原始带宽（线速率）", zorder=3)
ax.barh(y - 0.19, eff, height=0.34, color=colors, edgecolor="white",
        linewidth=0.6, label="有效带宽（真正能装画面的）", zorder=3)

# 数值标注（含编码开销说明）
for yy, r, e, n in zip(y, raw, eff, notes):
    ax.text(r + 1.2, yy + 0.19, f"{r:g} Gbps", va="center", ha="left",
            fontsize=8.2, color="#65788c")
    ax.text(e + 1.2, yy - 0.19, f"{e:g}　({n}，编码开销 {100*(1-e/r):.0f}%)",
            va="center", ha="left", fontsize=8.0, color=H.DARK, fontweight="bold",
            bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none", alpha=0.82), zorder=6)

# 需求参考线（均含约 1.25 的协议开销因子）
refs = [
    (18.66, H.ORANGE, "4K60 10bit 4:4:4 ≈ 18.7 Gbps"),
    (37.32, H.RED,    "4K120 10bit 4:4:4 ≈ 37.3 Gbps"),
]
for xv, c, lab in refs:
    ax.axvline(xv, color=c, ls="--", lw=1.8, zorder=5, label=lab)

# 结论注记（放在右上空白处）
ax.text(52, 4.05,
        "HDMI 2.0（18）差一点点装不下 4K60 10bit 4:4:4（18.7）\n"
        "→ 该档位只好降成 8bit 4:4:4 或 10bit 4:2:0",
        fontsize=8.2, color=H.RED, ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.3", fc="#fdf1ec", ec=H.RED, lw=0.9, alpha=0.95), zorder=7)

ax.set_yticks(y)
ax.set_yticklabels(names, fontsize=9.5)
ax.set_xlabel("带宽（Gbps）")
ax.set_xlim(0, 100)
ax.set_ylim(-0.65, 5.5)
ax.set_title("图 14-1　HDMI / DisplayPort 各版本带宽：别只看“原始”，有效带宽才装得下画面", pad=12)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=2, fontsize=8.4)
ax.grid(axis="y", visible=False)
ax.grid(axis="x", color="#dde3ea", lw=0.7)

fig.tight_layout()
H.save(fig, 14, "f2_bandwidth_bars")
