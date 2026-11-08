# Atlas figures from the registry (single source of truth).
import json, os
R = os.path.join(os.path.dirname(__file__), '..', 'research_registry')
F = os.path.join(os.path.dirname(__file__), '..', 'figures')
models = json.load(open(os.path.join(R, 'models.json')))
exps = json.load(open(os.path.join(R, 'experiments.json')))
SVG = 'http:' + '//www.w3.org/2000/svg'
def bar(name, title, rows, unit, note, color='#2a6f97'):
    W, H, m = 760, 60 + 40 * len(rows) + 60, 210
    mx = max(v for _, v in rows) * 1.3 or 1
    p = ['<svg xmlns="%s" width="%d" height="%d" font-family="Helvetica,Arial,sans-serif">' % (SVG, W, H)]
    p.append('<rect width="100%%" height="100%%" fill="white"/>')
    p.append('<text x="24" y="34" font-size="18" font-weight="bold" fill="#111">%s</text>' % title)
    for i, (label, v) in enumerate(rows):
        y = 66 + i * 40
        w = int((W - m - 70) * v / mx)
        p.append('<text x="24" y="%d" font-size="13" fill="#222">%s</text>' % (y + 15, label))
        p.append('<rect x="%d" y="%d" width="%d" height="20" fill="%s"/>' % (m, y, w, color))
        p.append('<text x="%d" y="%d" font-size="13" fill="#111">%s %s</text>' % (m + w + 8, y + 16, ('%.2f' % v) if isinstance(v, float) else v, unit))
    p.append('<text x="24" y="%d" font-size="11" fill="#666">%s</text>' % (H - 14, note))
    p.append('</svg>')
    open(os.path.join(F, name), 'w').write(''.join(p))
# hypothesis funnel
fun = [('Hypotheses raised', 8), ('Executed', 6), ('Rejected/failed', 4), ('Insufficient evidence', 2), ('Positive expectancy', 0)]
bar('fig_hypothesis_funnel.svg', 'Research hypothesis funnel: zero survivors', [(a, float(b)) for a, b in fun], '', 'From registry experiments.json; the null result is the finding', '#a4413c')
# status census
from collections import Counter
c = Counter(m['status'] for m in models)
rows = sorted(c.items(), key=lambda kv: -kv[1])
bar('fig_model_status_census.svg', 'Model-family evidence-status census (registry)', [(k, float(v)) for k, v in rows], 'families', 'Generated from research_registry/models.json')
print('atlas figures written')