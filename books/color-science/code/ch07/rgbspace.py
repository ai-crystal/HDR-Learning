# -*- coding: utf-8 -*-
"""第 07 章专用辅助模块：RGB 空间的构造、传递函数与色差。

基色与白点坐标取自公开标准：
  sRGB / BT.709      IEC 61966-2-1、ITU-R BT.709-6
  Adobe RGB (1998)   Adobe Systems, 1998
  DCI-P3             SMPTE RP 431-2；Display P3 为同基色 + D65
  BT.2020            ITU-R BT.2020-2
  ACES AP0 / AP1     SMPTE ST 2065-1（AP0）、S-2014-004（AP1），白点 D60
  ProPhoto RGB       ISO 22028-2（ROMM RGB），白点 D50
  Adobe Wide Gamut   Adobe Systems, 1998，白点 D50
传递函数：IEC 61966-2-1（sRGB）、BT.709、BT.2020、SMPTE ST 2084（PQ）、
BT.2100（HLG）、ARRI LogC3（SUP 3.x，EI 800）。
"""
import numpy as np

# ---------------- 基色与白点（CIE 1931 xy） ----------------
PRIMARIES = {
    "sRGB":    {"R": (0.640, 0.330), "G": (0.300, 0.600), "B": (0.150, 0.060),
                "white": "D65", "tf": "sRGB 分段", "note": "网络与桌面"},
    "AdobeRGB": {"R": (0.640, 0.330), "G": (0.210, 0.710), "B": (0.150, 0.060),
                 "white": "D65", "tf": "gamma 2.2", "note": "印刷与摄影"},
    "P3":      {"R": (0.680, 0.320), "G": (0.265, 0.690), "B": (0.150, 0.060),
                "white": "DCI", "tf": "gamma 2.6", "note": "数字影院"},
    "DisplayP3": {"R": (0.680, 0.320), "G": (0.265, 0.690), "B": (0.150, 0.060),
                  "white": "D65", "tf": "sRGB 分段", "note": "消费广色域"},
    "BT2020":  {"R": (0.708, 0.292), "G": (0.170, 0.797), "B": (0.131, 0.046),
                "white": "D65", "tf": "BT.2020 / PQ / HLG", "note": "UHDTV"},
    "AP0":     {"R": (0.7347, 0.2653), "G": (0.0000, 1.0000), "B": (0.0001, -0.0770),
                "white": "D60", "tf": "线性", "note": "ACES 存档交换"},
    "AP1":     {"R": (0.713, 0.293), "G": (0.165, 0.830), "B": (0.128, 0.044),
                "white": "D60", "tf": "线性", "note": "ACES 工作空间"},
    "ProPhoto": {"R": (0.734699, 0.265301), "G": (0.159597, 0.840403),
                 "B": (0.036598, 0.000105), "white": "D50", "tf": "gamma 1.8", "note": "ROMM 存档"},
    "WideGamut": {"R": (0.7347, 0.2653), "G": (0.1152, 0.8264), "B": (0.1566, 0.0177),
                  "white": "D50", "tf": "gamma 2.2", "note": "Adobe 广色域"},
}

WHITE = {
    "A":   (0.44758, 0.40745),
    "D50": (0.34570, 0.35850),
    "D55": (0.33243, 0.34744),
    "D60": (0.32168, 0.33767),
    "D65": (0.31271, 0.32902),
    "DCI": (0.31400, 0.35100),
    "E":   (1 / 3, 1 / 3),
}


def xy_to_XYZ(x, y, Y=1.0):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    z = 1.0 - x - y
    return np.stack([x * Y / y, np.full_like(x, Y), z * Y / y], axis=-1)


def primary_matrix(prim):
    """三个基色各自归一化到 Y=1 时的 XYZ 矩阵（列 = 基色）。"""
    cols = [xy_to_XYZ(*prim[k], 1.0) for k in "RGB"]
    return np.array(cols).T


def rgb_to_xyz_matrix(name, white=None):
    """由基色坐标与白点构造 RGB->XYZ 矩阵，白点归一化到 Y=1。"""
    prim = PRIMARIES[name]
    P = primary_matrix(prim)
    wn = white or prim["white"]
    W = xy_to_XYZ(*WHITE[wn], 1.0)
    S = np.linalg.solve(P, W)          # 三个基色的亮度系数
    return P * S, S


def bradford_matrix(src="D65", dst="D50"):
    """Bradford 色适应矩阵（白点 xy -> 完整适应）。"""
    M = np.array([[0.8951, 0.2664, -0.1614],
                  [-0.7502, 1.7135, 0.0367],
                  [0.0389, -0.0685, 1.0296]])
    ws = M @ xy_to_XYZ(*WHITE[src], 1.0)
    wd = M @ xy_to_XYZ(*WHITE[dst], 1.0)
    return np.linalg.inv(M) @ np.diag(wd / ws) @ M


# ---------------- 传递函数 ----------------
def gamma_oetf(x, g=2.2):
    return np.asarray(x, dtype=float) ** (1.0 / g)


def gamma_eotf(v, g=2.2):
    return np.asarray(v, dtype=float) ** g


