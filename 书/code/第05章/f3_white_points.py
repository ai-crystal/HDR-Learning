# -*- coding: utf-8 -*-
"""第 05 章 图 3：白点位置 —— D65 与 DCI 白点差别在哪。

左：色度图放大区，画出黑体轨迹与日光轨迹，标出 D65 / DCI / D50 与等能白点。
右：同一张纯白在三种白点下的实际观感，以及把色偏差放大约 6 倍后的示意。
"""
import sys
sys.path.insert(0, "E:/Study/HDR-Learning/书/code/common")
sys.path.insert(0, "E:/Study/HDR-Learning/书/code/第04章")
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import Rectangle
import hdrfig as H
import cie1931 as C

plt = H.plt

SRGB_FROM_XYZ = np.array([
    [3.2409699419045226, -1.5373831775700940, -0.4986107602930034],
    [-0.9692436362808796, 1.8759675015077202, 0.0415550574071756],
    [0.0556300796969937, -0.2039769588889765, 1.0569715142428786]])

WHITES = {
    "D75": (0.2990, 0.3149),
    "D65": (0.3127, 0.3290),
    "D55": (0.3324, 0.3474),
    "D50": (0.3457, 0.3585),
    "DCI": (0.3140, 0.3510),
    "E": (1 / 3, 1 / 3),
}
D65, DCI = WHITES["D65"], WHITES["DCI"]


def planck_xy(T):
    T = np.asarray(T, dtype=float)
    x = np.where(T <= 4000,
                 -0.2661239e9 / T ** 3 - 0.2343589e6 / T ** 2 + 0.8776956e3 / T + 0.179910,
                 -3.0258469e9 / T ** 3 + 2.1070379e6 / T ** 2 + 0.2226347e3 / T + 0.240390)
    lo, mid, hi = T <= 2222, (T > 2222) & (T <= 4000), T > 4000
    y = np.empty_like(x)
    y[lo] = -1.1063814 * x[lo] ** 3 - 1.34811020 * x[lo] ** 2 + 2.18555832 * x[lo] - 0.20219683
    y[mid] = -0.9549476 * x[mid] ** 3 - 1.37418593 * x[mid] ** 2 + 2.09137015 * x[mid] - 0.16748867
    y[hi] = 3.0817580 * x[hi] ** 3 - 5.87338670 * x[hi] ** 2 + 3.75112997 * x[hi] - 0.37001483
    return x, y


def daylight_xy(T):
    T = np.asarray(T, dtype=float)
    x = np.where(T <= 7000,
                 -4.6070e9 / T ** 3 + 2.9678e6 / T ** 2 + 0.09911e3 / T + 0.244063,
                 -2.0064e9 / T ** 3 + 1.9018e6 / T ** 2 + 0.24748e3 / T + 0.237040)
    return x, -3.000 * x ** 2 + 2.870 * x - 0.275


def white_rgb(x, y, level=0.90, amp=1.0, ref=D65):
    """把白点坐标渲染成一块近似“白”的色块；amp>1 时放大相对参考白点的偏差。"""
    if amp != 1.0:
        x = ref[0] + amp * (x - ref[0])
        y = ref[1] + amp * (y - ref[1])
    rgb = np.clip(np.asarray(C.xy_to_srgb01(x, y, 1.0), dtype=float), 0.0, 1.0)
    m = max(rgb.max(), 1e-6)
    return np.clip(rgb / m * level, 0.0, 1.0)


LAM, LX, LY = C.spectral_locus()


