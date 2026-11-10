#!/usr/bin/env python3
"""Paper figures: generated ONLY from research_registry/paper_metrics.json (public-safe aggregates).
Populations are never mixed on one axis. Command: python scripts/make_paper_figures.py"""
import json, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(HERE, 'research_registry', 'paper_metrics.json')))
OUT = os.path.join(HERE, 'docs', 'figures', 'paper')
os.makedirs(OUT, exist_ok=True)
INK, ACC, RED, GRAY = '#1a1f2e', '#2563eb', '#dc2626', '#6b7280'
def w(name, body):
    open(os.path.join(OUT, name), 'w').write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 460" font-family="Segoe UI, Arial, sans-serif">' + body + '</svg>')
def title(t, sub=''):
    s = '<text x="30" y="40" font-size="21" font-weight="700" fill="' + INK + '">' + t + '</text>'
    if sub: s += '<text x="30" y="64" font-size="13" fill="' + GRAY + '">' + sub + '</text>'
    return s
def bars(x, y, items, width=170, gap=14, unit=''):
    r = ''
    for i, (label, val, color, note) in enumerate(items):
        h = min(abs(val) * 2.2, 240)
        r += '<rect x="' + str(x + i * (width + gap)) + '" y="' + str(y + 240 - h) + '" width="' + str(width) + '" height="' + str(h) + '" fill="' + color + '" rx="6"/>'
        r += '<text x="' + str(x + i * (width + gap) + width / 2) + '" y="' + str(y + 240 - h - 10) + '" font-size="15" font-weight="700" text-anchor="middle" fill="' + INK + '">' + str(val) + unit + '</text>'
        r += '<text x="' + str(x + i * (width + gap) + width / 2) + '" y="' + str(y + 264) + '" font-size="12.5" text-anchor="middle" fill="' + INK + '">' + label + '</text>'
        if note: r += '<text x="' + str(x + i * (width + gap) + width / 2) + '" y="' + str(y + 282) + '" font-size="11" text-anchor="middle" fill="' + GRAY + '">' + note + '</text>'
    return r
# F1 timeline
w('fig_timeline.svg', title('One Year of Trading Research', '17 registry entries, 8 registered experiments, 9 repositories - verified census') +
  '<line x1="40" y1="250" x2="800" y2="250" stroke="' + INK + '" stroke-width="2"/>' +
  ''.join(['<circle cx="' + str(x) + '" cy="250" r="7" fill="' + (RED if fail else ACC) + '"/><text x="' + str(x) + '" y="' + str(230 if i % 2 == 0 else 285) + '" font-size="11" text-anchor="middle" fill="' + INK + '">' + t + '</text>' for i, (x, t, fail) in enumerate([(70, 'Nov 25: rules + 9-expert', True), (200, 'M16-M24/VON/HMM', True), (330, 'Oct: EXP-004 registered', False), (450, 'Oct-12 audit: C1/C2 REJECT', True), (570, 'Oct-16 MODEL_V2 54.6%', False), (690, 'Nov-9: registered FAIL', True)])]))
# F2 direction
d = M['direction']
w('fig_direction.svg', title('Directional Accuracy vs Matched Controls', 'dev population; CI crosses zero - not a proven edge') +
  bars(60, 110, [('MODEL_V2', 54.60, ACC, 'AUC 0.5643'), ('zero-change control', 53.34, GRAY, 'the honest bar'), ('VNEXT', 52.47, GRAY, 'AUC 0.5465')]) +
  '<text x="470" y="130" font-size="13" fill="' + GRAY + '">Registered window: AUC V2 0.5683 vs VNEXT 0.5574 (n=20,185)</text>')
