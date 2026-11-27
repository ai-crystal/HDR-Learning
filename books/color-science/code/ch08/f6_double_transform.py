# -*- coding: utf-8 -*-
"""第 08 章 图 6：双重转换的两种损失（按标准矩阵与量化算出）。

(a) sRGB → Display P3 → sRGB 一次往返的色差分布（8 bit）
(b) Display P3 素材经 sRGB 中转：超出 sRGB 的部分被裁掉，
    往返后与原色的色差随越界量上升；色域内只剩量化误差
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

M_S2P = np.linalg.inv(C.M_P3) @ C.M_SRGB
M_P2S = np.linalg.inv(C.M_SRGB) @ C.M_P3


def quant(x, bits):
    n = 2 ** bits - 1
    return np.clip(np.round(np.clip(x, 0, 1) * n), 0, n) / n


fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1),
                         gridspec_kw={"wspace": 0.30})

# ---------- (a) 一次往返的色差分布 ----------
ax = axes[0]
g = np.linspace(0, 1, 9)
G = np.array(np.meshgrid(g, g, g, indexing="ij")).reshape(3, -1).T
lab0 = C.xyz_to_lab(C.srgb_eotf(G) @ C.M_SRGB.T)


def roundtrip(u, bits):
    p3 = quant(C.srgb_oetf(C.srgb_eotf(u) @ M_S2P.T), bits)
    return quant(C.srgb_oetf(C.srgb_eotf(p3) @ M_P2S.T), bits)


d8 = C.delta_e00(C.xyz_to_lab(C.srgb_eotf(roundtrip(G, 8)) @ C.M_SRGB.T), lab0)
d16 = C.delta_e00(C.xyz_to_lab(C.srgb_eotf(roundtrip(G, 16)) @ C.M_SRGB.T), lab0)

bins = np.linspace(0, 1.0, 41)
ax.hist(d8, bins=bins, color=H.NAVY, alpha=0.88,
        edgecolor="white", linewidth=0.4, zorder=3)
ax.axvline(d8.mean(), color=H.RED, lw=1.2, ls=(0, (4, 2)), zorder=5)
ax.annotate(f"8 bit 平均 {d8.mean():.3f}，最大 {d8.max():.2f}",
            (d8.mean(), 300), xytext=(0.28, 0.62), textcoords="axes fraction",
            fontsize=6.2, color=H.RED, va="center",
            arrowprops=dict(arrowstyle="-|>", color=H.RED, lw=0.7))
ax.text(0.30, 0.80, f"16 bit 中转：平均 {d16.mean():.4f}\n全部落在最左侧一格",
        fontsize=6.0, color=H.ORANGE, transform=ax.transAxes, va="top",
        linespacing=1.5)
ax.set_xlim(0, 1.0)
ax.set_ylim(0, 800)
ax.set_xlabel("往返后与原始色的 $\\Delta E_{00}$", fontsize=8.2)
ax.set_ylabel("色块数（共 729）", fontsize=8.2)
ax.set_title("(a) 一次 sRGB→P3→sRGB 往返", fontsize=8.4, pad=5)
ax.text(0.03, 0.95, "8 bit 中转", fontsize=7.0, color=H.NAVY,
        transform=ax.transAxes, ha="left", va="top")

# ---------- (b) 越界裁剪的损失 ----------
ax = axes[1]
gp = np.linspace(0, 1, 12)
GP = np.array(np.meshgrid(gp, gp, gp, indexing="ij")).reshape(3, -1).T
xyz_p3 = C.srgb_eotf(GP) @ C.M_P3.T
lab_p3 = C.xyz_to_lab(xyz_p3)

lin_srgb = xyz_p3 @ np.linalg.inv(C.M_SRGB).T
ex = np.maximum(np.maximum(-lin_srgb, 0), np.maximum(lin_srgb - 1, 0)).max(axis=1)
s_clip = quant(C.srgb_oetf(np.clip(lin_srgb, 0, 1)), 16)
back_xyz = C.srgb_eotf(s_clip) @ C.M_SRGB.T
d = C.delta_e00(C.xyz_to_lab(back_xyz), lab_p3)

in_g = ex < 1e-6
ax.scatter(ex[in_g], d[in_g], s=12, color=H.GRAY, alpha=0.6, linewidth=0,
           label="sRGB 色域内", zorder=3)
ax.scatter(ex[~in_g], d[~in_g], s=13, color=H.RED, alpha=0.55, linewidth=0,
           label="超出 sRGB", zorder=4)

edges = np.array([0.001, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.25])
cent, means = [], []
for a, b in zip(edges[:-1], edges[1:]):
    m = (ex >= a) & (ex < b)
    if m.sum() > 3:
        cent.append((a + b) / 2)
        means.append(d[m].mean())
ax.plot(cent, means, "o-", color=H.DARK, ms=3.4, lw=1.2, label="分箱均值",
        zorder=6)

ax.set_yscale("log")
ax.set_xlim(-0.008, 0.26)
ax.set_ylim(0.0002, 30)
ax.set_yticks([0.0005, 0.002, 0.01, 0.05, 0.2, 1, 5, 20])
ax.set_yticklabels(["0.0005", "0.002", "0.01", "0.05", "0.2", "1", "5", "20"])
ax.minorticks_off()
ax.set_xlabel("线性光的越界量（$0$ 为恰在边界上）", fontsize=8.0)
ax.set_ylabel("往返后与原始色的 $\\Delta E_{00}$", fontsize=8.0)
ax.set_title("(b) 掉进窄色域的损失", fontsize=8.4, pad=5)
ax.legend(loc="lower right", fontsize=6.2, handlelength=1.3,
          borderaxespad=0.3, markerscale=1.5)

H.save(fig, 8, "f6_double_transform")
print("8bit mean/max %.3f %.3f" % (d8.mean(), d8.max()))
print("16bit mean/max %.4f %.4f" % (d16.mean(), d16.max()))
print("in gamut %d, out %d" % (in_g.sum(), (~in_g).sum()))
print("bin means", [round(v, 2) for v in means])
