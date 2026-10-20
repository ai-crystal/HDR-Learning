#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把 书/ 下的 Markdown 源文件组装成可打印的 HTML 分节文件 + manifest.json。
渲染与合成 PDF 由 build_pdf.mjs 完成。"""
import os, re, json, markdown

BASE = "E:/Study/HDR-Learning/书"
BUILD = BASE + "/build"
HTMLDIR = BUILD + "/html"
os.makedirs(HTMLDIR, exist_ok=True)

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
.page{ position:relative; width:210mm; height:297mm; overflow:hidden;
       background:linear-gradient(150deg,#08111d 0%,#0f2a44 48%,#08111d 100%); color:#fff; }
.cv-glow{ position:absolute; width:430mm; height:430mm; left:-130mm; top:-170mm;
          background:radial-gradient(circle at center, rgba(230,126,34,0.30) 0%, rgba(230,126,34,0) 55%); }
.cv-glow2{ position:absolute; width:360mm; height:360mm; right:-150mm; bottom:-190mm;
          background:radial-gradient(circle at center, rgba(52,152,219,0.22) 0%, rgba(52,152,219,0) 58%); }
.cv-frame{ position:absolute; inset:15mm; border:0.8pt solid rgba(255,255,255,0.22);
           display:flex; flex-direction:column; justify-content:space-between; padding:22mm 18mm 18mm; }
.cv-top{ text-align:left; }
.cv-kicker{ font-family:"Microsoft YaHei",sans-serif; letter-spacing:5pt; font-size:9.5pt; color:#e67e22; }
.cv-mid{ text-align:left; margin-top:-4mm; }
.cv-en{ font-family:"Georgia","Times New Roman",serif; font-size:98pt; line-height:1;
        font-weight:700; letter-spacing:5pt; color:#ffffff; }
.cv-cn{ font-family:"Source Han Serif SC","SimSun",serif; font-size:41pt; font-weight:700;
        letter-spacing:14pt; margin-top:5mm; color:#ffffff; }
.cv-bar-wrap{ margin:13mm 0 8mm; width:100%; }
.cv-bar{ height:3.2mm; border-radius:2mm;
         background:linear-gradient(90deg,#000 0%,#2b2b2b 25%,#8a8a8a 55%,#dcdcdc 80%,#ffffff 100%);
         border:0.5pt solid rgba(255,255,255,0.35); }
.cv-bar-labels{ display:flex; justify-content:space-between; margin-top:2.5mm;
                font-family:"Microsoft YaHei",sans-serif; font-size:7.5pt; color:#9fb0c2; letter-spacing:0.5pt; }
.cv-sub{ font-family:"Microsoft YaHei",sans-serif; font-size:15pt; color:#cdd8e4; letter-spacing:3pt; }
.cv-bottom{ display:flex; flex-direction:column; align-items:flex-start; }
.cv-author{ font-family:"Microsoft YaHei",sans-serif; font-size:14pt; letter-spacing:4pt; }
.cv-date{ font-family:"Microsoft YaHei",sans-serif; font-size:9.5pt; color:#8fa1b4; margin-top:2.5mm; }
.cv-logo{ width:66mm; margin-top:11mm; }
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
<base href="file:///E:/Study/HDR-Learning/%E4%B9%A6/">
<title>{title}</title>
<style>{css}</style>
</head>
<body class="kind-{kind}">
<main class="page {pagecls}">
{body}
</main>
<script src="file:///E:/Study/HDR-Learning/%E4%B9%A6/build/mermaid.min.js"></script>
<script>try{{mermaid.initialize({{startOnLoad:true,theme:'neutral',securityLevel:'loose',flowchart:{{htmlLabels:true}}}});}}catch(e){{}}</script>
<script>
window.MathJax = {{ tex: {{ inlineMath: [['$','$']], displayMath: [['$$','$$']] }}, svg: {{ fontCache: 'global' }} }};
</script>
<script src="file:///E:/Study/HDR-Learning/%E4%B9%A6/build/tex-svg.js"></script>
</body></html>
"""

_MATH_TOKENS = []

