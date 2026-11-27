# -*- coding: utf-8 -*-
"""第 10 章专用辅助模块：色域边界描述（GBD）、边界求交、裁剪与压缩类映射算法。

基色与白点取自公开标准（IEC 61966-2-1、SMPTE RP 431-2、ITU-R BT.2020-2），
矩阵由基色坐标与白点解析求得，所有数值可复算。
Lab 采用 CIE 1976 L*a*b*，参考白为 D65（Y_n = 1）。
"""
import numpy as np

WHITE_D65 = (0.3127, 0.3290)

PRIMARIES = {
    "sRGB":   {"R": (0.640, 0.330), "G": (0.300, 0.600), "B": (0.150, 0.060)},
    "P3":     {"R": (0.680, 0.320), "G": (0.265, 0.690), "B": (0.150, 0.060)},
    "BT2020": {"R": (0.708, 0.292), "G": (0.170, 0.797), "B": (0.131, 0.046)},
}


def xy_to_xyz(x, y, Y=1.0):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    return np.stack([x * Y / y, np.full_like(x, Y), (1.0 - x - y) * Y / y], axis=-1)


def rgb_to_xyz_matrix(prim, white=WHITE_D65):
    """由基色 xy 与白点 xy 构造 RGB(线性) -> XYZ 矩阵，白点 Y = 1。"""
    P = np.array([xy_to_xyz(*prim["R"]), xy_to_xyz(*prim["G"]),
                  xy_to_xyz(*prim["B"])]).T
    W = xy_to_xyz(*white, 1.0)
    S = np.linalg.solve(P, W)
    return P * S


MATS = {k: rgb_to_xyz_matrix(v) for k, v in PRIMARIES.items()}
INV_MATS = {k: np.linalg.inv(v) for k, v in MATS.items()}
WP = xy_to_xyz(*WHITE_D65, 1.0)


# ---------------- Lab / LCh ----------------
def f_lab(t):
    d = 6.0 / 29.0
    t = np.asarray(t, dtype=float)
    return np.where(t > d ** 3, np.cbrt(np.maximum(t, 0.0)), t / (3 * d * d) + 4.0 / 29.0)


def f_inv(t):
    d = 6.0 / 29.0
    t = np.asarray(t, dtype=float)
    return np.where(t > d, t ** 3, 3 * d * d * (t - 4.0 / 29.0))


def xyz_to_lab(XYZ):
    t = np.asarray(XYZ, dtype=float) / WP
    fx, fy, fz = f_lab(t[..., 0]), f_lab(t[..., 1]), f_lab(t[..., 2])
    return np.stack([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)], axis=-1)


def lab_to_xyz(lab):
    lab = np.asarray(lab, dtype=float)
    fy = (lab[..., 0] + 16) / 116.0
    fx = fy + lab[..., 1] / 500.0
    fz = fy - lab[..., 2] / 200.0
    return np.stack([f_inv(fx), f_inv(fy), f_inv(fz)], axis=-1) * WP


def lab_to_lch(lab):
    lab = np.asarray(lab, dtype=float)
    L = lab[..., 0]
    C = np.hypot(lab[..., 1], lab[..., 2])
    h = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360.0
    return np.stack([L, C, h], axis=-1)


def lch_to_lab(lch):
    lch = np.asarray(lch, dtype=float)
    L, C, h = lch[..., 0], lch[..., 1], np.radians(lch[..., 2])
    return np.stack([L, C * np.cos(h), C * np.sin(h)], axis=-1)


def hue_diff(h1, h2):
    """色相角差，折算到 (-180, 180]。"""
    d = (np.asarray(h1) - np.asarray(h2) + 180.0) % 360.0 - 180.0
    return d


