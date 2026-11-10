# Show HN draft (owner submits; primary link = the repo, per HN norms)

**Title:** Show HN: The Gambler Trading Lab — a trading AI that proved it should not trade

**URL:** https://github.com/MajidAsghariTabrizi/the-gambler-trading-lab

**Text (first comment by owner):**
One year of trading research, open-sourced with the negative result as the headline. The system collects its own market data, runs registered (frozen, timer-driven) evaluations, and reconciles its own results from raw ledgers. Best model: 54.6% directional accuracy (AUC 0.5683 out-of-sample) — and −42.53 bps per modeled trade under a frozen cost-aware policy, 0/14 positive days. The repo contains the decimal-exact cost accounting (78.3598661987 bps fixture), the frozen maker-experiment spec, a runnable offline demo, and a full engineering postmortem (ten defects, including two we made in our own audit). The complete study: https://majidasgharitabrizi.github.io/the-gambler-trading-lab/research/from-prediction-to-executable-alpha/

Happy to go deep on: evaluation registration, day-blocked uncertainty, why a constant beats a trained regressor here, maker-fill non-identifiability, or the reconciliation of the 1,110-pair population mismatch.
