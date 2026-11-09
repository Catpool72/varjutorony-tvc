#!/usr/bin/env python3
"""
A Sárkány szeme – TVC GRAPHICS 2 demó build.

  python3 build.py [--tokens 512] [--images 3]

Lépések:
 1. ábécé -> font-indexek (0 = fejezet vége), 8x10-es font (font.py)
 2. a teljes könyv BPE + kanonikus Huffman tömörítése a font-indexekre
    (a kicsomagoló közvetlenül font-indexet ír a pufferbe)
 3. demó-részhalmaz: az 1. fejezettől szélességi bejárással annyi fejezet,
    amennyi a CAS-ba fér ($19EF..$BFFF), plusz az első N illusztráció
 4. a rajzok 240x240-es keretbe (30 bájt x 240 sor), GRAPHICS 2 formátumban
 5. data.inc + bináris blobok, sjasmplus fordítás, CAS
"""
import argparse, collections, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tvc_text', 'tools'))
sys.path.insert(0, os.path.join(HERE, '..', 'tvc_gfx'))
sys.path.insert(0, HERE)
import encode as enc                       # bpe, limited_lengths, canonical, BitWriter, limoff
from font import cell
import rules as game
from tvcgfx import to_tvc, PIX_ASPECT
from PIL import Image
import numpy as np

SJ = os.environ.get('SJASMPLUS', 'sjasmplus')
BOOK = os.path.join(HERE, '..', 'tvc_text', 'sarkany_szeme.json')
ILL_DIR = os.environ.get('ILL_DIR', os.path.join(HERE, 'ill'))      # kivágott rajzok: p<oldal>.png
IMG_SECT = os.path.join(HERE, 'img_sections.json')                  # oldal -> fejezet
LIMIT = 0xC000                                                      # a CAS a $C000 alatt kell véget érjen

