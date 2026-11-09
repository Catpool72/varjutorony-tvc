#!/usr/bin/env python3
"""
A Sárkány szeme – szövegtömörítő TVC-hez (BPE + kanonikus Huffman).

Minden fejezet önállóan, véletlen eléréssel kicsomagolható:
  * BPE: a gyakori karakterpárokat rekurzívan új tokenekkel helyettesíti
    (token < NBASE: alapkarakter, különben szabály: bal + jobb token).
  * A tokenfolyamot kanonikus Huffman-kód tömöríti (max. 15 bit/kód).
    Dekódolás bitenként: code = code*2 + bit; ha code < LIM[len], akkor
    token = SYMS[code + OFF[len]] (LIM és OFF előre kiszámolva).
  * Minden fejezet END tokennel zárul, és bájthatáron kezdődik.

Kimenet (az --out könyvtárba):
  book_text.bin    tömörített fejezetek egymás után
  book_index.bin   407 x 3 bájt: a fejezet kezdete a book_text.bin-ben (24 bit, little endian)
  book_tables.asm  NBASE, CHARTAB, RULES, LIMOFF, SYMS – a kicsomagoló rezidens táblái
  book_ref.txt     a várt kimenet (ellenőrzéshez), fejezetenként egy sor

Használat:
  python3 encode.py sarkany_szeme.json --tokens 1024 --out build/
"""
import argparse, collections, heapq, json, os

MAXBITS = 15      # így a LIM érték 16 biten mindig ábrázolható

# Alapkarakter -> kimeneti kód. Alapértelmezés: ISO-8859-2 (Latin-2).
# A TVC saját karakterkódjaihoz ezt a táblát kell átírni (csak az ékezetes betűket).
def default_charmap(ch):
    try:
        b = ch.encode('iso8859_2')
        if len(b) == 1 and b[0] != 0:
            return b[0]
    except UnicodeEncodeError:
        pass
    return ord('?')

def bpe(seqs, base, K, minpair=4):
    """Rekurzív párhelyettesítés. Visszaad: új szekvenciák, szabálylista [(bal, jobb)]."""
    seqs = [list(s) for s in seqs]
    pc = collections.Counter()
    for s in seqs:
        pc.update(zip(s, s[1:]))
    rules = []
    nxt = base
    while nxt < K and pc:
        (a, b), c = pc.most_common(1)[0]
        if c < minpair:
            break
        rules.append((a, b))
        for i, s in enumerate(seqs):
            if a not in s:
                continue
            o = []
            j = 0
            n = len(s)
            changed = False
            while j < n:
                if j + 1 < n and s[j] == a and s[j + 1] == b:
                    o.append(nxt); j += 2; changed = True
                else:
                    o.append(s[j]); j += 1
            if changed:
                pc.subtract(zip(s, s[1:]))
                pc.update(zip(o, o[1:]))
                seqs[i] = o
        pc = +pc
        nxt += 1
    return seqs, rules

def huff_lengths(freq):
    h = [(f, i, (s,)) for i, (s, f) in enumerate(sorted(freq.items()))]
    heapq.heapify(h)
    L = collections.Counter({s: 0 for s in freq})
    if len(h) == 1:
        L[h[0][2][0]] = 1
        return L
    k = len(h)
    while len(h) > 1:
        f1, _, a = heapq.heappop(h)
        f2, _, b = heapq.heappop(h)
        for s in a + b:
            L[s] += 1
        k += 1
        heapq.heappush(h, (f1 + f2, k, a + b))
    return L

