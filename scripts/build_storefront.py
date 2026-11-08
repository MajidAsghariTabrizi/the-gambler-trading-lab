"""Sync public evidence into the buildless storefront; --check detects drift."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRIES = ('models', 'experiments', 'benchmarks', 'repositories', 'evidence_manifest')


def build(check=False):
    target = ROOT / 'storefront' / 'data'
    if not check:
        target.mkdir(parents=True, exist_ok=True)
    stale = []
    for name in REGISTRIES:
        source = ROOT / 'research_registry' / f'{name}.json'
        content = source.read_bytes()
        json.loads(content)  # Reject invalid source before publication.
        destination = target / source.name
        if check:
            if not destination.exists() or destination.read_bytes() != content:
                stale.append(source.name)
        else:
            destination.write_bytes(content)
    if stale:
        raise SystemExit('Stale storefront data: ' + ', '.join(stale) + '. Run python scripts/build_storefront.py')
    print('Storefront evidence synchronized.' if not check else 'Storefront evidence matches source registries.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    build(parser.parse_args().check)