def delta_e00(lab1, lab2, kL=1.0, kC=1.0, kH=1.0):
    """CIEDE2000，实现依据 CIE 142:2001。"""
    lab1 = np.atleast_2d(np.asarray(lab1, dtype=float))
    lab2 = np.atleast_2d(np.asarray(lab2, dtype=float))
    L1, a1, b1 = lab1[:, 0], lab1[:, 1], lab1[:, 2]
    L2, a2, b2 = lab2[:, 0], lab2[:, 1], lab2[:, 2]
    C1 = np.hypot(a1, b1)
    C2 = np.hypot(a2, b2)
    Cb = (C1 + C2) / 2.0
    G = 0.5 * (1 - np.sqrt(Cb ** 7 / (Cb ** 7 + 25.0 ** 7)))
    a1p = (1 + G) * a1
    a2p = (1 + G) * a2
    C1p = np.hypot(a1p, b1)
    C2p = np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360.0
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360.0
    dLp = L2 - L1
    dCp = C2p - C1p
    dhp = h2p - h1p
    dhp = np.where(dhp > 180, dhp - 360, np.where(dhp < -180, dhp + 360, dhp))
    dhp = np.where(C1p * C2p == 0, 0.0, dhp)
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp / 2.0))
    Lbp = (L1 + L2) / 2.0
    Cbp = (C1p + C2p) / 2.0
    hsum = h1p + h2p
    hbp = np.where(np.abs(h1p - h2p) > 180, (hsum + 360) / 2.0, hsum / 2.0)
    hbp = np.where(C1p * C2p == 0, hsum, hbp)
    T = (1 - 0.17 * np.cos(np.radians(hbp - 30)) + 0.24 * np.cos(np.radians(2 * hbp))
         + 0.32 * np.cos(np.radians(3 * hbp + 6)) - 0.20 * np.cos(np.radians(4 * hbp - 63)))
    dth = 30 * np.exp(-(((hbp - 275) / 25.0) ** 2))
    RC = 2 * np.sqrt(Cbp ** 7 / (Cbp ** 7 + 25.0 ** 7))
    SL = 1 + 0.015 * (Lbp - 50) ** 2 / np.sqrt(20 + (Lbp - 50) ** 2)
    SC = 1 + 0.045 * Cbp
    SH = 1 + 0.015 * Cbp * T
    RT = -np.sin(np.radians(2 * dth)) * RC
    return np.sqrt((dLp / (kL * SL)) ** 2 + (dCp / (kC * SC)) ** 2
                   + (dHp / (kH * SH)) ** 2 + RT * (dCp / (kC * SC)) * (dHp / (kH * SH)))


# ---------------- 色域边界：沿等色相射线的最大彩度 ----------------
def in_gamut(lab, gname):
    xyz = lab_to_xyz(lab)
    rgb = xyz @ INV_MATS[gname].T
    return np.all((rgb >= -1e-9) & (rgb <= 1 + 1e-9), axis=-1)


def cmax(L, h, gname, c_hi=260.0, n=48, iters=40):
    """给定 (L*, h_ab)，返回该方向上的最大彩度（边界点），二分求解。"""
    L = float(L)
    h = float(h)
    if not in_gamut(lch_to_lab([L, 0.0, h]), gname):
        return np.nan
    if n is not None:                      # 先用粗网格定位上界
        cs = np.linspace(0, c_hi, n)
        ok = [in_gamut(lch_to_lab([L, c, h]), gname) for c in cs]
        idx = np.argmin(ok)
        lo = cs[max(idx - 1, 0)]
        hi = cs[idx]
    else:
        lo, hi = 0.0, c_hi
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if in_gamut(lch_to_lab([L, mid, h]), gname):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def gamut_ring(L, gname, n_hue=72):
    """等亮度切片：返回 (hue 数组, C_max 数组)。"""
    hs = np.linspace(0, 360, n_hue, endpoint=False)
    cs = np.array([cmax(L, h, gname) for h in hs])
    return hs, cs


def cusp(h, gname, nL=61):
    """色相 h 的尖点：沿 L 扫描取 C_max 最大处，再在邻域内细化。"""
    Ls = np.linspace(1, 99, nL)
    cs = np.array([cmax(L, h, gname) for L in Ls])
    i = int(np.nanargmax(cs))
    lo = Ls[max(i - 1, 0)]
    hi = Ls[min(i + 1, len(Ls) - 1)]
    for _ in range(20):
        m1 = lo + (hi - lo) / 3.0
        m2 = hi - (hi - lo) / 3.0
        if np.nan_to_num(cmax(m1, h, gname)) < np.nan_to_num(cmax(m2, h, gname)):
            lo = m1
        else:
            hi = m2
    Lc = 0.5 * (lo + hi)
    return Lc, cmax(Lc, h, gname)


