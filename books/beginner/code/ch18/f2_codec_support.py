# -*- coding: utf-8 -*-
"""第 18 章 图 2：HEVC / VP9 / AV1 对 HDR 元数据的支持对比。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle

rows = [
    "HDR10 静态元数据\n（ST 2086 + CLL）",
    "HDR10+ 动态元数据",
    "Dolby Vision（RPU）",
    "10bit / 12bit 色深",
    "BT.2020 广色域标识",
    "硬件解码普及度",
    "免版税 / 授权成本",
    "生态角色",
]
cols = ["HEVC (H.265)", "VP9", "AV1"]

data = [
    [(3, "完整"), (2, "部分"), (3, "完整")],
    [(3, "完整"), (0, "不支持"), (2, "支持（较新）")],
    [(3, "完整"), (0, "不支持"), (1, "新版支持")],
    [(3, "10 / 12bit"), (3, "10bit"), (3, "10 / 12bit")],
    [(3, "完整"), (3, "完整"), (3, "完整")],
    [(3, "很普及"), (2, "较普及"), (1, "普及中")],
    [(0, "专利池收费"), (3, "免版税"), (3, "免版税")],
    [(3, "蓝光 / 流媒体主力"), (2, "YouTube 主力"), (3, "新一代主流")],
]

score = np.array([[c[0] for c in row] for row in data], dtype=float)
lab = [[c[1] for c in row] for row in data]

# 0=不支持/有成本 → 红, 1=较弱 → 橙, 2=部分 → 金, 3=完整/成熟 → 绿
cmap = ListedColormap(["#e8b4ae", "#f6d5b0", "#f3e3a6", "#bfe0c4"])
ccol = ["#a63b2b", "#b06a1e", "#8a7414", "#1e7a41"]

fig = plt.figure(figsize=(7.2, 6.4))
gs = fig.add_gridspec(2, 1, height_ratios=[4.3, 1.25], hspace=0.42)
ax = fig.add_subplot(gs[0])
axb = fig.add_subplot(gs[1])

ax.imshow(score, cmap=cmap, vmin=-0.5, vmax=3.5, aspect="auto")
for i in range(len(rows)):
    for j in range(len(cols)):
        s = int(score[i, j])
        ax.text(j, i, lab[i][j], ha="center", va="center", fontsize=7.6,
                color=ccol[s], fontweight="bold")

ax.set_xticks(range(len(cols)))
ax.set_xticklabels(cols, fontsize=10, fontweight="bold", color=H.DARK)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels(rows, fontsize=8.0, color="#333")
ax.set_xticks(np.arange(-0.5, len(cols), 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(rows), 1), minor=True)
ax.grid(which="minor", color="white", linewidth=2.0)
ax.grid(which="major", visible=False)
ax.tick_params(which="minor", length=0)
ax.set_xticks([])
ax.set_xticklabels([])
# 重新画顶部列名
for j, c in enumerate(cols):
    ax.text(j, -0.72, c, ha="center", va="center", fontsize=9.6,
            fontweight="bold", color=H.DARK)
ax.set_title("HEVC / VP9 / AV1：谁能把 HDR 元数据完整带过去？", fontsize=12,
             fontweight="bold", color=H.DARK, pad=22)

# 图例
leg = [(3, "完整 / 成熟"), (2, "部分支持"), (1, "较弱 / 新版才有"), (0, "不支持 / 有成本")]
x0 = -0.5
for k, (s, t) in enumerate(leg):
    x = x0 + k * (len(cols) / 4.0)
    ax.add_patch(Rectangle((x + 0.06, len(rows) - 0.42), 0.22, 0.24,
                           facecolor=cmap(s), edgecolor="white", lw=1.0,
                           transform=ax.transData, clip_on=False))
    ax.text(x + 0.38, len(rows) - 0.30, t, ha="left", va="center", fontsize=7.0,
            color="#444", clip_on=False)

ax.text(-0.5, 0.0, "", transform=ax.transData)

# ---------- 下半部分：相同画质下的相对码率 ----------
names = ["HEVC", "VP9", "AV1"]
vals = [100, 110, 72]
colors = [H.NAVY, H.GOLD, H.GREEN]
bars = axb.bar(names, vals, color=colors, width=0.5, zorder=3)
for b, v in zip(bars, vals):
    axb.text(b.get_x() + b.get_width() / 2, v + 2.5, f"{v}%", ha="center",
             va="bottom", fontsize=8.6, fontweight="bold", color="#333")
axb.axhline(100, color=H.GRAY, lw=1.0, ls="--", zorder=2)
axb.text(-0.42, 120, "虚线为基准（HEVC = 100%）", ha="left", va="bottom", fontsize=7.0,
         color=H.GRAY)
axb.set_ylim(0, 132)
axb.set_ylabel("相对码率（%）", fontsize=9)
axb.set_title("相同主观画质下的相对码率：越低越省带宽（示意值）", fontsize=9.6,
              fontweight="bold", color=H.DARK)
axb.grid(axis="x", visible=False)
axb.tick_params(labelsize=9)

fig.text(0.5, 0.012,
         "评分综合“规范是否支持”与“生态成熟度”；实际能否用还取决于封装格式（MP4/WebM）、播放器与显卡是否实现。\n"
         "HDR 视频几乎都是 10bit 起步：PQ 曲线暗部陡，8bit 会压出一圈圈色带；省流量的平台有时会偷偷降回 8bit。",
         ha="center", va="bottom", fontsize=7.2, color="#555", linespacing=1.6)

H.save(fig, 18, "f2_codec_support")
