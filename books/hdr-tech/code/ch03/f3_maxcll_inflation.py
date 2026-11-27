# -*- coding: utf-8 -*-
"""图 3-3：MaxCLL 虚高与元数据缺失时，显示端给出的实际亮度（公式推导的示意）。

模型说明（正文图注同样写明，属简化模型，不代表任何厂商实现）：
在 PQ 码值域做分段压缩。内容亮度 L 的绝对码值 c = PQ_OETF(L)，显示峰值 D、
元数据声明的内容峰值 S，拐点取
    L_k = 0.7 · min(D, S)            （S ≤ D 时曲线退化为 1:1 直通）
拐点以下逐点保留，拐点以上按
    t = (c - c_k)/(c_S - c_k),  q = 1 - (1 - t)^2
    c_out = c_k + (c_D - c_k)·q
压到显示峰值。用二次幂代替贝塞尔肩部，只保留单调性与端点条件。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H
H.set_book("hdr-tech")

plt = H.plt
plt.rcParams["mathtext.fontset"] = "dejavusans"


def tone(L, S, D, knee_frac=0.7, p=2.0):
    L = np.asarray(L, dtype=float)
    c = H.pq_oetf(L)
    cS = float(H.pq_oetf(S))
    cD = float(H.pq_oetf(D))
    if S <= D:
        return L.copy()
    ck = float(H.pq_oetf(knee_frac * min(D, S)))
    t = np.clip((c - ck) / (cS - ck), 0, 1)
    c_out = np.where(c <= ck, c, ck + (cD - ck) * (1 - (1 - t) ** p))
    return H.pq_eotf(c_out)


GROUPS = [
    ("1000 nit 屏\n内容高光 1000 nit", 1000, 1000),
    ("600 nit 屏\n内容高光 600 nit", 600, 600),
    ("600 nit 屏\n内容高光 1000 nit", 600, 1000),
]
SCEN = [(1000, H.TEAL, "元数据正确"),
        (4010, H.ORANGE, "MaxCLL 虚高 4010"),
        (10000, H.RED, "元数据缺失")]

fig, ax = plt.subplots(figsize=(8.4, 4.0))
fig.subplots_adjust(left=0.095, right=0.982, bottom=0.185, top=0.905)

n, w = len(GROUPS), 0.24
xs = np.arange(n)
for j, (S, color, lab) in enumerate(SCEN):
    vals = [float(tone(L, S, D)) for _, D, L in GROUPS]
    pos = xs + (j - 1) * w
    ax.bar(pos, vals, width=w * 0.92, color=color, edgecolor="white",
           linewidth=0.8, label=lab, zorder=3)
    for x, v in zip(pos, vals):
        ax.text(x, v + 18, f"{v:.0f}", ha="center", va="bottom", fontsize=8.0,
                color=color)

# 理想输出位置（元数据正确时的输出）
ideal = [float(tone(L, 1000, D)) for _, D, L in GROUPS]
for x, v in zip(xs, ideal):
    ax.plot([x - 0.42, x + 0.42], [v, v], color=H.NAVY, lw=1.0,
            ls=(0, (4, 3)), zorder=4)

ax.set_xticks(xs)
ax.set_xticklabels([g[0] for g in GROUPS], fontsize=8.6)
ax.set_ylabel("显示端实际输出亮度（cd/m$^2$）")
ax.set_ylim(0, 1180)
ax.grid(axis="x", visible=False)
ax.legend(loc="upper right", fontsize=8.0, handlelength=1.6, ncol=1,
          borderpad=0.45, labelspacing=0.32)
ax.text(0.012, 0.945, "虚线为元数据正确时的输出", transform=ax.transAxes,
        fontsize=7.8, color=H.NAVY, va="top")

H.save(fig, 3, "f3_maxcll_inflation")
for S, c, lab in SCEN:
    print(lab, [round(float(tone(L, S, D)), 1) for _, D, L in GROUPS])