def lmax(gname, h=0.0):
    """色域在给定色相上的最高亮度（L* 上端）。"""
    lo, hi = 0.0, 100.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if in_gamut(lch_to_lab([mid, 0.0, h]), gname):
            lo = mid
        else:
            hi = mid
    return lo


# ---------------- 裁剪类算法 ----------------
def clip_rgb(rgb):
    """逐通道裁剪（在线性 RGB 上做）。"""
    return np.clip(rgb, 0.0, 1.0)


def lch_to_rgb(lch, gname):
    return lab_to_xyz(lch_to_lab(lch)) @ INV_MATS[gname].T


def rgb_to_lch(rgb, gname):
    return lab_to_lch(xyz_to_lab(rgb @ MATS[gname].T))


def clip_target(lab_src, gt="sRGB"):
    """逐通道裁剪：转到目标设备的线性 RGB，三个通道各自夹到 [0,1]，再转回来。"""
    rgb = lab_to_xyz(np.atleast_2d(lab_src)) @ INV_MATS[gt].T
    return xyz_to_lab(clip_rgb(rgb) @ MATS[gt].T)[0]


def leaf_boundary(h, g, nL=41):
    """给定色相的等色相截面（hue leaf）边界：返回 (L*, C_max) 采样。"""
    Ls = np.linspace(0.5, lmax(g, h) - 1e-3, nL)
    cs = np.array([cmax(L, h, g) for L in Ls])
    ok = np.isfinite(cs)
    return Ls[ok], cs[ok]


def hp_minde(lab_src, gt="sRGB", nL=41):
    """HPMinDE：在等色相截面的边界曲线上找 ΔE00 最小的点（色相不破）。"""
    L0, C0, h0 = lab_to_lch(np.atleast_2d(lab_src))[0]
    if in_gamut(lab_src, gt):
        return np.asarray(lab_src, dtype=float).ravel(), 0.0
    Ls, cs = leaf_boundary(h0, gt, nL)
    cand = lch_to_lab(np.stack([Ls, np.minimum(0.998 * cs, C0), np.full_like(Ls, h0)], axis=-1))
    d = delta_e00(np.atleast_2d(lab_src), cand)
    i = int(np.argmin(d))
    return cand[i], float(d[i])


def minde_lattice(lab_src, gt="sRGB", n=21):
    """MinDE：把目标色域按 n 格采样成候选点，取 ΔE00 最近者（不保色相）。"""
    g = np.linspace(0, 1, n)
    R, G, B = np.meshgrid(g, g, g, indexing="ij")
    rgb = np.stack([R.ravel(), G.ravel(), B.ravel()], axis=-1)
    lab_t = xyz_to_lab(rgb @ MATS[gt].T)
    d = delta_e00(np.atleast_2d(lab_src), lab_t)
    i = int(np.argmin(d))
    return lab_t[i], float(d[i])


def hue_clip(lab_src, gt="sRGB"):
    """等色相裁剪：保持 L* 与 h，把 C 压到目标边界上。"""
    L, C, h = lab_to_lch(np.atleast_2d(lab_src))[0]
    Ltop = lmax(gt, h)
    Lq = min(max(L, 0.0), max(Ltop - 1e-6, 0.0))
    Cl = cmax(Lq, h, gt)
    if not np.isfinite(Cl):
        Cl = 0.0
    return lch_to_lab([Lq, min(C, 0.998 * Cl), h])


# ---------------- 尖点表与 cusp 裁剪 ----------------
def cusp_table(gname, step=5.0):
    hs = np.arange(0, 360 + step, step)
    tab = np.array([cusp(h % 360, gname) for h in hs])
    return hs, tab[:, 0], tab[:, 1]


def cusp_at(h, table):
    hs, Lc, Cc = table
    return np.interp(np.asarray(h, dtype=float) % 360.0, hs, Lc),            np.interp(np.asarray(h, dtype=float) % 360.0, hs, Cc)


