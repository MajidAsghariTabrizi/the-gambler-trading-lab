'"""Decimal-exact execution economics. Spread crossed ONCE; fees per leg once; unit guards."""'
from decimal import Decimal, ROUND_DOWN, getcontext
getcontext().prec = 28
EIGHT = Decimal('0.00000001')

def validate_price_tmn(p):
    d = Decimal(str(p))
    if not (Decimal('1e9') < d < Decimal('1e11')):
        raise ValueError('BTCTMN price outside TMN/BTC unit range: %s' % d)
    return d

def book_quality(best_bid, best_ask, max_spread_bps=500):
    bb, ba = Decimal(str(best_bid)), Decimal(str(best_ask))
    if bb <= 0 or ba <= 0: return 'INVALID_PRICES'
    if ba < bb: return 'CROSSED'
    if ba == bb: return 'LOCKED_ZERO_SPREAD'
    mid = (ba + bb) / 2
    if (ba - bb) / mid * 10000 > max_spread_bps: return 'WIDE_SPREAD'
    return 'OK'

def round_trip(notional_tmn, best_bid, best_ask, taker_fee_bps, fee_in_quote=True):
    N = Decimal(str(notional_tmn)); bb = validate_price_tmn(best_bid); ba = validate_price_tmn(best_ask)
    f = Decimal(str(taker_fee_bps)) / 10000
    if fee_in_quote:
        qty = (N * (1 - f)) / ba                    # FULL precision: no exchange quantize here
        gross = qty * bb
        proceeds = gross * (1 - f)
        fees = N - qty * ba + gross - proceeds
    else:
        qty = N / ba
        qty_out = qty * (1 - f)
        proceeds = qty_out * bb
        fees = (qty - qty_out) * bb
    net = proceeds - N
    mid = (ba + bb) / 2
    return {'notional_tmn': N, 'qty_btc': qty if fee_in_quote else qty_out, 'proceeds_tmn': proceeds,
            'fees_tmn': fees.quantize(EIGHT), 'net_tmn': net.quantize(EIGHT),
            'net_bps': net / N * 10000, 'spread_bps_crossed_once': (ba - bb) / mid * 10000,
            'fee_bps_total': Decimal(str(taker_fee_bps)) * 2,
            'convention': 'fee_in_quote' if fee_in_quote else 'fee_in_base',
            'qty_precision': 'full-internal (exchange 8dp layer available via exchange_qty)'}

def net_from_vwap_gross(gross_bps, taker_fee_bps):
    'VWAP gross already includes spread+depth. Fees applied ONCE on top.'
    return Decimal(str(gross_bps)) - Decimal(str(taker_fee_bps)) * 2
def exchange_qty(qty_btc):
    'OPTIONAL explicit exchange-precision layer: 8dp ROUND_DOWN, never applied silently.'
    return Decimal(str(qty_btc)).quantize(EIGHT, ROUND_DOWN)
