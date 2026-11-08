import os, sys, json, time, shutil
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))
from decimal import Decimal
DBDIR = os.path.join(os.path.dirname(__file__), '..', 'state')

def _fresh_db():
    'Point the unified store at a throwaway DB for deterministic integration tests.'
    import unified.state as S
    if getattr(S, '_c', None) is not None:
        try: S._c.close()
        except Exception: pass
    S._c = None
    S.DB = os.path.join(DBDIR, 'test_gambler.db')
    if os.path.exists(S.DB): os.remove(S.DB)
    if os.path.exists(S.DB + '-wal'): os.remove(S.DB + '-wal')
    S.conn()
    return S

def test_A_fresh_data_to_decision():
    S = _fresh_db()
    from unified import cli, predict, decide as ds
    out = cli.run_cycles(1, live=False)  # stub market, real pipeline
    c = out['cycles'][0]
    assert c['ingested'] and c['decision'] == 'NO_TRADE' and c['net_forecast'] is not None
    assert S.events_count() == 1 and json.loads(S.conn().execute('select record from decisions').fetchone()[0])['decision'] == 'NO_TRADE'

def test_B_prediction_to_outcome_to_learning():
    S = _fresh_db()
    from unified import cli, outcome, learn
    cli.run_cycles(1, live=False)
    did = S.conn().execute('select decision_id from decisions').fetchone()[0]
    outcome.record_pending(did, 0)
    n = outcome.mature(now_ms=int(time.time() * 1000) + 7200 * 1000, y_bps_fn=lambda d: 5.0)
    assert n == 1
    r = learn.learning_cycle(min_matured=50)
    assert r['status'] == 'INSUFFICIENT_DATA'  # honest gate at low evidence
    r2 = learn.learning_cycle(min_matured=1)
    assert r2['status'] == 'CHALLENGER_SHADOW_ONLY' and 'GATED_OFF' in r2['promotion']

def test_C_controlled_promotion_atomic():
    S = _fresh_db()
    from unified import registry
    registry.register('champ_v1', 'ridge_net', 'h1', 'w1', {})
    assert registry.promote('champ_v1', 'test-only: synthetic promotion')
    assert registry.champion() == 'champ_v1'
    registry.register('chall_v2', 'ridge_net', 'h2', 'w2', {})
    assert registry.promote('chall_v2', 'test-only: synthetic promotion 2')
    assert registry.champion() == 'chall_v2'
    rows = dict((m[0], m[1]) for m in registry.all_models())
    assert rows['champ_v1'] == 'ROLLED_BACK'  # atomic swap, rollback ref kept
    registry.rollback('champ_v1')
    assert registry.champion() == 'champ_v1'

def test_D_restart_recovery_exactly_once():
    S = _fresh_db()
    from unified import cli
    a = cli.run_cycles(1, live=False)  # process 1
    b = cli.run_cycles(1, live=False)  # process 2 (restart) - same stub minute -> same decision_id
    d1, d2 = a['cycles'][0]['decision_id'], b['cycles'][0]['decision_id']
    n = S.conn().execute('select count(*) from decisions').fetchone()[0]
    assert d1 == d2 and n == 1  # idempotent: exactly-once economic record

def test_E_replay_parity():
    S = _fresh_db()
    from unified import cli
    a = cli.run_cycles(1, live=False)['cycles'][0]['decision_id']
    S2 = _fresh_db()
    b = cli.run_cycles(1, live=False)['cycles'][0]['decision_id']
    assert a == b  # frozen inputs -> identical decision identity

def test_engine_accepts_local_net():
    from gambler.engine import decide as D
    sig = [{'model': 'v3_local_net', 'target': 'executable_net_bps_h60', 'score': -80.8},
           {'model': 'v2_live_shadow_direction', 'score': 1.0}]
    r = D(1794070800, 20211184058, 20254178111, {'cash': Decimal('15000000'), 'btc': Decimal('0')}, signals=sig)
    assert r['decision'] == 'NO_TRADE' and 'below_buffer' in r['reason']

def test_G_isolation_safety():
    root = os.path.join(os.path.dirname(__file__), '..', 'unified')
    bad = ('orders', 'trade/create', 'cancel?', 'apikey', 'secret', '2026-11-02', 'l2fwd')
    for fn in os.listdir(root):
        if fn.endswith('.py'):
            src = open(os.path.join(root, fn)).read().lower()
            for b in bad:
                assert b not in src, fn + ' contains ' + b