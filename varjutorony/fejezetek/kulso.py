"""5. A torony külseje."""
from kv import *

sec('toronyut', '''A régi út kanyarogva kapaszkodik fel a dombra, a Varjútorony felé. A torony közelről még nagyobb és
sötétebb: a falai fekete kőből épültek, a csúcsa csorba, mint egy letört fog. Varjak százai ülnek
a párkányain, és mind téged figyelnek. Az út mentén egy romos kápolna áll, mögötte egy kőfallal
körülvett temető, a lovagok temetője. Az út a torony vasalt kapujához vezet. Ha a kápolnába mész,
[[kapolna_rom]]. Ha a temetőbe, [[lovag_temeto]]. Ha egyenesen a kapuhoz, [[varjak_lat]]. Az út mentén egy korhadt akasztófa is
áll; ha odamész, [[akasztofa]].''')

sec('varjak_lat', '''Ahogy közeledsz a kapuhoz, a varjak felröppennek a párkányokról, és károgva köröznek a fejed
fölött. Ha van varjútollad, [[varjak_toll]]. Ha nincs, [[varjak_tamad]].''',
    gate(T('varjak_toll'), 'varjutoll'), gate(T('varjak_tamad'), '!varjutoll'))

sec('varjak_toll', '''A varjak alacsonyan elsuhannak fölötted, és egy pillanatra megtorpannak. Meglátják a sapkádon a
kékes tollat, és elégedett károgással visszaülnek a párkányokra. Azt hiszik, Morvath egyik
szolgája vagy. A kapuhoz mész: [[kapuor]].''')

sec('varjak_tamad', '''A varjak egy fekete felhőként csapnak le rád. A csőrük és a karmuk mindenhol: a kezeden, az
arcodon, a nyakadon. Meg kell küzdened a rajjal, mintha egyetlen ellenfél volna. Ha legyőzöd,
[[varjak_utan]].''', fight([M('Varjúraj', 7, 8)], T('varjak_utan')))

sec('varjak_utan', '''A varjak megtizedelve, károgva szétrebbennek. De a károgásuk messze hallatszik, és a torony egyik
ablakában egy pillanatra egy sápadt arc jelenik meg, aztán eltűnik. Morvath tudja, hogy itt vagy.
Elveszítesz 1 SZERENCSE pontot. A kapuhoz mész: [[kapuor]].''', st(SZ, -1))

sec('kapuor', '''A torony kapuja hatalmas, vasalt tölgyfa kapu, a közepén egy kis ezüstzárral. Előtte két csontváz
áll őrt rozsdás alabárdokkal, a koponyájuk üres szemgödrében vörös fény pislákol. Ahogy meglátnak,
lassú, csörgő léptekkel feléd indulnak. Ha van ezüsttőröd, azzal harcolsz: [[csontvaz1]]. Ha nincs, a
kardoddal: [[csontvaz2]]. Ha van rézcsengőd, és megrázod, [[kapu_csengo]].''',
    gate(T('csontvaz1'), 'ezusttor'), gate(T('csontvaz2'), '!ezusttor'), gate(T('kapu_csengo'), 'csengo'))

sec('kapu_csengo', '''Megrázod a temetői csengőt. A csontvázak megtorpannak, a vörös fény kihuny a szemükben, és
csörömpölve a földre omlanak, mint egy halom tűzifa. Mátyás sírásó igazat mondott: a holtak nem
szeretik a csengő hangját. A kapuhoz lépsz: [[vaskapu]].''')

sec('csontvaz1', '''Az ezüsttőr minden csapásra recsegve szétzúzza a csontokat. Egyenként küzdesz meg a két
csontvázzal. Ha mindkettőt legyőzöd, [[vaskapu]].''',
    fight([M('Első csontváz', 7, 6), M('Második csontváz', 7, 6)], T('vaskapu'), pdmg=4, mdmg=2))