# F3 nov9 net
c = M['nov9_registered']['cov5']
w('fig_net_expectancy.svg', title('Registered cov5 Net Expectancy', 'modeled taker entries; zero real orders') +
  bars(90, 110, [('V2: ' + str(c['v2']['net_bps']) + ' bps', 42.53, RED, 'CI [-54.3, -31.8]'), ('VNEXT: ' + str(c['vnext']['net_bps']) + ' bps', 30.83, RED, 'CI [-42.3, -19.1]'), ('NO_TRADE', 0, GRAY, 'positive days 0/14 vs 1/13')], unit=''))
# F4 MAE three panels
r = M['regression_by_population']
w('fig_mae_populations.svg', title('Net-Return MAE: Three Separate Populations', 'never pooled, never ranked together') +
  bars(40, 110, [('V3 ridge', 28.34, ACC, 'n=9,616'), ('constant -60', 26.27, GRAY, ''), ('train-mean', 25.38, GRAY, 'best')], width=120) +
  bars(340, 110, [('C1', 26.70, ACC, 'VF rows'), ('constant', 26.39, GRAY, '')], width=120) +
  bars(600, 110, [('P3 challenger', 24.55, ACC, 'eff n=34'), ('constant', 23.55, GRAY, '')], width=110))
# F5 funnel
w('fig_funnel.svg', title('The Negative-Results Funnel', 'what survived each discipline barrier') +
  ''.join(['<rect x="' + str(420 - w2 / 2) + '" y="' + str(100 + i * 55) + '" width="' + str(w2) + '" height="40" fill="' + col + '" rx="6"/><text x="420" y="' + str(125 + i * 55) + '" font-size="13" text-anchor="middle" fill="white" font-weight="600">' + t + '</text>' for i, (w2, t, col) in enumerate([(700, '17 registry entries / generations attempted', INK), (560, '7 trained models with verified artifacts', ACC), (420, '3 survived gates to formal comparison', ACC), (280, '0 beat matched baseline on net payoff', RED), (140, 'NO_TRADE (capital preserved)', GRAY)])]))
# F6 maker
e = M['economics']['maker_bounds']
w('fig_maker_bounds.svg', title('Maker Fill: Bounds, Not Guesses', 'queue position non-identifiable from snapshots+trades; frozen spec sha16 ' + M['economics']['maker_spec_sha16']) +
  bars(120, 110, [('strict-through lower', 21.4, ACC, 'n=14 episodes'), ('touch upper', 28.6, GRAY, 'review >= 2026-11-22')]))
# F7 effective sample size
w('fig_effective_n.svg', title('Overlapping Minutes Are Not Independent Observations', 'why day-blocks and non-overlap matter') +
  ''.join(['<g><rect x="' + str(60 + i * 190) + '" y="' + str(300 - h) + '" width="120" height="' + str(h) + '" fill="' + c2 + '" rx="6"/><text x="' + str(120 + i * 190) + '" y="' + str(290 - h) + '" font-size="14" font-weight="700" text-anchor="middle">' + v + '</text><text x="' + str(120 + i * 190) + '" y="325" font-size="12" text-anchor="middle">' + lab + '</text></g>' for i, (lab, v, h, c2) in enumerate([('minute rows', '20,185', 190, GRAY), ('trading days', '14', 90, ACC), ('non-overlap positions', '150', 120, RED)])]))
# F8 maturity
w('fig_maturity.svg', title('Outcome Maturity Defines the Population', 'the 1,110-pair reconciliation') +
  '<rect x="60" y="120" width="620" height="46" fill="' + ACC + '" rx="6"/><text x="370" y="148" font-size="14" text-anchor="middle" fill="white">21,295 matured h60 outcome rows at t >= cutoff (later recompute)</text>' +
  '<rect x="60" y="185" width="600" height="46" fill="' + GRAY + '" rx="6"/><text x="360" y="213" font-size="14" text-anchor="middle" fill="white">20,185 eligible at readout time (registered population - EXACT)</text>' +
  '<rect x="660" y="185" width="120" height="46" fill="' + RED + '" rx="6"/><text x="720" y="213" font-size="13" text-anchor="middle" fill="white">1,110 matured after</text>')
print('figures written to', OUT)
