# Three short research-result posts

## Post 1 — The 54.6% that wasn't
"Our best trading model hit 54.6% directional accuracy. A zero-change control scored 53.3% on identical data. Day-blocked CI: crosses zero. Lesson: 10,000 overlapping minutes ≠ 10,000 observations; effective n ≈ 88. Accuracy claims without block-level uncertainty are marketing. https://github.com/MajidAsghariTabrizi/the-gambler-trading-lab"

## Post 2 — 78.36 basis points
"Round trip: cross the spread once, pay two fee legs, compound in quote currency. 78.36 bps, verified to 10 decimal places and pinned as a regression test. Best net forecast in 10,478 audited minutes: +4.18 bps. When the signal is smaller than the rake, NO_TRADE is the alpha. Repo: https://github.com/MajidAsghariTabrizi/the-gambler-trading-lab"

## Post 3 — The challenger that lost to a constant
"We built a real learning loop: predict → mature outcomes → purge overlaps → train a challenger → gate promotion. First challenger: MAE 24.55 vs constant baseline 23.55. It lost. It stays in SHADOW. A learning system that can't say 'no' isn't learning — it's overfitting with extra steps. https://github.com/MajidAsghariTabrizi/the-gambler-trading-lab"