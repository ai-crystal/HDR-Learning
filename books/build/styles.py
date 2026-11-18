# -*- coding: utf-8 -*-
# 从单册构建脚本抽出的排版样式（系列共用）

CSS_NORMAL = r"""
@page { size: A4; margin: 20mm 20mm 22mm 20mm; }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html,body{ margin:0; padding:0; }
body{ font-family:"Source Han Serif SC","Noto Serif CJK SC","SimSun","宋体",serif;
      font-size:10.5pt; line-height:1.78; color:#1b1b1b; }
.page{ }
h1,h2,h3,h4{ font-family:"Microsoft YaHei","微软雅黑","SimHei",sans-serif; color:#12233b; line-height:1.35; }
h1{ font-size:19pt; margin:0 0 14pt; padding-bottom:7pt; border-bottom:2.4pt solid #1f4e79; }
h2{ font-size:14pt; margin:18pt 0 8pt; }
h3{ font-size:11.5pt; margin:14pt 0 6pt; color:#1f4e79; }
h4{ font-size:10.5pt; margin:12pt 0 5pt; }
p{ margin:0 0 8pt; text-align:justify; }
ul,ol{ margin:0 0 8pt; padding-left:2.6em; }
li{ margin:2pt 0; }
blockquote{ margin:10pt 0; padding:6pt 12pt; border-left:3pt solid #1f4e79; background:#f3f6fa; color:#3f3f3f; }
table{ width:100%; border-collapse:collapse; margin:10pt 0; font-size:9pt; }
th,td{ border:0.6pt solid #c3ccd6; padding:4pt 6pt; vertical-align:top; text-align:left; }
th{ background:#eaf0f6; font-family:"Microsoft YaHei",sans-serif; }
pre{ background:#f6f8fa; border:0.6pt solid #d8dee6; border-radius:4pt; padding:8pt 10pt;
     font-size:8.4pt; line-height:1.5; white-space:pre-wrap; word-break:break-word; overflow:hidden; }
code{ font-family:"Cascadia Mono","Consolas","Courier New",monospace; font-size:9pt; background:#eef1f4; padding:0 2pt; border-radius:2pt; }
pre code{ background:none; padding:0; font-size:8.4pt; }
img{ max-width:100%; height:auto; display:block; margin:10pt auto; }
figure{ margin:12pt 0; text-align:center; }
figcaption{ font-size:8.8pt; color:#666; margin-top:4pt; }
hr{ border:none; border-top:0.6pt solid #ccd3da; margin:14pt 0; }
a{ color:#1f4e79; text-decoration:none; }
pre.mermaid{ background:transparent; border:none; text-align:center; padding:6pt 0; }
table,pre,blockquote,figure,li{ break-inside:avoid; }
h1,h2,h3,h4{ break-after:avoid; }
.part-title{ break-before:auto; }
"""

CSS_COVER = r"""
@page { size: A4; margin: 0; }
* { box-sizing:border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html,body{ margin:0; padding:0; }
body{ font-family:"Source Han Serif SC","SimSun","宋体",serif; }
.page{ position:relative; width:210mm; height:297mm; overflow:hidden; background:#05070d; color:#fff; }
.cv-bg{ position:absolute; inset:0;
        background-image:url("images/logo/cover_bg.jpg");
        background-size:cover; background-position:center center; }
.cv-scrim{ position:absolute; inset:0;
  background:
    linear-gradient(180deg, rgba(5,7,13,0.74) 0%, rgba(5,7,13,0.22) 16%, rgba(5,7,13,0.04) 32%, rgba(5,7,13,0.40) 52%, rgba(5,7,13,0.90) 66%, #05070d 82%),
    radial-gradient(130% 85% at 50% 52%, rgba(5,7,13,0) 38%, rgba(5,7,13,0.55) 100%); }
.cv-frame{ position:absolute; inset:13mm; border:0.7pt solid rgba(255,255,255,0.20); }
.cv-kicker{ position:absolute; left:26mm; top:24mm;
            font-family:"Microsoft YaHei",sans-serif; font-size:8.5pt; letter-spacing:5pt;
            color:#d8b26a; }
.cv-content{ position:absolute; left:26mm; right:26mm; bottom:28mm; }
.cv-en{ font-family:"Georgia","Times New Roman",serif; font-size:102pt; line-height:0.92;
        font-weight:700; letter-spacing:6pt; color:#ffffff;
        text-shadow:0 2mm 12mm rgba(0,0,0,0.60); }
.cv-cn{ font-family:"Source Han Serif SC","SimSun",serif; font-size:43pt; font-weight:700;
        letter-spacing:16pt; margin-top:4mm; color:#ffffff;
        text-shadow:0 1mm 8mm rgba(0,0,0,0.55); }
.cv-rule{ width:46mm; height:1.6pt; background:#d8b26a; margin:9mm 0 7mm; }
.cv-sub{ font-family:"Microsoft YaHei",sans-serif; font-size:14.5pt; letter-spacing:3pt; color:#e9eff7; }
.cv-meta{ margin-top:13mm; display:flex; justify-content:space-between; align-items:flex-end; }
.cv-author{ font-family:"Microsoft YaHei",sans-serif; font-size:14pt; letter-spacing:4pt; color:#fff; }
.cv-date{ font-family:"Microsoft YaHei",sans-serif; font-size:9.5pt; letter-spacing:1.5pt; color:#9fb0c2; }
"""

