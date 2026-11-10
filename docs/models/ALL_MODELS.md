# All Models (generated from registry; statuses are evidence grades)

| ID | Family | Status | Key result / evidence |
|---|---|---|---|
| structured-rule-v0 | rule/indicator | TRAINED_REPORTED_ONLY | archived 2025-12 |
| smart-trader-experts-v0..v4 | 9-expert ensemble + router | TRAINED_VERIFIED | ablation: 0 flips, eff-dim 2.755 |
| uncertainty-gate | calibrated filter | IMPLEMENTED_VERIFIED | 100% protective abstention while C1/C2 negative |
| C1/C2 | net candidates | REJECTED | −24…−28 bps |
| C3-h30 | net candidate | INSUFFICIENT_EVIDENCE | +1.23→−1.01 bps, CI crosses 0 |
| EXP-004 | sealed experiment | REGISTERED_READOUT_20261014 | readout exists (server artifacts); superseded 2026-11-09 |
| M16–M24 / VON / FeatureFactory / HMM / LightGBM / XGBoost / CatBoost | historical generations | TRAINED_REPORTED_ONLY | listed, not re-verified, not ranked |
| genesis-v2-gnx | cost-corrected paper | TRAINED_VERIFIED | −28.99 bps avg |
| genesis-v3 | ridge net-bps | TRAINED_VERIFIED | MAE 28.336; 0 BUY/10,478 |
| vf-c1 / vf-c2 | fusion | REJECTED | worse than constant |
| model-v2 | Huber walk-forward | TRAINED_VERIFIED | 54.60%/0.5643 vs 53.34% control |
| vnext | adaptive experts | TRAINED_VERIFIED | 52.47%/0.5465 |
| p3-challenger | purged ridge | TRAINED_VERIFIED | loses to constant → SHADOW |
| v3-local-reconstruction | 6-col ridge | EXPERIMENTAL | corr −0.08 pinned |
| p4-opportunity-filter | conditional | INSUFFICIENT_EVIDENCE | n=40 |
| p5-maker-bounds | fill-bounds model | IMPLEMENTED_VERIFIED | strict 21.4% / touch 28.6% (n=14)