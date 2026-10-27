# -*- coding: utf-8 -*-
"""第 01 章 图 6：CIE 1931 RGB 颜色匹配函数 r̄(λ)、ḡ(λ)、b̄(λ)。

由 CIE 1931 2° 标准观察者 XYZ 数据反算（RGB = M⁻¹·XYZ），
重点展示红色曲线在 ~490–560 nm 出现的负值——这正是"某些饱和色
用实际三原色配不出来、要给红原色加负强度"的数学表现。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
sys.path.insert(0, "E:/Study/HDR技术/book/code/ch04")
import numpy as np
import hdrfig as H
import cie1931 as C

# CIE RGB（700 / 546.1 / 435.8 nm，E 白）-> XYZ 矩阵（经典未归一化形式）
M = np.array([[2.7689, 1.7517, 1.1302],
              [1.0000, 4.5907, 0.0601],
              [0.0000, 0.0565, 5.5943]])
Minv = np.linalg.inv(M)
lam = C.LAM
r, g, b = Minv @ np.stack([C.XBAR, C.YBAR, C.ZBAR])

fig, ax = H.plt.subplots(figsize=(7.2, 4.2))
ax.axhline(0, color="#333333", lw=0.9)
ax.plot(lam, r, color=H.RED, lw=2.5, label=r"$\bar r(\lambda)$　红原色 (R)")
ax.plot(lam, g, color=H.GREEN, lw=2.5, label=r"$\bar g(\lambda)$　绿原色 (G)")
ax.plot(lam, b, color=H.BLUE, lw=2.5, label=r"$\bar b(\lambda)$　蓝原色 (B)")

# 负值区
neg = r < -1e-4
ax.fill_between(lam, r, 0, where=neg, color=H.RED, alpha=0.16, lw=0)
imin = int(np.argmin(np.where(neg, r, 0)))
ax.annotate("负值区（约 490–560 nm）：实际三原色配不出这种颜色，\n"
            "只能把红原色加到待测光一侧抵消 → 红色强度记为负",
            xy=(lam[imin], r[imin]), xytext=(382, -0.085),
            fontsize=8.0, color=H.RED, va="top",
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.1),
            bbox=dict(boxstyle="round,pad=0.22", fc="white", ec=H.RED, lw=0.7, alpha=0.95))

# 峰值标注
for arr, col in [(r, H.RED), (g, H.GREEN), (b, H.BLUE)]:
    i = int(np.argmax(arr))
    ax.plot(lam[i], arr[i], "o", color=col, ms=5, zorder=6,
            markeredgecolor="white", markeredgewidth=0.8)
_lines = ["峰值："]
for arr, txt in [(r, r"$\bar r$"), (g, r"$\bar g$"), (b, r"$\bar b$")]:
    i = int(np.argmax(arr))
    _lines.append(f"{txt} {arr[i]:.2f} @ {int(lam[i])} nm")
ax.text(632, -0.018, "\n".join(_lines), fontsize=7.8, va="top", ha="left",
        linespacing=1.5,
        bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="#c3ccd6", lw=0.8))

# 示例：600 nm
i6 = int(np.argmin(np.abs(lam - 600)))
for arr, col in [(r, H.RED), (g, H.GREEN), (b, H.BLUE)]:
    ax.plot(600, arr[i6], "o", color=col, ms=4, zorder=6)
ax.axvline(600, color="#999999", ls=":", lw=0.9)
ax.text(600, -0.028, "600 nm", ha="center", va="top", fontsize=7.6, color="#666")

ax.set_xlim(380, 780)
ax.set_ylim(-0.16, 0.40)
ax.set_xlabel("波长 λ（nm）")
ax.set_ylabel("颜色匹配函数值")
ax.set_title("CIE 1931 RGB 颜色匹配函数：红色有一段负值", fontsize=12.5, fontweight="bold")
ax.legend(loc="upper left", fontsize=8.6)
ax.grid(True, color="#e6ebf0", lw=0.7)

# 底部可见光谱色带
strip = np.linspace(0, 1, 400)[None, :].repeat(14, axis=0)
axin = fig.add_axes([0.125, 0.085, 0.775, 0.045])
rgb = C.wavelength_to_srgb01(np.linspace(380, 780, 400), normalized=True)
axin.imshow(rgb[None, :, :], aspect="auto", extent=[380, 780, 0, 1])
axin.set_yticks([]); axin.set_xticks([]); axin.grid(False)
for sp in axin.spines.values():
    sp.set_edgecolor("#c3ccd6")
ax.text(0.5, -0.55, "可见光谱（紫 → 红）", transform=axin.transAxes,
        ha="center", va="top", fontsize=7.4, color=H.GRAY)
fig.subplots_adjust(bottom=0.24)

H.save(fig, 1, "f6_rgb_cmf")
