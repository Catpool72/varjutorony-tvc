#!/usr/bin/env python3
"""
A Sárkány szeme – játékszabályok fejezetenként (kézzel, a könyv szövegéből).

Minden fejezethez egy műveletlista tartozik; a build.py ebből bájtkódot fordít,
amit a kaland.asm értelmező futtat, miután a fejezet szövege megjelent.
A választható lapozási célok alapból a fejezet célpontjai (sarkany_szeme.json),
ezeket a GATE / ONLY / HIDE / ADD / KEYS műveletek szűkítik vagy bővítik.

Feltételek (cond):  'kotel'  = van ilyen tárgy,  '!kotel' = nincs,
                    'key' = bármilyen kulcs, 'res' = az előző próba / harc eredménye,
                    'x' = X > 0,  ('gold', 10) = van legalább 10 arany.
"""

# ---------------------------------------------------------------- tárgyak
# (azonosító, kiírt név – üres: rejtett jelző)
ITEMS = [
    ('pajzs', 'Pajzs'), ('emerald', 'Emeráld'), ('emerald2', 'Második emeráld'),
    ('fokhagyma', 'Fokhagyma'), ('ezusttor', 'Ezüsttőr'), ('karszalag', 'Ezüst karszalag'),
    ('levelek', 'Csípős levelek'), ('aranygomb', 'Aranygömb'), ('tukor', 'Tükördarab'),
    ('k14', 'Ezüstkulcs 14'), ('k34', 'Vaskulcs 34'), ('k85', 'Bronzkulcs 85'),
    ('k192', 'Rézkulcs 192'), ('k325', 'Aranykulcs 325'),
    ('zarnyito', 'Zárnyitó készlet'), ('kris', 'Kris kés'), ('turkiz', 'Türkizgyűrű'),
    ('koponya', 'Koponyahasogató'), ('lancing', 'Láncing'), ('sisak', 'Rúnás sisak'),
    ('kotel', 'Kötél'), ('karperec', 'Arany karperec'), ('harang', 'Bronzharang'),
    ('kristor', 'Kristálytőr'), ('zombigyuru', 'Zombiuraló gyűrű'), ('gyogyital', 'Gyógyital'),
    ('nyaklanc', 'Kígyós nyaklánc'), ('elfcsizma', 'Elf csizma'), ('amulett', 'Oroszlán amulett'),
    ('holdko', 'Holdkő melltű'), ('bot', 'Mennydörgés botja'), ('onsip', 'Ónsíp'),
    ('fejsze', 'Fejszefej'), ('csuzli', 'Csúzli'), ('aranyrog', 'Aranyrög'),
    ('sarkanyerme', 'Sárkányérme'), ('kereszt', 'Ezüstkereszt'), ('csontamulett', 'Csont amulett'),
    ('nyakek', 'Kristály nyakék'), ('majom', 'Majomszobor'), ('terkep', 'Térkép'),
    ('horog', 'Horgászhorog'), ('kreta', 'Kréta'), ('fakacsa', 'Fakacsa'),
    ('disznofarok', 'Disznófarok'), ('borzolaj', 'Borzolaj'), ('gyertya', 'Viaszgyertya'),
    ('gomba', 'Aszalt gomba'), ('tisztanlatas', 'Tisztánlátás itala'),
    ('vizlegzes', 'Vízlégzés itala'), ('zoldbor', 'Zöld bőr itala'), ('festmeny', 'Bagolyfestmény'),
    ('paszta', ''), ('tocsa', ''), ('varazsige', ''),
]
ITEM_ID = {k: i for i, (k, _) in enumerate(ITEMS)}
assert len(ITEMS) <= 64
KEY_ITEMS = [('k14', 14), ('k34', 34), ('k85', 85), ('k192', 192), ('k325', 325)]
NO_RANDOM_LOSS = {'emerald', 'emerald2'}          # ezeket a véletlen tárgyvesztés nem viszi el
START_ITEMS = ['pajzs', 'emerald']
START_GOLD = 10
POTIONS = ['ÜGYESSÉG Itala', 'ERŐ Itala', 'SZERENCSE Itala']

