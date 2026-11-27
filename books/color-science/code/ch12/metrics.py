# -*- coding: utf-8 -*-
"""第 12 章辅助模块：四种 HDR 色差度量的统一实现。

复用第 06 章 ictcp.py 里的 PQ、ICtCp、Jzazbz、CIEDE2000，另加：
  * CAM16 前向模型与 CAM16-UCS 的 ΔE'
  * CIELAB 的反算（L*, a*, b* -> 绝对 XYZ）
  * BT.2020 线性 RGB <-> XYZ
  * 从绝对 XYZ 直接得到 ICtCp / Jzazbz 的封装

参考：
  ITU-R BT.2100-2 / BT.2124（ICtCp、ΔE_ITP）
  Safdar et al., "Perceptually uniform color space for image signals
      including high dynamic range and wide gamut", Opt. Express 25(13), 2017
  Li et al., "Comprehensive color solutions: CAM16, CAT16, and CAM16-UCS",
      Color Res. Appl. 42(6), 2017
  CIE 248:2022（CAM16 的正式标准文本）
"""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ch06"))
import ictcp as I  # noqa: E402

# BT.2020 线性 RGB -> XYZ（与 ictcp.py 同一张矩阵）
M_2020 = I.M_2020
M_2020_INV = I.M_2020_INV

WHITE_D65 = np.array([0.95047, 1.0, 1.08883])


# ---------------------------------------------------------------- CIELAB
def lab_to_xyz(lab, white_ref=203.0, white=WHITE_D65):
    """CIELAB -> 绝对 XYZ。Y_n = white_ref（cd/m²），L* 可以超过 100。"""
    lab = np.asarray(lab, dtype=float)
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    fy = (L + 16.0) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0
    d = 6.0 / 29.0

    def finv(t):
        return np.where(t > d, t ** 3, 3 * d * d * (t - 4.0 / 29.0))

    return np.stack([white[0] * finv(fx), white[1] * finv(fy),
                     white[2] * finv(fz)], axis=-1) * white_ref


def xyz_to_lab(XYZ, white_ref=203.0, white=WHITE_D65):
    return I.xyz_to_lab(np.asarray(XYZ) / white_ref, white=white)


def lch_to_lab(L, C, h_deg):
    h = np.radians(np.asarray(h_deg, dtype=float))
    return np.stack([np.asarray(L, dtype=float) + 0 * C,
                     C * np.cos(h), C * np.sin(h)], axis=-1)


# ---------------------------------------------------------------- ICtCp
def xyz_to_ictcp(XYZ):
    """绝对 XYZ（cd/m²）-> ICtCp。超出 BT.2020 色域的点返回 NaN。"""
    XYZ = np.asarray(XYZ, dtype=float)
    rgb = XYZ @ M_2020_INV.T          # 绝对亮度下的线性 RGB
    ok = np.all(rgb >= 0, axis=-1)
    rgb_safe = np.clip(rgb, 0.0, None) / 10000.0
    out = I.rgb_lin_to_ictcp(rgb_safe, peak=10000.0)
    return np.where(ok[..., None], out, np.nan)


def deltaE_ITP_xyz(x1, x2):
    return I.deltaE_ITP(xyz_to_ictcp(x1), xyz_to_ictcp(x2))


# ---------------------------------------------------------------- Jzazbz
def xyz_to_jz(xyz):
    return I.xyz_to_jzazbz(np.asarray(xyz, dtype=float))


def deltaE_z_xyz(x1, x2):
    return I.deltaE_z(xyz_to_jz(x1), xyz_to_jz(x2))


# ---------------------------------------------------------------- CAM16
M16 = np.array([[0.401288, 0.650173, -0.051461],
                [-0.250268, 1.204414, 0.045854],
                [-0.002079, 0.048952, 0.953127]])


def _adapt(rgb, FL):
    x = (FL * np.clip(rgb, 0.0, None) / 100.0) ** 0.42
    return 400.0 * x / (x + 27.13) + 0.1


