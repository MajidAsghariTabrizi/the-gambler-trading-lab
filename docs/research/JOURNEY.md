# The Research Journey

A serious engineering process, failures included. Dates are UTC; evidence grades in brackets.

## Timeline

| When | Stage | What happened | Status |
|---|---|---|---|
| 2026-10 | Directional prediction | VNEXT control (52.47% / AUC 0.5465); MODEL_V2 Huber walk-forward reached 54.60% / 0.5643 — but day-block CI vs a 53.34% zero-change control crosses zero | VERIFIED (private data) |
| 2026-11-02 | Registered forward trial (L2 T1/T2) | Preregistered evaluation FAILED | REJECTED |
| 2026-11-04 | Genesis V2 | Fee-corrected simulator; 5 paper trades averaged **−28.99 bps** — fees are real | VERIFIED |
| 2026-11-04 | Genesis V3 | Cost-aware gate: h60/h240/h1440 net forecasts all below any executable threshold; **0 BUY in 10,478 decision minutes** (max forecast +4.18 bps) | REPRODUCED (parquet, private) |
| 2026-11-05 | Victory Fusion | Model fusion C1/C2 both *worse* than a constant −60 bps predictor | REJECTED |
| 2026-11-07 | The Gambler P0/P1 | Decimal accounting corrected three times (spread double-count → fee slip → quantity truncation); live read-only prediction consumption proven | REPRODUCED |
| 2026-11-07 | Unified runtime (P2) | One app: events → features → inference → decision → paper → outcomes; 25 tests | REPRODUCED |
| 2026-11-08 | Real learning loop (P3) | 9,616 matured prediction→outcome joins; purged challenger **loses to the constant** (MAE 24.55 vs 23.55) → stays SHADOW | REPRODUCED |
| 2026-11-08 | Edge discovery (P4) | 3-market frontier: BTCTMN bimodal 5.8–37.5 bps; BTCUSDT size-infeasible; USDTTMN ~0.15 bps | VERIFIED (private tape) |
| 2026-11-08 | Maker research (P5) | Frozen preregistered experiment; queue fills NON_IDENTIFIABLE from available data — bounds only | FROZEN |

## Why each major change happened

- **V2→V3:** accuracy alone proved nothing once fees were priced; V3 predicts *executable net bps*, not direction.
- **V3→Gambler:** predictions without a disciplined account and ledger kept producing unauditable claims; the unified runtime made every claim replayable.
- **Standalone→integrated (P5):** execution research lived in throwaway scripts until an audit caught it; it became a service.

## Bugs found and frozen as tests

1. Spread counted twice in round-trip cost (97.2 → corrected once-crossing).
2. Fee applied on wrong base (148.5 → corrected exact).
3. BTC quantity truncated to 8dp *inside* accounting (+1.26 bps bias) → full-precision internal math, explicit exchange-precision layer.

Each is now a pinned regression. [docs/execution/COST_MATH.md](../execution/COST_MATH.md)

## The negative-result curriculum

54.6% direction ≠ alpha. Fusion ≠ improvement. Zero trades ≠ profit. The system's most valuable output is a *justified NO_TRADE*.