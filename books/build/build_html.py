# -*- coding: utf-8 -*-
"""系列通用：把某一册的 Markdown 组装成分节 HTML + manifest.json。

用法：
    python books/build/build_html.py --book books/beginner
"""
import os, re, json, argparse
from pathlib import Path
import markdown
from styles import CSS_NORMAL, CSS_COVER, CSS_TITLE, CSS_BACK, TEMPLATE

REPO = Path(__file__).resolve().parents[2]
ASSETS = REPO / "books" / "build"

_MATH = []


def _protect_math(text):
    global _MATH
    _MATH = []
    def rep(m):
        _MATH.append(m.group(0)); return f"@@MATHX{len(_MATH)-1}@@"
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
    for i, tok in enumerate(_MATH):
        html = html.replace(f"@@MATHX{i}@@", tok)
    return html


def _fig(m):
    tag = m.group(1)
    alt = re.search(r'alt="([^"]*)"', tag)
    cap = alt.group(1).strip() if alt else ""
    if cap:
        return '<figure>' + tag + '<figcaption>' + cap + '</figcaption></figure>'
    return '<figure>' + tag + '</figure>'


def md_to_html(text, cfg):
    md = markdown.Markdown(extensions=['extra', 'sane_lists', 'toc', 'attr_list', 'md_in_html'])
    html = md.convert(_protect_math(text))
    html = _restore_math(html)
    html = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>',
                  lambda m: '<pre class="mermaid">' + m.group(1) + '</pre>', html, flags=re.S)
    html = re.sub(r'<p>\s*(<img[^>]*>)\s*</p>', _fig, html)
    # 正文图片 -> 构建用压缩图
    html = re.sub(r'src="(?:\.\./)?images/([^"]+?)\.(?:png|jpg|jpeg|webp)"',
                  r'src="images_opt/\1.jpg"', html, flags=re.I)
    return html


def first_heading(text):
    for line in text.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return None


def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def ensure_opt_images(book, tmp):
    from PIL import Image
    src_root = book / "images"
    out_root = tmp / "images_opt"
    if not src_root.exists():
        return
    for p in src_root.rglob("*"):
        if not p.is_file() or p.name.lower().startswith(('logo1','logo2','logo3')):
            continue
        rel = p.relative_to(src_root)
        ext = p.suffix.lower()
        if ext not in ('.png', '.jpg', '.jpeg', '.webp', '.svg'):
            continue
        dst = out_root / rel
        if ext == '.svg':
            dst = dst.with_suffix('.svg')
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists() or dst.stat().st_mtime < p.stat().st_mtime:
                dst.write_bytes(p.read_bytes())
            continue
        dst = dst.with_suffix('.jpg')
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() and dst.stat().st_mtime >= p.stat().st_mtime:
            continue
        im = Image.open(p).convert("RGB")
        w, h = im.size
        if w > 1400:
            im = im.resize((1400, int(h * 1400 / w)), Image.LANCZOS)
        im.save(dst, "JPEG", quality=88, optimize=True)


def render_cover(text, cfg):
    title = sub = author = date = ''
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith('### '):
            author = s[4:].strip()
        elif s.startswith('## '):
            sub = s[3:].strip()
        elif s.startswith('# '):
            title = s[2:].strip()
        else:
            date = s
    en = 'HDR'
    cn = title
    m = re.match(r'^\s*HDR\s*(.*)$', title, re.I)
    if m:
        cn = m.group(1).strip() or title
    vol = cfg.get('volume') or ''
    vol_html = f'<div class="cv-vol">{vol}</div>' if vol else ''
    return ('<div class="cv-bg"></div><div class="cv-scrim"></div>'
            '<div class="cv-frame"></div>'
            f'<div class="cv-kicker">{cfg.get("kicker", "A COMPLETE GUIDE TO HDR")}</div>'
            '<div class="cv-content">'
            f'<div class="cv-en">{en}</div>'
            f'<div class="cv-cn">{cn}</div>'
            f'{vol_html}'
            '<div class="cv-rule"></div>'
            f'<div class="cv-sub">{sub}</div>'
            '<div class="cv-meta">'
            f'<div class="cv-author">{author}</div>'
            f'<div class="cv-date">{date}</div>'
            '</div></div>')


def render_titlepage(text):
    lines = [s.strip() for s in text.splitlines() if s.strip()]
    t = lines[0] if len(lines) > 0 else ''
    sub = lines[1] if len(lines) > 1 else ''
    author = lines[2] if len(lines) > 2 else ''
    date = lines[3] if len(lines) > 3 else ''
    return ('<div class="tp-title">' + t + '</div>'
            '<div class="tp-sub">' + sub + '</div>'
            '<div class="tp-rule"></div>'
            '<div class="tp-author">' + author + '</div>'
            '<div class="tp-date">' + date + '</div>')


def write_section(sec, book, cfg, tmp, html_dir, css_cover):
    src = sec.get('src')
    text = read(book / src) if src else ''
    kind = sec['kind']
    if kind == 'cover':
        body = render_cover(text, cfg)
    elif kind == 'title':
        body = render_titlepage(text)
    elif kind == 'back':
        body = '<div class="bc-box">' + md_to_html(text, cfg) + '</div>'
    elif src:
        body = md_to_html(text, cfg)
    else:
        body = ''
    css = CSS_NORMAL
    pagecls = ''
    if kind == 'cover':
        css = css_cover; pagecls = 'cover-wrap'
    elif kind == 'title':
        css = CSS_TITLE
    elif kind == 'back':
        css = CSS_BACK
    base_uri = tmp.as_uri() + '/'
    assets_uri = ASSETS.as_uri() + '/'
    tpl = (TEMPLATE
           .replace('file:///E:/Study/HDR技术/book/build/', assets_uri)
           .replace('file:///E:/Study/HDR技术/book/', base_uri))
    html = tpl.format(title=sec['title'], css=css, kind=kind, pagecls=pagecls, body=body)
    out = html_dir / (sec['id'] + '.html')
    out.write_text(html, encoding='utf-8')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--book', default='books/beginner')
    args = ap.parse_args()
    book = (REPO / args.book).resolve()
    name = book.name
    tmp = REPO / 'books' / 'build' / 'tmp' / name
    html_dir = tmp / 'html'
    html_dir.mkdir(parents=True, exist_ok=True)

    cfg = json.loads(read(book / 'book.json'))
    structure = json.loads(read(book / 'structure.json'))
    sections = structure['sections']

    cb = cfg.get('cover_bg', 'images/logo/cover_bg.jpg')
    cb_opt = 'images_opt/' + cb[len('images/'):] if cb.startswith('images/') else cb
    cb_opt = re.sub(r'\.(png|jpe?g|webp)$', '.jpg', cb_opt, flags=re.I)
    css_cover = CSS_COVER.replace('images/logo/cover_bg.jpg', cb_opt)

    ensure_opt_images(book, tmp)

    manifest = []
    for sec in sections:
        src = sec.get('src')
        title = sec.get('title')
        if not title and src:
            title = first_heading(read(book / src)) or sec['id']
        sec['title'] = title or sec['id']
        html = write_section(sec, book, cfg, tmp, html_dir, css_cover)
        manifest.append(dict(id=sec['id'], kind=sec['kind'], title=sec['title'],
                             toc=sec.get('toc'), numbered=(sec['kind'] == 'numbered'),
                             html=str(html).replace('\\', '/')))

    (tmp / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding='utf-8')
    (tmp / 'book.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding='utf-8')
    print('sections:', len(manifest), '->', tmp)


if __name__ == '__main__':
    main()