# ---------------------------------------------------------------- műveletek
U, E, SZ = 0, 1, 2
def st(s, d):        return ('STAT', s, d)
def gold(d):         return ('GOLD', d)
def gain(*it):       return [('GAIN', i) for i in it]
def lose(i):         return ('LOSE', i)
def gate(t, c):      return ('GATE', t, c)
def only(t):         return ('ONLY', t)
def pick(a, b):      return ('PICK', a, b)
def luck(a=None, b=None):
    return [('LUCK',)] + ([pick(a, b)] if a else [])
def skill(a=None, b=None):
    return [('SKILL',)] + ([pick(a, b)] if a else [])
def dmg(n, add=0):   return ('DMG', n, add)
def iff(c, then, els=None): return ('IF', c, then, els or [])

def M(name, sk, sta): return (name, sk, sta)
def fight(mons, win=None, **kw):
    """kw: all (egyszerre), lb (Littlebig is üt, Ü8), mdbl (a szörny kétszer támad),
    hitlim=n (n sebzés után res=1), pdmg/mdmg, skmod, ev=(típus, param), ext=típus"""
    ops = [('FIGHT', mons, kw)]
    if win is not None: ops.append(only(win))
    return ops

# harci események (ev) és kiegészítők (ext) – a kaland.asm FIGHT műveletével egyezően
EV_LOSE_ROUND, EV_FIRST_ROUND, EV_WIN_N, EV_SURVIVE_N, EV_WIN_ROUND, EV_FLEE6 = 1, 2, 3, 4, 5, 6
EXT_GAS, EXT_DRAIN, EXT_KRIS = 1, 2, 3

R = {}
def r(n, *ops):
    out = []
    for o in ops:
        out += o if isinstance(o, list) else [o]
    R[n] = out

# --- egyszerű pontváltozások, tárgyak, arany
r(3, st(U, -1), st(SZ, -1), st(E, -3))
r(5, st(U, -2))
r(7, gain('emerald2'))
r(8, st(E, -2))
r(17, st(E, 2), lose('gyogyital'))
r(19, gain('zombigyuru'))
r(21, st(U, 1), st(E, 1), gain('k34'))
r(24, st(SZ, -1))
r(28, st(U, -1), st(E, -2))
r(29, gain('aranyrog'))
r(31, st(SZ, -1))
r(32, st(E, 2), gain('gyogyital'))
r(37, st(U, 1), st(SZ, 1), gain('levelek'))
r(41, st(E, -1))
r(43, gold(2), gain('amulett'))
r(51, st(E, -2))
r(62, st(SZ, 1), gain('nyakek'))
r(66, st(U, -1), st(E, -4))
r(67, gain('holdko'))
r(68, gain('csontamulett'))
r(72, gain('turkiz'))
r(82, st(SZ, 1))
r(86, gain('varazsige'))
r(89, st(E, 1))
r(100, gold(7), gain('fokhagyma', 'k85'))
r(101, gold(3), gain('kereszt', 'kris'))
r(109, gain('k325'))
r(113, gold(5))
r(114, gold(2), gain('csuzli'))
r(118, gain('kotel'))
r(121, gain('sisak'), gate(331, 'nyaklanc'), gate(90, '!nyaklanc'))
r(123, st(E, 4), gain('terkep'))
r(127, gold(2), gain('karszalag'))
r(129, gold(5))
r(131, gold(5), gain('kristor'))
r(140, gain('majom'))
r(146, st(U, 1), gain('lancing'))
r(147, gold(2), gain('harang', 'horog'))
r(150, st(E, 1), gain('tocsa'))
r(155, gain('pajzs'))
r(168, lose('gyogyital'))
r(170, st(U, 1), st(E, 1))
r(179, st(E, -3))
r(198, st(E, -1), gain('bot'))
r(200, gold(3))
r(205, gain('aranygomb'))
r(207, st(E, -3))
r(215, st(U, -2), st(E, -2))
r(218, st(U, 1))
r(221, st(E, -7))
r(222, lose('sisak'))
r(228, st(E, 2))
r(244, st(U, -1))
r(247, st(E, 4))
r(252, gold(15), st(SZ, 1))
r(258, gold(1), gain('tukor'))
r(263, st(E, -2))
r(272, st(U, -1), st(E, -1), gain('karperec'))
r(278, st(U, 1), st(E, 2), gain('k14', 'paszta'))
r(283, st(E, -1))
r(289, st(U, 1), gain('elfcsizma'))
r(294, st(U, -1), st(E, -4), gate(110, ('gold', 10)))
r(295, st(E, 2), st(U, 1), gain('k192'))
r(297, gain('nyaklanc'))
r(299, gold(2), gain('harang', 'horog'))
r(302, st(U, -4), st(E, -4))
r(311, gain('fejsze'))
r(314, st(E, 2))
r(316, lose('pajzs'), st(E, -2))
r(327, gold(27))
r(331, st(SZ, 1), st(U, 1))
r(340, st(E, 2))
r(347, st(U, 1))
r(349, st(U, -1))
r(358, st(U, 1), gain('koponya'))
r(364, gain('sarkanyerme'))
r(369, st(E, -2))
r(375, st(E, -2))
r(379, gold(-10), gold(2), gain('karszalag'))
r(382, gold(7), gain('zarnyito', 'kereszt', 'horog'))
r(383, st(E, -2))
r(392, st(U, -1), st(E, -4))
r(404, st(E, -1))
# fizetés
r(15, gold(-1))
r(39, ('GOLD0',))
r(110, gold(-10))
r(243, gate(15, ('gold', 1)))
r(334, gate(379, ('gold', 10)))
r(354, gate(96, ('gold', 1)))
# kulcsok
for k, n in KEY_ITEMS:
    r(n, lose(k))
