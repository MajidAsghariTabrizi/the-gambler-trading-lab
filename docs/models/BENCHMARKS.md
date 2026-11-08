# Model Benchmarks — every model, honestly graded

Evaluation populations differ; never compare across rows as if identical.
"Constant" = predict −60 bps net (approximate friction floor).

| Model | Target | Result | vs Baseline | Status |
|---|---|---|---|---|
| Zero-change control | direction | 53.34% | — | VERIFIED (private data) |
| VNEXT | direction | 52.47% / AUC 0.5465 | below control | VERIFIED (private data) |
| **MODEL_V2** (Huber WF, daily refit) | direction h60 | **54.60% / AUC 0.5643** | day-block CI [−0.033, +0.072] crosses 0; ~88 effective independent positions | VERIFIED (private data); live emitter |
| L2 T1/T2 | registered forward | FAILED | — | REJECTED (preregistered) |
| Genesis V3 (audited ridge) | net bps h60 | MAE 28.336; max forecast **+4.18 bps**; 0 BUY / 10,478 | never cleared +10 bps buffer | REPRODUCED (private parquet) |
| Victory Fusion C1 | net bps | MAE 26.70 / IC −0.017 | loses to constant (26.39) | REJECTED |
| Victory Fusion C2 | net bps | MAE 37.47 / IC −0.018 | loses to constant | REJECTED |
| Constant −60 bps | net bps | MAE 26.39 (VF rows) / 23.55 (P3 rows) | **best on both populations** | REPRODUCED |
| P3 challenger (purged ridge) | net bps | MAE 24.546 / IC −0.0158 (2 val days, eff. n≈34) | **loses to constant** | REPRODUCED (private parquet) |
| P3 parity check | — | local 6-col reconstruction vs audited V3: corr **−0.08** | not the audited model | EXPERIMENTAL (test-pinned) |

**Reading this correctly:** the best *prediction* was V2 at 54.6% (not distinguishable from control). The best *net-forecast* is a constant. No model produced a single trade-clearing forecast in 10,478 minutes. Prediction was never the binding constraint — execution cost was.