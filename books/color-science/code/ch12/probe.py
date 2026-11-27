# -*- coding: utf-8 -*-
"""第 12 章的自检与数值探针，不产出图片。

跑一遍可以得到正文里引用的所有数字：
  python probe.py
"""
import os
import sys
import numpy as np

sys.path.insert(0, "E:/Study/HDR技术/books/common")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import metrics as M

np.set_printoptions(precision=4, suppress=True)

WHITE_LUM = 203.0
mm = M.Metrics(white_lum=WHITE_LUM)


def xyz_of(L, C, h):
    return M.lab_to_xyz(M.lch_to_lab(L, C, h), white_ref=WHITE_LUM)


def check_cam16():
    white = np.array([0.95047, 1.0, 1.08883]) * WHITE_LUM
    cam = mm.cam.forward(white)
    print("白点 J=%.3f Q=%.3f C=%.4f M=%.4f h=%.2f  D=%.3f FL=%.3f"
          % (cam["J"], cam["Q"], cam["C"], cam["M"], cam["h"], mm.cam.D, mm.cam.FL))
    grey = np.array([0.95047, 1.0, 1.08883]) * 20.0
    cam = mm.cam.forward(grey)
    print("20 cd/m2 中性灰 J=%.3f Q=%.3f C=%.4f" % (cam["J"], cam["Q"], cam["C"]))


# ---------------------------------------------------------------- 色样对
# 每组：(名字, 基色 L*, C*, h, dL, dC, dh)
PAIRS = [
    ("近白 200nit", 97.0, 2.0, 90.0, -1.5, 1.0, 8.0),
    ("中性灰 100nit", 78.0, 1.0, 0.0, -2.0, 0.5, 0.0),
    ("暗部深灰", 12.0, 3.0, 300.0, 1.5, 1.5, 20.0),
    ("肤色", 65.0, 28.0, 55.0, -1.2, 1.5, 2.0),
    ("深红", 40.0, 60.0, 30.0, -2.0, -4.0, -1.0),
    ("叶绿", 60.0, 50.0, 135.0, 1.5, 3.0, 1.0),
    ("天蓝", 55.0, 40.0, 250.0, -1.0, -3.0, 2.0),
    ("深蓝紫", 35.0, 45.0, 295.0, -1.0, 4.0, 1.5),
    ("亮黄高亮", 105.0, 70.0, 95.0, 2.0, -3.0, -1.5),
    ("高饱和绿 600nit", 115.0, 65.0, 140.0, -2.0, 3.0, 1.0),
    ("暗部高饱和蓝", 9.0, 25.0, 280.0, 1.0, 3.0, 2.0),
    ("亮部低饱和青", 100.0, 12.0, 200.0, -3.0, 2.0, 4.0),
]


def table():
    rows = []
    for name, L, C, h, dL, dC, dh in PAIRS:
        x1 = xyz_of(L, C, h)
        x2 = xyz_of(L + dL, C + dC, h + dh)
        r = mm.all(x1, x2)
        rows.append((name, r))
        print("%-16s dE00=%6.3f dEITP=%7.2f dEz=%7.4f dEu=%6.3f"
              % (name, r["dE00"], r["dEITP"], r["dEz"], r["dEu"]))
    keys = ["dE00", "dEITP", "dEz", "dEu"]
    print("\n秩次（1 最大）")
    ranks = {k: [] for k in keys}
    for k in keys:
        vals = np.array([r[k] for _, r in rows])
        order = np.argsort(-vals)
        rk = np.empty(len(vals))
        rk[order] = np.arange(1, len(vals) + 1)
        ranks[k] = rk
    for i, (name, _) in enumerate(rows):
        print("%-16s " % name + "  ".join("%d" % ranks[k][i] for k in keys))
    print("\n比值范围")
    for k in keys:
        v = np.array([r[k] for _, r in rows])
        print("%-6s min %.3f max %.3f  max/min %.2f" % (k, v.min(), v.max(), v.max() / v.min()))
    # 斯皮尔曼
    from scipy.stats import spearmanr
    mat = np.array([[r[k] for k in keys] for _, r in rows])
    rho, _ = spearmanr(mat)
    print("\nSpearman")
    print(np.array2string(rho, precision=2))


def contour_extent(L, C, h, level):
    """在 (L*, C*) 局部网格上找四个度量的等值线包络，用于定图幅范围。"""
    dL = np.linspace(-22, 22, 89)
    dC = np.linspace(-22, 22, 89)
    x0 = xyz_of(L, C, h)
    for sp, fn in (("00", lambda a, b: mm.all(a, b)["dE00"]),
                   ("itp", lambda a, b: mm.all(a, b)["dEITP"]),
                   ("jz", lambda a, b: mm.all(a, b)["dEz"]),
                   ("cam", lambda a, b: mm.all(a, b)["dEu"])):
        ext = []
        for dl, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            lo, hi = 0.0, 30.0
            for _ in range(30):
                mid = 0.5 * (lo + hi)
                v = fn(x0, xyz_of(L + dl * mid, C + dc * mid, h))
                if v < level:
                    lo = mid
                else:
                    hi = mid
            ext.append(0.5 * (lo + hi))
        print("  %-4s L-:%.2f L+:%.2f C-:%.2f C+:.%2f" % (sp, ext[0], ext[1], ext[2], ext[3]))


if __name__ == "__main__":
    check_cam16()
    print()
    table()
    print("\n等值线包络 level=2")
    for name, L, C, h in (("红橙", 70, 45, 40), ("蓝紫", 40, 35, 295)):
        print(name)
        contour_extent(L, C, h, 2.0)
