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

# =====================  扩写补充：更多色域、Luv、体积与切片  =====================

# Adobe RGB (1998)、ACES AP0/AP1、ProPhoto 的基色与白点（公开标准）
PRIMARIES.update({
    "AdobeRGB": {"R": (0.640, 0.330), "G": (0.210, 0.710), "B": (0.150, 0.060)},
    "AP0":      {"R": (0.7347, 0.2653), "G": (0.0000, 1.0000), "B": (0.0001, -0.0770)},
    "AP1":      {"R": (0.713, 0.293), "G": (0.165, 0.830), "B": (0.128, 0.044)},
    "ProPhoto": {"R": (0.734699, 0.265301), "G": (0.159597, 0.840403),
                 "B": (0.036598, 0.000105)},
})
WHITE_XY.update({"ACES": (0.32168, 0.33767)})

GAMUT_WHITE = {
    "sRGB": "D65", "P3": "D65", "BT2020": "D65", "AdobeRGB": "D65",
    "AP0": "ACES", "AP1": "ACES", "ProPhoto": "D50",
}


def prim_xy(name):
    """返回 (R, G, B) 三个基色的 xy 数组。"""
    p = PRIMARIES[name]
    return np.array([p["R"], p["G"], p["B"]])


def xyz_to_luv(XYZ, white="D65"):
    """CIELUV：L*、u*、v*（D65 参考白，Y 归一化到 1）。"""
    W = xy_to_xyz(*WHITE_XY[white], 1.0)
    X, Y, Z = XYZ[..., 0], XYZ[..., 1], XYZ[..., 2]
    d = 6.0 / 29.0

    def f(t):
        return np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4.0 / 29.0)

    L = 116 * f(Y / W[1]) - 16
    den = X + 15 * Y + 3 * Z
    denw = W[0] + 15 * W[1] + 3 * W[2]
    up = 4 * X / np.maximum(den, 1e-12)
    vp = 9 * Y / np.maximum(den, 1e-12)
    upw, vpw = 4 * W[0] / denw, 9 * W[1] / denw
    return np.stack([L, 13 * L * (up - upw), 13 * L * (vp - vpw)], axis=-1)


def lab_slice_area(name, L_target, n=90, white=None):
    """在 CIELAB 的 L* = L_target 平面上，色域截面的多边形面积。

    做法：在 RGB 立方体表面采样，取 L* 最接近 L_target 的等值线，
    用凸包围成的多边形面积近似（截面本身是凸的）。
    """
    from scipy.spatial import ConvexHull
    w = white or GAMUT_WHITE[name]
    M = rgb_to_xyz_matrix(PRIMARIES[name], w)
    t = np.linspace(0, 1, n)
    # 立方体六个面
    faces = []
    for axis in range(3):
        for val in (0.0, 1.0):
            grid = np.array(np.meshgrid(t, t, indexing="ij")).reshape(2, -1).T
            rgb = np.zeros((grid.shape[0], 3))
            others = [i for i in range(3) if i != axis]
            rgb[:, axis] = val
            rgb[:, others[0]] = grid[:, 0]
            rgb[:, others[1]] = grid[:, 1]
            faces.append(rgb)
    rgb = np.concatenate(faces, axis=0)
    lab = xyz_to_lab(rgb @ M.T, w)
    sel = np.abs(lab[:, 0] - L_target) < 0.35
    if sel.sum() < 8:
        return 0.0
    pts = lab[sel][:, 1:3]
    try:
        return ConvexHull(pts).volume
    except Exception:
        return 0.0


def gamut_volume_lab(name, n=34):
    """CIELAB 下的色域体积（凸包）。"""
    from scipy.spatial import ConvexHull
    w = GAMUT_WHITE[name]
    M = rgb_to_xyz_matrix(PRIMARIES[name], w)
    g = np.linspace(0, 1, n)
    R, G, B = np.meshgrid(g, g, g, indexing="ij")
    rgb = np.stack([R.ravel(), G.ravel(), B.ravel()], axis=-1)
    lab = xyz_to_lab(rgb @ M.T, w)
    return ConvexHull(lab).volume


def gamut_volume_luv(name, n=34):
    """CIELUV 下的色域体积（凸包）。"""
    from scipy.spatial import ConvexHull
    w = GAMUT_WHITE[name]
    M = rgb_to_xyz_matrix(PRIMARIES[name], w)
    g = np.linspace(0, 1, n)
    R, G, B = np.meshgrid(g, g, g, indexing="ij")
    rgb = np.stack([R.ravel(), G.ravel(), B.ravel()], axis=-1)
    luv = xyz_to_luv(rgb @ M.T, w)
    return ConvexHull(luv).volume


def clamp_rgb(rgb):
    """逐通道裁剪到 [0,1]。"""
    return np.clip(rgb, 0.0, 1.0)


