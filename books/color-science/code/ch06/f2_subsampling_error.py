# -*- coding: utf-8 -*-
"""第 06 章 图 2：4:2:0 色度子采样在 YCbCr 与 ICtCp 下的误差。

测试图案：6 个 BT.2020 满饱和色（1000 cd/m²）各自与"等亮度灰"相邻，构成 2×2 的
子采样单元；色度按单元取平均、亮度保持逐像素，然后重建并计算 ΔE_ITP。
所有数值由 ictcp.py 的公式算出，无手工填数。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H

H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import ictcp as T

plt = H.plt

PEAK = 1000.0
NAMES = ["红", "黄", "绿", "青", "蓝", "品红"]
COLS = [(1., 0, 0), (1, 1, 0), (0, 1., 0), (0, 1, 1), (0, 0, 1.), (1, 0, 1)]

px = []
for c in COLS:
    Y = float(np.array(c) @ T.M_2020.T[1])
    px += [np.array(c, dtype=float), np.full(3, Y)]
img = np.array(px)


def recon(space):
    n = len(img)
    if space == "ycbcr":
        enc = T.rgb_lin_to_ycbcr(img, PEAK)
        rec = enc.copy()
        for i in range(0, n, 2):
            rec[i:i + 2, 1:] = enc[i:i + 2, 1:].mean(0)
        y, cb, cr = rec[:, 0], rec[:, 1], rec[:, 2]
        rp = y + 1.4746 * cr
        bp = y + 1.8814 * cb
        gp = (y - 0.2627 * rp - 0.0593 * bp) / 0.6780
        return T.pq_eotf(np.clip(np.stack([rp, gp, bp], 1), 0, 1)) / PEAK
    enc = T.rgb_lin_to_ictcp(img, PEAK)
    rec = enc.copy()
    for i in range(0, n, 2):
        rec[i:i + 2, 1:] = enc[i:i + 2, 1:].mean(0)
    return np.clip(T.ictcp_to_rgb_lin(rec, PEAK), 0, None)


ref = T.rgb_lin_to_ictcp(img, PEAK)
rows = {}
for space in ("ycbcr", "ictcp"):
    back = recon(space)
    got = T.rgb_lin_to_ictcp(back, PEAK)
    de = T.deltaE_ITP(ref, got)
    dI = 720.0 * np.abs(got[:, 0] - ref[:, 0])
    dC = 720.0 * np.sqrt(0.25 * (got[:, 1] - ref[:, 1]) ** 2 + (got[:, 2] - ref[:, 2]) ** 2)
    rows[space] = dict(
        de=np.array([de[i:i + 2].mean() for i in range(0, 12, 2)]),
        lum=np.array([dI[i:i + 2].mean() for i in range(0, 12, 2)]),
        chr=np.array([dC[i:i + 2].mean() for i in range(0, 12, 2)]))

fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.7))
fig.subplots_adjust(left=0.085, right=0.985, top=0.92, bottom=0.17, wspace=0.26)

# ---------- (a) ΔE_ITP 对比 ----------
ax = axes[0]
x = np.arange(len(NAMES))
ax.bar(x - 0.19, rows["ycbcr"]["de"], width=0.36, color=H.NAVY, label="YCbCr 4:2:0")
ax.bar(x + 0.19, rows["ictcp"]["de"], width=0.36, color=H.ORANGE, label="ICtCp 4:2:0")
ax.set_xticks(x)
ax.set_xticklabels(NAMES, fontsize=9)
ax.set_ylim(0, 340)
ax.set_ylabel("$\\Delta E_{ITP}$", fontsize=10.5)
ax.set_xlabel("测试色（与其等亮度灰相邻）", fontsize=9.5)
ax.legend(loc="upper left", fontsize=8.4, frameon=False, ncol=1)
ax.text(0.98, 0.93, "两组几乎等高\n平均差 %.1f%%" %
        (100 * np.mean(np.abs(rows["ycbcr"]["de"] - rows["ictcp"]["de"]) / rows["ycbcr"]["de"])),
        transform=ax.transAxes, fontsize=8.0, color="#39485a", ha="right", va="top")

# ---------- (b) 误差构成 ----------
ax = axes[1]
idx = np.arange(2)
lum = np.array([rows["ycbcr"]["lum"].mean(), rows["ictcp"]["lum"].mean()])
chr_ = np.array([rows["ycbcr"]["chr"].mean(), rows["ictcp"]["chr"].mean()])
ax.bar(idx, lum, width=0.46, color=H.PURPLE, label="亮度项 $720\\,|\\Delta I|$")
ax.bar(idx, chr_, width=0.46, bottom=lum, color=H.TEAL,
       label="色度项 $720\\sqrt{0.25\\Delta C_t^2+\\Delta C_p^2}$")
ax.set_xticks(idx)
ax.set_xticklabels(["YCbCr 4:2:0", "ICtCp 4:2:0"], fontsize=9.5)
ax.set_ylabel("$\\Delta E_{ITP}$ 的构成（6 色平均）", fontsize=10.0)
ax.set_ylim(0, 300)
ax.legend(loc="upper center", fontsize=7.8, frameon=False,
          bbox_to_anchor=(0.5, -0.13), ncol=2, handlelength=1.4, columnspacing=1.0)
for i in range(2):
    ax.text(i, lum[i] + chr_[i] / 2, f"色度项 {chr_[i]:.0f}", ha="center", va="center",
            fontsize=8.2, color="white")
    ax.text(i, lum[i] + chr_[i] + 8, f"合计 {lum[i] + chr_[i]:.0f}", ha="center",
            va="bottom", fontsize=8.2, color="#39485a")
    ax.annotate(f"亮度项 {lum[i]:.0f}", xy=(i + 0.24, lum[i] * 0.6), xytext=(i + 0.32, 70),
                fontsize=7.6, color=H.PURPLE, ha="left" if i == 0 else "left", va="center",
                arrowprops=dict(arrowstyle="-", color=H.PURPLE, lw=0.8, shrinkA=1,
                                shrinkB=2))

H.save(fig, 6, "f2_subsampling_error")
