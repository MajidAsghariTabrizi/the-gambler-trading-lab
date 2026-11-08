create table if not exists events (event_id text primary key, source text, market text, source_timestamp integer,
 received_at integer, available_at integer, event_type text, schema_version text, payload_hash text, chronology text, payload text);
create index if not exists ev_type_ts on events(event_type, source_timestamp);
create table if not exists kv (k text primary key, v text);
create table if not exists heartbeats (name text primary key, ms integer, detail text);
create table if not exists models (model_id text primary key, state text, kind text, spec_hash text, train_window text,
 metrics text, promotion text, created_ms integer);
create table if not exists decisions (decision_id text primary key, ts_ms integer, decision text, reason text,
 model_id text, record text);
create table if not exists outcomes (decision_id text, matured integer, y_bps real, primary key (decision_id));
