# -*- coding: utf-8 -*-
"""第 04 章 图 7：逐通道压缩与亮度比例压缩的色相与彩度差异（按公式计算）。

两种做法：
  A 逐通道：对 R、G、B 三个通道各自做 BT.2390 EETF（目标峰值 300 nit）；
  B 亮度比例：按亮度决定压缩比，三个通道乘同一个系数（彩度变、色相不变）。
两种结果都换到 Rec.2020 线性、再算 CIELAB 的色相角 h_ab 与彩度 C*_ab。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

M = np.array([[0.6369580, 0.1446169, 0.1688810],
              [0.2627002, 0.6779981, 0.0593017],
              [0.0000000, 0.0280727, 1.0609851]])
WHITE = M @ np.ones(3)


def eetf_code(e1, max_lum):
    ks = 1.5 * max_lum - 0.5
    t = np.clip((e1 - ks) / (1.0 - ks), 0.0, 1.0)
    return np.where(e1 < ks, e1,
                    ks * (2 * t ** 3 - 3 * t ** 2 + 1)
                    + (1.0 - ks) * (t ** 3 - 2 * t ** 2 + t)
                    + max_lum * (-2 * t ** 3 + 3 * t ** 2))


def compress_channel(rgb, target):
    e = H.pq_oetf(np.clip(rgb, 0.0, None))
    return H.pq_eotf(eetf_code(e, float(H.pq_oetf(target))))


def lab(rgb):
    r = (M @ rgb) / WHITE
    f = np.where(r > 216.0 / 24389.0, np.cbrt(r), (24389.0 / 27.0 * r + 16.0) / 116.0)
    return np.array([116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])])


def hue_c(rgb):
    L, a, b = lab(rgb)
    return np.degrees(np.arctan2(b, a)) % 360.0, np.hypot(a, b)


colors = {
    "橙红": np.array([1.00, 0.35, 0.10]),
    "黄": np.array([1.00, 1.00, 0.15]),
    "青": np.array([0.10, 1.00, 1.00]),
    "品红": np.array([1.00, 0.15, 1.00]),
    "天蓝": np.array([0.15, 0.55, 1.00]),
    "肤色": np.array([1.00, 0.62, 0.42]),
}
Y0, TARGET = 1000.0, 300.0

names, dh_a, dh_b, dc_a, dc_b = [], [], [], [], []
for name, c in colors.items():
    c = c / (M[1] @ c) * Y0
    h0, c0 = hue_c(c)

    a = compress_channel(c, TARGET)
    h1, c1 = hue_c(a)
    d1 = (h1 - h0 + 180.0) % 360.0 - 180.0

    y = float(M[1] @ c)
    ratio = float(H.pq_eotf(eetf_code(np.array([float(H.pq_oetf(y))]),
                                      float(H.pq_oetf(TARGET)))[0])) / y
    h2, c2 = hue_c(c * ratio)

    names.append(name)
    dh_a.append(d1)
    dh_b.append((h2 - h0 + 180.0) % 360.0 - 180.0)
    dc_a.append((c1 / c0 - 1.0) * 100.0)
    dc_b.append((c2 / c0 - 1.0) * 100.0)

xpos = np.arange(len(names))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 4.0))
fig.subplots_adjust(wspace=0.30)

ax1.bar(xpos - 0.19, dh_a, width=0.38, color=H.RED, label="逐通道 EETF")
ax1.bar(xpos + 0.19, dh_b, width=0.38, color=H.TEAL, label="按亮度比例压缩")
ax1.axhline(0.0, color=H.DARK, lw=0.9)
ax1.axhline(2.0, color=H.GRAY, lw=0.9, ls="--")
ax1.axhline(-2.0, color=H.GRAY, lw=0.9, ls="--")
ax1.text(1.55, 27.0, "虚线为 ±2° 参考", fontsize=8.0, color=H.GRAY)
ax1.set_xticks(xpos)
ax1.set_xticklabels(names)
ax1.set_ylim(-34, 40)
ax1.set_ylabel("CIELAB 色相角偏移（度）")
ax1.set_title("(a) 色相", fontsize=10, pad=4)
ax1.legend(loc="upper right", fontsize=7.8, labelspacing=0.3, borderpad=0.4)

for i, v in enumerate(dh_a):
    ax1.text(i - 0.19, v + (1.2 if v >= 0 else -3.4), f"{v:+.0f}", fontsize=7.4,
             color=H.RED, ha="center")

ax2.bar(xpos - 0.19, dc_a, width=0.38, color=H.RED, label="逐通道 EETF")
ax2.bar(xpos + 0.19, dc_b, width=0.38, color=H.TEAL, label="按亮度比例压缩")
ax2.axhline(0.0, color=H.DARK, lw=0.9)
ax2.set_xticks(xpos)
ax2.set_xticklabels(names)
ax2.set_ylim(-95, 12)
ax2.set_ylabel("CIELAB 彩度 $C^*_{ab}$ 的相对变化（%）")
ax2.set_title("(b) 彩度", fontsize=10, pad=4)
for i, v in enumerate(dc_a):
    ax2.text(i - 0.19, v - 4.5, f"{v:.0f}", fontsize=7.4, color=H.RED, ha="center")
for i, v in enumerate(dc_b):
    ax2.text(i + 0.19, v - 4.5, f"{v:.0f}", fontsize=7.4, color=H.TEAL, ha="center")

H.save(fig, 4, "f7_color_order")
print("dHue", dict(zip(names, np.round(dh_a, 1))))
print("dChroma", dict(zip(names, np.round(dc_a, 1))), np.round(dc_b, 1))
