'"""Live MODEL_V2 shadow emitter adapter - authorized read-only SSH tail."""'
import json, subprocess, datetime, os
REMOTE = '/private/redacted/vnext/model_v2/shadow.jsonl'
KEY = os.path.join(os.environ.get('USERPROFILE', ''), '.ssh', '__KEY_FROM_ENV__')

def _ssh(cmd, timeout=60):
    full = ['ssh', '-o', 'ConnectTimeout=25', '-o', 'BatchMode=yes', '-i', KEY, '__SSH_TARGET_FROM_ENV__', cmd]
    return subprocess.run(full, capture_output=True, text=True, timeout=timeout).stdout.strip()

def pull(n=5):
    'Return dict with latest rows + REAL emission evidence (file mtime + server clock).'
    rows_raw = _ssh('tail -%d %s' % (n, REMOTE)).splitlines()
    meta_raw = _ssh('stat -c %%Y %s; date -u +%%s' % REMOTE)
    lines = [l for l in meta_raw.splitlines() if l.strip()]
    mtime_s, server_now_s = int(lines[0]), int(lines[1])
    rows = [json.loads(l) for l in rows_raw if l.strip()]
    latest = rows[-1] if rows else None
    emit_ms = mtime_s * 1000  # REAL write time - conservative emission evidence (never invented)
    age_s = server_now_s - (latest['t'] if latest else 0)
    return {'rows': rows, 'latest': latest, 'file_mtime_ms': emit_ms, 'server_now_s': server_now_s,
            'latest_age_s': age_s, 'fresh': 0 <= age_s <= 900,
            'schema_ok': bool(latest and 't' in latest and 'score' in latest and latest.get('oof') is False),
            'spec': (latest or {}).get('spec', ''), 'refit_day': (latest or {}).get('refit_day', '')}

def signal_for_engine(pkt):
    'Preserve score semantics: DIRECTION score + Platt p. NOT an executable-net forecast.'
    L = pkt['latest']
    return {'model': 'v2_live_shadow_direction', 'target': 'direction_score', 'horizon_min': 60,
            'score': float(L['score']), 'p_platt': float(L.get('p') or 0),
            'available_ms': pkt['file_mtime_ms'], 'emission_evidence': 'file_mtime (real write time)',
            'validation': 'acc 54.60/AUC 0.5643 h60 fwd; control-CI crosses 0',
            'model_hash': 'spec:' + str(L.get('spec', pkt.get('spec', ''))), 'age_note': 'refit_day ' + str(L.get('refit_day', pkt.get('refit_day', '')))}
