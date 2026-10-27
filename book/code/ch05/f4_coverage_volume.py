# -*- coding: utf-8 -*-
"""第 05 章 图 4：覆盖率（2D 面积交集）vs 覆盖体积（3D，含亮度）。

左上：覆盖率 = 设备三角形与目标三角形的交集面积 ÷ 目标面积。
右上：覆盖体积 = 把亮度也算进去的三维体积，可以“超过 100%”。
下方：同一台屏两个口径给出的数字对比（这正是营销话术的来路）。
"""
import sys
sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
sys.path.insert(0, "E:/Study/HDR技术/book/code/ch04")
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import Polygon, Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import hdrfig as H

plt = H.plt

P3 = np.array([(0.680, 0.320), (0.265, 0.690), (0.150, 0.060)])
DEV = np.array([(0.680, 0.320), (0.285, 0.660), (0.150, 0.060)])


def tri_area(p):
    x = np.array([q[0] for q in p])
    y = np.array([q[1] for q in p])
    return 0.5 * abs(x[0] * (y[1] - y[2]) + x[1] * (y[2] - y[0]) + x[2] * (y[0] - y[1]))


# ---------------- 数值：覆盖率 ----------------
rng = np.random.default_rng(7)
pts = np.column_stack([rng.uniform(P3[:, 0].min(), P3[:, 0].max(), 400000),
                       rng.uniform(P3[:, 1].min(), P3[:, 1].max(), 400000)])
in_p3 = Path(np.vstack([P3, P3[:1]])).contains_points(pts)
in_dev = Path(np.vstack([DEV, DEV[:1]])).contains_points(pts)
COV = float(in_dev[in_p3].mean())              # 覆盖率
H_TGT, H_DEV = 0.65, 0.98                      # 目标/设备“亮度高度”（示意）
VOL = COV * H_DEV / H_TGT                      # 体积比

fig = plt.figure(figsize=(7.2, 5.4))
gs = fig.add_gridspec(2, 2, height_ratios=[1.32, 1.0], width_ratios=[1.0, 1.0],
                      hspace=0.46, wspace=0.20,
                      left=0.085, right=0.975, top=0.855, bottom=0.10)

# ================= 左上：覆盖率（2D） =================
axA = fig.add_subplot(gs[0, 0])
UNCOV = [tuple(P3[0]), tuple(P3[1]), tuple(P3[2]), tuple(DEV[1])]
axA.add_patch(Polygon(P3, closed=True, facecolor="#eef1f4", edgecolor="#8b95a1",
                      lw=1.6, ls="--", alpha=0.75, zorder=2))
axA.add_patch(Polygon(DEV, closed=True, facecolor=H.GREEN, edgecolor=H.GREEN,
                      lw=2.0, alpha=0.34, zorder=3))
axA.add_patch(Polygon(UNCOV, closed=True, facecolor=H.RED, edgecolor=H.RED,
                      lw=1.0, alpha=0.30, hatch="///", zorder=4))
axA.plot([DEV[0, 0], DEV[1, 0]], [DEV[0, 1], DEV[1, 1]], color=H.GREEN, lw=2.0, zorder=5)
axA.plot([DEV[1, 0], DEV[2, 0]], [DEV[1, 1], DEV[2, 1]], color=H.GREEN, lw=2.0, zorder=5)

axA.annotate("整条顶边都差一点点 ——\n这就是“盖不到”的部分", xy=(0.268, 0.641), xytext=(0.118, 0.560),
             fontsize=7.6, color=H.RED, ha="left", va="center", zorder=8,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.2,
                             connectionstyle="arc3,rad=-0.25"),
             bbox=dict(boxstyle="round,pad=0.24", fc="white", ec=H.RED, alpha=0.92, lw=0.8))
axA.text(0.395, 0.200, "交集 = 设备能显示的部分", fontsize=8.2, color="#14663f",
         ha="center", va="center", fontweight="bold", zorder=8)
axA.set_xlim(0.10, 0.75)
axA.set_ylim(0.00, 0.82)
axA.set_xlabel("色度坐标 x")
axA.set_ylabel("色度坐标 y")
axA.set_title("① 覆盖率 = 面积交集 ÷ 目标面积", fontsize=10.2, pad=7)
axA.text(0.125, 0.745, f"覆盖率 ≈ {COV * 100:.0f}%", fontsize=10.5, color=H.NAVY,
         fontweight="bold", ha="left", va="center", zorder=9,
         bbox=dict(boxstyle="round,pad=0.32", fc="#eef4fa", ec=H.NAVY, lw=1.0))
axA.legend(handles=[Patch(facecolor="#eef1f4", edgecolor="#8b95a1", ls="--",
                          label="目标色域：DCI-P3（100%）"),
                    Patch(facecolor=H.GREEN, alpha=0.5, edgecolor=H.GREEN,
                          label="设备实际能显示的部分"),
                    Patch(facecolor=H.RED, alpha=0.35, hatch="///", edgecolor=H.RED,
                          label="盖不到的部分（约 7%）")],
           loc="upper right", fontsize=7.2, handlelength=1.5, labelspacing=0.45,
           bbox_to_anchor=(1.005, 1.005))

