# -*- coding: utf-8 -*-
"""图 19-3　ICC 配置文件 vs 3D LUT：两种“修正处方”的形状差异。

左图：ICC 配置文件主要是一组逐通道 TRC 曲线（外加一个 3×3 矩阵），
      用来近似描述并修正屏幕特性——通用、轻量，适合日常使用。
右图：3D LUT 是一张三通道联合的三维查找表（如 17³ / 33³ 网格点），
      能表达通道之间的交叉影响，精度更高，适合专业调色与影视监看。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(7.2, 4.4))

# ================= 左：ICC（逐通道 TRC + 矩阵） =================
ax0 = fig.add_subplot(1, 2, 1)
code = np.linspace(0, 1, 256)
ax0.plot(code, code ** 2.20, "--", color="#4a5666", lw=1.3, label="目标 γ2.2")
ax0.plot(code, code ** 2.14, "-", color=H.RED, lw=2.0, label="R 通道 TRC")
ax0.plot(code, code ** 2.20, "-", color=H.GREEN, lw=2.0, label="G 通道 TRC")
ax0.plot(code, code ** 2.27, "-", color=H.BLUE, lw=2.0, label="B 通道 TRC")
ax0.set_xlim(0, 1); ax0.set_ylim(0, 1)
ax0.set_xlabel("输入码值"); ax0.set_ylabel("输出")
ax0.set_title("ICC：逐通道曲线 + 矩阵（1D 近似）", pad=8, fontsize=10.8)
ax0.legend(loc="lower right", fontsize=8)
ax0.text(0.03, 0.97,
         "描述屏幕特性：白点、色域、\n逐通道 TRC 曲线（+ 3x3 矩阵）\n"
         "轻量、通用，适合日常与消费级工作流",
         ha="left", va="top", fontsize=7.8, color=H.DARK, linespacing=1.5,
         bbox=dict(boxstyle="round,pad=0.35", fc="#eef3f9", ec=H.NAVY,
                   lw=0.9))

# ================= 右：3D LUT（三通道联合网格） =================
ax1 = fig.add_subplot(1, 2, 2, projection="3d")
n = 5
g = np.linspace(0, 1, n)
RG, GG, BG = np.meshgrid(g, g, g)
pts = np.column_stack([RG.ravel(), GG.ravel(), BG.ravel()])
cols = pts.copy()
ax1.scatter(pts[:, 0], pts[:, 1], pts[:, 2], c=cols, s=26, depthshade=False,
            edgecolors="#555f6b", linewidths=0.4)

# 立方体棱边
edges = [((0, 0, 0), (1, 0, 0)), ((0, 0, 0), (0, 1, 0)), ((0, 0, 0), (0, 0, 1)),
         ((1, 1, 1), (1, 1, 0)), ((1, 1, 1), (1, 0, 1)), ((1, 1, 1), (0, 1, 1)),
         ((1, 0, 0), (1, 1, 0)), ((1, 0, 0), (1, 0, 1)),
         ((0, 1, 0), (1, 1, 0)), ((0, 1, 0), (0, 1, 1)),
         ((0, 0, 1), (1, 0, 1)), ((0, 0, 1), (0, 1, 1))]
for a, b in edges:
    ax1.plot(*zip(a, b), color="#9aa6b2", lw=1.0, zorder=1)

ax1.set_xlabel("R", fontsize=9); ax1.set_ylabel("G", fontsize=9)
ax1.set_zlabel("B", fontsize=9)
ax1.set_xticks([0, 1]); ax1.set_yticks([0, 1]); ax1.set_zticks([0, 1])
ax1.tick_params(labelsize=7)
ax1.set_title("3D LUT：三通道联合网格\n（如 17×17×17 = 4913 点 / 33×33×33）",
              pad=2, fontsize=10.8)
ax1.view_init(elev=22, azim=32)
ax1.grid(False)

fig.suptitle("ICC 是“通用矫正处方”，3D LUT 是“更精细的定制处方”", fontsize=12.5,
             fontweight="bold", y=1.02)
fig.text(0.5, -0.10,
         "ICC：每通道一条 1D 曲线 + 矩阵，用近似方式描述屏幕，几乎对所有软件透明；"
         "3D LUT：把 (R,G,B) 映射到 (R',G',B') 的三维查表，能处理通道串扰，"
         "多用于专业调色 / 影视监看。",
         ha="center", fontsize=7.9, color=H.GRAY, wrap=True)
H.save(fig, 19, "f3_icc_lut")
