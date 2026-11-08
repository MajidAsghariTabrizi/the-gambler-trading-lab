import os, sys, json
from conftest import needs_private
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))

@needs_private
def test_spec_frozen_immutable_shape():
    from unified import exresearch as XR
    spec = XR.load_spec()
    assert spec['experiment_id'] == 'EXPERIMENT_MAKER_BTCTMN_v1'
    assert spec['preregistered'] is True and spec['hypothesis_count'] == 1
    assert spec['required_independent_sample']['min_eligible_entries'] == 100
    assert XR.spec_hash() == '2591749e4d1bea4c'

def test_spread_distribution_and_regime():
    from unified import exresearch as XR
    pairs = [{'ts': i * 1000, 'bid': 100.0, 'ask': 100.0 + (0.01 if i < 70 else 0.5)} for i in range(100)]
    d = XR.spread_distribution(pairs)
    assert d['n'] == 100 and d['frac_below_6bps'] == 0.7
    e = XR.regime_episodes(pairs, thresh_bps=6.0, min_secs=60)
    assert e['episodes'] == 1 and e['longest_s'] == 70

def test_fill_bounds_conservative_lower_upper():
    from unified import exresearch as XR
    pairs = [{'ts': i * 1000, 'bid': 100.0, 'ask': 100.4} for i in range(120)]
    trades = [{'ts': 40000, 'buy': False, 'p': 99.9}, {'ts': 90000, 'buy': False, 'p': 100.0}]
    fb = XR.fill_bounds(pairs, trades, T_ms=20000, sample_every=30)
    assert fb['identifiable'] is False
    assert fb['strict']['fill_rate'] <= fb['touch']['fill_rate']

def test_policy_economics_no_double_count():
    from unified import exresearch as XR
    p = XR.policy_economics(20.0)
    assert p['A_taker_taker'] == 80.0
    assert p['B_maker_taker_fee0'] == 40.0
    assert p['D_maker_maker_fee0'] == 0.0