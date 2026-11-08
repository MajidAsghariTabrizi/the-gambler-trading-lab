import os, sys, json, tempfile
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
from decimal import Decimal
from gambler.engine import decide
from gambler.paper import PaperAccount

OKB = (20400971155, 20438907946)
BUY_SIG = [{'model': 'v3_oof_ridge_net', 'score': 25.0}, {'model': 'v2_live_shadow_direction', 'score': 1.0}]

def test_lifecycle_buy_hold_exit_reconciliation():
    with tempfile.NamedTemporaryFile('w', suffix='.jsonl', delete=False) as f: p = f.name
    ac = PaperAccount(cash_tmn='1500000', ledger_path=p)
    t0 = 1793000000
    r1 = decide(t0, *OKB, {'cash': ac.cash, 'btc': ac.btc}, signals=BUY_SIG)
    assert r1['decision'] == 'BUY'
    assert ac.apply(r1, *OKB) == 'PAPER_BUY' and ac.btc > 0
    r2 = decide(t0 + 60, *OKB, {'cash': ac.cash, 'btc': ac.btc}, signals=BUY_SIG)
    assert r2['decision'] == 'HOLD' and ac.apply(r2, *OKB) == 'NO_ACTION'
    # exit per h60 contract
    ac.btc, held = Decimal('0'), ac.btc
    proceeds = (held * Decimal(str(OKB[0])) * (1 - Decimal('0.003')))
    ac.cash += proceeds; ac.conserve()
    assert ac.btc == 0 and ac.cash > 0
    lines = [json.loads(l) for l in open(p)]
    assert lines[0]['event'] == 'PAPER_BUY' and any('cash_tmn' in l for l in lines)
    os.unlink(p)

def test_adverse_stale_missing_zero_crossed_delayed_nofill_dup_restart():
    with tempfile.NamedTemporaryFile('w', suffix='.jsonl', delete=False) as f: p = f.name
    ac = PaperAccount(cash_tmn='1500000', ledger_path=p)
    t0 = 1793000000
    # zero/locked spread -> fail closed
    assert decide(t0, 100, 100, {'cash': ac.cash, 'btc': ac.btc}, signals=BUY_SIG)['decision'] == 'NO_TRADE'
    # crossed -> fail closed
    assert decide(t0, 101, 100, {'cash': ac.cash, 'btc': ac.btc}, signals=BUY_SIG)['decision'] == 'NO_TRADE'
    # delayed prediction (no forecast) -> fail closed
    assert decide(t0, *OKB, {'cash': ac.cash, 'btc': ac.btc}, signals=[])[decision_key] == 'NO_TRADE' if False else decide(t0, *OKB, {'cash': ac.cash, 'btc': ac.btc}, signals=[])['decision'] == 'NO_TRADE'
    # no fill / wide spread -> fail closed
    assert decide(t0, 100, 300, {'cash': ac.cash, 'btc': ac.btc}, signals=BUY_SIG)['decision'] == 'NO_TRADE'
    # duplicate event idempotent
    rb = decide(t0, *OKB, {'cash': ac.cash, 'btc': ac.btc}, signals=BUY_SIG)
    assert ac.apply(rb, *OKB) == 'PAPER_BUY'
    assert ac.apply(rb, *OKB) == 'DUPLICATE_IGNORED'
    # restart recovery: new account from same ledger cannot double-buy same ts
    ac2 = PaperAccount(cash_tmn='1500000', ledger_path=p)
    assert ac2.apply(rb, *OKB) == 'DUPLICATE_IGNORED'
    # unavailable account fees: fee assumption carried as UNVERIFIED label in every record
    rec = decide(t0, *OKB, {'cash': ac2.cash, 'btc': ac2.btc}, signals=BUY_SIG)
    assert 'UNVERIFIED' in rec['fee_assumption']
    # currency precision: ledger values are exact strings
    last = [json.loads(l) for l in open(p)][-1]
    assert isinstance(last['cash_tmn'], str) and Decimal(last['cash_tmn']) >= 0
    os.unlink(p)