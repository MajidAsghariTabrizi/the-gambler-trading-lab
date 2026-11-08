# Generate figures from committed verified values. Pure python, no deps.
import json, os
F = os.path.join(os.path.dirname(__file__), '..', 'figures')
os.makedirs(F, exist_ok=True)
DATA = {
 'mae': [('Constant -60', 23.546), ('Audited V3 val rows', 24.247), ('P3 challenger', 24.546), ('VF C1', 26.70), ('VF C2', 37.47)],
 'acc': [('VNEXT', 52.47), ('Zero-change control', 53.34), ('MODEL_V2', 54.60)],
 'cost': [('Spread crossed once', 18.58), ('Fees 2x30 compd', 59.78)],
 'spread_dist': [('p95', 34.56), ('p75', 34.56), ('median', 10.4), ('p25', 2.89), ('p05', 1.3)]}
json.dump(DATA, open(os.path.join(F, 'figure_data.json'), 'w'), indent=1)
SVG = 'http:' + '//www.w3.org/2000/svg'
def bar(name, title, rows, unit, note):
    W, H, m = 760, 60 + 44 * len(rows) + 60, 200
    mx = max(v for _, v in rows) * 1.25
    p = ['<svg xmlns="%s" width="%d" height="%d" font-family="Helvetica,Arial,sans-serif">' % (SVG, W, H)]
    p.append('<rect width="100%%" height="100%%" fill="white"/>')
    p.append('<text x="24" y="34" font-size="19" font-weight="bold" fill="#111">%s</text>' % title)
    for i, (label, v) in enumerate(rows):
        y = 70 + i * 44
        w = int((W - m - 60) * v / mx)
        p.append('<text x="24" y="%d" font-size="14" fill="#222">%s</text>' % (y + 16, label))
        p.append('<rect x="%d" y="%d" width="%d" height="22" fill="#2a6f97"/>' % (m, y, w))
        p.append('<text x="%d" y="%d" font-size="14" fill="#111">%.2f %s</text>' % (m + w + 8, y + 17, v, unit))
    p.append('<text x="24" y="%d" font-size="12" fill="#666">%s</text>' % (H - 16, note))
    p.append('</svg>')
    open(os.path.join(F, name), 'w').write(''.join(p))
bar('fig_mae_vs_constant.svg', 'Net-forecast MAE vs constant baseline (lower is better)', DATA['mae'], 'bps', 'Populations differ - see docs/models/BENCHMARKS.md')
bar('fig_direction_accuracy.svg', 'Directional accuracy vs controls (V2 CI crosses zero vs control)', DATA['acc'], '%', 'Day-block CI; ~88 effective independent positions')
bar('fig_cost_decomposition.svg', 'Verified round-trip cost fixture: 78.36 bps total', DATA['cost'], 'bps', 'Assumed fees 0.3 pct/leg; arithmetic fixture, not account terms')
bar('fig_spread_distribution.svg', 'BTCTMN spread distribution quantiles, one dev day (n=412)', DATA['spread_dist'], 'bps', '43.2 pct of matched seconds below 6 bps; aggregate stats only')
print('figures:', len(os.listdir(F)))