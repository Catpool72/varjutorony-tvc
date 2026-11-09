"""4. A Kőkapu-hágó."""
from kv import *

sec('hago1', '''A keleti út meredeken kapaszkodik fölfelé a sziklák között. A fenyők elmaradnak, helyüket
törpefenyő és szürke kőgörgeteg veszi át. Délutánra egy szűk szorosba érsz, ahol két hatalmas
sziklaoszlop áll egymással szemben, mint egy kapu: a Kőkapu. A kapu mögül vékony füst száll fel,
és rikácsoló hangok hallatszanak. Ha óvatosan előrelopakodsz, hogy megnézd, kik azok, [[kobold_les]].
Ha bátran továbbmész az úton, [[kobold_ut]]. Ha letérsz az útról, és a sziklákon át kerülöd ki a
kaput, [[hago_kerulo]].''')

sec('kobold_les', '''Hasra fekszel egy szikla mögött, és kilesel. A Kőkapu mögötti mélyedésben koboldok táboroznak:
alacsony, szürke bőrű, hegyes fülű lények, rozsdás lándzsákkal. Hatan vannak. A tábor közepén egy
fakalitka áll, benne egy szakállas, zömök kis ember ül megkötözve: egy törp! Tedd próbára a
szerencsédet! Ha szerencséd van, nem vesznek észre: [[kobold_terv]]. Ha nincs, egy kavics megcsúszik a
lábad alatt: [[kobold_eszrevesz]].''', luck(T('kobold_terv'), T('kobold_eszrevesz')))

sec('kobold_terv', '''Figyeled a tábort. A koboldok a tűz körül ülnek, és egy nagy bográcsban főznek valamit. A vezérük,
egy tollas sisakot viselő, kövér kobold, éppen a törpöt piszkálja egy bottal. A kalitka a tábor
szélén áll, közel egy sziklafalhoz. Ha alkonyatig vársz, és a sötétben kiszabadítod a törpöt,
[[kobold_szabadit]]. Ha nyíltan rájuk támadsz, [[kobold_harc]]. Ha nem avatkozol bele, és
elosonsz a tábor mellett, [[kobold_oson]]. Ha előlépsz, és alkudni kezdesz a koboldvezérrel a
fogoly áráról, [[kobold_alku]].''', gate(T('kobold_alku'), ('gold', 5)))

sec('kobold_szabadit', '''Leszáll az alkony. A koboldok jól belaktak, és horkolnak a tűz körül; csak egy őr bóbiskol a kalitka
mellett. Odalopózol. Tedd próbára az ügyességedet! Ha sikerül, hangtalanul leütöd az őrt: [[torp_szabad]].
Ha nem, az őr felriad, és sikoltozni kezd: [[kobold_harc]].''', skill(T('torp_szabad'), T('kobold_harc')))

sec('kobold_eszrevesz', '''A kavics csörögve gurul le a lejtőn. A koboldok felugranak, és visítva rohannak feléd a
lándzsáikkal. Nincs hová menekülnöd. [[kobold_harc]].''')

sec('kobold_ut', '''Ahogy átlépsz a Kőkapun, a koboldok visítva felugranak a tűz mellől. Hatan vannak, de csak hárman
mernek közelebb jönni, a többiek a vezérük mögé bújnak, egy kövér, tollas sisakos kobold mögé. A
tábor közepén egy kalitkában egy törp ül. [[kobold_harc]].''')

sec('kobold_harc', '''A koboldok rád rontanak. Egyenként küzdesz meg a három legbátrabbal; ha mindhármat legyőzöd, a
többiek elmenekülnek. Ha legyőzöd őket, [[kobold_gyoz]].''',
    fight([M('Kobold lándzsás', 5, 4), M('Kobold lándzsás', 5, 5), M('Koboldvezér', 7, 6)], T('kobold_gyoz')))

sec('kobold_gyoz', '''A koboldvezér elesik, és a többiek visítva menekülnek a sziklák közé. A tábor a tiéd. A tűz
mellett egy zsákban négy aranytallért találsz. A kalitkában a törp ugrál izgatottan. - Engedj ki,
jó ember! Engedj ki! Ha kinyitod a kalitkát, [[torp_szabad]]. Ha nem törődsz vele, és továbbmész,
[[hago2]].''', gold(4))

