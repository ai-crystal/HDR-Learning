# -*- coding: utf-8 -*-
"""第 05 章专用辅助模块：三色域的真实基色、白点、RGB↔XYZ 矩阵与 Lab 换算。

基色坐标取自公开标准：
  sRGB / BT.709 —— IEC 61966-2-1、ITU-R BT.709
  DCI-P3       —— SMPTE RP 431-2（白点 DCI），Display P3 为同基色 + D65
  BT.2020      —— ITU-R BT.2020-2
"""
import numpy as np

# (R, G, B) 的 CIE 1931 xy 坐标
PRIMARIES = {
    "sRGB":   {"R": (0.640, 0.330), "G": (0.300, 0.600), "B": (0.150, 0.060)},
    "P3":     {"R": (0.680, 0.320), "G": (0.265, 0.690), "B": (0.150, 0.060)},
    "BT2020": {"R": (0.708, 0.292), "G": (0.170, 0.797), "B": (0.131, 0.046)},
}
WHITE_XY = {
    "D65": (0.3127, 0.3290),
    "DCI": (0.3140, 0.3510),
    "D50": (0.3457, 0.3585),
}


def xy_to_xyz(x, y, Y=1.0):
    return np.array([x * Y / y, Y, (1.0 - x - y) * Y / y])


def rgb_to_xyz_matrix(prim, white="D65"):
    """由基色坐标与白点构造 RGB→XYZ 矩阵（归一化到白点 Y = 1）。"""
    P = np.array([xy_to_xyz(*prim["R"]), xy_to_xyz(*prim["G"]),
                  xy_to_xyz(*prim["B"])]).T
    W = xy_to_xyz(*WHITE_XY[white], 1.0)
    S = np.linalg.solve(P, W)
    return P * S


def xyz_to_lab(XYZ, white="D65"):
    W = xy_to_xyz(*WHITE_XY[white], 1.0)
    t = np.asarray(XYZ, dtype=float) / W

    def f(u):
        d = 6.0 / 29.0
        return np.where(u > d ** 3, np.cbrt(u), u / (3 * d * d) + 4.0 / 29.0)

    fx, fy, fz = f(t[..., 0]), f(t[..., 1]), f(t[..., 2])
    return np.stack([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)], axis=-1)


def xyz_to_uv76(XYZ):
    """CIE 1976 u'v'（更接近感知均匀的色度图）。"""
    X, Y, Z = XYZ[..., 0], XYZ[..., 1], XYZ[..., 2]
    d = X + 15 * Y + 3 * Z
    u = 4 * X / d
    v = 9 * Y / d
    return np.stack([u, v], axis=-1)


def xy_to_uv76(x, y):
    d = -2 * x + 12 * y + 3
    return 4 * x / d, 9 * y / d


def gamut_triangle(name, n=400):
    """色域的色度边界（在 xy 与 u'v' 中的三角形）。"""
    prim = PRIMARIES[name]
    xy = np.array([prim["R"], prim["G"], prim["B"], prim["R"]])
    return xy, xy_to_uv76(xy[:, 0], xy[:, 1])


def uv_area(pts):
    """多边形面积（鞋带公式）。pts 可以是 (N,2) 数组或 (x, y) 两个数组。"""
    if isinstance(pts, tuple):
        x, y = np.asarray(pts[0], float), np.asarray(pts[1], float)
    else:
        pts = np.asarray(pts, float)
        x, y = pts[:, 0], pts[:, 1]
    return 0.5 * np.abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
