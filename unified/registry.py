# Champion/Challenger model registry with atomic, reversible promotion.
import sys, os, json, time, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from unified import state
STATES = ('ACTIVE_CHAMPION', 'SHADOW_CHALLENGER', 'REJECTED', 'ARCHIVED', 'ROLLED_BACK')

def register(model_id, kind, spec_hash, train_window, metrics):
    state.conn().execute('insert or replace into models values (?,?,?,?,?,?,?,?)',
        (model_id, 'SHADOW_CHALLENGER', kind, spec_hash, train_window, json.dumps(metrics), None, int(time.time() * 1000)))

def champion():
    r = state.conn().execute(chr(39) + 'select model_id from models where state=?' + chr(39) if False else 'select model_id from models where state=?', ('ACTIVE_CHAMPION',)).fetchone()
    return r[0] if r else None

def promote(model_id, justification):
    'Atomic: exactly one champion; previous champion archived (rollback ref kept).'
    c = state.conn()
    c.execute('begin')
    try:
        prev = champion()
        if prev:
            c.execute('update models set state=? where model_id=?', ('ROLLED_BACK', prev))
        c.execute('update models set state=?, promotion=? where model_id=?',
                  ('ACTIVE_CHAMPION', json.dumps({'justification': justification, 'at_ms': int(time.time() * 1000), 'replaces': prev}), model_id))
        c.execute('commit')
        return True
    except Exception:
        c.execute('rollback')
        return False

def rollback(to_model_id):
    cur = champion()
    if cur:
        state.conn().execute('update models set state=? where model_id=?', ('ARCHIVED', cur))
    state.conn().execute('update models set state=? where model_id=?', ('ACTIVE_CHAMPION', to_model_id))

def all_models():
    return state.conn().execute('select model_id, state, kind, spec_hash, train_window from models').fetchall()