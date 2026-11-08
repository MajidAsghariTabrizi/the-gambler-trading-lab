'"""Single-cycle paper runner: live read-only book -> signals -> decision -> paper -> dashboard."""'
import json, urllib.request, datetime, os, sys
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
from decimal import Decimal
from gambler.engine import decide
from gambler.paper import PaperAccount
from gambler.dashboard import render

def fetch_book(symbol='BTCTMN', timeout=15):
    req = urllib.request.Request('https://api.wallex.ir/v1/depth?symbol=' + symbol, headers={'User-Agent': 'gambler-final/1.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read().decode())
    res = d.get('result') or {}
    bids = [(float(b['price']), float(b['quantity'])) for b in (res.get('bid') or [])]
    asks = [(float(a['price']), float(a['quantity'])) for a in (res.get('ask') or [])]
    return max(p for p, _ in bids), min(p for p, _ in asks)

def run_once(t_min=None, ledger=None, offline_book=None):
    now = datetime.datetime.now(datetime.timezone.utc)
    t = t_min or int(now.timestamp()) // 60 * 60
    bb, ba = offline_book if offline_book else fetch_book()
    acct = PaperAccount(ledger_path=ledger or os.path.join(os.path.dirname(__file__), '..', 'evidence', 'paper_ledger.jsonl'))
    rec = decide(t, bb, ba, {'cash': acct.cash, 'btc': acct.btc})
    ev = acct.apply(rec, bb, ba)
    dash = render(rec, 'cash=%s TMN btc=%s' % (acct.cash, acct.btc), ['[EVENT] ' + ev])
    return rec, dash

if __name__ == '__main__':
    rec, dash = run_once()
    print(dash)
    print(json.dumps(rec)[:600])
