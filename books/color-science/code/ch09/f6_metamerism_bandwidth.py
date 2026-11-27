# -*- coding: utf-8 -*-
"""图 9-4　三种原色技术的白场光谱与观察者同色异谱的累积分布。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import observer_model as OM
plt = H.plt

lam = OM.LAM


def gauss(c, fwhm):
    s = fwhm / 2.3548
    return np.exp(-0.5 * ((lam - c) / s) ** 2)


def rgb_spd(spec):
    """三个原色的 SPD（列为 R,G,B），权重解到标准观察者下恰好合成 D65 白。"""
    G = np.stack([gauss(c, f) for c, f in spec], axis=1)
    T = G.T @ OM.CMF_STD
    w = np.linalg.solve(T.T, OM.D65)
    return G * w


def planck(T):
    l = lam * 1e-9
    c2 = 1.4388e-2
    return 1.0 / (l ** 5 * (np.exp(c2 / (l * T)) - 1.0))


# 日光型参考光源：黑体 6500 K 加二次倾斜项，调到与 D65 三刺激值一致
ref = planck(6500)
ref = ref / ref.max()
a = np.linspace(-1, 1, len(lam))
for _ in range(4):
    B = np.stack([ref, ref * a, ref * a * a], axis=1)
    c = np.linalg.solve(OM.CMF_STD.T @ B, OM.D65)
    ref = np.clip(B @ c, 0, None)
print("参考光源 XYZ", np.round(ref @ OM.CMF_STD, 4))

tech = [("激光 2 nm", [(638, 2), (532, 2), (465, 2)], H.RED),
        ("量子点 22–28 nm", [(630, 28), (530, 28), (448, 22)], H.TEAL),
        ("荧光粉 LED 20–60 nm", [(615, 30), (545, 60), (450, 20)], H.NAVY)]

rng = np.random.default_rng(5)
N = 200
ages = rng.uniform(20, 70, N)
macs = rng.uniform(0.30, 0.45, N)
ls = rng.uniform(-2, 2, N)
ms = rng.uniform(-1.5, 1.5, N)
cms = [OM.observer_cmf(ages[i], macs[i], ls[i], ms[i]) for i in range(N)]


def uv(X):
    X, Y, Z = X
    d = X + 15.0 * Y + 3.0 * Z
    return np.array([4.0 * X / d, 9.0 * Y / d])


fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.9),
                         gridspec_kw=dict(wspace=0.27, width_ratios=[1.15, 1.0]))
fig.subplots_adjust(bottom=0.26)

ax = axes[0]
ax.fill_between(lam, 0, ref / ref.max(), color="#cfd6de", lw=0, alpha=0.9,
                label="日光型参考光源")
for name, spec, c in tech:
    G = rgb_spd(spec)
    w = G.sum(1)
    ax.plot(lam, w / w.max(), color=c, lw=1.5, label=name)
ax.set_xlim(380, 700)
ax.set_ylim(0, 1.60)
ax.set_xlabel("波长（nm）")
ax.set_ylabel("归一化后的光谱功率")
ax.legend(loc="upper center", fontsize=7.8, ncol=2, handlelength=1.5,
          columnspacing=1.0)

ax = axes[1]
for name, spec, c in tech:
    G = rgb_spd(spec)
    w = G.sum(1)
    d = np.array([np.hypot(*(uv(w @ cm) - uv(ref @ cm))) for cm in cms])
    d = np.sort(d)
    p = np.arange(1, len(d) + 1) / len(d)
    ax.plot(d, p * 100, color=c, lw=1.8, label=name)
    p95 = np.percentile(d, 95)
    print(f"{name:22s} median {np.median(d):.4f}  p95 {p95:.4f}  max {d.max():.4f}")
    ax.plot([p95], [95], "o", color=c, ms=4.5)
ax.axhline(95, color=H.GRAY, ls=":", lw=1.0)
ax.text(0.0004, 97.5, "95%", fontsize=8, color=H.GRAY, ha="left")
ax.set_xlim(0, 0.0135)
ax.set_ylim(0, 103)
ax.set_xlabel("与参考光源白的 $\\Delta u'v'$")
ax.set_ylabel("观察者累积比例（%）")
ax.legend(loc="lower right", fontsize=7.8, handlelength=1.5)

H.save(fig, 9, "f6_metamerism_bandwidth")
