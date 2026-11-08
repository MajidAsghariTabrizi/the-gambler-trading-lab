# Reproducibility & Data Limitations

## Fully reproducible from this repository (offline)
- The 78.3598661987 bps cost fixture and its regression tests.
- Decision engine determinism, fail-closed behavior, paper lifecycle, restart idempotency (synthetic fixtures).
- Champion/challenger promotion atomicity and rollback (synthetic).
- The offline demo pipeline.

## Reproducible only with private research data (not redistributable)
Exchange terms do not clearly grant redistribution of raw tapes/depth, so the following numbers are published as **VERIFIED (private data)** with commands that ran against sealed private artifacts:
- MODEL_V2 54.60% / 0.5643; VNEXT 52.47%; zero-change control 53.34%.
- Genesis V3 MAE 28.336 and the 0-BUY/10,478 result.
- Victory Fusion C1/C2; P3 challenger; spread/fill-bound distributions.

We publish schemas, code paths, and cryptographic hashes of the sealed artifacts (see manifest) so the *methods* are auditable even where the *data* cannot travel.

## Grading scheme
VERIFIED · REPRODUCED · REPORTED_ONLY · EXPERIMENTAL · UNVERIFIED · REJECTED · INSUFFICIENT_EVIDENCE — every public claim carries one.