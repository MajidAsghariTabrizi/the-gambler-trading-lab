#!/usr/bin/env python
"""Offline deterministic demo: synthetic book -> synthetic-model net forecast -> cost gate -> decision -> ledger."""
import sys, os, json, random, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decimal import Decimal
from gambler.engine import decide
from gambler.economics import round_trip
from gambler.paper import PaperAccount

random.seed(42)  # deterministic

# 1) synthetic market book (SYNTHETIC VALUES, realistic scale)
base = 20_250_000_000.0
mid = base * (1 + random.uniform(-0.001, 0.001))
spread_bps = 18.58
half = mid * spread_bps / 2 / 10_000
bid, ask = mid - half, mid + half

# 2) verified cost fixture demonstration (from tests)
rt = round_trip(1_500_000, 20_400_971_155, 20_438_907_946, 30)

# 3) synthetic net forecast below the +10 bps buffer (the honest usual case)
signal_net = -70.2
sig = [{'model': 'demo_synthetic_net', 'target': 'executable_net_bps_h60', 'score': signal_net},
       {'model': 'demo_synthetic_direction', 'score': 0.8}]

acct = PaperAccount(cash_tmn='15000000')  # in-memory ledger
rec = decide(1794070800, bid, ask, {'cash': acct.cash, 'btc': acct.btc}, signals=sig)

print('=== THE GAMBLER - OFFLINE DEMO (synthetic data) ===')
print('[BOOK]      bid %.0f ask %.0f spread %.2f bps (SYNTHETIC)' % (bid, ask, spread_bps))
print('[FIXTURE]   1.5M round trip -> %s TMN (cost %.10f bps, exact)' % (rt['proceeds_tmn'], -rt['net_bps']))
print('[FORECAST]  net %+.2f bps (synthetic model)' % signal_net)
print('[ACCOUNT]   cash %s TMN, btc %s' % (acct.cash, acct.btc))
print('[DECISION]  %s - %s' % (rec['decision'], rec['reason']))
print('[RULE]      BUY requires validated net forecast >= +10 bps AND direction agreement AND clean book')
print()
print(json.dumps(rec, indent=1, default=str)[:900])
print()
print('Ledger event:', acct.apply(rec, bid, ask))
print('Deterministic: run twice, byte-identical output (seed=42).')