UI = {
    'TITLE1': 'A SÁRKÁNY SZEME',
    'TITLE2': 'Ian Livingstone',
    'TITLE3': 'Kaland Játék Kockázat',
    'TITLE4': 'TVC GRAPHICS 2 demó',
    'TITLE5': 'Szóköz/Tűz: indulás',
    'TITLE6': 'Esc: kilépés',
    'MSG_MORE': '--- tovább: Szóköz ---',
    'MSG_LAPOZZ': 'Lapozz:',
    'MSG_END': 'Kalandod véget ért. Szóköz: újra',
    'MSG_MISSING': 'Ez a fejezet ebben a demóban nem szerepel.',
    'MSG_WIN': 'GYŐZTÉL! Szóköz: új játék',
    'MSG_GAIN': 'Megszerezted: ', 'MSG_LOSE': 'Elvesztetted: ',
    'MSG_LUCK': 'Szerencsepróba: ', 'MSG_SKILL': 'Ügyességpróba: ',
    'MSG_OK': ' Sikerült!', 'MSG_FAIL': ' Nem sikerült.',
    'MSG_DICE': 'Dobás: ', 'MSG_DMG': ' ÉLETERŐ elvész',
    'MSG_LARVA': 'Húslárvák száma: ', 'MSG_KILL': 'Megöltél ', 'MSG_LEFT': ', maradt ',
    'MSG_SHEET': 'KALANDLAP', 'MSG_SK': 'ÜGYESSÉG  ', 'MSG_ST': 'ÉLETERŐ   ', 'MSG_LK': 'SZERENCSE ',
    'MSG_GOLD': 'Aranytallér: ', 'MSG_POT': 'Varázsital: ', 'MSG_DOSE': ' adag', 'MSG_ITEMS': 'Tárgyak:',
    'MSG_BACK': 'Szóköz: vissza', 'MSG_POTSEL': 'Válassz varázsitalt (2 adag):',
    'MSG_LMHELP': 'Fel/le, bal/jobb, Szóköz: ok',
    'MSG_SHOP': 'Vásárlás. Aranyad: ', 'MSG_DONE': 'Kész', 'MSG_NOGOLD': 'Nincs elég aranyad.',
    'MSG_HAVE': 'Ez már megvan.', 'MSG_LAP': 'Lap', 'MSG_ITAL': 'Ital', 'MSG_FIGHT': 'Harc', 'MSG_COLHINT': 'Bal/Jobb: háttér- és tintaszín', 'MSG_TRY': 'Próba',
    'MSG_S_SK': 'Ü ', 'MSG_S_ST': ' É ', 'MSG_S_LK': ' Sz ', 'MSG_S_GOLD': ' Arany ',
    'MSG_DRANK': 'Ittál a varázsitalból.', 'MSG_HARC': 'HARC', 'MSG_TOFIGHT': 'Harc következik! Szóköz: tovább', 'MSG_LB': 'Littlebig is harcol (Ü 8)',
    'MSG_ATTACK': 'Szóköz/Tűz: támadás', 'MSG_FLEEQ': 'Szóköz: támadás, Fel: menekülés',
    'MSG_NOFLEE': 'Nem sikerült, harcolnod kell!', 'MSG_ROUND': '. kör: ',
    'MSG_HIT': 'Megsebezted!', 'MSG_HURT': 'Megsebzett!', 'MSG_DRAW': 'Döntetlen.', 'MSG_PARRY': 'Kivédted.',
    'MSG_LBN': '   Littlebig: ', 'MSG_LBHIT': 'Talált!', 'MSG_MISS': 'Nem talált.',
    'MSG_SECOND': '   2. támadás: ', 'MSG_OTHER': '   Másik: ',
    'MSG_GAS': 'A gázfelhő elért! -4', 'MSG_DRAIN': 'Vérszívás: -1 ÉLETERŐ',
    'MSG_WON': 'Győztél! Szóköz: tovább',
    'TITLE7': 'Le: a mentett játék', 'MSG_SHEETKEYS': 'Szóköz: vissza Fel: ment Le: tölt',
    'MSG_SAVED': 'Elmentve. Szóköz: tovább', 'MSG_SAVEERR': 'Mentési hiba: ',
    'MSG_NOSAVE': 'Nincs mentés. Szóköz: tovább',
    'MSG_DISKERR': 'Lemezhiba: ', 'MSG_INTRO': 'ELŐZMÉNYEK', 'MSG_RETRY': ' Szóköz: újra', 'MSG_FEND': 'A harc véget ért. Szóköz: tovább',
}
assert all(len(v) <= 33 for k, v in UI.items() if k != 'MSG_MISSING'), [k for k, v in UI.items() if len(v) > 33]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tokens', type=int, default=512)
    ap.add_argument('--images', type=int, default=3)
    ap.add_argument('--out', default='')
    ap.add_argument('--book', default='', help='könyv mappa: book.json, rules_book.py, ill/, img_sections.json (alap: A Sárkány szeme)')
    ap.add_argument('--disk', action='store_true', help='teljes könyv VT-DOS lemezre (build_disk/)')
    ap.add_argument('--include', default='', help='ezek a fejezetek mindenképp a demóba (teszthez), pl. 227,14,143')
    a = ap.parse_args()
    if not a.out:
        a.out = os.path.join(HERE, 'build' + ('_' + os.path.basename(os.path.abspath(a.book)) if a.book else ''))
    global BOOK, ILL_DIR, IMG_SECT
    meta = {}
    if a.book:
        bd = os.path.abspath(a.book)
        BOOK = os.path.join(bd, 'book.json'); ILL_DIR = os.path.join(bd, 'ill'); IMG_SECT = os.path.join(bd, 'img_sections.json')
        sys.path.insert(0, bd)
        import importlib; importlib.import_module('rules_book')      # átírja a rules modul tartalmát
        meta = json.load(open(BOOK, encoding='utf-8')).get('meta', {})
        for k, v in meta.get('ui', {}).items(): UI[k] = v
    if a.disk:
        UI['TITLE4'] = meta.get('disk_title4', 'Teljes könyv, lemezes változat')
        if a.out == os.path.join(HERE, 'build'): a.out = os.path.join(HERE, 'build_disk')
        elif a.book and a.out == os.path.join(HERE, 'build_' + os.path.basename(os.path.abspath(a.book))):
            a.out += '_disk'
    a.out = os.path.abspath(a.out)
    os.makedirs(a.out, exist_ok=True)
    doc = json.load(open(BOOK, encoding='utf-8'))
    secs = {s['id']: s for s in doc['sections']}
    NS = max(secs)                                  # a könyv fejezeteinek száma
    assert NS + 1 < 52 * 8, f"túl sok fejezet a bejárt-térképhez: {NS}"
    WIN = meta.get('win', 400)                      # a győzelmi fejezet

    # 1. ábécé
    extra = ''.join(UI.values()) + ''.join(n for _, n in game.ITEMS) + ''.join(game.POTIONS) + \
        ''.join(m[0] for o in game.R.values() for x in o for m in (x[1] if x[0] == 'FIGHT' else []))
    for o in game.R.values():                 # harc az IF/ONCHOOSE ágakban
        for x in o:
            for y in (x[3] if x[0] == 'IF' else x[2] if x[0] == 'ONCHOOSE' else []):
                if y[0] == 'FIGHT': extra += ''.join(m[0] for m in y[1])
    if 'intro' in doc:
        intro = ' '.join(doc['intro'].split())
    else:
        it = doc['intro_text']
        intro = it[it.index('TANÁCSOK A JÁTÉKHOZ'):].replace('HÁTTÉRTÖRTÉNET', ' HÁTTÉRTÖRTÉNET ')
        intro = ' '.join(intro.split())
    TEXT_MAX = 0xF000 - 0xDC40 - 1                  # a szövegpuffer mérete (TEXT_BUF..VARS)
    HAS_INTRO = a.disk or 'intro' in doc           # az előzmények: lemezen mindig, kazettán, ha a könyv adja
    if HAS_INTRO:                                  # 0. és NS+1. "fejezet": tanácsok és háttértörténet
        cut = intro.index('. ', len(intro) // 2) + 2
        secs[0] = {'id': 0, 'text': intro[:cut - 1], 'jumps': [NS + 1]}
        secs[NS + 1] = {'id': NS + 1, 'text': intro[cut:], 'jumps': [1]}
    assert max(len(s['text']) for s in secs.values()) <= TEXT_MAX
    alpha = sorted(set(''.join(s['text'] for s in doc['sections']) + extra + intro))
    idx = {c: i + 1 for i, c in enumerate(alpha)}
    nbase = len(alpha) + 1
    font = bytes(10) + b''.join(bytes(cell(c)) for c in alpha)
    open(os.path.join(a.out, 'font.bin'), 'wb').write(font)

    # 2. tömörítés (teljes könyv)
    nums = ([0] if HAS_INTRO else []) + list(range(1, NS + 1)) + ([NS + 1] if HAS_INTRO else [])
    seqs = [[idx[c] for c in secs[n]['text']] for n in nums]
    body, rules = enc.bpe(seqs, nbase, a.tokens)
    toks = [s + [0] for s in body]
    L = enc.limited_lengths(collections.Counter(t for s in toks for t in s))
    count, syms, codes = enc.canonical(L)
    lim, off = enc.limoff(count)
    comp = {}
    for n, s in zip(nums, toks):
        bw = enc.BitWriter()
        for t in s: bw.put(*codes[t])
        bw.flush(); comp[n] = bytes(bw.out)
    chartab = list(range(nbase))                     # a kicsomagoló font-indexet ad ki
    # önellenőrzés
    for n in (1, NS):
        got = enc.ref_decode(comp[n], 0, count, syms, nbase, rules, chartab)
        assert got == bytes(idx[c] for c in secs[n]['text'])
    tables_size = nbase + 4 * len(rules) + 4 * enc.MAXBITS + 2 * len(syms)

    # 4. rajzok
    img_sect = {int(k): v for k, v in json.load(open(IMG_SECT)).items()}
    sect_img_page = {v: k for k, v in img_sect.items()}

    def make_img(page):
        src = Image.open(os.path.join(ILL_DIR, f'p{page}.png'))
        r = src.width / src.height
        h = 240
        if round(h * r / PIX_ASPECT) > 240:
            h = int(240 * PIX_ASPECT / r)
        bw = to_tvc(src, h, 'fs')
        frame = np.zeros((240, 240), bool)
        y0 = (240 - bw.shape[0]) // 2; x0 = (240 - bw.shape[1]) // 2
        # 2 színű mód: 0 = fekete háttér, 1 = zöld. A to_tvc kimenetében 1 = az eredeti fehér papír,
        # így a papír zöld, a rajz fekete vonalai feketék maradnak; a keret körülötte fekete.
        frame[y0:y0 + bw.shape[0], x0:x0 + bw.shape[1]] = bw
        Image.fromarray(np.stack([np.zeros_like(frame), np.where(frame, 255, 0), np.zeros_like(frame)], -1).astype('uint8')).save(os.path.join(a.out, f'img_p{page}.png'))
        return np.packbits(frame, axis=1).tobytes()     # 240 x 30 bájt

    # 3. részhalmaz: szélességi bejárás az 1-től
    order, seen, q = ([0, NS + 1] if HAS_INTRO else []), {1}, collections.deque([1])
    while q:
        n = q.popleft(); order.append(n)
        for j in secs[n]['jumps']:
            if j not in seen: seen.add(j); q.append(j)
    for n in range(1, NS + 1):                       # a kulcsos fejezetek a végére
        if n not in seen: order.append(n)
    force = [int(x) for x in a.include.split(',') if x]
    order = force + [n for n in order if n not in force]

    # lemezes változat: a tömörített fejezetek 4 KB-os blokkokba, bejárási sorrendben
    chunk_data, chunk_of = [], {}
    if a.disk:
        cur = bytearray()
        for n in order:
            if len(cur) + len(comp[n]) > 4096:
                chunk_data.append(bytes(cur)); cur = bytearray()
            chunk_of[n] = (len(chunk_data), len(cur)); cur += comp[n]
        chunk_data.append(bytes(cur))
        assert len(chunk_data) <= 100

    def emit(nsec, nimg, nslot=2):
        chosen = order[:nsec]
        cs = set(chosen)
        imgs = [n for n in chosen if n in sect_img_page][:nimg]
        if a.disk:
            imgs = sorted(n for n in sect_img_page)
            blob = b''; imgblob = b''
        else:
            blob = bytearray(); index = {}
            for n in sorted(chosen):
                index[n] = len(blob); blob += comp[n]
            open(os.path.join(a.out, 'secdata.bin'), 'wb').write(blob)
            imgblob = b''.join(make_img(sect_img_page[n]) for n in imgs)
            open(os.path.join(a.out, 'images.bin'), 'wb').write(imgblob)
        o = []
        w = o.append
        w('; generálta a build.py – ne szerkeszd kézzel')
        w(f'NBASE       equ {nbase}')
        w(f'SP_IDX      equ {idx[" "]}')
        w(f'DIG0_IDX    equ {idx["0"]}')
        w(f'DOT_IDX     equ {idx["."]}')
        for nm, ch in (('SLASH', '/'), ('COLON', ':'), ('LPAR', '('), ('RPAR', ')')):
            w(f'{nm}_IDX equ {idx[ch]}')
        kids = [game.ITEM_ID[k] for k, _ in game.KEY_ITEMS] or [0]
        if not game.KEY_ITEMS: kids = []
        assert len({i >> 3 for i in kids}) <= 1
        w(f'N_ITEMS     equ {len(game.ITEMS)}')
        w(f'WIN_SEC     equ {WIN}')
        w(f'INTRO2_SEC  equ {NS + 1}')
        w(f'START_SEC   equ {0 if HAS_INTRO else 1}')
        w(f'KEYBYTE     equ {kids[0] >> 3 if kids else 0}')
        w(f'KEYMASK     equ {sum(1 << (i & 7) for i in kids)}')
        w(f'START_GOLD  equ {game.START_GOLD}')
        w(f'N_SECT_DEMO equ {len(chosen)}')
        w(f'N_IMG       equ {len(imgs)}')
        def dbs(vals, kw='db', per=16):
            for i in range(0, len(vals), per):
                w(f'        {kw} ' + ','.join(str(v) for v in vals[i:i + per]))
        for k, s in UI.items():
            w(f'{k}:'); dbs([idx[c] for c in s] + [0])
        for i, (k, nm) in enumerate(game.ITEMS):
            if nm: w(f'IN{i}:'); dbs([idx[c] for c in nm] + [0])
        w('ITEMNAMES:'); dbs([f'IN{i}' if nm else '0' for i, (k, nm) in enumerate(game.ITEMS)], 'dw')
        w('ITEMLOSS:'); dbs([int(bool(nm) and k not in game.NO_RANDOM_LOSS) for k, nm in game.ITEMS])
        w('KEYTAB:')
        for k, n in game.KEY_ITEMS: w(f'        db {game.ITEM_ID[k]}\n        dw {n}')
        w('        db $FF')
        w('START_ITEMS:'); dbs([game.ITEM_ID[k] for k in game.START_ITEMS] + [255])
        for i, p in enumerate(game.POTIONS): w(f'POT{i}:'); dbs([idx[c] for c in p] + [0])
        w('POTNAMES: dw POT0,POT1,POT2')
        w('CHARTAB:'); dbs(chartab)
        w('RULES:'); dbs([x for r in rules for x in r], 'dw')
        w('LIMOFF:'); dbs([x for ln in range(1, enc.MAXBITS + 1) for x in (lim[ln], off[ln])], 'dw')
        w('SYMS:'); dbs(syms, 'dw')
        w('FONT:   incbin "font.bin"')
        if not a.disk:
            w('SEC_INDEX:                ; fejezetszám -> eltolás a SEC_DATA-ban, $FFFF = nincs a demóban')
            dbs([index.get(n, 0xFFFF) for n in range(0, NS + 1 + (1 if HAS_INTRO else 0))], 'dw')
        else:
            w('SEC_CHUNK:                ; fejezetszám -> blokk (Tnn.CAS), eltolás')
            for n in range(0, NS + 2):
                c, of = chunk_of.get(n, (0, 0))
                w(f'        db {c}\n        dw {of}')
            w('CHUNK_LEN:'); dbs([len(x) for x in chunk_data], 'dw')
        w('SEC_IMG:                  ; fejezetszám -> rajz sorszáma (0 = nincs)')
        dbs([0] + [imgs.index(n) + 1 if n in imgs else 0 for n in range(1, NS + 1)] + ([0] if HAS_INTRO else []))
        w('JUMPTAB:                  ; fejezetszám -> mutató: db darab, dw célok')
        dbs([('J0' if 0 in cs else '0')] + [f'J{n}' if n in cs else '0' for n in range(1, NS + 1)]
            + ([f'J{NS + 1}'] if HAS_INTRO else []), 'dw')
        enc_str = lambda t: [idx[c] for c in t] + [0]
        nscr = 0
        for n in sorted(chosen):
            j = secs[n]['jumps']
            w(f'J{n}:    db {len(j)}' + ('' if not j else '\n        dw ' + ','.join(map(str, j))))
            sc = game.script(n, enc_str) or [0]
            nscr += len(sc)
            dbs(sc)
        if not a.disk:
            w('IMGTAB:'); dbs(['0'] + [f'IMG_DATA+{7200 * i}' for i in range(len(imgs))], 'dw')
            w('SEC_DATA:  incbin "secdata.bin"')
            w('IMG_DATA:  incbin "images.bin"')
            w('DATA_END:')
        else:
            w('DATA_END:')
            w('CACHE      equ (DATA_END + 255) & $FF00')
            w('IMG_STAGE  equ $C000 - 7200')
            w(f'NSLOT      equ {nslot}')
        open(os.path.join(a.out, 'data.inc'), 'w', encoding='utf-8').write('\n'.join(o) + '\n')
        emit.nscr = nscr
        return chosen, imgs, len(blob), len(imgblob)

    import zene
    zene.build(os.path.join(a.out, 'zene.inc'))

    def assemble():
        r = subprocess.run([SJ, '--nologo'] + (['-DDISK'] if a.disk else []) + [ f'--sym={a.out}/kaland.sym', f'--lst={a.out}/kaland.lst',
                            f'-I{a.out}', f'-I{HERE}', os.path.join(HERE, 'kaland.asm')],
                           capture_output=True, text=True, cwd=a.out)
        syms_ = {}
        if os.path.exists(f'{a.out}/kaland.sym'):
            for line in open(f'{a.out}/kaland.sym'):
                p = line.replace(':', ' ').split()
                if len(p) >= 3 and p[1].upper() == 'EQU':
                    syms_[p[0]] = int(p[2].replace('0x', '').rstrip('h').lstrip('$'), 16)
        return r, syms_

    if a.disk:
        build_disk(a, emit, assemble, comp, order, make_img, sect_img_page, chunk_data)
        return

    # a legtöbb fejezet, ami befér
    lo, hi = 1, len(order)
    best = None
    while lo <= hi:
        mid = (lo + hi) // 2
        emit(mid, a.images)
        r, s = assemble()
        end = s.get('DATA_END')
        if r.returncode == 0 and end is not None and end <= LIMIT:
            best = mid; lo = mid + 1
        else:
            if r.returncode != 0 and end is None and mid < 3:
                print(r.stdout, r.stderr); sys.exit(1)
            hi = mid - 1
    chosen, imgs, tb, ib = emit(best, a.images)
    r, s = assemble()
    if r.returncode:
        print(r.stdout, r.stderr); sys.exit(1)
    subprocess.run([sys.executable, os.path.join(HERE, 'mkcas.py'), f'{a.out}/kaland.bin', f'{a.out}/kaland.cas'], check=True)
    info = {'tokens': a.tokens, 'nbase': nbase, 'tables_bytes': tables_size, 'sections_in_demo': len(chosen),
            'sections': sorted(chosen), 'images_sections': imgs, 'text_bytes': tb, 'image_bytes': ib,
            'code_end': hex(s.get('CODE_END', 0)), 'data_end': hex(s['DATA_END']),
            'free_bytes': LIMIT - s['DATA_END'], 'script_bytes': emit.nscr,
            'rules_sections_in_demo': sorted(n for n in chosen if n in game.R)}
    json.dump(info, open(f'{a.out}/info.json', 'w'), indent=1)
    print(json.dumps({k: v for k, v in info.items() if k != 'sections'}, indent=1))

def cas_bytes(data, autorun=False):
    """TVC .CAS: 128 bájtos külső fejléc (bufferelatlan) + 16 bájtos programfejléc + adat"""
    body = bytearray(16)
    body[1] = 0x01; body[2] = len(data) & 255; body[3] = len(data) >> 8
    body[4] = 0xFF if autorun else 0x00
    body += data
    blocks, last = divmod(len(body), 128)
    if last: blocks += 1
    hdr = bytearray(128)
    hdr[0] = 0x11; hdr[2] = blocks & 255; hdr[3] = blocks >> 8; hdr[4] = last
    return bytes(hdr + body)

def fat12_720k(files, label='SARKANY'):
    """720 KB-os TVC (VT-DOS) lemezkép: 2 oldal, 80 sáv, 9 szektor, 2 szektor/klaszter,
    112 gyökérbejegyzés, 2 x 3 szektoros FAT, F9 hordozó; a boot szektor EB FE 90 kezdetű."""
    SS, SPC, RES, NFAT, ROOT, TOT, SPF = 512, 2, 1, 2, 112, 1440, 3
    img = bytearray(SS * TOT)
    bs = bytearray(SS)
    bs[0:3] = b'\xEB\xFE\x90'; bs[3:11] = b'VTDOS1.2'
    bs[11:13] = SS.to_bytes(2, 'little'); bs[13] = SPC; bs[14:16] = RES.to_bytes(2, 'little'); bs[16] = NFAT
    bs[17:19] = ROOT.to_bytes(2, 'little'); bs[19:21] = TOT.to_bytes(2, 'little'); bs[21] = 0xF9
    bs[22:24] = SPF.to_bytes(2, 'little'); bs[24:26] = (9).to_bytes(2, 'little'); bs[26:28] = (2).to_bytes(2, 'little')
    img[0:SS] = bs
    root_off = SS * (RES + NFAT * SPF)
    data_off = root_off + ROOT * 32
    ncl = (TOT * SS - data_off) // (SS * SPC)
    fat = [0] * (ncl + 2); fat[0] = 0xFF9; fat[1] = 0xFFF
    assert len(files) <= ROOT
    nxt = 2
    for i, (name, data) in enumerate(files):
        base, ext = (name.split('.') + [''])[:2]
        e = bytearray(32)
        e[0:8] = base.upper().ljust(8).encode('ascii'); e[8:11] = ext.upper().ljust(3).encode('ascii')
        e[11] = 0x20
        e[22:24] = (0).to_bytes(2, 'little'); e[24:26] = ((2026 - 1980) << 9 | 11 << 5 | 8).to_bytes(2, 'little')
        need = max(1, -(-len(data) // (SS * SPC)))
        assert nxt + need <= ncl + 2, 'nem fér a lemezre'
        e[26:28] = nxt.to_bytes(2, 'little'); e[28:32] = len(data).to_bytes(4, 'little')
        for k in range(need):
            fat[nxt + k] = nxt + k + 1 if k < need - 1 else 0xFFF
        o = data_off + (nxt - 2) * SS * SPC
        img[o:o + len(data)] = data
        nxt += need
        img[root_off + 32 * i: root_off + 32 * i + 32] = e
    fb = bytearray(SPF * SS)
    for k in range(0, len(fat) - 1, 2):
        v = fat[k] | (fat[k + 1] << 12)
        fb[k * 3 // 2: k * 3 // 2 + 3] = v.to_bytes(3, 'little')
    if len(fat) % 2:
        k = len(fat) - 1; fb[k * 3 // 2: k * 3 // 2 + 2] = fat[k].to_bytes(2, 'little')
    for f in range(NFAT):
        o = SS * (RES + f * SPF); img[o:o + len(fb)] = fb
    return bytes(img), (ncl - (nxt - 2)) * SS * SPC

def build_disk(a, emit, assemble, comp, order, make_img, sect_img_page, chunk_data):
    emit(len(order), 0, 2)
    r, s = assemble()
    if r.returncode:
        print(r.stdout[-3000:], r.stderr); sys.exit(1)
    cache = (s['DATA_END'] + 255) & 0xFF00
    nslot = min(8, (0xC000 - 7200 - cache) // 4096)
    emit(len(order), 0, nslot)
    r, s = assemble()
    if r.returncode:
        print(r.stdout[-3000:], r.stderr); sys.exit(1)
    dist = os.path.join(a.out, 'lemez'); os.makedirs(dist, exist_ok=True)
    for f in os.listdir(dist): os.remove(os.path.join(dist, f))
    files = [('KALAND.CAS', cas_bytes(open(f'{a.out}/kaland.bin', 'rb').read(), autorun=True))]
    for i, c in enumerate(chunk_data):
        files.append((f'T{i:02d}.CAS', cas_bytes(c)))
    imgs = sorted(sect_img_page)
    for i, n in enumerate(imgs):
        files.append((f'I{i + 1:02d}.CAS', cas_bytes(make_img(sect_img_page[n]))))
    for name, data in files:
        open(os.path.join(dist, name), 'wb').write(data)
    dsk, free = fat12_720k(files)
    dsk_name = (os.path.basename(os.path.abspath(a.book)) if a.book else 'sarkany') + '.dsk'
    open(os.path.join(a.out, dsk_name), 'wb').write(dsk)
    info = {'disk': True, 'chunks': len(chunk_data), 'chunk_bytes': [len(c) for c in chunk_data],
            'images': len(imgs), 'nslot': nslot, 'code_end': hex(s['CODE_END']), 'data_end': hex(s['DATA_END']),
            'cache': hex(cache), 'disk_free_bytes': free, 'files': len(files),
            'main_cas_bytes': len(files[0][1])}
    json.dump(info, open(f'{a.out}/info.json', 'w'), indent=1)
    print(json.dumps(info, indent=1))

if __name__ == '__main__':
    main()