def draw_chroma_bg(ax, xlim, ylim, n=700):
    xs = np.linspace(xlim[0], xlim[1], n)
    ys = np.linspace(ylim[0], ylim[1], n)
    XX, YY = np.meshgrid(xs, ys)
    Yp = np.maximum(YY, 1e-6)
    XYZ = np.stack([XX / Yp, np.ones_like(XX), (1.0 - XX - YY) / Yp], axis=-1)
    with np.errstate(invalid="ignore", divide="ignore"):
        lin = XYZ @ SRGB_FROM_XYZ.T
    lin = np.clip(np.nan_to_num(lin), 0.0, 1.0)
    img = H.srgb_oetf(lin) * 0.86 + 0.14
    pts = np.column_stack([XX.ravel(), YY.ravel()])
    path = Path(np.column_stack([np.append(LX, LX[0]), np.append(LY, LY[0])]))
    inside = path.contains_points(pts).reshape(XX.shape) & (YY > 1e-4)
    img = np.dstack([img, np.where(inside, 1.0, 0.0)])
    ax.imshow(img, extent=[xlim[0], xlim[1], ylim[0], ylim[1]], origin="lower",
              aspect="auto", zorder=-1, interpolation="bilinear")


fig = plt.figure(figsize=(7.2, 5.0))
gs = fig.add_gridspec(1, 2, width_ratios=[1.32, 1.0], wspace=0.26,
                      left=0.075, right=0.985, top=0.80, bottom=0.115)

# ================= 左：白点位置 =================
axL = fig.add_subplot(gs[0, 0])
XLIM, YLIM = (0.238, 0.472), (0.238, 0.452)
axL.set_axisbelow(True)
for gl in axL.get_xgridlines() + axL.get_ygridlines():
    gl.set_zorder(-5)
draw_chroma_bg(axL, XLIM, YLIM)

Tp = np.linspace(2800, 25000, 400)
px, py = planck_xy(Tp)
axL.plot(px, py, color="#5c6672", lw=1.9, zorder=3, label="黑体轨迹（色温线）")
dx, dy = daylight_xy(np.linspace(4000, 25000, 400))
axL.plot(dx, dy, color=H.GOLD, lw=1.9, ls="--", zorder=3,
         label="日光轨迹（CIE D 系列）")
for T in [3000, 4000, 5000, 6500, 10000, 20000]:
    tx, ty = planck_xy(np.array([T]))
    axL.plot([tx[0]], [ty[0]], "o", ms=3.4, color="#48525e", zorder=5)
    axL.text(tx[0] + 0.0040, ty[0] - 0.0110, f"{T} K", fontsize=7.0,
             color="#48525e", ha="left", va="top", zorder=5)

axL.plot([D65[0]], [D65[1]], marker="*", ms=17, color="white", mec="#2b2b2b",
         mew=1.1, zorder=9, label="D65　(0.3127, 0.3290)　6504 K")
axL.plot([DCI[0]], [DCI[1]], marker="*", ms=14, color=H.GOLD, mec="#2b2b2b",
         mew=1.0, zorder=9, label="DCI 白点　(0.3140, 0.3510)　≈6300 K")
axL.plot([WHITES["D50"][0]], [WHITES["D50"][1]], marker="s", ms=7.5, color=H.TEAL,
         mec="white", mew=1.0, zorder=9, label="D50　(0.3457, 0.3585)　5003 K")
axL.plot([WHITES["E"][0]], [WHITES["E"][1]], marker="P", ms=6, color=H.PURPLE,
         mec="white", mew=0.9, zorder=9, label="E 等能白点　(0.333, 0.333)")

axL.plot([D65[0], DCI[0]], [D65[1], DCI[1]], color=H.RED, lw=1.6, ls=":",
         zorder=7)
axL.annotate("", xy=DCI, xytext=D65,
             arrowprops=dict(arrowstyle="<->", color=H.RED, lw=1.5), zorder=10)
axL.text(0.3020, 0.3370, "Δy = 0.022\n同一张纯白，\n影院端更暖、略偏绿", fontsize=7.2,
         color=H.RED, ha="right", va="center", zorder=10, linespacing=1.5,
         bbox=dict(boxstyle="round,pad=0.24", fc="white", ec=H.RED,
                   alpha=0.92, lw=0.8))

axL.text(0.3980, 0.3290, "黑体轨迹", fontsize=7.2, color="#4a5560",
         ha="left", va="center", zorder=9, rotation=-25)