def srgb_oetf(x):
    x = np.asarray(x, dtype=float)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(np.maximum(x, 0), 1 / 2.4) - 0.055)


def srgb_eotf(v):
    v = np.asarray(v, dtype=float)
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def rec709_oetf(x):
    x = np.asarray(x, dtype=float)
    return np.where(x < 0.018, 4.5 * x, 1.099 * np.power(np.maximum(x, 0), 0.45) - 0.099)


def rec2020_oetf(x):
    x = np.asarray(x, dtype=float)
    return np.where(x < 0.0181, 4.5 * x, 1.0993 * np.power(np.maximum(x, 0), 0.45) - 0.0993)


def pq_oetf(nit):
    m1, m2 = 0.1593017578125, 78.84375
    c1, c2, c3 = 0.8359375, 18.8515625, 18.6875
    y = np.clip(np.asarray(nit, dtype=float), 0, 10000) / 10000.0
    ym = y ** m1
    return ((c1 + c2 * ym) / (1.0 + c3 * ym)) ** m2


def pq_eotf(code):
    m1, m2 = 0.1593017578125, 78.84375
    c1, c2, c3 = 0.8359375, 18.8515625, 18.6875
    p = np.clip(np.asarray(code, dtype=float), 0, 1) ** (1.0 / m2)
    return 10000.0 * (np.maximum(p - c1, 0) / (c2 - c3 * p)) ** (1.0 / m1)


def hlg_oetf(x):
    a, b, c = 0.17883277, 0.28466892, 0.55991073
    x = np.asarray(x, dtype=float)
    arg = np.maximum(12 * x - b, 1e-6)
    return np.where(x <= 1 / 12, np.sqrt(3 * x), a * np.log(arg) + c)


def logc3_oetf(x, ei=800):
    """ARRI LogC3（SUP 3.x）在 EI 800 下的编码曲线。"""
    x = np.asarray(x, dtype=float)
    cut = 0.010591
    a, b, c, d = 5.555556, 0.052272, 0.247190, 0.385537
    e, f = 5.367655, 0.092809
    return np.where(x > cut, np.log10(a * np.maximum(x, 1e-8) + b) * c + d, e * x + f)


# ---------------- 色差 ----------------
def XYZ_to_Lab(XYZ, white="D65"):
    W = xy_to_XYZ(*WHITE[white], 1.0)
    t = np.asarray(XYZ, dtype=float) / W
    d = 6.0 / 29.0

    def f(u):
        return np.where(u > d ** 3, np.cbrt(np.maximum(u, 0)), u / (3 * d * d) + 4.0 / 29.0)

    fx, fy, fz = f(t[..., 0]), f(t[..., 1]), f(t[..., 2])
    return np.stack([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)], axis=-1)


def de2000(lab1, lab2, kL=1.0, kC=1.0, kH=1.0):
    lab1 = np.asarray(lab1, dtype=float)
    lab2 = np.asarray(lab2, dtype=float)
    L1, a1, b1 = lab1[..., 0], lab1[..., 1], lab1[..., 2]
    L2, a2, b2 = lab2[..., 0], lab2[..., 1], lab2[..., 2]
    C1 = np.hypot(a1, b1)
    C2 = np.hypot(a2, b2)
    Cm = 0.5 * (C1 + C2)
    G = 0.5 * (1 - np.sqrt(Cm ** 7 / (Cm ** 7 + 25.0 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360
    dLp = L2 - L1
    dCp = C2p - C1p
    dhp = h2p - h1p
    dhp = np.where(dhp > 180, dhp - 360, dhp)
    dhp = np.where(dhp < -180, dhp + 360, dhp)
    dhp = np.where(np.abs(C1p * C2p) < 1e-12, 0.0, dhp)
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp) / 2)
    Lpm = 0.5 * (L1 + L2)
    Cpm = 0.5 * (C1p + C2p)
    hsum = h1p + h2p
    hpm = np.where(np.abs(h1p - h2p) > 180, (hsum + 360) / 2, hsum / 2)
    hpm = np.where(np.abs(C1p * C2p) < 1e-12, hsum, hpm)
    T = (1 - 0.17 * np.cos(np.radians(hpm - 30)) + 0.24 * np.cos(np.radians(2 * hpm))
         + 0.32 * np.cos(np.radians(3 * hpm + 6)) - 0.20 * np.cos(np.radians(4 * hpm - 63)))
    dth = 30 * np.exp(-((hpm - 275) / 25) ** 2)
    RC = 2 * np.sqrt(Cpm ** 7 / (Cpm ** 7 + 25.0 ** 7))
    SL = 1 + 0.015 * (Lpm - 50) ** 2 / np.sqrt(20 + (Lpm - 50) ** 2)
    SC = 1 + 0.045 * Cpm
    SH = 1 + 0.015 * Cpm * T
    RT = -np.sin(np.radians(2 * dth)) * RC
    return np.sqrt((dLp / (kL * SL)) ** 2 + (dCp / (kC * SC)) ** 2
                   + (dHp / (kH * SH)) ** 2 + RT * (dCp / (kC * SC)) * (dHp / (kH * SH)))


def xy_to_uv76(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    den = -2 * x + 12 * y + 3
    return 4 * x / den, 9 * y / den
