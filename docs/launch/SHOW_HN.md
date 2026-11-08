# Show HN (owner to submit personally)

**Title:** Show HN: The Gambler – A trading research system that proves its own signals can't pay the fees

**URL:** https://github.com/MajidAsghariTabrizi/the-gambler-trading-lab

**Talking points (all evidence-backed, owner's voice):**
- Complete pipeline: read-only data → causal features → predictions → cost gate → paper account → outcome maturity → gated learning. 27-test offline suite, deterministic demo, no API keys.
- Best model 54.6% directional accuracy — CI vs 53.34% control crosses zero at day-block level (~88 effective observations, not 10k overlapping minutes).
- Verified cost fixture: 78.3598661987 bps round trip, exact Decimal, regression-pinned. Three historical accounting bugs found, fixed, frozen as tests.
- Every claim carries an evidence grade: VERIFIED / REPRODUCED / REPORTED_ONLY / EXPERIMENTAL / REJECTED.
- The learning loop rejected its own challenger for losing to a constant. Promotion stays gated.
- One preregistered hypothesis remains (maker fills in spread-compression regimes); queue position is provably non-identifiable from our data, so we publish bounds, not estimates.
- Not advice, no profits claimed, live trading impossible by design (no order code exists).
- Why it might interest HN: it's a reference implementation of *scientific honesty* in trading ML — prequential evaluation, purge/embargo, preregistration, negative results kept.