# -*- coding: utf-8 -*-
"""第 08 章 图 5：显示 profile 的两个核心读法（示意，数据由模型算出）。

(a) 灰阶跟踪：把中性灰从 5% 扫到 100%，逐级算与 D65 中性色的 $\\Delta E_{00}$，
    校准前是逐通道伽马不一致加黑位泄漏，校准后只剩 8 bit 输出的量化残差
(b) 色域覆盖：按标称基色在 $u'v'$ 上的凸多边形面积算出的覆盖率
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cms_util as C

plt = H.plt
plt.rcParams["mathtext.fontset"] = "dejavusans"

fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.2),
                         gridspec_kw={"width_ratios": [1.12, 1.0], "wspace": 0.30})

# ---------------- (a) 灰阶跟踪 ----------------
ax = axes[0]
LW = np.array([0.2126, 0.7152, 0.0722])
G = np.array([2.24, 2.19, 2.13])
K = 0.0055
FLARE = 0.0015
WHITE = C.WHITE_D65


def chan(v, g, k=K, flare=FLARE):
    v = np.asarray(v, dtype=float)
    num = np.maximum(v + k, 0) ** g - k ** g
    den = (1 + k) ** g - k ** g
    return np.clip(num / den, 0, 1) + flare


levels = np.linspace(0.05, 1.0, 60)
chan_before = np.stack([chan(levels, G[0]),
                        chan(levels, G[1]),
                        chan(levels, G[2])], axis=1)
xyz_before = chan_before @ C.M_SRGB.T

Y_want = C.srgb_eotf(levels)
xyz_want = np.outer(Y_want, WHITE)

lab_b = C.xyz_to_lab(xyz_before, WHITE)
lab_w = C.xyz_to_lab(xyz_want, WHITE)
de_before = C.delta_e00(lab_b, lab_w)

# 校准后：每通道 8 bit 一维 LUT，误差只剩输出量化
code_q = np.round(levels * 255) / 255.0
lin_after = C.srgb_eotf(code_q)
xyz_after = np.outer(lin_after, WHITE)
de_after = np.maximum(C.delta_e00(C.xyz_to_lab(xyz_after, WHITE), lab_w), 0.02)

ax.semilogy(levels * 100, np.maximum(de_before, 0.02), color=H.RED, lw=1.8,
            label="校准前")
ax.semilogy(levels * 100, de_after, color=H.TEAL, lw=1.8, ls=(0, (5, 2)),
            label="校准后（8 bit 残差）")
ax.axhline(1.0, color=H.GRAY, lw=0.9, ls=(0, (3, 3)))
ax.text(46, 0.58, "常见验收线 $\\Delta E_{00}=1$", fontsize=6.0, color=H.GRAY,
        va="bottom")
ax.set_xlim(5, 100)
ax.set_ylim(0.02, 6)
ax.set_yticks([0.02, 0.05, 0.1, 0.5, 1, 2, 4])
ax.set_yticklabels(["0.02", "0.05", "0.1", "0.5", "1", "2", "4"])
ax.minorticks_off()
ax.set_xlabel("输入码值  %", fontsize=8.5)
ax.set_ylabel("与 D65 中性色的 $\\Delta E_{00}$", fontsize=8.0)
ax.set_title("(a) 灰阶跟踪", fontsize=8.4, pad=5)
ax.legend(loc="upper right", fontsize=6.4, handlelength=2.0,
          labelspacing=0.25, borderaxespad=0.3)

# ---------------- (b) 色域覆盖 ----------------
ax = axes[1]
refs = {"sRGB": [(0.640, 0.330), (0.300, 0.600), (0.150, 0.060)],
        "P3": [(0.680, 0.320), (0.265, 0.690), (0.150, 0.060)],
        "BT.2020": [(0.708, 0.292), (0.170, 0.797), (0.131, 0.046)]}
disp = {"sRGB 面板": refs["sRGB"], "P3 面板": refs["P3"],
        "BT.2020 面板": refs["BT.2020"]}
ux = {k: C.primaries_uv(v) for k, v in refs.items()}

x = np.arange(len(refs))
w = 0.26
cols = [H.GRAY, H.NAVY, H.ORANGE]
for i, (name, prim) in enumerate(disp.items()):
    vals = [100 * C.coverage(ux[k], C.primaries_uv(prim)) for k in refs]
    bars = ax.bar(x + (i - 1) * w, vals, w * 0.88, label=name, color=cols[i],
                  edgecolor="white", linewidth=0.6, zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 2.0, f"{v:.0f}", ha="center",
                va="bottom", fontsize=5.6, color=H.DARK, zorder=4)

ax.set_xticks(x)
ax.set_xticklabels(list(refs.keys()), fontsize=7.4)
ax.set_ylim(0, 140)
ax.set_yticks([0, 25, 50, 75, 100])
ax.set_ylabel("$u'v'$ 面积覆盖率  %", fontsize=8.0)
ax.set_xlabel("参考色域", fontsize=8.5)
ax.set_title("(b) 三种基色组合的覆盖率", fontsize=8.4, pad=5)
ax.legend(loc="upper center", fontsize=6.0, ncol=3, handlelength=1.2,
          columnspacing=0.8, borderaxespad=0.1, bbox_to_anchor=(0.5, 1.02))
ax.grid(axis="x", visible=False)

H.save(fig, 8, "f4_display_profile")
print("de before max/mean", de_before.max(), de_before.mean())
print("de after max/mean", de_after.max(), de_after.mean())
