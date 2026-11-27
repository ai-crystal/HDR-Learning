# -*- coding: utf-8 -*-
"""第 04 章专用辅助模块：CIECAM02 与 CAM16 正向模型。

公式来源：CIE 159:2004（CIECAM02）、Li et al. 2017 (CAM16, 14th CIC)。
XYZ 输入按 0–100 标度，白点 Yw = 100；LA 为适应亮度 cd/m²。
所有中间量按标准顺序计算，未做任何“便捷”简化。
"""
import numpy as np

# ---------------- 矩阵：CIE 标准给出 ---------------- #
M_CAT02 = np.array([[0.7328, 0.4296, -0.1624],
                    [-0.7036, 1.6975, 0.0061],
                    [0.0030, 0.0136, 0.9834]])
M_HPE = np.array([[0.38971, 0.68898, -0.07868],
                  [-0.22981, 1.18340, 0.04641],
                  [0.00000, 0.00000, 1.00000]])
# CAM16 的 CAT16 矩阵（单一矩阵，取代 CAT02 + HPE 两步）
M_CAT16 = np.array([[0.401288, 0.650173, -0.051461],
                    [-0.250268, 1.204414, 0.045854],
                    [-0.002079, 0.048952, 0.953127]])

# 环绕条件预设：(F, c, Nc)
SURROUND = {
    "average": (1.00, 0.69, 1.00),   # 平均环绕，如客厅、影厅
    "dim":     (0.90, 0.59, 0.95),   # 昏暗环绕
    "dark":    (0.80, 0.525, 0.80),  # 暗室
}


def xy_to_XYZ(x, y, Y=100.0):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    X = x * Y / y
    Z = (1.0 - x - y) * Y / y
    return np.stack([X, np.full_like(X, Y), Z], axis=-1)


def white_XYZ(name):
    """常用光源白点（CIE 1931 2°，Y = 100）。"""
    xy = {
        "A":    (0.44758, 0.40745),   # 2856 K 白炽灯 / 标准光源 A
        "D50":  (0.34567, 0.35850),   # 印刷观察
        "D65":  (0.31272, 0.32903),   # sRGB / BT.709 / BT.2020
        "DCI":  (0.31400, 0.35100),   # 数字影院
        "E":    (1 / 3, 1 / 3),
    }[name]
    return xy_to_XYZ(*xy, Y=100.0)


def _luminance_level(LA):
    """背景因子 k 与亮度因子 F_L。"""
    k = 1.0 / (5.0 * LA + 1.0)
    k4 = k ** 4
    FL = 0.2 * k4 * (5.0 * LA) + 0.1 * (1.0 - k4) ** 2 * (5.0 * LA) ** (1.0 / 3.0)
    return FL


def _compress(x, FL):
    """CIECAM02 的锥响应压缩，对负值取符号保持（避免 log/幂运算域错误）。"""
    xa = (FL * np.abs(x) / 100.0) ** 0.42
    return np.sign(x) * 400.0 * xa / (xa + 27.13) + 0.1


