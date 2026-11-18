# -*- coding: utf-8 -*-
"""图 08-2：静态元数据“整部影片共用一套参数”。

上：逐帧亮度随时间变化（24 fps，示意内容）——不管暗场还是雪原，都看同一组参数。
下：全片唯一一条色调映射曲线（对比“本应分场景切换”的两条理想曲线）。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import numpy as np
import hdrfig as H
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

FPS = 24
DUR = 6000.0                                  # 秒，约 100 分钟
N = int(FPS * DUR)                            # 144000 帧

# 场景：(起, 止) 秒, 名称, 峰值基准 nit, 平均基准 nit
SCENES = [
    (0, 600, "烛光晚餐（暗场）", 150, 10),
    (600, 1800, "夜晚街头（点光源闪烁）", 700, 25),
    (1800, 2700, "室内对话（中亮）", 320, 110),
    (2700, 3300, "正午雪原（大面积亮场）", 2100, 900),
    (3300, 3390, "爆炸高光（一闪而过）", 4000, 380),
    (3390, 4400, "海边日落", 1400, 420),
    (4400, 6000, "夜景收尾（暗场）", 350, 20),
]


def build_content():
    """合成“逐帧峰值亮度 / 逐帧平均亮度”两条曲线（示意数值，固定随机种子可复现）。"""
    rng = np.random.default_rng(8)
    peak = np.zeros(N)
    avg = np.zeros(N)
    for s, e, name, pk, av in SCENES:
        i0, i1 = int(s * FPS), int(e * FPS)
        n = i1 - i0
        t = np.linspace(0, 1, n)
        f = 1.0 + 0.6 * np.sin(2.0 * np.pi * 0.7 * t) + 0.25 * np.sin(2.0 * np.pi * 3.1 * t)
        peak[i0:i1] = pk * (0.75 + 0.25 * f) * (1.0 + 0.02 * rng.standard_normal(n))
        avg[i0:i1] = av * (0.85 + 0.15 * f) * (1.0 + 0.02 * rng.standard_normal(n))
    # 街头点光源的瞬时闪烁、闪电式短暂高光
    for s, e, name, pk, av in SCENES:
        if "点光源" in name:
            i0, i1 = int(s * FPS), int(e * FPS)
            blk = (rng.random(i1 - i0) < 0.004)
            peak[i0:i1] = np.where(blk, peak[i0:i1] * 1.8, peak[i0:i1])
    peak = np.clip(peak, 1.31, 4000)
    avg = np.clip(avg, 1.31, peak * 0.95)
    return peak, avg


peak, avg = build_content()
maxcll = peak.max()
i_cll = int(np.argmax(peak))
maxfall = avg.max()
i_fall = int(np.argmax(avg))
print(f"MaxCLL = {maxcll:.0f} nit @ {i_cll/FPS:.0f}s ; MaxFALL = {maxfall:.0f} nit @ {i_fall/FPS:.0f}s")

# ---------------- 色调映射：BT.2390 EETF ----------------
def bt2390_eetf(code_in, target_nit, min_nit=0.0):
    maxL = H.pq_oetf(target_nit)
    minL = H.pq_oetf(max(min_nit, 1e-5))
    KS = 1.5 * maxL - 0.5
    E1 = (code_in - minL) / (1.0 - minL)
    E2 = np.array(E1, dtype=float)
    m = E1 >= KS
    P = (E1[m] - KS) / (1.0 - KS)
    E2[m] = ((2 * P ** 3 - 3 * P ** 2 + 1) * KS
             + (P ** 3 - 2 * P ** 2 + P) * (1 - KS)
             + (-2 * P ** 3 + 3 * P ** 2) * maxL)
    return np.clip(E2 + minL, 0, 1)


cin = np.linspace(H.pq_oetf(0.001), 1.0, 900)
x_nit = H.pq_eotf(cin)
y_single = H.pq_eotf(bt2390_eetf(cin, 600))
y_dark = H.pq_eotf(bt2390_eetf(cin, 1000))
y_bright = H.pq_eotf(bt2390_eetf(cin, 350))
o_4000 = np.interp(4000.0, x_nit, y_single)

fig = plt.figure(figsize=(7.2, 5.8))
gs = fig.add_gridspec(2, 1, height_ratios=[1.25, 1.0], hspace=0.46)

# ---------------- 上：逐帧亮度时序 ----------------
ax = fig.add_subplot(gs[0])
tt = np.arange(N) / FPS / 60.0            # 分钟
ax.fill_between(tt, 1.3, peak, color=H.ORANGE, alpha=0.16, lw=0, zorder=2)
ax.plot(tt, peak, color=H.ORANGE, lw=0.55, zorder=3, label="逐帧峰值亮度（最亮像素）")
ax.plot(tt, avg, color=H.TEAL, lw=0.7, zorder=3, label="逐帧平均亮度（全画面）")
ax.axhline(maxcll, color=H.RED, ls="--", lw=1.5, zorder=4,
           label=f"MaxCLL = {maxcll:.0f} nit（全片唯一值）")
ax.axhline(maxfall, color=H.BLUE, ls="-.", lw=1.5, zorder=4,
           label=f"MaxFALL = {maxfall:.0f} nit（全片唯一值）")

# 场景分隔与名称
for k, (s, e, name, pk, av) in enumerate(SCENES):
    ax.axvline(s / 60.0, color=H.LGRAY, lw=0.8, zorder=1)
    short = name.split("（")[0]
    ax.text((s + e) / 120.0, 26000 if k % 2 == 0 else 12000, short,
            fontsize=6.2, color=H.DARK, ha="center", va="center", zorder=7)
ax.axvline(DUR / 60.0, color=H.LGRAY, lw=0.8, zorder=1)

ax.plot([i_cll / FPS / 60.0], [maxcll], marker="v", ms=5, color=H.RED, zorder=6)
ax.annotate("全片最亮的一帧（爆炸）\n→ 它决定了 MaxCLL",
            xy=(i_cll / FPS / 60.0 + 0.6, maxcll), xytext=(58, 2300),
            fontsize=7.0, color=H.RED, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=0.9),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=H.RED, lw=0.7, alpha=0.95))
ax.plot([i_fall / FPS / 60.0], [maxfall], marker="v", ms=5, color=H.BLUE, zorder=6)
ax.annotate("整片“平均最亮”的那一帧（雪原）\n→ 它决定了 MaxFALL",
            xy=(i_fall / FPS / 60.0, maxfall * 0.93), xytext=(46, 250),
            fontsize=7.0, color=H.BLUE, ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=H.BLUE, lw=0.9),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=H.BLUE, lw=0.7, alpha=0.95))

ax.set_yscale("log")
ax.set_ylim(1.3, 42000)
ax.set_xlim(0, DUR / 60.0)
ax.set_xlabel("影片时间（分钟，逐帧 24 fps 采样）")
ax.set_ylabel("亮度（nit，对数轴）")
ax.set_title("静态元数据：整部影片共用一套参数，从烛光到雪原都不换",
             fontsize=11, color=H.NAVY, pad=18)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"{v:g}"))
ax.yaxis.set_minor_formatter(mticker.NullFormatter())
ax.grid(True, which="both", alpha=0.45)
ax.legend(loc="lower left", fontsize=7.0, ncol=2, handlelength=1.8,
          columnspacing=1.0, labelspacing=0.3)

# ---------------- 下：唯一一条映射曲线 ----------------
ax2 = fig.add_subplot(gs[1])
ax2.plot(x_nit, x_nit, color=H.GRAY, ls=":", lw=1.1, label="理想 1:1（不压缩）")
ax2.plot(x_nit, y_dark, color=H.GRAY, ls="--", lw=1.2,
         label="偏暗场景“想要”的曲线（少压高光、多抬暗部）")
ax2.plot(x_nit, y_bright, color=H.GRAY, ls="--", lw=1.2,
         label="偏亮场景“想要”的曲线（狠压高光）")
ax2.plot(x_nit, y_single, color=H.NAVY, lw=2.6,
         label="HDR10 全片唯一共用的那一条（目标 600 nit 屏）")
ax2.axhline(600, color=H.RED, ls="-.", lw=1.1)
ax2.text(200, 780, "显示器峰值 600 nit", fontsize=7.0, color=H.RED, ha="center")
ax2.plot([4000], [o_4000], marker="o", ms=4.5, color=H.NAVY, zorder=5)
ax2.annotate(f"4000 nit 高光 → 压到 {o_4000:.0f} nit\n暗场也被同一条曲线抬灰",
             xy=(4000, o_4000), xytext=(60, 6),
             fontsize=7.0, color=H.NAVY,
             arrowprops=dict(arrowstyle="->", color=H.NAVY, lw=0.9))
ax2.text(0.02, 0.97,
         "一部电影 = 一张曝光表：\n暗场和亮场只能用同一条曲线折中",
         transform=ax2.transAxes, ha="left", va="top", fontsize=8.0,
         color=H.DARK, linespacing=1.5)
ax2.set_xscale("log"); ax2.set_yscale("log")
ax2.set_xlim(0.001, 10000); ax2.set_ylim(0.002, 10000)
ax2.set_xlabel("内容输入亮度（nit，对数轴）")
ax2.set_ylabel("映射后输出亮度（nit，对数轴）")
ax2.set_title("全片只有一条映射曲线 → 两端都只能折中", fontsize=10.5,
              color=H.NAVY, pad=6)
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"{v:g}"))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"{v:g}"))
ax2.xaxis.set_minor_formatter(mticker.NullFormatter())
ax2.yaxis.set_minor_formatter(mticker.NullFormatter())
ax2.grid(True, which="both", alpha=0.45)
ax2.legend(loc="lower right", fontsize=6.8, handlelength=1.8, labelspacing=0.3)

H.save(fig, 8, "f2_static_meta")
