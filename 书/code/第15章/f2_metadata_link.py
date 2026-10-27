# -*- coding: utf-8 -*-
"""第15章 图2：AVI InfoFrame 携带 HDR 元数据的链路与字段示意。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(7.2, 5.8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 9.6)
ax.axis("off")


def rbox(x, y, w, h, fc="#ffffff", ec=H.GRAY, lw=1.2, r=0.08, z=3, alpha=1.0):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={r}",
                       fc=fc, ec=ec, lw=lw, zorder=z, alpha=alpha)
    ax.add_patch(p)
    return p


def sec(y, txt, color=H.NAVY):
    ax.add_patch(FancyBboxPatch((0.26, y - 0.15), 0.16, 0.3,
                 boxstyle="round,pad=0,rounding_size=0.04",
                 fc=color, ec="none", zorder=4))
    ax.text(0.56, y, txt, ha="left", va="center", fontsize=9.5,
            color=color, fontweight="bold", zorder=4)


ax.set_title("图 15-2　元数据怎么随链路走：AVI InfoFrame 携带的 HDR 信息",
             fontsize=12.4, fontweight="bold", pad=8)

# ---------------- ① 逐帧传输 ----------------
sec(9.25, "① 元数据随每一帧走：画面帧和 AVI InfoFrame 打包在同一条链路上")
fx0, fw, fgap, fy, fh = 0.3, 1.25, 0.10, 7.90, 0.95
for i in range(6):
    x = fx0 + i * (fw + fgap)
    rbox(x, fy, fw, fh, fc="#f6f9fc", ec=H.NAVY, lw=1.1, r=0.06)
    ax.text(x + fw / 2, fy + fh - 0.25, "画面帧", ha="center", va="center",
            fontsize=6.6, color=H.NAVY, fontweight="bold", zorder=5)
    ax.add_patch(FancyBboxPatch((x + 0.06, fy + 0.07), fw - 0.12, 0.33,
                 boxstyle="round,pad=0,rounding_size=0.04",
                 fc=H.TEAL, ec="none", zorder=5))
    ax.text(x + fw / 2, fy + 0.235, "AVI IF", ha="center", va="center",
            fontsize=5.6, color="white", fontweight="bold", zorder=6)

ax.add_patch(FancyArrowPatch((8.36, fy + fh / 2), (9.33, fy + fh / 2),
             arrowstyle="-|>", mutation_scale=16, color=H.GREEN, lw=2.2, zorder=4))
ax.text(8.85, fy + fh / 2 + 0.20, "逐帧", ha="center", va="bottom",
        fontsize=7.2, color=H.GREEN, fontweight="bold")
rbox(9.45, fy - 0.13, 2.35, fh + 0.26, fc="#eafaf1", ec=H.GREEN, lw=1.5, r=0.10)
ax.text(10.62, fy + fh / 2 + 0.08, "显示器 / 电视", ha="center", va="center",
        fontsize=8.3, color=H.GREEN, fontweight="bold", zorder=5)
ax.text(10.62, fy + fh / 2 - 0.30, "逐帧接收并解析元数据", ha="center", va="center",
        fontsize=6.8, color=H.DARK, zorder=5)

# ---------------- ② 信息帧结构 ----------------
sec(7.18, "② 帧内的 AVI InfoFrame 字节结构（Packet Type = 0x82，逐帧更新）")
cells = [
    ("Byte 1", "包类型", "0x82", H.NAVY, "#f2f6fb"),
    ("Byte 2", "版本", "Version", H.GRAY, "#ffffff"),
    ("Byte 3", "长度", "Length", H.GRAY, "#ffffff"),
    ("PB0", "校验", "Checksum", H.GRAY, "#ffffff"),
    ("PB1", "扫描 / 条形", "信息", H.GRAY, "#ffffff"),
    ("PB2", "色彩空间", "C1C0", H.ORANGE, "#fdf3e7"),
    ("PB3", "像素编码", "位深/采样", H.ORANGE, "#fdf3e7"),
    ("PB4", "视频格式", "VIC", H.GRAY, "#ffffff"),
    ("PB5", "EOTF", "元数据标识", H.RED, "#fdecea"),
    ("PB6–8", "静态元数据", "SMD", H.RED, "#fdecea"),
]
cy, ch = 5.72, 1.18
cw = (11.6 - 9 * 0.08) / 10
for i, (top, mid, sub, ec, fc) in enumerate(cells):
    x = 0.2 + i * (cw + 0.08)
    rbox(x, cy, cw, ch, fc=fc, ec=ec, lw=1.3, r=0.06)
    ax.text(x + cw / 2, cy + ch - 0.22, top, ha="center", va="center",
            fontsize=6.0, color=H.GRAY, fontweight="bold", zorder=5)
    ax.text(x + cw / 2, cy + ch / 2 + 0.02, mid, ha="center", va="center",
            fontsize=7.3, color=ec, fontweight="bold", zorder=5)
    ax.text(x + cw / 2, cy + 0.20, sub, ha="center", va="center",
            fontsize=5.7, color=H.DARK, zorder=5)

# ---------------- ③ 携带的 HDR 关键字段 ----------------
sec(5.05, "③ 这张“说明书”里，HDR10 会写清下面四件事")
cards = [
    (H.TEAL, "色彩空间", ["色度 C1C0 = BT.2020", "（SDR 回退 BT.709）"]),
    (H.RED, "EOTF / 传递函数", ["PQ（ET = 10）", "HLG（ET = 11）"]),
    (H.PURPLE, "静态元数据 SMD", ["母版显示亮度", "MaxCLL / MaxFALL"]),
    (H.BLUE, "像素编码", ["10bit 色深", "4:4:4 / 4:2:2 / 4:2:0"]),
]
cw2 = (11.6 - 3 * 0.2) / 4
for i, (color, title, lines) in enumerate(cards):
    x = 0.2 + i * (cw2 + 0.2)
    rbox(x, 3.50, cw2, 1.42, fc="#f7f9fc", ec=color, lw=1.7, r=0.09)
    ax.text(x + 0.14, 4.62, title, ha="left", va="center", fontsize=8.3,
            color=color, fontweight="bold", zorder=5)
    for j, ln in enumerate(lines):
        ax.text(x + 0.14, 4.24 - j * 0.36, ln, ha="left", va="center",
                fontsize=7.2, color=H.DARK, zorder=5)

# ---------------- 底部要点 ----------------
rbox(0.2, 0.35, 11.6, 2.72, fc="#f3f6fa", ec=H.LGRAY, lw=1.4, r=0.10)
ax.text(0.46, 2.72, "要点", ha="left", va="center", fontsize=8.6,
        color=H.NAVY, fontweight="bold", zorder=5)
notes = [
    ("元数据随链路逐帧传：显卡 → 线材 → 接口 → 显示器，每一环都得“认识”它。", H.NAVY),
    ("HDR10 的静态元数据（母版亮度 / MaxCLL / MaxFALL）走 AVI InfoFrame · CTA-861。", H.DARK),
    ("HDR10+ / Dolby Vision 的动态元数据走专用通道；不支持时播放器向下兼容为 HDR10。", H.DARK),
    ("任一环不认识元数据 → 系统里有 HDR 开关，画面却仍按 SDR 放、发灰发平。", H.RED),
]
for i, (txt, c) in enumerate(notes):
    ax.text(0.46, 2.26 - i * 0.52, ("· " + txt), ha="left", va="center",
            fontsize=7.9, color=c, fontweight=("bold" if i in (0, 3) else "normal"))

H.save(fig, 15, "f2_metadata_link")