def _protect_math(text):
    """把 $...$ / $$...$$ 换成占位符，避免 markdown 处理其中的 \\ _ ^ * 等字符。"""
    global _MATH_TOKENS
    _MATH_TOKENS = []
    def rep(m):
        _MATH_TOKENS.append(m.group(0))
        return f"@@MATHX{len(_MATH_TOKENS)-1}@@"
    parts = re.split(r'(```.*?```)', text, flags=re.S)
    out = []
    for seg in parts:
        if seg.startswith('```'):
            out.append(seg); continue
        seg = re.sub(r'\$\$.+?\$\$', rep, seg, flags=re.S)
        seg = re.sub(r'(?<!\$)\$(?!\$).+?(?<!\$)\$(?!\$)', rep, seg, flags=re.S)
        out.append(seg)
    return ''.join(out)

def _restore_math(html):
    for i, tok in enumerate(_MATH_TOKENS):
        html = html.replace(f"@@MATHX{i}@@", tok)
    return html

def md_to_html(text):
    md = markdown.Markdown(extensions=['extra','sane_lists','toc','attr_list','md_in_html'])
    html = md.convert(_protect_math(text))
    html = _restore_math(html)
    # mermaid code fences -> <pre class="mermaid">
    html = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>',
                  lambda m: '<pre class="mermaid">'+m.group(1)+'</pre>', html, flags=re.S)
    # images -> figure/figcaption
    def fig(m):
        tag = m.group(1)
        alt = re.search(r'alt="([^"]*)"', tag)
        cap = alt.group(1).strip() if alt else ""
        if cap:
            return '<figure>'+tag+'<figcaption>'+cap+'</figcaption></figure>'
        return '<figure>'+tag+'</figure>'
    html = re.sub(r'<p>\s*(<img[^>]*>)\s*</p>', fig, html)
    return html

def read(p):
    with open(os.path.join(BASE, p), 'r', encoding='utf-8') as f:
        return f.read()

def first_heading(text):
    for line in text.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return None

def render_cover(text):
    title=sub=author=date=''
    for line in text.splitlines():
        s=line.strip()
        if not s: continue
        if s.startswith('### '): author=s[4:].strip()
        elif s.startswith('## '): sub=s[3:].strip()
        elif s.startswith('# '): title=s[2:].strip()
        else: date=s
    en='HDR'; cn=title
    m=re.match(r'^\s*HDR\s*(.*)$', title, re.I)
    if m:
        cn=m.group(1).strip() or '超详解'
    return ('<div class="cv-glow"></div><div class="cv-glow2"></div>'
            '<div class="cv-frame">'
            '<div class="cv-top"><span class="cv-kicker">JUPITER　SPATIAL　REALITY</span></div>'
            '<div class="cv-mid">'
            f'<div class="cv-en">{en}</div>'
            f'<div class="cv-cn">{cn}</div>'
            '<div class="cv-bar-wrap">'
            '<div class="cv-bar"></div>'
            '<div class="cv-bar-labels"><span>0.001 nit</span><span>1 nit</span>'
            '<span>100 nit</span><span>10000 nit</span></div>'
            '</div>'
            f'<div class="cv-sub">{sub}</div>'
            '</div>'
            '<div class="cv-bottom">'
            f'<div class="cv-author">{author}</div>'
            f'<div class="cv-date">{date}</div>'
            '<img class="cv-logo" src="图片/logo/JupiterSR_橙标+白字.png" alt="Jupiter Spatial Reality">'
            '</div>'
            '</div>')

def render_titlepage(text):
    lines=[s.strip() for s in text.splitlines() if s.strip()]
    t=lines[0] if len(lines)>0 else ''
    sub=lines[1] if len(lines)>1 else ''
    author=lines[2] if len(lines)>2 else ''
    date=lines[3] if len(lines)>3 else ''
    return ('<div class="tp-title">'+t+'</div>'
            '<div class="tp-sub">'+sub+'</div>'
            '<div class="tp-rule"></div>'
            '<div class="tp-author">'+author+'</div>'
            '<div class="tp-date">'+date+'</div>')

