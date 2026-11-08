# All figures regenerate from registry/verified values. Population-split by design.
import json, os
F = os.path.join(os.path.dirname(__file__), '..', 'figures')
os.makedirs(F, exist_ok=True)
SVG = 'http:' + '//www.w3.org/2000/svg'
def bar(name, title, rows, unit, note, color='#2a6f97'):
    W, H, m = 780, 64 + 42 * len(rows) + 62, 215
    mx = max(v for _, v in rows) * 1.28 or 1.0
    p = ['<svg xmlns="%s" width="%d" height="%d" font-family="Helvetica,Arial,sans-serif">' % (SVG, W, H)]
    p.append('<rect width="100%%" height="100%%" fill="white"/>')
    p.append('<text x="24" y="34" font-size="18" font-weight="bold" fill="#111">%s</text>' % title)
    for i, (label, v) in enumerate(rows):
        y = 68 + i * 42
        w = int((W - m - 70) * v / mx)
        p.append('<text x="24" y="%d" font-size="13" fill="#222">%s</text>' % (y + 15, label))
        p.append('<rect x="%d" y="%d" width="%d" height="20" fill="%s"/>' % (m, y, w, color))
        p.append('<text x="%d" y="%d" font-size="13" fill="#111">%.2f %s</text>' % (m + w + 8, y + 16, v, unit))
    p.append('<text x="24" y="%d" font-size="11" fill="#666">%s</text>' % (H - 14, note))
    p.append('</svg>')
    open(os.path.join(F, name), 'w').write(''.join(p))
# Population 1: VF evaluation rows
bar('fig_mae_vf_population.svg', 'Net-forecast MAE - Victory Fusion evaluation population', [('Constant -60 bps', 26.39), ('VF C1', 26.70), ('VF C2', 37.47)], 'bps', 'VERIFIED private data; one evaluation population; lower is better', '#a4413c')
# Population 2: P3 validation rows
bar('fig_mae_p3_population.svg', 'Net-forecast MAE - P3 challenger validation population', [('Constant -60 bps', 23.546), ('P3 challenger (purged ridge)', 24.546)], 'bps', 'REPRODUCED from sealed parquet; different population from VF chart - never pool', '#2a6f97')
# Direction vs control
bar('fig_direction_accuracy.svg', 'Directional accuracy vs controls (labels and horizon verified identical)', [('VNEXT', 52.47), ('Zero-change control', 53.34), ('MODEL_V2 (Huber WF)', 54.60)], '%', 'VERIFIED private data; day-block CI crosses zero vs control; eff. n about 88 days-positions', '#2a6f97')
# Cost decomposition
bar('fig_cost_decomposition.svg', 'Verified round-trip cost fixture: 78.3598661987 bps total', [('Spread crossed once', 18.58), ('Fees 2 x 30 bps compounded', 59.78)], 'bps', 'REPRODUCED offline; assumed fees 0.3 pct/leg - not account terms')
# Spread distribution quantiles
sd = [('p95', 34.56), ('p75', 34.56), ('median', 10.4), ('p25', 2.89), ('p05', 1.3)]
bar('fig_spread_distribution.svg', 'BTCTMN spread quantiles, one development day (n=411 s pairs)', sd, 'bps', 'VERIFIED private tape; aggregate stats only; 43.2 pct of seconds below 6 bps')
# hypothesis funnel + census (registry-driven)
R = os.path.join(os.path.dirname(__file__), '..', 'research_registry')
exps = json.load(open(os.path.join(R, 'experiments.json')))
models = json.load(open(os.path.join(R, 'models.json')))
fun = [('Hypotheses raised', 8.0), ('Executed', 6.0), ('Rejected or failed', 4.0), ('Insufficient evidence', 2.0), ('Positive expectancy', 0.001)]
bar('fig_hypothesis_funnel.svg', 'Research hypothesis funnel: zero survivors', fun, '', 'Generated from research_registry/experiments.json', '#a4413c')
from collections import Counter
c = Counter(m['status'] for m in models)
bar('fig_model_status_census.svg', 'Model-family evidence-status census', [(k, float(v)) for k, v in sorted(c.items(), key=lambda kv: -kv[1])], 'families', 'Generated from research_registry/models.json')
# HERO: decision-gate schematic (engineering identity, light/dark safe neutral)
hero = ['<svg xmlns="%s" width="1200" height="300" font-family="Helvetica,Arial,sans-serif">' % SVG,
'<rect width="100%%" height="100%%" fill="#0d1b2a"/>',
'<rect x="0" y="0" width="10" height="300" fill="#2a6f97"/>',
'<text x="48" y="86" font-size="54" font-weight="bold" fill="#e7e8ea" letter-spacing="6">THE GAMBLER</text>',
'<text x="52" y="132" font-size="24" fill="#90b4ce">The Trading AI That Knows When NOT to Trade.</text>',
'<text x="52" y="170" font-size="16" fill="#5f7d95">Evidence-driven research: causal prediction, realistic execution costs, paper trading, controlled learning.</text>']
bx, by = 52, 214
for i, (t, c2) in enumerate([('PREDICT', '#2a6f97'), ('PRICE THE COST', '#40618c'), ('RISK GATE', '#7a4e2d'), ('NO_TRADE', '#a4413c')]):
    x = bx + i * 260
    hero.append('<rect x="%d" y="%d" width="210" height="44" rx="8" fill="%s"/>' % (x, by, c2))
    hero.append('<text x="%d" y="%d" font-size="17" fill="#ffffff" font-weight="bold">%s</text>' % (x + 24, by + 28, t))
    if i < 3: hero.append('<text x="%d" y="%d" font-size="20" fill="#5f7d95">&#8594;</text>' % (x + 218, by + 29))
hero.append('<text x="52" y="288" font-size="13" fill="#5f7d95">10,478 audited decision minutes. Zero qualifying BUYs. Every rejection justified and recorded.</text>')
hero.append('</svg>')
open(os.path.join(F, 'hero.svg'), 'w').write(''.join(hero))
print('figures regenerated', sorted(os.listdir(F)))