# LinkedIn draft (ready — owner posts personally)

One year ago I set out to build a trading AI. Last week its registered evaluation delivered the verdict: **no profitable edge** — and that result is the most valuable thing the system ever produced.

Three numbers tell the story:
1. 54.6% directional accuracy vs a 53.34% control. Real, modest, and — as the confidence interval admitted — not proven.
2. AUC 0.5683 on 20,185 registered out-of-sample pairs. Genuinely above chance.
3. −42.53 bps per modeled trade, 0 positive days out of 14, under a frozen taker policy with row-specific realized costs. Every path from signal to profit ran through 66–97 bps of friction.

What I take into every AI product now:
- A constant is a model. Beat the right baseline or beat nothing.
- Register the test before the data exists. Our verdict ran without human intervention and said FAIL — that is the only reason I trust the positive parts.
- Costs are the strategy. Accuracy without a cost model is entertainment.
- Negative results, fully instrumented, are publishable engineering.

The full study — every number reconciled from raw ledgers, every failure documented:
https://majidasgharitabrizi.github.io/the-gambler-trading-lab/research/from-prediction-to-executable-alpha/

Open source: https://github.com/MajidAsghariTabrizi/the-gambler-trading-lab