def write_section(sec):
    src = sec.get('src')
    kind = sec['kind']
    text = read(src) if src else ''
    if kind == 'cover':
        body = render_cover(text)
    elif kind == 'title':
        body = render_titlepage(text)
    elif kind == 'back':
        body = '<div class="bc-box">' + md_to_html(text) + '</div>'
    elif src:
        body = md_to_html(text)
    else:
        body = sec.get('body', '')
    css = CSS_NORMAL
    pagecls = ''
    if kind == 'cover': css = CSS_COVER; pagecls = 'cover-wrap'
    elif kind == 'title': css = CSS_TITLE
    elif kind == 'back': css = CSS_BACK
    html = TEMPLATE.format(title=sec['title'], css=css, kind=kind, pagecls=pagecls, body=body)
    out = os.path.join(HTMLDIR, sec['id'] + '.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    return out

# ---------- section list ----------
S = []
def add(id, kind, src=None, toc=None, body=None, title=None):
    S.append(dict(id=id, kind=kind, src=src, toc=toc, body=body, title=title))

add('cover','cover','00-封面.md')
add('title','title','01-扉页.md')
add('copyright','plain','02-版权页.md')
add('preface','plain','03-前言.md', toc='entry')
add('toc','toc', None)

parts = [
    ('part1','篇一-篇首.md', [
        ('ch01','正文/第01章-从SDR说起.md'),
        ('ch02','正文/第02章-亮度对比度与动态范围.md'),
        ('ch03','正文/第03章-人眼如何看光.md')]),
    ('part2','篇二-篇首.md', [
        ('ch04','正文/第04章-颜色的坐标系.md'),
        ('ch05','正文/第05章-色域漫游.md'),
        ('ch06','正文/第06章-传递函数与Gamma.md'),
        ('ch07','正文/第07章-PQ与HLG.md')]),
    ('part3','篇三-篇首.md', [
        ('ch08','正文/第08章-HDR10基石.md'),
        ('ch09','正文/第09章-DolbyVision与HDR10加.md'),
        ('ch10','正文/第10章-位深编码与色度采样.md')]),
    ('part4','篇四-篇首.md', [
        ('ch11','正文/第11章-面板与背光.md'),
        ('ch12','正文/第12章-自发光时代.md'),
        ('ch13','正文/第13章-认证与DisplayHDR.md')]),
    ('part5','篇五-篇首.md', [
        ('ch14','正文/第14章-接口与带宽.md'),
        ('ch15','正文/第15章-链路握手.md'),
        ('ch16','正文/第16章-操作系统里的HDR.md')]),
    ('part6','篇六-篇首.md', [
        ('ch17','正文/第17章-ToneMapping.md'),
        ('ch18','正文/第18章-内容世界.md'),
        ('ch19','正文/第19章-选购校准与色彩管理.md'),
        ('ch20','正文/第20章-常见误区与精通路线.md')]),
]
for pid, psrc, chs in parts:
    add(pid,'numbered', psrc, toc='part')
    for cid, csrc in chs:
        add(cid,'numbered', csrc, toc='entry')

add('appendix','numbered','附录/附录A-术语速查.md', toc='entry')
add('refs','numbered','附录/附录B-参考文献.md', toc='entry')
add('afterword','numbered','后记.md', toc='entry')
add('back','back','封底.md')

# ---------- normalize titles & write ----------
manifest = []
for sec in S:
    src = sec.get('src')
    if sec.get('title'):
        title = sec['title']
    elif src:
        title = first_heading(read(src)) or sec['id']
    else:
        title = {'toc':'目录'}.get(sec['kind'], sec['id'])
    sec['title'] = title
    if src:
        sec['body'] = None
    htmlfile = write_section(sec)
    numbered = (sec['kind'] == 'numbered')
    manifest.append(dict(
        id=sec['id'], kind=sec['kind'], title=title,
        toc=sec.get('toc'), html=htmlfile.replace('\\','/'),
        numbered=numbered,
    ))

with open(BUILD + '/manifest.json','w',encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)

print("sections:", len(manifest))
for m in manifest:
    print(" ", m['id'], '|', m['kind'], '|', m['toc'], '|', m['title'])