sec('kobold_oson', '''Nagy ívben megkerülöd a tábort a sziklák között. A törp kétségbeesett pillantása követ, de nem
állsz meg. Egy óra múlva már messze jársz, és a koboldok rikácsolása elhal mögötted. Valamiért
mégis nyomja a lelked a dolog. Elveszítesz 1 SZERENCSE pontot. [[hago2]].''', st(SZ, -1))

sec('torp_szabad', '''Elvágod a kalitka köteleit, és a törp kibújik. Kinyújtóztatja zömök tagjait, és kezet ráz veled. -
Dömötör vagyok, a régi bánya törpjeinek utolsó kőfaragója. Ezek a gazemberek el akartak adni a
varjak urának. Tartozom neked. - A csizmájából egy kis, éles acélvésőt húz elő. - Ez a véső minden
követ megrepeszt, ha tudod, hol üsd. És ha a bányába mennél, velem mehetsz; ismerem minden zugát.
Ha vele mész a bányába, [[banya_bejarat]]. Ha megköszönöd, és folytatod az utad a hágón, [[hago2]].''',
    gain('fahej'), gain('dometor'))

sec('hago_kerulo', '''Letérsz az útról, és a sziklák között kapaszkodsz fölfelé. Nehéz út, a köveken megcsúszik a
csizmád, de a koboldok tábora messze elmarad alattad. Egy idő után egy szűk, sziklás párkányra érsz,
ahonnan egy barlang nyílik. A barlang szájában egy ősz, hosszú szakállú öregember ül, és mintha
rád várna. Ha odamész hozzá, [[remete]]. Ha továbbkapaszkodsz, [[hago2]].''', st(E, -1))

sec('hago2', '''Az út egyre magasabbra kapaszkodik. A levegő hideg és ritka, a szél fütyül a sziklák között. Egy
fennsíkra érsz, ahonnan több ösvény is indul. Az egyik egy barlang felé vezet, amelynek szájában tűz
pislákol. A másik egy régi, beomlott tárna felé, amelynek bejáratát törpfaragványok díszítik. A
harmadik a hó borította csúcsok felé kapaszkodik, ahol egy nagy sas köröz. A negyedik lefelé vezet,
a hágó túloldalára. Ha a barlanghoz mész, [[remete]]. Ha a tárnához, [[banya_bejarat]]. Ha a csúcsok felé,
[[sasberc]]. Ha a hágó túloldalára, [[hoviharos]].''')

sec('remete', '''A barlang szájában egy ősz öregember ül, előtte kis tűz pattog. A ruhája kopott szerzetesi csuha.
- Ambrus vagyok - mondja. - Valaha a Varjútorony kolostorában szolgáltam, amikor az még a
Holdanya szerzeteseié volt. Ülj le. - Forró gyökérteát ad. - Tudom, miért jöttél. Bence is itt járt.
Ha megkérdezed, mit tud Bencéről, [[remete_bence]]. Ha a toronyról kérdezed, [[remete_torony]]. Ha
megköszönöd a teát, és továbbmész, [[hago2]]. Ha megkéred, hogy imádkozzon érted, [[remete_ima]].''', st(E, 2))

sec('remete_bence', '''- Bátor fiú - sóhajt Ambrus. - Egy éjszakát töltött nálam, aztán a sasbérc felé ment, mert azt
hallotta, hogy a sasok a toronyig repülnek. De a varjak elkapták a kötélhídnál. Láttam, ahogy
elviszik. Most a torony börtönében van, biztosan. A börtön ajtaját egy vaskulcs nyitja, amit a
konyhán tartanak, mert a szakács a börtönőr is. Ha a toronyról kérdezed, [[remete_torony]]. Ha
megköszönöd, és továbbmész, [[hago2]].''')

sec('remete_torony', '''- A torony valaha kolostor volt - meséli Ambrus. - A kapuját egy ezüstkulcs nyitja. Az egyiket én
őrzöm, mióta elmenekültem. Neked adom, de csak ha bebizonyítod, hogy van eszed is, nem csak kardod.
Mert Morvath ellen az ész többet ér. - Felemeli az ujját. - Felelj: mi az, amit ha kimondasz, már nincs
többé? Ha azt feleled, "a titok", [[remete_rossz]]. Ha azt feleled, "a csend", [[remete_jo]]. Ha azt
feleled, "a név", [[remete_rossz2]].''')

