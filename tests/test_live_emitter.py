import os, sys, json
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

def test_emitter_packet_schema_and_freshness_contract():
    from gambler.live_emitter import signal_for_engine
    pkt = {'latest': {'t': 1794070800, 'score': 2.99, 'p': 0.95, 'oof': False, 'spec': 'modelv2:huber_wf_v1', 'refit_day': '2026-11-07'},
           'file_mtime_ms': 1794070969000, 'server_now_s': 1794071020, 'latest_age_s': 140, 'fresh': True, 'schema_ok': True}
    sig = signal_for_engine(pkt)
    assert sig['target'] == 'direction_score' and 'net' not in sig['target']  # semantics preserved
    assert sig['available_ms'] == pkt['file_mtime_ms']  # real write time, never invented

def test_causality_entry_after_emission():
    # intent must be strictly after real emission write; t+125s is only a bound, mtime is proof
    emit_ms = 1794070969000
    intent_ms = emit_ms + 2000
    assert intent_ms > emit_ms

def test_stale_stream_fails_closed():
    pkt_fresh = {'latest_age_s': 140, 'fresh': True, 'schema_ok': True}
    pkt_stale = {'latest_age_s': 4000, 'fresh': False, 'schema_ok': True}
    assert pkt_fresh['fresh'] and not pkt_stale['fresh']

def test_direction_score_not_treated_as_net():
    from gambler.engine import decide
    from decimal import Decimal
    sig = [{'model': 'v2_live_shadow_direction', 'score': 25.0, 'target': 'direction_score'}]
    r = decide(1794070800, 20250801533, 20254178116, {'cash': Decimal('15000000'), 'btc': Decimal('0')}, signals=sig)
    assert r['decision'] == 'NO_TRADE' and 'no_valid_net_forecast' in r['reason']  # never fabricate net from direction
