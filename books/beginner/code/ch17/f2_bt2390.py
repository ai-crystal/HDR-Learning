# -*- coding: utf-8 -*-
"""第 17 章 f2：BT.2390 EETF 曲线（HDR → SDR）

EETF = Electrical-Electrical Transfer Function，ITU-R BT.2390 给出的参考映射。
算法（在 PQ 码值域里做）：
    maxLum = PQ(显示峰值) / PQ(内容峰值)        # 相对内容峰值归一化
    KS     = 1.5 * maxLum - 0.5                 # 滚降起点
    u <  KS : 原样通过（恒等段）
    u >= KS : 用分段三次 Hermite 样条把 [KS,1] 平滑收进 [KS,maxLum]
              （起点斜率 1，终点斜率 0 —— 所以高光是"缓缓减速"而不是硬折）
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np


def eetf(x_nit, cmax_nit, dmax_nit, offset=0.5):
    """返回 (输出亮度 nit, KS, maxLum, 恒等段顶端的绝对 nit)。

    offset=0.5 时 KS = (1+offset)*maxLum - offset = 1.5*maxLum - 0.5。
    """
    pq_c = float(H.pq_oetf(cmax_nit))
    pq_d = float(H.pq_oetf(dmax_nit))
    maxLum = pq_d / pq_c
    ks = float(np.clip((1.0 + offset) * maxLum - offset, 0.0, 0.95))
    u = H.pq_oetf(np.clip(x_nit, 0.0, cmax_nit)) / pq_c
    out = u.copy()
    if ks < 1.0:
        t = np.clip((u - ks) / (1.0 - ks), 0.0, 1.0)
        pb = ((2 * t**3 - 3 * t**2 + 1) * ks
              + (t**3 - 2 * t**2 + t) * (1.0 - ks)
              + (-2 * t**3 + 3 * t**2) * maxLum)
        out = np.where(u < ks, u, pb)
    y = H.pq_eotf(np.clip(out * pq_c, 0.0, 1.0))
    knee_nit = float(H.pq_eotf(np.clip(ks * pq_c, 0.0, 1.0)))
    return y, ks, maxLum, knee_nit


DISP = 100.0                                   # 目标 SDR 显示峰值（nit）
CASES = [("内容峰值 1000 nit", H.NAVY, 1000.0),
         ("内容峰值 4000 nit", H.TEAL, 4000.0)]

fig = H.plt.figure(figsize=(7.2, 4.0))
gs = fig.add_gridspec(1, 2, wspace=0.32, width_ratios=[1.0, 1.0])
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
fig.subplots_adjust(left=0.085, right=0.90, top=0.775, bottom=0.245)

# ============================ (a) nit 域的输入输出曲线 ============================
xs = np.logspace(0, 4, 3000)
ax1.plot(xs, np.minimum(xs, DISP), color=H.RED, ls=":", lw=2.2, label="硬裁剪（直接砍平）")
ax1.plot(xs, xs, color=H.LGRAY, ls=(0, (1, 2)), lw=1.6, label="输入 = 输出（超出屏幕能力）")

for label, col, cmax in CASES:
    y, ks, maxLum, knee = eetf(xs, cmax, DISP)
    ax1.plot(xs, y, color=col, lw=2.3, label=f"BT.2390 EETF：{label} → 100 nit")
    ax1.plot([knee], [knee], "o", color=col, ms=5.5, mec="white", mew=1.0, zorder=6)

ax1.axhline(DISP, color=H.GOLD, lw=1.2, ls="-.", alpha=0.95)
ax1.text(8500, 112, "SDR 上限 100 nit", fontsize=8.2, color="#a07d1f", ha="right")
ax1.text(33, 1.05,
         "○ 滚降起点 KS：低亮度段原样通过\n"
         "滚降段：越亮压得越狠，但不会突然截断\n"
         "内容峰值越高，同一块屏幕压得越早",
         fontsize=8.0, color="#33475b", va="bottom", ha="left",
         bbox=dict(boxstyle="round,pad=0.30", fc="white", ec="#c3ccd6", lw=0.8, alpha=0.93))
ax1.set_xscale("log"); ax1.set_yscale("log")
ax1.set_xlim(1, 10000); ax1.set_ylim(0.8, 620)
ax1.set_xlabel("输入亮度 / nit（对数轴）")
ax1.set_ylabel("输出亮度 / nit（对数轴）")
ax1.set_title("(a) HDR → SDR：亮度坐标里的映射", fontsize=10.5)

# ============================ (b) PQ 码值域里的走法 ============================
xq = np.linspace(0, 1, 4000)
xq_nit = H.pq_eotf(xq)
ax2.plot(xq, xq, color=H.LGRAY, ls=(0, (1, 2)), lw=1.6)
ks_txt = []
for label, col, cmax in CASES:
    _y, ks, maxLum, knee = eetf(xq_nit, cmax, DISP)
    pcmax = float(H.pq_oetf(cmax))
    m = xq <= pcmax + 1e-9
    ax2.plot(xq[m], H.pq_oetf(_y[m]), color=col, lw=2.3)
    ax2.axhline(maxLum, color=col, ls="--", lw=1.0, alpha=0.8)
    ax2.axvline(ks * pcmax, color=col, ls=":", lw=1.0, alpha=0.8)
    ax2.plot([ks * pcmax], [ks * pcmax], "o", color=col, ms=5.5, mec="white", mew=1.0, zorder=6)
    ax2.text(0.955, maxLum + 0.014, f"最高只能到 PQ={maxLum:.3f}",
             fontsize=7.8, color=col, ha="right")
    ks_txt.append(f"{label} → 100 nit：KS={ks:.2f}（{knee:.0f} nit）")

ax2.set_xlim(0, 1); ax2.set_ylim(0, 1.0)
ax2.set_xlabel("输入（PQ 码值 0–1）")
ax2.set_ylabel("输出\n（PQ 码值 0–1）")
ax2.set_title("(b) PQ 码值域：恒等段 + 滚降段", fontsize=10.5)
sx = ax2.secondary_xaxis("top", functions=(H.pq_eotf, H.pq_oetf))
sx.set_xlabel("对应的输入亮度 / nit", fontsize=8.5, labelpad=3)
sx.set_ticks([0, 1, 10, 100, 1000, 10000]); sx.tick_params(labelsize=7.5)
sy = ax2.secondary_yaxis("right", functions=(H.pq_eotf, H.pq_oetf))
sy.set_ylabel("对应的输出亮度 / nit", fontsize=8.5, labelpad=3)
sy.set_ticks([0, 1, 10, 100]); sy.tick_params(labelsize=7.5)
ax2.text(0.50, 0.40,
         "恒等段（u < KS）：原样通过\n"
         "滚降段（u > KS）：Hermite 样条，\n"
         "起点斜率 1、终点斜率 0 —— 平滑收住\n"
         + "\n".join(ks_txt),
         fontsize=7.7, color="#33475b", va="top", ha="left",
         bbox=dict(boxstyle="round,pad=0.32", fc="#f7f9fb", ec="#c3ccd6", lw=0.8))

h, l = ax1.get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=2, fontsize=8.0,
           bbox_to_anchor=(0.5, -0.035), handlelength=2.1, columnspacing=1.4,
           labelspacing=0.35)
fig.suptitle("BT.2390 EETF：把 HDR 高光“缓缓收住”的标准参考曲线",
             fontsize=12.5, fontweight="bold", y=0.985)

H.save(fig, 17, "f2_bt2390")
