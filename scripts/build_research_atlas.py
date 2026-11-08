# Build the Research Atlas registry from verified lineage evidence.
# Single source of truth: research_registry/*.json; docs and figures generate FROM these.
import json, os, datetime
R = os.path.join(os.path.dirname(__file__), '..', 'research_registry')
os.makedirs(R, exist_ok=True)
now = '2026-11-08'
models = [
 {'id': 'structured-rule-v0', 'family': 'rule/indicator', 'project': 'stractued-trade', 'repo': 'local:stractued-trade@abd3330 (2025-12)', 'status': 'TRAINED_REPORTED_ONLY', 'target': 'direction', 'note': 'earliest structured experiments; artifacts not re-verified', 'public_ref': None},
 {'id': 'smart-trader-experts-v0..v4', 'family': 'expert ensemble + router (9 experts incl. huber-direction triples)', 'project': 'smart-trader', 'repo': 'github:MajidAsghariTabrizi/smart-trader@4de0220 (183 commits, 2025-11..2026-09)', 'status': 'TRAINED_VERIFIED', 'evidence': 'router ablation Oct-9 replay: 0 action flips V0-V4; effective dim 2.755; audit_20261012/expert_router_ablation.json', 'target': 'direction + net', 'note': 'router redundancy proven; no incremental OOS value'},
 {'id': 'uncertainty-gate-aleatoric', 'family': 'calibrated uncertainty gate', 'project': 'smart-trader', 'status': 'IMPLEMENTED_VERIFIED', 'evidence': 'gate attribution: rejects 100 pct of minutes (aleatoric saturation 0.884-1.0); prevented measured C1/C2 losses', 'target': 'trade filter'},
 {'id': 'C1/C2-net', 'family': 'net-expectancy candidates', 'project': 'smart-trader', 'status': 'REJECTED', 'evidence': 'net -24..-28 bps/trade verified twice', 'target': 'net bps'},
 {'id': 'C3-h30', 'family': 'net-expectancy candidate', 'project': 'smart-trader', 'status': 'INSUFFICIENT_EVIDENCE', 'evidence': '+1.23 then -1.01 bps, CI crosses 0 both times', 'target': 'net bps'},
 {'id': 'EXP-004', 'family': 'preregistered sealed experiment', 'project': 'smart-trader', 'status': 'REGISTERED_SEALED', 'evidence': 'registry REGISTERED + RUN CONTINUE_SHADOW only; readout gate-gated', 'target': 'shadow eval'},
 {'id': 'M16..M24/VON/FeatureFactory/HMM/boosting', 'family': 'historical smart-trader generations', 'status': 'TRAINED_REPORTED_ONLY', 'note': 'referenced across smart-trader history (M21/M22 LightGBM, M23 magnitude, M24 Huber multi-horizon, VON ACCEPT/ABSTAIN); artifacts not independently re-verified this atlas - listed for completeness, not ranked'},
 {'id': 'genesis-v2-gnx', 'family': 'cost-corrected paper simulator', 'project': 'genesis_next_gnx_20261031a', 'status': 'TRAINED_VERIFIED', 'evidence': '5 paper trades avg -28.99 bps (fees are real)', 'target': 'paper execution'},
 {'id': 'genesis-v3', 'family': 'ridge on causal features, net-bps target', 'project': 'genesis_v3_gnxv3_20261104b@private', 'status': 'TRAINED_VERIFIED', 'evidence': 'MAE 28.336; max forecast +4.18 bps; 0 BUY / 10,478 min', 'target': 'executable_net_bps_h60'},
 {'id': 'vf-c1', 'family': 'Victory Fusion C1', 'project': 'trader_vf@9f08f36', 'status': 'REJECTED', 'evidence': 'MAE 26.70 / IC -0.017 vs constant 26.39'},
 {'id': 'vf-c2', 'family': 'Victory Fusion C2', 'project': 'trader_vf@9f08f36', 'status': 'REJECTED', 'evidence': 'MAE 37.47 / IC -0.018'},
 {'id': 'model-v2', 'family': 'Huber walk-forward direction', 'project': 'smart-trader lineage -> Gambler live emitter', 'status': 'TRAINED_VERIFIED', 'evidence': '54.60 pct / AUC 0.5643 vs zero-change control 53.34 pct; day-block CI crosses 0; ~88 effective positions', 'target': 'direction h60', 'public': 'metrics VERIFIED on private data'},
 {'id': 'vnext', 'family': 'adaptive experts', 'project': 'pre-Gambler', 'status': 'TRAINED_VERIFIED', 'evidence': '52.47 pct / 0.5465 below control'},
 {'id': 'p3-challenger', 'family': 'purged ridge challenger', 'project': 'the_gambler_final@0752b2c..a432c0a', 'status': 'TRAINED_VERIFIED', 'evidence': 'MAE 24.546 / IC -0.0158 vs constant 23.546 -> SHADOW, promotion GATED'},
 {'id': 'v3-local-reconstruction', 'family': '6-col Ridge refit', 'project': 'the_gambler_final', 'status': 'EXPERIMENTAL', 'evidence': 'corr -0.08 vs audited V3 (test-pinned)'},
 {'id': 'p4-opportunity-filter', 'family': 'execution-aware conditional', 'project': 'the_gambler_final@b7bb255', 'status': 'INSUFFICIENT_EVIDENCE', 'evidence': 'n=40 admissible minutes/9 days'},
 {'id': 'p5-maker-bounds', 'family': 'passive fill bounds model', 'project': 'the_gambler_final@d1642ad', 'status': 'IMPLEMENTED_VERIFIED', 'evidence': 'strict 21.4 pct / touch 28.6 pct on n=14 attempts; queue NON_IDENTIFIABLE'}]
