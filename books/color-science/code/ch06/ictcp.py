# -*- coding: utf-8 -*-
"""第 06 章专用辅助模块：BT.2020 的 YCbCr、ICtCp、PQ 与色差。

公式来源：
  ITU-R BT.2020-2（NCL YCbCr 系数）
  ITU-R BT.2100-2（ICtCp 矩阵与常数）
  SMPTE ST 2084（PQ）
  ITU-R BT.2124（ΔE_ITP）
"""
import numpy as np

M_2020 = np.array([[0.6370, 0.1446, 0.1689],
                   [0.2627, 0.6780, 0.0593],
                   [0.0000, 0.0281, 1.0610]])
M_2020_INV = np.linalg.inv(M_2020)

# BT.2100 的 LMS 变换（4 位小数定点，分母 4096）
M1 = np.array([[1688.0, 2146.0, 262.0],
               [683.0, 2951.0, 462.0],
               [99.0, 309.0, 3688.0]]) / 4096.0
M1_INV = np.linalg.inv(M1)


def pq_oetf(nit, peak=10000.0):
    """绝对亮度（cd/m²）-> PQ 码值 0..1。"""
    m1, m2 = 0.1593017578125, 78.84375
    c1, c2, c3 = 0.8359375, 18.8515625, 18.6875
    y = np.clip(np.asarray(nit, dtype=float) / peak, 0.0, 1.0)
    ym = y ** m1
    return ((c1 + c2 * ym) / (1.0 + c3 * ym)) ** m2


def pq_eotf(code, peak=10000.0):
    """PQ 码值 0..1 -> 绝对亮度（cd/m²）。"""
    m1, m2 = 0.1593017578125, 78.84375
    c1, c2, c3 = 0.8359375, 18.8515625, 18.6875
    p = np.clip(np.asarray(code, dtype=float), 0.0, 1.0) ** (1.0 / m2)
    return peak * (np.maximum(p - c1, 0.0) / (c2 - c3 * p)) ** (1.0 / m1)


def rgb_lin_to_ycbcr(rgb_lin, peak=1000.0):
    """线性 RGB（0..1，代表 peak 相对值）-> BT.2020 NCL YCbCr（PQ 域）。"""
    rp = pq_oetf(np.asarray(rgb_lin) * peak)
    y = 0.2627 * rp[..., 0] + 0.6780 * rp[..., 1] + 0.0593 * rp[..., 2]
    cb = (rp[..., 2] - y) / 1.8814
    cr = (rp[..., 0] - y) / 1.4746
    return np.stack([y, cb, cr], axis=-1)


def ycbcr_to_rgb_lin(ycbcr, peak=1000.0):
    y, cb, cr = ycbcr[..., 0], ycbcr[..., 1], ycbcr[..., 2]
    rp = y + 1.4746 * cr
    bp = y + 1.8814 * cb
    gp = (y - 0.2627 * rp - 0.0593 * bp) / 0.6780
    code = np.clip(np.stack([rp, gp, bp], axis=-1), 0.0, 1.0)
    return pq_eotf(code) / peak


def rgb_lin_to_ictcp(rgb_lin, peak=1000.0):
    """线性 RGB -> ICtCp（BT.2100）。"""
    rp = pq_oetf(np.asarray(rgb_lin) * peak)
    lms = rp @ M1.T
    L, M, S = lms[..., 0], lms[..., 1], lms[..., 2]
    I = 0.5 * L + 0.5 * M
    Ct = (6610.0 * L - 13613.0 * M + 7003.0 * S) / 4096.0
    Cp = (17933.0 * L - 17390.0 * M - 543.0 * S) / 4096.0
    return np.stack([I, Ct, Cp], axis=-1)


def ictcp_to_rgb_lin(ictcp, peak=1000.0):
    I, Ct, Cp = ictcp[..., 0], ictcp[..., 1], ictcp[..., 2]
    L = I + 0.008609037037932 * Ct + 0.111029625003026 * Cp
    M = I - 0.008609037037932 * Ct - 0.111029625003026 * Cp
    S = I + 0.560031335710601 * Ct - 0.320627174987318 * Cp
    lms = np.stack([L, M, S], axis=-1)
    rp = np.clip(lms @ M1_INV.T, 0.0, 1.0)
    return pq_eotf(rp) / peak


