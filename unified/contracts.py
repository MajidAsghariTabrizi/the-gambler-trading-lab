# Canonical versioned event contract for the unified runtime.
import json, hashlib, datetime, uuid
SCHEMA_VERSION = 'gambler-event/1'

def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def make_event(source, market, source_ts_ms, received_ms, event_type, payload, chronology='VERIFIED'):
    'received_ms is REAL local receipt time recorded when it occurs; legacy data uses UNVERIFIED.'
    body = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    return {'event_id': hashlib.sha256((source + market + str(source_ts_ms) + event_type + body).encode()).hexdigest()[:24],
            'source': source, 'market': market, 'source_timestamp': source_ts_ms, 'received_at': received_ms,
            'available_at': received_ms, 'event_type': event_type, 'schema_version': SCHEMA_VERSION,
            'payload_hash': hashlib.sha256(body.encode()).hexdigest()[:16], 'chronology': chronology, 'payload': payload}