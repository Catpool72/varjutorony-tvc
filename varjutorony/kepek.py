#!/usr/bin/env python3
"""
A Varjútorony ura – a könyv 72 képe: melyik fejezethez tartozik, mit ábrázol (leírás és angol prompt
egy másik képalkotó MI-nek), és egy egyszerű, programmal rajzolt változat (ideiglenes kép).

Futtatás:  python3 kepek.py           -> ill/p1..p72.png, img_sections.json, KEPEK.md, kepek_attekintes.png
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rajzkeszlet import Scene, W, H

K = []      # (fejezetnév, cím, leírás, prompt, rajzoló)
def kep(name, cim, leiras, prompt):
    def deco(f):
        K.append((name, cim, ' '.join(leiras.split()), ' '.join(prompt.split()), f)); return f
    return deco

STYLE = ('black ink illustration on white paper, classic 1980s fantasy gamebook style, bold cross-hatching, '
         'high contrast, no grey wash, portrait 5:8')

# =================================================================== Fenyvesvölgy
@kep('kezdet', 'Bodor a kútnál', '''Fenyvesvölgy kihalt főtere este: bedeszkázott ablakok, középen kút, mellette egy ősz
szakállú öregember (Bodor) erszényt nyújt a nézőnek. A háztetőkön és a kút káváján varjak ülnek.''',
'''Deserted village square at dusk, boarded-up windows, an old bearded village elder by a stone well holding out a
small purse towards the viewer, crows perched on roofs and on the well.''')
def _(s):
    s.sky(30, 90, 300); s.glow(150, 260, 140, 110, 60)
    for x, w, h in [(30, 70, 120), (110, 60, 90), (190, 80, 130), (270, 70, 100)]: s.house(x, 300, w, h, 14, 0)
    s.ground(300, 30, 2)
    s.well(110, 400, 1.1, 70)
    s.person(200, 430, 150, 6, cloak=True, beard=True, staff=True)
    s.d.ellipse([168, 345, 182, 360], fill=200)
    for x, y in [(30, 170), (120, 205), (200, 160), (90, 312), (128, 312)]: s.crow(x, y, 8, 4, perched=True)
    s.crows(4, y1=120)

@kep('fogado', 'A Részeg Kecske', '''A fogadó füstös ivója: kandalló, gerendákról lógó sonkák, a pult mögött egy erős
fogadósné, egy asztalnál kockázó szekeresek, a sarokban egy csuklyás idegen.''',
'''Smoky medieval tavern interior, fireplace, hams hanging from beams, a sturdy innkeeper woman behind the bar,
carters playing dice at a table, a hooded stranger sitting alone in the corner.''')
def _(s):
    s.im.paste(40, [0, 0, W, H]); s.bricks(0, 0, W, 300, None, 55)
    s.d.rectangle([0, 0, W, 20], fill=15); s.d.rectangle([0, 60, W, 70], fill=15)
    for x in (40, 90, 140, 200, 250): s.d.polygon([(x, 70), (x - 8, 100), (x + 8, 100)], fill=15)
    s.fire(230, 300, 1.0); s.d.rectangle([180, 220, 290, 240], fill=20)
    s.floor(330, 30, 45)
    s.d.rectangle([20, 260, 140, 330], fill=18); s.person(70, 260, 110, 10, cloak=True)
    s.d.rectangle([110, 380, 230, 395], fill=15)
    s.person(130, 400, 120, 8, cloak=False, hat=True); s.person(215, 405, 125, 8, cloak=False)
    s.person(40, 470, 150, 4, hood=True, eyes=230)

@kep('kovacs', 'A kovácsműhely', '''Kovácsműhely: izzó kohó, üllő, egy vállas kovács kalapáccsal, a falon kötél, lámpás,
patkók, az asztalon egy ezüsttőr.''',
'''Village smithy, glowing forge, broad-shouldered blacksmith with a hammer at the anvil, rope, lantern and
horseshoes hanging on the wall, a silver dagger on the table.''')
def _(s):
    s.im.paste(25, [0, 0, W, H]); s.bricks(0, 0, W, 330, None, 40)
    s.fire(220, 320, 1.4)
    s.d.rectangle([160, 330, 290, 360], fill=30)
    s.d.polygon([(60, 360), (140, 360), (120, 380), (80, 380)], fill=8); s.d.rectangle([90, 380, 110, 430], fill=8)
    s.person(120, 450, 190, 4, cloak=False, sword=False, arms_up=True)
    s.d.rectangle([140, 210, 165, 225], fill=4)
    s.d.ellipse([20, 80, 80, 140], outline=150, width=4)
    for x in (110, 135, 160): s.d.arc([x, 80, x + 20, 105], 0, 180, fill=150, width=4)
    s.d.line([(30, 420), (90, 418)], fill=220, width=3); s.ground(450, 15, 1)

@kep('fuvesno', 'Gyopár néni kunyhója', '''Füvesasszony kunyhója belülről: a mennyezetről szárított füvek csokrai lógnak,
a tűzhelyen bogrács gőzölög, egy kendős öregasszony üvegcsét nyújt át.''',
'''Herb-woman's cottage interior, bundles of dried herbs hanging from the ceiling, a cauldron steaming on the hearth,
an old woman in a headscarf handing over a small glass vial.''')
def _(s):
    s.im.paste(30, [0, 0, W, H])
    for x in range(10, W, 28):
        h = s.r.randrange(40, 90); s.d.line([(x, 0), (x, 20)], fill=120)
        s.d.polygon([(x - 10, 20), (x + 10, 20), (x + 3, 20 + h), (x - 3, 20 + h)], fill=s.r.choice([90, 120, 150]))
    s.fire(80, 360, 0.9); s.d.ellipse([45, 290, 115, 340], fill=12)
    for i in range(4): s.glow(80 + i * 6, 260 - i * 30, 18, 120, 10)
    s.floor(380, 25, 35)
    s.person(200, 460, 210, 6, cloak=True, hood=True, bent=True)
    s.flask(140, 300, 0.9, 220)

@kep('kapolna_f', 'A kifosztott kápolna', '''A falu kápolnája: üres fülke az oltár mögött, betört ablak, a padlón fekete
varjútollak, egy fiatal pap térdel az oltár előtt.''',
'''Small village chapel interior, an empty niche behind the altar where a gem was kept, a broken window,
black crow feathers on the floor, a young priest kneeling in prayer.''')
def _(s):
    s.im.paste(25, [0, 0, W, H])
    s.arch(110, 190, 60, 250, 70); s.arch(125, 175, 90, 230, 15)
    s.lightpoly([(200, 40), (270, 40), (230, 330), (150, 330)], 110, 10, 160)
    s.arch(210, 260, 30, 140, 160)
    for i in range(6): s.d.line([(220 + i * 7, 40 + i * 9), (240 - i * 4, 60 + i * 12)], fill=20, width=2)
    s.d.rectangle([90, 250, 210, 300], fill=60); s.floor(300, 30, 40)
    s.person(150, 400, 110, 6, cloak=True)
    for _ in range(14):
        x, y = s.r.randrange(30, 280), s.r.randrange(320, 470)
        s.d.polygon([(x, y), (x + 14, y - 4), (x + 2, y + 3)], fill=5)

@kep('harang_fent', 'A harangláb tetején', '''A harangláb tetején a hős egy hatalmas, vörös szemű varjúval harcol; a
háttérben a völgy, a láp ködje, a hegyek, és messze a Varjútorony.''',
'''Top of a wooden bell tower, a hero fighting a huge crow with glowing red eyes, wide valley below with fog over
a marsh, snowy mountains, and a dark tower far away on the horizon.''')
def _(s):
    s.sky(40, 120, 300); s.hills(300, 50, 60); s.fog(300, 20, 140, 120); s.hills(340, 40, 35)
    s.tower(240, 290, 10, 60, 20, 0)
    s.d.rectangle([20, 330, 280, 345], fill=10); s.d.line([(30, 345), (30, H)], fill=10, width=8); s.d.line([(270, 345), (270, H)], fill=10, width=8)
    s.d.chord([110, 340, 190, 420], 180, 360, fill=12); s.d.rectangle([110, 380, 190, 400], fill=12)
    s.person(90, 330, 130, 4, sword=True, cloak=True)
    s.eagle(190, 170, 30, 4, up=True); s.glow(190, 155, 8, 255, 4)

@kep('molnar', 'Gáspár, a molnár', '''Egy félvak öreg molnár lisztes kötényben a konyhájában; a tűzhely fölött egy fiatal
legény rajza, a legény vállán varjú.''',
'''A half-blind old miller in a floury apron in his kitchen; above the hearth hangs a charcoal drawing of a young
man with a crow on his shoulder.''')
def _(s):
    s.im.paste(30, [0, 0, W, H]); s.bricks(0, 0, W, 330, None, 48)
    s.d.rectangle([90, 70, 210, 210], fill=200); s.d.rectangle([90, 70, 210, 210], outline=20, width=4)
    s.person(150, 205, 110, 30, cloak=False); s.crow(170, 135, 8, 30, perched=True)
    s.fire(150, 320, 1.0); s.floor(340, 28, 38)
    s.person(80, 470, 220, 6, cloak=True, beard=True, bent=True)

@kep('temeto_virraszt', 'Éjfél a temetőben', '''Holdfényes temető, kidőlt keresztek, a feltúrt sírokból két élőhalott
tápászkodik fel; egy öreg sírásó lapáttal, mellette a hős.''',
'''Moonlit village graveyard, toppled crosses, two rotting dead men climbing out of freshly dug graves, an old
gravedigger raising his shovel beside the hero.''')
def _(s):
    s.sky(10, 50, 300); s.moon(220, 80, 40); s.stars(30, 200)
    for x in (30, 260): s.deadtree(x, 330, 150, 8)
    s.ground(320, 20, 4)
    for x, y in [(70, 360), (150, 345), (230, 370)]:
        s.d.line([(x, y), (x, y - 40)], fill=70, width=5); s.d.line([(x - 14, y - 28), (x + 14, y - 28)], fill=70, width=5)
    s.d.ellipse([100, 400, 200, 430], fill=8)
    s.person(130, 430, 100, 60, cloak=False, arms_up=True); s.person(180, 425, 90, 60, cloak=False, arms_up=True)
    s.person(45, 470, 150, 4, cloak=True, sword=True); s.person(260, 470, 140, 4, beard=True, staff=True)

@kep('kapu', 'Az északi kapu', '''Fenyvesvölgy fa palánkkapuja, egy ijedt fiatal őr lándzsával; a kapu fölött fakereszt és
egy odaszögezett varjú, a kapun túl a sötét fenyőerdő.''',
'''Wooden palisade gate of a mountain village, a frightened young guard with a spear, a wooden cross and a nailed
crow above the gate, dark pine forest beyond.''')
def _(s):
    s.sky(40, 100, 250); s.forest(250, 14, 80, 160, 12)
    s.ground(380, 30, 3)
    for x in range(0, W, 22): s.d.polygon([(x, 380), (x, 150), (x + 10, 135), (x + 20, 150), (x + 20, 380)], fill=10)
    s.d.rectangle([90, 180, 210, 380], fill=60); s.forest(380, 4, 60, 120, 20, 95, 205)
    s.d.line([(150, 110), (150, 175)], fill=10, width=5); s.d.line([(132, 128), (168, 128)], fill=10, width=5)
    s.crow(185, 150, 8, 4, perched=True)
    s.person(60, 470, 160, 4, cloak=False, staff=True, hat=False)

# =================================================================== Feketeerdő
@kep('erdo', 'A vörös szemű farkas', '''Fenyőerdei út, az út közepén hatalmas szürke farkas izzó vörös szemmel, lopakodva
közelít.''', '''Narrow path through a dark pine forest, a huge grey wolf with glowing red eyes stalking towards the viewer.''')
def _(s):
    s.sky(60, 110, 300); s.forest(260, 10, 120, 220, 10)
    s.d.polygon([(110, 300), (190, 300), (290, H), (10, H)], fill=60); s.forest(330, 5, 150, 260, 6, 0, 80); s.forest(330, 5, 150, 260, 6, 230, W)
    s.wolf(150, 420, 50, 5, 255, -1)

@kep('erdo_ut2', 'Rablók a gázlónál', '''Erdei patak gázlója, három rongyos rabló ugrik elő a bokrokból rozsdás kardokkal; a
vezérük fél fülű, vigyorog.''', '''Forest stream ford, three ragged bandits jumping out of the bushes with rusty swords, their one-eared
leader grinning.''')
def _(s):
    s.sky(70, 120, 240); s.forest(240, 12, 90, 170, 14)
    s.water(330, 40, 400, 50, 140); s.ground(400, 18, 4)
    s.person(80, 440, 190, 4, sword=True, hat=True); s.person(170, 420, 160, 6, sword=True); s.person(245, 430, 150, 8, sword=True, cloak=False)
    s.reeds(0, 60, 380, 15, 6, 90)

@kep('vadasz', 'A sebesült vadász', '''Vadászkunyhó előtt egy idős vadász ül bekötött, véres karral, a lábánál öreg
vadászkutya; a falon prémek száradnak.''', '''An old hunter with a bloody bandaged arm sitting in front of his log cabin, an old hound at
his feet, furs drying on the wall.''')
def _(s):
    s.sky(80, 130, 250); s.forest(250, 8, 100, 180, 20)
    s.house(160, 330, 220, 150, 20, 150); s.ground(330, 40, 2)
    for x in (80, 230): s.d.rectangle([x - 18, 210, x + 18, 260], fill=90)
    s.person(130, 450, 170, 6, cloak=True, beard=True); s.d.ellipse([150, 360, 175, 385], fill=230)
    s.wolf(220, 460, 26, 6, 0, -1)

@kep('farkasvezer', 'Vörösszem, a falka vezére', '''Bűzös barlang mélye csontokkal, egy borjúnyi szürke farkas vörös
szemmel, a vállán fekete varjú ül.''', '''Deep foul cave strewn with bones, a calf-sized grey wolf with burning red eyes, a black crow
perched on its shoulder.''')
def _(s):
    s.im.paste(10, [0, 0, W, H]); s.glow(150, 300, 160, 70, 60)
    s.d.chord([-60, 40, 360, 600], 180, 360, fill=None, outline=40, width=20)
    s.wolf(150, 400, 70, 4, 255, 1); s.crow(120, 330, 12, 4, perched=True)
    for _ in range(20):
        x, y = s.r.randrange(W), s.r.randrange(420, H)
        s.d.line([(x, y), (x + s.r.randrange(-20, 20), y + s.r.randrange(-6, 6))], fill=170, width=3)

@kep('favago', 'A fa alá szorult favágó', '''Erdei tisztás, egy kidőlt fenyőtörzs alá szorult favágó segítségért nyúl;
mellette fejsze áll a tönkbe vágva.''', '''Forest clearing, a woodcutter pinned under a fallen pine trunk reaching out for help, an axe stuck
in a stump nearby.''')
def _(s):
    s.sky(90, 150, 260); s.forest(260, 12, 90, 180, 25)
    s.ground(330, 60, 3)
    s.d.polygon([(0, 360), (300, 300), (300, 330), (0, 395)], fill=10)
    s.person(170, 380, 120, 6, cloak=False, arms_up=True)
    s.d.rectangle([40, 420, 90, 470], fill=20); s.d.line([(60, 420), (80, 380)], fill=20, width=4); s.d.polygon([(72, 385), (95, 372), (90, 395)], fill=20)

@kep('tunderkor', 'A tündérkör', '''Holdfényes tisztás, gombák tökéletes körben, a kör közepén apró, áttetsző szárnyú tündérek
táncolnak a hős körül.''', '''Moonlit glade, mushrooms in a perfect fairy ring, tiny translucent-winged fairies dancing around the hero
in the middle.''')
def _(s):
    s.sky(15, 50, 300); s.forest(270, 12, 120, 230, 6); s.ground(320, 25, 1)
    s.glow(150, 380, 120, 120, 50)
    for k in range(18):
        a = k / 18 * 2 * math.pi; x, y = 150 + 120 * math.cos(a), 390 + 40 * math.sin(a)
        s.d.chord([x - 8, y - 10, x + 8, y + 2], 180, 360, fill=220); s.d.rectangle([x - 2, y - 4, x + 2, y + 4], fill=200)
    s.person(150, 400, 110, 4, cloak=True)
    for k in range(9):
        a = k / 9 * 2 * math.pi; x, y = 150 + 70 * math.cos(a), 320 + 50 * math.sin(a)
        s.glow(x, y, 10, 250, 5); s.d.ellipse([x - 7, y - 4, x - 1, y + 2], fill=200); s.d.ellipse([x + 1, y - 4, x + 7, y + 2], fill=200)

@kep('borcsa', 'Varga Borcsa', '''Egy vén tölgy gyökerei közé épült mohos kunyhó, zöld füstöt eregető kémény; az ajtóban
egy görbe hátú, hosszú orrú boszorkány, a vállán fekete macska.''', '''Mossy hut built into the roots of an ancient oak, chimney puffing green smoke; a hunchbacked witch with a
long nose in the doorway, a black cat on her shoulder.''')
def _(s):
    s.sky(40, 80, 300); s.deadtree(150, 300, 260, 14, 30)
    for i in range(5): s.glow(220 + i * 8, 90 - i * 18, 18 + i * 3, 100, 10)
    s.house(150, 360, 180, 120, 20, 140); s.ground(360, 30, 3)
    s.d.rectangle([125, 270, 175, 360], fill=120)
    s.person(150, 360, 100, 4, hat=True, bent=True, staff=True)
    s.d.ellipse([160, 268, 176, 282], fill=4); s.d.polygon([(162, 270), (165, 262), (168, 270)], fill=4)

@kep('kokereszt', 'A kőkereszt', '''Dombtetőn mohos kőkereszt, mellette apró fehér kápolnácska; két út indul: az egyik
a ködös láp, a másik a havas hágó felé, a messzeségben a torony.''', '''A mossy stone cross on a hilltop beside a tiny white wayside chapel; one road leads down into a foggy
marsh, the other up into snowy mountains; a distant dark tower.''')
def _(s):
    s.sky(60, 140, 300); s.hills(240, 60, 90, 2); s.fog(280, 30, 170, 150)
    s.tower(150, 230, 8, 50, 30, 0)
    s.hills(330, 40, 30, 1)
    s.d.line([(110, 330), (0, 420)], fill=110, width=12); s.d.line([(180, 330), (300, 400)], fill=110, width=12)
    s.d.rectangle([70, 240, 86, 340], fill=10); s.d.rectangle([50, 265, 106, 280], fill=10)
    s.chapel(220, 340, 70, 60, 200, 30)

@kep('elagazas', 'Bence üzenete', '''Közeli kép a kőkereszt tövéről: friss vadvirágcsokor, mellette egy kőhöz szorított,
szénnel írt cédula egy kisfiú kerek betűivel.''', '''Close-up at the foot of a stone cross: a fresh bunch of wildflowers and a charcoal-written note
held down by a stone, in a child's round handwriting.''')
def _(s):
    s.im.paste(70, [0, 0, W, H]); s.d.rectangle([90, 0, 210, 330], fill=110); s.bricks(90, 0, 210, 330, None, 80, 30, 24)
    s.ground(330, 40, 4)
    s.d.polygon([(60, 360), (240, 340), (250, 440), (70, 460)], fill=230)
    for k in range(5): s.d.line([(85, 375 + k * 15), (225 - s.r.randrange(30), 365 + k * 15)], fill=40, width=3)
    for k in range(8):
        x = 180 + s.r.randrange(-40, 40); y = 320 + s.r.randrange(-20, 20)
        s.d.line([(200, 360), (x, y)], fill=20, width=2); s.d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=s.r.choice([180, 220, 250]))

# =================================================================== Suttogó-láp
@kep('lap1', 'A Suttogó-láp', '''Ködös láp: korhadt pallósor vezet be a ködbe, nád és elszáradt fa, a távolban kék lidércfény
imbolyog; egy cölöpön tábla.''', '''Foggy marsh, a rotten boardwalk leading into the mist, reeds and a dead tree, a blue will-o'-the-wisp
hovering in the distance, a wooden sign on a post.''')
def _(s):
    s.sky(30, 90, 250)
    for i in range(6): s.fog(170 + i * 24, 12, 130, 70)
    s.water(270, 18, H, 50, 70)
    for i in range(16):
        t = i / 15; y = H - 10 - t * 190; w = 80 - t * 66; x = 150 - t * 10
        s.d.rectangle([x - w / 2, y - 6 + t * 4, x + w / 2, y], fill=int(130 - t * 70))
    s.reeds(0, 80, 300, 40); s.reeds(230, W, 300, 40); s.deadtree(255, 330, 170)
    s.d.line([(60, 420), (60, 330)], fill=10, width=6); s.d.rectangle([30, 320, 110, 345], fill=150)
    s.glow(90, 220, 34, 230, 16); s.d.ellipse([84, 214, 96, 226], fill=255)

@kep('liderc', 'A lidércfény', '''Közelről a lidércfény: egy ember magasságában lebegő kék fénygömb, benne egy áttetsző,
nevető arc; a hős süppedő talajon követi.''', '''Close-up of a will-o'-the-wisp: a floating ball of cold light with a faint laughing face in it, the
hero following it across sinking ground.''')
def _(s):
    s.sky(15, 40, 300); s.fog(250, 40, 80, 120); s.water(330, 14, H, 30, 40)
    s.glow(170, 200, 70, 230, 30); s.d.ellipse([150, 180, 190, 220], fill=255)
    s.d.arc([160, 195, 180, 210], 20, 160, fill=40, width=2); s.d.ellipse([160, 190, 166, 196], fill=40); s.d.ellipse([174, 190, 180, 196], fill=40)
    s.reeds(0, W, 330, 25, 6, 80)
    s.person(80, 460, 160, 4, cloak=True)

@kep('lap_sziget', 'A fűzfás sziget', '''Kis füves sziget a láp közepén, egy öreg fűzfa, a törzsébe vésett nyilakkal;
a ködből egy templomtorony csúcsa emelkedik ki a vízből.''', '''A small grassy islet in the marsh with an old willow tree, arrows carved into its trunk; the top of a
church steeple rises from the water in the misty distance.''')
def _(s):
    s.sky(50, 120, 280); s.fog(230, 30, 150, 140)
    s.chapel(230, 270, 30, 50, 40, 0); s.water(270, 30, H, 40, 90)
    s.d.ellipse([20, 330, 280, 430], fill=40)
    s.d.line([(150, 380), (140, 200)], fill=10, width=18)
    for k in range(26):
        x = 140 + s.r.randrange(-110, 110); y = 190 + s.r.randrange(-40, 30)
        s.d.line([(140, 200), (x, y)], fill=10, width=3); s.d.line([(x, y), (x + s.r.randrange(-6, 6), y + s.r.randrange(60, 140))], fill=10, width=2)
    for k in range(3): s.d.polygon([(130, 270 + k * 25), (155, 262 + k * 25), (155, 278 + k * 25)], fill=200)

@kep('bekak', 'A békák királynője', '''Kerek tó a nád között, a közepén egy tavirózsalevélen borjúnyi koronás béka ül; a parton
egy szürke gém egy kis békára készül lecsapni.''', '''A round pond among reeds; a calf-sized frog wearing a golden crown sits on a lily pad in the middle; a grey
heron on the bank is about to strike a little frog.''')
def _(s):
    s.sky(60, 130, 250); s.reeds(0, W, 230, 60, 15, 120)
    s.water(270, 40, H, 60, 120)
    s.d.ellipse([60, 360, 240, 400], fill=110); s.frog(150, 380, 60, 8, crown=True)
    s.d.line([(250, 470), (255, 380)], fill=6, width=3); s.d.line([(262, 470), (258, 380)], fill=6, width=3)
    s.d.ellipse([235, 330, 280, 385], fill=6); s.d.line([(265, 335), (270, 280)], fill=6, width=5)
    s.d.ellipse([255, 268, 280, 288], fill=6); s.d.polygon([(258, 280), (215, 300), (258, 286)], fill=6)
    s.frog(215, 455, 14, 10)

@kep('revesz', 'Csobán, a révész', '''Cölöpökre épült kunyhó a láp szélén, előtte lapos fenekű csónak; a stégen egy
szakállas, horgas orrú öreg révész pipázik.''', '''A hut on stilts at the edge of the marsh, a flat-bottomed boat tied up in front; a bearded hook-nosed old
ferryman smoking a pipe on the jetty.''')
def _(s):
    s.sky(50, 110, 280); s.fog(240, 30, 130, 120); s.water(300, 20, H, 50, 80)
    s.house(200, 260, 130, 90, 12, 160)
    for x in (145, 175, 225, 255): s.d.line([(x, 260), (x, 330)], fill=12, width=6)
    s.d.rectangle([40, 330, 240, 342], fill=50)
    s.d.polygon([(20, 400), (260, 400), (230, 430), (50, 430)], fill=10)
    s.person(110, 330, 130, 4, beard=True, hat=True)
    for i in range(4): s.glow(140 + i * 6, 235 - i * 14, 8, 160, 5)

@kep('atkeles', 'A lápi troll', '''Csónak a fekete vízen a ködben, egy hatalmas, mohos lápi troll a csónak peremébe
kapaszkodik; a révész evezővel, a hős karddal.''', '''A rowing boat on black water in thick fog, a huge mossy swamp troll grabbing the side of the boat; the
ferryman with an oar, the hero with a sword.''')
def _(s):
    s.sky(70, 130, H); s.fog(200, 50, 150, 130)
    s.water(320, 30, H, 60, 90)
    s.troll(180, 380, 55, 6, 240)
    s.d.polygon([(0, 390), (240, 390), (200, 440), (20, 440)], fill=12)
    s.person(70, 400, 130, 4, sword=True); s.person(150, 400, 110, 4, beard=True, staff=True)

@kep('troll_hid', 'A troll hídja', '''Ősi, mohos kőhíd a patak fölött, a pillérei közötti üregből egy hatalmas troll mászik elő
bunkóval; a hős a híd közepén.''', '''An ancient mossy stone bridge over a stream; a huge troll with a club climbs out of the hollow between the
piers; the hero stands in the middle of the bridge.''')
def _(s):
    s.sky(60, 120, 280); s.fog(230, 30, 130, 110)
    s.water(330, 25, H, 40, 90)
    s.d.rectangle([0, 250, W, 280], fill=60); s.d.chord([60, 260, 240, 420], 180, 360, fill=30)
    s.d.rectangle([0, 280, 60, 360], fill=60); s.d.rectangle([240, 280, W, 360], fill=60)
    s.person(150, 252, 90, 4, sword=True)
    s.troll(150, 400, 45, 6, 240); s.d.line([(210, 360), (250, 300)], fill=6, width=12)

@kep('malom', 'A romos vízimalom', '''A Fekete-patak partján romos vízimalom, a mohos kerék még forog, vízfüggöny zuhog a mély
malomgödörbe; a háttérben a torony.''', '''A ruined watermill on the bank of a dark stream, its mossy wheel still turning, a curtain of water pouring
into a deep pit; the dark tower in the background.''')
def _(s):
    s.sky(60, 130, 260); s.tower(240, 210, 22, 110, 25, 0, broken=True)
    s.house(110, 330, 160, 130, 15, 0); s.d.polygon([(40, 200), (80, 160), (110, 210)], fill=60)
    s.d.ellipse([170, 230, 290, 350], outline=10, width=10)
    for k in range(8):
        a = k * math.pi / 4; s.d.line([(230, 290), (230 + 60 * math.cos(a), 290 + 60 * math.sin(a))], fill=10, width=5)
    s.lightpoly([(175, 330), (285, 330), (290, H), (170, H)], 190, 6, 200)
    s.water(400, 20, H, 30, 120); s.ground(330, 18, 3, 400)

@kep('sullyedt', 'Az elsüllyedt falu', '''Ködből előbukkanó, vízbe süllyedt falu: kiálló háztetők, kémények varjakkal, középen
templomtorony; a hős derékig a vízben.''', '''A drowned village emerging from fog: rooftops and chimneys sticking out of the water with crows on them, a church
tower in the middle; the hero wading waist-deep.''')
def _(s):
    s.sky(40, 110, 260); s.fog(220, 40, 140, 130)
    s.chapel(150, 330, 60, 120, 20, 120)
    for x, h in [(40, 40), (90, 25), (220, 35), (270, 30)]: s.house(x, 330, 50, h, 15, 0)
    s.water(300, 25, H, 70, 100)
    for x in (40, 222, 270): s.crow(x, 270, 7, 4, perched=True)
    s.person(80, 470, 120, 4, sword=True)
    s.d.rectangle([0, 420, 140, H], fill=25)

@kep('sullyedt_templom', 'A vízbefúlt lelkek', '''Derékig vízzel elárasztott templombelső, úszó padok, megfakult freskók;
sápadt, kékes, üres szemű kísértetek lebegnek a hős felé.''', '''Flooded church interior, water waist-deep, floating pews, faded frescoes; pale glowing ghosts with empty eyes
drifting towards the hero.''')
def _(s):
    s.im.paste(20, [0, 0, W, H])
    for x in (20, 220): s.arch(x, x + 60, 40, 320, 35)
    s.arch(110, 190, 60, 300, 50)
    s.water(300, 30, H, 50, 70)
    for x, y, h in [(90, 330, 140), (160, 320, 160), (230, 340, 130)]: s.ghost(x, y, h, 190)
    s.person(150, 470, 120, 4, sword=True)

@kep('banya', 'A lápi banya', '''Cölöpös kunyhó a Holt Fák szigetén, csupasz fehér fák; az ajtóban egy ránctól barázdált
vén asszony hínárszerű hajjal, előtte ezüstös holdvirág nyílik.''', '''A stilted hut on an island of dead white trees; in the doorway a wrinkled old hag with seaweed-like hair;
a silvery moon-flower blooms in front of the hut.''')
def _(s):
    s.sky(20, 60, 300); s.fog(260, 30, 90, 110)
    for x in (40, 250, 280): s.deadtree(x, 340, 200, 150, 6)
    s.house(150, 300, 140, 100, 15, 0)
    for x in (95, 150, 205): s.d.line([(x, 300), (x, 360)], fill=15, width=6)
    s.water(350, 15, H, 30, 60)
    s.d.rectangle([128, 220, 172, 300], fill=90); s.person(150, 300, 80, 4, bent=True)
    s.glow(80, 400, 24, 240, 10)
    for k in range(6):
        a = k * math.pi / 3; s.d.ellipse([80 + 10 * math.cos(a) - 7, 400 + 10 * math.sin(a) - 7, 80 + 10 * math.cos(a) + 7, 400 + 10 * math.sin(a) + 7], fill=255)

# =================================================================== Kőkapu-hágó
@kep('hago1', 'A Kőkapu', '''Szűk sziklaszoros, két hatalmas sziklaoszlop kapuként áll egymással szemben, rúnákkal és egy
faragott törpfejjel; mögülük vékony füst száll fel.''', '''A narrow mountain pass where two huge rock pillars stand like a gate, carved with runes and a dwarf's face;
thin smoke rising behind them.''')
def _(s):
    s.sky(80, 160, 300); s.hills(200, 60, 120, 2)
    for i in range(4): s.glow(150 + i * 4, 170 - i * 25, 16, 160, 10)
    s.d.polygon([(20, H), (40, 120), (110, 100), (120, H)], fill=15); s.d.polygon([(180, H), (190, 110), (260, 125), (280, H)], fill=15)
    s.d.ellipse([55, 180, 95, 220], outline=120, width=3); s.d.polygon([(60, 210), (90, 210), (75, 245)], fill=120)
    for k in range(6): s.d.line([(200, 160 + k * 22), (215, 170 + k * 22)], fill=120, width=3)
    s.ground(400, 40, 4); s.person(150, 470, 110, 4, sword=True)

@kep('kobold_les', 'A koboldtábor', '''Sziklák közti mélyedés, tábortűz körül hegyes fülű, szürke koboldok lándzsákkal,
egy tollas sisakos kövér vezér; a tábor szélén fakalitka, benne egy megkötözött törp.''', '''A hollow among rocks, grey pointy-eared goblins with spears around a campfire, a fat leader in a feathered
helmet; at the edge of the camp a wooden cage holding a tied-up dwarf.''')
def _(s):
    s.sky(20, 50, 250); s.rocks(260, 10, 25, 70); s.ground(300, 30, 6)
    s.fire(150, 380, 1.0)
    for x in (70, 110, 200, 240): s.person(x, 400, 70, 4, cloak=False, staff=True)
    s.person(150, 430, 85, 4, hat=True)
    s.d.rectangle([220, 280, 290, 360], outline=60, width=4); s.bars(220, 290, 280, 360, 60, 14, 3)
    s.person(255, 355, 55, 30, beard=True)

@kep('torp_szabad', 'Dömötör, a törp', '''Zömök törp kőfaragó fonott, ezüstkarikás szakállal, kinyújtóztatja magát a kinyitott
kalitka mellett, a kezében egy éles acélvéső.''', '''A stocky dwarf stonecarver with a braided beard decorated with silver rings, stretching beside an opened
cage, holding a sharp steel chisel.''')
def _(s):
    s.sky(70, 140, 300); s.rocks(300, 10, 40, 80); s.ground(330, 50, 4)
    s.d.rectangle([20, 230, 110, 340], outline=20, width=5); s.d.line([(110, 230), (150, 250)], fill=20, width=5)
    s.person(190, 440, 150, 6, beard=True, cloak=False, arms_up=True)
    s.d.line([(235, 290), (255, 270)], fill=230, width=4)

@kep('remete', 'Ambrus, a remete', '''Sziklapárkányon nyíló barlang szája, kis tűz mellett ősz, hosszú szakállú öregember
kopott szerzetesi csuhában; mögötte fakereszt és könyvek.''', '''Mouth of a cave on a rocky ledge, a white-bearded old hermit in a worn monk's habit sitting by a small fire,
a wooden cross and a few books behind him.''')
def _(s):
    s.im.paste(15, [0, 0, W, H]); s.d.chord([-40, 40, 340, 700], 180, 360, fill=40)
    s.d.chord([20, 120, 280, 640], 180, 360, fill=15)
    s.fire(170, 400, 0.9)
    s.person(90, 420, 150, 6, hood=True, beard=True)
    s.d.line([(240, 220), (240, 300)], fill=90, width=5); s.d.line([(225, 240), (255, 240)], fill=90, width=5)

@kep('banya_csarnok', 'A törpkirályok csarnoka', '''Föld alatti csarnok faragott törpkirály-oszlopokkal, ezüsterek a
falakon; középen kőasztal mögött vén törp kereskedő gyertyafényben; a háttérben kőajtó és egy mozdulatlan kőóriás.''',
'''Underground hall with pillars carved as dwarf kings, silver veins glittering in the walls; an old dwarf merchant
behind a stone table by candlelight; a stone door and a motionless stone giant in the background.''')
def _(s):
    s.im.paste(10, [0, 0, W, H]); s.glow(150, 300, 150, 60, 60)
    for x in (30, 270):
        s.d.rectangle([x - 18, 40, x + 18, 400], fill=50); s.d.ellipse([x - 16, 60, x + 16, 92], fill=70)
    s.d.rectangle([110, 120, 190, 300], fill=35); s.troll(150, 300, 32, 60, 200)
    for _ in range(20): s.d.line([(s.r.randrange(W), s.r.randrange(300)), (s.r.randrange(W), s.r.randrange(300))], fill=110, width=1)
    s.floor(360, 20, 30)
    s.d.rectangle([90, 380, 210, 420], fill=60); s.glow(180, 370, 20, 240, 8)
    s.person(130, 390, 70, 6, beard=True)

@kep('koorias', 'A kőóriás', '''Háromszor emberméretű kőóriás repedezett, mohos testtel, izzó kristályszemmel áll egy
hatalmas kőajtó előtt; a hős kicsinek tűnik előtte.''', '''A stone giant three times human height, cracked and mossy, with glowing crystal eyes, guarding a huge stone
door; the hero looks tiny before it.''')
def _(s):
    s.im.paste(15, [0, 0, W, H]); s.d.rectangle([40, 40, 260, 420], fill=35); s.bricks(40, 40, 260, 420, None, 50, 60, 40)
    s.troll(150, 430, 80, 10, 255)
    s.floor(430, 20, 30); s.person(60, 475, 80, 4, sword=True, lantern=True)

@kep('kiralysir', 'A napkő', '''Törpkirályok sírkamrája csillagos, kristályos mennyezettel, kőkoporsók kőkoronákkal; egy
nyitott ládikában tojásnyi, napként izzó kő.''', '''Tomb chamber of dwarf kings with a starry crystal-studded ceiling, stone coffins with stone crowns; in an open
casket an egg-sized stone glowing like the sun.''')
def _(s):
    s.im.paste(10, [0, 0, W, H]); s.stars(70, 200)
    for x in (60, 240): s.d.rectangle([x - 40, 280, x + 40, 340], fill=40)
    s.floor(340, 18, 26)
    s.glow(150, 380, 90, 200, 35)
    s.d.rectangle([115, 380, 185, 420], fill=60); s.d.ellipse([135, 355, 165, 385], fill=255)
    for a in range(0, 360, 30):
        c, n = math.cos(math.radians(a)), math.sin(math.radians(a))
        s.d.line([(150 + 22 * c, 370 + 22 * n), (150 + 50 * c, 370 + 50 * n)], fill=255, width=2)

@kep('sasberc', 'A sasfészek', '''Havas, meredek sziklafal tetején ágakból és csontokból rakott hatalmas fészek, benne éhesen
vijjogó sasfióka; a hős kötélen mászik fel.''', '''A huge nest of branches and bones atop a steep snowy cliff, a hungry eaglet screeching inside; the hero
climbing up on a rope.''')
def _(s):
    s.sky(80, 170, H); s.snow(150)
    s.d.polygon([(60, H), (90, 140), (230, 120), (260, H)], fill=30)
    s.d.ellipse([70, 90, 250, 160], fill=12)
    for _ in range(30): s.d.line([(s.r.randrange(70, 250), s.r.randrange(95, 150)), (s.r.randrange(70, 250), s.r.randrange(95, 150))], fill=40, width=3)
    s.d.ellipse([140, 60, 180, 100], fill=200); s.d.polygon([(175, 75), (195, 82), (175, 88)], fill=230)
    s.d.line([(130, 140), (140, 400)], fill=200, width=2); s.person(142, 380, 80, 5, cloak=False, arms_up=True)

@kep('sas_repul', 'A sas repülése', '''Óriási sas repül a felhők fölött, a hátán a hős kapaszkodik; alattuk a völgy, előttük
a Varjútorony csúcsa, a varjak szétrebbennek.''', '''A giant eagle flying above the clouds with the hero clinging to its back; the valley far below, the top of the
dark crow tower ahead, crows scattering.''')
def _(s):
    s.sky(110, 200, H); s.fog(330, 50, 230, 160); s.hills(420, 30, 120)
    s.tower(240, 330, 30, 160, 20, 160)
    s.crows(10, 150, W, 40, 200, 4, 9, 30)
    s.eagle(110, 200, 45, 8, up=True); s.person(110, 200, 60, 8, cloak=True)

@kep('kotelhid', 'A kötélhíd', '''Mély szakadék fölött rozoga kötélhíd, a deszkák fele hiányzik; a szakadék szélén egy fiú
szakadt tarisznyája hever.''', '''A rickety rope bridge over a deep chasm with half its planks missing; a boy's torn satchel lies at the edge of
the chasm.''')
def _(s):
    s.sky(70, 150, 300); s.d.polygon([(0, 220), (90, 230), (110, H), (0, H)], fill=20); s.d.polygon([(220, 200), (W, 190), (W, H), (200, H)], fill=20)
    s.d.rectangle([110, 300, 200, H], fill=5); s.d.line([(150, 420), (160, H)], fill=80, width=3)
    s.d.line([(90, 230), (150, 280), (220, 205)], fill=110, width=3); s.d.line([(90, 210), (150, 255), (220, 185)], fill=110, width=2)
    for k in range(14):
        if k % 3 == 1: continue
        t = k / 13; x = 90 + t * 130; y = 230 + 50 * math.sin(t * math.pi) - t * 25
        s.d.line([(x, y - 2), (x, y + 6)], fill=150, width=5)
    s.d.ellipse([20, 400, 70, 430], fill=120); s.d.line([(30, 405), (60, 380)], fill=120, width=3)
    s.crows(5, 120, 280, 60, 160, 6, 10, 10)

@kep('hoviharos', 'Hóvihar a hágón', '''Vízszintesen hulló hóvihar a hágón, a hős lehajtott fejjel küzd a széllel; az út
eltűnik a hóban.''', '''A blizzard on the mountain pass, snow flying sideways, the hero bent against the wind; the path disappearing
in the snow.''')
def _(s):
    s.sky(140, 200, H); s.hills(260, 40, 170, 2); s.ground(380, 210, 6)
    s.person(150, 430, 160, 20, cloak=True, hood=True, bent=True, staff=True)
    s.snow(900, 250)

@kep('jegbarlang', 'A jégtroll barlangja', '''Kékes fényű jégbarlang, falaiba fagyott állatok és kristályok; a mélyén egy fehér
bundájú, jégcsapos szakállú jégtroll alszik.''', '''A glowing blue ice cave with animals frozen in its walls and crystals; deep inside sleeps an ice troll with
white fur and an icicle beard.''')
def _(s):
    s.im.paste(60, [0, 0, W, H]); s.glow(150, 300, 140, 150, 60)
    for k in range(14):
        x = k * 22; s.d.polygon([(x, 0), (x + 10, 30 + s.r.randrange(60)), (x + 20, 0)], fill=200)
    for _ in range(8):
        x, y = s.r.randrange(W), s.r.randrange(150, 400)
        s.d.polygon([(x, y), (x + 12, y - 40), (x + 24, y)], fill=230)
    s.troll(160, 420, 50, 240, 30)
    s.floor(420, 120, 150)

# =================================================================== A torony külseje
@kep('toronyut', 'A Varjútorony', '''Sziklás dombon áll a fekete kőből épült, csorba tetejű Varjútorony, párkányain varjak
százai; az úton romos kápolna és kőfalas temető.''', '''The crow tower of black stone with a broken top on a rocky hill, hundreds of crows on its ledges; along the road
a ruined chapel and a walled graveyard.''')
def _(s):
    s.sky(20, 70, 300); s.moon(80, 80, 34); s.stars(40, 200)
    s.hills(330, 60, 18, 1)
    s.tower(170, 300, 60, 220, 6, 230, broken=True)
    s.crows(25, 60, 280, 20, 220, 4, 10, 4)
    s.chapel(60, 400, 60, 50, 25, 90); s.d.rectangle([180, 390, 290, 400], fill=30)
    for x in (200, 230, 260): s.d.line([(x, 390), (x, 370)], fill=30, width=4); s.d.line([(x - 8, 378), (x + 8, 378)], fill=30, width=4)
    s.d.polygon([(130, H), (160, 300), (180, 300), (190, H)], fill=50)

@kep('kapuor', 'Csontvázak a kapuban', '''A torony vasalt tölgyfa kapuja ezüstzárral, előtte két csontváz őr rozsdás alabárddal,
a koponyájukban vörös fény.''', '''The iron-studded oak gate of the tower with a silver lock, guarded by two skeletons with rusty halberds and
red light in their skulls.''')
def _(s):
    s.im.paste(15, [0, 0, W, H]); s.bricks(0, 0, W, 400, None, 35)
    s.arch(60, 240, 60, 400, 50)
    for x in range(70, 240, 30): s.d.line([(x, 160), (x, 400)], fill=30, width=2)
    s.d.ellipse([140, 270, 160, 290], fill=230)
    s.ground(400, 25, 2)
    s.skeleton(70, 450, 160, 220); s.skeleton(230, 450, 160, 220)
    for x in (70, 230): s.glow(x, 300, 10, 255, 5)

@kep('kapolna_rom', 'Ábris szelleme', '''Romos, beomlott tetejű kápolna, korhadt padok; az oltár előtt áttetsző, kékes,
páncélos és szakállas lovagszellem térdel, és a néző felé fordul.''', '''A ruined chapel with a collapsed roof and rotten pews; before the altar kneels a translucent armoured, bearded
knight's ghost turning towards the viewer.''')
def _(s):
    s.sky(30, 70, 200); s.moon(230, 60, 26); s.im.paste(25, [0, 200, W, H])
    s.d.polygon([(0, 0), (60, 0), (40, 300), (0, 300)], fill=25); s.d.polygon([(W, 0), (240, 0), (260, 300), (W, 300)], fill=25)
    s.d.rectangle([90, 280, 210, 330], fill=50); s.floor(330, 22, 32)
    s.ghost(150, 400, 200, 200)
    for y in (380, 430): s.d.rectangle([20, y, 100, y + 10], fill=40); s.d.rectangle([200, y, 280, y + 10], fill=40)

@kep('lovag_temeto', 'A lovagok temetője', '''Csendes, elhagyatott temető, sírlapokon fekvő kőlovagok kőkarddal; a harmadik sír
fedőlapja megrepedt; középen nyitott kripta, a hátsó falat borostyán futja be.''', '''A quiet abandoned graveyard with stone knight effigies lying on the tombs holding stone swords; one slab is
cracked; an open crypt in the middle, ivy covering the back wall.''')
def _(s):
    s.sky(40, 100, 260); s.d.rectangle([0, 180, W, 260], fill=30)
    for _ in range(80): s.d.ellipse([s.r.randrange(W), s.r.randrange(180, 260), s.r.randrange(W), s.r.randrange(180, 260)], fill=None, outline=60)
    s.house(150, 290, 80, 50, 20, 0); s.d.rectangle([135, 255, 165, 290], fill=5)
    s.ground(290, 45, 2)
    for k, (x, y) in enumerate([(70, 360), (230, 360), (70, 440), (230, 440)]):
        s.d.polygon([(x - 50, y), (x + 50, y), (x + 40, y - 20), (x - 40, y - 20)], fill=110)
        s.d.ellipse([x - 45, y - 32, x - 25, y - 14], fill=150); s.d.rectangle([x - 25, y - 30, x + 35, y - 18], fill=150)
        if k == 2: s.d.line([(x - 20, y - 20), (x + 10, y)], fill=10, width=3)

@kep('kripta', 'A kőlovag', '''Boltíves kripta, a falak mentén kőkoporsók; a középső faragott koporsóról izzó szemű kőlovag
tápászkodik fel, kőkardját felemelve.''', '''A vaulted crypt with stone coffins along the walls; from the central carved sarcophagus a stone knight with
glowing eyes rises, lifting his stone sword.''')
def _(s):
    s.im.paste(10, [0, 0, W, H])
    for x in (0, 150): s.arch(x, x + 150, 0, 300, 30)
    s.floor(300, 15, 25)
    s.d.rectangle([60, 360, 240, 420], fill=60)
    s.person(150, 370, 230, 90, cloak=False, sword=False, arms_up=True, eyes=255)
    s.d.line([(220, 150), (245, 30)], fill=120, width=8)

@kep('akasztofa', 'Vince szelleme', '''Kis dombon korhadt akasztófa rongyos kötéldarabbal; a tövében lévő kőhalmon
szürke, áttetsző szellem ül, a fejét a kezébe temetve.''', '''A rotten gallows on a little hill with a frayed rope end; on a cairn beneath it sits a grey translucent ghost,
head buried in his hands.''')
def _(s):
    s.sky(30, 110, 330); s.moon(220, 90, 30)
    s.hills(360, 40, 20, 1)
    s.d.line([(90, 360), (90, 120)], fill=8, width=10); s.d.line([(80, 130), (210, 130)], fill=8, width=10)
    s.d.line([(110, 130), (90, 160)], fill=8, width=5); s.d.line([(190, 130), (190, 190)], fill=8, width=3)
    s.rocks(400, 5, 30, 40)
    s.ghost(170, 390, 150, 180)

# =================================================================== A torony belseje
@kep('udvar', 'A torony udvara', '''Kövezett udvar fekete tollakkal, középen koponyákkal kirakott kávájú kút; körben a
kaszárnya, a kéményes konyha, a torony kapuja és egy varjakkal teli kerek torony.''', '''A cobbled courtyard littered with black feathers, a well whose rim is lined with skulls in the middle; around it
barracks, a kitchen with a smoking chimney, the main tower door and a round tower full of crows.''')
def _(s):
    s.sky(30, 80, 250); s.tower(250, 260, 50, 200, 12, 0, cone=True); s.crows(12, 200, W, 20, 160, 4, 8, 4)
    s.tower(130, 260, 120, 250, 8, 150, cone=False)
    s.house(40, 270, 80, 70, 14, 120)
    s.floor(260, 30, 45)
    s.well(150, 400, 1.2, 60, skulls=True)

@kep('kaszarnya', 'A kaszárnya', '''Hosszú, sötét terem, priccseken páncélos csontvázak fekszenek, mintha aludnának; a falon
kardok és pajzsok, a terem végén láda.''', '''A long dark barracks hall, armoured skeletons lying on bunks as if asleep; swords and shields on the wall, a chest
at the far end.''')
def _(s):
    s.im.paste(18, [0, 0, W, H]); s.floor(240, 22, 32)
    for k in range(5):
        t = k / 4; y = 260 + t * 200; w = 60 + t * 80
        for side in (-1, 1):
            x = 150 + side * (40 + t * 70)
            s.d.rectangle([x - w / 2, y - 8, x + w / 2, y + 4], fill=50)
            s.d.ellipse([x - w / 2 + 2, y - 14 - t * 6, x - w / 2 + 12 + t * 8, y - 6], fill=200)
            s.d.line([(x - w / 2 + 12, y - 9), (x + w / 2 - 4, y - 9)], fill=180, width=int(2 + t * 3))
    for x in (40, 110, 190, 260): s.d.ellipse([x - 16, 120, x + 16, 160], fill=60); s.d.line([(x + 20, 100), (x + 30, 200)], fill=90, width=3)
    s.d.rectangle([125, 210, 175, 240], fill=70); s.torch(20, 230)

@kep('konyha', 'Gorgó, a ghoul szakács', '''Mocskos toronykonyha, kampókon lógó állatok, óriási üstben fortyogó zöld lé;
egy tagbaszakadt, szürke bőrű ghoul szakács kavargat, az övén vaskulcs lóg.''', '''A filthy castle kitchen, carcasses on hooks, a huge cauldron bubbling with green broth; a hulking grey-skinned
ghoul cook stirring, an iron key hanging from his belt.''')
def _(s):
    s.im.paste(20, [0, 0, W, H]); s.bricks(0, 0, W, 330, None, 34)
    for x in (30, 80, 250): s.d.line([(x, 0), (x, 60)], fill=80); s.d.ellipse([x - 12, 60, x + 12, 130], fill=60)
    s.fire(120, 420, 1.2)
    s.d.chord([40, 300, 200, 440], 0, 180, fill=40); s.d.rectangle([40, 360, 200, 372], fill=60)
    for i in range(5): s.glow(80 + i * 15, 340 - i * 25, 16, 130, 10)
    s.person(230, 460, 230, 6, cloak=False, arms_up=False, eyes=230)
    s.d.line([(255, 330), (170, 360)], fill=6, width=5)
    s.d.ellipse([215, 365, 235, 385], outline=200, width=3)

@kep('pince_feny', 'Az óriáspók', '''Boltíves, pókhálós pince hordókkal; a lámpás fényében egy kutyányi óriáspók ereszkedik le
a mennyezetről.''', '''A vaulted cellar full of cobwebs and barrels; in the lantern light a dog-sized giant spider descends from the
ceiling.''')
def _(s):
    s.im.paste(12, [0, 0, W, H]); s.arch(0, W, 0, 400, 30)
    for _ in range(14):
        x, y = s.r.randrange(W), s.r.randrange(200)
        for k in range(6): s.d.line([(x, y), (x + 40 * math.cos(k), y + 40 * math.sin(k))], fill=90)
    for x in (30, 90, 230): s.d.ellipse([x - 30, 330, x + 30, 410], fill=50); s.d.line([(x - 30, 370), (x + 30, 370)], fill=25, width=3)
    s.floor(400, 18, 26)
    s.d.line([(170, 0), (170, 150)], fill=200); s.spider(170, 180, 40, 4, 250)
    s.person(70, 475, 140, 4, sword=True, lantern=True)

@kep('katakomba', 'A katakomba', '''Végtelen katakombafolyosó, a falakba vájt fülkékben koponyák és csontok; a folyosó
elágazik, balra zöld fény dereng.''', '''An endless catacomb corridor, niches in the walls full of skulls and bones; the corridor forks, a green glow
on the left.''')
def _(s):
    s.im.paste(8, [0, 0, W, H])
    s.d.polygon([(0, 0), (110, 160), (110, 330), (0, H)], fill=35); s.d.polygon([(W, 0), (190, 160), (190, 330), (W, H)], fill=35)
    for side in (-1, 1):
        for k in range(10):
            t = k / 10; x = 150 + side * (150 - t * 110); y = 60 + t * 120
            for j in range(3):
                yy = y + j * (90 - t * 50); r = 9 - t * 6
                s.d.ellipse([x - r, yy - r, x + r, yy + r], fill=190); s.d.ellipse([x - r / 2, yy - r / 3, x, yy], fill=20)
    s.glow(120, 250, 30, 160, 15)
    s.floor(330, 20, 28)

@kep('kata_mely', 'A kőszemű őr', '''Katakombafolyosó kővé dermedt, rémült szerzetesszobrokkal; a folyosó végén egy
pikkelyes, kígyófejű lény közeledik sárgán izzó szemmel; a hős ezüsttükröt tart elé, elfordított fejjel.''', '''A catacomb corridor with petrified, terrified monk statues; at the end a scaly serpent-headed creature with
glowing yellow eyes approaches; the hero holds up a silver mirror, looking away.''')
def _(s):
    s.im.paste(10, [0, 0, W, H]); s.glow(150, 230, 60, 70, 30)
    s.person(80, 360, 150, 110, cloak=True, arms_up=True); s.person(230, 340, 130, 100, cloak=True, hood=True)
    s.person(150, 290, 90, 4, cloak=False, eyes=255); s.d.polygon([(140, 210), (160, 210), (150, 190)], fill=4)
    s.floor(300, 16, 24)
    s.person(200, 475, 170, 4, cloak=True); s.d.ellipse([140, 330, 175, 375], fill=240); s.d.ellipse([146, 337, 169, 368], fill=150)

@kep('kata_zold', 'A Holdanya könnye', '''Kis katakombakápolna zöld fényben, kőoltáron kristálykehely, benne magától világító
víz; a falon ezüstbetűs nevek.''', '''A small catacomb chapel in green light, a crystal chalice of self-glowing water on a stone altar; names in silver
letters on the walls.''')
def _(s):
    s.im.paste(10, [0, 0, W, H]); s.arch(40, 260, 40, 420, 30)
    for k in range(10): s.d.line([(60, 120 + k * 22), (60 + s.r.randrange(40, 80), 120 + k * 22)], fill=120, width=2); s.d.line([(240, 120 + k * 22), (240 - s.r.randrange(40, 80), 120 + k * 22)], fill=120, width=2)
    s.d.rectangle([100, 330, 200, 420], fill=60); s.floor(420, 18, 26)
    s.glow(150, 290, 70, 230, 30)
    s.d.polygon([(125, 270), (175, 270), (160, 305), (140, 305)], fill=255); s.d.rectangle([146, 305, 154, 325], fill=255); s.d.rectangle([132, 325, 168, 332], fill=255)

@kep('borton', 'A börtön', '''A torony börtönfolyosója, nyirkos cellák rozsdás láncokkal, egy fáklya; a folyosó végén
vasajtós cella, a rácsos ablakán át egy arc néz ki.''', '''The tower's dungeon corridor, damp cells with rusty chains, a torch; at the far end a cell with an iron door, a
face looking out through its barred window.''')
def _(s):
    s.im.paste(12, [0, 0, W, H]); s.d.polygon([(0, 0), (120, 140), (120, 300), (0, H)], fill=30); s.d.polygon([(W, 0), (180, 140), (180, 300), (W, H)], fill=30)
    s.bars(10, 90, 80, 380, 6, 16, 4)
    s.d.rectangle([125, 145, 175, 300], fill=60); s.d.rectangle([138, 170, 162, 190], fill=200); s.d.ellipse([143, 172, 157, 188], fill=30)
    s.torch(230, 230); s.floor(300, 18, 28)
    s.d.line([(220, 300), (240, 360), (260, 330)], fill=120, width=3)

@kep('bence_cella', 'Bence a cellában', '''Közelről egy cella vasajtajának rácsos ablaka, mögötte egy sápadt, piszkos arcú,
dacos szemű tizenhat éves fiú.''', '''Close-up of a cell door's barred window; behind it a pale, dirty-faced teenage boy with defiant eyes.''')
def _(s):
    s.im.paste(40, [0, 0, W, H]); s.bricks(0, 0, W, H, None, 60, 50, 24)
    s.d.rectangle([40, 80, 260, 440], fill=70)
    s.d.rectangle([80, 140, 220, 300], fill=15)
    s.glow(150, 220, 60, 90, 25)
    s.d.ellipse([110, 160, 190, 260], fill=150); s.d.polygon([(105, 190), (150, 150), (195, 190), (190, 170), (150, 140), (110, 170)], fill=20)
    s.d.ellipse([125, 200, 140, 210], fill=20); s.d.ellipse([160, 200, 175, 210], fill=20); s.d.line([(135, 240), (165, 240)], fill=30, width=3)
    s.bars(80, 220, 140, 300, 8, 28, 6)

@kep('kata_csontkamra', 'A csontkamra', '''Mennyezetig csontokkal teli oldalkamra, koponyaoszlopok, combcsont-boltívek, csontoltár
ezüst gyertyatartóval; a falból csuhás szerzetes-csontvázak bontakoznak ki zöld szemmel.''', '''An ossuary chamber filled to the ceiling with bones, pillars of skulls, arches of thighbones, a bone altar with a
silver candlestick; hooded monk skeletons emerging from the wall with green eyes.''')
def _(s):
    s.im.paste(30, [0, 0, W, H])
    for y in range(0, 330, 20):
        for x in range(-10, W, 20):
            s.d.ellipse([x + (y // 20 % 2) * 10, y, x + 16 + (y // 20 % 2) * 10, y + 16], fill=s.r.choice([110, 140, 170]))
    s.floor(330, 25, 40)
    s.d.rectangle([110, 300, 190, 360], fill=160); s.d.line([(150, 300), (150, 260)], fill=230, width=4); s.glow(150, 250, 12, 250, 6)
    for x in (60, 240): s.skeleton(x, 440, 170, 230, weapon=False); s.d.polygon([(x - 25, 290), (x, 260), (x + 25, 290)], fill=30)

# =================================================================== A torony felső része
@kep('csarnok', 'A varjúdémon', '''Magas, sötét csarnok fekete gerendákkal, varjúfejes címerpajzsokkal; a kőtrónon
emberméretű, fekete tollas, varjúfejű, sarlókarmú démon gubbaszt.''', '''A tall dark hall with black beams and crow-headed coats of arms; on the stone throne crouches a man-sized
black-feathered, crow-headed demon with sickle claws.''')
def _(s):
    s.im.paste(15, [0, 0, W, H])
    s.arch(90, 210, 20, 300, 60); s.arch(110, 190, 50, 290, 100)
    for x in (30, 270): s.d.polygon([(x - 18, 120), (x + 18, 120), (x + 14, 160), (x, 175), (x - 14, 160)], fill=50)
    s.d.rectangle([100, 280, 200, 340], fill=40); s.d.rectangle([110, 180, 190, 290], fill=40)
    s.demon(150, 290, 40, 4)
    s.floor(340, 18, 30); s.torch(20, 300); s.torch(260, 300)

@kep('varjuhaz', 'A varjak tornya', '''Kerek torony belseje, gerendákon és fészkekben száz meg száz varjú; középen egy
rúdon okos szemű, ősz tollú vén holló.''', '''Inside a round tower, hundreds of crows on beams and in nests; in the middle an old raven with grey feathers
and clever eyes on a perch.''')
def _(s):
    s.im.paste(20, [0, 0, W, H]); s.glow(150, 30, 40, 200, 20)
    for y in range(80, 380, 60):
        s.d.line([(0, y), (W, y + 10)], fill=60, width=6)
        for x in range(10, W, 26): s.crow(x + s.r.randrange(-5, 5), y - 2, 7, 4, perched=True)
    s.d.line([(150, 470), (150, 350)], fill=60, width=5); s.d.line([(110, 350), (190, 350)], fill=60, width=5)
    s.crow(150, 330, 22, 140, perched=True)

@kep('konyvtar', 'Morvath könyvtára', '''Mennyezetig érő polcok bőrkötéses könyvekkel, íróasztalon gyertya és nyitott napló,
olvasópulton egy fekete könyv; a polcok közül könyvek röppennek fel.''', '''Floor-to-ceiling shelves of leather-bound books, a candle and an open diary on a writing desk, a black book on a
lectern; books flying off the shelves like birds.''')
def _(s):
    s.im.paste(15, [0, 0, W, H]); s.shelves(0, 90, 20, 400, 40, 90); s.shelves(210, W, 20, 400, 40, 90)
    s.floor(400, 18, 26)
    s.d.rectangle([100, 330, 200, 345], fill=60); s.d.rectangle([110, 345, 120, 420], fill=60); s.d.rectangle([180, 345, 190, 420], fill=60)
    s.glow(170, 300, 30, 200, 14); s.d.rectangle([167, 305, 173, 330], fill=240)
    s.d.polygon([(115, 330), (150, 322), (150, 330)], fill=220); s.d.polygon([(150, 322), (160, 330), (150, 330)], fill=180)
    for _ in range(6):
        x, y = s.r.randrange(100, 220), s.r.randrange(60, 250)
        s.d.polygon([(x - 14, y), (x, y - 8), (x + 14, y), (x, y + 4)], fill=120)

@kep('alkimia', 'Az alkímiai műhely', '''Varázslóműhely lombikokkal, fortyogó üvegekkel; az asztalon egy piros, egy kék és
egy fekete üvegcse, mögötte egy macskanagyságú, ráncos, szarvacskás homunkulusz.''', '''A sorcerer's laboratory with alembics and bubbling glassware; on the table a red, a blue and a black vial, behind
them a cat-sized wrinkled homunculus with little horns.''')
def _(s):
    s.im.paste(18, [0, 0, W, H]); s.bricks(0, 0, W, 300, None, 30)
    s.fire(60, 300, 0.8); s.flask(60, 250, 1.6, 180)
    s.d.rectangle([0, 330, W, 345], fill=60); s.floor(345, 20, 28)
    for x, lv in [(130, 240), (170, 150), (210, 60)]: s.flask(x, 330, 0.9, lv)
    s.d.ellipse([235, 280, 285, 330], fill=6); s.d.ellipse([242, 255, 278, 290], fill=6)
    for x in (247, 273): s.d.polygon([(x - 4, 262), (x, 245), (x + 4, 262)], fill=6)
    s.d.ellipse([250, 266, 258, 274], fill=230); s.d.ellipse([262, 266, 270, 274], fill=230)

@kep('lepcso', 'A csigalépcső', '''Csigalépcső a torony falában, fáklyák; a falréseiből éles pengék csapnak ki, a hős
félreugrik.''', '''A spiral staircase inside the tower wall lit by torches; sharp blades shoot out of slits in the wall as the hero
leaps aside.''')
def _(s):
    s.im.paste(15, [0, 0, W, H]); s.bricks(0, 0, W, H, None, 30)
    for k in range(9):
        y = H - k * 52; x0 = 20 + (k % 2) * 30
        s.d.polygon([(x0, y), (x0 + 220, y - 20), (x0 + 230, y - 5), (x0 + 10, y + 15)], fill=60 + k * 6)
    s.torch(250, 200)
    for y in (230, 250, 270): s.d.polygon([(0, y), (120, y - 4), (120, y + 4)], fill=240)
    s.person(170, 330, 130, 4, sword=True, arms_up=True)

@kep('tukorterem', 'Az árnyékod', '''Kerek terem, falai, padlója, mennyezete tükör; az egyik tükörképe kilép a tükörből fekete
szemmel, a kezében a hős kardjának mása.''', '''A round chamber whose walls, floor and ceiling are mirrors; one reflection steps out of the glass with black
eyes, holding a copy of the hero's sword.''')
def _(s):
    s.im.paste(60, [0, 0, W, H])
    for x in range(0, W, 60): s.d.rectangle([x + 4, 20, x + 56, 400], fill=110); s.d.line([(x + 20, 30), (x + 40, 120)], fill=200, width=2)
    for x in range(30, W, 60): s.person(x, 380, 120, 70, sword=True)
    s.floor(400, 90, 120)
    s.person(90, 470, 180, 4, sword=True); s.person(210, 470, 180, 4, sword=True, eyes=40)

@kep('tetoterasz', 'A tetőterasz', '''A torony lapos teteje, peremén varjak, középen kőoltár csillagászati műszerrel
(Nap, csillagok, Hold egy körben); csapóajtó; alatta mélyen a völgy, lemenő nap.''', '''The tower's flat roof terrace, crows on the parapet, a stone altar with an astronomical instrument (sun, stars and
moon in a circle) in the middle; a trapdoor; the valley far below under a setting sun.''')
def _(s):
    s.sky(60, 180, 330); s.glow(60, 300, 60, 240, 25); s.hills(330, 30, 90)
    s.d.rectangle([0, 330, W, 360], fill=20)
    for x in range(0, W, 40): s.d.rectangle([x, 310, x + 22, 340], fill=20); s.crow(x + 11, 305, 6, 4, perched=True)
    s.floor(360, 40, 55)
    s.d.rectangle([120, 330, 180, 400], fill=80)
    s.d.ellipse([110, 280, 190, 340], outline=200, width=4)
    s.d.ellipse([125, 300, 140, 315], fill=240); s.d.polygon([(150, 290), (155, 305), (145, 305)], fill=240); s.d.chord([160, 300, 178, 318], 90, 270, fill=240)
    s.d.rectangle([210, 420, 270, 450], fill=10)

@kep('pecset', 'A pecsétes ajtó', '''Hatalmas fekete kőajtó három faragott, benyomható kőkoronggal: sugaras Nap, ötágú csillag,
holdsarló; fölöttük figyelmeztető felirat.''', '''A huge black stone door with three carved push-discs: a rayed sun, a five-pointed star and a crescent moon; a
warning inscription above them.''')
def _(s):
    s.im.paste(20, [0, 0, W, H]); s.bricks(0, 0, W, H, None, 30)
    s.arch(40, 260, 20, 460, 8)
    for k in range(3): s.d.line([(80, 90 + k * 16), (220, 90 + k * 16)], fill=130, width=3)
    cy = 260
    for x in (85, 150, 215): s.d.ellipse([x - 28, cy - 28, x + 28, cy + 28], fill=60)
    s.d.ellipse([75, cy - 10, 95, cy + 10], fill=230)
    for a in range(0, 360, 45): s.d.line([(85 + 12 * math.cos(math.radians(a)), cy + 12 * math.sin(math.radians(a))), (85 + 22 * math.cos(math.radians(a)), cy + 22 * math.sin(math.radians(a)))], fill=230, width=3)
    s.d.polygon([(150 + 20 * math.cos(math.radians(-90 + k * 144)), cy + 20 * math.sin(math.radians(-90 + k * 144))) for k in range(5)], fill=230)
    s.d.ellipse([197, cy - 20, 233, cy + 20], fill=230); s.d.ellipse([207, cy - 22, 241, cy + 16], fill=60)
    s.glow(150, 350, 80, 60, 30)

# =================================================================== A befejezés
@kep('morvath_terem', 'Morvath, a varjak ura', '''Kör alakú terem üvegkupolával, csillagos ég; az oltáron ragyog a
Holdkő; mellette sápadt, fekete szemű, fekete köpenyes varázsló, a vállán ősz holló.''', '''A round chamber under a glass dome and starry sky; the Moonstone shines on an altar; beside it a pale sorcerer
with black eyes in a black cloak, an old grey raven on his shoulder.''')
def _(s):
    s.im.paste(15, [0, 0, W, H]); s.d.chord([0, -150, W, 250], 0, 180, fill=40); s.stars(50, 90)
    for k in range(1, 6): s.d.line([(k * 50, 0), (150, 100)], fill=15, width=3)
    s.floor(330, 22, 34)
    s.d.rectangle([60, 300, 140, 380], fill=55); s.glow(100, 270, 50, 235, 20); s.d.ellipse([88, 258, 112, 282], fill=255)
    s.person(210, 470, 260, 4, cloak=True, hood=False, eyes=200, staff=True)
    s.crow(232, 250, 10, 120, perched=True)

@kep('morvath_nev', 'A név hatalma', '''A hős kinyújtott kézzel kiáltja a nevet; a varázsló megtántorodik, a fekete fény
szétfoszlik körülötte, a holló riadtan felrebben.''', '''The hero shouts a name with outstretched arm; the sorcerer staggers back as the black aura around him shreds
apart, the raven flaps away in alarm.''')
def _(s):
    s.im.paste(30, [0, 0, W, H]); s.glow(210, 280, 120, 120, 40)
    for k in range(16):
        a = k / 16 * 2 * math.pi; s.d.line([(210 + 50 * math.cos(a), 300 + 70 * math.sin(a)), (210 + 120 * math.cos(a), 300 + 140 * math.sin(a))], fill=20, width=4)
    s.person(210, 440, 200, 4, cloak=True, bent=True)
    s.crow(250, 120, 18, 4)
    s.person(60, 470, 190, 4, cloak=True, arms_up=True)

@kep('morvath_napko', 'A napkő fénye', '''A hős a magasba emeli a vakítóan izzó napkövet; a varázsló a szeme elé kapja a
kezét, a sötétség elillan a fény elől.''', '''The hero raises the blazing sunstone high; the sorcerer throws his arm over his eyes as the darkness flees from
the light.''')
def _(s):
    s.im.paste(10, [0, 0, W, H]); s.glow(90, 120, 90, 230, 40)
    for a in range(0, 360, 15):
        c, n = math.cos(math.radians(a)), math.sin(math.radians(a))
        s.d.line([(90 + 30 * c, 120 + 30 * n), (90 + 300 * c, 120 + 300 * n)], fill=150, width=2)
    s.d.ellipse([75, 105, 105, 135], fill=255)
    s.person(90, 470, 200, 4, cloak=True, arms_up=True)
    s.person(230, 470, 210, 4, cloak=True, bent=True, arms_up=True)

@kep('atok_amulett', 'A halálátok', '''A földre rogyott varázsló felemelt kezéből fekete füstként kígyózik az átok a hős felé;
a hős nyakában az amulett fehér fénnyel felragyog, és visszaveri.''', '''The fallen sorcerer raises a hand and a curse snakes towards the hero like black smoke; the amulet on the hero's
chest blazes with white light and turns it back.''')
def _(s):
    s.im.paste(40, [0, 0, W, H]); s.floor(380, 30, 45)
    s.person(80, 470, 220, 4, cloak=True, sword=True)
    s.glow(85, 330, 50, 255, 18); s.d.ellipse([78, 323, 92, 337], fill=255)
    for k in range(5):
        pts = [(260 - t * 15, 400 - t * 4 + 20 * math.sin(t * 0.9 + k)) for t in range(12)]
        s.d.line(pts, fill=8, width=6)
    s.person(250, 470, 110, 4, cloak=True, arms_up=True)

@kep('omlas', 'Az omló torony', '''A Varjútorony omlik: a kupola üvege hullik, kövek zuhannak, a padló megreped; a hős a
Holdkővel a kezében menekül, mellette a fiú.''', '''The crow tower collapses: the glass dome shatters, stones fall, the floor cracks; the hero flees holding the
Moonstone, the boy at his side.''')
def _(s):
    s.im.paste(50, [0, 0, W, H])
    for _ in range(40):
        x, y = s.r.randrange(W), s.r.randrange(320); r = s.r.randrange(4, 18)
        s.d.polygon([(x, y), (x + r, y + r // 2), (x + r // 2, y + r)], fill=s.r.choice([10, 20, 200]))
    s.floor(350, 30, 45)
    for k in range(4): s.d.line([(s.r.randrange(W), 360), (s.r.randrange(W), H)], fill=5, width=4)
    s.person(120, 470, 200, 4, cloak=True); s.glow(150, 330, 20, 255, 8)
    s.person(200, 470, 150, 4, cloak=False, child=True)

@kep('kijut', 'A romok', '''A domb tetején már csak fekete kőhalom maradt a Varjútoronyból; a porfelhő elül, az ég
kitisztul, a varjak szétszélednek; a hős a Holdkővel a kezében nézi.''', '''Only a heap of black stones remains of the crow tower on the hilltop; the dust settles, the sky clears, crows
scatter; the hero watches, holding the Moonstone.''')
def _(s):
    s.sky(150, 220, 330); s.glow(150, 100, 120, 240, 50)
    s.hills(330, 30, 60, 1)
    s.rocks(330, 14, 15, 60)
    s.crows(14, 0, W, 20, 220, 4, 10, 40)
    s.person(80, 470, 190, 4, cloak=True, sword=True); s.glow(110, 380, 15, 255, 6)

@kep('gyozelem', 'A Holdkő hazatér', '''A kápolna fülkéjében újra ragyog a Holdkő, telihold éjszakáján ezüstös fénye
beragyogja a völgyet; a falu népe ünnepel, egy fiú fűzfasípot fúj.''', '''The Moonstone shines again in the chapel niche; on the night of the full moon its silver light floods the valley;
the villagers celebrate, a boy plays a willow pipe.''')
def _(s):
    s.sky(20, 60, 300); s.moon(150, 70, 40); s.stars(40, 200)
    s.chapel(150, 330, 140, 120, 20, 0); s.glow(150, 260, 40, 255, 15); s.d.ellipse([140, 250, 160, 270], fill=255)
    for x, w, h in [(30, 60, 80), (270, 60, 90)]: s.house(x, 330, w, h, 15, 150)
    s.ground(330, 40, 2)
    for x in (30, 70, 110, 190, 230, 270): s.person(x + s.r.randrange(-6, 6), 450 + s.r.randrange(-10, 10), 110, 4, cloak=s.r.random() < 0.5, arms_up=True)
    s.person(150, 470, 90, 4, cloak=False, child=True); s.d.line([(160, 400), (185, 395)], fill=220, width=3)


# ---------------------------------------------------------------------------------------- futtatás
def main():
    import konyv
    from PIL import Image
    ill = os.path.join(HERE, 'ill'); os.makedirs(ill, exist_ok=True)
    assert len({k[0] for k in K}) == len(K)
    sects = {}
    for i, (name, cim, le, pr, f) in enumerate(K, 1):
        s = Scene(seed=i); f(s); s.save(os.path.join(ill, f'p{i}.png'))
        sects[str(i)] = konyv.NUM[name]
    json.dump(sects, open(os.path.join(HERE, 'img_sections.json'), 'w'), indent=0)
    md = ['# A Varjútorony ura – a képek listája', '',
          f'{len(K)} kép. Mindegyik az `ill/pN.png` fájl, és a lemezen a megadott fejezethez tartozik.',
          'A képeket a `kepcsere.py` cseréli (lásd a README-t). Közös stílus a promptokhoz:', '',
          f'> {STYLE}', '',
          '| # | Fejezet | Cím | Leírás | Prompt (angol) |', '|---|---|---|---|---|']
    for i, (name, cim, le, pr, f) in enumerate(K, 1):
        md.append(f'| {i} | {konyv.NUM[name]} | {cim} | {le} | {pr} |')
    open(os.path.join(HERE, 'KEPEK.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    json.dump([{'kep': i, 'fejezet': konyv.NUM[n], 'nev': n, 'cim': c, 'leiras': le, 'prompt': pr + '. ' + STYLE}
               for i, (n, c, le, pr, f) in enumerate(K, 1)],
              open(os.path.join(HERE, 'kepek.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(K), 'kép')

if __name__ == '__main__':
    main()