sec('remete_jo', '''Ambrus elmosolyodik. - Csend. Jó válasz. - A csuhája alól egy régi ezüstkulcsot húz elő. - A torony
kapujáé. És még valamit tudj: aki Morvath valódi nevét kimondja, megtöri a hatalmát. A nevét én
sem tudom, de valahol a faluban él valaki, aki igen. A könyvtárában talán a naplója is elárulja.
Ha a sasbérc felé mész, [[sasberc]]. Ha a hágó túloldalára, [[hoviharos]]. Ha visszamész a
fennsíkra, [[hago2]].''', gain('ezustkulcs'), st(SZ, 1))

sec('remete_rossz', '''Ambrus megrázza a fejét. - A titok megmarad, ha kimondod, csak már nem titok. Nem ez a válasz. - A
tűzbe néz. - Kulcsot nem kapsz, de egy tanácsot igen: aki Morvath valódi nevét kimondja, megtöri a
hatalmát. A nevét én sem tudom, de valahol a faluban él valaki, aki igen. Ha a sasbérc felé mész,
[[sasberc]]. Ha a hágó túloldalára, [[hoviharos]]. Ha visszamész a fennsíkra, [[hago2]].''')

sec('remete_rossz2', '''Ambrus furcsán néz rád. - A név? Nem, a név megmarad, ha kimondod. Sőt, akkor van csak igazán
ereje. Jól jegyezd meg ezt, mert fontos lesz. - Megpaskolja a vállad. - Kulcsot nem kapsz, de ezt a
tanácsot igen: aki Morvath valódi nevét kimondja, megtöri a hatalmát. Ha a sasbérc felé mész,
[[sasberc]]. Ha a hágó túloldalára, [[hoviharos]]. Ha visszamész a fennsíkra, [[hago2]].''')

sec('banya_bejarat', '''A tárna bejáratát két kőből faragott törpharcos őrzi, a szakálluk a földig ér. A kapu fölött
rúnák: "Kőkapu-bánya. Belépni csak a hegy engedelmével." Mögötte sötét, hideg járat vezet a hegy
gyomrába. Ha Dömötör veled van, [[banya_dometor]]. Ha van lámpásod, és egyedül mész be, [[banya_lampas]].
Ha lámpás nélkül indulsz el, [[banya_sotet]]. Ha visszamész a fennsíkra, [[hago2]].''',
    gate(T('banya_dometor'), 'dometor'), gate(T('banya_lampas'), 'lampas'), gate(T('banya_sotet'), '!lampas'))

sec('banya_dometor', '''Dömötör megtapogatja az egyik kőharcos szakállát, és a kőben egy rejtett mélyedésből egy
ősi, kékes fényű kristálylámpát vesz elő. - A törpök fénye - mondja büszkén. - Nem kell olaj neki.
Kövess! - A bánya járatain keresztül vezet, ahol magadtól eltévednél. Egy nagy, oszlopos csarnokba
értek. [[banya_csarnok]].''')

sec('banya_lampas', '''Meggyújtod a lámpást, és belépsz a hideg tárnába. A járat sokszor elágazik, a falakon törp
rúnák. Egy darabig követed a sínpárt, amelyen valaha csillék jártak, és egy nagy, oszlopos
csarnokba érsz. [[banya_csarnok]].''')

sec('banya_sotet', '''A sötétben botladozva haladsz, a kezeddel a falat tapogatva. Egyszer megbotlasz egy sínben, és
elesel. A térded vérzik. Tedd próbára a szerencsédet! Ha szerencséd van, halvány fényt látsz a
távolban: [[banya_csarnok]]. Ha nincs, egy aknába zuhansz: [[banya_akna]].''',
    st(E, -1), luck(T('banya_csarnok'), T('banya_akna')))

sec('banya_akna', '''A lábad alól eltűnik a talaj, és zuhansz a sötétben. Egy kőpárkányon érsz földet, összetörve. A
fejed fölött messze, apró fénypont: az akna szája. Elveszítesz 4 ÉLETERŐ pontot. Kapaszkodva,
fogcsikorgatva kezdesz felmászni a falon. Tedd próbára az ügyességedet! Ha sikerül, [[banya_csarnok]].
Ha nem, [[banya_akna_halal]].''', st(E, -4), skill(T('banya_csarnok'), T('banya_akna_halal')))

