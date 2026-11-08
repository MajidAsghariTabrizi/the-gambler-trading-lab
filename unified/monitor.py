# MonitoringService + dashboard: reads ONLY the shared state store.
import json, time, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from unified import state, registry

def dashboard():
    c = state.conn()
    last_md = state.latest('MARKET_V2_BOOK')
    last_dec = c.execute('select record from decisions order by ts_ms desc limit 1').fetchone()
    dec = json.loads(last_dec[0]) if last_dec else None
    acct = state.account_state()
    hb = dict(c.execute('select name, ms from heartbeats').fetchall())
    champ = registry.champion()
    models = registry.all_models()
    L = ['=== ONE GAMBLER - UNIFIED DASHBOARD ===']
    L.append('[RUNNING] heartbeats: ' + json.dumps({k: int((time.time() * 1000 - v) / 1000) for k, v in hb.items()}) + 's ago')
    if last_md:
        p = last_md['payload']
        sp = (p['ask'] - p['bid']) / ((p['ask'] + p['bid']) / 2) * 1e4
        L.append('[DATA] bid %g ask %g spread %.2f bps | rake if traded %.2f bps (fees 60 unverified)' % (p['bid'], p['ask'], sp, sp + 60))
        L.append('[MODEL] V2 direction %.3f (server-live) | net forecast %s' % (p.get('v2_score') or 0, 'see decision'))
    L.append('[REGISTRY] champion=%s | models=%d | promotion GATED (no preregistered eval)' % (champ, len(models)))
    L.append('[ACCOUNT] cash %s TMN btc %s' % (acct['cash_tmn'], acct['btc']))
    if dec:
        L.append('[DECISION] %s - %s' % (dec['decision'], dec['reason']))
    exr = state.latest('EXEC_RESEARCH')
    if exr:
        d = exr['payload'].get('spread_distribution', {})
        fb = exr['payload'].get('fill_bounds', {}).get('strict', {})
        L.append('[EXEC-RESEARCH] spread median %s bps | <6bps frac %s | episodes %s | strict fill rate %s | queue NON_IDENTIFIABLE | spec %s' % (d.get('median'), d.get('frac_below_6bps'), exr['payload'].get('compression_episodes', {}).get('episodes'), fb.get('fill_rate'), exr['payload'].get('spec_hash')))
    L.append('[ECONOMY] edge NOT_ESTABLISHED | live trading OFF')
    return chr(10).join(L)