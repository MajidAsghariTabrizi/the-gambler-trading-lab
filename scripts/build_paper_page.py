#!/usr/bin/env python3
"""Build the flagship paper page INTO the existing storefront deployment.
Source of truth: docs/research/from-prediction-to-executable-alpha.md (markdown).
Output: storefront/research/from-prediction-to-executable-alpha/index.html (+ figures copy).
No new dependencies: minimal markdown converter, storefront styles reused."""
import os, re, shutil, html
ROOT = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(ROOT, 'docs', 'research', 'from-prediction-to-executable-alpha.md')
OUTDIR = os.path.join(ROOT, 'storefront', 'research', 'from-prediction-to-executable-alpha')
FIGS = os.path.join(ROOT, 'docs', 'figures', 'paper')
os.makedirs(OUTDIR, exist_ok=True)
if os.path.isdir(os.path.join(ROOT, 'storefront', 'figures', 'paper')):
    shutil.rmtree(os.path.join(ROOT, 'storefront', 'figures', 'paper'))
shutil.copytree(FIGS, os.path.join(ROOT, 'storefront', 'figures', 'paper'))
md = open(SRC, encoding='utf-8').read()
if md.startswith('---'):
    md = md.split('---', 2)[2]
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" style="max-width:100%;border:1px solid #e5e7eb;border-radius:8px;margin:8px 0">\n', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\w)\*([^*]+)\*(?!\w)', r'<em>\1</em>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s
out, i, lines, incode, codebuf = [], 0, md.split('\n'), False, []
while i < len(lines):
    ln = lines[i]
    if ln.startswith('~~~'):
        if incode:
            out.append('<pre><code>' + html.escape('\n'.join(codebuf)) + '</code></pre>'); codebuf = []
        incode = not incode; i += 1; continue
    if incode: codebuf.append(ln); i += 1; continue
    m = re.match(r'^(#{1,3}) (.+)$', ln)
    if m:
        h = len(m.group(1)) + 1
        out.append('<h' + str(h) + ' id="' + re.sub(r'[^a-z0-9]+', '-', m.group(2).lower()).strip('-') + '">' + inline(m.group(2)) + '</h' + str(h) + '>'); i += 1; continue
    if ln.startswith('|') and i + 1 < len(lines) and set(lines[i + 1].replace('|', '').replace(' ', '')) <= set('-:'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            if not set(lines[i].replace('|', '').replace(' ', '')) <= set('-:'):
                rows.append([c.strip() for c in lines[i].strip('|').split('|')])
            i += 1
        t = '<table><thead><tr>' + ''.join('<th>' + inline(c) + '</th>' for c in rows[0]) + '</tr></thead><tbody>'
        t += ''.join('<tr>' + ''.join('<td>' + inline(c) + '</td>' for c in r) + '</tr>' for r in rows[1:]) + '</tbody></table>'
        out.append(t); continue
    if ln.startswith('> '):
        buf = []
        while i < len(lines) and lines[i].startswith('> '): buf.append(lines[i][2:]); i += 1
        out.append('<blockquote>' + inline(' '.join(buf)) + '</blockquote>'); continue
    if re.match(r'^\d+\. ', ln) or ln.startswith('- '):
        ordered = re.match(r'^\d+\. ', ln) is not None
        tag = 'ol' if ordered else 'ul'
        buf = []
        while i < len(lines) and (re.match(r'^\d+\. ', lines[i]) or lines[i].startswith('- ')):
            buf.append('<li>' + inline(re.sub(r'^(\\d+\\. |- )', '', lines[i])) + '</li>'); i += 1
        out.append('<' + tag + '>' + ''.join(buf) + '</' + tag + '>'); continue
    if not ln.strip(): i += 1; continue
    buf = []
    while i < len(lines) and lines[i].strip() and not lines[i].startswith(('#', '|', '>', '~~~')) and not re.match(r'^(\d+\. |- )', lines[i]): buf.append(lines[i]); i += 1
    out.append('<p>' + inline(' '.join(buf)) + '</p>')
page = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>From Predictive Accuracy to Executable Alpha - The Gambler Trading Lab</title>
<meta name="description" content="A one-year longitudinal case study: directional accuracy above chance never became positive net expectancy. Registered forward evaluation and exact metric reconciliation.">
<meta property="og:title" content="From Predictive Accuracy to Executable Alpha">
<meta property="og:description" content="How 54.6% directional accuracy became a registered -42.53 bps/trade verdict.">
<meta property="og:type" content="article">
<link rel="canonical" href="https://majidasgharitabrizi.github.io/the-gambler-trading-lab/research/from-prediction-to-executable-alpha/">
<link rel="stylesheet" href="../../styles.css">
</head><body>
<nav class="topnav"><a href="../../">Evidence Observatory</a> <a href="https://github.com/MajidAsghariTabrizi/the-gambler-trading-lab">GitHub</a> <a href="https://github.com/MajidAsghariTabrizi/the-gambler-trading-lab/blob/master/docs/research/ATLAS.md">Research Atlas</a></nav>
<article class="paper">
''' + chr(10).join(out) + '''
</article>
<footer class="foot">The Gambler Trading Lab - zero real orders, LIVE_EXECUTION=OFF throughout. Not investment advice.</footer>
</body></html>'''
open(os.path.join(OUTDIR, 'index.html'), 'w', encoding='utf-8').write(page)
print('paper page written:', os.path.join(OUTDIR, 'index.html'))
