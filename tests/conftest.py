import os, pytest
_PRIV = os.path.join(os.path.dirname(__file__), '..', '..', 'research', 'genesis_v3_gnxv3_20261104b', 'exports', 'v3_policy_decisions.parquet')
needs_private = pytest.mark.skipif(not os.path.exists(_PRIV), reason='private sealed artifact absent in public edition')
