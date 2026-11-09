# Validate the Atlas: registry invariants + doc coverage + link integrity.
import json, os, re, sys
root = os.path.join(os.path.dirname(__file__), '..')
R = os.path.join(root, 'research_registry')
models = json.load(open(os.path.join(R, 'models.json')))
exps = json.load(open(os.path.join(R, 'experiments.json')))
repos = json.load(open(os.path.join(R, 'repositories.json')))
assert len(models) >= 15 and len(exps) >= 8 and len(repos) >= 9
VALID = {'TRAINED_VERIFIED','TRAINED_REPORTED_ONLY','TRAINED_ARTIFACT_MISSING','IMPLEMENTED_NOT_TRAINED','PROPOSED_ONLY','REJECTED','NOT_FOUND','IMPLEMENTED_VERIFIED','REGISTERED_SEALED','REGISTERED_READOUT_20261014','INSUFFICIENT_EVIDENCE','EXPERIMENTAL'}
for m in models: assert m['status'] in VALID, m.get('id')
frozen = [e for e in exps if e['status'] == 'FROZEN_PROSPECTIVE']
assert any('2591749e4d1bea4c' in str(e) for e in frozen)
for need in ['docs/research/ATLAS.md','docs/models/ALL_MODELS.md','docs/research/FAILED_HYPOTHESES.md']:
    assert os.path.exists(os.path.join(root, need)), need
bad = []
for dirpath, _, files in os.walk(root):
    for fn in files:
        if not fn.endswith('.md'): continue
        fp = os.path.join(dirpath, fn)
        for m2 in re.finditer(r'\]\(([^)#?\s]+)(?:#[^)\s]*)?\)', open(fp, encoding='utf-8').read()):
            t = m2.group(1)
            if t.startswith(('http://','https://','mailto:')): continue
            if not os.path.exists(os.path.normpath(os.path.join(dirpath, t))): bad.append(fn + ' -> ' + t)
assert not bad, bad
print('ATLAS_VALID: %d models, %d experiments, %d repositories, 0 broken links' % (len(models), len(exps), len(repos)))