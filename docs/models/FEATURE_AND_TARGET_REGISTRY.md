# Feature & Target Registry

**Targets:** direction h60 (sign) · executable_net_bps_h60 (net of spread-once + fees at decision-time book) · triple-barrier labels (smart-trader era).
**Feature families:** causal returns (1–300 s) · realized vol · L2 spread/imbalance/mid-offset/age · trade-flow/micro aggregates · V2 direction prior.
**Invariants (test-enforced):** every feature computable from data available *at* emission time; per-row emission evidence; label maturity ≥ horizon + 71-min purge; overlap handled by day-block statistics.
**Registry hashes:** V3 parquet sha16 `9366bd85ad487cdc` (sealed, private); local spec `19ce72e56f69679e`.