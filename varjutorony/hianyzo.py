"""Gyors ellenőrzés írás közben: hiányzó hivatkozások, fejezetszám, hossz régiónként."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'fejezetek'))
import kv
kv.load_all()
def refs(o):
    if isinstance(o, kv.T): yield str(o)
    elif isinstance(o, (list, tuple)):
        for x in o: yield from refs(x)
miss = {}
for n, (t, ops) in kv.S.items():
    for m in re.findall(r'\[\[(\w+)\]\]', t) + list(refs(ops)):
        if m not in kv.S: miss.setdefault(m, []).append(n)
    links = set(re.findall(r'\[\[(\w+)\]\]', t))
    for m in refs(ops):
        if m not in links and m != n: print('szabálycél nincs a szövegben:', n, '->', m)
    if len(t) > 1400: print('hosszú:', n, len(t))
from collections import Counter
c = Counter(kv.REGION.values()); ch = Counter()
for n in kv.S: ch[kv.REGION[n]] += len(kv.S[n][0])
print({r: (c[r], ch[r]) for r in c}, 'össz:', len(kv.S), sum(ch.values()))
print('hiányzó:', miss)