sec('csontvaz2', '''A kardod csak nehezen boldogul a csontvázakkal: a pengéd átsuhan a bordáik között. Egyenként
küzdesz meg a két csontvázzal. Ha mindkettőt legyőzöd, [[vaskapu]].''',
    fight([M('Első csontváz', 7, 6), M('Második csontváz', 7, 6)], T('vaskapu')))

sec('vaskapu', '''A csontvázak maradványai szétszórva hevernek a kapu előtt. A kapu közepén az ezüstzár halványan
csillog. Ha van ezüstkulcsod, kinyithatod vele a kaput: [[kapu_nyit]]. Ha nincs, megpróbálhatsz
átmászni a falon: [[fal]]. Ha van térképed a toronyról, megkeresheted a rejtett kiskaput: [[kiskapu]].''',
    gate(T('kapu_nyit'), 'ezustkulcs'), gate(T('kiskapu'), 'terkep'))

sec('kapu_nyit', '''Az ezüstkulcs hangtalanul fordul el a zárban, és a hatalmas kapu lassan, nyikorogva kitárul. Egy
sötét kapualj, és mögötte egy kövezett udvar. Belépsz: [[udvar]].''')

sec('fal', '''A torony körüli fal háromszor olyan magas, mint egy ember, a kövei közül moha és gaz nő. Ha van
köteled, egy kampós kővel a fal tetejére vetheted: [[falkotel]]. Ha nincs, puszta kézzel kell
felmásznod: [[falmaszas]]. Ha van kőfaragó vésőd, lépcsőt vághatsz a falba: [[falveso]].''',
    gate(T('falkotel'), 'kotel'), gate(T('falveso'), 'fahej'))

sec('falkotel', '''A kötelet egy kőre kötöd, és a fal tetejére hajítod. A harmadik dobásra beakad két fog közé. Felmászol
rajta, és a fal tetejéről leugrasz az udvar egy sötét sarkába. [[udvar]].''')

sec('falveso', '''A törp vésője úgy hatol a kőbe, mintha vaj volna. Kis lépcsőfokokat vágsz a fal hézagaiba, és
lassan feljutsz a tetejére. Dömötör büszke lenne rád. Leugrasz az udvar egy sötét sarkába. [[udvar]].''')

sec('falmaszas', '''A falon nehéz kapaszkodót találni, a kövek nedvesek és csúszósak. Tedd próbára az ügyességedet! Ha
sikerül, feljutsz a tetejére, és leugrasz az udvarra: [[udvar]]. Ha nem, lezuhansz: [[zuhanas]].''',
    skill(T('udvar'), T('zuhanas')))

sec('zuhanas', '''Félúton megcsúszik a kezed, és a fal tövébe zuhansz. Elveszítesz 3 ÉLETERŐ pontot. Feltápászkodsz.
Ha újra megpróbálod, [[falmaszas2]]. Ha van térképed, a kiskaput is megkeresheted: [[kiskapu]].''',
    st(E, -3), gate(T('kiskapu'), 'terkep'))

sec('falmaszas2', '''Újra nekifeszülsz a falnak, és most egy másik helyen próbálkozol, ahol a kövek között szélesebbek a
rések. Tedd próbára az ügyességedet! Ha sikerül, [[udvar]]. Ha nem, megint lezuhansz, és ezúttal
rosszabbul érsz földet: [[zuhanas2]].''', skill(T('udvar'), T('zuhanas2')))

sec('zuhanas2', '''A fal tövébe zuhansz, és a fejed egy kőbe csapódik. Elveszítesz 4 ÉLETERŐ pontot. Szédülve, de
konokul harmadszor is nekiindulsz, és ezúttal, a kövek között kapaszkodva, minden erődet összeszedve
feljutsz a fal tetejére. Leugrasz az udvarra: [[udvar]].''', st(E, -4))

sec('kiskapu', '''A térkép szerint a rejtett kiskapu a lovagok temetőjének hátsó falánál van, ahol a torony fala
a temetőfalba fut. Odamész, és a borostyán mögött egy keskeny vasajtót találsz. Nincs rajta zár,
csak egy rozsdás retesz. Kinyitod. Mögötte egy szűk, sötét lépcső vezet fel a falon belül. Ha
felmész rajta, [[kiskapu_lepcso]].''')

