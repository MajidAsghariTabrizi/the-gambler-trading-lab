# FeatureService: causal features from the ingested event only (no future data).
def features_from(ev_payload):
    bid, ask = ev_payload['bid'], ev_payload['ask']
    mid = (bid + ask) / 2
    spread_bps = (ask - bid) / mid * 1e4
    return {'f_spread_bps': spread_bps, 'f_mid': mid, 'f_book_imbalance': 0.0,
            'f_v2_score': ev_payload.get('v2_score'), 'schema': 'unified-feat/1'}