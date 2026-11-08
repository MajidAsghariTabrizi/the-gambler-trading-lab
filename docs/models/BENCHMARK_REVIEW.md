# Public benchmark review

## Which is best?

There is no defensible overall winning trading strategy in the available evidence.

| Matched population | Metric | Best observed | Interpretation |
|---|---|---|---|
| Direction h60 | Accuracy, higher is better | MODEL_V2, 54.60% | 1.26 percentage points above the 53.34% control; day-block confidence interval crosses zero; roughly 88 effective observations. |
| Victory Fusion evaluation | Net-bps MAE, lower is better | Constant −60, 26.39 bps | C1 is 26.70 and C2 is 37.47; neither improves on the control. |
| P3 validation | Net-bps MAE, lower is better | Constant −60, 23.55 bps | Challenger is 24.55; promotion stays gated. |

These are previously published private-data summaries. The public repository does not contain the raw populations needed to independently re-estimate those scores or their uncertainty. Genesis V3's MAE is excluded from these rankings because its rows/horizon mix differs.

## What can be benchmarked independently?

`python scripts/benchmark_public.py` ranks only within those three populations, verifies the public 78.3598661987 bps fixture using an independent proceeds conservation identity, and measures 2,000 warmed cost-engine calls. Timing is machine-specific arithmetic performance, not model inference, trading performance, or a comparison against other platforms. No model was retrained or selected on new private data.

## Storefront design benchmark

The design comparison is qualitative, not a measured usability or speed ranking:

- [TradingView's chart/table exploration](https://www.tradingview.com/support/solutions/43000724233-chart-view-mode/) informed a clear route between visual comparisons and a searchable registry.
- [QuantConnect's backtest workflow](https://www.quantconnect.com/docs/v2/cloud-platform/backtesting/getting-started) informed a route from research evidence to reproducible local execution.
- The Gambler's specific contribution is prominent evidence status, failed experiments, explicit population boundaries, and the distinction between accuracy and executable expectancy.

No claim of being the world's best platform, fastest system, or most profitable strategy follows from this comparison.
