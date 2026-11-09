#!/usr/bin/env python3
"""
A VARJÚTORONY URA – saját kalandkönyv a TVC kalandkönyv-motorhoz (bővített, lemezes változat).

A fejezetek régiónként a fejezetek/*.py fájlokban vannak: sec(név, szöveg, *szabályok).
A szövegben a [[név]] hivatkozásból "lapozz a(z) N-re/-ra" lesz; a szabályokban T('név').
A számozás rögzített véletlen sorrend: az 1. a kezdet.
"""
import json, os, random, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'fejezetek'))
import kv
kv.load_all()

TITLE = 'A VARJÚTORONY URA'
INTRO = open(os.path.join(HERE, 'fejezetek', 'intro.txt'), encoding='utf-8').read()

names = list(kv.ORDER)
first = 'kezdet'
rest = [n for n in names if n != first]
random.Random(1975).shuffle(rest)
NUM = {first: 1}
for i, n in enumerate(rest): NUM[n] = i + 2

ONES = ['', 'egy', 'kettő', 'három', 'négy', 'öt', 'hat', 'hét', 'nyolc', 'kilenc']
TENS = ['', 'tíz', 'húsz', 'harminc', 'negyven', 'ötven', 'hatvan', 'hetven', 'nyolcvan', 'kilencven']
VOW = 'aáeéiíoóöőuúüű'
def last_word(n):
    if n % 10: return ONES[n % 10]
    if n % 100: return TENS[(n % 100) // 10]
    return 'száz'
def first_word(n):
    if n >= 100: return 'száz' if n < 200 else ONES[n // 100]
    if n >= 10: return TENS[n // 10]
    return ONES[n]
def lapozz(n):
    art = 'az' if first_word(n)[0] in VOW else 'a'
    vow = [c for c in last_word(n) if c in VOW]
    return f'lapozz {art} {n}-{"re" if vow[-1] in "eéiíöőüű" else "ra"}'

def clean(s):
    return s.replace('–', '-').replace('„', '"').replace('”', '"').replace('…', '...')

def render(text):
    jumps = []
    def sub(m):
        name = m.group(1)
        assert name in NUM, f'nincs ilyen fejezet: {name}'
        t = NUM[name]
        if t not in jumps: jumps.append(t)
        return lapozz(t)
    return clean(re.sub(r'\[\[(\w+)\]\]', sub, text)), jumps

def resolve(o):
    if isinstance(o, kv.T): return NUM[str(o)]
    if isinstance(o, tuple): return tuple(resolve(x) for x in o)
    if isinstance(o, list): return [resolve(x) for x in o]
    return o

def build():
    secs = []
    for name in names:
        text, jumps = render(kv.S[name][0])
        secs.append({'id': NUM[name], 'name': name, 'region': kv.REGION[name], 'text': text, 'jumps': jumps})
    secs.sort(key=lambda s: s['id'])
    meta = {'title': TITLE, 'win': NUM['gyozelem'],
            'ui': {'TITLE1': TITLE, 'TITLE2': 'kalandkönyv', 'TITLE3': 'Kaland Játék Kockázat',
                   'TITLE4': 'TVC lemezes változat'},
            'disk_title4': 'TVC lemezes változat'}
    return {'meta': meta, 'intro': clean(' '.join(INTRO.split())), 'sections': secs}

if __name__ == '__main__':
    doc = build()
    json.dump(doc, open(os.path.join(HERE, 'book.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(doc['sections']), 'fejezet;', sum(len(s['text']) for s in doc['sections']), 'karakter;',
          dict(Counter(s['region'] for s in doc['sections'])))

def write_txt(doc, path):
    import textwrap
    o = [TITLE, '=' * len(TITLE), '', textwrap.fill(doc['intro'], 100), '']
    for s in doc['sections']:
        o += [f"{s['id']}.", textwrap.fill(s['text'], 100), '']
    open(path, 'w', encoding='utf-8').write('\n'.join(o))

if __name__ == '__main__':
    write_txt(build(), os.path.join(HERE, 'varjutorony.txt'))
