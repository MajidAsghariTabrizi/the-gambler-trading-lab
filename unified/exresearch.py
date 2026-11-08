# ExecutionResearchService: integrated maker/taker execution research (P5).
import os, sys, json, time, math, statistics
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from unified.contracts import make_event
from unified import state

SPEC_PATH = os.path.join(os.path.dirname(__file__), '..', 'experiments', 'EXPERIMENT_MAKER_BTCTMN_v1.json')

def load_spec():
    return json.load(open(SPEC_PATH))

def spec_hash():
    import hashlib
    return hashlib.sha256(open(SPEC_PATH, 'rb').read()).hexdigest()[:16]

def parse_tape(depth_lines, trade_lines):
    bids, asks = {}, {}
    for l in depth_lines:
        try:
            r = json.loads(l)
            if r.get('ch') == 'BTCTMN@buyDepth': bids[r['ts']] = max(float(x['price']) for x in r['d'])
            elif r.get('ch') == 'BTCTMN@sellDepth': asks[r['ts']] = min(float(x['price']) for x in r['d'])
        except Exception: pass
    pairs = [{'ts': ts, 'bid': bids[ts], 'ask': asks[ts]} for ts in sorted(set(bids) & set(asks))]
    trades = []
    for l in trade_lines:
        try:
            r = json.loads(l)
            trades.append({'ts': r['ts'], 'buy': r['d']['isBuyOrder'], 'p': float(r['d']['price'])})
        except Exception: pass
    return pairs, sorted(trades, key=lambda x: x['ts'])

def spread_distribution(pairs):
    sp = [10000.0 * (p['ask'] - p['bid']) / ((p['ask'] + p['bid']) / 2) for p in pairs]
    sp.sort()
    def q(f): return sp[min(int(f * len(sp)), len(sp) - 1)]
    return {'n': len(sp), 'p05': round(q(0.05), 2), 'p25': round(q(0.25), 2), 'median': round(q(0.5), 2),
            'p75': round(q(0.75), 2), 'p95': round(q(0.95), 2), 'frac_below_6bps': round(sum(1 for x in sp if x < 6) / len(sp), 4),
            'frac_below_10bps': round(sum(1 for x in sp if x < 10) / len(sp), 4), 'frac_below_20bps': round(sum(1 for x in sp if x < 20) / len(sp), 4)}

def regime_episodes(pairs, thresh_bps=6.0, min_secs=60):
    'Compression episode: >= min_secs consecutive matched snapshots with spread < thresh. DISTRIBUTION-LEVEL, not anecdotes.'
    eps, cur = [], 0
    for p in pairs:
        s = 10000.0 * (p['ask'] - p['bid']) / ((p['ask'] + p['bid']) / 2)
        if s < thresh_bps: cur += 1
        else:
            if cur >= min_secs: eps.append(cur)
            cur = 0
    if cur >= min_secs: eps.append(cur)
    return {'threshold_bps': thresh_bps, 'min_duration_s': min_secs, 'episodes': len(eps),
            'total_s': sum(eps), 'longest_s': max(eps) if eps else 0}

def fill_bounds(pairs, trades, T_ms=600000, sample_every=30):
    'LOWER bound: SELL prints strictly below limit. UPPER bound: touch. Markouts at +T mid.'
    sample = pairs[::sample_every]
    res = {'strict': [], 'touch': []}
    for d in sample:
        b = d['bid']
        t0 = d['ts']
        future_mids = [p for p in pairs if p['ts'] >= t0 + T_ms]
        m = (future_mids[0]['bid'] + future_mids[0]['ask']) / 2 if future_mids else None
        if m is None: continue
        for mode in ('strict', 'touch'):
            for t in trades:
                if t['ts'] <= t0 or t['ts'] > t0 + T_ms or t['buy']: continue
                hit = (t['p'] < b) if mode == 'strict' else (t['p'] <= b)
                if hit:
                    res[mode].append((m / b - 1) * 10000.0)
                    break
    n = max(len(sample), 1)
    out = {}
    for mode in ('strict', 'touch'):
        v = res[mode]
        out[mode] = {'fill_rate': round(len(v) / n, 4), 'n_filled': len(v), 'n_attempts': len(sample),
                     'markout_mean_bps': round(statistics.mean(v), 2) if v else None}
    out['identifiable'] = False
    out['note'] = 'queue position unidentifiable: these are bounds, not estimates'
    return out

def policy_economics(spread_bps, fee_taker=30.0, fee_maker_scen=(0.0, 30.0)):
    rows = {'A_taker_taker': spread_bps + 2 * fee_taker,
            'B_maker_taker_fee0': spread_bps / 2 + fee_taker,
            'B_maker_taker_fee30': spread_bps / 2 + fee_taker + fee_maker_scen[1],
            'C_taker_maker_fee0': spread_bps / 2 + fee_taker,
            'D_maker_maker_fee0': 0.0}
    return {k: round(v, 2) for k, v in rows.items()}

def run_bounded_analysis(depth_lines, trade_lines, persist=True):
    pairs, trades = parse_tape(depth_lines, trade_lines)
    if len(pairs) < 60:
        return {'status': 'INSUFFICIENT_WINDOW', 'pairs': len(pairs)}
    dist = spread_distribution(pairs)
    eps = regime_episodes(pairs)
    fb = fill_bounds(pairs, trades)
    med = dist['median']
    pol = policy_economics(med)
    rec = {'ts_utc': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
           'spec_hash': spec_hash(), 'pairs': len(pairs), 'trades': len(trades),
           'spread_distribution': dist, 'compression_episodes': eps, 'fill_bounds': fb,
           'policy_costs_at_median_bps': pol,
           'verdict_input': {'identifiable': False, 'development_only': True}}
    if persist:
        ev = make_event('vps-readonly-tape', 'BTCTMN', int(pairs[-1]['ts']), int(time.time() * 1000),
                        'EXEC_RESEARCH', rec)
        state.upsert_event(ev)
        state.heartbeat('exresearch', 'pairs %d episodes %d' % (len(pairs), eps['episodes']))
    return rec
