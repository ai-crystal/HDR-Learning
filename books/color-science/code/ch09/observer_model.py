# -*- coding: utf-8 -*-
"""第 09 章辅助模块：色适应变换矩阵、生理学观察者的参数化模型。

数据与假设：
- 色匹配函数取自 CIE 1931 2° 标准观察者（5 nm，380–780 nm，见 cie1931.py）。
- 三种视锥基函数用 Smith–Pokorny (1975) 的线性变换，满足 l+m = ȳ。
- 晶状体光谱密度按 van Norren & Vos (1974) 的模板形状取锚点，
  以 550 nm 为 1 归一化（只给相对值），年龄修正用 Pokorny 等 (1987)
  的线性模型 D(λ,age) = D(λ,20) * (1 + 0.02 (age-20))。
- 黄斑色素用峰值 458 nm 的非对称高斯，光密度按个体在 0.15–0.60 之间取值。
- 锥体峰值位移用曲线在波长轴上重采样近似，L 取 ±3 nm，M 取 ±2 nm。

本模块只服务于本章插图，输出的数值是模型结果，不是实测数据。
"""
import numpy as np

import cie1931 as C

# 统一到 1 nm 网格，窄带光源才不会被 5 nm 采样漏掉
LAM = np.arange(380.0, 781.0, 1.0)
XBAR = np.interp(LAM, C.LAM, C.XBAR)
YBAR = np.interp(LAM, C.LAM, C.YBAR)
ZBAR = np.interp(LAM, C.LAM, C.ZBAR)
CMF_STD = np.stack([XBAR, YBAR, ZBAR], axis=1)   # (401, 3)

# ---------------- 色适应变换矩阵 ----------------
M_BFD = np.array([[0.8951, 0.2664, -0.1614],
                  [-0.7502, 1.7135, 0.0367],
                  [0.0389, -0.0685, 1.0296]])
M_CAT02 = np.array([[0.7328, 0.4296, -0.1624],
                    [-0.7036, 1.6975, 0.0061],
                    [0.0030, 0.0136, 0.9834]])
M_CAT16 = np.array([[0.401288, 0.650173, -0.051461],
                    [-0.250268, 1.204414, 0.045854],
                    [-0.002079, 0.048952, 0.953127]])
M_CMCCAT2000 = np.array([[0.7982, 0.3389, -0.1371],
                         [-0.5918, 1.5512, 0.0406],
                         [0.0008, 0.0239, 0.9753]])
M_HPE = np.array([[0.38971, 0.68898, -0.07868],
                  [-0.22981, 1.18340, 0.04641],
                  [0.0, 0.0, 1.0]])

CATS = {
    "Bradford": M_BFD,
    "CAT02": M_CAT02,
    "CAT16": M_CAT16,
    "CMCCAT2000": M_CMCCAT2000,
}

# ---------------- 白点 ----------------
D65 = np.array([0.95047, 1.0, 1.08883])
A_WH = np.array([1.09850, 1.0, 0.35585])
D50 = np.array([0.96422, 1.0, 0.82521])
E_WH = np.array([1.0, 1.0, 1.0])


def cmf_xyz(spd, cmf=None):
    """SPD 与色匹配函数的内积，5 nm 等间隔求和（单位间隔可约去）。"""
    if cmf is None:
        cmf = CMF_STD
    spd = np.asarray(spd, dtype=float)
    return spd @ cmf


def xyz_to_uv(X, Y, Z):
    """CIE 1976 u'v'。"""
    d = np.maximum(X + 15.0 * Y + 3.0 * Z, 1e-12)
    return 4.0 * X / d, 9.0 * Y / d


def cat_matrix(M, w_src, w_dst, D=1.0):
    """给定矩阵与两个白点、适应度 D，返回 3x3 适应矩阵。

    D=0 表示完全不适应（单位矩阵），D=1 为完全 von Kries。
    """
    M = np.asarray(M, dtype=float)
    rgb_s = M @ np.asarray(w_src, dtype=float)
    rgb_d = M @ np.asarray(w_dst, dtype=float)
    g = (rgb_d / rgb_s) ** D
    return np.linalg.inv(M) @ np.diag(g) @ M


