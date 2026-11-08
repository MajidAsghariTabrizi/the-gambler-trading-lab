'"""Common inference interface over RECOVERED models only."""'
import os, json, hashlib
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
V3P = os.path.join(ROOT, 'research', 'genesis_v3_gnxv3_20261104b', 'exports', 'v3_policy_decisions.parquet')
SHDW = os.path.join(ROOT, 'research', '_pull', 'shadow.jsonl')
EMIT_LAG_MS = 125000

def _sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()[:16]

_V3 = None; _V2 = None
def v3_forecasts():
    global _V3
    if _V3 is None:
        import pyarrow.parquet as pq
        d = pq.read_table(V3P).to_pydict()
        _V3 = {t: v for t, v in zip(d['t'], d['predicted_net_bps']) if v is not None}
    return _V3

def v2_scores():
    global _V2
    if _V2 is None:
        _V2 = {}
        for l in open(SHDW, encoding='utf-8'):
            try:
                r = json.loads(l)
                if r.get('oof') is False: _V2[int(r['t'])] = float(r['score'])
            except Exception: pass
    return _V2

def signals_for(t_min):
    out = []
    v3, v2 = v3_forecasts(), v2_scores()
    if t_min in v3: out.append({'model': 'v3_oof_ridge_net', 'target': 'executable_net_bps_h60', 'horizon_min': 60,
        'score': v3[t_min], 'available_ms': t_min * 1000 + EMIT_LAG_MS, 'validation': 'MAE 28.34/IC -0.0118 (audit-parity)',
        'model_hash': _sha(V3P), 'age_note': 'frozen dev-window OOF; never refit'})
    if t_min in v2: out.append({'model': 'v2_live_shadow_direction', 'target': 'direction_score', 'horizon_min': 60,
        'score': v2[t_min], 'available_ms': t_min * 1000 + EMIT_LAG_MS, 'validation': 'acc 54.60/AUC 0.5643; CI vs control crosses 0',
        'model_hash': _sha(SHDW), 'age_note': 'live emitter, refit daily 00:00Z'})
    return out
