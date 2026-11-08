import os, sys, time, datetime
from conftest import needs_private
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
P = os.path.join('..', '..', '..', 'research', 'genesis_v3_gnxv3_20261104b', 'exports', 'v3_policy_decisions.parquet')

def test_p3_outcome_join_maturity():
    from unified import state, outcome
    state._c = None
    state.DB = os.path.join(os.path.dirname(__file__), '..', 'state', 'test_p3.db')
    for suf in ('', '-wal', '-shm'):
        if os.path.exists(state.DB + suf):
            try: os.remove(state.DB + suf)
            except Exception: pass
    state.conn()
    t0 = int(time.time()) - 7200
    did = datetime.datetime.fromtimestamp(t0, datetime.timezone.utc).isoformat() + '|hist'
    state.conn().execute('insert or ignore into decisions values (?,?,?,?,?,?)', (did, t0 * 1000, 'NO_TRADE', 'seed', 'v3', '{}'))
    outcome.record_pending(did, t0 * 1000)
    n = outcome.mature(now_ms=int(time.time() * 1000), y_bps_fn=lambda d: 3.0)
    row = state.conn().execute('select matured, y_bps from outcomes where decision_id=?', (did,)).fetchone()
    assert n == 1 and row[0] == 1 and row[1] == 3.0

@needs_private
def test_p3_parity_is_reconstruction_not_equivalence():
    import numpy as np
    import pyarrow.parquet as pq
    d = pq.read_table(os.path.join(os.path.dirname(__file__), P)).to_pydict()
    m = np.array([v is not None for v in d['predicted_net_bps']])
    y = np.array([0.0 if v is None else float(v) for v in d['realized_label_net_bps']])
    cols = ['f_ret_1', 'f_ret_5', 'f_ret_15', 'f_ret_60', 'f_rv_30', 'f_l2_spread_bp']
    X = np.array([[0.0 if d[c][i] is None else float(d[c][i]) for c in cols] for i in range(len(m))])
    from sklearn.linear_model import Ridge
    fit = Ridge(alpha=1e-4).fit(X[m], y[m])
    ph = np.array([float(v) for i, v in enumerate(d['predicted_net_bps']) if m[i]])
    corr = float(np.corrcoef(fit.predict(X[m]), ph)[0, 1])
    assert abs(corr) < 0.5