def cam02(XYZ, XYZ_w, LA=100.0, Yb=20.0, surround="average"):
    """CIECAM02 正向模型。

    参数
    ----
    XYZ   : (..., 3) 待测色的三刺激值，0–100 标度
    XYZ_w : (3,) 参考白（适应白）的三刺激值，Yw = 100
    LA    : 适应亮度 cd/m²
    Yb    : 背景亮度因数（相对 Yw = 100）
    surround : "average" / "dim" / "dark"

    返回 dict：J, Q, C, M, s, h, a, b, A, Aw, FL, D
    """
    XYZ = np.asarray(XYZ, dtype=float)
    XYZ_w = np.asarray(XYZ_w, dtype=float)
    F, c, Nc = SURROUND[surround]
    FL = _luminance_level(LA)
    Yw = XYZ_w[1]

    # 1) CAT02 色适应
    rgb = XYZ @ M_CAT02.T
    rgb_w = XYZ_w @ M_CAT02.T
    D = F * (1.0 - (1.0 / 3.6) * np.exp((-LA - 42.0) / 92.0))
    D = float(np.clip(D, 0.0, 1.0))
    scale = D * Yw / rgb_w + 1.0 - D
    rgb_c = rgb * scale

    # 2) 转回 XYZ，再进 Hunt-Pointer-Estevez 锥空间
    xyz_c = rgb_c @ np.linalg.inv(M_CAT02).T
    rgb_p = xyz_c @ M_HPE.T
    rgb_pw = (XYZ_w @ M_CAT02.T * scale) @ np.linalg.inv(M_CAT02).T @ M_HPE.T

    # 3) 非线性压缩
    rp = _compress(rgb_p, FL)
    rp_w = _compress(rgb_pw, FL)

    # 4) 对立色与色相
    Rap, Gap, Bap = rp[..., 0], rp[..., 1], rp[..., 2]
    a = Rap - 12.0 * Gap / 11.0 + Bap / 11.0
    b = (Rap + Gap - 2.0 * Bap) / 9.0
    h = np.degrees(np.arctan2(b, a)) % 360.0
    et = 0.25 * (np.cos(np.radians(h) + 2.0) + 3.8)

    # 5) 明度
    n = Yb / Yw
    Nbb = Ncb = 0.725 * (1.0 / n) ** 0.2      # 与背景诱导因子 n 有关，不是 Yw
    z = 1.48 + np.sqrt(n)
    A = (2.0 * Rap + Gap + Bap / 20.0 - 0.305) * Nbb
    Aw = (2.0 * rp_w[0] + rp_w[1] + rp_w[2] / 20.0 - 0.305) * Nbb
    J = 100.0 * np.power(np.clip(A / Aw, 1e-8, None), c * z)

    # 6) 亮度与色彩量
    Q = (4.0 / c) * np.sqrt(J / 100.0) * (Aw + 4.0) * FL ** 0.25
    denom = Rap + Gap + 21.0 * Bap / 20.0
    t = (50000.0 / 13.0 * Nc * Ncb * et * np.sqrt(a ** 2 + b ** 2)) / denom
    t = np.clip(t, 0.0, None)
    C = t ** 0.9 * np.sqrt(J / 100.0) * (1.64 - 0.29 ** n) ** 0.73
    M = C * FL ** 0.25
    s = 100.0 * np.sqrt(M / np.maximum(Q, 1e-9))

    return dict(J=J, Q=Q, C=C, M=M, s=s, h=h, a=a, b=b, A=A, Aw=Aw,
                FL=FL, D=D, Jp=J)


def cam16(XYZ, XYZ_w, LA=100.0, Yb=20.0, surround="average"):
    """CAM16 正向模型：CAT16 单矩阵适应，其余结构与 CIECAM02 相同。"""
    XYZ = np.asarray(XYZ, dtype=float)
    XYZ_w = np.asarray(XYZ_w, dtype=float)
    F, c, Nc = SURROUND[surround]
    FL = _luminance_level(LA)
    Yw = XYZ_w[1]

    rgb = XYZ @ M_CAT16.T
    rgb_w = XYZ_w @ M_CAT16.T
    D = float(np.clip(F * (1.0 - (1.0 / 3.6) * np.exp((-LA - 42.0) / 92.0)), 0.0, 1.0))
    scale = D * Yw / rgb_w + 1.0 - D
    rp = _compress(rgb * scale, FL)
    rp_w = _compress(rgb_w * scale, FL)

    Rap, Gap, Bap = rp[..., 0], rp[..., 1], rp[..., 2]
    a = Rap - 12.0 * Gap / 11.0 + Bap / 11.0
    b = (Rap + Gap - 2.0 * Bap) / 9.0
    h = np.degrees(np.arctan2(b, a)) % 360.0
    et = 0.25 * (np.cos(np.radians(h) + 2.0) + 3.8)

    n = Yb / Yw
    Nbb = Ncb = 0.725 * (1.0 / n) ** 0.2
    z = 1.48 + np.sqrt(n)
    A = (2.0 * Rap + Gap + Bap / 20.0 - 0.305) * Nbb
    Aw = (2.0 * rp_w[0] + rp_w[1] + rp_w[2] / 20.0 - 0.305) * Nbb
    J = 100.0 * np.power(np.clip(A / Aw, 1e-8, None), c * z)
    Q = (4.0 / c) * np.sqrt(J / 100.0) * (Aw + 4.0) * FL ** 0.25
    denom = Rap + Gap + 21.0 * Bap / 20.0
    t = (50000.0 / 13.0 * Nc * Ncb * et * np.sqrt(a ** 2 + b ** 2)) / denom
    t = np.clip(t, 0.0, None)
    C = t ** 0.9 * np.sqrt(J / 100.0) * (1.64 - 0.29 ** n) ** 0.73
    M = C * FL ** 0.25
    s = 100.0 * np.sqrt(M / np.maximum(Q, 1e-9))
    return dict(J=J, Q=Q, C=C, M=M, s=s, h=h, a=a, b=b, A=A, Aw=Aw,
                FL=FL, D=D)