def cusp_map(lab_src, gt="sRGB", gs="P3", tb=None, ts=None):
    """cusp 裁剪：色相的尖点对齐，明度按尖点亮度比缩放，彩度按尖点彩度比缩放后限幅。"""
    if tb is None:
        tb = cusp_table(gt)
    if ts is None:
        ts = cusp_table(gs)
    L, C, h = lab_to_lch(np.atleast_2d(lab_src))[0]
    Lct, Cct = cusp_at(h, tb)
    Lcs, Ccs = cusp_at(h, ts)
    Lq = L * (Lct / max(Lcs, 1e-6))
    Cq = C * (Cct / max(Ccs, 1e-6))
    Lim = lmax(gt, h)
    Lq = np.clip(Lq, 0.0, max(Lim - 1e-3, 0.0))
    Cmax_ = cmax(max(Lq, 0.5), h, gt)
    if not np.isfinite(Cmax_):
        Cmax_ = 0.0
    return lch_to_lab([Lq, min(Cq, 0.999 * Cmax_), h])


# ---------------- 压缩类算法：SGCK ----------------
def s_shape(x, amp=0.35):
    """两端过 (0,0)、(1,1)、端点斜率 1-amp、中段斜率 1+amp/2 的 S 形。

    f(x) = x - amp * x(1-x)(1-2x)。amp = 0 退化为恒等。
    """
    x = np.asarray(x, dtype=float)
    return x - amp * x * (1.0 - x) * (1.0 - 2.0 * x)


def knee_curve(c_in, c_lim, knee=0.9):
    """双曲膝函数：膝点以内恒等，以外单调逼近 c_lim，膝点处一阶导连续。"""
    ck = knee * c_lim
    span = c_lim - ck
    u = np.maximum(c_in - ck, 0.0)
    out = np.where(c_in <= ck, c_in, ck + span * u / (u + span))
    return np.minimum(out, c_lim)


def llin_map(lab_src, gt="sRGB", knee=0.8):
    """LLIN 思路：亮度线性归一到目标亮度，彩度用同一个膝函数分段压缩。"""
    L, C, h = lab_to_lch(np.atleast_2d(lab_src))[0]
    Ltop = lmax(gt, h)
    Lq = np.clip(L * Ltop / 100.0, 0.0, max(Ltop - 1e-3, 0.0))
    Cl = cmax(max(Lq, 0.5), h, gt)
    if not np.isfinite(Cl):
        Cl = 0.0
    return lch_to_lab([Lq, min(knee_curve(C, max(Cl, 1e-6), knee), 0.999 * Cl), h])


def sgck(lab_src, gt="sRGB", gs="P3", pj=0.5, knee=0.9, amp=0.35):
    """SGCK：亮度用线性项与 S 形项按 pj 混合，彩度用膝函数，色相保持。"""
    L, C, h = lab_to_lch(np.atleast_2d(lab_src))[0]
    Ls = lmax(gs, h)
    Lt = lmax(gt, h)
    x = np.clip(L / max(Ls, 1e-6), 0.0, 1.0)
    Lq = Lt * ((1.0 - pj) * x + pj * s_shape(x, amp))
    Lim = max(Lt - 1e-3, 0.0)
    Lq = float(np.clip(Lq, 0.0, Lim))
    Cl = cmax(max(Lq, 0.5), h, gt)
    if not np.isfinite(Cl):
        Cl = 0.0
    return lch_to_lab([Lq, min(knee_curve(C, max(Cl, 1e-6), knee), 0.999 * Cl), h])


# ---------------- α-shape（用于 GBD 对比图） ----------------
def alpha_shape(points, alpha):
    """返回 α-shape 的边界边与保留三角形，判据为 Delaunay 三角形外接圆半径 < 1/alpha。"""
    from scipy.spatial import Delaunay
    from collections import Counter
    pts = np.asarray(points, dtype=float)
    tri = Delaunay(pts)
    keep = []
    for simplex in tri.simplices:
        p = pts[simplex]
        a = np.linalg.norm(p[1] - p[2])
        b = np.linalg.norm(p[0] - p[2])
        c = np.linalg.norm(p[0] - p[1])
        v1 = p[1] - p[0]
        v2 = p[2] - p[0]
        area = abs(v1[0] * v2[1] - v1[1] * v2[0]) / 2.0
        R = a * b * c / (4.0 * area) if area > 1e-12 else np.inf
        if R < 1.0 / alpha:
            keep.append(tuple(simplex))
    cnt = Counter()
    for simplex in keep:
        for i, j in ((0, 1), (1, 2), (2, 0)):
            cnt[tuple(sorted((simplex[i], simplex[j])))] += 1
    edges = [e for e, k in cnt.items() if k == 1]
    return edges, pts
