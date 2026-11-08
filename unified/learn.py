# LearningService: scheduled loop - outcome maturity -> challenger -> GATED promotion.
import os, sys, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from unified import state, registry, predict

def learning_cycle(min_matured=50):
    rows = state.conn().execute('select count(*) from outcomes where matured=1 and y_bps is not null').fetchone()[0]
    if rows < min_matured:
        return {'status': 'INSUFFICIENT_DATA', 'matured_with_y': rows, 'min_required': min_matured}
    m, cols, spec_hash, n = predict._fit()
    metrics = {'train_n': n, 'cols': cols, 'note': 'mechanical refit; economic evaluation preregistration required'}
    model_id = 'challenger_' + spec_hash[:8]
    registry.register(model_id, 'ridge_net', spec_hash, 'dev-window', metrics)
    'Promotion gate: requires a PREREGISTERED independent evaluation - none registered -> stays SHADOW.'
    return {'status': 'CHALLENGER_SHADOW_ONLY', 'model_id': model_id, 'promotion': 'GATED_OFF: no preregistered evaluation'}