def cam02_ucs(res):
    """CAM02-UCS（Luo, Cui, Li 2006）：J'、a'、b'，用于色差与色域体积。"""
    Jp = 1.7 * res["J"] / (1.0 + 0.007 * res["J"])
    Mp = np.log1p(0.0228 * res["M"]) / 0.0228
    h = np.radians(res["h"])
    return Jp, Mp * np.cos(h), Mp * np.sin(h)


# ============  扩写补充：色相四分之一圆 H、逆变换、CAM16-UCS  ============

def hue_quadrature(h):
    """色相四分之一圆 H（0–400）。输入色相角 h（度）。CIE 159:2004 式 (7.11)。

    标准里 h' 的取法：h < 20.14° 时 h' = h + 360°，落在最后一个区间
    （红锚点 20.14° 与下一轮红锚点 380.14° 之间），这样 H 才能连续覆盖
    0–400 而不出现负值。
    """
    h = np.asarray(h, dtype=float) % 360.0
    hi = np.array([20.14, 90.00, 164.25, 237.53, 380.14])
    ei = np.array([0.8, 0.7, 1.0, 1.2, 0.8])
    Hi = np.array([0.0, 100.0, 200.0, 300.0, 400.0])
    hp = np.where(h < hi[0], h + 360.0, h)
    idx = np.clip(np.searchsorted(hi, hp, side="right") - 1, 0, 3)
    num = (hp - hi[idx]) / ei[idx]
    den = num + (hi[idx + 1] - hp) / ei[idx + 1]
    return Hi[idx] + 100.0 * num / den


def _compress_inv(rap, FL):
    """锥响应压缩的逆：R_a -> R'（对负值做符号保持处理）。"""
    rap = np.asarray(rap, dtype=float)
    x = np.minimum(np.abs(rap - 0.1), 399.999)
    base = 100.0 / FL * (27.13 * x / (400.0 - x)) ** (1.0 / 0.42)
    return np.sign(rap - 0.1) * base


def _view(XYZ_w, LA, Yb, surround):
    F, c, Nc = SURROUND[surround]
    FL = _luminance_level(LA)
    Yw = XYZ_w[1]
    D = float(np.clip(F * (1.0 - (1.0 / 3.6) * np.exp((-LA - 42.0) / 92.0)), 0.0, 1.0))
    n = Yb / Yw
    Nbb = Ncb = 0.725 * (1.0 / n) ** 0.2
    z = 1.48 + np.sqrt(n)
    return dict(F=F, c=c, Nc=Nc, FL=FL, Yw=Yw, D=D, n=n, Nbb=Nbb, Ncb=Ncb, z=z)


