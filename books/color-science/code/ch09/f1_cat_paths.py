# -*- coding: utf-8 -*-
"""图 9-1　四组色适应变换对同一组刺激的预测差异（A 光源 -> D65）。"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import observer_model as OM
plt = H.plt

uA, vA = OM.xyz_to_uv(*OM.A_WH)
uD, vD = OM.xyz_to_uv(*OM.D65)

angs = np.arange(0, 360, 30.0)
rad = 0.035
us = uA + rad * np.cos(np.deg2rad(angs))
vs = vA + rad * np.sin(np.deg2rad(angs))
den = 6.0 * us - 16.0 * vs + 12.0
xs = 9.0 * us / den
ys = 4.0 * vs / den
src = OM.xy_to_xyz(xs, ys, 0.2)

res = {}
for name, M in OM.CATS.items():
    res[name] = OM.apply_cat(src, M, OM.A_WH, OM.D65, D=1.0)

brdf = res["Bradford"]


def duvset(xyz):
    u, v = OM.xyz_to_uv(xyz[:, 0], xyz[:, 1], xyz[:, 2])
    return np.stack([u, v], axis=1)


p_src = duvset(src)
p_bfd = duvset(brdf)

print("== 每个 CAT 相对 Bradford 的 u'v' 偏差 ==")
for name in OM.CATS:
    p = duvset(res[name])
    d = np.hypot(p[:, 0] - p_bfd[:, 0], p[:, 1] - p_bfd[:, 1])
    print(f"{name:12s} mean={d.mean():.4f} max={d.max():.4f}")

p_xyz = duvset(OM.apply_cat(src, np.eye(3), OM.A_WH, OM.D65, D=1.0))
d = np.hypot(p_xyz[:, 0] - p_bfd[:, 0], p_xyz[:, 1] - p_bfd[:, 1])
print(f"{'XYZ-scal':12s} mean={d.mean():.4f} max={d.max():.4f}")
print("src u range", p_src[:, 0].min(), p_src[:, 0].max())
print("bfd u range", p_bfd[:, 0].min(), p_bfd[:, 0].max())
print("bfd v range", p_bfd[:, 1].min(), p_bfd[:, 1].max())

fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.0),
                         gridspec_kw=dict(wspace=0.32, width_ratios=[1.05, 1.0]))
fig.subplots_adjust(bottom=0.24)

ax = axes[0]
for i in range(len(src)):
    ax.annotate("", xy=(p_bfd[i, 0], p_bfd[i, 1]),
                xytext=(p_src[i, 0], p_src[i, 1]),
                arrowprops=dict(arrowstyle="->", color="#b9c2cc", lw=0.9,
                                shrinkA=0, shrinkB=2))
h, = ax.plot(np.r_[p_src[:, 0], p_src[0, 0]], np.r_[p_src[:, 1], p_src[0, 1]],
             "--", color=H.GRAY, lw=1.0, label="适应前（A）")
handles = [h]
cols = {"Bradford": H.NAVY, "CAT02": H.ORANGE, "CAT16": H.RED,
        "CMCCAT2000": H.TEAL}
for name, c in cols.items():
    p = duvset(res[name])
    ln, = ax.plot(np.r_[p[:, 0], p[0, 0]], np.r_[p[:, 1], p[0, 1]],
                  "-o", color=c, ms=3.2, lw=1.4, label=name)
    handles.append(ln)
ax.plot([uA], [vA], "s", color=H.GRAY, ms=5)
ax.plot([uD], [vD], "s", color=H.DARK, ms=5)
ax.annotate("A 白", (uA, vA), textcoords="offset points", xytext=(6, 4),
            fontsize=8.5, color=H.GRAY)
ax.annotate("D65 白", (uD, vD), textcoords="offset points", xytext=(6, 4),
            fontsize=8.5, color=H.DARK)
ax.set_xlabel("$u'$")
ax.set_ylabel("$v'$")
ax.set_xlim(0.135, 0.325)
ax.set_ylim(0.355, 0.605)

ax = axes[1]
order = ["CAT02", "CMCCAT2000", "CAT16"]
for name, c in zip(order, [H.ORANGE, H.TEAL, H.RED]):
    p = duvset(res[name])
    d = np.hypot(p[:, 0] - p_bfd[:, 0], p[:, 1] - p_bfd[:, 1])
    ax.plot(np.r_[angs, 360], np.r_[d, d[0]], "-o", color=c, ms=3.2, lw=1.4,
            label=name)
d = np.hypot(p_xyz[:, 0] - p_bfd[:, 0], p_xyz[:, 1] - p_bfd[:, 1])
ax.plot(np.r_[angs, 360], np.r_[d, d[0]], "-s", color=H.GRAY, ms=3.0, lw=1.1,
        label="XYZ 直接缩放")
ax.set_xlabel("刺激在 $u'v'$ 平面上的方位角（度）")
ax.set_ylabel("相对 Bradford 的 $\\Delta u'v'$")
ax.set_xlim(0, 360)
ax.set_xticks([0, 90, 180, 270, 360])
ax.set_ylim(0, 0.030)
ax.legend(loc="upper right", fontsize=8, ncol=1)

fig.legend(handles=handles, loc="lower center", ncol=5, fontsize=8.5,
           bbox_to_anchor=(0.5, 0.005), frameon=False)
H.save(fig, 9, "f1_cat_paths")
