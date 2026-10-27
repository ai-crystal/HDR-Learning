# -*- coding: utf-8 -*-
"""第 03 章 图 5　同时对比：相同灰块在不同背景下“看起来不一样亮”。

用 PIL 直接绘制像素图：两块内部灰块的 RGB 完全相同（均为 140），
周围背景一黑一白；下方再加一条黑→白渐变背景，放 7 块同样的灰。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import numpy as np
import hdrfig as H
from PIL import Image, ImageDraw
plt = H.plt

GRAY = (140, 140, 140)
W, Hh = 1240, 720
img = Image.new("RGB", (W, Hh), "white")
d = ImageDraw.Draw(img)

# ---- 上排：黑背景 / 白背景 + 完全相同的灰块 ----
d.rectangle([40, 60, 600, 430], fill=(10, 10, 10))
d.rectangle([260, 175, 380, 295], fill=GRAY)
d.rectangle([640, 60, 1200, 430], fill=(242, 242, 242))
d.rectangle([860, 175, 980, 295], fill=GRAY)
d.rectangle([640, 60, 1200, 430], outline=(210, 210, 210))

# ---- 下：黑→白渐变背景 + 7 块同样的灰 ----
gx0, gx1, gy0, gy1 = 40, 1200, 500, 670
for x in range(gx0, gx1):
    v = int(round(255 * (x - gx0) / (gx1 - gx0)))
    d.line([(x, gy0), (x, gy1)], fill=(v, v, v))
step = (gx1 - gx0) / 7.0
for i in range(7):
    cx = gx0 + (i + 0.5) * step
    d.rectangle([cx - 45, gy0 + 25, cx + 45, gy1 - 25], fill=GRAY)

# ---------------- matplotlib 叠加中文标注 ----------------
fig = plt.figure(figsize=(7.2, 7.2 * Hh / W))
ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(img)
ax.set_xlim(0, W); ax.set_ylim(Hh, 0)
ax.axis("off")

ax.text(620, 24, "图 03-5　同时对比：灰块的“亮暗”由邻居决定",
        ha="center", va="center", fontsize=12, fontweight="bold", color="#1f4e79")
ax.text(620, 48, "两块灰的 RGB 完全相同：(140, 140, 140)",
        ha="center", va="center", fontsize=9.8, color="#333333")
ax.annotate("", xy=(322, 170), xytext=(560, 62),
            arrowprops=dict(arrowstyle="->", color="#555555", lw=1.2))
ax.annotate("", xy=(918, 170), xytext=(680, 62),
            arrowprops=dict(arrowstyle="->", color="#555555", lw=1.2))

ax.text(320, 100, "背景：全黑  (0, 0, 0)", ha="center", va="center",
        fontsize=9, color="white")
ax.text(920, 100, "背景：全白  (242, 242, 242)", ha="center", va="center",
        fontsize=9, color="#333333")
ax.text(320, 340, "被黑包围 → 感觉更亮", ha="center", va="center",
        fontsize=10.5, color="white", fontweight="bold")
ax.text(920, 340, "被白包围 → 感觉更暗", ha="center", va="center",
        fontsize=10.5, color="#222222", fontweight="bold")

for cx in (320, 920):
    ax.plot([cx], [235], "+", color="#c0392b", ms=11, mew=1.6)

ax.text(620, 466, "同一块灰（物理像素值一样），放到从黑到白的渐变背景上 —— 背景越亮，这块灰看起来越暗",
        ha="center", va="center", fontsize=9.2, color="#1f4e79")
ax.text(44, 492, "背景 0", ha="left", va="bottom", fontsize=8.2, color="#7f8c8d")
ax.text(1196, 492, "背景 255", ha="right", va="bottom", fontsize=8.2, color="#7f8c8d")

ax.text(122, 676, "最亮", ha="center", va="top", fontsize=8.6, color="#333333")
ax.text(1117, 676, "最暗", ha="center", va="top", fontsize=8.6, color="#333333")

ax.text(620, 708,
        "物理量相同 ≠ 感知量相同：视觉系统判断的是“与邻域的对比”，而不是绝对亮度",
        ha="center", va="center", fontsize=9.6, color="#c0392b", fontweight="bold")

H.save(fig, 3, "f5_simultaneous")
