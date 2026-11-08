# Open-Source Benchmarks & Attribution

We studied these projects as engineering benchmarks (October–November 2026). Commits pinned via the GitHub API on 2026-11-08. **We adopted none as dependencies; ideas only.** No endorsement implied.

| Project | Pinned commit | License | Why studied | What we took | What we rejected |
|---|---|---|---|---|---|
| [hftbacktest](https://github.com/nkaz001/hftbacktest) | `5f3ec40b2afb` | MIT | Queue/fill modeling rigor | Conservative fill *bounds* discipline | Rust core; duplicate engine |
| [nautilus_trader](https://github.com/nautechsystems/nautilus_trader) | `77d785c69205` | LGPL-3.0 | Event-driven architecture | Event contract ideas | Full engine (license + duplication) |
| [river](https://github.com/online-ml/river) | `4768de0579f9` | BSD-3-Clause | Prequential evaluation | Predict-before-outcome protocol (implemented natively) | Dependency |
| [qlib](https://github.com/microsoft/qlib) | `543552324638` | MIT | Validation hygiene | Purge/embargo checklist | Framework |
| [freqtrade](https://github.com/freqtrade/freqtrade) | `58d4e710f9bb` | GPL-3.0 | Lookahead-bias tooling | Lookahead-audit mindset | GPL engine |
| [cryptofeed](https://github.com/bmoscon/cryptofeed) | `f3e9096d4606` | custom (NOASSERTION) | Feed normalization | Channel/timestamp conventions | Feed dependency |
| [backtest-guard](https://github.com/AgentJDrew/backtest-guard) | `317cd5a3d560` | MIT | Backtest protection | Cross-check habit | Unproven (0★), unused |

Also: scikit-learn (BSD-3) and numpy (BSD-3) are runtime dependencies; pytest (MIT) for tests. Their licenses are respected.