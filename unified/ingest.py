# MarketDataService: one authorized read-only VPS pull -> book + latest V2 row + candle tail.
import json, subprocess, os, time, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from unified.contracts import make_event, now_iso
KEY = os.path.join(os.environ.get('USERPROFILE', ''), '.ssh', '__KEY_FROM_ENV__')

def _ssh(cmd, timeout=60):
    full = ['ssh', '-o', 'ConnectTimeout=25', '-o', 'BatchMode=yes', '-i', KEY, '__SSH_TARGET_FROM_ENV__', cmd]
    return subprocess.run(full, capture_output=True, text=True, timeout=timeout).stdout.strip()

def pull_once():
    'Single combined read-only probe. Receipt times recorded LOCALLY at the moment of receipt.'
    received_ms = int(time.time() * 1000)
    raw = _ssh('date -u +%s; stat -c %Y /private/redacted/vnext/model_v2/shadow.jsonl; tail -1 /private/redacted/vnext/model_v2/shadow.jsonl')
    lines = [l for l in raw.splitlines() if l.strip()]
    if len(lines) < 3:
        return {'ok': False, 'error': 'ssh_short_output', 'received_ms': received_ms}
    server_now_s = int(lines[0]); mtime_s = int(lines[1])
    row = json.loads(lines[2])
    'book via local fetch (or fallback ssh curl):'
    try:
        import urllib.request
        req = urllib.request.Request('https://api.wallex.ir/v1/depth?symbol=BTCTMN', headers={'User-Agent': 'gambler-unified/1.0'})
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.loads(r.read().decode())
        res = d.get('result') or {}
        bid = max(float(b['price']) for b in res['bid']); ask = min(float(a['price']) for a in res['ask'])
        top_bid_qty = sum(float(b['quantity']) for b in res['bid'][:1]); top_ask_qty = sum(float(a['quantity']) for a in res['ask'][:1])
        book = {'ok': True, 'bid': bid, 'ask': ask, 'top_bid_qty': top_bid_qty, 'top_ask_qty': top_ask_qty}
    except Exception as e:
        book = {'ok': False, 'error': type(e).__name__}
    age = server_now_s - row['t']
    return {'ok': True, 'received_ms': received_ms, 'server_now_s': server_now_s, 'emit_write_ms': mtime_s * 1000,
            'v2_row': row, 'v2_age_s': age, 'fresh': 0 <= age <= 900, 'book': book}

def ingest_once(store_event=True):
    pkt = pull_once()
    if not pkt.get('ok') or not pkt.get('fresh') or not pkt['book'].get('ok'):
        return {'ingested': False, 'pkt': pkt}
    if store_event:
        from unified import state
        ev = make_event('vps-readonly+wallex', 'BTCTMN', pkt['v2_row']['t'] * 1000, pkt['received_ms'], 'MARKET_V2_BOOK',
                        {'bid': pkt['book']['bid'], 'ask': pkt['book']['ask'], 'v2_score': pkt['v2_row']['score'],
                         'v2_p': pkt['v2_row'].get('p'), 'emit_write_ms': pkt['emit_write_ms'], 'server_now_s': pkt['server_now_s']})
        state.upsert_event(ev)
        state.heartbeat('market_data', 'event ' + ev['event_id'][:8])
    return {'ingested': True, 'pkt': pkt}