def deltaE_ITP(c1, c2):
    """BT.2124 的 ΔE_ITP。输入为 ICtCp 坐标。"""
    d = np.asarray(c1) - np.asarray(c2)
    return 720.0 * np.sqrt(d[..., 0] ** 2 + 0.25 * d[..., 1] ** 2 + d[..., 2] ** 2)


def rgb_lin_to_xyz(rgb_lin, peak=1000.0):
    return (np.asarray(rgb_lin) * peak) @ M_2020.T


def xyz_to_lab(XYZ, white=(0.95047, 1.0, 1.08883)):
    t = np.asarray(XYZ) / np.asarray(white)
    d = 6.0 / 29.0
    f = np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4.0 / 29.0)
    return np.stack([116 * f[..., 1] - 16,
                     500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], axis=-1)


def deltaE_2000(lab1, lab2):
    """CIEDE2000（kL = kC = kH = 1），支持单个色对与数组。"""
    lab1 = np.asarray(lab1, dtype=float)
    lab2 = np.asarray(lab2, dtype=float)
    L1, a1, b1 = lab1[..., 0], lab1[..., 1], lab1[..., 2]
    L2, a2, b2 = lab2[..., 0], lab2[..., 1], lab2[..., 2]
    C1, C2 = np.hypot(a1, b1), np.hypot(a2, b2)
    Cm = 0.5 * (C1 + C2)
    G = 0.5 * (1 - np.sqrt(Cm ** 7 / (Cm ** 7 + 25.0 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
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
    hpm = np.where(np.abs(h1p - h2p) <= 180, 0.5 * (h1p + h2p),
                   np.where(h1p + h2p < 360, 0.5 * (h1p + h2p + 360),
                            0.5 * (h1p + h2p - 360)))
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


# =====================  扩写补充：Jzazbz、绝对亮度 Lab、恒定亮度分析  =====================

def _pq_xyz(v):
    """Jzazbz 内部的 PQ 型压缩，输入已归一化到 10000。"""
    b, g = 1.15, 0.66
    c1, c2, c3 = 3424.0 / 4096.0, 2413.0 / 128.0, 2392.0 / 128.0
    n, p = 2610.0 / 16384.0, 1.7 * 2523.0 / 32.0
    x = np.clip(v, 0.0, None) ** n
    return ((c1 + c2 * x) / (1.0 + c3 * x)) ** p


def xyz_to_jzazbz(XYZ):
    """Safdar et al. 2017 的 Jzazbz（输入 XYZ，Y 为绝对亮度 cd/m²）。"""
    X, Y, Z = [np.asarray(c, dtype=float) for c in (XYZ[..., 0], XYZ[..., 1], XYZ[..., 2])]
    b, g = 1.15, 0.66
    d, d0 = -0.56, 1.6295499532821566e-11
    Xp = b * X - (b - 1.0) * Z
    Yp = g * Y - (g - 1.0) * X
    Zp = Z
    L = _pq_xyz(Xp / 10000.0)
    M = _pq_xyz(Yp / 10000.0)
    S = _pq_xyz(Zp / 10000.0)
    Iz = 0.5 * (L + M)
    az = 3.524000 * L - 4.066708 * M + 0.542708 * S
    bz = 0.199076 * L + 1.096799 * M - 1.295875 * S
    Jz = (1.0 + d) * Iz / (1.0 + d * Iz) - d0
    return np.stack([Jz, az, bz], axis=-1)


def deltaE_z(p, q):
    """ΔEz（Safdar et al. 2017）：Jzazbz 平面上的欧氏差。"""
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    dJ = p[..., 0] - q[..., 0]
    dC = np.hypot(p[..., 1], p[..., 2]) - np.hypot(q[..., 1], q[..., 2])
    dh = np.arctan2(p[..., 2], p[..., 1]) - np.arctan2(q[..., 2], q[..., 1])
    dHu = 2.0 * np.hypot(p[..., 1], p[..., 2]) * np.hypot(q[..., 1], q[..., 2]) \
        * np.sin(dh / 2.0)
    return np.sqrt(dJ ** 2 + dC ** 2 + dHu ** 2)


def pq_step(nbit, nit):
    """给定位深下，某个亮度处的相邻码值亮度差（cd/m²）。"""
    code = pq_oetf(nit)
    return pq_eotf(code + 1.0 / (2 ** nbit - 1)) - pq_eotf(code)
