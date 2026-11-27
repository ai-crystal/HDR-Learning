# -*- coding: utf-8 -*-
"""图 9-3　个体观察者色匹配函数的分布带与观察者间的相对离散度。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import observer_model as OM
plt = H.plt

lam = OM.LAM
rng = np.random.default_rng(5)
N = 400
ages = rng.uniform(20, 70, N)
macs = rng.uniform(0.30, 0.45, N)
lshift = rng.uniform(-2, 2, N)
mshift = rng.uniform(-1.5, 1.5, N)
cm = np.array([OM.observer_cmf(ages[i], macs[i], lshift[i], mshift[i])
               for i in range(N)])

fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.9),
                         gridspec_kw=dict(wspace=0.27, width_ratios=[1.12, 1.0]))
fig.subplots_adjust(bottom=0.26)

labels = [r"$\bar{x}(\lambda)$", r"$\bar{y}(\lambda)$", r"$\bar{z}(\lambda)$"]
cols = [H.RED, H.GREEN, H.BLUE]

ax = axes[0]
for k in range(3):
    cur = cm[:, :, k]
    cur = cur / cur.max(axis=1, keepdims=True)
    med = np.median(cur, axis=0)
    lo = np.percentile(cur, 5, axis=0)
    hi = np.percentile(cur, 95, axis=0)
    ax.fill_between(lam, lo, hi, color=cols[k], alpha=0.15, lw=0)
    ax.plot(lam, med, color=cols[k], lw=1.8, label=labels[k])
ax.plot(lam, OM.CMF_STD[:, 1] / OM.CMF_STD[:, 1].max(), "k--", lw=1.0,
        label="标准观察者 $\\bar{y}$")
ax.set_xlim(380, 780)
ax.set_ylim(0, 1.55)
ax.set_xlabel("波长（nm）")
ax.set_ylabel("归一化后的色匹配函数")
ax.legend(loc="upper right", fontsize=8.5, handlelength=1.6)

ax = axes[1]
for k in range(3):
    cur = cm[:, :, k]
    cur = cur / cur.max(axis=1, keepdims=True)
    med = np.median(cur, axis=0)
    lo = np.percentile(cur, 5, axis=0)
    hi = np.percentile(cur, 95, axis=0)
    rel = (hi - lo) / med.max() * 100.0
    ker = np.ones(25) / 25.0
    rel = np.convolve(np.pad(rel, 12, mode="edge"), ker, mode="valid")
    ax.plot(lam, rel, color=cols[k], lw=1.7, label=labels[k])
    i = int(np.argmax(np.where(lam > 410, rel, 0)))
    print(f"{k}: peak {rel[i]:.0f}% at {lam[i]:.0f} nm, at450 {rel[70]:.0f}%,"
          f" at550 {rel[170]:.0f}%")
ax.set_xlim(400, 700)
ax.set_ylim(0, 26)
ax.set_xlabel("波长（nm）")
ax.set_ylabel("5%–95% 宽度（占峰值的百分比）")
ax.legend(loc="upper right", fontsize=8.5, handlelength=1.6)

H.save(fig, 9, "f4_observer_cmf_band")
