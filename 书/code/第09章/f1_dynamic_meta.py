# -*- coding: utf-8 -*-
"""图 09-1　动态元数据：逐帧亮度曲线 + 每帧可调的映射。

上半：一条影片的"逐帧峰值亮度"曲线（按场景着色），叠加
      - HDR10 静态元数据：全片只有一条固定的目标线（折中）
      - DV / HDR10+ 动态元数据：目标随每一帧变化（贴合内容）
下半：三个代表场景各自的映射曲线（烛光 / 室内 / 雪原），
      与 HDR10 那一条"全片通用"曲线对比，展示"每帧可调"的含义。
"""
import sys; sys.path.insert(0, "E:/Study/HDR技术/书/code/common")
import numpy as np
import hdrfig as H

plt = H.plt

# ---------------------------------------------------------------- 场景数据
# 每段场景：(名称, 帧数, 峰值亮度 nit, 代表色)
scenes = [
    ("烛光晚餐", 90, 300, H.ORANGE),
    ("夜间街道", 70, 180, H.PURPLE),
    ("室内白天", 120, 800, H.TEAL),
    ("正午雪原", 130, 4000, H.NAVY),
    ("烟花夜景", 60, 6000, H.RED),
    ("黄昏海面", 90, 1200, H.GOLD),
]

rng = np.random.default_rng(9)
frame_peak = []          # 逐帧峰值亮度
frame_color = []         # 每帧所属场景颜色
scene_spans = []         # (start, end, name, peak, color)
t = 0
for name, n, peak, c in scenes:
    # 场景内部围绕峰值起伏（曲线更真实）
    base = peak * (0.75 + 0.25 * np.sin(np.linspace(0, np.pi, n)))
    fluct = 1.0 + 0.06 * rng.standard_normal(n)
    seg = np.clip(base * fluct, 5, None)
    frame_peak.append(seg)
    frame_color.append(np.tile(c, (n, 1)))
    scene_spans.append((t, t + n, name, peak, c))
    t += n

peak = np.concatenate(frame_peak)
x = np.arange(len(peak))
peak_smooth = np.convolve(peak, np.ones(9) / 9, mode="same")
peak_smooth[:4] = peak[:4]
peak_smooth[-4:] = peak[-4:]

# HDR10 静态元数据：整片只给一套统计（这里取全片"折中"目标）
STATIC_CLL = 1000.0

fig = plt.figure(figsize=(7.2, 6.4))
gs = fig.add_gridspec(2, 1, height_ratios=[1.15, 1.0], hspace=0.42)

# ================================================================ 上：逐帧曲线
ax = fig.add_subplot(gs[0])
for (s, e, name, p, c) in scene_spans:
    ax.axvspan(s, e, color=c, alpha=0.09, lw=0)
ax.plot(x, peak, color=H.GRAY, lw=0.6, alpha=0.45, label="逐帧峰值亮度（原始波动）")
ax.plot(x, peak_smooth, color=H.DARK, lw=2.2, label="逐帧峰值亮度（平滑）")

# HDR10：一条全片固定的目标线
ax.axhline(STATIC_CLL, color=H.RED, lw=2.0, ls="--",
           label="HDR10 静态元数据：全片一套（≈1000 nit，折中）")
# DV / HDR10+：目标随帧变化
ax.plot(x, peak_smooth, color=H.BLUE, lw=2.4, alpha=0.85,
        label="DV / HDR10+ 动态元数据：逐帧/逐场景目标")

ax.set_yscale("log")
ax.set_ylim(60, 12000)
ax.set_xlim(0, len(peak))
ax.set_ylabel("峰值亮度（nit，对数轴）")
ax.set_xlabel("影片播放进度（帧序号）")
ax.set_title("动态元数据：元数据随时变，映射也随之变", fontweight="bold")
ax.legend(loc="upper left", ncol=1, fontsize=7.6)

# 场景标注（名称放在底部空白带，避免与图例/竖线相加）
for (s, e, name, p, c) in scene_spans:
    ax.text((s + e) / 2, 74, name, ha="center", va="bottom",
            fontsize=8, color=c, fontweight="bold", rotation=0)
    ax.annotate(f"{int(p)}", xy=((s + e) / 2, p), xytext=((s + e) / 2, p * 1.35),
                ha="center", fontsize=7.5, color=c,
                arrowprops=dict(arrowstyle="-", color=c, lw=0.8))

ax.annotate("静态：暗场被抬高、\n亮场被压低", xy=(150, STATIC_CLL),
            xytext=(335, 1350), fontsize=8, color=H.RED, ha="left", va="bottom",
            arrowprops=dict(arrowstyle="->", color=H.RED, lw=1.1),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=H.RED, lw=0.7, alpha=0.95))

# 右侧小注
for (s, e, name, p, c) in scene_spans:
    if p >= 4000:
        ax.axhline(p, color=c, lw=0.7, ls=":", alpha=0.6)

# ================================================================ 下：映射曲线
ax2 = fig.add_subplot(gs[1])


def hdr10_static(Lin, target=1000.0):
    """HDR10 全片通用的硬压曲线：超过 target 的部分统一滚降。"""
    Lin = np.asarray(Lin, float)
    out = np.where(Lin <= target, Lin, target * (1 + 0.25 * (1 - np.exp(-(Lin - target) / 2500.0))))
    return out


def scene_map(Lin, peak_scene):
    """按场景峰值定制的滚降：暗场景保护暗部，亮场景压缩大范围高光。"""
    Lin = np.asarray(Lin, float)
    knee = max(60.0, peak_scene * 0.55)
    head = Lin <= knee
    out = np.empty_like(Lin)
    out[head] = Lin[head]
    over = Lin[~head]
    out[~head] = knee + (peak_scene - knee) * (1 - np.exp(-(over - knee) /
                                                           (peak_scene * 0.66)))
    return out


L = np.logspace(np.log10(0.5), np.log10(10000), 600)
ax2.plot(L, hdr10_static(L), color=H.RED, ls="--", lw=2.0,
         label="HDR10 一条通用曲线（全片不变）")
for (name, _n, p, c) in [scenes[0], scenes[2], scenes[3]]:
    ax2.plot(L, scene_map(L, p), color=c, lw=2.1,
             label=f"{name}：按该场景定制（峰值 {int(p)} nit）")

ax2.plot(L, L, color=H.LGRAY, lw=1.0, ls=":", label="理想 1:1（参考）")
ax2.set_xscale("log"); ax2.set_yscale("log")
ax2.set_xlim(0.5, 10000); ax2.set_ylim(0.5, 10000)
ax2.set_xlabel("输入亮度（nit，对数轴）")
ax2.set_ylabel("映射后显示亮度（nit）")
ax2.set_title("每个场景一张\"曝光表\"：暗场护暗部、亮场压高光", fontweight="bold")
ax2.legend(loc="upper left", fontsize=8)
ax2.grid(which="both", color="#e6ebf0", lw=0.6)

# 标注：放在 1:1 参考线下方空白区，避开曲线与图例
ax2.text(28, 0.75, "同一份母版，每个场景各调各的\n（越亮的场景，高光压得越狠）",
         fontsize=8, color=H.NAVY, ha="left", va="bottom",
         bbox=dict(boxstyle="round,pad=0.30", fc="white", ec=H.NAVY, lw=0.7, alpha=0.95))

fig.text(0.5, -0.02,
         "动态元数据 = 一串\"每帧的调色备注\"：显示端读到一组就立刻调整一次映射",
         ha="center", fontsize=8.5, color=H.GRAY)

H.save(fig, 9, "f1_dynamic_meta")