sec('kiskapu_lepcso', '''A falon belüli lépcső keskeny és meredek, az őrök egykor ezen jártak a falak tetejére. A tetején
egy kis ajtó nyílik az udvar fölé, egy keskeny bástyafolyosóra. Senki sem lát. Egy létrán lemászol
az udvar sarkába. [[udvar]].''', st(SZ, 1))

sec('kapolna_rom', '''A romos kápolna tetőzete beomlott, a padok korhadtak. Az oltár előtt egy áttetsző, kékes alak térdel:
egy páncélos, szakállas férfi szelleme. Ahogy belépsz, feléd fordul. - Ábris vagyok, a torony
utolsó őre - szól a hangja, mint a szél. - Morvath megölt, amikor a tornyot elfoglalta. Nem
nyughatom, amíg ő uralkodik. Ha megkérdezed, hogyan győzheted le Morvathot, [[abris_kerdez]]. Ha
megmutatod neki a pecsétgyűrűt, [[abris_gyuru]]. Ha meghajolsz, és kimész, [[toronyut]].''',
    gate(T('abris_gyuru'), 'gyuru'))

sec('abris_kerdez', '''- Morvath ereje a nevén alapul - mondja Ábris. - A valódi nevét eltitkolja, mert aki kimondja,
megtöri a hatalmát. Én nem tudom a nevét, de a könyvtárában, a naplójában leírta. És ha
legyőznéd, halálos átkot fog mondani rád: az amulettem megvéd tőle. A temetőben nyugszik a
testem, a harmadik sírban a kápolna felől. Vidd el az amulettet, és a bronzkulcsot is; az a
katakombák kapuját nyitja. Ha megmutatod neki a pecsétgyűrűt, [[abris_gyuru]]. Ha kimész, [[toronyut]].''',
    gain('abris'), gate(T('abris_gyuru'), 'gyuru'))

sec('abris_gyuru', '''A szellem a gyűrűre mered. - A varjú a K betűvel! Ezt a jelet láttam a köpenyén, azon az éjszakán.
- A homlokához emeli az áttetsző kezét. - Emlékszem... a varjak ura egyszer a falubeli apjáról
beszélt. Egy molnárról. Kelemen. Igen, Kelemennek szólította magát, amikor nem tudta, hogy hallom.
Ez a valódi neve! - A szellem fénye erősebb lesz. - Mondd ki, amikor szembeállsz vele! És vidd el
az amulettemet a sírból. Kimész: [[toronyut]].''', gain('nev'), gain('abris'))

sec('lovag_temeto', '''A lovagok temetője csendes és elhagyatott. Kőlovagok fekszenek a sírokon, kezükben kőkarddal.
A kápolna felől nézve a harmadik sír fedőlapja megrepedt, rajta egy név: "Ábris, a torony őre". A
temető hátsó falánál borostyán futja be a falat, a torony fala felé. A temető közepén egy kripta
áll, a bejárata nyitva, és lentről hideg lehelet árad. Ha Ábris sírjához mész, [[abris_sir]]. Ha
lemész a kriptába, [[kripta]]. Ha visszamész az útra, [[toronyut]].''')

sec('abris_sir', '''Ábris sírjának fedőlapja félrecsúszott. Ha Ábris szelleme megengedte, hogy elvidd, amit a sírjában
találsz, [[abris_amulett]]. Ha a szelleme nem tud róla, és mégis kinyitod a sírt, [[sirrablo]]. Ha
nem bolygatod meg a halott nyugalmát, [[lovag_temeto]].''',
    gate(T('abris_amulett'), 'abris'), gate(T('sirrablo'), '!abris'))