sec('banya_akna_halal', '''Félúton a kezed megcsúszik a nedves sziklán. Még egyszer zuhansz, és ezúttal nincs párkány, ami
megállítana. A hegy gyomra elnyel. A kalandod itt véget ért.''')

sec('banya_csarnok', '''A csarnok mennyezetét faragott oszlopok tartják, mindegyik egy-egy törpkirály alakja. A falakon
ezüsterek csillognak. Középen egy kőasztal mögött egy idős törp ül egy halom áru között, egy kis
gyertya fényénél: a bánya utolsó kereskedője. A csarnok túlsó végén egy hatalmas kőajtó, előtte
mozdulatlan, háromszor akkora alak, mint egy ember: kőóriás. Ha a kereskedőhöz mész, [[torp_bolt]].
Ha az ezüsterekből próbálsz kitörni egy darabot, [[ezuster]]. Ha a kőajtóhoz mész, [[koorias]]. Ha
visszamész a felszínre, [[hago2]].''')

sec('torp_bolt', '''- Vásárló! - kiált fel a vén törp. - Bodrog vagyok. Kötél, lámpás, ezüsttükör, minden van, ami
egy hősnek kell. - Kiterít mindent a kőasztalra. - Árat alkudni nem lehet. De ha ezüstércet
hozol, azt megveszem: négy aranyat adok egy szép darabért. Ha vásárolsz, megteheted most. Ha
ezüströgöt adsz el neki, [[torp_elad]]. Ha végeztél, és visszamész a csarnok közepére,
[[banya_csarnok]].''',
    shop(('kotel', 2), ('lampas', 3), ('tukor', 4), ('olaj', 1)), gate(T('torp_elad'), 'ezustrog'))

sec('torp_elad', '''Bodrog a nagyítója alatt forgatja a rögöt. - Szép darab. Tiszta ezüst. - Négy aranytallért számol
a kezedbe. - Ha még találsz, hozd! Visszamész a csarnok közepére: [[banya_csarnok]].''',
    lose('ezustrog'), gold(4))

sec('ezuster', '''Az ezüstér a falban csillog, de a kő kemény. Ha van vésőd, azzal könnyen kifejtheted: [[ezuster_veso]].
Ha nincs, a kardod markolatával próbálkozol: [[ezuster_kard]].''',
    gate(T('ezuster_veso'), 'fahej'), gate(T('ezuster_kard'), '!fahej'))

sec('ezuster_veso', '''Dömötör vésője egyetlen pontos ütéssel kifeszít egy ökölnyi, tiszta ezüströgöt a falból. A kő
mintha magától engedne. Elteszed a rögöt. Visszamész a csarnok közepére: [[banya_csarnok]].''',
    gain('ezustrog'))

sec('ezuster_kard', '''Hosszan ütögeted a sziklát a markolattal. A kő lassan repedezik, és végül kitörik belőle egy kisebb
ezüströg. A karod sajog, és a kardod éle is csorbult egy kicsit. Elveszítesz 1 ÉLETERŐ pontot.
Elteszed a rögöt. Visszamész a csarnok közepére: [[banya_csarnok]].''', st(E, -1), gain('ezustrog'))

sec('koorias', '''Ahogy közeledsz a kőajtóhoz, a kőóriás szemei felizzanak, és dörgő hangon megszólal: - Ki zavarja a
törpkirályok álmát? Az ajtó mögött a királyok kincse. Csak az léphet be, aki a hegy barátja. Ha
Dömötör veled van, [[koorias_dometor]]. Ha harcolsz az óriással, [[koorias_harc]]. Ha meghajolsz,
és visszavonulsz, [[banya_csarnok]].''', gate(T('koorias_dometor'), 'dometor'))

sec('koorias_dometor', '''Dömötör előlép, és törp nyelven mond valamit az óriásnak. A kőóriás lassan meghajol, és félreáll. -
A hegy barátja - dörgi. A kőajtó feltárul. A királyok sírkamrájában kőkoporsók sorakoznak, rajtuk
kőkoronák. Az egyik koporsó lábánál egy kis ládika. Dömötör kinyitja. - Ezt a királyok neked szánják,
mert kiszabadítottál. - Hat aranytallér és egy kis, sárgán izzó kő van benne. [[kiralysir]].''')

