# -*- coding: utf-8 -*-
"""第 06 章 图 1：合成 HDR 测试图案（用 numpy 直接生成像素，不是画框）。

每个子图都是按 PQ 码值生成的像素阵列。预览时把码值映射到 8 位灰度，
暗部两块（c 与 f）单独拉伸了显示范围，否则近黑台阶在预览里并成一片黑，
标题里注明"已拉伸"，真实图案仍按 ST 2084 的绝对亮度输出。
  (a) 灰阶斜坡 0–1023     看量化台阶与色带
  (b) 灰阶阶梯 11 级       测灰阶跟踪
  (c) 近黑阶梯 0–64 步进 8  查黑位裁切
  (d) 窗口 10%/2%/1%       测峰值与 ABL
  (e) 4×4 棋盘             测 ANSI 对比度
  (f) PLUGE                调亮度与黑位
  (g) 彩条                 查饱和度与色相
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

C_BLACK = float(H.pq_oetf(0.005)) * 1023.0


def ramp(n=900, h=90):
    return np.tile(np.linspace(0, 1023, n), (h, 1))


def steps(levels, n=11, h=140):
    arr = np.zeros((h, n * 40))
    for i, c in enumerate(levels):
        arr[:, i * 40:(i + 1) * 40 - 2] = c
    return arr


def window_panel(areas=(10, 2, 1), w=460, h=180):
    arr = np.full((h, w), C_BLACK)
    for i, a in enumerate(areas):
        side = int(h * 0.70 * np.sqrt(a / max(areas)))
        x0 = int((i + 0.5) * w / len(areas) - side / 2)
        y0 = (h - side) // 2
        arr[y0:y0 + side, x0:x0 + side] = 1023
    return arr


def checker(n=4, size=45):
    arr = np.zeros((n * size, n * size))
    for r in range(n):
        for c in range(n):
            if (r + c) % 2 == 0:
                arr[r * size:(r + 1) * size, c * size:(c + 1) * size] = 1023
    return arr


def pluge(w=560, h=110):
    arr = np.full((h, w), C_BLACK)
    arr[:, int(w * 0.16):int(w * 0.30)] = float(H.pq_oetf(0.0049)) * 1023.0
    arr[:, int(w * 0.62):int(w * 0.76)] = float(H.pq_oetf(0.0051)) * 1023.0
    return arr


def color_bars(w=560, h=110):
    cols = [(1023, 1023, 1023), (509, 509, 509), (1023, 0, 0), (0, 1023, 0),
            (0, 0, 1023), (0, 1023, 1023), (1023, 0, 1023), (1023, 1023, 0)]
    arr = np.zeros((h, w, 3))
    bw = w // len(cols)
    for i, c in enumerate(cols):
        arr[:, i * bw:(i + 1) * bw - 3] = np.array(c) / 1023.0
    return arr


fig = plt.figure(figsize=(7.4, 5.4))
gs = fig.add_gridspec(3, 3, height_ratios=[0.40, 1.0, 0.60],
                      hspace=0.46, wspace=0.16,
                      left=0.02, right=0.98, top=0.93, bottom=0.03)

panels = [
    (gs[0, :], ramp(), "(a) 灰阶斜坡 0–1023", (0, 1023)),
    (gs[1, 0], steps(np.linspace(0, 1023, 11)), "(b) 灰阶阶梯 11 级", (0, 1023)),
    (gs[1, 1], steps(range(0, 65, 8), n=9, h=140), "(c) 近黑阶梯 0–64（放大显示）", (0, 64)),
    (gs[1, 2], window_panel(), "(d) 窗口 10% / 2% / 1%", (0, 1023)),
    (gs[2, 0], checker(), "(e) 4×4 棋盘", (0, 1023)),
    (gs[2, 1], pluge(), "(f) PLUGE 黑 ±2%（已拉伸）", (C_BLACK - 1.2, C_BLACK + 1.2)),
    (gs[2, 2], color_bars(), "(g) 彩条", None),
]

for spec, arr, title, vlim in panels:
    ax = fig.add_subplot(spec)
    asp = "equal" if title.startswith("(d)") else "auto"
    if arr.ndim == 3:
        ax.imshow(arr, interpolation="nearest", aspect=asp)
    else:
        ax.imshow(arr, cmap="gray", vmin=vlim[0], vmax=vlim[1],
                  interpolation="nearest", aspect=asp)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#7d8b9a")
        s.set_linewidth(0.7)
    ax.set_title(title, fontsize=8.4, pad=3)

H.save(fig, 6, "f1_test_pattern")