CSS_TITLE = r"""
@page { size: A4; margin: 0; }
* { box-sizing:border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html,body{ margin:0; padding:0; }
body{ font-family:"Source Han Serif SC","SimSun","宋体",serif; color:#12233b; }
.page{ height:297mm; padding:60mm 30mm; display:flex; flex-direction:column; justify-content:center; text-align:center; }
.tp-title{ font-size:30pt; font-weight:700; letter-spacing:4pt; }
.tp-sub{ font-family:"Microsoft YaHei",sans-serif; font-size:14pt; color:#3a4a5e; margin-top:10mm; letter-spacing:2pt; }
.tp-rule{ width:40mm; height:2pt; background:#c8a24a; margin:14mm auto; }
.tp-author{ font-family:"Microsoft YaHei",sans-serif; font-size:13pt; letter-spacing:4pt; }
.tp-date{ font-family:"Microsoft YaHei",sans-serif; font-size:10.5pt; color:#6a7686; margin-top:6mm; }
"""

CSS_BACK = r"""
@page { size: A4; margin: 0; }
* { box-sizing:border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html,body{ margin:0; padding:0; }
body{ font-family:"Source Han Serif SC","SimSun","宋体",serif; color:#1b1b1b; }
.page{ height:297mm; padding:34mm 24mm; display:flex; flex-direction:column; justify-content:center; }
.bc-box{ border:0.9pt solid #b9c4d0; padding:14mm 12mm; }
.bc-box h2{ font-family:"Microsoft YaHei",sans-serif; color:#12233b; font-size:16pt; text-align:center; margin:0 0 4mm; }
.bc-sub{ font-family:"Microsoft YaHei",sans-serif; color:#3a4a5e; font-size:11pt; text-align:center; margin-bottom:8mm; letter-spacing:2pt; }
.bc-box p{ font-size:10pt; line-height:1.8; text-align:justify; }
.bc-box blockquote{ margin:8mm 0; padding:4mm 6mm; border-left:3pt solid #c8a24a; color:#4a5568; background:#faf7f0; text-align:center; }
.bc-foot{ text-align:center; margin-top:10mm; color:#6a7686; font-size:10pt; letter-spacing:2pt; }
"""

TEMPLATE = r"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<base href="file:///E:/Study/HDR技术/book/">
<title>{title}</title>
<style>{css}</style>
</head>
<body class="kind-{kind}">
<main class="page {pagecls}">
{body}
</main>
<script src="file:///E:/Study/HDR技术/book/build/mermaid.min.js"></script>
<script>try{{mermaid.initialize({{startOnLoad:true,theme:'neutral',securityLevel:'loose',flowchart:{{htmlLabels:true}}}});}}catch(e){{}}</script>
<script>
window.MathJax = {{ tex: {{ inlineMath: [['$','$']], displayMath: [['$$','$$']] }}, svg: {{ fontCache: 'global' }} }};
</script>
<script src="file:///E:/Study/HDR技术/book/build/tex-svg.js"></script>
</body></html>
"""