sec('kiralysir', '''- Napkő - mondja Dömötör tisztelettel. - A törpök a nap fényét zárták bele. Ha a sötétségben
felemeled, a sötét lények megvakulnak tőle. - Elteszed a kincseket. A törp kikísér a bánya
kapujáig, és ott búcsút vesz. - Én maradok, rendbe teszem, amit a koboldok összetörtek. Sok szerencsét!
Kilépsz a napfényre: [[hago2]].''', gold(6), gain('napko'))

sec('koorias_harc', '''A kőóriás lassan, de rettenetes erővel csap le a kőöklével. A kardod szikrát vet a testén. Meg kell
küzdened vele, de minden csapása kétszeresen sebez. Ha legyőzöd, [[koorias_gyoz]].''',
    fight([M('Kőóriás', 9, 12)], T('koorias_gyoz'), mdmg=3))

sec('koorias_gyoz', '''A kőóriás megreped, és kőtörmelékké omlik. A kőajtó feltárul. A királyok sírkamrájában kőkoporsók
sorakoznak. Az egyik lábánál egy ládika: benne egy sárgán izzó kő. Ahogy kezedbe veszed, meleg árad
belőle, mint a napsugárból. A sírkamra levegője azonban hirtelen megfagy: a királyok nem szeretik a
sírrablókat. Elveszítesz 2 SZERENCSE pontot. Kimenekülsz a bányából: [[hago2]].''',
    gain('napko'), st(SZ, -2))

sec('sasberc', '''A csúcsok felé vezető ösvény egyre keskenyebb, a hó egyre mélyebb. Egy sziklakiszögellés alatt
állsz meg, ahol a szél kevésbé fúj. Fölötted, egy meredek sziklafal tetején, egy hatalmas fészek:
ágakból és csontokból rakták. Éles, éhes vijjogás hallatszik belőle: egy sasfióka. Az anyja nincs
sehol. Ha van köteled, és felmászol a fészekhez, [[sas_kotel]]. Ha kötél nélkül próbálsz felmászni,
[[sas_maszik]]. Ha továbbmész az ösvényen, [[kotelhid]].''',
    gate(T('sas_kotel'), 'kotel'), gate(T('sas_maszik'), '!kotel'))

sec('sas_kotel', '''A kötelet egy kiálló sziklacsúcsra hurkolod, és lassan felmászol a fészekig. A fióka már majdnem
akkora, mint egy kutya, és éhesen tátogatja a csőrét. Fehér tollai között vérző seb: egy varjú
csípte meg. [[sas_fiok]].''')

sec('sas_maszik', '''A szikla jeges és csúszós. Tedd próbára az ügyességedet! Ha sikerül, feljutsz a fészekig: [[sas_fiok]].
Ha nem, lecsúszol, és a havas párkányra zuhansz: [[sas_esik]].''', skill(T('sas_fiok'), T('sas_esik')))

sec('sas_esik', '''A hóba zuhansz, és a lábad megrándul. Elveszítesz 3 ÉLETERŐ pontot. Felülsz, és a fészek felé nézel.
Még egyszer nem mered megpróbálni. Folytatod az utad az ösvényen: [[kotelhid]].''', st(E, -3))

sec('sas_fiok', '''A fióka éhesen vijjog, és a kezed felé kap. Ha adsz neki a füstölt húsból, [[sas_etet]]. Ha nincs mit
adnod neki, és lemászol, [[kotelhid]]. Ha elveszed a fészekben heverő fényes holmit, egy
aranyláncot, amit a sasok valahonnan elhoztak, [[sas_lop]].''', gate(T('sas_etet'), 'hus'))

sec('sas_etet', '''A fióka mohón kapkodja a húscafatokat. Amikor jóllakott, elégedetten összegömbölyödik. Ekkor hatalmas
árnyék vetül rád: az anyasas száll le a fészek szélére. Akkora, mint egy ló, a szeme aranyszínű. Egy
pillanatig fenyegetően mered rád, aztán meglátja a jóllakott fiókáját, és lehajtja a fejét. Érted,
hogy megköszöni. [[sas_baratsag]].''', lose('hus'), gain('sas'))