r(159, gate(276, 'key'), gate(259, '!key'))
r(175, ('KEYS',))
r(227, ('KEYS',))
r(378, gate(175, 'key'), gate(390, '!key'))
# tárgyfeltételek
r(10, gate(372, 'fokhagyma'), gate(163, 'ezusttor'), gate(107, '!fokhagyma'), gate(107, '!ezusttor'))
r(30, gate(56, 'karszalag'), gate(279, '!karszalag'))
r(122, gate(342, 'karszalag'), gate(61, '!karszalag'))
r(135, dmg(2), gate(247, 'levelek'), gate(4, '!levelek'), gate(318, '!levelek'))
r(145, gate(347, 'aranygomb'))
r(160, st(E, -2), gate(195, 'kris'), gate(371, '!kris'))
r(177, gate(138, 'amulett'), gate(52, 'holdko'), gate(333, 'bot'), gate(96, ('gold', 1)))
r(181, gate(82, 'turkiz'), gate(332, '!turkiz'))
r(185, gate(49, 'emerald2'), gate(84, '!emerald2'))
r(187, gate(347, 'aranygomb'), gate(145, 'onsip'))
r(197, gate(87, 'koponya'), gate(172, '!koponya'))
r(216, gate(397, 'pajzs'), gate(132, '!pajzs'))
r(233, gate(242, 'kotel'), gate(120, '!kotel'))
r(241, gate(12, 'karperec'), gate(182, '!karperec'))
r(259, gate(296, 'harang'), gate(189, '!harang'))
r(260, gate(315, 'paszta'), gate(338, '!paszta'))
r(276, gate(296, 'harang'), gate(189, '!harang'))
r(279, st(E, -4), gate(195, 'kris'), gate(371, '!kris'))
r(301, gate(58, 'zombigyuru'), gate(310, '!zombigyuru'), gate(78, '!zombigyuru'))
r(305, gate(194, 'elfcsizma'), gate(335, '!elfcsizma'))
r(318, gate(344, 'zarnyito'), gate(159, '!zarnyito'))
r(345, gate(270, 'karperec'), gate(93, '!karperec'))
r(352, gate(17, 'gyogyital'), gate(115, '!gyogyital'))
r(363, gate(91, 'karszalag'), gate(275, '!karszalag'))
r(372, gate(163, 'ezusttor'))
r(384, gate(168, 'gyogyital'), gate(221, '!gyogyital'))
r(386, gate(292, 'varazsige'), gate(130, '!varazsige'))
r(394, gate(282, 'tocsa'), gate(135, '!tocsa'))
r(180, iff('sisak', [st(E, -1)], [st(E, -4)]))
r(208, iff('lancing', [st(E, -1)], [st(E, -4)]))
# szerencse- és ügyességpróbák
for n, a, b in [(44, 33, 316), (50, 118, 392), (78, 164, 339), (256, 48, 375), (257, 273, 384),
                (274, 23, 80), (285, 313, 28), (307, 77, 174), (335, 203, 269), (365, 105, 179),
                (403, 246, 207)]:
    r(n, luck(a, b))