json.dump(models, open(os.path.join(R, 'models.json'), 'w'), indent=1)
experiments = [
 {'id': 'L2-T1/T2', 'when': '2026-11-02', 'status': 'REJECTED', 'what': 'preregistered forward eval of L2 features', 'why_failed': 'registered fail; protected outcomes never reused for tuning'},
 {'id': 'GENESIS-V2-paper', 'when': '2026-11-03', 'status': 'COMPLETED_NEGATIVE', 'what': 'fee-corrected paper execution', 'result': '-28.99 bps avg over 5 trades'},
 {'id': 'GENESIS-V3-gate', 'when': '2026-11-04', 'status': 'COMPLETED_NEGATIVE', 'what': 'net-forecast gate over 10,478 min', 'result': '0 BUY; max +4.18 bps < +10 buffer'},
 {'id': 'VF-fusion', 'when': '2026-11-05', 'status': 'REJECTED', 'what': 'C1/C2 fusion', 'result': 'both worse than constant'},
 {'id': 'P3-learning', 'when': '2026-11-08', 'status': 'COMPLETED', 'what': 'real outcome-feedback loop + purged challenger', 'result': 'challenger loses to constant; promotion gated'},
 {'id': 'P4-frontier', 'when': '2026-11-08', 'status': 'COMPLETED_NEGATIVE', 'what': '3-market opportunity frontier', 'result': 'no market qualifies; BTCUSDT size-infeasible; USDTTMN FX-leg only'},
 {'id': 'P5-maker', 'when': '2026-11-08', 'status': 'FROZEN_PROSPECTIVE', 'what': 'maker execution economics, spec 2591749e4d1bea4c', 'earliest_review': '2026-11-22'},
 {'id': 'EXP-004', 'when': '2026-10', 'status': 'SEALED', 'what': 'smart-trader preregistered shadow experiment', 'note': 'readout never computed; remains sealed by protocol'}]
json.dump(experiments, open(os.path.join(R, 'experiments.json'), 'w'), indent=1)
repos = [
 {'url': 'https://github.com/MajidAsghariTabrizi/smart-trader', 'role': 'FIRST_PARTY', 'created': '2025-11-20', 'local_head': '4de0220', 'commits': 183, 'scope': 'production prediction plane, expert router, gates, sealed EXP-004'},
 {'url': 'https://github.com/MajidAsghariTabrizi/the-gambler-trading-lab', 'role': 'FIRST_PARTY_CURRENT', 'scope': 'canonical public research platform'},
 {'url': 'https://github.com/MajidAsghariTabrizi/anti-gravity-phoenix-v4', 'role': 'FIRST_PARTY_SEPARATE_TRACK', 'created': '2026-07-08', 'scope': 'Arbitrum/DeFi liquidation+arb research; deliberately NOT merged with Wallex spot evaluations'},
 {'name': 'local:stractued-trade@abd3330', 'role': 'FIRST_PARTY_ARCHIVED', 'scope': 'earliest structured experiments (2025-12)'},
 {'name': 'local:smart-trader-stg@882daa3', 'role': 'FIRST_PARTY_ARCHIVED', 'scope': 'staging line (172 commits)'},
 {'name': 'local:research/genesis_next_gnx_20261031a', 'role': 'FIRST_PARTY_RESEARCH', 'scope': 'Genesis V2 cost-corrected simulator'},
 {'name': 'local:research/genesis_v3_gnxv3_20261104b', 'role': 'FIRST_PARTY_RESEARCH_PRIVATE', 'scope': 'V3 training artifacts (sealed parquet)'},
 {'name': 'local:research/trader_vf@9f08f36', 'role': 'FIRST_PARTY_RESEARCH', 'scope': 'Victory Fusion'},
 {'name': 'local:research/the_gambler_final@7d4f1ea', 'role': 'FIRST_PARTY_CANONICAL_PRIVATE', 'scope': 'P0-P5, release package'}]
json.dump(repos, open(os.path.join(R, 'repositories.json'), 'w'), indent=1)
evidence = {'accounting_fixture': 'REPRODUCED offline (78.3598661987 bps)', 'v2_metrics': 'VERIFIED private', 'v3_vf_p3_metrics': 'VERIFIED private parquet', 'router_ablation': 'VERIFIED private audit replay', 'gate_attribution': 'VERIFIED private audit', 'p5_bounds': 'VERIFIED private tape', 'restricted': ['raw trade tape', 'depth archives', 'parquet training rows', 'VPS identity']}
json.dump(evidence, open(os.path.join(R, 'evidence_manifest.json'), 'w'), indent=1)
print('registry files', sorted(os.listdir(R)))