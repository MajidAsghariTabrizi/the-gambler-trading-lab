# DecisionService: reuses gambler.engine.decide - ONE cost engine, ONE decision semantics.
import os, sys, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from decimal import Decimal
from gambler.engine import decide as base_decide
from unified import state

def decide_and_record(pkt, net_forecast):
    bid, ask = pkt['book']['bid'], pkt['book']['ask']
    sigs = [{'model': 'v2_live_shadow_direction', 'target': 'direction_score', 'horizon_min': 60,
             'score': pkt['v2_row']['score'], 'available_ms': pkt['emit_write_ms'],
             'model_hash': 'spec:' + pkt['v2_row'].get('spec', ''), 'validation': 'acc 54.60/AUC 0.5643; CI crosses 0'}]
    if net_forecast:
        sigs.append({'model': 'v3_local_net', 'target': 'executable_net_bps_h60', 'horizon_min': 60,
                     'score': net_forecast['net_bps'], 'available_ms': net_forecast['emitted_ms'],
                     'model_hash': net_forecast['spec_hash'], 'validation': 'DEV-ONLY not economically validated'})
    acct = state.account_state()
    rec = base_decide(pkt['v2_row']['t'], bid, ask, {'cash': Decimal(str(acct['cash_tmn'])), 'btc': Decimal(str(acct['btc']))}, signals=sigs)
    rec['net_forecast'] = net_forecast
    rec['causality'] = {'emission_write_ms': pkt['emit_write_ms'], 'intent_ms': int(time.time() * 1000)}
    rec['causality']['entry_after_emission'] = rec['causality']['intent_ms'] > pkt['emit_write_ms']
    did = rec['ts_utc'] + '|' + (net_forecast['spec_hash'] if net_forecast else 'none')
    state.conn().execute('insert or ignore into decisions values (?,?,?,?,?,?)',
        (did, int(time.time() * 1000), rec['decision'], rec['reason'], (net_forecast or {}).get('model_id'), json.dumps(rec)))
    state.heartbeat('decision', rec['decision'] + ' ' + rec['reason'][:40])
    return did, rec