r(90, st(E, -5), luck(222, 385))
r(262, luck(), iff('!res', [st(E, -2)]))
for n, a, b in [(120, 305, 137), (138, 267, 216), (191, 370, 66), (306, 190, 55), (320, 267, 216),
                (388, 125, 22)]:
    r(n, skill(a, b))
r(96, ('GOLD0',), skill(267, 216))
r(158, skill(), iff('res', [gate(210, 'tukor'), gate(281, '!tukor'), ('HIDE', 377)], [only(377)]))
# 389: a próba csak akkor, ha a játékos a "Próba" menüpontot választja (a 88 választható nélküle is);
# sikertelen próba: -1 ÉLETERŐ, és vissza a 389-re (újra próbálhatja, vagy mehet a 88-ra)
r(389, ('ONCHOOSE', 26, skill() + [iff('!res', [st(E, -1)]), pick(26, 389)], 1))
# kockadobásos sebzés, tárgyvesztés
r(73, dmg(1))
r(357, dmg(1))
r(94, ('LOSEITEMS', 1))
r(264, st(E, -2), ('LOSEITEMS', 0))
# húslárvák: 1d6+6 lárva, 2d6-ot ölsz meg; a maradék mindegyike 1 ÉLETERŐ
r(143, ('XSET', 1, 6), ('XSUB', 2), ('PICKX', 271, 102))
r(271, ('DMGX',), ('XSUB', 2), ('PICKX', 63, 102))
r(63, ('DMGX',))
# Pestispatkányok raja
r(182, ('SWARM', 37), only(57))
# boltok
r(11, st(E, 4), ('SHOP', [('tisztanlatas', 5), ('vizlegzes', 5), ('zoldbor', 5)]))
r(196, ('SHOP', [('festmeny', 5)]))
r(329, ('SHOP', [('kreta', 1), ('fokhagyma', 1), ('ezusttor', 3), ('fakacsa', 2), ('disznofarok', 1),
                 ('borzolaj', 2), ('gyertya', 1), ('horog', 1), ('onsip', 1), ('gomba', 1)]))

# --- harcok
LB = 8
witch = [M('Kígyóboszorkány', 10, 6)]
r(12, st(SZ, 1), fight(witch, mdbl=1, hitlim=3), pick(352, 201))
r(57, fight(witch, mdbl=1, hitlim=3), pick(352, 201))
r(13, fight([M('Kardmester', 11, 6)], 152))
r(27, fight([M('Őrző Szellem', 8, 99)], ev=(EV_WIN_ROUND, 0)), luck(401, 263))
r(35, fight([M('Csontvázkirály', 9, 7)], 399, lb=1, pdmg=1))
r(45, fight([M('Első Csontváz', 6, 5), M('Második Csontváz', 5, 6)], 309))
r(49, fight([M('Sharcle', 8, 8)], 400, ev=(EV_WIN_N, 2)))
r(55, st(E, -3), fight([M('Óriáspók', 7, 8)], 21))
r(79, ('ONCHOOSE', 229, fight([M('Első Óriáspatkány', 5, 4), M('Második Óriáspatkány', 5, 3),
                               M('Harmadik Óriáspatkány', 5, 2)], all=1)))
