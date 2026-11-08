import re, os, sys
root = os.path.dirname(os.path.abspath(__file__))
bad = []
for dirpath, _, files in os.walk(root):
    for fn in files:
        if not fn.endswith('.md'): continue
        fp = os.path.join(dirpath, fn)
        for m in re.finditer(r'\]\(([^)#?\s]+)(?:#[^)\s]*)?\)', open(fp, encoding='utf-8').read()):
            t = m.group(1)
            if t.startswith(('http://', 'https://', 'mailto:')): continue
            if not os.path.exists(os.path.normpath(os.path.join(dirpath, t))): bad.append(fn + ' -> ' + t)
print('BROKEN_LINKS', len(bad))
for b in bad: print(' ', b)