# -*- coding: utf-8 -*-
"""图 19-4　色彩管理链路：源 → 源配置文件 → CMM/PCS → 目标配置文件 → 目标设备。

上排给出标准 ICC 色彩管理链路（以与设备无关的 PCS 为桥梁，把源色彩空间
转换到目标色彩空间）；下排用色度图示意：源色域（如 DCI-P3）里超出目标
设备（sRGB）能力的颜色，会被映射/裁剪到目标色域边界内。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

fig = plt.figure(figsize=(7.2, 5.2))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.2], hspace=0.45)

# ================= 上：色彩管理链路 =================
axT = fig.add_subplot(gs[0]); axT.set_xlim(0, 100); axT.set_ylim(0, 10)
axT.axis("off"); axT.grid(False)
axT.set_title("色彩管理链路：源 → 配置文件 → 目标", pad=6, fontsize=11.8)

boxes = [
    ("源内容", "相机 / 素材\n源色彩空间", H.NAVY),
    ("源配置文件", "ICC / F32\n描述源的特性", H.BLUE),
    ("CMM", "色彩管理引擎\n做转换运算", H.ORANGE),
    ("PCS 连接空间", "XYZ / Lab\n与设备无关", H.GOLD),
    ("目标配置文件", "显示器 ICC\n描述屏幕特性", H.TEAL),
    ("目标设备", "显示 / 打印\n输出结果", H.GREEN),
]
n = len(boxes)
BW, BH, y0 = 13.0, 5.0, 2.3
gap = (100 - n * BW) / (n - 1)
xs = [i * (BW + gap) for i in range(n)]


def box(ax, x, y, w, h, fc, ec, radius=0.10, lw=1.3, z=3, alpha=1.0):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0.02,rounding_size={radius}",
                       linewidth=lw, edgecolor=ec, facecolor=fc, alpha=alpha,
                       zorder=z)
    ax.add_patch(p)
    return p


for (title, note, c), x in zip(boxes, xs):
    is_pcs = title.startswith("PCS")
    yy = y0 - 0.35 if is_pcs else y0
    hh = BH + 0.7 if is_pcs else BH
    box(axT, x, yy, BW, hh, c, c, radius=0.12,
        lw=2.2 if is_pcs else 1.3, alpha=0.90 if not is_pcs else 1.0)
    axT.text(x + BW / 2, yy + hh * 0.68, title, ha="center", va="center",
             color="white", fontsize=8.6, fontweight="bold", zorder=4)
    axT.text(x + BW / 2, yy + hh * 0.28, note, ha="center", va="center",
             color="white", fontsize=5.9, alpha=0.95, linespacing=1.35, zorder=4)

for i in range(n - 1):
    x0 = xs[i] + BW
    x1 = xs[i + 1]
    axT.add_patch(FancyArrowPatch((x0 + 0.2, y0 + BH / 2), (x1 - 0.2, y0 + BH / 2),
                                  arrowstyle="-|>", mutation_scale=12,
                                  linewidth=1.7, color=H.DARK, zorder=2))

axT.text(50, 0.50, "每个设备都用自己的“语言”（色彩空间）；CMM 借 PCS 把源语言翻译成目标语言",
         ha="center", va="center", fontsize=7.4, color=H.GRAY)

# ================= 下：色域映射示意 =================
axB = fig.add_subplot(gs[1]); axB.set_xlim(0.0, 0.80); axB.set_ylim(0.0, 0.92)
axB.set_xlabel("x", fontsize=9); axB.set_ylabel("y", fontsize=9)
axB.set_title("同一份颜色：源色域（P3）超出目标（sRGB）的部分被映射/裁剪",
              pad=6, fontsize=10.6)
axB.set_aspect("equal", adjustable="box")

# 近似的 CIE 1931 光谱轨迹（示意）
locus = np.array([
    (0.1741, 0.0050), (0.1733, 0.0048), (0.1714, 0.0051), (0.1649, 0.0109),
    (0.1440, 0.0297), (0.0913, 0.1327), (0.0082, 0.5384), (0.0743, 0.8338),
    (0.2296, 0.7543), (0.3731, 0.6245), (0.5125, 0.4866), (0.6270, 0.3725),
    (0.6915, 0.3083), (0.7190, 0.2809), (0.7260, 0.2740), (0.7283, 0.2717),
    (0.7347, 0.2653)])
axB.plot(locus[:, 0], locus[:, 1], color="#b8c2cc", lw=1.4)
axB.plot([0.7347, 0.1741], [0.2653, 0.0050], color="#b8c2cc", lw=1.4)
axB.fill(locus[:, 0], locus[:, 1], color="#eef3f9", alpha=0.6, zorder=0)

# 源色域 DCI-P3、目标色域 sRGB
p3 = np.array([(0.680, 0.320), (0.265, 0.690), (0.150, 0.060)])
srgb = np.array([(0.640, 0.330), (0.300, 0.600), (0.150, 0.060)])
axB.add_patch(Polygon(p3, closed=True, fill=True, facecolor=H.ORANGE,
                      alpha=0.14, edgecolor=H.ORANGE, lw=2.2, zorder=1))
axB.add_patch(Polygon(srgb, closed=True, fill=True, facecolor=H.NAVY,
                      alpha=0.12, edgecolor=H.NAVY, lw=2.2, zorder=2))

# 直接标注，避免图例拥挤
axB.text(0.27, 0.745, "源色域 DCI-P3", ha="left", va="bottom", fontsize=8.6,
         color=H.ORANGE, fontweight="bold")
axB.text(0.30, 0.555, "目标色域 sRGB", ha="center", va="top", fontsize=8.6,
         color=H.NAVY, fontweight="bold")

# 白点
axB.plot(0.3127, 0.3290, "o", color=H.DARK, ms=6, zorder=5)
axB.annotate("D65 白点", (0.3127, 0.3290), textcoords="offset points",
             xytext=(8, -12), fontsize=8, color=H.DARK)

# 越界颜色的映射箭头
for corner in [p3[0], p3[1]]:
    inner = corner * 0.68 + np.array([0.3127, 0.3290]) * 0.32
    axB.annotate("", xy=inner, xytext=corner,
                 arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=1.5))
axB.text(0.02, 0.86, "超出目标色域的颜色 → 裁剪 / 压缩映射",
         ha="left", va="center", fontsize=8.2, color=H.RED, fontweight="bold")

fig.suptitle("色彩管理：让“源里是什么色”到“屏幕上就是什么色”", fontsize=12.5,
             fontweight="bold", y=1.0)
H.save(fig, 19, "f4_color_mgmt")
