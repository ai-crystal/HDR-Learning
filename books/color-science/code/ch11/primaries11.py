# -*- coding: utf-8 -*-
"""第 11 章专用辅助模块：多原色、窄带光谱、RGBW 映射与色域体积。

基色表与矩阵函数复用第 07 章的 rgbspace.py，色匹配函数复用第 05 章的 cie1931.py，
保证与前几章的数值一致。本章新增的内容：
  * 用高斯型窄带光谱积分出原色坐标（激光 / 量子点 / 荧光粉的区别）
  * 原色集合的凸包色域多边形与面积、覆盖率（多边形裁剪求交）
  * 由原色三刺激值集合直接算 Lab 体积（凸包）
  * RGBW 的子像素面积模型与解的一维族
"""
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_HERE, "..", "ch05"), os.path.join(_HERE, "..", "ch07")):
    _p = os.path.normpath(_p)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import cie1931 as C          # noqa: E402
import rgbspace as R         # noqa: E402

PRIMARIES = R.PRIMARIES
WHITE = R.WHITE
xy_to_XYZ = R.xy_to_XYZ
xyz_to_lab = R.XYZ_to_Lab

# ---------------- 参考白 ----------------
Y_REF = 1000.0               # 体积口径：把 1000 cd/m2 的 D65 定为参考白（L* = 100）


def xy_to_uv76(x, y):
    d = -2 * x + 12 * y + 3
    return 4 * x / d, 9 * y / d


def xyz_to_uv76(XYZ):
    X, Y, Z = XYZ[..., 0], XYZ[..., 1], XYZ[..., 2]
    d = X + 15 * Y + 3 * Z
    return np.stack([4 * X / d, 9 * Y / d], axis=-1)


# ---------------- 窄带光谱 ----------------
def gauss_spd(lam, peak, fwhm):
    """高斯型发射谱。fwhm 为半高全宽，单位 nm。"""
    sigma = fwhm / (2.0 * np.sqrt(2.0 * np.log(2.0)))
    return np.exp(-0.5 * ((lam - peak) / sigma) ** 2)


def spd_to_xyz(peak, fwhm, lam=None):
    """对 380–780 nm 按 1 nm 积分，返回归一化到 Y = 1 的 XYZ。"""
    if lam is None:
        lam = np.arange(380.0, 781.0, 1.0)
    spd = gauss_spd(lam, peak, fwhm)
    xb = np.interp(lam, C.LAM, C.XBAR)
    yb = np.interp(lam, C.LAM, C.YBAR)
    zb = np.interp(lam, C.LAM, C.ZBAR)
    X = np.trapezoid(spd * xb, lam)
    Y = np.trapezoid(spd * yb, lam)
    Z = np.trapezoid(spd * zb, lam)
    return np.array([X, Y, Z]) / Y


def spd_to_xy(peak, fwhm):
    q = spd_to_xyz(peak, fwhm)
    s = q.sum()
    return q[0] / s, q[1] / s


def xy_of_wavelength(nm):
    xb = np.interp(nm, C.LAM, C.XBAR)
    yb = np.interp(nm, C.LAM, C.YBAR)
    zb = np.interp(nm, C.LAM, C.ZBAR)
    s = xb + yb + zb
    return xb / s, yb / s


