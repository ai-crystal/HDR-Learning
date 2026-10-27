# -*- coding: utf-8 -*-
"""第15章 图3：HDCP 版本不匹配的后果（黑屏 / 降级）示意。"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

fig, ax = plt.subplots(figsize=(7.2, 5.9))
ax.set_xlim(0, 12)
ax.set_ylim(0, 9.9)
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


ax.set_title("图 15-3　HDCP 这道闸门：版本不匹配会黑屏或降级",
             fontsize=12.4, fontweight="bold", pad=8)

# ---------------- ① 两种链路对比 ----------------
sec(9.55, "① 同一部 4K HDR 受保护影片，两种链路结局完全不同")

BX = [0.2, 2.85, 5.5, 8.15]
BW = 2.05
names = ["播放器 / 显卡", "线材", "功放 / 切换器", "显示器 / 电视"]


def chain(y, ver, color, result, rcolor, rface, bad_idx=None, flag=None):
    for i, (x, nm) in enumerate(zip(BX, names)):
        bad = (bad_idx is not None and i == bad_idx)
        fc = "#fdecea" if bad else "#f6f9fc"
        ec = H.RED if bad else color
        rbox(x, y, BW, 0.82, fc=fc, ec=ec, lw=1.6, r=0.07)
        ax.text(x + BW / 2, y + 0.56, nm, ha="center", va="center",
                fontsize=7.6, color=H.DARK, fontweight="bold", zorder=5)
        ax.text(x + BW / 2, y + 0.24, ver[i], ha="center", va="center",
                fontsize=7.3, color=(H.RED if bad else color),
                fontweight="bold", zorder=5)
        if i < 3:
            ax.add_patch(FancyArrowPatch((x + BW + 0.03, y + 0.41),
                         (BX[i + 1] - 0.03, y + 0.41), arrowstyle="-|>",
                         mutation_scale=12, color=(H.RED if bad else H.GRAY),
                         lw=1.6, zorder=4))
    rbox(10.45, y, 1.35, 0.82, fc=rface, ec=rcolor, lw=1.7, r=0.09)
    ax.text(11.125, y + 0.41, result, ha="center", va="center", fontsize=8.6,
            color=rcolor, fontweight="bold", zorder=5)
    if flag:
        ax.text(0.2, y - 0.22, flag, ha="left", va="center", fontsize=7.6,
                color=rcolor, fontweight="bold", zorder=5)


chain(8.55, ["2.3", "支持", "2.3", "2.3"], H.GREEN, "4K HDR\n√ 正常",
      H.GREEN, "#eafaf1", flag="√ 全链路 HDCP 2.2 / 2.3 —— 验证通过，正常解密播放")
chain(7.15, ["2.3", "支持", "1.4", "2.3"], H.RED, "黑屏 /\n降级 ×",
      H.RED, "#fdecea", bad_idx=2,
      flag="× 中间那台老功放只有 HDCP 1.4 —— 链条断开，内容拒绝解密")

# ---------------- ② 后果 ----------------
sec(6.45, "② 版本不匹配的典型后果（用户看到的“怪毛病”）")
cons = [
    ("黑屏 / 无信号", "验证不通过，画面全黑"),
    ("只有声音没画面", "音频照常，视频被拦下"),
    ("分辨率降到 480p", "受保护内容只能低清播"),
    ("HDR 降成 SDR", "高位深 / 宽色域全部失效"),
]
cw2 = (11.6 - 3 * 0.2) / 4
for i, (t, d) in enumerate(cons):
    x = 0.2 + i * (cw2 + 0.2)
    rbox(x, 5.05, cw2, 1.18, fc="#fdecea", ec=H.RED, lw=1.6, r=0.09)
    ax.text(x + 0.14, 5.93, "× " + t, ha="left", va="center", fontsize=8.0,
            color=H.RED, fontweight="bold", zorder=5)
    ax.text(x + 0.14, 5.48, d, ha="left", va="center", fontsize=7.0,
            color=H.DARK, zorder=5)

# ---------------- ③ 版本门槛 ----------------
sec(4.66, "③ 内容分辨率门槛：HDCP 1.4 放不了 4K 受保护内容")
XS = {"480p": 1.4, "1080p": 3.6, "4K": 6.6, "8K": 9.3}

# 受保护内容区（4K 及以上）底纹
ax.add_patch(Rectangle((XS["4K"], 2.78), 9.6 - XS["4K"], 1.10,
             fc="#fdecea", ec="none", zorder=1))

# 条形
bars = [("HDCP 2.2 / 2.3", 3.34, 9.6, H.GREEN, "#eafaf1"),
        ("HDCP 1.4（老设备）", 2.86, XS["1080p"], H.RED, "#fdecea")]
for nm, y, xend, c, fc in bars:
    ax.add_patch(FancyBboxPatch((0.25, y), xend - 0.25, 0.42,
                 boxstyle="round,pad=0,rounding_size=0.06",
                 fc=fc, ec=c, lw=1.7, zorder=3))
    ax.text(0.40, y + 0.21, nm, ha="left", va="center", fontsize=7.6,
            color=c, fontweight="bold", zorder=5)

# 4K 门槛线
ax.plot([XS["4K"], XS["4K"]], [2.78, 3.88], color=H.RED, lw=1.8,
        ls=(0, (5, 3)), zorder=5)
ax.text(XS["4K"] - 0.16, 3.96, "4K 受保护内容门槛", ha="left", va="bottom",
        fontsize=7.3, color=H.RED, fontweight="bold", zorder=5)

ax.text(XS["1080p"] + 0.16, 3.07, "最远只能到 1080p ×", ha="left", va="center",
        fontsize=7.2, color=H.RED, fontweight="bold", zorder=5)
ax.text(XS["4K"] + 0.25, 3.55, "√ 覆盖 4K / 8K", ha="left",
        va="center", fontsize=7.3, color=H.GREEN, fontweight="bold", zorder=5)

# 底部刻度轴
ax.plot([0.25, 9.9], [2.74, 2.74], color=H.GRAY, lw=1.2, zorder=3)
for lab, xp in XS.items():
    ax.plot([xp, xp], [2.74, 2.64], color=H.GRAY, lw=1.2, zorder=3)
    ax.text(xp, 2.46, lab, ha="center", va="center", fontsize=7.0,
            color=H.GRAY, fontweight="bold", zorder=3)

# ---------------- 底部排查建议 ----------------
rbox(0.2, 0.30, 11.6, 1.90, fc="#f3f6fa", ec=H.LGRAY, lw=1.4, r=0.10)
ax.text(0.46, 1.86, "排查口诀", ha="left", va="center", fontsize=8.6,
        color=H.NAVY, fontweight="bold", zorder=5)
tips = [
    "放 4K HDR 片黑屏、只有声音没画面、分辨率莫名变低 → 第一反应查 HDCP 版本。",
    "重点怀疑中间设备：功放、HDMI 切换器、廉价转接头（它们常是 HDCP 1.4）。",
    "把中间设备去掉、显卡直连显示器试一次，往往立刻见效；仍不行再换线材。",
]
for i, t in enumerate(tips):
    ax.text(0.46, 1.44 - i * 0.42, "· " + t, ha="left", va="center",
            fontsize=7.6, color=H.DARK)

H.save(fig, 15, "f3_hdcp")