axL.text(0.2955, 0.2955, "日光轨迹", fontsize=7.2, color="#8a6d1f",
         ha="left", va="center", zorder=9, rotation=-22)

axL.set_xlim(*XLIM)
axL.set_ylim(*YLIM)
axL.set_xlabel("色度坐标 x")
axL.set_ylabel("色度坐标 y")
axL.set_title("白点都挤在色度图中心的一小片区域里", fontsize=10.5, pad=8)
axL.legend(loc="lower right", fontsize=7.0, handletextpad=0.5, labelspacing=0.42,
           borderpad=0.5, bbox_to_anchor=(1.005, -0.01))

# ================= 右：白点观感 =================
axR = fig.add_subplot(gs[0, 1])
axR.set_xlim(0, 3.0)
axR.set_ylim(0, 3.0)
axR.axis("off")

COLS = [("D65", D65, "6504 K", "PC / 网页 / 电视"),
        ("DCI 白点", DCI, "≈6300 K", "数字影院"),
        ("D50", WHITES["D50"], "5003 K", "印刷")]

axR.text(0.00, 2.90, "① 同一张“纯白”的实际观感", fontsize=8.8,
         color="#2b3540", fontweight="bold", ha="left", va="center")
axR.text(0.00, 1.46, "② 相对 D65 的色偏差放大约 6 倍（示意见往哪偏）", fontsize=8.8,
         color="#2b3540", fontweight="bold", ha="left", va="center")

for i, (name, xy, cct, use) in enumerate(COLS):
    x0 = i * 1.0 + 0.05
    c1 = white_rgb(*xy, level=0.90, amp=1.0)
    c2 = white_rgb(*xy, level=0.90, amp=6.0)
    axR.add_patch(Rectangle((x0, 1.84), 0.90, 0.48, facecolor=c1,
                            edgecolor="#b9c2cc", lw=0.8, zorder=3))
    axR.add_patch(Rectangle((x0, 0.92), 0.90, 0.48, facecolor=c2,
                            edgecolor="#b9c2cc", lw=0.8, zorder=3))
    hexc = "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in c2)
    axR.text(x0 + 0.45, 2.70, name, fontsize=8.6, ha="center", va="center",
             fontweight="bold", color="#2b3540")
    axR.text(x0 + 0.45, 2.56, cct, fontsize=7.4, ha="center", va="center",
             color=H.GRAY)
    axR.text(x0 + 0.45, 2.42, use, fontsize=7.2, ha="center", va="center",
             color="#3b4450")
    axR.text(x0 + 0.45, 0.80, hexc, fontsize=7.0, ha="center", va="center",
             color=H.GRAY, family="monospace")

axR.text(1.50, 1.68, "三块看起来几乎一模一样 —— 肉眼不留心根本分不出来",
         fontsize=7.4, ha="center", va="center", color="#3b4450")
axR.text(1.50, 0.66, "放大后：DCI 白点偏绿（y 更高）且更暖；D50 偏黄",
         fontsize=7.4, ha="center", va="center", color="#3b4450")

axR.text(0.00, 0.50,
         "白点不一致 = 整幅画面偏色：D65 设备上的“纯白”搬到 DCI 白点设备上就不再是白。\n"
         "所以专业流程必须对齐白点：网页 / PC / 电视 = D65，数字影院 = DCI 白点，印刷 = D50。\n"
         "Display P3 把白点从 DCI 换回 D65，正是为了在与 sRGB 混用的环境里不偏色。",
         fontsize=7.3, color="#3b4450", ha="left", va="top", linespacing=1.75)

fig.suptitle("白点：同样是“白”，标准却不止一个", fontsize=11.5,
             fontweight="bold", y=0.95)

H.save(fig, 5, "f3_white_points")
print("D65", D65, "DCI", DCI)
print("daylight(6504) =", tuple(np.round(daylight_xy(np.array([6504.0])), 4)))
print("DCI swatch RGB=", np.round(white_rgb(*DCI), 3),
      " D50 swatch RGB=", np.round(white_rgb(*WHITES["D50"]), 3))
