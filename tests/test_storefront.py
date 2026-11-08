"""Evidence integrity and matched-population checks for the public storefront."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_published_storefront_matches_canonical_registry():
    subprocess.run([sys.executable, str(ROOT / 'scripts/build_storefront.py'), '--check'], check=True)


def test_benchmarks_preserve_population_and_control_semantics():
    data = json.loads((ROOT / 'research_registry/benchmarks.json').read_text())
    assert set(data) == {'direction', 'vf', 'p3'}
    for group in data.values():
        assert sum(bool(row[2]) for row in group['rows']) == 1
        assert all(0 <= row[1] <= group['max'] for row in group['rows'])
        assert 'population' in group['population'].lower() or 'Population:' in group['population']
    assert 'crosses zero' in data['direction']['explanation']
    assert min(data['vf']['rows'], key=lambda row: row[1])[2]
    assert min(data['p3']['rows'], key=lambda row: row[1])[2]


def test_public_fixture_independently_reproduces():
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/benchmark_public.py')], capture_output=True, text=True, check=True)
    report = json.loads(result.stdout)
    assert report['fixture']['independent_identity'] == 'passed'
    assert abs(float(report['fixture']['cost_bps']) - 78.3598661987) < 1e-9
