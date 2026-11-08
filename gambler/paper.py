'"""Paper account lifecycle: Decimal conservation, append-only ledger, idempotent by ts."""'
import json, os
from decimal import Decimal
from gambler.economics import round_trip, EIGHT

class PaperAccount:
    def __init__(self, cash_tmn='15000000', btc='0', ledger_path=None):
        self.cash = Decimal(str(cash_tmn)); self.btc = Decimal(str(btc))
        self.ledger_path = ledger_path
        self._seen_ts = set()
        if ledger_path and os.path.exists(ledger_path):
            for l in open(ledger_path):
                try: self._seen_ts.add(json.loads(l)['ts_utc'])
                except Exception: pass
    def conserve(self):
        assert self.cash >= 0 and self.btc >= 0, 'negative balance forbidden'
    def apply(self, decision_rec, best_bid, best_ask, probe_notional=1500000):
        ts = decision_rec['ts_utc']
        if ts in self._seen_ts: return 'DUPLICATE_IGNORED'  # restart idempotency
        if decision_rec['decision'] == 'BUY' and self.btc == 0:
            notional = min(Decimal(str(probe_notional)), self.cash * Decimal('0.10'))
            rt = round_trip(notional, best_bid, best_ask, 30)
            self.cash -= notional; self.btc += rt['qty_btc']
            out = 'PAPER_BUY'
        elif decision_rec['decision'] == 'SELL' and self.btc > 0:
            rt = round_trip(0, best_bid, best_ask, 30)  # fees only
            proceeds = (self.btc * Decimal(str(best_bid)) * (1 - Decimal('0.003'))).quantize(EIGHT)
            self.cash += proceeds; self.btc = Decimal('0')
            out = 'PAPER_SELL'
        else:
            out = 'NO_ACTION'
        self.conserve()
        if self.ledger_path:
            with open(self.ledger_path, 'a') as f:
                f.write(json.dumps({'ts_utc': ts, 'event': out, 'cash_tmn': str(self.cash), 'btc': str(self.btc)}) + chr(10))
        self._seen_ts.add(ts)
        return out
