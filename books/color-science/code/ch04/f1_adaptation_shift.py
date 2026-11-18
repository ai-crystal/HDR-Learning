# -*- coding: utf-8 -*-
"""第 04 章 图 1：同一批色样在暖色光源 A 下，适应前后 CIECAM02 色貌坐标的变化。

物理设定：以 D65 下的 XYZ 代表色样的“反射特性”，用 CAT02 完全 von Kries 换算到光源 A；
"适应前"= 观察者仍按 D65 白点解读，"适应后"= 参考白取 A。
所有数值由 cam02.py 的 CIECAM02 正向模型计算。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cam02 as C

plt = H.plt

WD = C.white_XYZ("D65")
WA = C.white_XYZ("A")


def von_kries(XYZ, w_from, w_to):
    M = C.M_CAT02
    rgb = np.atleast_2d(XYZ) @ M.T
    r = (np.atleast_2d(w_to) @ M.T) / (np.atleast_2d(w_from) @ M.T)
    return (rgb * r) @ np.linalg.inv(M).T


PATCHES = [
    ("红",   0.550, 0.330),
    ("橙",   0.500, 0.410),
    ("黄",   0.420, 0.500),
    ("绿",   0.280, 0.520),
    ("青",   0.220, 0.350),
    ("蓝",   0.180, 0.160),
    ("紫",   0.280, 0.200),
    ("肤色", 0.400, 0.360),
]

rows = []
for name, x, y in PATCHES:
    XYZ_D65 = C.xy_to_XYZ(x, y, 18.0)
    XYZ_A = von_kries(XYZ_D65, WD, WA)[0]
    before = C.cam02(XYZ_A, WD, LA=200.0, Yb=20.0)    # 未适应：仍按 D65 解读
    after = C.cam02(XYZ_A, WA, LA=200.0, Yb=20.0)     # 适应后
    rows.append(dict(name=name, before=before, after=after))

fig = plt.figure(figsize=(7.6, 4.5))
ax = fig.add_axes([0.02, 0.12, 0.44, 0.80], projection="polar")
ax.set_theta_zero_location("E")
ax.set_theta_direction(1)
ax.set_rlim(0, 128)
ax.set_rticks([25, 50, 75, 100])
ax.set_rlabel_position(292)
ax.grid(color="#dde3ea", lw=0.7)
ax.set_xticks(np.radians(np.arange(0, 360, 45)))
ax.set_xticklabels(["0°", "45°", "90°", "135°", "180°", "225°", "270°", "315°"],
                   fontsize=8.2)
ax.set_xlabel("角度为色相角 h（°），径向为彩度 C", fontsize=9.5, labelpad=12)

LAB = {"红": (0, 14), "橙": (-6, 16), "黄": (4, 16), "绿": (-10, 14),
       "青": (-8, 12), "蓝": (0, -14), "紫": (10, 12), "肤色": (24, 13)}

for row in rows:
    b, a = row["before"], row["after"]
    th0, th1 = np.radians([b["h"], a["h"]])
    if abs(b["h"] - a["h"]) > 180:
        th1 = th1 + np.radians(360) * np.sign(b["h"] - a["h"])
    ax.annotate("", xy=(th1, a["C"]), xytext=(th0, b["C"]),
                arrowprops=dict(arrowstyle="-|>", color=H.ORANGE, lw=1.3,
                                shrinkA=3.5, shrinkB=3.5), zorder=3)
    ax.plot([th0], [b["C"]], marker="o", ms=7, mfc="white", mec=H.NAVY,
            mew=1.5, zorder=4)
    ax.plot([th1], [a["C"]], marker="o", ms=7, mfc=H.NAVY, mec=H.NAVY,
            mew=1.2, zorder=4)
    dth, dr = LAB[row["name"]]
    rl = max(b["C"], a["C"]) + dr
    ax.text(th0 * 0.5 + th1 * 0.5 + np.radians(dth), rl, row["name"],
            fontsize=8.6, color="#12233b", ha="center", va="center", zorder=5,
            bbox=dict(facecolor="white", alpha=0.9, edgecolor="none", pad=1.2))


ax.plot([], [], "o", ms=7, mfc="white", mec=H.NAVY, mew=1.5, label="适应前")
ax.plot([], [], "o", ms=7, mfc=H.NAVY, mec=H.NAVY, label="适应后")
ax.legend(loc="lower left", bbox_to_anchor=(-0.16, -0.10), fontsize=8.4,
          frameon=False, ncol=2, columnspacing=1.0)

# ---------- 右：明度几乎不变，彩度大幅回落，色相同时旋转 ----------
ax2 = fig.add_axes([0.60, 0.15, 0.375, 0.70])
idx = np.arange(len(rows))
dC = [r["after"]["C"] - r["before"]["C"] for r in rows]
dJ = [r["after"]["J"] - r["before"]["J"] for r in rows]
dh = [((r["after"]["h"] - r["before"]["h"] + 180) % 360) - 180 for r in rows]

ax2.barh(idx - 0.19, dC, height=0.34, color=H.TEAL, label="ΔC 彩度")
ax2.barh(idx + 0.19, dJ, height=0.34, color=H.PURPLE, label="ΔJ 明度")
ax2.axvline(0, color="#4a5666", lw=1.0)
ax2.set_yticks(idx)
ax2.set_yticklabels([r["name"] for r in rows], fontsize=9)
ax2.invert_yaxis()
ax2.set_xlabel("适应后减适应前（CIECAM02 单位）", fontsize=9.5)
ax2.set_xlim(-42, 82)
ax2.set_ylim(len(rows) - 0.45, -1.15)
ax2.legend(loc="lower left", bbox_to_anchor=(0.0, 1.005), fontsize=8.4,
           ncol=2, columnspacing=1.2, frameon=False)
ax2.grid(axis="y", visible=False)

for i, (c, h) in enumerate(zip(dC, dh)):
    ax2.text(c + (1.8 if c >= 0 else -1.8), i - 0.19, f"{c:+.0f}", fontsize=7.8,
             va="center", ha="left" if c >= 0 else "right", color="#0f5f50")
    ax2.text(60, i, f"Δh {h:+.0f}°", fontsize=7.8, va="center", ha="left",
             color="#8a5a12")
ax2.text(60, -0.82, "Δh", fontsize=8.0, color="#8a5a12")

H.save(fig, 4, "f1_adaptation_shift")
