# DEV Community draft (ready — owner posts via own account)

**Title:** We Built a Trading AI for a Year. Its Best Skill Was Refusing to Trade.

**Canonical:** https://majidasgharitabrizi.github.io/the-gambler-trading-lab/research/from-prediction-to-executable-alpha/

Body sketch (adapt, do not duplicate the paper verbatim):

- Hook: our best model was RIGHT more often than chance — 54.6% vs 53.34% control, registered AUC 0.5683 on 20,185 matured minute-pairs — and its simulated trades LOST 42.53 bps each, 0 positive days out of 14.
- The engineering lessons (the DEV angle): ten defects we found in our own pipeline — spread double-counting, fee-basis errors, quantity-precision at the exchange layer, feature parity drift, a score-lineage mapping error in our own audit, a 1,110-row population mismatch caused by outcome maturity, overlapping-label dependence, maker-fill non-identifiability, a router that added 9 experts and flipped 0 actions, and cross-population metric traps.
- Code walkthrough pointers: the decimal-exact cost fixture (78.3598661987 bps, pinned to 1e-9), the registered evaluator semantics, the bounds-only maker methodology.
- Close: negative results, honestly instrumented, are the reusable part. Repo link + paper link.
- Tags: machinelearning, quanttrading, mlops, python, datascience