class CAM16(object):
    """固定观察条件下的 CAM16 前向模型。XYZ 用绝对单位（cd/m²）。"""

    def __init__(self, white_xyz=(0.95047, 1.0, 1.08883), white_lum=203.0,
                 L_A=40.0, Y_b=20.0, surround=(1.0, 0.69, 1.0)):
        self.Y_w = white_lum
        self.XYZ_w = np.asarray(white_xyz, dtype=float) * white_lum
        F, c, Nc = surround
        self.c, self.Nc = c, Nc
        D = F * (1.0 - np.exp((-L_A - 42.0) / 92.0) / 3.6)
        self.D = float(np.clip(D, 0.0, 1.0))

        k = 1.0 / (5.0 * L_A + 1.0)
        self.FL = (0.2 * k ** 4 * (5.0 * L_A)
                   + 0.1 * (1.0 - k ** 4) ** 2 * (5.0 * L_A) ** (1.0 / 3.0))

        n = Y_b / self.Y_w
        self.n = n
        self.z = 1.48 + np.sqrt(n)
        self.Nbb = 0.725 * n ** -0.2
        self.Ncb = self.Nbb

        rgb_w = M16 @ self.XYZ_w
        self.D_RGB = self.D * self.Y_w / rgb_w + 1.0 - self.D
        rgb_wc = self.D_RGB * rgb_w
        rw, gw, bw = _adapt(rgb_wc, self.FL)
        self.A_w = (2.0 * rw + gw + 0.05 * bw - 0.305) * self.Nbb

    def forward(self, xyz):
        xyz = np.asarray(xyz, dtype=float)
        rgb = xyz @ M16.T
        rgb_c = self.D_RGB * rgb
        ra, ga, ba = np.moveaxis(_adapt(rgb_c, self.FL), -1, 0)
        a = ra - 12.0 * ga / 11.0 + ba / 11.0
        b = (ra + ga - 2.0 * ba) / 9.0
        h = np.degrees(np.arctan2(b, a)) % 360.0
        A = (2.0 * ra + ga + 0.05 * ba - 0.305) * self.Nbb
        J = 100.0 * np.power(np.clip(A / self.A_w, 0.0, None), self.c * self.z)
        Q = (4.0 / self.c) * np.sqrt(J / 100.0) * (self.A_w + 4.0) * self.FL ** 0.25
        t = (50000.0 / 13.0 * self.Nc * self.Ncb
             * (0.25 * (np.cos(np.radians(h) + 2.0) + 3.8))
             * np.hypot(a, b)) / (ra + ga + 21.0 / 20.0 * ba + 1e-12)
        t = np.clip(t, 0.0, None)
        C = t ** 0.9 * np.sqrt(J / 100.0) * (1.64 - 0.29 ** self.n) ** 0.73
        M = C * self.FL ** 0.25
        return dict(J=J, Q=Q, C=C, M=M, h=h)


def cam16_ucs(cam):
    """CAM16-UCS：J'、M' 与 (a', b')。KL=1, c1=0.007, c2=0.0228。"""
    c1, c2 = 0.007, 0.0228
    Jp = (1.0 + 100.0 * c1) * cam["J"] / (1.0 + c1 * cam["J"])
    Mp = np.log(1.0 + c2 * cam["M"]) / c2
    h = np.radians(cam["h"])
    return dict(Jp=Jp, Mp=Mp, ap=Mp * np.cos(h), bp=Mp * np.sin(h), h=cam["h"])


def deltaE_CAM16UCS(xyz1, xyz2, model):
    u1 = cam16_ucs(model.forward(xyz1))
    u2 = cam16_ucs(model.forward(xyz2))
    return np.sqrt((u1["Jp"] - u2["Jp"]) ** 2
                   + (u1["ap"] - u2["ap"]) ** 2
                   + (u1["bp"] - u2["bp"]) ** 2)


# ---------------------------------------------------------------- 统一接口
class Metrics(object):
    """四种度量的统一封装，观察条件一次性设定。"""

    def __init__(self, white_lum=203.0, L_A=None, Y_b=20.0):
        self.white_lum = white_lum
        self.cam = CAM16(white_lum=white_lum,
                         L_A=0.2 * white_lum if L_A is None else L_A,
                         Y_b=Y_b)

    def lab(self, xyz):
        return xyz_to_lab(xyz, white_ref=self.white_lum)

    def all(self, xyz1, xyz2):
        d00 = float(I.deltaE_2000(self.lab(xyz1), self.lab(xyz2)))
        ditp = float(I.deltaE_ITP(xyz_to_ictcp(xyz1), xyz_to_ictcp(xyz2)))
        dez = float(I.deltaE_z(xyz_to_jz(xyz1), xyz_to_jz(xyz2)))
        dec = float(deltaE_CAM16UCS(xyz1, xyz2, self.cam))
        return dict(dE00=d00, dEITP=ditp, dEz=dez, dEu=dec)


def hue_in(space, xyz, model):
    """返回某个空间里该颜色的色相角（度）。space 取 00 / 16 / jz / itp。"""
    if space == "00":
        lab = model.lab(xyz)
        C = np.hypot(lab[..., 1], lab[..., 2])
        G = 0.5 * (1.0 - np.sqrt(C ** 7 / (C ** 7 + 25.0 ** 7)))
        return np.degrees(np.arctan2(lab[..., 2], (1.0 + G) * lab[..., 1])) % 360
    if space == "16":
        return model.cam.forward(xyz)["h"]
    if space == "jz":
        jz = xyz_to_jz(xyz)
        return np.degrees(np.arctan2(jz[..., 2], jz[..., 1])) % 360
    if space == "itp":
        it = xyz_to_ictcp(xyz)
        return np.degrees(np.arctan2(it[..., 2], it[..., 1])) % 360
    raise ValueError(space)
