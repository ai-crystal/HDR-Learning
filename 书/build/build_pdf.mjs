// 渲染 HTML -> PDF（Chrome），计算页数，生成目录，合并，加盖页眉页码。
import fs from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';
import { pathToFileURL } from 'url';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const { PDFDocument, rgb } = require('./pdf-lib.min.js');
let fontkit = require('./fontkit.umd.js');
if (fontkit && fontkit.default) fontkit = fontkit.default;

const BUILD = 'E:/Study/HDR-Learning/书/build';
const PDFDIR = BUILD + '/pdf';
const OUTDIR = 'E:/Study/HDR-Learning/书籍输出';
const OUT = OUTDIR + '/HDR超详解.pdf';
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const SIMHEI = 'C:/Windows/Fonts/simhei.ttf';
const BOOKTITLE = 'HDR 超详解';

fs.mkdirSync(PDFDIR, { recursive: true });
fs.mkdirSync(OUTDIR, { recursive: true });

const manifest = JSON.parse(fs.readFileSync(BUILD + '/manifest.json', 'utf-8'));

function render(htmlPath, pdfPath) {
  const url = pathToFileURL(htmlPath).href;
  execFileSync(CHROME, [
    '--headless=new', '--disable-gpu', '--no-sandbox',
    '--allow-file-access-from-files',
    '--no-pdf-header-footer', '--print-to-pdf-no-header',
    '--virtual-time-budget=25000',
    '--print-to-pdf=' + pdfPath, url
  ], { stdio: 'ignore', timeout: 120000 });
  if (!fs.existsSync(pdfPath)) throw new Error('render failed: ' + htmlPath);
}

async function pageCount(pdfPath) {
  const doc = await PDFDocument.load(fs.readFileSync(pdfPath));
  return doc.getPageCount();
}

function shortTitle(sec) {
  const t = sec.title;
  let m = t.match(/^第\s*0?(\d+)\s*章/);
  if (m) return '第 ' + m[1] + ' 章';
  m = t.match(/^第([一二三四五六])篇/);
  if (m) return '第' + m[1] + '篇';
  return t;
}

function buildTocHtml(startPages, firstNumberedStart) {
  // 用 preface 已生成的 html 作为模板，替换 <main> 内容。
  const tplPath = manifest.find(s => s.id === 'preface').html;
  let tpl = fs.readFileSync(tplPath, 'utf-8');
  const css = `<style>
.toc{font-family:"Microsoft YaHei",sans-serif;font-size:11pt;margin-top:8pt;}
.toc-part{display:flex;align-items:baseline;font-weight:700;color:#12233b;margin:14pt 0 5pt;border-bottom:0.6pt solid #dce3ea;padding-bottom:3pt;}
.toc-item{display:flex;align-items:baseline;margin:3.5pt 0;padding-left:12pt;color:#243244;}
.toc .dots{flex:1;border-bottom:1px dotted #b7c0ca;margin:0 6pt 3pt;}
.toc .p{font-variant-numeric:tabular-nums;color:#555;}
.toc-title{border-bottom:2.4pt solid #1f4e79;}
</style>`;
  tpl = tpl.replace('</style>', css + '</style>');
  tpl = tpl.replace(/<title>[\s\S]*?<\/title>/, '<title>目录</title>');
  let rows = '';
  for (const m of manifest) {
    if (m.toc === 'part') {
      const pg = m.numbered ? (startPages[m.id] - firstNumberedStart + 1) : '';
      rows += `<div class="toc-part"><span class="t">${m.title}</span><span class="dots"></span><span class="p">${pg}</span></div>`;
    } else if (m.toc === 'entry') {
      const pg = m.numbered ? (startPages[m.id] - firstNumberedStart + 1) : '';
      rows += `<div class="toc-item"><span class="t">${m.title}</span><span class="dots"></span><span class="p">${pg}</span></div>`;
    }
  }
  const body = `<h1 class="toc-title">目录</h1><div class="toc">${rows}</div>`;
  tpl = tpl.replace(/<main[^>]*>[\s\S]*?<\/main>/, `<main class="page">${body}</main>`);
  const out = BUILD + '/html/toc.html';
  fs.writeFileSync(out, tpl, 'utf-8');
  return out;
}

