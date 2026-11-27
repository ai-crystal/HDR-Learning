# -*- coding: utf-8 -*-
"""第 11 章 图 4：trim pass 的分段与逐镜头参数。

最上一行是镜头切分（示意），下面三行是三个参数轨：高光滚降强度、黑位调整、饱和度。
每个镜头一组取值，虚线的自动初稿与实线的人工结果常在同一镜头上分开。
标注处是一个典型镜头，自动给出的滚降太强，云层被压平，人工往回退。
参数取值为示例，用来说明工作方式，不代表任何具体片子的设置。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
from matplotlib.patches import Rectangle

H.set_book("hdr-tech")
plt = H.plt

EDGES = np.array([0, 9, 21, 33, 42, 58, 67, 79, 95, 108, 120], dtype=float)
N = len(EDGES) - 1
MID = (EDGES[:-1] + EDGES[1:]) / 2
AUTO_ROLL = np.array([0.55, 0.62, 0.90, 0.48, 0.70, 0.86, 0.52, 0.66, 0.58, 0.74])
FINAL_ROLL = np.array([0.55, 0.60, 0.55, 0.46, 0.68, 0.58, 0.52, 0.64, 0.58, 0.70])
AUTO_BLACK = np.array([0.0, 0.5, 1.5, 0.0, -1.0, 1.0, 0.0, 0.5, 0.0, 1.0])
FINAL_BLACK = np.array([0.0, 0.5, 0.0, 0.0, -1.0, 0.0, 0.0, 0.5, 0.0, 1.0])
AUTO_SAT = np.array([0.0, -3.0, -8.0, 0.0, -4.0, -10.0, 0.0, -2.0, 0.0, -5.0])
FINAL_SAT = np.array([0.0, -3.0, -4.0, 0.0, -4.0, -5.0, 0.0, -2.0, 0.0, -5.0])

fig, axes = plt.subplots(4, 1, figsize=(7.6, 4.9), sharex=True,
                         gridspec_kw=dict(height_ratios=[0.42, 1.0, 1.0, 1.0],
                                          hspace=0.10))
fig.subplots_adjust(left=0.135, right=0.975, bottom=0.115, top=0.975)

# ---------------- 镜头条 ----------------
ax0 = axes[0]
for i in range(N):
    c = "#dbe4ee" if i % 2 == 0 else "#eef3f8"
    if i == 2:
        c = "#f6d7cf"
    ax0.add_patch(Rectangle((EDGES[i], 0), EDGES[i + 1] - EDGES[i], 1,
                            facecolor=c, edgecolor="white", lw=1.0))
    ax0.text(MID[i], 0.5, f"镜 {i + 1}", fontsize=7.4, color="#33455a",
             ha="center", va="center")
ax0.set_ylim(0, 1)
ax0.set_yticks([])
ax0.grid(False)
for sp in ("top", "right", "left"):
    ax0.spines[sp].set_visible(False)


# ---------------- 参数轨 ----------------
TRACKS = [
    ((axes[1], AUTO_ROLL, FINAL_ROLL, 1.0, "高光滚降强度", (-0.08, 1.14)), H.NAVY),
    ((axes[2], AUTO_BLACK, FINAL_BLACK, 4.0, "黑位调整（IRE）", (-2.5, 5.0)), H.TEAL),
    ((axes[3], AUTO_SAT, FINAL_SAT, 5.0, "饱和度（%）", (-13, 4.5)), H.ORANGE),
]

for (ax, auto, final, _, lab, ylim), c in TRACKS:
    ax.step(EDGES, np.append(auto, auto[-1]), where="post", color="#9aa7b4",
            lw=1.5, ls=(0, (4, 2)), zorder=3)
    ax.step(EDGES, np.append(final, final[-1]), where="post", color=c,
            lw=2.2, zorder=4)
    ax.plot(MID, final, "o", ms=5.0, color=c, mec="white", mew=1.0, zorder=5)
    for e in EDGES[1:-1]:
        ax.axvline(e, color="#c9d3de", lw=0.8, ls=":", zorder=1)
    ax.axhline(0, color="#b7c1cc", lw=0.8, zorder=2)
    ax.set_ylim(*ylim)
    ax.set_ylabel(lab, fontsize=8.6, labelpad=4)
    ax.tick_params(labelsize=8)
    ax.grid(axis="x", visible=False)

axes[1].legend(handles=[
    plt.Line2D([], [], color="#9aa7b4", lw=1.5, ls=(0, (4, 2)), label="自动初稿"),
    plt.Line2D([], [], color=H.NAVY, lw=2.2, label="人工确认"),
], loc="upper right", fontsize=7.4, ncol=2, borderpad=0.4,
    columnspacing=1.0, handlelength=2.2)

axes[1].text(6.5, 0.13, "镜 3 的云层在自动滚降下被压平，人工把强度退到 0.58",
             fontsize=7.2, color=H.RED, ha="left", va="center")

axes[3].set_xlabel("片长（秒，示例）", fontsize=9)
axes[3].set_xlim(0, 120)
axes[3].set_xticks([0, 20, 40, 60, 80, 100, 120])

H.save(fig, 11, "f4_trim_pass")
