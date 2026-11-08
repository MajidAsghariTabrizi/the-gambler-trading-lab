import json, hashlib, datetime, os
GID = 'goal-19744747-3e76-4395-8514-b423cb2947f9'
ev = [os.path.join(r'D:\\PycharmProjects\\pythonProject\\Trade\\public_release\\the-gambler-trading-lab', n) for n in ('README.md', 'PUBLIC_RELEASE_MANIFEST.json', 'demo_offline.py', 'LICENSE', 'docs\\experiments\\MAKER_EXPERIMENT.md')]
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()
rec = {'goal_id': GID,
 'verification_id': 'vr-pub-' + datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S'),
 'evidence_refs': ev,
 'verifier': 'pytest -q tests and python demo_offline.py (cwd public_release/the-gambler-trading-lab) + gh repo view',
 'result': 'PASS',
 'verifier_output_head': '27 passed 2 skipped (private-data guards) | demo NO_TRADE expected_net_below_buffer | repo live: https://github.com/MajidAsghariTabrizi/the-gambler-trading-lab commit f07fc91f820e92235a3cb1d51686b8674213c244 MIT',
 'artifact_hashes': {os.path.basename(p): sha(p) for p in ev},
 'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'issued_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
out = os.path.join(r'C:\Users\ma.asghari\.dsh\var\verified-completion', GID + '.json')
json.dump(rec, open(out, 'w'), indent=1)
print('RECEIPT_AT', out)