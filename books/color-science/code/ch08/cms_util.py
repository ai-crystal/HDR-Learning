# -*- coding: utf-8 -*-
"""第 08 章绘图共用的小工具：矩阵、Lab、CIEDE2000、u'v' 面积覆盖率。

所有数值都由标准公式算出，不含任何实测数据。
"""
import numpy as np

# ---- sRGB 与 Display P3 的 RGB->XYZ 矩阵（D65，BT.709 / DCI-P3 基色） ----
M_SRGB = np.array([[0.4123908, 0.3575843, 0.1804808],
                   [0.2126390, 0.7151687, 0.0721923],
                   [0.0193308, 0.1191948, 0.9505322]])

M_P3 = np.array([[0.4865709, 0.2656677, 0.1982173],
                 [0.2289746, 0.6917385, 0.0792869],
                 [0.0000000, 0.0451134, 1.0439444]])

M_2020 = np.array([[0.6369580, 0.1446169, 0.1688810],
                   [0.2627002, 0.6779981, 0.0593017],
                   [0.0000000, 0.0280727, 1.0609851]])

WHITE_D65 = np.array([0.9504559, 1.0, 1.0890578])
WHITE_D50 = np.array([0.96422, 1.0, 0.82521])


def srgb_eotf(v):
    v = np.asarray(v, dtype=float)
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def srgb_oetf(l):
    l = np.asarray(l, dtype=float)
    l = np.clip(l, 0.0, 1.0)
    return np.where(l <= 0.0031308, l * 12.92, 1.055 * l ** (1 / 2.4) - 0.055)


def xyz_to_lab(xyz, white=WHITE_D65):
    xyz = np.asarray(xyz, dtype=float)
    t = xyz / white
    d = 6.0 / 29.0

    def f(t):
        return np.where(t > d ** 3, np.cbrt(t), t / (3 * d ** 2) + 4.0 / 29.0)

    fx, fy, fz = f(t[..., 0]), f(t[..., 1]), f(t[..., 2])
    return np.stack([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)], axis=-1)


def lab_to_xyz(lab, white=WHITE_D65):
    lab = np.asarray(lab, dtype=float)
    fy = (lab[..., 0] + 16) / 116.0
    fx = fy + lab[..., 1] / 500.0
    fz = fy - lab[..., 2] / 200.0
    d = 6.0 / 29.0

    def finv(t):
        return np.where(t > d, t ** 3, 3 * d ** 2 * (t - 4.0 / 29.0))

    return np.stack([finv(fx), finv(fy), finv(fz)], axis=-1) * white


def delta_e00(lab1, lab2):
    """CIEDE2000，Sharma 2005 的实现，向量化。"""
    L1, a1, b1 = lab1[..., 0], lab1[..., 1], lab1[..., 2]
    L2, a2, b2 = lab2[..., 0], lab2[..., 1], lab2[..., 2]
    C1 = np.hypot(a1, b1)
    C2 = np.hypot(a2, b2)
    Cm = 0.5 * (C1 + C2)
    G = 0.5 * (1 - np.sqrt(Cm ** 7 / (Cm ** 7 + 25.0 ** 7)))
    a1p = (1 + G) * a1
    a2p = (1 + G) * a2
    C1p = np.hypot(a1p, b1)
    C2p = np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360
    dLp = L2 - L1
    dCp = C2p - C1p
    dhp = h2p - h1p
    dhp = np.where(dhp > 180, dhp - 360, np.where(dhp < -180, dhp + 360, dhp))
    dhp = np.where(C1p * C2p == 0, 0.0, dhp)
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp / 2))
    Lpm = 0.5 * (L1 + L2)
    Cpm = 0.5 * (C1p + C2p)
    hpm = np.where(C1p * C2p == 0, h1p + h2p,
                   np.where(np.abs(h1p - h2p) <= 180, 0.5 * (h1p + h2p),
                            np.where(h1p + h2p < 360, 0.5 * (h1p + h2p) + 180,
                                     0.5 * (h1p + h2p) - 180)))
    T = (1 - 0.17 * np.cos(np.radians(hpm - 30))
         + 0.24 * np.cos(np.radians(2 * hpm))
         + 0.32 * np.cos(np.radians(3 * hpm + 6))
         - 0.20 * np.cos(np.radians(4 * hpm - 63)))
    dtheta = 30 * np.exp(-(((hpm - 275) / 25) ** 2))
    RC = 2 * np.sqrt(Cpm ** 7 / (Cpm ** 7 + 25.0 ** 7))
    SL = 1 + 0.015 * (Lpm - 50) ** 2 / np.sqrt(20 + (Lpm - 50) ** 2)
    SC = 1 + 0.045 * Cpm
    SH = 1 + 0.015 * Cpm * T
    RT = -np.sin(np.radians(2 * dtheta)) * RC
    return np.sqrt((dLp / SL) ** 2 + (dCp / SC) ** 2 + (dHp / SH) ** 2
                   + RT * (dCp / SC) * (dHp / SH))


# ---- u'v' 1976 ----
def xyz_to_uv(xyz):
    xyz = np.asarray(xyz, dtype=float)
    X, Y, Z = xyz[..., 0], xyz[..., 1], xyz[..., 2]
    den = X + 15 * Y + 3 * Z
    return np.stack([4 * X / den, 9 * Y / den], axis=-1)


def primaries_uv(xy_list):
    out = []
    for x, y in xy_list:
        out.append(xyz_to_uv(np.array([x / y, 1.0, (1 - x - y) / y])))
    return np.array(out)


def poly_area(p):
    x, y = p[:, 0], p[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def clip_poly(subject, clip):
    """Sutherland-Hodgman，两个凸多边形求交。"""
    def inside(p, a, b):
        return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0

    def inter(p1, p2, a, b):
        dx1, dy1 = p2[0] - p1[0], p2[1] - p1[1]
        dx2, dy2 = b[0] - a[0], b[1] - a[1]
        den = dx1 * dy2 - dy1 * dx2
        t = ((a[0] - p1[0]) * dy2 - (a[1] - p1[1]) * dx2) / den
        return np.array([p1[0] + t * dx1, p1[1] + t * dy1])

    output = list(subject)
    for i in range(len(clip)):
        a, b = clip[i], clip[(i + 1) % len(clip)]
        if not output:
            break
        inp, output = output, []
        s = inp[-1]
        for e in inp:
            if inside(e, a, b):
                if not inside(s, a, b):
                    output.append(inter(s, e, a, b))
                output.append(e)
            elif inside(s, a, b):
                output.append(inter(s, e, a, b))
            s = e
    return np.array(output)


def coverage(ref_uv, disp_uv):
    """显示色域对参考色域的 u'v' 面积覆盖率（0..1）。"""
    inter = clip_poly(disp_uv, ref_uv)
    if len(inter) < 3:
        return 0.0
    return poly_area(inter) / poly_area(ref_uv)
