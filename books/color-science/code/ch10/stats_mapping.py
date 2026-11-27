# -*- coding: utf-8 -*-
"""第 10 章统计口径：P3 -> sRGB 七种映射在超界色样上的色差与色相偏移。"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cslib as C

TB = C.cusp_table("sRGB", 5.0)
TS = C.cusp_table("P3", 5.0)
print("cusp tables ready")

def sample(n=17):
    g = np.linspace(0, 1, n)
    R, G, B = np.meshgrid(g, g, g, indexing="ij")
    rgb = np.stack([R.ravel(), G.ravel(), B.ravel()], axis=-1)
    lab = C.xyz_to_lab(rgb @ C.MATS["P3"].T)
    m = (lab[:, 0] > 10) & (~C.in_gamut(lab, "sRGB"))
    return rgb[m], lab[m]

rgb_s, lab_s = sample()
print("samples", len(lab_s))

methods = {}
t = time.time(); methods["逐通道裁剪"] = np.array([C.clip_target(l, "sRGB") for l in lab_s]); print("clip", time.time()-t)
t = time.time(); methods["等色相裁剪"] = np.array([C.hue_clip(l, "sRGB") for l in lab_s]); print("hc", time.time()-t)
t = time.time(); methods["HPMinDE"] = np.array([C.hp_minde(l, "sRGB")[0] for l in lab_s]); print("hp", time.time()-t)
t = time.time(); methods["MinDE"] = np.array([C.minde_lattice(l, "sRGB")[0] for l in lab_s]); print("minde", time.time()-t)
t = time.time(); methods["LLIN"] = np.array([C.llin_map(l, "sRGB") for l in lab_s]); print("llin", time.time()-t)
t = time.time(); methods["cusp裁剪"] = np.array([C.cusp_map(l, "sRGB", "P3", TB, TS) for l in lab_s]); print("cusp", time.time()-t)
t = time.time(); methods["SGCK"] = np.array([C.sgck(l, "sRGB", "P3") for l in lab_s]); print("sgck", time.time()-t)

lch_s = C.lab_to_lch(lab_s)
for k, v in methods.items():
    d = C.delta_e00(lab_s, v)
    lch_o = C.lab_to_lch(v)
    h_d = np.abs(C.hue_diff(lch_o[:, 2], lch_s[:, 2]))
    dC = np.abs(lch_o[:, 1] - lch_s[:, 1])
    dL = np.abs(lch_o[:, 0] - lch_s[:, 0])
    oog = np.mean(~C.in_gamut(v, "sRGB"))
    print(f"{k:8s} dE mean {d.mean():5.2f} p95 {np.percentile(d,95):5.2f} max {d.max():6.2f} "
          f"|dh| mean {h_d.mean():4.2f} >2 {100*np.mean(h_d>2):5.1f}% max {h_d.max():5.2f} "
          f"| dC {dC.mean():5.1f} dL {dL.mean():5.1f} oog {100*oog:.2f}%")

np.savez("_stats.npz", lab_s=lab_s, **{k: v for k, v in methods.items()})
