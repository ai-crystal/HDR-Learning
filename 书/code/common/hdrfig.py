# -*- coding: utf-8 -*-
"""HDR 图示通用工具：统一的字体、配色、尺寸、保存，以及 HDR 相关的精确数学函数。
所有章节的绘图脚本都应 import 本模块，以保证全书图示风格一致。

用法：
    import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
    import hdrfig as H
    fig, ax = H.plt.subplots(figsize=(7.2, 4))
    ...
    H.save(fig, 7, "f1_pq_curve")      # -> 图片/07/f1_pq_curve.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ---------- 字体（中文） ----------
_FONT = "C:/Windows/Fonts/simhei.ttf"
if os.path.exists(_FONT):
    fm.fontManager.addfont(_FONT)
    _CJK = fm.FontProperties(fname=_FONT).get_name()
else:
    _CJK = "SimHei"
plt.rcParams.update({
    "font.sans-serif": [_CJK, "SimHei", "Microsoft YaHei", "sans-serif"],
    "font.family": "sans-serif",
    "axes.unicode_minus": False,
    "figure.dpi": 150, "savefig.dpi": 150,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.edgecolor": "#4a5666", "axes.linewidth": 0.9,
    "axes.grid": True, "grid.color": "#dde3ea", "grid.linewidth": 0.7,
    "axes.titlesize": 13, "axes.titleweight": "bold",
    "axes.labelsize": 10.5,
    "xtick.labelsize": 9, "ytick.labelsize": 9,
    "legend.fontsize": 9, "legend.frameon": True,
    "legend.framealpha": 0.92, "legend.edgecolor": "#c9d3de",
    "legend.fancybox": True,
    "lines.linewidth": 2.0,
})

# ---------- 统一配色 ----------
NAVY = "#1f4e79"
BLUE = "#2980b9"
ORANGE = "#e67e22"
TEAL = "#16a085"
GREEN = "#27ae60"
RED = "#c0392b"
PURPLE = "#8e44ad"
GOLD = "#c8a24a"
GRAY = "#7f8c8d"
LGRAY = "#d5dbe2"
DARK = "#12233b"
PALETTE = [NAVY, ORANGE, TEAL, RED, PURPLE, GREEN, BLUE, GOLD, GRAY]

OUTROOT = "E:/Study/HDR技术/书/图片"


def outdir(ch):
    d = f"{OUTROOT}/{ch:02d}"
    os.makedirs(d, exist_ok=True)
    return d


def save(fig, ch, name, tight=True):
    """保存到 图片/<NN>/<name>.png，返回路径。"""
    p = f"{outdir(ch)}/{name}.png"
    fig.savefig(p, bbox_inches="tight" if tight else None, facecolor="white")
    plt.close(fig)
    print("saved", p)
    return p


# ---------- HDR 数学（可直接用于画曲线） ----------
def pq_eotf(code01):
    """SMPTE ST 2084 PQ EOTF：输入归一化码值 0..1，返回绝对亮度 nit（0..10000）。"""
    m1, m2 = 0.1593017578125, 78.84375
    c1, c2, c3 = 0.8359375, 18.8515625, 18.6875
    code01 = np.clip(np.asarray(code01, dtype=float), 0, 1)
    p = code01 ** (1.0 / m2)
    num = np.maximum(p - c1, 0.0)
    den = c2 - c3 * p
    return 10000.0 * (num / den) ** (1.0 / m1)


def pq_oetf(nit):
    """PQ 逆函数：输入绝对亮度 nit，返回归一化码值 0..1。"""
    m1, m2 = 0.1593017578125, 78.84375
    c1, c2, c3 = 0.8359375, 18.8515625, 18.6875
    y = np.clip(np.asarray(nit, dtype=float), 0, 10000) / 10000.0
    ym = y ** m1
    return ((c1 + c2 * ym) / (1.0 + c3 * ym)) ** m2


def hlg_oetf(e):
    """BT.2100 HLG OETF：输入场景线性 0..1，返回 0..1。"""
    a, b, c = 0.17883277, 0.28466892, 0.55991073
    e = np.asarray(e, dtype=float)
    return np.where(e <= 1.0 / 12.0, np.sqrt(3.0 * e),
                    a * np.log(12.0 * e - b) + c)


def hlg_eotf(v):
    """BT.2100 HLG EOTF（逆）。"""
    a, b, c = 0.17883277, 0.28466892, 0.55991073
    v = np.asarray(v, dtype=float)
    return np.where(v <= 0.5, v ** 2 / 3.0, (np.exp((v - c) / a) + b) / 12.0)


def srgb_eotf(v):
    """sRGB 电光转换（码值 0..1 -> 线性 0..1）。"""
    v = np.asarray(v, dtype=float)
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def srgb_oetf(l):
    """sRGB 线性 0..1 -> 码值 0..1。"""
    l = np.asarray(l, dtype=float)
    return np.where(l <= 0.0031308, l * 12.92, 1.055 * l ** (1 / 2.4) - 0.055)


def gamma_oetf(l, g=2.2):
    return np.asarray(l, dtype=float) ** (1.0 / g)


def gamma_eotf(v, g=2.2):
    return np.asarray(v, dtype=float) ** g


def banding_gray(bit, width=512, height=120):
    """生成位深量化灰度带，用于演示色带。返回 uint8 灰度图。"""
    levels = 2 ** bit
    x = np.linspace(0, 1, width)
    q = np.round(x * (levels - 1)) / (levels - 1)
    img = np.tile(q * 255.0, (height, 1))
    return img.astype(np.uint8)