sec('sas_baratsag', '''Az anyasas a szárnyával a hátára mutat. Mintha azt mondaná: ülj fel. Messze, a hegyek alatt látszik
a Varjútorony csúcsa, a tetején egy lapos terasz. Ha felülsz a sas hátára, [[sas_repul]]. Ha inkább
gyalog folytatod az utad a kötélhíd felé, [[kotelhid]].''')

sec('sas_repul', '''Belekapaszkodsz a sas tollaiba, és a hatalmas madár elrugaszkodik a szikláról. A szél süvít a
füledben, a völgy messze alattad. A sas a torony felé suhan, a varjak károgva szétrebbennek
előle. Ha van varjútollad, nem is figyelnek rád; ha nincs, egy csapat varjú utánatok repül, de
nem érnek utol. A sas lassan köröz, és leereszkedik a torony lapos tetőteraszára. [[tetoterasz]].''')

sec('sas_lop', '''Kinyújtod a kezed az aranylánc felé. Ebben a pillanatban hatalmas árnyék vetül rád, és éles
vijjogás hasít a levegőbe: az anyasas száll le a fészek szélére, és a karmaival rád támad! Meg kell
küzdened vele. Ha legyőzöd, [[sas_megolt]].''', fight([M('Anyasas', 9, 8)], T('sas_megolt')))

sec('sas_megolt', '''Az anyasas a mélybe zuhan. A fióka sírva vijjog. Az aranylánc a tiéd, öt aranyat ér, de a szíved
nehéz. Ezzel a sasok barátságát örökre eljátszottad. Elveszítesz 2 SZERENCSE pontot. Lemászol a
fészekből, és folytatod az utad: [[kotelhid]].''', gold(5), st(SZ, -2))

sec('kotelhid', '''Az ösvény egy mély szakadékhoz vezet, amelynek alján egy patak csillog. Egy rozoga kötélhíd ível át
rajta; a deszkák fele hiányzik, a kötelek kopottak. A híd túlsó végénél a lejtő a hágó túloldalára
vezet. A szakadék szélén egy fiú tarisznyája hever: Bence itt járt! Ha átkelsz a hídon, [[kotelhid_at]].
Ha előbb megnézed a tarisznyát, [[bence_tarisznya]].''')

sec('bence_tarisznya', '''A tarisznya szakadt, mintha karmok tépték volna szét. Benne kenyérhéj, egy kis kés, és egy szénnel
írt cetli: "Ha valaki megtalálja: a varjak elvittek. A toronyba visznek. Mondják meg nagyapának,
hogy nem félek. Bence." A kenyérhéjat és a cetlit elteszed. Ha átkelsz a hídon, [[kotelhid_at]].''',
    gain('kenyer'), st(SZ, 1))

sec('kotelhid_at', '''Óvatosan rálépsz a hídra. A kötelek nyikorognak, a deszkák rezegnek. A közepén járhatsz, amikor
károgás hallatszik: egy csapat varjú csap le rád, és a karmaikkal a köteleket tépik! Ha van
varjútollad, [[hid_toll]]. Ha van köteled, magadhoz kötheted a híd korlátjához, mielőtt a varjak
odaérnek: [[hid_kotel]]. Ha egyik sincs, rohanni kezdesz: [[hid_rohan]].''',
    gate(T('hid_toll'), 'varjutoll'), gate(T('hid_kotel'), 'kotel'))

sec('hid_toll', '''A varjak egy pillanatra megtorpannak fölötted, ahogy meglátják a sapkádon a kékes varjútollat.
Károgva köröznek, aztán elhúznak a torony irányába. Azt hiszik, közéjük tartozol. Nyugodtan
átkelsz a hídon: [[hagotul]].''')

sec('hid_kotel', '''A kötelet a derekadra és a híd korlátjára hurkolod. A varjak a köteleket tépik, a híd megbillen, és
egy pillanatig a szakadék fölött lógsz. De a kötél megtart. A varjak elrepülnek, és te
fogcsikorgatva átkapaszkodsz a túloldalra. Elveszítesz 2 ÉLETERŐ pontot. [[hagotul]].''', st(E, -2))