r(80, fight([M('Ogre', 8, 10)], 319))
r(87, fight([M('Élősködőivadék', 10, 10)], 380, lb=1))
r(95, fight([M('Első Vámpírdenevér', 5, 4), M('Második Vámpírdenevér', 5, 4)], 241, ext=EXT_DRAIN))
r(97, fight([M('Alakváltoztató', 10, 10)], 60, skmod=-2))
r(99, st(E, -1), fight([M('Első Tolvaj', 6, 6), M('Második Tolvaj', 7, 5)], 382))
r(105, fight([M('Óriáspók', 7, 8)], 21))
r(107, fight([M('Vámpír', 10, 12)], ev=(EV_FLEE6, 6)), pick(116, 83))
r(111, fight([M('Uglukk Ork', 8, 8)], 285))
r(126, fight([M('Küklopsz', 9, 9)], 200))
dragon = [M('Fekete Sárkány', 14, 18)]
r(137, fight(dragon, 337, lb=1, ext=EXT_GAS))
r(269, fight(dragon, 337, lb=1, ext=EXT_GAS))
r(172, fight([M('Élősködőivadék', 10, 10)], 380, skmod=-3))
r(184, fight([M('Vörös Sárkány', 6, 6)], 391))
r(195, fight([M('Pokoldémon', 10, 10)], 232, pdmg=4, ext=EXT_KRIS))
r(223, fight([M('Zsoldos', 8, 10)], 147))
r(231, iff('sisak', [st(E, -1)], [st(E, -3)]),
       fight([M('Első Niblick', 4, 3), M('Második Niblick', 5, 2), M('Harmadik Niblick', 3, 4)], 295))
r(266, fight([M('Gigantusz', 12, 12)], 133, lb=1, mdmg=4))
wiz = [M('Gonosz Varázsló', 8, 8)]
r(267, fight(wiz, ev=(EV_LOSE_ROUND, 0)), pick(81, 113))
r(397, st(E, -1), fight(wiz, ev=(EV_LOSE_ROUND, 0)), pick(81, 113))
r(290, iff('kristor', [only(367)], fight([M('Óriás Homokhernyó', 8, 10)], 47)))
r(293, fight([M('Goblin', 5, 5)], 146))
r(310, fight([M('Első Zombi', 6, 6), M('Második Zombi', 6, 7), M('Harmadik Zombi', 5, 7),
              M('Negyedik Zombi', 5, 5)], 178))
r(313, fight([M('Uglukk Ork', 8, 9)], 161, ev=(EV_SURVIVE_N, 3)))
r(343, fight([M('Gremlin', 4, 3)], 395))
r(348, fight([M('Üvöltő Farkas', 7, 8)], 218))
r(359, fight([M('Két-fejű Troll', 8, 9)], 43))
r(360, fight([M('Littlebig', 8, 10)], ev=(EV_FIRST_ROUND, 0)), pick(261, 341))
r(362, fight([M('Ghoul', 8, 7)], hitlim=4), iff('res', [('DEATH',)], [only(155)]))

# ---------------------------------------------------------------- fordítás
OP = {'END': 0, 'STAT': 1, 'GOLD': 2, 'GOLD0': 3, 'GAIN': 4, 'LOSE': 5, 'GATE': 6, 'IF': 7, 'SKIP': 8,
      'LUCK': 9, 'SKILL': 10, 'PICK': 11, 'ONLY': 12, 'DMG': 13, 'FIGHT': 14, 'LOSEITEMS': 15,
      'KEYS': 16, 'SWARM': 17, 'XSET': 18, 'XSUB': 19, 'DMGX': 20, 'ADD': 21, 'HIDE': 22, 'SHOP': 23,
      'ONCHOOSE': 24, 'PICKX': 25, 'DEATH': 26}
C_KEY, C_RES, C_X, C_GOLD, C_VIS, C_REV = 64, 65, 66, 67, 68, 69

def cond(c):
    neg = 0
    if isinstance(c, tuple):
        if c[0] == 'vis': return [C_VIS] + w16(c[1])
        if c[0] == '!vis': return [C_VIS | 0x80] + w16(c[1])
        return [C_GOLD, c[1]]
    if c.startswith('!'):
        neg, c = 0x80, c[1:]
    v = {'key': C_KEY, 'res': C_RES, 'x': C_X, 'rev': C_REV}.get(c)
    if v is None: v = ITEM_ID[c]
    return [v | neg]

def w16(v): return [v & 255, v >> 8]

