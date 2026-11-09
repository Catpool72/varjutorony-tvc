"""A könyv ellenőrzése a fejezetfájlokból: elérhetőség, zsákutcák, nyerhetőség (tárgyállapotokkal).
Az arany, a próbák és a harcok kimenetele ismeretlen: mindkét ágat bejárja."""
import os, re, sys
from collections import deque, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'fejezetek'))
import kv
kv.load_all()

def flat(ops):
    out = []
    for o in ops:
        out += flat(o) if isinstance(o, list) else [o]
    return out
LINKS = {n: list(dict.fromkeys(re.findall(r'\[\[(\w+)\]\]', t))) for n, (t, _) in kv.S.items()}
OPS = {n: flat(o) for n, (_, o) in kv.S.items()}

VIS = None
def cond(c, items):
    """-> lehetséges értékek halmaza"""
    if isinstance(c, tuple):
        if c[0] in ('vis', '!vis'):
            if VIS is None: return {True, False}
            return {(str(c[1]) in VIS) == (c[0] == 'vis')}
        return {True}                         # arany: feltételezzük
    neg = c.startswith('!'); c = c.lstrip('!')
    if c in ('res', 'rev'): return {True, False}
    v = c in items
    return {v != neg}

def run(ops, items, choices):
    """-> [(items, choices)]"""
    if not ops: return [(items, choices)]
    o, rest = ops[0], ops[1:]
    k = o[0]
    if k == 'GAIN': return run(rest, items | {o[1]}, choices)
    if k == 'LOSE': return run(rest, items - {o[1]}, choices)
    if k == 'GATE':
        out = []
        for v in cond(o[2], items):
            out += run(rest, items, choices if v else [c for c in choices if c != str(o[1])])
        return out
    if k == 'ONLY': return run(rest, items, [str(o[1])])
    if k == 'PICK': return run(rest, items, [str(o[1])]) + run(rest, items, [str(o[2])])
    if k == 'IF':
        out = []
        for v in cond(o[1], items):
            out += run(flat(o[2] if v else o[3]) + rest, items, choices)
        return out
    if k == 'SHOP':
        out = run(rest, items, choices)
        for it, _ in o[1]:
            out += run(rest, items | {it}, choices)
        return out
    return run(rest, items, choices)

import itertools, random
def conds_of(ops):
    for o in ops:
        if o[0] == 'GATE': yield o[2]
        if o[0] == 'IF': yield o[1]; yield from conds_of(flat(o[2])); yield from conds_of(flat(o[3]))
def item_of(c):
    return None if isinstance(c, tuple) or c.lstrip('!') in ('res', 'rev') else c.lstrip('!')
dead = [n for n in kv.S if not LINKS[n] and n != 'gyozelem']
print('fejezet:', len(kv.S), 'halál-fejezet:', len(dead))
# 1. helyi zsákutca: a fejezet saját feltételeinek minden kombinációjára marad-e választás
for n in kv.S:
    if n in dead: continue
    its = sorted({item_of(c) for c in conds_of(OPS[n])} - {None})
    for combo in itertools.product([0, 1], repeat=len(its)):
        items = {i for i, b in zip(its, combo) if b}
        for _, ch in run(OPS[n], frozenset(items), LINKS[n]):
            if not ch and not any(isinstance(c, tuple) and 'vis' in c[0] for c in conds_of(OPS[n])):
                print('üres menü:', n, sorted(items))
    if len(LINKS[n]) > 6: print('túl sok cél:', n, len(LINKS[n]))
# 3. véletlen játékosok a valódi tárgyállapottal (a próbák/harcok kimenete véletlen)
rnd = random.Random(7); wins = 0; deaths = defaultdict(int); stuck = defaultdict(int); visit = defaultdict(int)
WINWAY = defaultdict(int)
for g in range(20000):
    n, items, path = 'kezdet', frozenset(['kenyer']), []
    VIS.clear() if VIS is not None else None; globals()['VIS'] = set()
    for step in range(400):
        visit[n] += 1; path.append(n); globals()['VIS'].add(n)
        if n == 'gyozelem': wins += 1; break
        if n in dead: deaths[n] += 1; break
        outs = run(OPS[n], items, LINKS[n])
        items, ch = rnd.choice(outs); items = frozenset(items)
        if not ch: stuck[n] += 1; break
        n = rnd.choice(ch)
    else: stuck['(hurok)'] += 1
    if n == 'gyozelem':
        WINWAY[next((p for p in ('morvath_nev', 'morvath_gyuru', 'morvath_viz', 'morvath_napko', 'morvath_harc') if p in path), '?')] += 1
print('győzelem:', wins, 'a 20000 véletlen játékból; módja:', dict(WINWAY))
print('halál:', dict(sorted(deaths.items(), key=lambda x: -x[1])))
print('elakadás:', dict(stuck))
print('soha nem látogatott (véletlen):', [n for n in kv.S if not visit[n]])
