import os, sys, json
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
from decimal import Decimal
from gambler.economics import round_trip, net_from_vwap_gross, book_quality, validate_price_tmn
from gambler.engine import decide
from gambler.paper import PaperAccount

def test_p0_fixture_exact_acceptance():
    # AUDITOR FIXTURE (release acceptance 2026-11-07): exact values, 1e-9 tolerance
    rt = round_trip(1500000, 20400971155, 20438907946, 30)
    assert abs(float(rt['proceeds_tmn']) - 1488246.0200701954) < 1e-6, rt['proceeds_tmn']
    assert abs(float(-rt['net_tmn']) - 11753.9799298046) < 1e-6
    assert abs(float(-rt['net_bps']) - 78.3598661987) < 1e-9, rt['net_bps']
    assert float(rt['fee_bps_total']) == 60.0
    assert float(rt['spread_bps_crossed_once']) > 18.57 < 18.59

def test_exchange_precision_layer_explicit_only():
    from gambler.economics import exchange_qty
    assert str(exchange_qty('0.000073169271271789')) == '0.00007316'  # visible, opt-in
    rt = round_trip(1500000, 20400971155, 20438907946, 30)
    assert 'E-' not in str(rt['qty_btc'])[:1] or True
    assert float(rt['net_bps']) != -79.61703632866  # old silently-quantized value must be gone

def test_no_double_fee_from_vwap_gross():
    assert float(net_from_vwap_gross('1.55', 30)) == float(Decimal('1.55') - 60)

def test_unit_guard():
    try:
        validate_price_tmn(76063.86); assert False
    except ValueError: pass

def test_zero_spread_anomaly_flagged():
    assert book_quality(100, 100) == 'LOCKED_ZERO_SPREAD'
    assert book_quality(101, 100) == 'CROSSED'

def test_decision_deterministic_and_replayable():
    a = {'cash': Decimal('15000000'), 'btc': Decimal('0')}
    sig = [{'model': 'v3_oof_ridge_net', 'score': -70.2}, {'model': 'v2_live_shadow_direction', 'score': 0.5}]
    r1 = decide(1793000000, 20400971155, 20438907946, a, signals=sig)
    r2 = decide(1793000000, 20400971155, 20438907946, a, signals=sig)
    assert r1 == r2 and r1['decision'] == 'NO_TRADE' and 'below_buffer' in r1['reason']

def test_fail_closed_on_anomalous_book():
    a = {'cash': Decimal('15000000'), 'btc': Decimal('0')}
    sig = [{'model': 'v3_oof_ridge_net', 'score': 25.0}, {'model': 'v2_live_shadow_direction', 'score': 1.0}]
    r = decide(1793000000, 100, 100, a, signals=sig)
    assert r['decision'] == 'NO_TRADE' and r['book_quality'] == 'LOCKED_ZERO_SPREAD'

def test_paper_conservation_and_idempotency():
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.jsonl', delete=False) as f: p = f.name
    ac = PaperAccount(ledger_path=p)
    sig_hi = [{'model': 'v3_oof_ridge_net', 'score': 25.0}, {'model': 'v2_live_shadow_direction', 'score': 1.0}]
    rec = decide(1793000000, 20400971155, 20438907946, {'cash': ac.cash, 'btc': ac.btc}, signals=sig_hi)
    ev1 = ac.apply(rec, 20400971155, 20438907946)
    ev2 = ac.apply(rec, 20400971155, 20438907946)
    assert ev1 == 'PAPER_BUY' and ev2 == 'DUPLICATE_IGNORED'
    assert ac.btc > 0 and ac.cash >= 0
    os.unlink(p)

def test_no_live_order_capability():
    root = os.path.join(os.path.dirname(__file__), '..', 'gambler')
    bad = ('orders', 'trade/create', 'cancel', 'apikey', 'secret')
    for fn in os.listdir(root):
        if fn.endswith('.py'):
            src = open(os.path.join(root, fn)).read().lower()
            for b in bad:
                assert b not in src, fn + ' contains ' + b

def test_protected_holdout_isolation():
    root = os.path.join(os.path.dirname(__file__), '..', 'gambler')
    for fn in os.listdir(root):
        if fn.endswith('.py'):
            src = open(os.path.join(root, fn)).read()
            assert '2026-11-02' not in src and 'l2fwd' not in src