'"""Live read-only paper decision cycle: emitter -> validation -> cost engine -> decision -> ledger."""'
import json, os, sys, datetime
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
from gambler import live_emitter as E
from gambler.runner import fetch_book
from gambler.engine import decide
from gambler.paper import PaperAccount

LEDGER = os.path.join(os.path.dirname(__file__), '..', 'evidence', 'PAPER_DECISION_LEDGER.jsonl')

def cycle():
    pkt = E.pull(n=5)
    if not pkt['fresh'] or not pkt['schema_ok']:
        decision, reason = 'NO_TRADE', 'PREDICTION_STREAM_%s' % ('STALE' if not pkt['fresh'] else 'SCHEMA_INVALID')
        book = (None, None)
    else:
        book = fetch_book()
        sig = [E.signal_for_engine(pkt)]
        ac = PaperAccount(ledger_path=LEDGER)
        # decision minute = latest prediction minute; its emission evidence = file mtime
        rec = decide(pkt['latest']['t'], book[0], book[1], {'cash': ac.cash, 'btc': ac.btc}, signals=sig)
        # causality proof: order intent (now+latency) must be AFTER real emission write time
        now_ms = int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
        rec['causality'] = {'emission_write_ms': pkt['file_mtime_ms'], 'intent_ms': now_ms,
                            'entry_after_emission': now_ms > pkt['file_mtime_ms'],
                            'book_ts_source': 'live fetch at intent', 'prediction_age_s': pkt['latest_age_s']}
        ac.apply(rec, book[0], book[1])
        with open(LEDGER, 'a') as f:
            f.write(json.dumps(rec, separators=(',', ':')) + chr(10))
        return rec
    fallback = {'ts_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'decision': decision, 'reason': reason,
                'server_now_s': pkt['server_now_s'], 'latest_age_s': pkt['latest_age_s']}
    with open(LEDGER, 'a') as f:
        f.write(json.dumps(fallback, separators=(',', ':')) + chr(10))
    return fallback

if __name__ == '__main__':
    print(json.dumps(cycle(), indent=1)[:1200])
