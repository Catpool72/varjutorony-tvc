"""Közös segédek a régiófájlokhoz: sec(név, szöveg, *szabályok), T('név') hivatkozás a szabályokban."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import rules as G

class T(str):
    """fejezetnév-hivatkozás egy szabályban (a számozás után számmá alakul)"""

S = {}          # név -> (szöveg, szabályok)
ORDER = []
REGION = {}     # név -> régió

def sec(name, text, *ops):
    assert name not in S, f'kétszer: {name}'
    S[name] = (' '.join(text.split()), list(ops))
    ORDER.append(name)
    REGION[name] = sys._getframe(1).f_globals.get('__name__', '?').split('.')[-1]

U, E, SZ = G.U, G.E, G.SZ
st, gold, gain, lose, gate, only, pick, luck, skill, M, dmg = (
    G.st, G.gold, G.gain, G.lose, G.gate, G.only, G.pick, G.luck, G.skill, G.M, G.dmg)
EV_LOSE_ROUND, EV_FIRST_ROUND, EV_WIN_N, EV_SURVIVE_N, EV_WIN_ROUND, EV_FLEE6 = 1, 2, 3, 4, 5, 6

def _fl(ops):
    out = []
    for o in ops or []:
        out += o if isinstance(o, list) else [o]
    return out
def iff(c, then, els=None):
    return G.iff(c, _fl(then), _fl(els))

def shop(*items):
    return ('SHOP', list(items))
def onchoose(target, ops, label=0):
    return ('ONCHOOSE', target, _fl(ops), label)

def vis(name):  return ('vis', T(name))     # feltétel: jártunk már ott
def nvis(name): return ('!vis', T(name))    # feltétel: még nem jártunk ott
def fight(mons, win=None, **kw):
    """harc; ha már jártunk a fejezetben (és élünk), a legyőzött ellenfél nem támad újra"""
    ops = [G.iff('!rev', [('FIGHT', mons, kw)])]
    if win is not None: ops.append(only(win))
    return ops

BOV = {}
def bovit(**kw):
    """kiegészítő leírás: a fejezet első választási mondata elé kerül"""
    for k, v in kw.items():
        assert k not in BOV, f'kétszer bővítve: {k}'
        BOV[k] = ' '.join(v.split())

def apply_bovit():
    import re
    for k, add in BOV.items():
        assert k in S, f'bővítés nem létező fejezethez: {k}'
        text, ops = S[k]
        i = text.find('[[')
        if i < 0:
            i = text.find('A kalandod itt')
            if i < 0: i = text.find('Kalandod véget')
            j = i
        else:
            j = max(text.rfind(e, 0, i) for e in ('. ', '! ', '? ', '." ', '!" ', '?" '))
            j = 0 if j < 0 else j + (3 if text[j + 1] == '"' else 2)
        if j <= 0: text = add + ' ' + text
        else: text = text[:j] + add + ' ' + text[j:]
        S[k] = (text, ops)

REGIONS = ['falu', 'erdo', 'lap', 'hago', 'kulso', 'belso', 'felso', 'veg']
def load_all():
    """a régiók és a bővítések betöltése"""
    import importlib
    here = os.path.dirname(os.path.abspath(__file__))
    for r in REGIONS:
        importlib.import_module(r)
    for r in REGIONS:
        if os.path.exists(os.path.join(here, 'bovit_' + r + '.py')):
            importlib.import_module('bovit_' + r)
    apply_bovit()
