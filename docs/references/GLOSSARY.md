# Glossary

- **Maker / Taker** — a passive limit order (maker) vs an aggressing market order (taker). Takers pay the spread; makers *provide* liquidity (and may earn better fees) but risk not filling.
- **Queue position** — your place in the line of resting orders at a price. Determines who fills first; not observable from snapshots.
- **Markout** — price movement after an execution, e.g. mid(+10 min) / fill − 1. Measures adverse selection.
- **Adverse selection** — the tendency to get filled exactly when the market moves against you.
- **AUC** — probability a random positive scores above a random negative (0.5 = coin flip).
- **Information coefficient (IC)** — correlation between forecast and realized outcome.
- **Purged / embargoed validation** — removing training samples whose labels overlap the test window in time.
- **Walk-forward** — refit on the past, predict the future, roll.
- **Prequential** — predict first, learn after the outcome matures; never test on data you trained on.
- **Day-block CI** — uncertainty computed over days (independent units), not overlapping minutes.
- **Economic expectancy** — mean net profit per trade *after* all costs; the only number that pays bills.