def apply_cat(xyz, M, w_src, w_dst, D=1.0):
    """对一组 XYZ（N×3 或长度 3）做适应。"""
    A = cat_matrix(M, w_src, w_dst, D)
    return np.asarray(xyz, dtype=float) @ A.T


def xyz_to_xy(X, Y, Z):
    s = np.maximum(X + Y + Z, 1e-12)
    return X / s, Y / s


def xy_to_xyz(x, y, Y=1.0):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    Y = np.asarray(Y, dtype=float)
    return np.stack([x * Y / np.maximum(y, 1e-9),
                     Y * np.ones_like(x),
                     (1.0 - x - y) * Y / np.maximum(y, 1e-9)], axis=-1)


# ---------------- 晶状体与黄斑 ----------------
_LENS_NM = np.array([380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480,
                     490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590,
                     600, 620, 640, 660, 700, 780], dtype=float)
# 20 岁晶状体相对光谱密度（550 nm 记 0），按模板取锚点
_LENS_D = np.array([1.25, 1.10, 0.90, 0.70, 0.48, 0.36, 0.29, 0.24, 0.185,
                    0.14, 0.105, 0.088, 0.070, 0.055, 0.042, 0.033, 0.018,
                    0.000, -0.004, -0.007, -0.011, -0.016, -0.020, -0.026,
                    -0.030, -0.033, -0.038, -0.048])


def lens_density(age=20.0, lam=None):
    """晶状体相对光谱密度（550 nm 为 0）。"""
    if lam is None:
        lam = LAM
    base = np.interp(lam, _LENS_NM, _LENS_D)
    k = 1.0 + 0.02 * (float(age) - 20.0)
    return base * k


def lens_trans(age=20.0, lam=None):
    """晶状体相对光谱透过率，按 550 nm 归一。"""
    return 10.0 ** (-lens_density(age, lam))


def macular_density(od=0.35, lam=None):
    """黄斑色素光谱密度，峰值在 458 nm，短波侧下降更快。"""
    if lam is None:
        lam = LAM
    d = lam - 458.0
    sigma = np.where(d < 0, 20.0, 40.0)
    return float(od) * np.exp(-0.5 * (d / sigma) ** 2)


def macular_trans(od=0.35, lam=None):
    return 10.0 ** (-macular_density(od, lam))


# ---------------- 视锥基函数 ----------------
# Smith–Pokorny 线性变换，l+m = ȳ
SP = np.array([[0.15514, 0.54312, -0.03286],
               [-0.15514, 0.45684, 0.03286],
               [0.0, 0.0, 0.01608]])
SP_INV = np.linalg.inv(SP)


def cone_basis(cmf=None):
    """标准观察者的三条视锥基函数（LMS）。"""
    if cmf is None:
        cmf = CMF_STD
    return cmf @ SP.T


def _shift(curve, dlam):
    """把曲线沿波长轴平移 dlam（nm），线性插值，两端保持端点值。"""
    lam = LAM
    shifted = np.interp(lam - dlam, lam, curve)
    if dlam > 0:
        shifted[lam < lam[0] + dlam] = curve[0]
    elif dlam < 0:
        shifted[lam > lam[-1] + dlam] = curve[-1]
    return shifted


REF_AGE, REF_OD = 32.0, 0.35   # 标准观察者对应的参考密度（Smith–Pokorny 已含此平均值）


def observer_cmf(age=32.0, macular_od=0.35, l_shift=0.0, m_shift=0.0):
    """按参数生成一个观察者的 CMF（81×3）。

    Smith–Pokorny 基函数是角膜处的灵敏度，已经含了平均的晶状体与黄斑吸收，
    因此这里只乘相对于参考观察者的比值。
    l_shift/m_shift 为 L/M 锥峰值位移（nm），正数表示向长波移动。
    """
    lms = cone_basis()
    pre = (lens_trans(age) / lens_trans(REF_AGE)) *           (macular_trans(macular_od) / macular_trans(REF_OD))
    lms = lms * pre[:, None]
    if l_shift:
        lms[:, 0] = _shift(lms[:, 0], l_shift)
    if m_shift:
        lms[:, 1] = _shift(lms[:, 1], m_shift)
    cmf = lms @ SP_INV.T
    # 归一化：等能白下的 Y 记为 1
    y = np.sum(cmf[:, 1])
    return cmf / max(y, 1e-12)


def all_equal(value, n):
    return np.full(n, float(value))
