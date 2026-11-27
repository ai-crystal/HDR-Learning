import io, re

p = 'chapters/ch03.md'
s = io.open(p, encoding='utf-8').read()

print('chars', len(s))
print('lines', s.count('\n') + 1)
print('ctrl chars', [hex(ord(c)) for c in s if ord(c) < 32 and c != '\n'])
print('display math blocks', s.count('$$'), '(must be even)')
print('images', re.findall(r'images/03/([a-z0-9_]+\.png)', s))
print('headings:')
for l in s.split('\n'):
    if l.startswith('#'):
        print('  ', l)
bad = [c for c in '_*#$%&<>|' if c in ''.join(l for l in s.split('\n') if l.startswith('#'))]
print('bad heading chars', bad)
# 单反斜杠后跟字母的可疑 LaTeX？（行内 $ 里 \b \t 会被吃掉）
sus = re.findall(r'\\[a-zA-Z]{0,2}(?![a-zA-Z])', s)
print('backslash count', s.count('\\'))
print('cases blocks', s.count('\\begin{cases}'), s.count('\\end{cases}'))
print('paragraph count', len([b for b in s.split('\n\n') if b.strip()]))
