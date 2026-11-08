# OutcomeService: h60 maturity tracker for recorded net forecasts.
import json, time, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from unified import state
HORIZON_MS = 3600 * 1000

def record_pending(did, t_ms):
    state.conn().execute('insert or ignore into outcomes values (?,0,NULL)', (did,))

def mature(now_ms=None, y_bps_fn=None):
    'Mark matured outcomes whose decision minute + horizon has passed; y from candles when available.'
    now_ms = now_ms or int(time.time() * 1000)
    rows = state.conn().execute('select decision_id from outcomes where matured=0').fetchall()
    n = 0
    for (did,) in rows:
        ts = did.split('|')[0]
        try:
            t_ms = __import__('datetime').datetime.fromisoformat(ts).timestamp() * 1000
        except Exception:
            continue
        if now_ms >= t_ms + HORIZON_MS:
            y = y_bps_fn(did) if y_bps_fn else None
            state.conn().execute('update outcomes set matured=1, y_bps=? where decision_id=?', (y, did))
            n += 1
    return n