def limited_lengths(freq):
    f = dict(freq)
    while True:
        L = huff_lengths(f)
        if max(L.values()) <= MAXBITS:
            return L
        f = {s: max(1, v // 2) for s, v in f.items()}

def canonical(L):
    """puff.c-kompatibilis kanonikus kód: hossz szerint, azon belül szimbólum szerint."""
    count = [0] * (MAXBITS + 1)
    for s, l in L.items():
        count[l] += 1
    syms = sorted(L, key=lambda s: (L[s], s))
    codes = {}
    code = 0
    first = 0
    idx = 0
    for ln in range(1, MAXBITS + 1):
        for k in range(count[ln]):
            codes[syms[idx + k]] = (first + k, ln)
        idx += count[ln]
        first = (first + count[ln]) << 1
    return count, syms, codes

class BitWriter:
    def __init__(self):
        self.out = bytearray(); self.acc = 0; self.n = 0
    def put(self, code, ln):
        for i in range(ln - 1, -1, -1):
            self.acc = (self.acc << 1) | ((code >> i) & 1); self.n += 1
            if self.n == 8:
                self.out.append(self.acc); self.acc = 0; self.n = 0
    def flush(self):
        if self.n:
            self.out.append(self.acc << (8 - self.n)); self.acc = 0; self.n = 0

def limoff(count):
    lim = [0] * (MAXBITS + 1); off = [0] * (MAXBITS + 1)
    first = idx = 0
    for ln in range(1, MAXBITS + 1):
        lim[ln] = first + count[ln]
        off[ln] = (idx - first) & 0xFFFF
        idx += count[ln]; first = (first + count[ln]) << 1
    assert max(lim) <= 0xFFFF
    return lim, off

def ref_decode(data, pos, count, syms, nbase, rules, chartab):
    """A Z80-rutinnal azonos algoritmus Pythonban."""
    bitbuf = 0x80
    def getbit():
        nonlocal bitbuf, pos
        bitbuf <<= 1
        if bitbuf & 0xFF == 0:
            byte = data[pos]; pos += 1
            bitbuf = ((byte << 1) | 1) & 0xFF
            return byte >> 7
        c = bitbuf >> 8; bitbuf &= 0xFF
        return c
    lim, off = limoff(count)
    out = bytearray()
    while True:
        code = 0
        for ln in range(1, MAXBITS + 1):
            code = (code << 1) | getbit()
            if code < lim[ln]:
                tok = syms[(code + off[ln]) & 0xFFFF]; break
        else:
            raise ValueError('rossz kód')
        st = [tok]
        while st:
            t = st.pop()
            if t < nbase:
                c = chartab[t]
                if c == 0:
                    return bytes(out)
                out.append(c)
            else:
                a, b = rules[t - nbase]; st.append(b); st.append(a)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('json')
    ap.add_argument('--tokens', type=int, default=1024, help='BPE tokenek max. száma (256..2048)')
    ap.add_argument('--out', default='build')
    a = ap.parse_args()
    doc = json.load(open(a.json, encoding='utf-8'))
    texts = [s['text'] for s in doc['sections']]
    assert len(texts) == 407
    os.makedirs(a.out, exist_ok=True)

    alphabet = sorted(set(''.join(texts)))
    chartab = [0] + [default_charmap(c) for c in alphabet]      # 0 = END
    cmap = {c: i + 1 for i, c in enumerate(alphabet)}
    nbase = len(chartab)
    assert nbase < 256, 'a Z80 kód 1 bájtos alapkarakter-indexet feltételez'
    seqs = [[cmap[c] for c in t] + [0] for t in texts]        # END token minden fejezet végén
    # az END-et ne vonja párba a BPE: külön kezeljük
    body, rules = bpe([s[:-1] for s in seqs], nbase, a.tokens)
    toks = [s + [0] for s in body]
    freq = collections.Counter(t for s in toks for t in s)
    L = limited_lengths(freq)
    count, syms, codes = canonical(L)

    data = bytearray(); index = []
    for s in toks:
        index.append(len(data))
        bw = BitWriter()
        for t in s:
            bw.put(*codes[t])
        bw.flush()
        data += bw.out
    assert len(data) < 1 << 24

    # mélység (a Z80 veremhez)
    depth = {}
    def d(t):
        if t < nbase: return 0
        if t in depth: return depth[t]
        l, r = rules[t - nbase]; depth[t] = 1 + max(d(l), d(r)); return depth[t]
    maxdepth = max((d(t) for t in range(nbase, nbase + len(rules))), default=0)

    # önellenőrzés
    exp = []
    for i, t in enumerate(texts):
        e = bytes(chartab[cmap[c]] for c in t)
        got = ref_decode(data, index[i], count, syms, nbase, rules, chartab)
        assert got == e, f'eltérés: {i+1}. fejezet'
        exp.append(e)

    open(os.path.join(a.out, 'book_text.bin'), 'wb').write(data)
    open(os.path.join(a.out, 'book_index.bin'), 'wb').write(b''.join(o.to_bytes(3, 'little') for o in index))
    with open(os.path.join(a.out, 'book_ref.txt'), 'wb') as f:
        for e in exp:
            f.write(e + b'\n')

    def dbrows(vals, per=16, kw='db'):
        out = []
        for i in range(0, len(vals), per):
            out.append(f'        {kw} ' + ','.join(str(v) for v in vals[i:i + per]))
        return '\n'.join(out)
    with open(os.path.join(a.out, 'book_tables.asm'), 'w', encoding='utf-8') as f:
        f.write('; A Sárkány szeme – kicsomagoló táblák (encode.py generálta, ne szerkeszd kézzel)\n')
        f.write(f'; BPE tokenek: {nbase + len(rules)}, alapkarakterek: {nbase} (0 = END), max. kódhossz: {max(L.values())} bit,'
                f' max. BPE-mélység: {maxdepth}\n')
        f.write(f'NBASE   equ {nbase}\n')
        f.write(f'NSECT   equ {len(texts)}\n\n')
        f.write('CHARTAB:                ; token < NBASE -> kimeneti kód (0 = fejezet vége)\n')
        f.write(dbrows(chartab) + '\n\n')
        f.write('RULES:                  ; token >= NBASE: dw bal, jobb\n')
        flat = [x for r in rules for x in r]
        f.write((dbrows(flat, 16, 'dw') if flat else '') + '\n\n')
        lim, off = limoff(count)
        f.write(f'LIMOFF:                 ; hosszanként (1..{MAXBITS} bit): dw LIM, OFF\n')
        f.write(dbrows([x for ln in range(1, MAXBITS + 1) for x in (lim[ln], off[ln])], 16, 'dw') + '\n\n')
        f.write('SYMS:                   ; tokenek kanonikus sorrendben\n')
        f.write(dbrows(syms, 16, 'dw') + '\n')

    tab = nbase + len(rules) * 4 + MAXBITS * 4 + len(syms) * 2
    stats = {
        'tokens': nbase + len(rules), 'nbase': nbase, 'rules': len(rules),
        'text_bytes': len(data), 'index_bytes': 3 * len(index), 'table_bytes': tab,
        'total_bytes': len(data) + 3 * len(index) + tab, 'raw_chars': sum(len(t) for t in texts),
        'max_code_bits': max(L.values()), 'max_bpe_depth': maxdepth,
        'max_section_chars': max(len(t) for t in texts),
        'alphabet': ''.join(alphabet),
    }
    json.dump(stats, open(os.path.join(a.out, 'stats.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(stats, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
