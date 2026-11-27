# -*- coding: utf-8 -*-
"""图 2-5：PQ 与 HLG 互转的量化误差。

链路为：亮度 → PQ 信号 → 亮度 → 场景线性 → HLG 信号（量化）→ 场景线性
→ 亮度。HLG 侧的系统 gamma 取 Lw = 1000 cd/m² 对应的 1.2。纵轴是“一个
量化间隔内的最大相对误差”，也就是码值落在间隔中点时的偏差，因此曲线是平滑
的包络而不是逐点采样的锯齿。PQ 一侧保持理想值，误差只来自 HLG 的量化。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
from matplotlib.ticker import FuncFormatter, NullFormatter
plt.rcParams["mathtext.fontset"] = "dejavusans"


def dec(v):
    s = f"{v:.0e}"
    return s.replace("e+0", "e").replace("e+", "e").replace("e-0", "e-")


LW = 1000.0
GAM = 1.2 + 0.42 * np.log10(LW / 1000.0)


def pq_err(L, bits):
    d = 0.5 / (2 ** bits - 1)
    sig = H.pq_oetf(L)
    hi = H.pq_eotf(np.clip(sig + d, 0, 1))
    lo = H.pq_eotf(np.clip(sig - d, 0, 1))
    return (hi - lo) / 2.0 / L * 100.0


def hlg_of_L(L):
    scene = (L / LW) ** (1.0 / GAM)
    return H.hlg_oetf(np.clip(scene, 1e-7, 1.0))


def L_of_hlg(sig):
    scene = H.hlg_eotf(np.clip(sig, 0, 1))
    return LW * scene ** GAM


def hlg_err(L, bits):
    d = 0.5 / (2 ** bits - 1)
    sig = hlg_of_L(L)
    return (L_of_hlg(sig + d) - L_of_hlg(sig - d)) / 2.0 / L * 100.0


L = np.logspace(np.log10(1e-3), np.log10(950), 700)

fig, ax = plt.subplots(figsize=(7.6, 4.2))
fig.subplots_adjust(left=0.098, right=0.975, bottom=0.145, top=0.95)

ax.axhline(1.0, color=H.GRAY, lw=0.8, ls=(0, (2, 2)), zorder=1)
ax.text(1.12e-3, 1.05, "1%", fontsize=7.6, color=H.GRAY, ha="left", va="bottom")

ax.loglog(L, pq_err(L, 10), color=H.NAVY, lw=2.0, ls=(0, (5, 2)),
          label="PQ 10 bit 量化（直通）")
ax.loglog(L, hlg_err(L, 10), color=H.ORANGE, lw=2.3,
          label="PQ → HLG 10 bit → PQ")
ax.loglog(L, hlg_err(L, 12), color=H.TEAL, lw=2.3,
          label="PQ → HLG 12 bit → PQ")

ax.axvline(203.0, color=H.RED, lw=0.9, ls=(0, (4, 3)), zorder=1)
ax.text(203 * 1.12, 12.5, "参考白 203", fontsize=7.8, color=H.RED,
        ha="left", va="center")

ax.annotate("平方根段码值稀疏，\n暗部互转误差迅速放大",
            xy=(0.012, float(hlg_err(np.array([0.012]), 10)[0])),
            xytext=(0.0014, 2.6), fontsize=7.9, color=H.ORANGE,
            arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=0.9,
                            shrinkA=2, shrinkB=4))
ax.annotate("对数段码值较密，\n亮部三者趋于一致",
            xy=(600.0, float(hlg_err(np.array([600.0]), 10)[0])),
            xytext=(150.0, 2.4), fontsize=7.9, color=H.TEAL,
            arrowprops=dict(arrowstyle="->", color=H.TEAL, lw=0.9,
                            shrinkA=2, shrinkB=4))

ax.set_xlim(1e-3, 1000)
ax.set_ylim(0.02, 40)
ax.set_xticks([1e-3, 1e-2, 1e-1, 1, 10, 100, 1000])
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: dec(v) if v < 1
                                           else f"{v:g}".replace("e+", "e")))
ax.xaxis.set_minor_formatter(NullFormatter())
ax.set_yticks([0.1, 1, 10])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
ax.yaxis.set_minor_formatter(NullFormatter())
ax.set_xlabel("原始亮度（cd/m$^2$）")
ax.set_ylabel("单个量化间隔内的最大相对误差（%）")
ax.legend(loc="lower left", fontsize=8.2, handlelength=2.6,
          borderpad=0.5, labelspacing=0.4)

H.save(fig, 2, "f5_roundtrip_error")
