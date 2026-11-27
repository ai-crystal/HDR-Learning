# -*- coding: utf-8 -*-
"""图 9-6　晶状体黄化对短波透过率与窄带蓝原色亮度的影响。"""
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


fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.9),
                         gridspec_kw=dict(wspace=0.29, width_ratios=[1.15, 1.0]))
fig.subplots_adjust(bottom=0.26)

ax = axes[0]
ref = OM.lens_trans(OM.REF_AGE)
for age, c, ls in [(20, H.BLUE, "-"), (32, H.GRAY, "--"), (50, H.ORANGE, "-"),
                   (70, H.RED, "-")]:
    t = OM.lens_trans(age) / ref
    ax.plot(lam, t, color=c, lw=1.7, ls=ls, label=f"{age} 岁")
ax.axhline(1.0, color=H.LGRAY, lw=0.9)
ax.axvline(450, color=H.GRAY, ls=":", lw=1.0)
ax.annotate("450 nm", (452, 0.42), fontsize=7.8, color="#6b7887")
for age, c in [(20, H.BLUE), (70, H.RED)]:
    t = OM.lens_trans(age) / ref
    ax.plot([450], [t[70]], "o", color=c, ms=5, mfc="white", mew=1.4)
    print(f"{age} 岁 450 nm 相对透过率 {t[70]:.3f}")
ax.set_xlim(385, 720)
ax.set_ylim(0, 2.15)
ax.set_xlabel("波长（nm）")
ax.set_ylabel("相对 32 岁的晶状体透过率")
ax.legend(loc="upper right", fontsize=8.5, title="观察者年龄", title_fontsize=8.5)

ax = axes[1]
blue = gauss(465, 2)
red = gauss(638, 2)
ages = np.arange(20, 76, 1)
ratio = []
for a in ages:
    c = OM.observer_cmf(a, OM.REF_OD, 0, 0)
    ratio.append((blue @ c[:, 1]) / (red @ c[:, 1]))
ratio = np.array(ratio)
ax.plot(ages, ratio, color=H.NAVY, lw=1.9)
for a in (20, 32, 50, 70):
    i = a - 20
    ax.plot([a], [ratio[i]], "o", color=H.NAVY, ms=5, mfc="white", mew=1.4)
    ax.annotate(f"{ratio[i]:.3f}", (a, ratio[i]), textcoords="offset points",
                xytext=(6 if a == 20 else 0, -14), fontsize=7.8, color=H.DARK,
                ha="left" if a == 20 else "center")
    print(f"{a} 岁：Y(465)/Y(638) = {ratio[i]:.3f}")
ax.set_xlim(18, 77)
ax.set_ylim(0.22, 0.44)
ax.set_xlabel("观察者年龄（岁）")
ax.set_ylabel("蓝原色与红原色的亮度比")
ax.annotate(f"从 32 岁到 70 岁下降 {100*(1-ratio[50]/ratio[12]):.0f}%",
            (0.35, 0.86), xycoords="axes fraction", fontsize=8.5, color=H.RED)

H.save(fig, 9, "f5_age_lens")
