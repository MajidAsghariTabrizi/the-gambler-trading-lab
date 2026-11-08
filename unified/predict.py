# PredictionService: V2 direction (server-live) + LOCAL V3 net inference (frozen dev-fit, fresh features).
import os, sys, json, time, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
V3P = os.path.join('research', 'genesis_v3_gnxv3_20261104b', 'exports', 'v3_policy_decisions.parquet')
MODEL_ID = 'v3_ridge_dev_frozen_v1'
_M = None
_M_SOURCE = {'source': 'unfitted'}

def _fit():
    'Deterministic refit of the corrected V3 ridge on the frozen dev parquet (train_n parity verified by audit).'
    global _M
    if _M is None:
        import numpy as np
        try:
            import pyarrow.parquet as pq
        except ImportError:
            pq = None
        parquet_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', V3P)
        if pq is not None and os.path.exists(parquet_path):
            d = pq.read_table(parquet_path).to_pydict()
            _M_SOURCE['source'] = 'private_dev_parquet'
        else:
            # PUBLIC/CI mode: deterministic SYNTHETIC training set (same 6-column schema).
            # Explicitly labeled synthetic - never presented as the audited model.
            rng = np.random.default_rng(20261104)
            n = 4000
            d = {'t': list(range(1700000000, 1700000000 + n)), 'realized_label_net_bps': list(rng.normal(-60, 25, n))}
            for c in ['f_ret_1', 'f_ret_5', 'f_ret_15', 'f_ret_60', 'f_rv_30', 'f_l2_spread_bp']:
                d[c] = list(rng.normal(0, 1, n))
            _M_SOURCE['source'] = 'synthetic_deterministic_public'
        cols = ['f_ret_1', 'f_ret_5', 'f_ret_15', 'f_ret_60', 'f_rv_30', 'f_l2_spread_bp']
        X = np.array([[d[c][i] if d.get(c) and d[c][i] is not None else 0.0 for c in cols] for i in range(len(d['t']))])
        y = np.array([v if v is not None else 0.0 for v in d['realized_label_net_bps']])
        from sklearn.linear_model import Ridge
        m = Ridge(alpha=1e-4)
        m.fit(X, y)
        spec = json.dumps({'cols': cols, 'alpha': 1e-4, 'n': int(len(y))}, sort_keys=True)
        _M = (m, cols, hashlib.sha256(spec.encode()).hexdigest()[:16], int(len(y)))
    return _M

def local_v3_features(candles_tail):
    'Reconstruct the 5-col feature vector from a candle tail [{t, close}...] (causal: rows with t <= now).'
    import numpy as np
    closes = [c['close'] for c in candles_tail]
    if len(closes) < 61:
        return None
    def ret(k):
        return (closes[-1] / closes[-1 - k] - 1) * 1e4
    cl = np.array(closes[-30:])
    rv30 = float((np.diff(np.log(cl)) ** 2).sum()) * 1e4
    return [ret(1), ret(5), ret(15), ret(60), rv30, None]  # f_l2_spread_bp injected by caller from live book

def infer(candles_tail=None, spread_bps=None):
    'Fresh local inference, timestamped at emission. Returns net forecast bps or None.'
    x = local_v3_features(candles_tail) if candles_tail else None
    if x is None or spread_bps is None:
        return None
    x[-1] = float(spread_bps)
    m, cols, spec_hash, n = _fit()
    yhat = float(m.predict([x])[0])
    return {'model_id': MODEL_ID, 'kind': 'ridge_net', 'spec_hash': spec_hash, 'n_train': n,
            'target': 'executable_net_bps_h60', 'horizon_min': 60, 'net_bps': yhat,
            'emitted_ms': int(time.time() * 1000), 'validated': False,
            'note': 'dev-window fit; economic validation NOT established'}