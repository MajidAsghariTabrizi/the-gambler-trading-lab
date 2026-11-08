'"""The Gambler decision engine. Deterministic, replayable, fail-closed."""'
import json, datetime
from decimal import Decimal
from gambler.economics import book_quality, round_trip
from gambler.models import signals_for

BUFFER_BPS = Decimal('10')
RAKE_FEE_BPS = 30

def decide(t_min, best_bid, best_ask, account, signals=None, config=None):
    cfg = config or {}
    sig = signals if signals is not None else signals_for(t_min)
    q = book_quality(best_bid, best_ask, cfg.get('max_spread_bps', 500))
    rt = None
    if q == 'OK':
        rt = round_trip(cfg.get('probe_notional', 1500000), best_bid, best_ask, RAKE_FEE_BPS)
    v3 = next((s for s in sig if s.get('target', 'executable_net_bps_h60') == 'executable_net_bps_h60'), None)
    v2 = next((s for s in sig if s['model'] == 'v2_live_shadow_direction'), None)
    if q != 'OK':
        action, reason = 'NO_TRADE', 'data_quality:' + q
    elif account['btc'] > 0:
        action, reason = 'HOLD', 'position_open_exit_contract_h60_pending'
    elif v3 is None:
        action, reason = 'NO_TRADE', 'no_valid_net_forecast_for_minute'
    elif Decimal(str(v3['score'])) < BUFFER_BPS:
        action, reason = 'NO_TRADE', 'expected_net_below_buffer(+10bps)'
    elif v2 is None or v2['score'] <= 0:
        action, reason = 'NO_TRADE', 'direction_gate_not_agreeing'
    else:
        action, reason = 'BUY', 'meta_gate_satisfied'
    rec = {'ts_utc': datetime.datetime.fromtimestamp(t_min, datetime.timezone.utc).isoformat(),
           'market': 'BTCTMN', 'book_quality': q, 'best_bid': str(best_bid), 'best_ask': str(best_ask),
           'spread_bps_crossed_once': str(rt['spread_bps_crossed_once']) if rt else None,
           'rake_total_bps_if_traded': str(rt['spread_bps_crossed_once'] + rt['fee_bps_total']) if rt else None,
           'signals': sig, 'account': {'cash_tmn': str(account['cash']), 'btc': str(account['btc'])},
           'decision': action, 'reason': reason,
           'fee_assumption': 'public taker 30bps/leg - account tier UNVERIFIED',
           'engine': 'gambler-final/1.0', 'deterministic': True}
    return rec