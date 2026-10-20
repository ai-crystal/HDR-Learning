# -*- coding: utf-8 -*-
"""第 17 章 f4：把 0–10000 nit 折叠进 0–600 nit

(a) 三种做法在"输入亮度 → 输出亮度"坐标里的差别：硬裁剪 / 等比压缩 / BT.2390 折弯。
(b) 用亮度分布的视角看"折叠"：输入的亮度分布被压进 600 nit 以内，高光在顶端堆积。
"""
import sys; sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
import hdrfig as H
import numpy as np

CMAX, DMAX = 10000.0, 600.0


def eetf_nit(x_nit, cmax_nit, dmax_nit, offset=0.5):
    """BT.2390 EETF，输入/输出均为 nit。"""
    pq_c = float(H.pq_oetf(cmax_nit))
    pq_d = float(H.pq_oetf(dmax_nit))
    maxLum = pq_d / pq_c
    ks = float(np.clip((1.0 + offset) * maxLum - offset, 0.0, 0.95))
    u = H.pq_oetf(np.clip(x_nit, 0.0, cmax_nit)) / pq_c
    t = np.clip((u - ks) / (1.0 - ks), 0.0, 1.0)
    pb = ((2 * t**3 - 3 * t**2 + 1) * ks
          + (t**3 - 2 * t**2 + t) * (1.0 - ks)
          + (-2 * t**3 + 3 * t**2) * maxLum)
    out = np.where(u < ks, u, pb)
    return H.pq_eotf(np.clip(out * pq_c, 0.0, 1.0))


xs = np.linspace(0, CMAX, 6000)
y_hard = np.minimum(xs, DMAX)
y_lin = xs * DMAX / CMAX
y_eetf = eetf_nit(xs, CMAX, DMAX)

pq600 = float(H.pq_oetf(DMAX))
pq_c = float(H.pq_oetf(CMAX))
ks = float(np.clip(1.5 * pq600 / pq_c - 0.5, 0.0, 0.95))
knee = float(H.pq_eotf(np.clip(ks * pq_c, 0, 1)))       # 滚降起点（nit）
y_e1 = float(eetf_nit(np.array([1000.0]), CMAX, DMAX)[0])
print(f"KS={ks:.4f}  knee={knee:.1f} nit  1000nit->{y_e1:.1f} nit")

fig = H.plt.figure(figsize=(7.2, 4.3))
gs = fig.add_gridspec(1, 2, wspace=0.30, width_ratios=[1.06, 1.0])
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
fig.subplots_adjust(left=0.085, right=0.965, top=0.80, bottom=0.145)

# ================================ (a) 映射曲线 ================================
ax1.axvspan(knee, CMAX, color=H.TEAL, alpha=0.075, zorder=0)
ax1.plot(xs, y_hard, color=H.RED, ls=":", lw=2.2, label="硬裁剪")
ax1.plot(xs, y_lin, color=H.GRAY, ls="--", lw=2.0, label="等比压缩（整体调暗）")
ax1.plot(xs, y_eetf, color=H.TEAL, lw=2.6, label="BT.2390 折弯")
ax1.axhline(DMAX, color=H.GOLD, lw=1.1, ls="-.", alpha=0.9)
ax1.plot([knee], [knee], "o", color=H.TEAL, ms=6, mec="white", mew=1.2, zorder=6)
ax1.annotate(f"滚降起点 ≈ {knee:.0f} nit\n（以下原样通过）", xy=(knee, knee),
             xytext=(knee + 750, knee + 150), fontsize=8.0, color=H.TEAL,
             arrowprops=dict(arrowstyle="->", color=H.TEAL, lw=1.0))

ax1.axvline(1000, color="#9aa7b4", lw=0.9, ls=":")
for yy, cc in ((600.0, H.RED), (60.0, H.GRAY), (y_e1, H.TEAL)):
    ax1.plot([1000], [yy], "o", color=cc, ms=4.6, mec="white", mew=0.9, zorder=6)
ax1.annotate("同一个 1000 nit 高光：\n"
             f"硬裁剪 {600:.0f} / 折弯 {y_e1:.0f} / 等比 {60:.0f} nit",
             xy=(1000, y_e1), xytext=(1900, 445), fontsize=8.0, color="#33475b",
             arrowprops=dict(arrowstyle="->", color="#33475b", lw=1.0))