sec('hid_rohan', '''Rohansz a deszkákon, a varjak a fejed körül csapkodnak. Az egyik kötél elszakad, a híd
megbillen. Tedd próbára a szerencsédet! Ha szerencséd van, [[hid_atjut]]. Ha nincs, [[hid_zuhan]].''',
    luck(T('hid_atjut'), T('hid_zuhan')))

sec('hid_atjut', '''Egy hatalmas ugrással átveted magad a túlsó szélre, éppen abban a pillanatban, amikor a híd
leszakad. A varjak sértett károgással elrepülnek. Véres karmolások borítják a karod. Elveszítesz 3
ÉLETERŐ pontot. [[hagotul]].''', st(E, -3))

sec('hid_zuhan', '''A híd leszakad alattad, és a szakadékba zuhansz. Egy bokorba kapaszkodsz, ami a falból nő ki, de
a varjak a kezed csipkedik. Tedd próbára az ügyességedet! Ha sikerül felhúzódzkodnod, [[hid_mentes]].
Ha nem, [[hid_halal]].''', st(E, -2), skill(T('hid_mentes'), T('hid_halal')))

sec('hid_mentes', '''Fogcsikorgatva felhúzódzkodsz a peremig, és kimászol. A híd elveszett, de a túlsó oldalra kerültél.
Elveszítesz 2 ÉLETERŐ pontot. [[hagotul]].''', st(E, -2))

sec('hid_halal', '''A bokor gyökerei kiszakadnak a sziklából, és a mélybe zuhansz. A varjak károgása kísér le a
patakig. A kalandod itt véget ért.''')

sec('hoviharos', '''A hágó túloldala felé vezető úton fekete felhők gyűlnek, és hirtelen hóvihar tör ki. A szél
csípős, a hó mindent eltakar. Nem látod az utat. Ha továbbmész a viharban, [[vihar_tovabb]]. Ha
menedéket keresel a sziklák között, [[jegbarlang]].''')

sec('vihar_tovabb', '''Lehajtott fejjel haladsz a viharban. A hideg a csontjaidig hatol, a kezed elgémberedik. Tedd
próbára a szerencsédet! Ha szerencséd van, a vihar elcsitul: [[vihar_vege]]. Ha nincs, eltévedsz:
[[vihar_eltevedt]].''', st(E, -2), luck(T('vihar_vege'), T('vihar_eltevedt')))

sec('vihar_eltevedt', '''Órák telnek el, mire a vihar alábbhagy. Fogalmad sincs, hol vagy. A lábad lefagyott, a lélegzeted
kristályként csillog. Elveszítesz még 3 ÉLETERŐ pontot. Végül egy barlang szájára bukkansz, ahol
menedéket kereshetsz: [[jegbarlang]].''', st(E, -3))

sec('vihar_vege', '''A felhők szétszakadnak, és a lemenő nap fényében meglátod magad előtt a lejtőt, amely a hágó
túloldalára vezet. A völgyben, egy sziklás dombon, ott áll a Varjútorony. Lefelé indulsz: [[hagotul]].''')

sec('jegbarlang', '''A barlang falait vastag jég borítja, és kékes fény dereng benne. Bent nincs szél, de hideg van. A
barlang mélyén jégkristályok csillognak, és mintha valami mozogna köztük: egy fehér bundájú, kétszer
akkora alak, mint egy ember, jégcsapokkal a szakállán. Jégtroll! Még nem vett észre. Ha
megtámadod, [[jegtroll]]. Ha csendben megvárod a vihar végét a barlang szájánál, [[jegbarlang_var]]. Ha a
barlang oldalfalában csillogó kristályokhoz lopakodsz, [[jegkristaly]].''')

sec('jegtroll', '''Rárontasz a jégtrollra. Hatalmas, de lassú, és a jeges karmaival csapkod. Meg kell küzdened vele.
Ha legyőzöd, [[jegtroll_gyoz]].''', fight([M('Jégtroll', 8, 10)], T('jegtroll_gyoz')))

sec('jegtroll_gyoz', '''A jégtroll összerogy, és a teste lassan jéggé dermed. A barlang mélyén a kristályok között egy
megfagyott vándor maradványait találod; a zsákjában három aranytallér és egy kötél. Elteszed. Ahogy a
vihar elül, kilépsz a barlangból: [[vihar_vege]].''', gold(3), iff('!kotel', gain('kotel')))

