# CLI: python -m unified.cli status|run|validate|models
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from unified import state, registry, monitor, ingest, decide as ds, outcome, learn

def run_cycles(n=1, live=True):
    from unified import decide as dsmod
    outs = []
    for i in range(n):
        if live:
            r = ingest.ingest_once()
        else:
            r = r_stub()
            ev = __import__('unified.contracts', fromlist=['make_event']).make_event(
                'stub', 'BTCTMN', r['pkt']['v2_row']['t'] * 1000, int(time.time() * 1000), 'MARKET_V2_BOOK',
                {'bid': r['pkt']['book']['bid'], 'ask': r['pkt']['book']['ask'], 'v2_score': r['pkt']['v2_row']['score'],
                 'emit_write_ms': r['pkt']['emit_write_ms']})
            state.upsert_event(ev)
            state.heartbeat('market_data', 'stub event')
        if not r.get('ingested'):
            outs.append({'cycle': i, 'ingested': False, 'reason': 'stale/schema/book'}); continue
        pkt = r['pkt']
        'candle tail fetch for local V3 inference:'
        candles = candle_tail() if live else synth_candles()
        from unified import predict
        spr = (pkt['book']['ask'] - pkt['book']['bid']) / ((pkt['book']['ask'] + pkt['book']['bid']) / 2) * 1e4
        nf = predict.infer(candles_tail=candles, spread_bps=spr)
        did, rec = dsmod.decide_and_record(pkt, nf)
        outs.append({'cycle': i, 'ingested': True, 'decision': rec['decision'], 'reason': rec['reason'],
                     'net_forecast': (nf or {}).get('net_bps'), 'decision_id': did})
        state.heartbeat('runner', 'cycle %d' % i)
    lr = learn.learning_cycle()
    outcome.mature()
    return {'cycles': outs, 'learning': lr, 'dashboard': monitor.dashboard()}

def r_stub():
    return {'ingested': True, 'pkt': {'book': {'ok': True, 'bid': 20211184058.0, 'ask': 20254178111.0},
            'v2_row': {'t': 1794070800, 'score': 1.2, 'spec': 'stub'}, 'emit_write_ms': int(time.time() * 1000) - 1000, 'fresh': True}}

def synth_candles():
    import random
    random.seed(42)
    c = 20200000000.0
    out = []
    for i in range(120):
        c = c * (1 + random.uniform(-0.0005, 0.0005))
        out.append({'t': 1794070000 + i * 60, 'close': c})
    return out

def candle_tail():
    from unified.ingest import _ssh
    import json as J
    raw = _ssh('f=$(/bin/ls -1 /private/redacted/candles/BTCTMN_1m/*.jsonl | tail -n 1); tail -n 120 $f')
    out = []
    for l in raw.splitlines():
        try:
            r = J.loads(l)
            out.append({'t': r.get('time') or r.get('t') or 0, 'close': float(r.get('close') or r.get('c'))})
        except Exception:
            pass
    out = [o for o in out if o['close'] > 0]
    return out[-90:] or None

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    if cmd == 'status':
        print(monitor.dashboard())
    elif cmd == 'run':
        n = int(sys.argv[sys.argv.index('--cycles') + 1]) if '--cycles' in sys.argv else 1
        live = '--stub' not in sys.argv
        print(json.dumps(run_cycles(n, live), indent=1)[:2000])
    elif cmd == 'models':
        for m in registry.all_models():
            print(m)
    elif cmd == 'exresearch':
        from unified import exresearch as XR
        from unified.ingest import _ssh
        depth = _ssh('f=$(ls -1 /private/redacted/micro/raw/BTCTMN/depth/*.jsonl.gz | tail -n 1); zcat $f | tail -n 6000', timeout=240).splitlines()
        trades = _ssh('tail -n 4000 /private/redacted/micro/raw/BTCTMN/$(date -u +%Y-%m-%d).jsonl', timeout=120).splitlines()
        print(json.dumps(XR.run_bounded_analysis(depth, trades), indent=1)[:2400])
    elif cmd == 'validate':
        print('events=%d decisions=%d account=%s' % (state.events_count(),
              state.conn().execute('select count(*) from decisions').fetchone()[0], state.account_state()))
