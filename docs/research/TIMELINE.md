# Timeline (registry-generated facts + dates)

| When | Line | Event | Outcome |
|---|---|---|---|
| 2025-11-20 | smart-trader created (GitHub) | production research line begins | — |
| 2025-12-05 | stractued-trade | earliest structured experiments archived | no surviving edge |
| 2026-09-01 | smart-trader @4de0220 | 183 commits: expert router, gates, EXP-004 sealed | lineage head |
| 2026-10-09 | audit | router ablation replay: 0 action flips V0–V4 | router redundant |
| 2026-10-12 | audit | kill-switch fail-closed on feed stall; gates proven protective (C1/C2 −24…−28 bps) | containment worked |
| 2026-10-31 | Genesis V2 (gnx) | fee-corrected paper execution | −28.99 bps avg / 5 trades |
| 2026-11-02 | L2 T1/T2 | preregistered forward eval | REJECTED |
| 2026-11-04 | Genesis V3 | net gate over 10,478 min | 0 BUY; max +4.18 bps |
| 2026-11-05 | Victory Fusion | C1/C2 vs constant | both REJECTED |
| 2026-11-07 | The Gambler P0–P2 | Decimal accounting (3 bugs fixed+tested), unified runtime | released |
| 2026-11-08 | P3 learning | real outcome feedback; challenger loses to constant | promotion GATED |
| 2026-11-08 | P4 frontier | 3 markets; no qualifier | negative |
| 2026-11-08 | P5 maker | frozen spec 2591749e4d1bea4c | prospective, review ≥2026-11-22 |
| 2026-11-08 | Public release | v1.0.0, CI green | this repository |

## Engineering corrections that changed results
Feature/emission causality → per-row evidence; **spread double-count** (97.2→78.4 bps); **fee-base slip**; **8dp quantity truncation** (+1.26 bps bias); **overlapping-label dependence** → day-block stats (~88 effective n, not 10,478); **maker non-identifiability** → bounds not estimates.