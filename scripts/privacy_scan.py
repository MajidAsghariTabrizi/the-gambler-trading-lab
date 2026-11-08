import os, re
root = r'D:\PycharmProjects\pythonProject\Trade\public_release\the-gambler-trading-lab'
pats = [r'C:\\Users\\', r'ma[.]asghari', r'goal-[0-9a-f]{8}-', r'verified-completion', r'87[.]107[.]152[.]67', r'trader_vps']
hits = {}
for dp, _, fs in os.walk(root):
    if '.git' in dp: continue
    for f in fs:
        p = os.path.join(dp, f)
        try: t = open(p, encoding='utf-8', errors='ignore').read()
        except Exception: continue
        if f == 'privacy_scan.py': continue
        for pat in pats:
            if re.search(pat, t): hits.setdefault(os.path.relpath(p, root), []).append(pat)
for k, v in hits.items(): print(k, '->', ','.join(v))
print('TOTAL_FILES_WITH_HITS', len(hits))