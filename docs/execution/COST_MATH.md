# Execution Cost Mathematics

## The verified fixture (offline, reproducible)

```python
from gambler.economics import round_trip
rt = round_trip(1_500_000, 20_400_971_155, 20_438_907_946, 30)  # fee 0.3%/leg
# proceeds 1,488,246.0200701954 TMN   loss 11,753.9799298046 TMN   cost 78.3598661987 bps
```

Assumptions: market buy at ask, market sell at bid (**the spread is crossed exactly once**), fee charged per leg in quote currency, full Decimal precision internally, exchange 8dp quantity rounding only as an explicit layer. **This is an arithmetic fixture with assumed fees — not a claim about any account's fee tier or permanent market conditions.**

Run it: `pytest -q tests/test_gambler.py -k fixture`

## Decomposition (bps)

| Component | Value |
|---|---|
| Spread crossed once (ask-in / bid-out) | 18.58 |
| Fees (30 + 30, quote-currency compounding) | ~59.8 |
| **Total** | **78.36** |

## Historical accounting bugs (now regression tests)

1. **Spread double-count** — an early draft subtracted 2× the quoted spread; one round trip crosses it *once*.
2. **Fee-base slip** — fee applied to the wrong notional produced a phantom 148.5 bps figure.
3. **Quantity truncation** — rounding BTC to 8dp *inside* the calculation biased costs by +1.26 bps; now full precision internally, rounding explicit.

## Why this matters more than accuracy

Best-ever selected signal: **+1.55 bps** gross. Audited taker friction: **66–97 bps**. A model must predict *net movement larger than the rake* — ours never came within a factor of four. See [BENCHMARKS.md](../models/BENCHMARKS.md).