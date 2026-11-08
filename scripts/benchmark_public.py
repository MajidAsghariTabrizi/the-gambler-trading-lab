"""Report matched published benchmarks and independently reproduce the cost fixture.

This does not retrain models or re-evaluate inaccessible private populations.
Run from the repository root: python scripts/benchmark_public.py
"""
import json
import platform
import sys
import time
from decimal import Decimal, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from gambler.economics import round_trip


def benchmark():
    groups = json.loads((ROOT / 'research_registry/benchmarks.json').read_text(encoding='utf-8'))
    comparisons = []
    for key, group in groups.items():
        # Rank inside one population only, with the metric's explicit direction.
        winner = (max if key == 'direction' else min)(group['rows'], key=lambda row: row[1])
        comparisons.append({'population': key, 'population_note': group['population'],
                            'metric': group['title'], 'best_observed': winner[0],
                            'value': winner[1], 'control': winner[2],
                            'interpretation': group['explanation'],
                            'evidence': 'published_private_data_summary_not_recomputed'})
    args = (1500000, 20400971155, 20438907946, 30)
    result = round_trip(*args)
    with localcontext() as context:
        context.prec = 40
        # Independent proceeds conservation identity, without engine helpers.
        ratio = Decimal(args[1]) / Decimal(args[2])
        expected = Decimal(args[0]) * ratio * (1 - Decimal('0.003')) ** 2
        if abs(result['proceeds_tmn'] - expected) > Decimal('1e-19'):
            raise AssertionError('Fixture disagrees with independent proceeds identity')
    for _ in range(50):
        round_trip(*args)
    iterations = 2000
    started = time.perf_counter()
    for _ in range(iterations):
        round_trip(*args)
    elapsed = time.perf_counter() - started
    return {'scope': 'Published within-population comparisons and public arithmetic fixture only',
            'python': platform.python_version(), 'comparisons': comparisons,
            'fixture': {'cost_bps': str(-result['net_bps']), 'proceeds_tmn': str(result['proceeds_tmn']),
                        'independent_identity': 'passed', 'fee_assumption_bps_per_leg': 30},
            'timing': {'iterations': iterations, 'seconds': round(elapsed, 6),
                       'microseconds_per_call': round(elapsed / iterations * 1e6, 3),
                       'note': 'Local warmed arithmetic microbenchmark, not model inference or a cross-platform guarantee'}}


if __name__ == '__main__':
    print(json.dumps(benchmark(), indent=2))
