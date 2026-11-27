# -*- coding: utf-8 -*-
"""第 11 章 图 2：BT.2446 三类方法的映射形状。

(a) 三种方法把 0.005–4000 nit 的 HDR 亮度送到 0–100 IRE 的 SDR，另画一条直接截断作参照。
    方法 A 按 203 cd/m2 的参考白定标，漫反射白落在约 87 IRE，再往上走肩部；
    方法 C 把膝点提前，肩部更陡，同样的漫反射白落在 85 IRE 上下，高光纹理多一点；
    方法 B 在 PQ 域用一个二次多项式逐帧拟合，暗部被抬起是二次项本身的代价。
(b) 肩部放大。三条曲线在漫反射白附近相差约 6 IRE，整幅画面的明暗手感就定在这段。
(c) 方法 B 的二次系数随帧统计量变化。同一个 50 nit 在三场里落到不同高度，
    这是自适应带来的好处，也是剪接点上亮度跳动的来源。
曲线按各方法的处理结构构造，用于比较形状。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/books/common")
import numpy as np
import hdrfig as H

H.set_book("hdr-tech")
plt = H.plt

x = np.logspace(np.log10(0.005), np.log10(4000), 700)


def ire(lin):
    """显示线性 0..1 -> BT.1886 编码后的 IRE。"""
    return 100.0 * np.clip(lin, 0, 1) ** (1 / 2.4)


def tone(t, knee, k_mid, gamma):
    """膝点以下按线性比例，膝点以上按对数肩部升到 4000 nit 的白。
    两段在膝点处取值相等（k_mid），肩部起点斜率较大，随后逐渐放平。"""
    lo = (t / knee) * k_mid
    hi = k_mid + (1 - k_mid) * (np.log10(np.maximum(t, knee) / knee)
                                / np.log10(4000.0 / knee)) ** gamma
    return ire(np.where(t <= knee, lo, hi))


def quad_from_anchors(xmin, xmid, xmax, smin=0.02, smid=0.74, smax=1.0):
    ex = H.pq_oetf(np.array([xmin, xmid, xmax], dtype=float))
    Amat = np.vstack([ex ** 2, ex, np.ones(3)]).T
    a, b, c = np.linalg.solve(Amat, np.array([smin, smid, smax]))
    return a, b, c


def method_b(t, coeffs):
    ex = H.pq_oetf(t)
    a, b, c = coeffs
    return 100.0 * np.clip(a * ex ** 2 + b * ex + c, 0, 1)


CB = quad_from_anchors(0.02, 100.0, 4000.0)
A = tone(x, 203.0, 0.72, 0.80)
B = method_b(x, CB)
C = tone(x, 150.0, 0.66, 1.25)
CLIP = ire(np.clip(x / 203.0, 0, 1))

fig, (ax1, ax2, ax3) = plt.subplots(
    1, 3, figsize=(9.0, 3.75),
    gridspec_kw={"width_ratios": [1.16, 0.90, 0.96]})
fig.subplots_adjust(left=0.062, right=0.988, bottom=0.155, top=0.95, wspace=0.34)

# ---------------- (a) 全范围 ----------------
ax1.semilogx(x, CLIP, color=H.LGRAY, lw=1.7, ls=(0, (4, 2)), label="直接截断")
ax1.semilogx(x, A, color=H.NAVY, lw=2.3, label="方法 A　场景光 + 肩部")
ax1.semilogx(x, B, color=H.ORANGE, lw=2.3, label="方法 B　PQ 域二次拟合")
ax1.semilogx(x, C, color=H.TEAL, lw=2.3, label="方法 C　混合")

ax1.axvline(203, color="#9aa7b4", lw=0.9, ls=":")
ax1.text(230, 30, "203 nit\n参考白", fontsize=7.0, color="#5b6b7c", ha="left", va="bottom")
ax1.annotate("暗部被抬起\n是二次项的代价", xy=(2.0, float(method_b(2.0, CB))), xytext=(0.006, 52),
             fontsize=7.2, color=H.ORANGE, ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color=H.ORANGE, lw=1.0,
                             connectionstyle="arc3,rad=0.22"))
ax1.set_xlim(0.005, 4000)
ax1.set_ylim(0, 106)
ax1.set_xlabel("输入亮度（cd/m2，HDR 母版）", fontsize=9.5)
ax1.set_ylabel("SDR 输出（IRE）", fontsize=9.5)
ax1.set_xticks([0.01, 0.1, 1, 10, 100, 1000])
ax1.set_xticklabels(["0.01", "0.1", "1", "10", "100", "1000"])
ax1.legend(loc="lower right", fontsize=7.4, borderpad=0.45, labelspacing=0.35)
ax1.text(0.0075, 90, "(a)", fontsize=10, fontweight="bold", color=H.DARK)

# ---------------- (b) 肩部放大 ----------------
m = x >= 120
ax2.semilogx(x[m], A[m], color=H.NAVY, lw=2.4, label="A")
ax2.semilogx(x[m], B[m], color=H.ORANGE, lw=2.4, label="B")
ax2.semilogx(x[m], C[m], color=H.TEAL, lw=2.4, label="C")
ax2.set_xlim(120, 4000)
ax2.set_ylim(72, 101)
ax2.set_xticks([150, 300, 600, 1200, 2400, 4000])
ax2.set_xticklabels(["150", "300", "600", "1200", "2400", "4000"])
ax2.set_xlabel("输入亮度（cd/m2）", fontsize=9.5)
ax2.set_ylabel("SDR 输出（IRE）", fontsize=9.5)
ax2.legend(loc="upper left", fontsize=8.0, borderpad=0.45, labelspacing=0.35)
ax2.annotate("漫反射白附近\n三条约差 6 IRE",
             xy=(250, float(method_b(250.0, CB))), xytext=(660, 74.6),
             fontsize=7.2, color="#40505f", ha="left", va="center",
             arrowprops=dict(arrowstyle="->", color="#7f8c8d", lw=0.9,
                             connectionstyle="arc3,rad=0.22"))
ax2.text(128, 98.5, "(b)", fontsize=10, fontweight="bold", color=H.DARK)

# ---------------- (c) 逐帧拟合 ----------------
SCENES = [
    ("夜景　0.002 / 6 / 120", (0.002, 6.0, 120.0), H.PURPLE),
    ("日景　0.3 / 250 / 4000", (0.3, 250.0, 4000.0), H.GREEN),
    ("室内　1 / 60 / 600", (1.0, 60.0, 600.0), H.RED),
]
vals = []
for k, (name, (lo, mid, hi), c) in enumerate(SCENES):
    cf = quad_from_anchors(lo, mid, hi)
    xs = np.logspace(np.log10(lo), np.log10(hi), 600)
    ax3.semilogx(xs, method_b(xs, cf), color=c, lw=2.2, label=name)
    v50 = float(np.interp(50, xs, method_b(xs, cf)))
    vals.append(v50)
    ax3.plot([50], [v50], "o", ms=5.5, color=c, mec="white", mew=1.0, zorder=6)
    if k == 0:                       # 夜景这一段画到范围外，示意外推会反折
        xe = np.logspace(np.log10(120), np.log10(3000), 200)
        ax3.semilogx(xe, method_b(xe, cf), color=c, lw=1.3, ls=(0, (3, 2)), alpha=0.55)

ax3.axvline(50, color="#b7c1cc", lw=0.9, ls=":")
ax3.text(3600, 38, "同一个 50 nit\n落在不同高度",
         fontsize=7.2, color="#40505f", ha="right", va="center", linespacing=1.5)

ax3.set_xlim(0.005, 4000)
ax3.set_ylim(0, 106)
ax3.set_xlabel("输入亮度（cd/m2）", fontsize=9.5)
ax3.set_ylabel("SDR 输出（IRE）", fontsize=9.5)
ax3.set_xticks([0.01, 0.1, 1, 10, 100, 1000])
ax3.set_xticklabels(["0.01", "0.1", "1", "10", "100", "1000"])
ax3.legend(loc="upper left", fontsize=7.0, borderpad=0.45, labelspacing=0.35)
ax3.text(1000, 8, "(c)", fontsize=10, fontweight="bold", color=H.DARK)

print("100/203/1000/4000:", [round(float(np.interp(t, x, v)), 1)
                              for t in (100, 203, 1000, 4000) for v in (A, B, C)])
print("50 nit per scene", [round(v, 1) for v in vals])
print("coef main", np.round(CB, 3))

H.save(fig, 11, "f2_bt2446_curves")