def _ab_from_t(t, A, h, v, use_C=True):
    """由 t（或 C）与 h 解出 a、b。v 为 _view() 的返回。"""
    p1 = (50000.0 / 13.0) * v["Nc"] * v["Ncb"] * (0.25 * (np.cos(h + 2.0) + 3.8)) \
        / np.maximum(t, 1e-12)
    p2 = A / v["Nbb"] + 0.305
    p3 = 21.0 / 20.0
    s_h, c_h = np.sin(h), np.cos(h)
    k1 = (2.0 + p3) * 460.0 / 1403.0
    k2 = (2.0 + p3) * 220.0 / 1403.0
    big = np.abs(s_h) >= np.abs(c_h)
    with np.errstate(divide="ignore", invalid="ignore"):
        b_big = p2 * k1 / (p1 / s_h + k2 * c_h / s_h - 27.0 / 1403.0 + p3 * 6300.0 / 1403.0)
        a_sml = p2 * k1 / (p1 / c_h + k2 - (27.0 / 1403.0 - p3 * 6300.0 / 1403.0) * s_h / c_h)
    a = np.where(big, b_big * c_h / s_h, a_sml)
    b = np.where(big, b_big, a_sml * s_h / c_h)
    return np.where(np.isfinite(a), a, 0.0), np.where(np.isfinite(b), b, 0.0)


def cam16_inverse(J, C, h, XYZ_w, LA=100.0, Yb=20.0, surround="average"):
    """CAM16 逆变换：由 (J, C, h) 反解三刺激值 XYZ（0–100 标度）。"""
    J = np.atleast_1d(np.asarray(J, dtype=float))
    C = np.atleast_1d(np.asarray(C, dtype=float))
    h = np.radians(np.atleast_1d(np.asarray(h, dtype=float)))
    XYZ_w = np.asarray(XYZ_w, dtype=float)
    v = _view(XYZ_w, LA, Yb, surround)

    rgb_w = XYZ_w @ M_CAT16.T
    scale = v["D"] * v["Yw"] / rgb_w + 1.0 - v["D"]
    rp_w = _compress(rgb_w * scale, v["FL"])
    Aw = (2.0 * rp_w[0] + rp_w[1] + rp_w[2] / 20.0 - 0.305) * v["Nbb"]

    with np.errstate(divide="ignore", invalid="ignore"):
        t = (C / (np.sqrt(J / 100.0) * (1.64 - 0.29 ** v["n"]) ** 0.73)) ** (1.0 / 0.9)
    A = Aw * (J / 100.0) ** (1.0 / (v["c"] * v["z"]))
    a, b = _ab_from_t(t, A, h, v)

    p2 = A / v["Nbb"] + 0.305
    Ra = (460.0 * p2 + 451.0 * a + 288.0 * b) / 1403.0
    Ga = (460.0 * p2 - 891.0 * a - 261.0 * b) / 1403.0
    Ba = (460.0 * p2 - 220.0 * a - 6300.0 * b) / 1403.0
    rp = np.stack([_compress_inv(Ra, v["FL"]),
                   _compress_inv(Ga, v["FL"]),
                   _compress_inv(Ba, v["FL"])], axis=-1)
    rgb_c = rp / scale                       # CAM16 中适应与压缩在同一空间，直接除增益
    return rgb_c @ np.linalg.inv(M_CAT16).T


def cam16_ucs(res):
    """CAM16-UCS（Li et al. 2017）：J'、a'、b'。"""
    Jp = 1.7 * res["J"] / (1.0 + 0.007 * res["J"])
    Mp = np.log1p(0.0228 * res["M"]) / 0.0228
    h = np.radians(res["h"])
    return Jp, Mp * np.cos(h), Mp * np.sin(h)


def dE_ucs(p, q):
    """UCS 上的欧氏色差（CAM16-UCS 或 CAM02-UCS 均可）。"""
    return np.sqrt(sum((np.asarray(u) - np.asarray(w)) ** 2 for u, w in zip(p, q)))