ax1.text(6320, DMAX + 18, "显示上限 600 nit", fontsize=8.2, color="#a07d1f", ha="left")
ax1.text(knee + 330, 34, "高光折叠区", fontsize=8.2, color="#0e7267")
ax1.set_xlim(0, CMAX); ax1.set_ylim(0, 700)
ax1.set_xlabel("输入亮度 / nit（0–10000）")
ax1.set_ylabel("输出亮度 / nit（0–600）")
ax1.set_title("(a) 0–10000 nit 怎么落进 0–600 nit", fontsize=10.5)
ax1.legend(loc="upper left", fontsize=7.7, handlelength=1.9, labelspacing=0.35,
           frameon=True, facecolor="white", edgecolor="#c3ccd6", framealpha=0.92)

axin = ax1.inset_axes([0.585, 0.10, 0.395, 0.325])
xz = np.linspace(0, 700, 1500)
axin.plot(xz, xz, color=H.LGRAY, ls=(0, (1, 2)), lw=1.2)
axin.plot(xz, np.minimum(xz, DMAX), color=H.RED, ls=":", lw=1.4)
axin.plot(xz, xz * DMAX / CMAX, color=H.GRAY, ls="--", lw=1.3)
axin.plot(xz, eetf_nit(xz, CMAX, DMAX), color=H.TEAL, lw=1.8)
axin.set_title("放大：中间调区", fontsize=7.2, pad=2)
axin.tick_params(labelsize=6.2)
axin.set_xlim(0, 700); axin.set_ylim(0, 620)
axin.grid(alpha=0.5)
axin.text(30, 470, "折弯曲线紧贴 45°虚线\n→ 中间调几乎不变", fontsize=6.2, color="#33475b")

# ================================ (b) 分布折叠 ================================
rng = np.random.default_rng(20261015)
sel = np.array([], dtype=float)
while sel.size < 400000:
    cand = rng.normal(1.7, 0.95, 400000)
    sel = np.concatenate([sel, cand[(cand > -3.0) & (cand < 4.0)]])
L = 10.0 ** sel[:400000]
pq_in = H.pq_oetf(L)
pq_out = H.pq_oetf(eetf_nit(L, CMAX, DMAX))
bins = np.linspace(0, 1, 141)
cent = 0.5 * (bins[1:] + bins[:-1])
h_in, _ = np.histogram(pq_in, bins=bins, density=True)
h_out, _ = np.histogram(pq_out, bins=bins, density=True)
ymax = max(h_in.max(), h_out.max())

ax2.fill_between(cent, h_in, color=H.ORANGE, alpha=0.30, lw=0,
                 label="输入：亮度分布")
ax2.plot(cent, h_in, color=H.ORANGE, lw=1.6)
ax2.fill_between(cent, h_out, color=H.TEAL, alpha=0.42, lw=0,
                 label="输出：折叠进 600 nit 以内")
ax2.plot(cent, h_out, color=H.TEAL, lw=1.8)
ax2.axvline(pq600, color=H.DARK, lw=1.2, ls="--", alpha=0.85)
ax2.axvline(float(H.pq_oetf(100.0)), color=H.GOLD, lw=1.1, ls="-.")
ax2.text(0.735, ymax * 1.45, "600 nit 上限", fontsize=8.0, color=H.DARK,
         ha="left", va="center")
ax2.text(float(H.pq_oetf(100.0)) - 0.020, ymax * 0.75, "100 nit\n（SDR 白）",
         fontsize=7.4, color="#a07d1f", ha="right", va="center")
ax2.annotate("高光尾巴被压到右边这一小段\n—— 这就是“折叠”",
             xy=(pq600 - 0.018, ymax * 0.90), xytext=(0.05, ymax * 1.45),
             fontsize=7.9, color="#0e7267", ha="left",
             arrowprops=dict(arrowstyle="->", color=H.TEAL, lw=1.0))
ax2.set_xlim(0, 1)
ax2.set_ylim(0, ymax * 2.05)
ax2.set_xlabel("亮度（PQ 码值 0–1）")
ax2.set_ylabel("相对像素数量（密度）")
ax2.set_title("(b) 折叠之后：高光挤在顶端", fontsize=10.5)
ax2.legend(loc="upper left", fontsize=7.5, handlelength=1.8, labelspacing=0.35,
           frameon=True, facecolor="white", edgecolor="#c3ccd6", framealpha=0.92)
sx = ax2.secondary_xaxis("top", functions=(H.pq_eotf, H.pq_oetf))
sx.set_xlabel("对应的绝对亮度 / nit", fontsize=8.5, labelpad=3)
sx.set_ticks([0, 1, 10, 100, 1000, 10000]); sx.tick_params(labelsize=7.5)

fig.suptitle("把 0–10000 nit 折叠进 0–600 nit：怎么折叠，效果差很多",
             fontsize=12.5, fontweight="bold", y=0.975)

H.save(fig, 17, "f4_fold")
