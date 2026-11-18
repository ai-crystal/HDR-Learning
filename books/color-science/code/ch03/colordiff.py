# -*- coding: utf-8 -*-
"""第 03 章公用模块：XYZ / Lab / Luv 换算与三种色差公式。

公式依据：CIE 15:2004（色度学）、CIE 1976 L*a*b* / L*u*v*、
CIE94（CIE 116-1995）、CIEDE2000（CIE 142-2001）。
"""
import numpy as np

# ---------------- 白点 D65 ----------------
XN, YN, ZN = 0.95047, 1.00000, 1.08883


def xy_to_XYZ(x, y, Y=0.5):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    return x * Y / y, np.full_like(x, Y), (1.0 - x - y) * Y / y


def xyz_to_lab(X, Y, Z, wp=(XN, YN, ZN)):
    Xn, Yn, Zn = wp

    def f(t):
        d = 6.0 / 29.0
        return np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4.0 / 29.0)

    fx, fy, fz = f(X / Xn), f(Y / Yn), f(Z / Zn)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def lab_to_xyz(L, a, b, wp=(XN, YN, ZN)):
    Xn, Yn, Zn = wp
    fy = (L + 16) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0

    def finv(t):
        d = 6.0 / 29.0
        return np.where(t > d, t ** 3, 3 * d * d * (t - 4.0 / 29.0))

    return Xn * finv(fx), Yn * finv(fy), Zn * finv(fz)


def xyz_to_luv(X, Y, Z, wp=(XN, YN, ZN)):
    Xn, Yn, Zn = wp
    d = X + 15 * Y + 3 * Z
    dn = Xn + 15 * Yn + 3 * Zn
    up, vp = 4 * X / d, 9 * Y / d
    upn, vpn = 4 * Xn / dn, 9 * Yn / dn
    yr = Y / Yn
    L = np.where(yr > (6 / 29) ** 3, 116 * np.cbrt(yr) - 16, (29 / 3) ** 3 * yr)
    return L, 13 * L * (up - upn), 13 * L * (vp - vpn)


def xyz_to_uvp(X, Y, Z):
    d = X + 15 * Y + 3 * Z
    return 4 * X / d, 9 * Y / d


# ---------------- 色差 ----------------
def de76(lab1, lab2):
    d = np.asarray(lab2, float) - np.asarray(lab1, float)
    return float(np.sqrt(np.sum(d ** 2)))


def de94(lab1, lab2, kL=1.0, kC=1.0, kH=1.0, K1=0.045, K2=0.015):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1 = np.hypot(a1, b1)
    C2 = np.hypot(a2, b2)
    dL = L2 - L1
    dC = C2 - C1
    dH2 = max(0.0, (a2 - a1) ** 2 + (b2 - b1) ** 2 - dC ** 2)
    dH = np.sqrt(dH2)
    SC = 1 + K1 * C1
    SH = 1 + K2 * C1
    return float(np.sqrt((dL / kL) ** 2 + (dC / (kC * SC)) ** 2
                         + (dH / (kH * SH)) ** 2))


def de2000(lab1, lab2, kL=1.0, kC=1.0, kH=1.0):
    L1, a1, b1 = [float(v) for v in lab1]
    L2, a2, b2 = [float(v) for v in lab2]
    C1 = np.hypot(a1, b1)
    C2 = np.hypot(a2, b2)
    Cbar = 0.5 * (C1 + C2)
    G = 0.5 * (1 - np.sqrt(Cbar ** 7 / (Cbar ** 7 + 25.0 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360

    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    else:
        dhp = h2p - h1p
        if dhp > 180:
            dhp -= 360
        elif dhp < -180:
            dhp += 360
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp / 2))

    Lbp = 0.5 * (L1 + L2)
    Cbp = 0.5 * (C1p + C2p)
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = 0.5 * (h1p + h2p)
    elif h1p + h2p < 360:
        hbp = 0.5 * (h1p + h2p + 360)
    else:
        hbp = 0.5 * (h1p + h2p - 360)

    T = (1 - 0.17 * np.cos(np.radians(hbp - 30))
         + 0.24 * np.cos(np.radians(2 * hbp))
         + 0.32 * np.cos(np.radians(3 * hbp + 6))
         - 0.20 * np.cos(np.radians(4 * hbp - 63)))
    dtheta = 30 * np.exp(-(((hbp - 275) / 25.0) ** 2))
    RC = 2 * np.sqrt(Cbp ** 7 / (Cbp ** 7 + 25.0 ** 7))
    SL = 1 + 0.015 * (Lbp - 50) ** 2 / np.sqrt(20 + (Lbp - 50) ** 2)
    SC = 1 + 0.045 * Cbp
    SH = 1 + 0.015 * Cbp * T
    RT = -np.sin(np.radians(2 * dtheta)) * RC

    t1 = dLp / (kL * SL)
    t2 = dCp / (kC * SC)
    t3 = dHp / (kH * SH)
    return float(np.sqrt(t1 ** 2 + t2 ** 2 + t3 ** 2 + RT * t2 * t3))


def de_itp(I1, Ct1, Cp1, I2, Ct2, Cp2):
    """BT.2124 ΔE_ITP，用于 HDR / 宽色域内容的色差度量。"""
    return float(720 * np.sqrt((I2 - I1) ** 2 + 0.25 * (Ct2 - Ct1) ** 2
                               + (Cp2 - Cp1) ** 2))
