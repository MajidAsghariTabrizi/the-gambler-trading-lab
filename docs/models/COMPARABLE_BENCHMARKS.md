# Comparable Benchmarks — matched samples only

**Group 1 — direction h60, same population (private):** MODEL_V2 54.60% · zero-change control 53.34% · VNEXT 52.47%. Day-block CI on V2-vs-control crosses 0; ~88 effective observations. *Horizons and labels verified identical before this comparison.*

**Group 2 — net-bps MAE, VF evaluation rows:** constant −60 → 26.39 · VF C1 26.70 · VF C2 37.47.

**Group 3 — net-bps MAE, P3 validation rows (different population from Group 2 — never pooled):** constant −60 → 23.55 · P3 challenger 24.55.

**Not comparable across groups:** V3 MAE 28.34 (different rows/horizon mix) is reported for the record, not ranked against Groups 2–3.

Cross-group ranking without population labels is the single most common benchmark lie in trading ML; every table here states its population.