# -*- coding: utf-8 -*-
"""第 05 章 图 5：同一串 RGB 码值，在 sRGB 与 Display P3 下的饱和度差异。

上：同一码值分别按 sRGB / Display P3 解释后实际呈现的颜色（转成 sRGB 画出来）。
左下：这些颜色在色度图上的位置与“往外挪”的方向（箭头）。
右下：饱和度渐变条 —— 同一串码值，P3 那一行明显更艳。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
sys.path.insert(0, "E:/Study/HDR技术/书/code/第04章")
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import Rectangle
import hdrfig as H
import cie1931 as C

plt = H.plt

# 线性 RGB -> XYZ（D65）
SRGB_M = np.array([[0.41239079926595934, 0.357584339383878, 0.1804807884018343],
                   [0.21263900587151027, 0.715168678767756, 0.07219231536073371],
                   [0.01933081871559182, 0.11919477979462598, 0.9505321522496607]])
P3_M = np.array([[0.4865709486482162, 0.26566769316909306, 0.1982172852343625],
                 [0.2289745640697488, 0.6917385218365064, 0.079286914093745],
                 [0.0, 0.04511338185890264, 1.043944368900976]])
SRGB_INV = np.linalg.inv(SRGB_M)

SRGB_PRI = np.array([(0.640, 0.330), (0.300, 0.600), (0.150, 0.060)])
P3_PRI = np.array([(0.680, 0.320), (0.265, 0.690), (0.150, 0.060)])

CODES = [((0.86, 0.16, 0.10), "红"),
         ((0.90, 0.52, 0.08), "橙"),
         ((0.22, 0.66, 0.30), "绿"),
         ((0.16, 0.32, 0.80), "蓝"),
         ((0.46, 0.24, 0.66), "紫"),
         ((0.05, 0.60, 0.62), "青")]


def code_hex(code):
    return "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in code)


def xy_of(xyz):
    s = xyz.sum()
    return xyz[0] / s, xyz[1] / s


def render_on_srgb(xyz):
    """把某个 XYZ 颜色转成 sRGB 屏上实际会看到的 RGB（0..1），返回 (rgb, 是否被裁剪)。"""
    lin = SRGB_INV @ np.asarray(xyz, dtype=float)
    clipped = bool(np.any(lin < -0.003) or np.any(lin > 1.003))
    return np.clip(H.srgb_oetf(np.clip(lin, 0.0, 1.0)), 0.0, 1.0), clipped


ROWS = []
for code, name in CODES:
    code = np.array(code, dtype=float)
    xyz_s = SRGB_M @ H.srgb_eotf(code)
    xyz_p = P3_M @ H.srgb_eotf(code)
    rgb_p, clip = render_on_srgb(xyz_p)
    ROWS.append(dict(name=name, cube=code_hex(code),
                     xy_s=xy_of(xyz_s), xy_p=xy_of(xyz_p),
                     disp_s=code.copy(), disp_p=rgb_p, clip=clip))

LAM, LX, LY = C.spectral_locus()


def draw_chroma_bg(ax, xlim, ylim, n=640, blend=0.45):
    xs = np.linspace(xlim[0], xlim[1], n)
    ys = np.linspace(ylim[0], ylim[1], n)
    XX, YY = np.meshgrid(xs, ys)
    Yp = np.maximum(YY, 1e-6)
    XYZ = np.stack([XX / Yp, np.ones_like(XX), (1.0 - XX - YY) / Yp], axis=-1)
    with np.errstate(invalid="ignore", divide="ignore"):
        lin = XYZ @ SRGB_M.T
    lin = np.clip(np.nan_to_num(lin), 0.0, 1.0)
    img = H.srgb_oetf(lin) * (1 - blend) + blend
    pts = np.column_stack([XX.ravel(), YY.ravel()])
    inside = Path(np.column_stack([np.append(LX, LX[0]), np.append(LY, LY[0])])
                  ).contains_points(pts).reshape(XX.shape) & (YY > 1e-4)
    img = np.dstack([img, np.where(inside, 1.0, 0.0)])
    ax.imshow(img, extent=[xlim[0], xlim[1], ylim[0], ylim[1]], origin="lower",
              aspect="auto", zorder=-1, interpolation="bilinear")


fig = plt.figure(figsize=(7.2, 5.7))
gs = fig.add_gridspec(2, 2, height_ratios=[1.10, 1.0], width_ratios=[1.10, 1.0],
                      hspace=0.36, wspace=0.20,
                      left=0.085, right=0.985, top=0.875, bottom=0.075)

# ================= 上：同一码值的两种呈现 =================
axT = fig.add_subplot(gs[0, :])
axT.set_xlim(0, 7.6)
axT.set_ylim(-0.40, 1.36)
axT.axis("off")

W, STEP, X0 = 0.96, 1.02, 1.42
axT.text(0.02, 1.20, "同一串码值 →", fontsize=8.0, color="#2b3540",
         fontweight="bold", ha="left", va="center")
axT.text(0.02, 0.90, "当作\nsRGB 显示", fontsize=8.0, color=H.NAVY,
         fontweight="bold", ha="left", va="center", linespacing=1.5)
axT.text(0.02, 0.25, "当作\nP3 显示", fontsize=8.0, color=H.ORANGE,
         fontweight="bold", ha="left", va="center", linespacing=1.5)

for i, r in enumerate(ROWS):
    x0 = X0 + i * STEP
    axT.text(x0 + W / 2, 1.24, r["cube"], fontsize=7.0, ha="center", va="center",
             color="#2b3540", family="monospace", fontweight="bold")
    axT.text(x0 + W / 2, 1.09, r["name"], fontsize=7.4, ha="center", va="center",
             color=H.GRAY)
    for y0, rgb in [(0.60, r["disp_s"]), (0.02, r["disp_p"])]:
        axT.add_patch(Rectangle((x0, y0), W, 0.42, facecolor=rgb,
                                edgecolor="#b9c2cc", lw=0.8, zorder=3))
        lum = float(np.dot(rgb, [0.2126, 0.7152, 0.0722]))
        axT.text(x0 + W / 2, y0 + 0.21, code_hex(rgb), fontsize=6.6, ha="center",
                 va="center", zorder=5, family="monospace",
                 color="white" if lum < 0.45 else "#2b3540")
    if r["clip"]:
        axT.text(x0 + W / 2, 0.475, "（超出 sRGB，已裁剪）", fontsize=6.3,
                 ha="center", va="center", color=H.RED)
    axT.annotate("", xy=(x0 + W / 2, 0.525), xytext=(x0 + W / 2, 0.585),
                 arrowprops=dict(arrowstyle="->", color=H.GRAY, lw=1.0), zorder=4)

axT.text(X0, -0.16,
         "下面一行 = 同一码值在 Display P3 屏上的真实颜色，再转成 sRGB 画到这里；"
         "两行码值完全相同，颜色却不一样。\n"
         "标红的是超出 sRGB 色域的鲜艳色 —— 在 sRGB 屏上只能裁剪呈现，在 P3 屏上才能原样显示。",
         fontsize=7.2, color="#3b4450", ha="left", va="top", linespacing=1.7)
axT.set_title("同一个 RGB 码值，两种色域下的实际颜色", fontsize=10.5, pad=6)

# ================= 左下：色度图上的位移 =================
axL = fig.add_subplot(gs[1, 0])
XLIM, YLIM = (0.135, 0.720), (0.055, 0.625)
axL.set_axisbelow(True)
for gl in axL.get_xgridlines() + axL.get_ygridlines():
    gl.set_zorder(-5)
draw_chroma_bg(axL, XLIM, YLIM)

for pri, col, lab in [(SRGB_PRI, H.NAVY, "sRGB 边界"),
                      (P3_PRI, H.ORANGE, "P3 边界")]:
    p = np.vstack([pri, pri[:1]])
    axL.plot(p[:, 0], p[:, 1], color=col, lw=1.6, ls="--", alpha=0.85,
             zorder=3, label=lab)

for r in ROWS:
    xs, ys = r["xy_s"]
    xp, yp = r["xy_p"]
    colhex = code_hex(r["disp_p"])
    axL.annotate("", xy=(xp, yp), xytext=(xs, ys),
                 arrowprops=dict(arrowstyle="-|>", color=colhex, lw=2.0,
                                 shrinkA=3.5, shrinkB=2.0, alpha=0.95), zorder=8)
    axL.plot([xs], [ys], "o", ms=5.4, color=colhex, mec="white", mew=1.0, zorder=9)
    axL.plot([xp], [yp], "o", ms=5.4, color="white", mec=colhex, mew=1.8, zorder=9)

axL.plot([], [], "o", ms=5.4, color=H.GRAY, mec="white", mew=1.0,
         label="按 sRGB 解释")
axL.plot([], [], "o", ms=5.4, color="white", mec=H.GRAY, mew=1.8,
         label="按 P3 解释（更靠外）")

axL.set_xlim(*XLIM)
axL.set_ylim(*YLIM)
axL.set_xlabel("色度坐标 x")
axL.set_ylabel("色度坐标 y")
axL.set_title("① 码值不变，位置被推到色域更外圈", fontsize=10.5, pad=6)
axL.legend(loc="upper right", fontsize=6.8, handletextpad=0.5, labelspacing=0.40,
           bbox_to_anchor=(1.005, 1.005))

# ================= 右下：饱和度渐变条 =================
axR = fig.add_subplot(gs[1, 1])
axR.set_xlim(-1.9, 12.1)
axR.set_ylim(-1.15, 2.85)
axR.axis("off")

N = 6
K = np.linspace(0.0, 0.9, N)
axR.text(-1.80, 2.72, "② 饱和度渐变：同一串码值，P3 更艳", fontsize=8.8,
         color="#2b3540", fontweight="bold", ha="left", va="center")
axR.text(3.0, 2.40, "红系（k 越大越纯）", fontsize=6.8,
         color="#3b4450", ha="center", va="center")
axR.text(9.6, 2.40, "绿系（k 越大越纯）", fontsize=6.8,
         color="#3b4450", ha="center", va="center")
axR.text(-0.15, 1.96, "sRGB", fontsize=7.6, color=H.NAVY, fontweight="bold",
         ha="right", va="center")
axR.text(-0.15, 0.86, "P3", fontsize=7.6, color=H.ORANGE, fontweight="bold",
         ha="right", va="center")

for gi, (xoff, fam) in enumerate([(0.0, "r"), (6.6, "g")]):
    for i, k in enumerate(K):
        if fam == "r":
            code = np.array([1.0, 1.0 - k, 1.0 - k])
        else:
            code = np.array([1.0 - k, 1.0, 1.0 - k])
        rgb_s = code.copy()
        rgb_p, _ = render_on_srgb(P3_M @ H.srgb_eotf(code))
        axR.add_patch(Rectangle((xoff + i, 1.66), 1.0, 0.60, facecolor=rgb_s,
                                edgecolor="white", lw=0.8, zorder=3))
        axR.add_patch(Rectangle((xoff + i, 0.56), 1.0, 0.60, facecolor=rgb_p,
                                edgecolor="white", lw=0.8, zorder=3))

axR.text(-1.80, -0.10, "红系码值 (255, 255-k, 255-k)；绿系码值 (255-k, 255, 255-k)。",
         fontsize=6.9, color="#3b4450", ha="left", va="center")
axR.text(-1.80, -0.52, "k 从左到右增大；上排是 sRGB 屏的样子，下排是 P3 屏的样子。",
         fontsize=6.9, color="#3b4450", ha="left", va="center")
axR.text(-1.80, -0.94, "同样一串码值，P3 上更接近纯色；绿系那一组差别最明显。",
         fontsize=6.9, color="#3b4450", ha="left", va="center")

fig.suptitle("广色域渲染：同一码值，在 sRGB 与 P3 上呈现的颜色并不相同",
             fontsize=11.5, fontweight="bold", y=0.972)

H.save(fig, 5, "f5_p3_render")
for r in ROWS:
    print(r["name"], r["cube"], "->", code_hex(r["disp_p"]), "clip=", r["clip"],
          "xy_s=", np.round(r["xy_s"], 4), "xy_p=", np.round(r["xy_p"], 4))
