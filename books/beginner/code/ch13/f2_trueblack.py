# -*- coding: utf-8 -*-
"""图 13-2　普通族（LCD）vs True Black 族（OLED）：峰值 vs 黑位。

要点：跨族比较不能只看峰值数字——True Black 600 峰值只有 600 nit，
却比 DisplayHDR 1400 更适合夜景，因为它黑位低到 0.0005 nit。
左图用峰值—黑位双对数散点叠加等对比度斜线；右图直接对比黑位（对数）。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/book/code/common")
import hdrfig as H
import numpy as np

# ---- 数据（规范量级/约值）----
normal = {"HDR 400": (400, 0.4), "HDR 500": (500, 0.2), "HDR 600": (600, 0.1),
          "HDR 1000": (1000, 0.05), "HDR 1400": (1400, 0.02)}
tb = {"TB 400": (400, 0.0005), "TB 500": (500, 0.0005), "TB 600": (600, 0.0005)}

fig, axes = H.plt.subplots(1, 2, figsize=(7.2, 4.0),
                           gridspec_kw={"width_ratios": [1.25, 1.0]})
fig.subplots_adjust(wspace=0.34)

# ---------- (1) 峰值 vs 黑位（双对数 + 等对比度线） ----------
ax = axes[0]
xx = np.logspace(np.log10(200), np.log10(2000), 200)
iso = [(1000, ":"), (10000, "-."), (100000, "--"), (1000000, "-")]
for ratio, ls in iso:
    ax.plot(xx, xx / ratio, ls, color="#c3ccd6", lw=1.1, zorder=1)

nk = list(normal.keys())
ax.plot([normal[k][0] for k in nk], [normal[k][1] for k in nk], "-o",
        color=H.NAVY, ms=7, lw=1.5, mfc=H.NAVY, mec="white", mew=1.0,
        label="普通族（LCD）", zorder=3)
for k, off in zip(nk, [(7, 6), (7, 6), (7, 6), (8, 6), (6, -14)]):
    ax.annotate(k, normal[k], textcoords="offset points", xytext=off,
                fontsize=8, color=H.NAVY, fontweight="bold")

tk = list(tb.keys())
ax.plot([tb[k][0] for k in tk], [tb[k][1] for k in tk], "-s", color=H.TEAL,
        ms=7, lw=1.5, mfc=H.TEAL, mec="white", mew=1.0,
        label="True Black 族（OLED）", zorder=3)

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(200, 2000); ax.set_ylim(2e-4, 2)
ax.set_xticks([200, 500, 1000, 2000])
ax.set_xticklabels(["200", "500", "1000", "2000"])
ax.set_yticks([0.0005, 0.002, 0.01, 0.05, 0.2, 1])
ax.set_yticklabels(["0.0005", "0.002", "0.01", "0.05", "0.2", "1"])
ax.minorticks_off()
ax.set_xlabel("峰值亮度 (nit，对数)")
ax.set_ylabel("黑位 (nit，对数，越低越好)")
ax.set_title("峰值—黑位分布（斜线 = 等对比度）", pad=8)
ax.legend(loc="lower right", fontsize=8.2)
ax.annotate("同样 400–600 nit 峰值，\nTrue Black 黑位低 ~1000 倍",
            xy=(560, 0.0006), xytext=(300, 0.0045), fontsize=8, color=H.TEAL,
            fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=H.TEAL, lw=1.1,
                            connectionstyle="arc3,rad=0.28"),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=H.TEAL, lw=0.7, alpha=0.95))

# 等对比度线标注（沿左边缘，避开数据点），角度按屏幕坐标计算
fig.canvas.draw()


def screen_angle(x1, y1, x2, y2):
    p1 = ax.transData.transform((x1, y1)); p2 = ax.transData.transform((x2, y2))
    return np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))


for ratio, txt in [(1000, "1000:1"), (10000, "1万:1"),
                   (100000, "10万:1"), (1000000, "100万:1")]:
    xa = 235.0
    ya = xa / ratio
    ya = max(ya, 2.6e-4)
    ax.text(xa, ya * 1.12, txt, fontsize=7.0, color=H.GRAY, zorder=2,
            rotation=screen_angle(xa, ya, xa * 1.30, ya * 1.30),
            rotation_mode="anchor", ha="left", va="bottom")

# ---------- (2) 黑位对比（对数条） ----------
ax = axes[1]
names = ["DisplayHDR 400", "DisplayHDR 600", "DisplayHDR 1400", "True Black 600"]
blk = [0.4, 0.1, 0.02, 0.0005]
col = [H.GRAY, H.BLUE, H.RED, H.TEAL]
ratio_txt = ["对比度 ≈ 1000:1", "对比度 ≈ 6000:1", "对比度 ≈ 70000:1",
             "对比度 ≈ 120万:1"]
ypos = np.arange(len(names))[::-1]
ax.barh(ypos, blk, color=col, edgecolor="white", linewidth=0.8, height=0.55)
for y, v in zip(ypos, blk):
    ax.text(v * 1.35, y, f"{v:g} nit", va="center", fontsize=8.6,
            fontweight="bold", color="#1b2a3a")
ax.text(0.0045, -0.40, "← 黑位极低：OLED 逐像素自发光、可完全熄灭\n"
        "　 同一张夜景，这里才看得见“真正的黑”",
        va="center", ha="left", fontsize=7.6, color=H.TEAL, fontweight="bold")
ax.set_xscale("log")
ax.set_xlim(3e-4, 15)
ax.set_xticks([0.001, 0.01, 0.1, 1, 10])
ax.set_xticklabels(["0.001", "0.01", "0.1", "1", "10"])
ax.minorticks_off()
ax.set_yticks(ypos)
ax.set_yticklabels([f"{n}\n({r})" for n, r in zip(names, ratio_txt)], fontsize=8)
ax.set_xlabel("黑位 (nit，对数，越靠左越黑)")
ax.set_title("黑位决定“夜景能不能看”", pad=8)
ax.grid(axis="y", visible=False)
ax.set_ylim(-0.85, 3.6)

fig.suptitle("跨族比较要比“对比度”，不是比“峰值数字”", fontsize=13,
             fontweight="bold", y=1.04)
fig.text(0.5, -0.12, "注：数值为规范量级/约值，仅示意族间差异；"
                     "True Black 峰值受 ABL（见第 12 章）限制，故数字不高。",
         ha="center", fontsize=8, color=H.GRAY)

H.save(fig, 13, "f2_trueblack")