sec('jegbarlang_var', '''Leülsz a barlang szájánál, és vársz. A jégtroll horkolni kezd a mélyben. A hideg a csontjaidig
hatol, de a vihar lassan elül. Elveszítesz 1 ÉLETERŐ pontot. Óvatosan kilépsz a barlangból:
[[vihar_vege]].''', st(E, -1))

sec('hagotul', '''A hágó túloldalán a lejtő meredeken ereszkedik egy sziklás völgybe. A völgy közepén, egy dombon
áll a Varjútorony, a csorba falai körül varjak keringenek. A domb lábánál egy régi út kanyarog,
amely egy romos kápolna és egy temető mellett halad el. Lefelé indulsz a köves ösvényen. [[toronyut]].''')

sec('kobold_alku', '''Kilépsz a szikla mögül, és felemelt kézzel a tábor felé indulsz. A koboldok visítva felugranak, de a
vezérük rájuk rikolt. - Mit akar a nagy ember? - Megvenném a foglyotokat - mondod, és megcsörgeted
az erszényedet. A koboldvezér szeme felcsillan. - Öt arany! Öt fényes arany, és a szakállas a tiéd!
A varjak ura csak hármat ígért! - Kifizeted az öt aranyat, és a koboldok vihogva kinyitják a
kalitkát. A törp dühösen ráz öklöt feléjük, aztán veled tart. [[torp_szabad]].''', gold(-5))

sec('remete_ima', '''Ambrus letérdel a barlang kőpadlójára, és a kezét a fejedre teszi. Halkan, egy régi nyelven
imádkozik, amit nem értesz, de a szavak úgy hatnak rád, mint a meleg napsugár. A barlang falán a tűz
árnyai elcsendesednek. Amikor feláll, a szemében könny csillog. - A Holdanya vigyázzon rád, ahogy
egykor a tornyára vigyázott. Visszanyered a SZERENCSÉD kezdeti értékét, és 2 ÉLETERŐ pontot. Ha a
Bencéről kérdezed, [[remete_bence]]. Ha a toronyról, [[remete_torony]]. Ha továbbmész, [[hago2]].''',
    st(SZ, 12), st(E, 2))

sec('jegkristaly', '''A barlang oldalfalában hatalmas, kékesfehér kristályok nőnek, és a belsejükben apró fénypontok
táncolnak, mint a szentjánosbogarak. Az egyik kristály tövében egy halom arany- és ezüstpénz
csillog, a jégbe fagyva; valaki egykor itt rejtette el. Ha megpróbálod kifeszíteni a pénzt a jégből,
[[jeg_kincs]]. Ha visszamész a barlang szájához, [[jegbarlang_var]].''')

sec('jeg_kincs', '''A kardod hegyével feszegetni kezded a jeget. A kristályok halkan csilingelnek, és a barlang mélyén a
horkolás egy pillanatra elhallgat. Tedd próbára a szerencsédet! Ha szerencséd van, a pénz kiszabadul,
és a troll alszik tovább: [[jeg_arany]]. Ha nincs, egy kristály megreped, és jéghideg pára tódul ki
belőle: [[jeg_halal]].''', luck(T('jeg_arany'), T('jeg_halal')))

sec('jeg_arany', '''A jég egy halk reccsenéssel enged, és a markodba hullik nyolc aranytallér és néhány
ezüstpénz, ami már semmit sem ér. Elteszed az aranyat, és lábujjhegyen visszaosonsz a barlang
szájához, ahol megvárod, amíg a vihar elül. Elveszítesz 1 ÉLETERŐ pontot a hidegtől. [[vihar_vege]].''',
    gold(8), st(E, -1))

sec('jeg_halal', '''A kristályból kiáramló pára fehér, mint a tej, és ahol hozzád ér, a bőröd elfehéredik és
megkeményedik. Megpróbálsz elhátrálni, de a lábad már a jégbe fagyott. A kezed a kardon marad, a
szemed nyitva, ahogy a jég lassan beborít. Mire a vihar elül, a barlang falában egy újabb kristály
csillog, és a belsejében egy vándor alakja látszik. A kalandod itt véget ért.''')
