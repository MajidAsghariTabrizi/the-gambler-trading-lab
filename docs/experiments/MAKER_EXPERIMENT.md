# The Frozen Maker Experiment (EXPERIMENT_MAKER_BTCTMN_v1)

**Status: FROZEN / prospective window opened 2026-11-08. Earliest review: 2026-11-22. Spec hash (sha16): `2591749e4d1bea4c`** — the immutable spec is [here](EXPERIMENT_MAKER_BTCTMN_v1.json) (published verbatim).

## Hypothesis (k=1)
Passive maker entry during liquidity-compression regimes improves net execution economics after missed fills, adverse selection, fees and exits.

## Frozen rules (no reselection permitted)
- Market BTCTMN; ticket 1,500,000 TMN-equivalent; horizon 60 min.
- Entry eligibility: spread < 6 bps sustained ≥ 60 s, book not locked/crossed, data fresh ≤ 5 s.
- Fill semantics: **queue position is NON_IDENTIFIABLE** from trade tape + 1 s snapshots. We publish bounds only:
  - *strict-through lower bound* — a sell print strictly below the limit;
  - *touch upper bound* — any sell print at or below the limit.
- Fees: scenarios (taker 30 bps/leg; maker 0 or 30) — account tier UNVERIFIED.
- Promotion bar: day-block 95% LCB **> +10 bps advantage in BOTH fill scenarios**, ≥100 entries / 30 episodes / 10 days.

## Development-window observations (NOT evidence of profitability)
Spread distribution (n=412 matched 1 s pairs, one day): median 10.4 bps, 5th pct 1.3, 75th pct 34.6; below-6-bps fraction 43.2%. Fill bounds on n=14 attempts: strict 21.4% / touch 28.6%, mean +10-min markout +23.5 / +24.3 bps. **These are bounds from one short window — not estimates, not fills, not profit.**

## What would falsify it
At review, if strict-through fill-rate × markout does not clear fees with sufficient sample → the maker line closes permanently.