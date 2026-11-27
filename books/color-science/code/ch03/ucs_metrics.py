# -*- coding: utf-8 -*-
"""第 03 章公用：CMC(l:c) 与 CIECAM02 / CAM02-UCS。

公式依据：
- CMC l:c（1984，Clarke, McDonald, Rigg），见 CIE 116-1995 附录；
- CIECAM02（CIE 159:2004），CAM02-UCS 的压缩式见 Luo, Cui, Li (2006)。
所有函数输入输出都用 0-100 标度的 XYZ，与 xyz_to_lab 的 0-1 标度不同，
de_ucs 内部会做换算。
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import colordiff as D

M_CAT02 = np.array([[0.7328, 0.4296, -0.1624],
                    [-0.7036, 1.6975, 0.0061],
                    [0.0030, 0.0136, 0.9834]])
M_HPE = np.array([[0.38971, 0.68898, -0.07868],
                  [-0.22981, 1.18340, 0.04641],
                  [0.0, 0.0, 1.0]])


def cmc(lab1, lab2, l=2.0, c=1.0):
    """CMC(l:c) 色差。参考色为 lab1。"""
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1 = float(np.hypot(a1, b1))
    C2 = float(np.hypot(a2, b2))
    dL = L2 - L1
    dC = C2 - C1
    dH = np.sqrt(max(0.0, (a2 - a1) ** 2 + (b2 - b1) ** 2 - dC ** 2))
    h1 = float(np.degrees(np.arctan2(b1, a1)) % 360)
    SL = 0.511 if L1 < 16 else 0.040975 * L1 / (1 + 0.01765 * L1)
    SC = 0.0638 * C1 / (1 + 0.0131 * C1) + 0.638
    F = np.sqrt(C1 ** 4 / (C1 ** 4 + 1900.0))
    if 164.0 <= h1 <= 345.0:
        T = 0.56 + abs(0.2 * np.cos(np.radians(h1 + 168.0)))
    else:
        T = 0.36 + abs(0.4 * np.cos(np.radians(h1 + 35.0)))
    SH = SC * (F * T + 1.0 - F)
    return float(np.sqrt((dL / (l * SL)) ** 2 + (dC / (c * SC)) ** 2
                         + (dH / SH) ** 2))


def viewing(XYZw, La=64.0, Yb=20.0, F=1.0, c=0.69, Nc=1.0):
    """给定白点（0-100 标度）与观察条件，返回 CIECAM02 的常数。"""
    XYZw = np.asarray(XYZw, float)
    rgbw = M_CAT02 @ XYZw
    Dp = float(np.clip(F * (1 - (1 / 3.6) * np.exp((-La - 42) / 92)), 0, 1))
    rgbwc = Dp * (100.0 / rgbw) + (1 - Dp) * 1.0
    k = 1.0 / (5 * La + 1)
    FL = 0.2 * k ** 4 * (5 * La) + 0.1 * (1 - k ** 4) ** 2 * (5 * La) ** (1 / 3)
    n = Yb / XYZw[1]
    z = 1.48 + np.sqrt(n)
    Nbb = Ncb = 0.725 * (1 / n) ** 0.2
    rgbp_w = M_HPE @ np.linalg.inv(M_CAT02) @ (rgbwc * rgbw)
    return dict(FL=FL, n=n, z=z, Nbb=Nbb, Ncb=Ncb, D=Dp, rgbwc=rgbwc,
                rgbp_w=rgbp_w, c=c, Nc=Nc)


def _nl(t, FL):
    t = np.asarray(t, float)
    p = np.abs(FL * t / 100.0) ** 0.42
    return np.sign(t) * 400.0 * p / (27.13 + p) + 0.1


def cam02(XYZ, V):
    """CIECAM02 前向：返回 J、C、h、M。XYZ 用 0-100 标度。"""
    FL = V["FL"]
    rgb = M_CAT02 @ np.asarray(XYZ, float)
    rgbp = M_HPE @ np.linalg.inv(M_CAT02) @ (V["rgbwc"] * rgb)
    rp, gp, bp = _nl(rgbp, FL)
    rpw, gpw, bpw = _nl(V["rgbp_w"], FL)
    Aw = (2 * rpw + gpw + 0.05 * bpw - 0.305) * V["Nbb"]
    a = rp - 12 * gp / 11 + bp / 11
    b = (rp + gp - 2 * bp) / 9
    h = float(np.degrees(np.arctan2(b, a)) % 360)
    et = 0.25 * (np.cos(np.radians(h) + 2) + 3.8)
    A = (2 * rp + gp + 0.05 * bp - 0.305) * V["Nbb"]
    J = 100 * (A / Aw) ** (V["c"] * V["z"])
    t = (50000 / 13 * V["Nc"] * V["Ncb"] * et * np.hypot(a, b)) / (
        rp + gp + 21 / 20 * bp)
    C = t ** 0.9 * np.sqrt(J / 100) * (1.64 - 0.29 ** V["n"]) ** 0.73
    return dict(J=float(J), C=float(C), h=h, M=float(C * FL ** 0.25))


def ucs(J, M):
    """CAM02-UCS 的压缩，c1=0.007，c2=0.0228。"""
    Jp = (1 + 100 * 0.007) * J / (1 + 0.007 * J)
    Mp = np.log(1 + 0.0228 * M) / 0.0228
    return float(Jp), float(Mp)


def de_ucs(V, lab1, lab2):
    """CAM02-UCS 下的欧氏色差（含色相项）。"""
    X1 = np.array(D.lab_to_xyz(*lab1), float) * 100.0
    X2 = np.array(D.lab_to_xyz(*lab2), float) * 100.0
    p1 = cam02(X1, V)
    p2 = cam02(X2, V)
    J1, M1 = ucs(p1["J"], p1["M"])
    J2, M2 = ucs(p2["J"], p2["M"])
    dh = p2["h"] - p1["h"]
    if dh > 180:
        dh -= 360
    elif dh < -180:
        dh += 360
    dH = 2 * np.sqrt(M1 * M2) * np.sin(np.radians(dh / 2))
    return float(np.sqrt((J2 - J1) ** 2 + (M2 - M1) ** 2 + dH ** 2))
