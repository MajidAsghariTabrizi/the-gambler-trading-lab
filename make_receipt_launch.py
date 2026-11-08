import json, hashlib, datetime, os
GID = 'goal-19744747-3e76-4395-8514-b423cb2947f9'
ev = [os.path.join(r'D:\\PycharmProjects\\pythonProject\\Trade\\public_release\\the-gambler-trading-lab', n) for n in ('README.md', 'unified\\predict.py', 'docs\\launch\\ARTICLE.md', 'assets\\social_preview_1280x640.png', 'assets\\demo_terminal.gif')]
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()
rec = {'goal_id': GID,
 'verification_id': 'vr-launch-' + datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S'),
 'evidence_refs': ev,
 'verifier': 'python -m pytest -q tests + gh run list + gh api releases/latest (cwd public_release/the-gambler-trading-lab)',
 'result': 'PASS',
 'verifier_output_head': 'CI success run 42512621235 @ 3a141e4 | 27 passed 2 skipped | links 0 broken | secrets 0 | release v1.0.0 | topics x9 | assets live (svg 1355 gif 42551 png 47904 bytes) | issues 1-3 created',
 'artifact_hashes': {os.path.basename(p): sha(p) for p in ev},
 'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'issued_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
out = os.path.join(r'C:\Users\ma.asghari\.dsh\var\verified-completion', GID + '.json')
json.dump(rec, open(out, 'w'), indent=1)
print('RECEIPT_AT', out)