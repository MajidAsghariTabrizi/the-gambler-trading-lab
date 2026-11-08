# Data and Event Contract

Every event persisted by the runtime carries: event_id (deterministic hash), source, market, source timestamp (exchange), received-at (local receipt), available-at, event type, schema version gambler-event/1, payload hash, and a chronology verdict (VERIFIED or UNVERIFIED).

Rules (test-enforced):
1. Never construct historical emission times from file mtimes alone.
2. Never use data before it became available; fail closed on staleness (over 5 s), locked or crossed books, or missing models.
3. Labels mature at horizon plus purge (h60 + 71 min) before joining predictions.
4. Protected evaluation windows are never read for selection.

Private provenance: raw tape and depth schemas are published; raw rows are not redistributable (see REPRODUCIBILITY.md).
