# Evidence Observatory

A buildless, responsive research storefront in `storefront/`. No Node dependency, API key, account, or trading connection is required. Google Fonts are optional; system fonts remain available when offline.

## Preview and maintain

```bash
python scripts/build_storefront.py
python -m http.server 4173 --directory storefront
# Open http://localhost:4173
python scripts/build_storefront.py --check
python scripts/benchmark_public.py
pytest -q tests
```

Edit evidence in `research_registry/`, then synchronize it. The check runs in the existing Python test suite and rejects stale copies. `benchmarks.json` contains three distinct published evaluation populations, their controls, metric direction, and interpretations. Updating a published finding requires rechecking its underlying evidence and population; syncing JSON alone does not validate new research.

The page provides population tabs, model search, status filters, evidence dialogs, filtered JSON export, all experiment records, clipboard quick start, and an illustrative round-trip calculator. Keyboard users can navigate benchmark tabs with arrow, Home, and End keys; `/` focuses search, and Escape closes the native model dialog. A narrow screen keeps the model table scrollable inside its own container.

## Evidence boundaries

Private market tapes and trained artifacts are not bundled. Model scores are published summaries, not evaluations recomputed in the browser. The hero's schematic bars are explicitly decorative. Accuracy is never ranked against net-bps MAE, and the VF and P3 MAE populations are never pooled.

The calculator uses `bid/ask = (1 - spread/20000) / (1 + spread/20000)` for a mid-quoted spread, then `proceeds/notional = bid/ask * (1 - fee/10000)^2`. It displays rounded browser arithmetic. The Python Decimal fixture remains authoritative. The quote spread and its contribution to notional loss differ slightly because they use different denominators.

## Hosting

Serve `storefront/` on any static host. The private Sites deployment is a reviewable preview; it does not make the public repository's page available to everyone. A GitHub Pages workflow is intentionally not enabled automatically: hosting settings and the public launch remain an owner decision. No secrets belong in this static directory.