sec('abris_amulett', '''Félretolod a fedőlapot. A sírban egy páncélos csontváz fekszik, a mellén egy ezüstamulett, rajta
a Holdanya jele. Mellette egy nagy bronzkulcs. - Vidd el, vitéz - suttogja a szél. - A kulcs a
katakomba kapuját nyitja, a pincében. - Elteszed az amulettet a nyakadba, és a kulcsot az övedbe.
Halk sóhaj hallatszik, mintha valaki megkönnyebbült volna. Visszamész a temető közepére:
[[lovag_temeto]].''', gain('amulett'), gain('bronzkulcs'), st(SZ, 1))

sec('sirrablo', '''Félretolod a fedőlapot. A sírban egy páncélos csontváz fekszik, a mellén ezüstamulett. Ahogy
kinyúlsz felé, a csontváz keze megmozdul, és megragadja a csuklódat. A koponya feléd fordul, a
szemgödreiben kék fény gyúl. - Sírrabló! - suttogja. Meg kell küzdened vele. Ha legyőzöd,
[[sirrablo_gyoz]].''', fight([M('Ábris csontváza', 8, 7)], T('sirrablo_gyoz')))

sec('sirrablo_gyoz', '''A csontváz szétesik. Az amulett és egy nagy bronzkulcs a tiéd. De ahogy felállsz, a temető
megremeg, és egy sóhaj hallatszik: a sírrablás átka rád szállt. Elveszítesz 2 SZERENCSE pontot.
Elteszed a kincseket, és visszamész a temető közepére: [[lovag_temeto]].''',
    gain('amulett'), gain('bronzkulcs'), st(SZ, -2))

sec('kripta', '''A kripta lépcsője egy hideg, boltíves terembe vezet. A falak mentén kőkoporsók, és a közepén egy
nagy, faragott koporsó áll, rajta egy kőlovag. Ahogy belépsz, a kőlovag szemei felizzanak, és lassan
feltápászkodik, a kőkardját felemelve. Ha harcolsz vele, [[kolovag]]. Ha azonnal kimenekülsz,
[[lovag_temeto]].''')

sec('kolovag', '''A kőlovag lassú, nehéz csapásokkal támad. A kardod szikrát vet a kőpáncélon. Meg kell küzdened
vele. Ha legyőzöd, [[kolovag_gyoz]].''', fight([M('Kőlovag', 8, 9)], T('kolovag_gyoz')))

sec('kolovag_gyoz', '''A kőlovag darabokra omlik. A koporsójában régi fegyverek, és egy aranyozott ládika: benne nyolc
aranytallér, és egy kis üvegcse, rajta a felirat: "Az utolsó csepp". Kinyitod, és megszagolod:
gyógyító balzsam, erős és tiszta. Megiszod, és visszanyersz 6 ÉLETERŐ pontot. Visszamész a temető
közepére: [[lovag_temeto]].''', gold(8), st(E, 6))

sec('akasztofa', '''Az akasztófa egy kis dombon áll az út mentén, a gerendája korhadt, a köteléből csak egy rongyos darab
lóg. Alatta egy kőhalom, és a kőhalom tetején egy áttetsző, szürke alak ül, a fejét a kezébe temetve.
Ahogy közeledsz, felnéz. - Te is a toronyba mész? - kérdezi szomorúan. - Én Ádor társa voltam, az
őrök közül. Morvath felakasztatott, mert nem hódoltam be neki. Ha leülsz mellé, és meghallgatod,
[[akasztott]]. Ha visszamész az útra, [[toronyut]].''')

sec('akasztott', '''- A nevem Vince - mondja a szellem. - Ádor elmenekült, én maradtam. Bolond voltam. - Felmutat a
torony falára. - Ott, a temető mögött van a kiskapu, amit mi, őrök használtunk. A kőhalom alatt
eltemettem a falak rajzát, mielőtt elfogtak. Vedd ki, és használd! És ha Ádorral találkozol, mondd
meg neki, hogy nem haragszom. - A szellem elmosolyodik, és lassan elhalványul, mint aki végre
megnyugodott. A kőhalom alatt egy viaszosvászonba csavart térképet találsz. Visszamész az útra:
[[toronyut]].''', iff('!terkep', gain('terkep')), st(SZ, 1))
