# -*- coding: utf-8 -*-
"""f5_codecs：HEVC / VP9 / AV1 对 HDR 的支持对比（矩阵 + 压缩效率）。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import numpy as np
from matplotlib.patches import Rectangle

features = [
    "HDR10（PQ + 静态元数据）",
    "HDR10+（动态元数据）",
    "Dolby Vision（RPU）",
    "10bit 支持",
    "12bit 支持",
    "BT.2020 宽色域",
    "ICtCp（HDR 感知恒定）",
    "免专利 / 开放",
]
codecs = ["HEVC\n(H.265)", "VP9", "AV1"]
# 2 = 支持(✓)，1 = 部分/有限(△)，0 = 不支持(✗)
M = np.array([
    [2, 2, 2],   # HDR10
    [2, 0, 1],   # HDR10+
    [2, 0, 1],   # Dolby Vision
    [2, 2, 2],   # 10bit
    [2, 1, 2],   # 12bit
    [2, 2, 2],   # BT.2020
    [1, 0, 1],   # ICtCp
    [0, 2, 2],   # 免专利
], dtype=float)
SYM = {2: "√", 1: "△", 0: "×"}
FACE = {2: "#dff2e3", 1: "#fbefd3", 0: "#f7dcd8"}
EDGE = {2: H.GREEN, 1: H.GOLD, 0: H.RED}

fig = H.plt.figure(figsize=(7.2, 5.2))
gs = fig.add_gridspec(2, 1, height_ratios=[2.3, 1.0], hspace=0.35,
                      left=0.03, right=0.97, top=0.90, bottom=0.09)

# ---------- 上：对比矩阵 ----------
axt = fig.add_subplot(gs[0])
axt.set_xlim(0, 3); axt.set_ylim(0, len(features))
axt.invert_yaxis()
axt.set_xticks([]); axt.set_yticks([])
axt.grid(False)
for s in axt.spines.values():
    s.set_visible(False)

for j, c in enumerate(codecs):
    axt.text(j + 0.5, -0.45, c, ha="center", va="center", fontsize=10.5,
             color=H.NAVY, fontweight="bold")
for i, f in enumerate(features):
    axt.text(-0.08, i + 0.5, f, ha="right", va="center", fontsize=9,
             color="#333333")
    for j in range(3):
        v = int(M[i, j])
        axt.add_patch(Rectangle((j + 0.02, i + 0.02), 0.96, 0.96,
                                facecolor=FACE[v], edgecolor=EDGE[v],
                                linewidth=1.4))
        axt.text(j + 0.5, i + 0.5, SYM[v], ha="center", va="center",
                 fontsize=15, color=EDGE[v], fontweight="bold")

# 图例
axt.text(0.0, len(features) + 0.55,
         "√ 原生支持　　△ 有限/派生支持　　× 不支持（或需额外封装）",
         fontsize=8.8, color=H.GRAY, va="center")

# ---------- 下：同等画质下的码率（相对 HEVC） ----------
axb = fig.add_subplot(gs[1])
names = ["HEVC", "VP9", "AV1"]
rates = [100, 97, 70]
cols = [H.GRAY, H.BLUE, H.GREEN]
bars = axb.barh(names, rates, color=cols, height=0.55)
axb.set_xlim(0, 118)
axb.invert_yaxis()
axb.set_xlabel("同等画质下的码率（相对 HEVC，越低越省）", fontsize=9.5)
for b, r in zip(bars, rates):
    axb.text(r + 2, b.get_y() + b.get_height() / 2, f"{r}%",
             va="center", fontsize=9.5, fontweight="bold", color=H.NAVY)
axb.set_title("压缩效率：AV1 在同等画质下约省 30% 码率（示意）",
              fontsize=10, color=H.NAVY, loc="left", pad=6)
axb.grid(axis="y", visible=False)

fig.suptitle("图 10-5　HEVC / VP9 / AV1 的 HDR 支持对比",
             fontsize=13, fontweight="bold", y=0.99)
H.save(fig, 10, "f5_codecs")
