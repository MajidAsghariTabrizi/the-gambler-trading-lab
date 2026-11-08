# SQLite WAL state store: immutable events + derived state, idempotent, restart-safe.
import sqlite3, os, json, time
DB = os.path.join(os.path.dirname(__file__), '..', 'state', 'gambler.db')
os.makedirs(os.path.dirname(DB), exist_ok=True)
_c = None
def conn():
    global _c
    if _c is None:
        _c = sqlite3.connect(DB, isolation_level=None)
        _c.execute('pragma journal_mode=WAL')
        _c.executescript(open(os.path.join(os.path.dirname(__file__), 'schema.sql')).read())
    return _c

def upsert_event(ev):
    c = conn()
    c.execute('insert or ignore into events values (?,?,?,?,?,?,?,?,?,?,?)',
              (ev['event_id'], ev['source'], ev['market'], ev['source_timestamp'], ev['received_at'],
               ev['available_at'], ev['event_type'], ev['schema_version'], ev['payload_hash'], ev['chronology'],
               json.dumps(ev['payload'], separators=(',', ':'))))
    row = c.execute('select count(*) from events where event_id=?', (ev['event_id'],)).fetchone()
    return row[0] == 1

def latest(event_type):
    c = conn()
    r = c.execute('select payload, received_at, source_timestamp from events where event_type=? order by source_timestamp desc limit 1', (event_type,)).fetchone()
    return ({'payload': json.loads(r[0]), 'received_ms': r[1], 'source_ts_ms': r[2]} if r else None)

def kv_get(k, default=None):
    r = conn().execute('select v from kv where k=?', (k,)).fetchone()
    return json.loads(r[0]) if r else default

def kv_set(k, v):
    conn().execute('insert or replace into kv values (?,?)', (k, json.dumps(v)))

def account_state():
    return kv_get('account', {'cash_tmn': '15000000', 'btc': '0'})

def save_account(a):
    kv_set('account', a)

def heartbeat(name, detail=''):
    conn().execute('insert or replace into heartbeats values (?,?,?)', (name, int(time.time() * 1000), detail))

def events_count():
    return conn().execute('select count(*) from events').fetchone()[0]