# Execution Evolution

1. **Assumed-cost era** — constant fee guess; produced phantom "edges."
2. **Quoted-spread era** — first real book pricing; caught the **spread double-count**.
3. **Decimal-exact era (current)** — fixture-pinned: one crossing, fees per leg compounded in quote currency, full-precision quantities, explicit 8dp exchange layer → **78.3598661987 bps** verified.
4. **Depth-aware era** — VWAP walks on real books: BTCUSDT cannot fill 1.5M (1.43M unfilled); USDTTMN ~0.15 bps deep.
5. **Fill-uncertainty era (P5)** — maker entries as *bounds* (strict-through lower / touch upper); queue provably non-identifiable; one frozen prospective experiment.

See [COST_MATH.md](COST_MATH.md) for the executable fixture and the three historical bugs.