def rgb_to_lab(rgb, name="sRGB"):
    w = GAMUT_WHITE[name]
    M = rgb_to_xyz_matrix(PRIMARIES[name], w)
    return xyz_to_lab(np.asarray(rgb) @ M.T, w)


def lab_to_rgb(lab, name="sRGB"):
    w = GAMUT_WHITE[name]
    M = rgb_to_xyz_matrix(PRIMARIES[name], w)
    W = xy_to_xyz(*WHITE_XY[w], 1.0)
    lab = np.asarray(lab, dtype=float)
    fy = (lab[..., 0] + 16) / 116
    fx = fy + lab[..., 1] / 500
    fz = fy - lab[..., 2] / 200
    d = 6.0 / 29.0

    def fi(f):
        return np.where(f > d, f ** 3, 3 * d * d * (f - 4.0 / 29.0))

    xyz = np.stack([fi(fx), fi(fy), fi(fz)], axis=-1) * W
    return xyz @ np.linalg.inv(M).T


def in_gamut(rgb, tol=1e-6):
    rgb = np.asarray(rgb, dtype=float)
    return np.all(rgb >= -tol, axis=-1) & np.all(rgb <= 1 + tol, axis=-1)


def max_chroma(L, h_deg, name, n_iter=22):
    """在 LCh 平面上二分求色域边界上的最大彩度 C_max(L, h)。"""
    lo, hi = 0.0, 180.0
    h = np.radians(h_deg)
    for _ in range(n_iter):
        mid = 0.5 * (lo + hi)
        lab = np.array([L, mid * np.cos(h), mid * np.sin(h)])
        if in_gamut(lab_to_rgb(lab, name)):
            lo = mid
        else:
            hi = mid
    return lo


def knee_map(c_in, c_knee, c_lim):
    """膝形彩度压缩：膝点以内恒等，以外指数收敛到 c_lim。"""
    c_in = np.asarray(c_in, dtype=float)
    out = np.where(c_in <= c_knee, c_in,
                   c_knee + (c_lim - c_knee) *
                   (1.0 - np.exp(-(c_in - c_knee) / max(c_lim - c_knee, 1e-9))))
    return np.minimum(out, c_lim)


def dE2000(lab1, lab2):
    """CIEDE2000（kL = kC = kH = 1），支持数组。"""
    L1, a1, b1 = [np.asarray(v, dtype=float) for v in (lab1[..., 0], lab1[..., 1], lab1[..., 2])]
    L2, a2, b2 = [np.asarray(v, dtype=float) for v in (lab2[..., 0], lab2[..., 1], lab2[..., 2])]
    C1, C2 = np.hypot(a1, b1), np.hypot(a2, b2)
    Cm = 0.5 * (C1 + C2)
    Gf = 0.5 * (1 - np.sqrt(Cm ** 7 / (Cm ** 7 + 25.0 ** 7)))
    a1p, a2p = (1 + Gf) * a1, (1 + Gf) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360
    dLp = L2 - L1
    dCp = C2p - C1p
    dhp = h2p - h1p
    dhp = np.where(dhp > 180, dhp - 360, np.where(dhp < -180, dhp + 360, dhp))
    dhp = np.where(C1p * C2p == 0, 0.0, dhp)
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp) / 2)
    Lpm = 0.5 * (L1 + L2)
    Cpm = 0.5 * (C1p + C2p)
    hsum = h1p + h2p
    hpm = np.where(np.abs(h1p - h2p) <= 180, 0.5 * hsum,
                   np.where(hsum < 360, 0.5 * (hsum + 360), 0.5 * (hsum - 360)))
    T = (1 - 0.17 * np.cos(np.radians(hpm - 30)) + 0.24 * np.cos(np.radians(2 * hpm))
         + 0.32 * np.cos(np.radians(3 * hpm + 6)) - 0.20 * np.cos(np.radians(4 * hpm - 63)))
    dtheta = 30 * np.exp(-((hpm - 275) / 25) ** 2)
    Rc = 2 * np.sqrt(Cpm ** 7 / (Cpm ** 7 + 25.0 ** 7))
    Sl = 1 + 0.015 * (Lpm - 50) ** 2 / np.sqrt(20 + (Lpm - 50) ** 2)
    Sc = 1 + 0.045 * Cpm
    Sh = 1 + 0.015 * Cpm * T
    Rt = -np.sin(np.radians(2 * dtheta)) * Rc
    return np.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2
                   + Rt * (dCp / Sc) * (dHp / Sh))


def lab_to_lch(lab):
    lab = np.asarray(lab, dtype=float)
    C = np.hypot(lab[..., 1], lab[..., 2])
    h = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360
    return lab[..., 0], C, h


def lch_to_lab(L, C, h):
    h = np.radians(np.asarray(h, dtype=float))
    return np.stack([np.asarray(L), np.asarray(C) * np.cos(h),
                     np.asarray(C) * np.sin(h)], axis=-1)
