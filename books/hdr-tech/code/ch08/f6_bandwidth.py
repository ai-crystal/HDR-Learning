# -*- coding: utf-8 -*-
"""图 8-6 帧缓冲格式与一条示例后处理链的带宽代价。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("hdr-tech")
import numpy as np

plt = H.plt

W, H_, FPS = 3840, 2160, 60
px = W * H_
B32 = px * 4 / 1e6          # 32 位格式，一次读或写
B64 = px * 8 / 1e6          # FP16，一次读或写

fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.3),
                         gridspec_kw={"width_ratios": [1.0, 1.15]})
ax1, ax2 = axes

# ---------- 左：单缓冲与 4 倍 MSAA ----------
names = ["RGBA8\nR10G10B10A2", "R11G11B10F", "RGBA16F", "RGBA16F\n4 倍 MSAA"]
bytes_px = [4, 4, 8, 32]
vals = [px * b / 1e6 for b in bytes_px]
cols = [H.GRAY, H.TEAL, H.ORANGE, H.RED]
bars = ax1.bar(range(4), vals, color=cols, width=0.62)
for i, v in enumerate(vals):
    ax1.text(i, v + 6, f"{v:.0f}", ha="center", va="bottom", fontsize=8.6,
             color=cols[i])
ax1.set_xticks(range(4))
ax1.set_xticklabels(names, fontsize=7.8)
ax1.set_ylim(0, 320)
ax1.set_axisbelow(True)
ax1.set_ylabel("单帧缓冲占用（MB，4K）")
ax1.set_title("(a) 同一个 4K 画面占多大", fontsize=9.8, pad=8)
ax1.text(0.02, 0.94, "4K 一帧 8.29 M 像素", transform=ax1.transAxes,
         fontsize=7.6, color=H.GRAY, va="top")

# ---------- 右：一条示例链路的缓冲流量 ----------
items = ["场景缓冲\n写加读", "四个后处理\n各读加写", "色调映射\n读加写", "交换链\n写"]
tr = [2, 8, 2, 1]
v32 = [t * B32 for t in tr]
v64 = [t * B64 for t in tr]

x = np.arange(len(items))
w = 0.36
ax2.bar(x - w / 2, v32, w, color=H.BLUE, label="全程 32 位整数")
ax2.bar(x + w / 2, v64, w, color=H.ORANGE, label="全程 FP16")
for i in range(len(items)):
    ax2.text(x[i] - w / 2, v32[i] + 8, f"{v32[i]:.0f}", ha="center",
             va="bottom", fontsize=8, color=H.BLUE)
    ax2.text(x[i] + w / 2, v64[i] + 8, f"{v64[i]:.0f}", ha="center",
             va="bottom", fontsize=8, color=H.ORANGE)
ax2.set_xticks(x)
ax2.set_xticklabels(items, fontsize=7.8)
ax2.set_ylim(0, 660)
ax2.set_axisbelow(True)
ax2.set_ylabel("每帧流量（MB）")
ax2.set_title("(b) 一条示例管线的缓冲流量", fontsize=9.8, pad=8)
ax2.legend(loc="upper right", fontsize=8)

tot32 = sum(v32)
tot64 = sum(v64)
ax2.text(0.98, 0.60, f"合计 {tot32:.0f} 与 {tot64:.0f} MB\n"
                     f"折合 {tot32*FPS/1e3:.1f} 与 {tot64*FPS/1e3:.1f} GB/s",
         transform=ax2.transAxes, ha="right", va="top", fontsize=8,
         color="#2c3e50", linespacing=1.6)

fig.subplots_adjust(wspace=0.36)
H.save(fig, 8, "f6_bandwidth")