# ================= 右上：覆盖体积（3D） =================
axB = fig.add_subplot(gs[0, 1], projection="3d")


def prism_faces(tri, z0, z1, scale=2.2, off=(0.12, 0.03)):
    q = [np.array([(x - off[0]) * scale, (y - off[1]) * scale]) for x, y in tri]
    faces = [[(q[0][0], q[0][1], z0), (q[1][0], q[1][1], z0), (q[2][0], q[2][1], z0)],
             [(q[0][0], q[0][1], z1), (q[1][0], q[1][1], z1), (q[2][0], q[2][1], z1)]]
    for i in range(3):
        a, b = q[i], q[(i + 1) % 3]
        faces.append([(a[0], a[1], z0), (b[0], b[1], z0),
                      (b[0], b[1], z1), (a[0], a[1], z1)])
    return faces


axB.add_collection3d(Poly3DCollection(prism_faces(P3, 0, H_TGT), facecolor="#9aa3ad",
                                      edgecolor="#4a5560", lw=1.0, alpha=0.16))
axB.add_collection3d(Poly3DCollection(prism_faces(DEV, 0, H_DEV), facecolor=H.GREEN,
                                      edgecolor="#14663f", lw=1.1, alpha=0.24))
axB.set_xlim(0, 1.30)
axB.set_ylim(0, 1.65)
axB.set_zlim(0, 1.25)
axB.set_box_aspect((1.0, 1.25, 1.0))
axB.view_init(elev=17, azim=-58)
axB.set_xticks([])
axB.set_yticks([])
axB.set_zticks([])
axB.set_zlabel("亮度（相对）", fontsize=8)
axB.set_title("② 覆盖体积 = 底面积（色度）× 高度（亮度）", fontsize=10.2, pad=0)
axB.text2D(0.02, 0.96, f"体积 ≈ {VOL * 100:.0f}%\n（底面积 93%，但更高）", transform=axB.transAxes,
           fontsize=8.6, color=H.RED, fontweight="bold", ha="left", va="top",
           bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=H.RED, alpha=0.92, lw=0.9))
axB.text2D(0.02, 0.03, "灰：目标 P3　绿：设备实际",
           transform=axB.transAxes, fontsize=7.4, color="#3b4450",
           ha="left", va="bottom")

# ================= 下：两个口径的数字 =================
axC = fig.add_subplot(gs[1, :])
axC.barh([1.0], [COV * 100], height=0.42, color=H.NAVY, alpha=0.90, zorder=3)
axC.barh([1.0], [100 - COV * 100], left=[COV * 100], height=0.42, color="#f3d3cf",
         edgecolor=H.RED, hatch="///", lw=0.8, zorder=3)
axC.barh([0.0], [100], height=0.42, color=H.LGRAY, alpha=0.9, zorder=3)
axC.barh([0.0], [VOL * 100], height=0.42, color=H.ORANGE, alpha=0.90, zorder=3)

axC.text(COV * 50, 1.0, "覆盖率（面积口径）", va="center", ha="center",
         fontsize=9.0, color="white", fontweight="bold", zorder=5)
axC.annotate(f"盖不到 {100 - COV * 100:.0f}%", xy=(COV * 100 + 3, 1.0),
             xytext=(COV * 100 + 12, 1.42), fontsize=8.0, color=H.RED,
             ha="left", va="center", zorder=6,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.1),
             bbox=dict(boxstyle="round,pad=0.24", fc="white", ec=H.RED, alpha=0.92, lw=0.8))
axC.text(VOL * 100 / 2, 0.0, "色域体积（含亮度口径）", va="center", ha="center",
         fontsize=9.0, color="white", fontweight="bold", zorder=5)
axC.axvline(100, color=H.NAVY, ls=":", lw=1.4, zorder=4)
axC.text(101, 0.42, "sRGB 基准 = 100%", fontsize=8.0, color=H.NAVY, ha="left",
         va="center", zorder=6)
axC.annotate("超过 100% 的部分\n其实是“更亮”撑出来的", xy=(VOL * 100 - 12, -0.28),
             xytext=(VOL * 100 + 3, -0.34), fontsize=8.0, color=H.RED,
             ha="left", va="center", zorder=6,
             arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.1),
             bbox=dict(boxstyle="round,pad=0.26", fc="white", ec=H.RED, alpha=0.92, lw=0.8))
axC.set_yticks([1.0, 0.0])
axC.set_yticklabels(["覆盖率\n（2D，看颜色种类）", "色域体积\n（3D，含亮度）"], fontsize=8.6)
axC.set_xlim(0, 178)
axC.set_ylim(-0.85, 1.62)
axC.set_xlabel("百分比（%）")
axC.set_title("③ 同一台屏，“面积口径”和“体积口径”差得很远", fontsize=10.2, pad=7)

fig.suptitle("覆盖率 vs 覆盖体积：一个说“颜色够不够”，一个把亮度也算进去",
             fontsize=11.5, fontweight="bold", y=0.965)

H.save(fig, 5, "f4_coverage_volume")
print("coverage = %.4f   volume = %.4f" % (COV, VOL))
print("area P3 = %.5f  area DEV = %.5f" % (tri_area(P3), tri_area(DEV)))
