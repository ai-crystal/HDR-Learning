# -*- coding: utf-8 -*-
"""图 7-2：时域分级参考结构（GOP 内含四层的分层 B 帧）。

横轴是显示顺序 POC，纵轴是时域层。编码器按层分配量化参数，
层号越大越靠上（离参考帧越远），QP 偏移越大。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt

NODES = [(0, 0, "I"), (8, 0, "P"), (4, 1, "B"), (2, 2, "B"), (6, 2, "B"),
         (1, 3, "B"), (3, 3, "B"), (5, 3, "B"), (7, 3, "B")]
COL = {0: H.NAVY, 1: H.BLUE, 2: H.TEAL, 3: H.ORANGE}
QP = {0: "+0", 1: "+1", 2: "+2", 3: "+3"}

fig, ax = plt.subplots(figsize=(7.6, 3.9))
fig.subplots_adjust(left=0.085, right=0.80, bottom=0.16, top=0.94)

# 参考连线：每个 B 帧取左右两侧最近的、层号更低的已解码帧作为两个参考
for x, lay, kind in NODES:
    if lay == 0:
        continue
    lefts = [n for n in NODES if n[1] < lay and n[0] < x]
    rights = [n for n in NODES if n[1] < lay and n[0] > x]
    for cand in (max(lefts, key=lambda n: n[0]) if lefts else None,
                 min(rights, key=lambda n: n[0]) if rights else None):
        if cand is None:
            continue
        px, pl = cand[0], cand[1]
        ax.plot([x, px], [lay, lay], color="#b8c3cf", lw=1.5, zorder=1)
        ax.plot([px, px], [lay, pl], color="#b8c3cf", lw=1.5,
                ls=(0, (4, 2)) if pl < lay - 1 else "-", zorder=1)

for lay in range(4):
    xs = [n[0] for n in NODES if n[1] == lay]
    ys = [n[1] for n in NODES if n[1] == lay]
    ax.scatter(xs, ys, s=150, color=COL[lay], edgecolor="white", linewidth=1.4,
               zorder=3)

for x, lay, kind in NODES:
    ax.text(x, lay, kind, ha="center", va="center", color="white",
            fontsize=7.6, zorder=4)

ax.set_xlim(-0.7, 8.7)
ax.set_ylim(-0.75, 3.55)
ax.set_yticks([0, 1, 2, 3])
ax.set_yticklabels(["T0", "T1", "T2", "T3"])
ax.set_xticks(range(9))
ax.set_xticklabels([str(i) for i in range(9)])
ax.set_xlabel("显示顺序（POC）")
ax.set_ylabel("时域层")
ax.grid(axis="y", visible=False)
ax.tick_params(axis="y", length=0)

for lay in range(4):
    ax.text(9.05, lay, "QP " + QP[lay], ha="left", va="center",
            fontsize=8.4, color=COL[lay])
ax.text(8.95, 3.42, "典型偏移", ha="left", va="center", fontsize=7.6,
        color=H.GRAY)

ax.text(4.0, -0.62, "解码顺序：0 → 8 → 4 → 2 → 6 → 1 → 3 → 5 → 7",
        ha="center", va="center", fontsize=8.2, color=H.DARK)

H.save(fig, 7, "f2_temporal_pyramid")
