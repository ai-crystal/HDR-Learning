# -*- coding: utf-8 -*-
"""图 09-2　HDR10 / HDR10+ / Dolby Vision 对比。

上半：亮度适配粒度——同一部影片的三条"调参时间线"：
      HDR10 全片一套；HDR10+ 逐场景；DV 逐场景/逐帧。
下半：属性对照表（元数据、授权、位深、色彩编码、向下兼容、生态）。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import numpy as np
import hdrfig as H

plt = H.plt

# 场景划分（与 f1 呼应）
scenes = [
    ("烛光", 90, H.ORANGE),
    ("夜街", 70, H.PURPLE),
    ("室内", 120, H.TEAL),
    ("雪原", 130, H.NAVY),
    ("烟花", 60, H.RED),
    ("黄昏", 90, H.GOLD),
]
total = sum(s[1] for s in scenes)
bounds = np.cumsum([0] + [s[1] for s in scenes])

fig = plt.figure(figsize=(7.2, 6.6))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.05], hspace=0.5)

# ============================================================ 上：适配粒度
ax = fig.add_subplot(gs[0])
rowh = 0.62

rows = [
    ("HDR10", 2.0, H.RED,  "静态：全片一套"),
    ("HDR10+", 1.0, H.ORANGE, "动态：逐场景"),
    ("Dolby Vision", 0.0, H.NAVY, "动态：逐场景 / 逐帧"),
]
for name, y, c, sub in rows:
    ax.axhspan(y - rowh / 2, y + rowh / 2, color=c, alpha=0.07, lw=0)
    if name == "HDR10":
        ax.plot([0, total], [y, y], color=c, lw=3.0)
        ax.scatter([total / 2], [y], color=c, s=70, zorder=5)
        ax.text(total / 2, y + 0.34, "一套参数（折中）", ha="center",
                fontsize=8, color=c, fontweight="bold")
    else:
        for i, (sname, n, sc) in enumerate(scenes):
            s, e = bounds[i], bounds[i + 1]
            seg_color = sc if float(e) else c
            ax.plot([s + 4, e - 4], [y, y], color=sc, lw=3.2,
                    solid_capstyle="butt")
            ax.text((s + e) / 2, y, sname, ha="center", va="center",
                    fontsize=7.5, color="white", fontweight="bold")
            ax.scatter([(s + e) / 2], [y], color=sc, s=0, zorder=5)
        if name == "Dolby Vision":
            ik = np.linspace(0, total, 26)
            ax.scatter(ik, np.full_like(ik, y + 0.16), marker="v",
                       color=c, s=16, zorder=6)
            ax.text(total * 0.02, y + 0.36, "逐帧微调标记", fontsize=7.5,
                    color=c)

    ax.text(-14, y, name, ha="right", va="center", fontsize=9.5,
            fontweight="bold", color=c)
    ax.text(total + 8, y, sub, ha="left", va="center", fontsize=8, color=H.GRAY)

ax.set_xlim(-60, total + 150)
ax.set_ylim(-0.7, 2.8)
ax.set_yticks([])
ax.set_xticks([])
for sp in ("left", "right", "top"):
    ax.spines[sp].set_visible(False)
ax.set_xlabel("影片播放进度 →")
ax.set_title("亮度适配粒度：一张曝光表 → 每个场景一张 → 每帧一张",
             fontweight="bold")
ax.text(total / 2, -0.55, "参数可调的密度，从\"一部\"到\"一帧\"逐级加密",
        ha="center", fontsize=8.5, color=H.GRAY)

# ============================================================ 下：属性表
ax2 = fig.add_subplot(gs[1])
ax2.axis("off")

cols = ["HDR10", "HDR10+", "Dolby Vision"]
data = [
    ["元数据形式", "静态（全片一套）", "动态（逐场景/帧）", "动态（逐场景/帧）"],
    ["授权 / 成本", "开放免费", "开放免费（免版税）", "专有、需授权认证"],
    ["位深精度", "10bit", "10bit", "可支持 12bit"],
    ["色彩编码", "BT.2020 + YCbCr", "BT.2020 + YCbCr", "常用 ICtCp"],
    ["元数据载体", "无", "随码流", "RPU（参考处理单元）"],
    ["向下兼容", "——（基础）", "兼容 HDR10", "通常含 HDR10 基础层"],
    ["生态支持", "最广，几乎人人支持", "中等，硬件/内容偏少", "较广，依赖授权认证"],
    ["效果潜力", "够用，两端折中", "优于 HDR10", "通常最精细"],
]

# 手动绘制表，便于配色与强调
x0, y0 = 0.0, 0.0
colw = [0.205, 0.245, 0.275, 0.275]
rowh2 = 1.0 / (len(data) + 1)
ys = [1.0 - i * rowh2 for i in range(len(data) + 1)]
xs = [0.0]
for w in colw:
    xs.append(xs[-1] + w)
xs = [x / xs[-1] for x in xs]  # 归一化到 0..1

# 表头
head_colors = [H.RED, H.ORANGE, H.NAVY]
ax2.add_patch(plt.Rectangle((xs[1], ys[0] - rowh2), xs[-1] - xs[1], rowh2,
                            color=H.LGRAY, alpha=0.0))
ax2.text(xs[0] + 0.01, ys[0] - rowh2 / 2, "对比项", va="center",
         fontsize=9, fontweight="bold", color=H.DARK)
for j, cn in enumerate(cols):
    ax2.add_patch(plt.Rectangle((xs[j + 1], ys[0] - rowh2),
                                xs[j + 2] - xs[j + 1], rowh2,
                                color=head_colors[j], alpha=0.16, lw=0))
    ax2.text((xs[j + 1] + xs[j + 2]) / 2, ys[0] - rowh2 / 2, cn,
             ha="center", va="center", fontsize=9.5, fontweight="bold",
             color=head_colors[j])

for r, row in enumerate(data):
    yc = ys[r + 1] - rowh2 / 2
    if r % 2 == 0:
        ax2.add_patch(plt.Rectangle((xs[0], ys[r + 1] - rowh2),
                                    xs[-1] - xs[0], rowh2,
                                    color="#f4f7fa", lw=0))
    ax2.text(xs[0] + 0.01, yc, row[0], va="center", fontsize=8.5,
             fontweight="bold", color=H.DARK)
    for j in range(3):
        ax2.text((xs[j + 1] + xs[j + 2]) / 2, yc, row[j + 1],
                 ha="center", va="center", fontsize=8,
                 color="#333333")

# 网格线
for x in xs:
    ax2.plot([x, x], [ys[-1], ys[0]], color="#c7d0da", lw=0.7)
for y in ys:
    ax2.plot([xs[0], xs[-1]], [y, y], color="#c7d0da", lw=0.7)

ax2.set_xlim(-0.002, 1.002)
ax2.set_ylim(ys[-1] - 0.02, ys[0] + 0.04)
ax2.set_title("三者速查：HDR10 打底，HDR10+ 免费升级，Dolby Vision 最精细",
              fontweight="bold", fontsize=12)

fig.text(0.5, -0.01,
         "色彩编码栏的 ICtCp 与 RPU 是 Dolby Vision 的两大标签，见后两图",
         ha="center", fontsize=8.5, color=H.GRAY)

H.save(fig, 9, "f2_formats_compare")
