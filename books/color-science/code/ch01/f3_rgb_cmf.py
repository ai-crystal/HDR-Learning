# -*- coding: utf-8 -*-
"""第 01 章 图 3：两组原色下的色匹配函数与负值区。

(a) Wright 实验的原色（R 650 nm、G 530 nm、B 460 nm）下的色匹配函数。三组原色
    各自按组内最大值归一，R 通道在 460–530 nm 出现负值。
(b) 三种原色组的 R 通道对比：Wright 650/530/460、Guild 620/540/460、
    CIE 最终采用的 700/546.1/435.8。红原色越靠长波端，负值区越宽。

计算方法：任一组原色 (λ1,λ2,λ3) 的色匹配函数由 2° 观察者数据线性换算得到，
    c(λ) = M⁻¹·(x̄,ȳ,z̄)(λ)，M 的列是三条原色各自的 XYZ；再除以等能白的响应，
    使 ∫c dλ = (1,1,1)。这是 Grassmann 加色定律的直接推论，不是实测数据。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C
from scipy.interpolate import PchipInterpolator

plt = H.plt

FX = PchipInterpolator(C.LAM, C.XBAR)
FY = PchipInterpolator(C.LAM, C.YBAR)
FZ = PchipInterpolator(C.LAM, C.ZBAR)
lam = np.linspace(380.0, 780.0, 801)
XYZ = np.stack([FX(lam), FY(lam), FZ(lam)])
INT = np.trapezoid(XYZ, lam, axis=1)


def cmf(primaries):
    """返回给定原色波长下的色匹配函数（3×N），等能白归一。"""
    Mp = np.stack([[FX(p), FY(p), FZ(p)] for p in primaries], axis=1)
    out = np.linalg.solve(Mp, XYZ)
    n = np.linalg.solve(Mp, INT)
    out = out / n[:, None]
    return out / np.abs(out).max()


SETS = [
    ("Wright 650/530/460", (650.0, 530.0, 460.0)),
    ("Guild 620/540/460", (620.0, 540.0, 460.0)),
    ("CIE RGB 700/546.1/435.8", (700.0, 546.1, 435.8)),
]
CM = {name: cmf(p) for name, p in SETS}

fig = plt.figure(figsize=(7.2, 4.3))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.0], wspace=0.26)

# ==================== (a) Wright 原色下的三条曲线 ====================
ax = fig.add_subplot(gs[0])
c = CM["Wright 650/530/460"]
cols = (H.RED, H.GREEN, H.BLUE)
labs = (r"$\bar{r}(\lambda)$", r"$\bar{g}(\lambda)$", r"$\bar{b}(\lambda)$")
ax.axhline(0, color="#4a5666", lw=0.9)
for k in range(3):
    ax.plot(lam, c[k], color=cols[k], lw=2.1, label=labs[k])
    if c[k].min() < -0.01:
        ax.fill_between(lam, 0, np.minimum(c[k], -0.004), color=cols[k],
                        alpha=0.30, lw=0)
mask = c[0] < 0
ax.annotate("负值区\n约 461–530 nm", xy=(497, -0.045), xytext=(516, -0.20),
            fontsize=7.4, color=H.RED, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9,
                            connectionstyle="arc3,rad=0.18"))
ax.text(556, 0.90, "负值表示要把该原色光\n加到待测一侧才能配平", fontsize=7.0,
        color="#4a5666", ha="center", va="center")

ax.set_xlim(380, 780)
ax.set_ylim(-0.30, 1.14)
ax.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
ax.set_xlabel("波长 λ（nm）")
ax.set_ylabel("色匹配函数（组内最大值归一）")
ax.set_title("(a) Wright 原色 650 / 530 / 460 nm", fontsize=9.5, pad=6)
ax.legend(loc="upper right", fontsize=8, frameon=True, handlelength=1.4,
          labelspacing=0.2, bbox_to_anchor=(1.0, 1.0))

# ==================== (b) 三种原色组的 R 通道 ====================
ax2 = fig.add_subplot(gs[1])
styles = [(H.RED, "-"), (H.ORANGE, (0, (5, 2))), (H.PURPLE, (0, (1.4, 1.4)))]
for (name, _), (col, ls) in zip(SETS, styles):
    ax2.plot(lam, CM[name][0], color=col, lw=2.0, ls=ls, label=name)
ax2.axhline(0, color="#4a5666", lw=0.9)
ax2.fill_between(lam, 0, np.minimum(CM["CIE RGB 700/546.1/435.8"][0], 0),
                 color=H.PURPLE, alpha=0.18, lw=0)

ax2.annotate("700 nm 原色的负值区\n宽达 436–546 nm", xy=(505, -0.155),
             xytext=(614, -0.240), fontsize=7.2, color=H.PURPLE, ha="left",
             va="center",
             arrowprops=dict(arrowstyle="->", color=H.PURPLE, lw=0.9,
                             connectionstyle="arc3,rad=-0.20"))
ax2.set_xlim(380, 780)
ax2.set_ylim(-0.30, 1.14)
ax2.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
ax2.set_xlabel("波长 λ（nm）")
ax2.set_ylabel(r"$\bar{r}(\lambda)$（组内最大值归一）")
ax2.set_title("(b) 三种原色组的 R 通道", fontsize=9.5, pad=6)
ax2.legend(loc="upper left", fontsize=7.0, frameon=True, handlelength=1.9,
           labelspacing=0.25)

H.save(fig, 1, "f3_rgb_cmf")

for name, _ in SETS:
    cc = CM[name]
    for k, tag in enumerate("RGB"):
        neg = lam[cc[k] < 0]
        if len(neg):
            print(f"{name} {tag}: neg {neg.min():.1f}-{neg.max():.1f} "
                  f"min={cc[k].min():.4f}")
print("Wright r peak", lam[CM['Wright 650/530/460'][0].argmax()])
