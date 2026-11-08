'"""Operational dashboard render: health, models, economics, research status."""'
def render(rec, account_line, extra=None):
    L = []
    L.append('=== THE GAMBLER - OPERATIONAL DASHBOARD ===')
    L.append('[SYSTEM] engine %s | deterministic=%s' % (rec.get('engine'), rec.get('deterministic')))
    L.append('[DATA] book_quality=%s bid=%s ask=%s' % (rec['book_quality'], rec['best_bid'], rec['best_ask']))
    L.append('[COST] spread_once=%s bps | rake_if_traded=%s bps | fees: %s' % (rec.get('spread_bps_crossed_once'), rec.get('rake_total_bps_if_traded'), rec.get('fee_assumption')))
    L.append('[MODELS] ' + ('; '.join('%s=%.3f (%s)' % (s['model'], s['score'], s['validation'][:24]) for s in rec['signals']) or 'none for minute'))
    L.append('[ACCOUNT] ' + account_line)
    L.append('[DECISION] %s - %s' % (rec['decision'], rec['reason']))
    L.append('[RESEARCH] frozen=NO_TRADE reference | reopening: spread<2bps 30d OR maker<10bps | gates: 30d/200pos/+10bps/97.5%%LCB')
    for e in (extra or []): L.append(e)
    return chr(10).join(L)