# ---------------- 多边形工具 ----------------
def polygon_area(pts):
    x = np.asarray(pts)[:, 0]
    y = np.asarray(pts)[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def convex_hull_2d(pts):
    pts = np.unique(np.round(np.asarray(pts, float), 12), axis=0)
    if len(pts) < 3:
        return pts
    pts = pts[np.lexsort((pts[:, 1], pts[:, 0]))]

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in pts[::-1]:
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return np.array(lower[:-1] + upper[:-1])


def clip_polygon(subject, clip):
    """Sutherland–Hodgman：返回 subject 与凸多边形 clip 的交集。"""
    out = [tuple(p) for p in subject]
    clip = [tuple(p) for p in clip]
    n = len(clip)
    ccw = polygon_signed(clip) > 0

    for i in range(n):
        a, b = clip[i], clip[(i + 1) % n]
        if not out:
            break
        inp, out = out, []

        def inside(p):
            v = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
            return v >= 0 if ccw else v <= 0

        def inter(p, q):
            x1, y1 = p
            x2, y2 = q
            dx1, dy1 = b[0] - a[0], b[1] - a[1]
            dx2, dy2 = x2 - x1, y2 - y1
            den = dx1 * dy2 - dy1 * dx2
            if abs(den) < 1e-15:
                return q
            t = ((x1 - a[0]) * dy1 - (y1 - a[1]) * dx1) / den
            return (x1 + t * dx2, y1 + t * dy2)

        s = inp[-1]
        for e in inp:
            if inside(e):
                if not inside(s):
                    out.append(inter(s, e))
                out.append(e)
            elif inside(s):
                out.append(inter(s, e))
            s = e
    return np.array(out)


def polygon_signed(pts):
    x = np.asarray(pts)[:, 0]
    y = np.asarray(pts)[:, 1]
    return 0.5 * (np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


# ---------------- 原色集合 ----------------
def prim_xyz(primaries):
    """primaries: [(x, y), ...]；返回每列是某原色在 Y = 1 时的 XYZ。"""
    return np.array([xy_to_XYZ(x, y, 1.0) for x, y in primaries]).T


def lum_weights(primaries, white_xy, peak):
    """解出各原色在白点处的亮度，使白点 Y = peak。原色多于 3 时用最小范数解。"""
    P = prim_xyz(primaries)
    W = xy_to_XYZ(*white_xy, peak)
    s, *_ = np.linalg.lstsq(P, W, rcond=None)
    return s


def covering_matrix(primaries, white_xy, peak):
    P = prim_xyz(primaries)
    s = lum_weights(primaries, white_xy, peak)
    return P * s, s


def lab_volume(columns, levels=15):
    """columns: 3xN 的 XYZ 列（各自峰值亮度下的三刺激值）。
    在单位立方体上采样，映射到 Lab（参考白 Y_REF），返回凸包体积。"""
    from scipy.spatial import ConvexHull

    g = np.linspace(0.0, 1.0, levels)
    a, b, c = np.meshgrid(g, g, g, indexing="ij")
    w = np.stack([a.ravel(), b.ravel(), c.ravel()], axis=0)
    XYZ = columns @ w
    lab = xyz_to_lab(XYZ.T, white="D65")
    lab = lab / np.array([1.0, 1.0, 1.0]) * np.array([1.0, 1.0, 1.0])
    lab[:, 0] *= 100.0 / 100.0
    try:
        return ConvexHull(lab).volume
    except Exception:
        return 0.0


def lab_volume_abs(columns, levels=13):
    """同上，但把 Y 换算到绝对亮度（cd/m2），参考白 Y_REF。
    columns 的 Y 单位是"相对峰值 1"，调用方先乘上峰值亮度。"""
    from scipy.spatial import ConvexHull

    columns = np.asarray(columns, dtype=float)
    n = columns.shape[1]
    g = np.linspace(0.0, 1.0, levels)
    grids = np.meshgrid(*([g] * n), indexing="ij")
    w = np.stack([q.ravel() for q in grids], axis=0)
    XYZ = (columns @ w).T                      # Y 已经是 cd/m2
    t = XYZ / xy_to_XYZ(*R.WHITE["D65"], Y_REF)
    d = 6.0 / 29.0

    def f(u):
        return np.where(u > d ** 3, np.cbrt(np.maximum(u, 0)), u / (3 * d * d) + 4.0 / 29.0)

    fx, fy, fz = f(t[:, 0]), f(t[:, 1]), f(t[:, 2])
    lab = np.stack([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)], axis=-1)
    try:
        return ConvexHull(lab).volume
    except Exception:
        return 0.0


def gamut_polygon_uv(primaries):
    uv = np.array([xy_to_uv76(*p) for p in primaries])
    return convex_hull_2d(uv)


def coverage(primaries, ref_primaries):
    """按 u'v' 面积算：交集 / 参考色域面积。"""
    a = gamut_polygon_uv(primaries)
    b = gamut_polygon_uv(ref_primaries)
    inter = clip_polygon(a, b)
    if len(inter) < 3:
        return 0.0
    return polygon_area(inter) / polygon_area(b)