(async () => {
  // pass 1: render all sections (toc placeholder html already exists)
  const counts = {};
  for (const m of manifest) {
    const pdf = PDFDIR + '/' + m.id + '.pdf';
    render(m.html, pdf);
    counts[m.id] = await pageCount(pdf);
  }
  // compute start pages (0-based within merged book)
  function computeStarts(cnt) {
    const starts = {}; let acc = 0;
    for (const m of manifest) { starts[m.id] = acc; acc += cnt[m.id]; }
    return { starts, total: acc };
  }
  let { starts } = computeStarts(counts);
  let firstNumberedStart = starts[manifest.find(m => m.numbered).id];

  // build TOC with numbers and re-render; iterate until page count stabilises
  const tocPdf = PDFDIR + '/toc.pdf';
  const numberedFirstId = manifest.find(m => m.numbered).id;
  for (let iter = 0; iter < 5; iter++) {
    ({ starts } = computeStarts(counts));
    firstNumberedStart = starts[numberedFirstId];
    const tocHtml = buildTocHtml(starts, firstNumberedStart);
    render(tocHtml, tocPdf);
    const tc = await pageCount(tocPdf);
    if (tc === counts['toc']) break;
    counts['toc'] = tc;
  }

  // 导出书签（大纲）数据，供 apply_outline.py 写入 PDF
  const outline = [];
  const push = (lvl, title, id) => outline.push([lvl, title, starts[id] + 1]);
  push(1, "封面", "cover");
  push(1, "前言", "preface");
  push(1, "目录", "toc");
  for (const m of manifest) {
    if (m.id.startsWith("part")) push(1, m.title, m.id);
    else if (m.id.startsWith("ch")) push(2, m.title, m.id);
    else if (m.id === "appendix") push(1, "附录 A　术语速查表", m.id);
    else if (m.id === "refs") push(1, "附录 B　参考文献", m.id);
    else if (m.id === "afterword") push(1, "后记", m.id);
  }
  fs.writeFileSync(BUILD + '/outline.json', JSON.stringify(outline, null, 1), 'utf-8');
  console.log('outline entries =', outline.length);

  // merge
  const out = await PDFDocument.create();
  out.registerFontkit(fontkit);
  const font = await out.embedFont(fs.readFileSync(SIMHEI), { subset: true });
  for (const m of manifest) {
    const src = await PDFDocument.load(fs.readFileSync(PDFDIR + '/' + m.id + '.pdf'));
    const pages = await out.copyPages(src, src.getPageIndices());
    pages.forEach(p => out.addPage(p));
  }

  // stamping
  const total = out.getPageCount();
  // page -> section
  const pageSec = [];
  for (const m of manifest) {
    for (let i = 0; i < counts[m.id]; i++) pageSec.push(m.id);
  }
  const byId = Object.fromEntries(manifest.map(m => [m.id, m]));
  const grey = rgb(0.42, 0.45, 0.5);
  const navy = rgb(0.13, 0.2, 0.31);
  for (let i = 0; i < total; i++) {
    const sec = byId[pageSec[i]];
    if (!sec || !sec.numbered) continue;
    const page = out.getPage(i);
    const { width, height } = page.getSize();
    const marginX = 56.7;
    const num = i - firstNumberedStart + 1;
    // header
    page.drawText(BOOKTITLE, { x: marginX, y: height - 34, size: 8, font, color: grey });
    const st = shortTitle(sec);
    const stw = font.widthOfTextAtSize(st, 8);
    page.drawText(st, { x: width - marginX - stw, y: height - 34, size: 8, font, color: grey });
    // footer page number
    const s = String(num);
    const w = font.widthOfTextAtSize(s, 9);
    page.drawText(s, { x: (width - w) / 2, y: 28, size: 9, font, color: navy });
  }

  const bytes = await out.save();
  let target = OUT;
  try {
    fs.writeFileSync(OUT, bytes);
  } catch (e) {
    target = OUTDIR + '/HDR超详解-new.pdf';
    fs.writeFileSync(target, bytes);
    console.log('(原文件被占用，已输出为新文件)', e.code);
  }
  console.log('OK total pages =', total);
  fs.writeFileSync(BUILD + '/last_output.txt', target);
  console.log('first numbered page index =', firstNumberedStart);
  console.log('output =', target);
})().catch(e => { console.error(e); process.exit(1); });
