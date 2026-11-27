# -*- coding: utf-8 -*-
"""第 01 章 图 7：三刺激值相同的反射率族，以及由此产生的同色异谱色差。

(a) 四条反射率曲线在光源 A（2856 K 黑体）下三刺激值完全相同：基准曲线 ρ0 加上
    两条"同色异谱黑"光谱的倍数，再把残余三刺激值精确补回，所以 X、Y、Z 的
    相对偏差 < 1e-10。
    同色异谱黑由 Gram-Schmidt 构造：从平滑的钟形函数出发，减掉它在三条色匹配
    函数加权子空间里的分量，剩下的部分对任何照明都不产生三刺激值。
(b) 换到 6500 K 黑体照明后，四条曲线开始分家，画出的 ΔE*ab 就是同色异谱色差，
    工业上叫同色异谱指数（改用 D65 与 A 的组合即 CIE 15 给出的定义）。
"""
import sys, os
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import hdrfig as H
H.set_book("color-science")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cie1931 as C

plt = H.plt

lam = np.arange(380.0, 781.0, 1.0)
XB = np.interp(lam, C.LAM, C.XBAR)
YB = np.interp(lam, C.LAM, C.YBAR)
ZB = np.interp(lam, C.LAM, C.ZBAR)
A = np.stack([XB, YB, ZB])                     # 3×N
C2 = 1.4388e-2


def planck(T, lam_nm=lam):
    l = lam_nm * 1e-9
    return 1.0 / (l ** 5 * (np.exp(C2 / (l * T)) - 1.0))


S_A = planck(2856.0)
S_B = planck(6500.0)
WA = A * S_A[None, :]
WB = A * S_B[None, :]

PWA = WA.T @ np.linalg.inv(WA @ WA.T) @ WA        # 到"照明 A 下有色响应"子空间的投影


def to_xyz(w, rho):
    return w @ rho


def metameric_black(f, basis):
    """把 f 投影到零空间：先减掉有色分量，再与已有零空间基正交。"""
    g = f - PWA @ f
    for b in basis:
        g = g - (g @ b) / (b @ b) * b
    return g / np.abs(g).max()


def gauss(cen, sig):
    return np.exp(-0.5 * ((lam - cen) / sig) ** 2)


b1 = metameric_black(gauss(455.0, 38.0), [])
b2 = metameric_black(gauss(625.0, 45.0), [b1])

rho0 = 0.06 + 0.30 * gauss(450.0, 55.0) + 0.42 * gauss(640.0, 90.0)
rho0 = np.clip(rho0, 0.0, 1.0)
XYZ_T = to_xyz(WA, rho0)


def make_partner(t1, t2):
    r = rho0 + t1 * b1 + t2 * b2
    r = np.clip(r, 0.0, 1.0)
    r = r + WA.T @ np.linalg.solve(WA @ WA.T, XYZ_T - to_xyz(WA, r))
    r = np.clip(r, 0.0, 1.0)
    r = r + WA.T @ np.linalg.solve(WA @ WA.T, XYZ_T - to_xyz(WA, r))
    return r


PARTNERS = [
    ("ρ1", make_partner(0.20, 0.13), H.ORANGE),
    ("ρ2", make_partner(-0.24, 0.09), H.TEAL),
    ("ρ3", make_partner(0.15, -0.21), H.PURPLE),
]

# ---------------- 色差（CIE76，在 6500 K 黑体下，参考白取理想漫反射体） ----------------
XN, YN, ZN = to_xyz(WB, np.ones_like(lam))


def lab(w, rho):
    X, Y, Z = to_xyz(w, rho)

    def f(t):
        d = 6.0 / 29.0
        return np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4.0 / 29.0)

    fx, fy, fz = f(X / XN), f(Y / YN), f(Z / ZN)
    return np.array([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)])


lab0_B = lab(WB, rho0)
bars = []
for name, r, col in PARTNERS:
    bars.append((name, float(np.linalg.norm(lab(WB, r) - lab0_B)), col))

fig = plt.figure(figsize=(7.2, 4.3))
gs = fig.add_gridspec(1, 2, width_ratios=[1.55, 1.0], wspace=0.30)

# ==================== (a) 反射率族 ====================
ax = fig.add_subplot(gs[0])
ax.plot(lam, rho0, color=H.NAVY, lw=2.4, label="ρ0（基准）")
for name, r, col in PARTNERS:
    ax.plot(lam, r, color=col, lw=1.7, label=name)
ax.set_xlim(380, 780)
ax.set_ylim(0, 0.72)
ax.set_xticks([400, 450, 500, 550, 600, 650, 700, 750])
ax.set_xlabel("波长 λ（nm）")
ax.set_ylabel("光谱反射率 ρ(λ)")
ax.set_title("(a) 光源 A 下三刺激值相同", fontsize=9.5, pad=6)
ax.legend(loc="upper left", fontsize=7.6, ncol=2, frameon=True,
          handlelength=1.6, columnspacing=1.2, labelspacing=0.25)
ax.text(688, 0.055, "四条曲线的 XYZ 完全一致\n（相对偏差 < 1e-6）", fontsize=7.4,
        color=H.DARK, ha="center", va="center")

# ==================== (b) 换光源后的色差 ====================
ax2 = fig.add_subplot(gs[1])
names = ["ρ0\n（基准）"] + [b[0] for b in bars]
vals = [0.0] + [b[1] for b in bars]
cols = [H.NAVY] + [b[2] for b in bars]
xo = np.arange(len(vals))
ax2.bar(xo, vals, 0.62, color=cols, edgecolor="#33414f", lw=0.7)
for xi, v in zip(xo, vals):
    if v > 0.02:
        ax2.text(xi, v + 0.12, f"{v:.2f}", ha="center", va="bottom",
                 fontsize=8.0, color="#2c3e50")
ax2.set_xticks(xo)
ax2.set_xticklabels(names, fontsize=8.0)
ax2.set_ylim(0, max(vals) * 1.25)
ax2.set_ylabel("ΔE*ab（改用 6500 K 照明）")
ax2.set_title("(b) 同色异谱引起的色差", fontsize=9.5, pad=6)
ax2.grid(axis="x", visible=False)

H.save(fig, 1, "f7_reconstruction")

print("XYZ_A(rho0) =", np.round(XYZ_T, 6))
for name, r, _ in PARTNERS:
    d = np.abs(to_xyz(WA, r) - XYZ_T) / XYZ_T * 100
    print(f"{name}: XYZ_A rel.err(%) = {np.round(d, 9)}  ΔE*ab(B) = "
          f"{np.linalg.norm(lab(WB, r) - lab0_B):.3f}")
print("reflectance range:", np.round([rho0.min(), rho0.max()], 3))
print("b1 min/max", np.round([b1.min(), b1.max()], 3),
      "b2", np.round([b2.min(), b2.max()], 3))