def compile_ops(ops, enc_str):
    """enc_str(s) -> font-index bájtok (0-val lezárva)"""
    out = []
    for o in ops:
        k = o[0]; out.append(OP[k])
        if k == 'STAT':   out += [o[1], o[2] & 255]
        elif k == 'GOLD': out += [o[1] & 255]
        elif k in ('GAIN', 'LOSE'): out += [ITEM_ID[o[1]]]
        elif k == 'GATE': out += w16(o[1]) + cond(o[2])
        elif k in ('PICK', 'PICKX'): out += w16(o[1]) + w16(o[2])
        elif k in ('ONLY', 'ADD', 'HIDE'): out += w16(o[1])
        elif k == 'DMG':  out += [o[1], o[2]]
        elif k == 'LOSEITEMS': out += [o[1]]
        elif k == 'SWARM': out += [o[1]]
        elif k == 'XSET': out += [o[1], o[2]]
        elif k == 'XSUB': out += [o[1]]
        elif k == 'SHOP':
            out += [len(o[1])]
            for it, price in o[1]: out += [ITEM_ID[it], price]
        elif k == 'IF':
            th = compile_ops(o[2], enc_str); el = compile_ops(o[3], enc_str)
            if el:
                th = th + [OP['SKIP'], len(el)]
            out += cond(o[1]) + [len(th)] + th + el
        elif k == 'ONCHOOSE':
            # a menüpont felirata: 0 = Harc, 1 = Próba; a törzs PICK/ONLY-ja felülírhatja a célt
            body = compile_ops(o[2], enc_str) + [0]
            out += w16(o[1]) + [o[3] if len(o) > 3 else 0, len(body)] + body
        elif k == 'FIGHT':
            mons, kw = o[1], o[2]
            flags = 0; extra = []
            if kw.get('all'): flags |= 1
            if kw.get('lb'): flags |= 2
            if kw.get('mdbl'): flags |= 4
            if 'hitlim' in kw: flags |= 8
            if 'pdmg' in kw or 'mdmg' in kw: flags |= 16
            if 'skmod' in kw: flags |= 32
            if 'ev' in kw: flags |= 64
            if 'ext' in kw: flags |= 128
            out += [len(mons), flags]
            if flags & 8: out += [kw['hitlim']]
            if flags & 16: out += [kw.get('pdmg', 2), kw.get('mdmg', 2)]
            if flags & 32: out += [kw['skmod'] & 255]
            if flags & 64: out += list(kw['ev'])
            if flags & 128: out += [kw['ext']]
            for name, sk, sta in mons:
                out += [sk, sta] + enc_str(name)
        assert all(0 <= b < 256 for b in out), (o, out)
    return out

def script(n, enc_str):
    """a fejezet bájtkódja (műveletek + 0), vagy None.
    Ismételt látogatáskor a nyereség (pozitív STAT/GOLD, GAIN) nem ismétlődik, a veszteség igen."""
    ops = R.get(n)
    if not ops: return None
    return compile_ops(ops, enc_str) + [0]

if __name__ == '__main__':
    import json, os
    here = os.path.dirname(os.path.abspath(__file__))
    doc = json.load(open(os.path.join(here, '..', 'tvc_text', 'sarkany_szeme.json'), encoding='utf-8'))
    secs = {s['id']: s for s in doc['sections']}
    tot = 0
    for n, ops in sorted(R.items()):
        b = script(n, lambda s: [1] * len(s) + [0])
        tot += len(b)
        # minden ONLY/PICK/GATE cél szerepel-e a fejezet célpontjai között
        def targets(l):
            for o in l:
                if o[0] in ('ONLY', 'GATE', 'HIDE'): yield o[1]
                if o[0] in ('PICK', 'PICKX'): yield o[1]; yield o[2]
                if o[0] == 'IF': yield from targets(o[2]); yield from targets(o[3])
                if o[0] == 'ONCHOOSE': yield o[1]; yield from targets(o[2])
        bad = [t for t in targets(ops) if t not in secs[n]['jumps'] and t != n]
        if bad: print('HIBA', n, bad, secs[n]['jumps'])
    fights = sum(1 for o in R.values() for x in o if x[0] == 'FIGHT' or (x[0] == 'IF' and any(y[0] == 'FIGHT' for y in x[3])) or (x[0] == 'ONCHOOSE'))
    print(len(R), 'fejezet szabállyal,', tot, 'bájt;', 'harc:', fights)
    mons_json = {s['id'] for s in doc['sections'] if s.get('monsters')}
    have = {n for n, o in R.items() if any(x[0] in ('FIGHT', 'ONCHOOSE') or (x[0] == 'IF' and any(y[0] == 'FIGHT' for y in x[3])) for x in o)}
    print('hiányzó harc:', sorted(mons_json - have), 'extra:', sorted(have - mons_json))
