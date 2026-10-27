# -*- coding: utf-8 -*-
"""图 13-3　“假 HDR”识别流程图。

从“看到‘支持 HDR’”出发，先问有没有 VESA 认证，再看实测峰值与分区调光，
最后落到“入门可用 / 谨慎乐观 / 假 HDR”三类结论，并在底部列出五个典型特征。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
from matplotlib.patches import FancyBboxPatch, Polygon

fig, ax = H.plt.subplots(figsize=(7.2, 5.6))
ax.set_xlim(0, 12)
ax.set_ylim(0, 11.0)
ax.axis("off")
ax.grid(False)

FILL_OK = "#e6f4ec"      # 绿：正面
FILL_BAD = "#fbe9e7"     # 红：负面
FILL_DEC = "#fdf3e3"     # 橙：判定
FILL_BOX = "#eaf1f8"     # 蓝：信息


def box(x, y, w, h, text, fill, edge, fs=8.5, bold=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.0,rounding_size=0.14",
                                linewidth=1.3, edgecolor=edge, facecolor=fill,
                                zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=3,
            color="#1b2a3a", fontweight="bold" if bold else "normal",
            linespacing=1.5)


def diamond(x, y, w, h, text, fs=8.5):
    ax.add_patch(Polygon([[x - w / 2, y], [x - w * 0.24, y + h / 2],
                          [x + w / 2, y], [x + w * 0.24, y - h / 2]],
                         closed=True, linewidth=1.4, edgecolor=H.ORANGE,
                         facecolor=FILL_DEC, zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=3,
            color="#1b2a3a", fontweight="bold", linespacing=1.5)


def arrow(p1, p2, color=H.NAVY, rad=0.0, lw=1.3):
    ax.annotate("", xy=p2, xytext=p1, zorder=1,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=1.5, shrinkB=1.5,
                                connectionstyle=f"arc3,rad={rad}"))


def tag(x, y, text, color):
    ax.text(x, y, text, ha="center", va="center", fontsize=8.5, color=color,
            fontweight="bold", zorder=4,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))


# ---------- 起点与第一层判定 ----------
box(6, 10.30, 5.4, 0.76, "看到宣传语：“支持 HDR” / “HDR Ready”", FILL_BOX,
    H.NAVY, 9.6, bold=True)
diamond(6, 8.90, 6.5, 1.5, "有 VESA DisplayHDR 认证吗？", 9.2)
arrow((6, 9.92), (6, 9.65))

# ---------- 左支：有认证 ----------
box(3.0, 7.30, 5.6, 0.74, "有认证 → 读「等级 + 所属族」", FILL_BOX, H.NAVY, 9.0,
    bold=True)
box(3.0, 6.10, 5.6, 0.62, "400 / 500 → 入门级，别期待惊艳", "#f2f4f6", H.GRAY, 8.6)
box(3.0, 5.05, 5.6, 0.62, "600 / 1000 / 1400 → 有分区调光，像样", FILL_OK, H.GREEN, 8.6)
box(3.0, 4.00, 5.6, 0.62, "True Black 400/500/600 → ≈0.0005 nit，看黑场",
    "#e4f2f1", H.TEAL, 8.4)
arrow((2.85, 8.62), (3.0, 7.69), H.GREEN, rad=0.08)
tag(2.30, 8.20, "有", H.GREEN)
for y0, y1 in [(6.90, 6.42), (5.77, 5.37), (4.72, 4.32)]:
    arrow((3.0, y0), (3.0, y1), H.NAVY)
ax.text(3.0, 3.28, "认证是“及格线” → 还要看实测成绩", ha="center", fontsize=8.2,
        color=H.TEAL, fontweight="bold")

# ---------- 右支：没有认证 ----------
diamond(9.0, 7.30, 5.5, 1.8, "实测峰值 ≥ 400 nit\n且带分区调光？", 8.8)
arrow((9.15, 8.62), (9.0, 8.22), H.RED, rad=-0.08)
tag(9.75, 8.20, "没有", H.RED)
box(7.60, 5.45, 2.70, 1.36, "是 → 谨慎乐观\n合格的入门 HDR", FILL_OK, H.GREEN, 8.2,
    bold=True)
box(10.40, 5.45, 2.70, 1.36, "否 → 基本是\n「假 HDR」", FILL_BAD, H.RED, 8.2,
    bold=True)
arrow((8.90, 6.40), (7.62, 6.15), H.GREEN, rad=0.22)
arrow((9.10, 6.40), (10.38, 6.15), H.RED, rad=-0.22)
tag(8.20, 6.34, "是", H.GREEN)
tag(9.80, 6.34, "否", H.RED)
box(9.0, 3.35, 5.4, 1.05, "跨族比“对比度”，不比峰值数字\n无认证的产品看实测峰值 + 分区调光",
    "#f7f9fb", H.GRAY, 8.2)

# ---------- 底部：五个特征 ----------
ax.add_patch(FancyBboxPatch((0.35, 0.45), 11.3, 1.90,
                            boxstyle="round,pad=0.0,rounding_size=0.14",
                            linewidth=1.3, edgecolor=H.RED, facecolor="#fdf1ef",
                            zorder=2))
ax.text(6.0, 2.06, "「假 HDR」五个典型特征", ha="center", va="center",
        fontsize=9.2, color=H.RED, fontweight="bold", zorder=3)
ax.text(6.0, 1.58,
        "① 只写「支持 HDR」、无任何认证　② 峰值亮度 < 400 nit　"
        "③ 无分区调光（或仅侧入式）",
        ha="center", va="center", fontsize=8.0, color="#1b2a3a", zorder=3)
ax.text(6.0, 1.14,
        "④ 仅 8bit、色域接近纯 sRGB　⑤ 只宣传「支持 HDR 视频解码」"
        "——能“读”信号 ≠ 能“显示”效果",
        ha="center", va="center", fontsize=8.0, color="#1b2a3a", zorder=3)
ax.text(6.0, 0.70,
        "记住：「支持 HDR」是能力描述，「DisplayHDR xxx」才是能力证明",
        ha="center", va="center", fontsize=8.4, color=H.NAVY, zorder=3,
        fontweight="bold")

fig.suptitle("“假 HDR”识别流程：认证 → 实测峰值 → 分区调光", fontsize=12.5,
             fontweight="bold", y=0.99)

H.save(fig, 13, "f3_fake_hdr")
