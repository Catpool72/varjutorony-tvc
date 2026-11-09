"""6b. A torony belseje: csarnok, varjak tornya, könyvtár, műhely, lépcső, emelet, tető, pecsétes ajtó."""
from kv import *

sec('csarnok', '''A csarnok magas, sötét terem, a mennyezetét fekete gerendák tartják. A falakon varjúfejes
címerpajzsok, a terem végén egy kőtrón. A trón karfáján egy emberméretű, fekete tollas alak gubbaszt,
a feje varjúé, a karmai, mint a sarló: a varjúdémon, a torony őre. Úgy tűnik, alszik. Ha a démon
már halott, [[csarnok_kozep]]. Ha van varjútollad, nyugodtan átsétálhatsz a termen: [[csarnok_toll]].
Ha nincs, megpróbálhatsz átosonni mellette: [[csarnok_oson]]. Ha Bence veled van, és kinyitjátok az
ablakok zsalugáterét, [[csarnok_ablak]].''',
    gate(T('csarnok_kozep'), 'demon'), gate(T('csarnok_toll'), 'varjutoll'), gate(T('csarnok_oson'), '!varjutoll'),
    gate(T('csarnok_ablak'), 'bence'))

sec('csarnok_toll', '''A démon felnyitja az egyik szemét, ahogy elhaladsz mellette. Meglátja a sapkádon a kékes varjútollat,
és álmosan károg egyet, mintha üdvözölne. Aztán újra lehunyja a szemét. A terem a tiéd: [[csarnok_kozep]].''')

sec('csarnok_ablak', '''Bence felmászik az egyik ablakpárkányra, és kinyitja a zsalugátert. Az ablakon besüt a napfény, és
a démon sötét alakjára esik. A démon összerándul, nyöszörög, a szárnyát a feje fölé húzza, és mély
álomba merül. - Mondtam! - suttogja Bence büszkén. A terem a tiétek: [[csarnok_kozep]].''')

sec('csarnok_oson', '''A falak árnyékában lopakodsz a terem túlsó vége felé. Tedd próbára a szerencsédet! Ha szerencséd van,
a démon tovább alszik: [[csarnok_kozep]]. Ha nincs, egy varjútoll roppan a talpad alatt, és a démon
felriad: [[demon]].''', luck(T('csarnok_kozep'), T('demon')))

sec('demon', '''A varjúdémon felrikolt, kitárja hatalmas, fekete szárnyát, és lecsap rád. A karmai, mint a kés.
Meg kell küzdened vele. Ha Bence veled van, és harcol, a démon egyszer-egyszer felé is kap, és így
kevesebbszer talál el téged. Ha legyőzöd, [[demon_gyoz]].''',
    iff('bence', fight([M('Varjúdémon', 9, 9)], skmod=1), fight([M('Varjúdémon', 9, 9)])), only(T('demon_gyoz')))

sec('demon_gyoz', '''A varjúdémon fülsiketítő rikoltással a földre zuhan, és a teste fekete tollak halmazává hullik szét.
A tollak között három aranytallér csillog, a démon ezeket gyűjtötte, mint a szarkák. A terem a
tiéd: [[csarnok_kozep]].''', gain('demon'), gold(3))

sec('csarnok_kozep', '''A csarnok közepén állsz. A falakon a varjúfejes címerek mintha téged néznének. Balra egy faragott
ajtó a könyvtárba vezet, jobbra egy vasalt ajtó mögül furcsa, kénes szag árad: Morvath műhelye.
A trón mögött egy csigalépcső kanyarog fel a torony felső szintjeire. Egy kisebb ajtó a börtön
felé vezet le, a nagy kapu pedig az udvarra. Ha a könyvtárba mész, [[konyvtar]]. Ha a műhelybe,
[[alkimia]]. Ha a csigalépcsőn mész fel, [[lepcso]]. Ha a börtönbe mész le, [[borton]]. Ha az udvarra
mész ki, [[udvar]].''')

sec('csarnok_oldal', '''A konyha hátsó ajtaja egy keskeny, sötét folyosóra nyílik, amelyen a szolgák jártak. A folyosó végén
egy függöny mögül a csarnokba látsz be. A trónon egy emberméretű, varjúfejű alak gubbaszt.
Kilépsz a függöny mögül: [[csarnok]].''')

sec('varjuhaz', '''A kerek torony belsejében száz meg száz varjú ül a gerendákon, a falba vájt fészkekben. Az ürülékük
bűze fojtogató. A torony közepén egy vén, ősz tollú holló gubbaszt egy rúdon, a szeme okosan
csillog. Ahogy belépsz, minden varjú feléd fordul. Ha van varjútollad, [[varju_toll]]. Ha nincs,
[[varju_tamad]].''', gate(T('varju_toll'), 'varjutoll'), gate(T('varju_tamad'), '!varjutoll'))

sec('varju_toll', '''A varjak megnyugszanak, ahogy meglátják a tollat. Az ősz holló a rúdon emberi hangon szól: - Új
testvér? Furcsa testvér. Kétlábú. - Kacag. - Morvath testvérünk volt, mielőtt varázsló lett. Kelemen
volt, a molnárfiú. Mi tanítottuk meg beszélni. Most rabszolgák vagyunk. Ha megkérdezed, hogyan lehet
legyőzni, [[hollo_tanacs]]. Ha kimész, [[udvar]].''', gain('nev'))

sec('hollo_tanacs', '''- Legyőzni? - A holló félrebillenti a fejét. - Mondd ki a nevét, és megtörik. Vagy hozd el neki az
apja szavát; akkor talán meg is szelídül. Csak az apja szereti még. Ő is szerette az apját, mielőtt
a falu gyűlölni tanította. - A holló felborzolja a tollát. - És ha a pecsétes ajtóhoz érsz, emlékezz:
reggel, este, éjjel. Kimész: [[udvar]].''', st(SZ, 1))

sec('varju_tamad', '''A varjak egy fekete felhőként csapnak le rád a gerendákról. Meg kell küzdened velük, mintha egyetlen
ellenfél volnának. Ha legyőzöd őket, [[varju_utan]].''', fight([M('Varjúraj', 7, 8)], T('varju_utan')))

sec('varju_utan', '''A varjak nagy része elmenekült, a többi holtan hever a padlón. Az ősz holló is elrepült. Az egyik
fészekben egy hosszú, kékesen fénylő evezőtollat találsz. Aki ezt viseli, azt a varjak a sajátjuknak
hiszik. A sapkádba tűzöd. Kimész: [[udvar]].''', gain('varjutoll'))

sec('konyvtar', '''A könyvtár polcai a mennyezetig érnek, tele poros, bőrkötéses könyvekkel. Egy íróasztalon gyertya ég,
és egy nyitott napló fekszik. A polcok között suhogás hallatszik, mintha lapok zizegnének. Ha az
íróasztalhoz mész, [[konyv_naplo]]. Ha a polcok közt kutatsz, [[konyv_polc]]. Ha az olvasópulton
nyitva fekvő fekete könyvbe olvasol, [[konyv_tiltott]]. Ha visszamész a
csarnokba, [[csarnok_kozep]].''')

sec('konyv_naplo', '''Belelapozol a naplóba. Morvath kézírása szép és szabályos. "Tíz éve hagytam el Fenyvesvölgyet. A
falu kicsúfolt, a legények a malomgödörbe löktek. Csak apám, Gáspár, a molnár szeretett. Ma már
senki sem tudja, hogy én vagyok Kelemen, a molnárfiú. És ha a Holdkő ereje az enyém lesz, telihold
éjszakáján az egész völgy varjakká változik." Morvath valódi neve tehát Kelemen! Ha a polcok közt
kutatsz, [[konyv_polc]]. Ha visszamész a csarnokba, [[csarnok_kozep]].''', gain('nev'), st(E, 2))

sec('konyv_polc', '''A polcok között a suhogás erősödik, és hirtelen tucatnyi könyv röppen le a polcokról. Úgy csapkodnak a
fedelükkel, mint a szárnyakkal, és az éles lapjaikkal vágnak. Meg kell küzdened velük, mintha
egyetlen ellenfél volnának. Ha legyőzöd őket, [[konyv_kincs]].''',
    fight([M('Repülő könyvek', 6, 6)], T('konyv_kincs')))

sec('konyv_kincs', '''A könyvek tépett lapokként hullanak a padlóra. Az egyik polc mögül, amit a könyvek őriztek, egy
titkos fülke tárul fel. Benne egy vastag, zöld bőrkötésű varázskönyv: a fedelén Varga Borcsa neve!
Ez az, amit Morvath ellopott tőle. Mellette egy tekercs: a torony alaprajza, rajta a pecsétes ajtó
és a három jel: Nap, csillag, Hold. Ha visszamész a csarnokba, [[csarnok_kozep]].''', iff('!terkep', gain('terkep')))

sec('alkimia', '''Morvath műhelyében lombikok, üstök és fortyogó üvegek sorakoznak. Egy asztalon három kis üvegcse áll,
egy piros, egy kék és egy fekete. Az asztal mögött egy macskanagyságú, ráncos bőrű kis lény ül,
a fején kis szarvak: egy homunkulusz, Morvath szolgája. Rémülten pislog rád. Ha a homunkuluszhoz
fordulsz, [[homunkulusz]]. Ha megiszod a piros üvegcsét, [[ital_piros]]. Ha a kéket, [[ital_kek]]. Ha a
feketét, [[ital_fekete]]. Ha a tűz fölött bugyborékoló nagy lombikhoz lépsz, [[alkimia_lombik]]. Ha
visszamész a csarnokba, [[csarnok_kozep]].''')

sec('homunkulusz', '''- Ne bánts! - cincogja a homunkulusz. - Én csak takarítok! - Remegve néz rád. - A gazdám, Morvath,
mindig azt mondja, hogy a piros az erő, a kék az ügyesség, a fekete pedig... a fekete az átkozott.
Azt csak az ellenségeinek adja. - Közelebb hajol. - Ha jó vagy hozzám, elmondom, hogyan
működik a pecsétes ajtó! Ha megígéred neki, hogy nem bántod, [[homunkulusz_titok]]. Ha visszamész
az asztalhoz, [[alkimia]].''')

sec('homunkulusz_titok', '''- A gazdám mindig így mondja, amikor megnyomja a jeleket: "Hajnalban felkel a Nap, este kigyúlnak a
csillagok, éjjel feljön a Hold." - A homunkulusz büszkén kihúzza magát. - És még valamit: ha
legyőzik, a gazdám halálos átkot mond. Én is félek tőle. - Elbújik az asztal alá. Visszamész az
asztalhoz: [[alkimia]].''', st(SZ, 1))

sec('ital_piros', '''A piros ital ízre olyan, mint a fahéjas bor. Melegség árad szét a testedben, és a sebeid begyógyulnak.
Visszanyersz 6 ÉLETERŐ pontot. Visszamész az asztalhoz: [[alkimia]].''', st(E, 6))

sec('ital_kek', '''A kék ital hideg és bizsergető, mint a hegyi patak. A kezed biztosabb lesz, a szemed élesebb. Az
ÜGYESSÉGED 1 ponttal nő, a kezdeti értékén túl is. Visszamész az asztalhoz: [[alkimia]].''', st(U, 1))

sec('ital_fekete', '''A fekete ital keserű, mint az epe. Azonnal görcsbe rándul a gyomrod, és a világ elsötétül előtted.
Morvath átka! Elveszítesz 4 ÉLETERŐ és 2 SZERENCSE pontot. Ha van holdvirágod, megrághatod egy szirmát,
és a méreg ereje megtörik: [[ital_holdvirag]]. Ha nincs, a földre rogysz, és amikor magadhoz térsz,
visszamész az asztalhoz: [[alkimia]].''', st(E, -4), st(SZ, -2), gate(T('ital_holdvirag'), 'holdvirag'))

sec('ital_holdvirag', '''A holdvirág hűvös íze kitisztítja a fejed, és a görcsök elmúlnak. Visszanyersz 4 ÉLETERŐ pontot.
Visszamész az asztalhoz: [[alkimia]].''', st(E, 4))

sec('lepcso', '''A csigalépcső a torony falában kanyarog fölfelé. A lépcsőfokok kopottak, és a falon fáklyák
pislákolnak. A harmadik fordulóban egy lépcsőfok különösen fényes, mintha senki sem lépne rá. Ha
átlépsz rajta, [[lepcso_tovabb]]. Ha rálépsz, [[lepcso_csapda]].''')

sec('lepcso_csapda', '''Ahogy rálépsz, kattanás hallatszik, és a fal réseiből éles pengék csapnak ki! Tedd próbára az
ügyességedet! Ha sikerül, félreugrasz: [[lepcso_tovabb]]. Ha nem, a pengék megsebeznek: [[lepcso_seb]].''',
    skill(T('lepcso_tovabb'), T('lepcso_seb')))

sec('lepcso_seb', '''A pengék a combodba és a karodba vágnak. Elveszítesz 4 ÉLETERŐ pontot. Bekötöd a sebeidet, és
sántikálva folytatod az utad fölfelé: [[lepcso_tovabb]].''', st(E, -4))

sec('lepcso_tovabb', '''A lépcső egy hosszú folyosóra vezet a torony legfelső szintjén. A folyosón több ajtó is nyílik:
egy díszes, bíborfüggönyös ajtó, egy tükrökkel kirakott ajtó, és egy egyszerű tölgyfa ajtó, mögüle
károgás és röhögés hallatszik. A folyosó végén egy létra vezet fel a tetőre, és mellette egy hatalmas,
fekete kőajtó áll, rajta három faragott jel. Ha a bíborfüggönyös ajtón mész be, [[halo]]. Ha a
tükrös ajtón, [[tukorterem]]. Ha a tölgyfa ajtón, [[orszoba]]. Ha a létrán a tetőre mész, [[tetoterasz]].
Ha a fekete kőajtóhoz, [[pecset]]. Ha lemész a csarnokba, [[csarnok_kozep]].''')

sec('halo', '''Morvath hálószobája fényűző: bíbor kárpitok, egy hatalmas ágy, és egy íróasztal, rajta egy
kristálygömb. A gömbben füst kavarog. Ha belenézel a kristálygömbbe, [[kristalygomb]]. Ha átkutatod az
íróasztalt, [[halo_asztal]]. Ha benézel az ágy alá, ahol egy vasalt ládika sötétlik, [[halo_lada]]. Ha kimész a folyosóra, [[lepcso_tovabb]].''')

sec('kristalygomb', '''A gömbben a füst szétoszlik, és egy kép jelenik meg: egy öreg molnár ül egy konyhában, és egy
fiatal legény rajzát nézi. Gáspár! Az öreg könnyezik. A kép elhalványul, és egy hang suttog: "Mindig
ezt nézi. Minden éjjel." Morvath tehát figyeli az apját. Talán még nem halt meg benne egészen
Kelemen. Ha átkutatod az íróasztalt, [[halo_asztal]]. Ha kimész a folyosóra, [[lepcso_tovabb]].''',
    st(SZ, 1))

sec('halo_asztal', '''Az íróasztal fiókjában egy erszényt találsz, benne hét aranytallér, és egy összegyűrt, régi
levelet. Egy gyermek kézírása: "Apám, ne haragudj, hogy elmegyek. Nem bírom tovább, hogy kinevetnek.
Egyszer erős leszek, és mind megfizetnek. Kelemen." Elteszed az aranyat. Ha belenézel a
kristálygömbbe, [[kristalygomb]]. Ha kimész a folyosóra, [[lepcso_tovabb]].''', gold(7), gain('nev'))

sec('tukorterem', '''A tükrös ajtó mögött egy kerek terem, a falai, a padlója és a mennyezete is tükörből van. Ezer
önmagadat látod. Ahogy beljebb lépsz, az egyik tükörképed nem mozdul veled: rád vigyorog, és kilép
a tükörből, a kezében a te kardod mása. A saját árnyékoddal kell megküzdened! Ha harcolsz vele,
[[arnyek]]. Ha összetöröd a tükröt, amiből kilépett, [[tukor_tor]].''')

sec('arnyek', '''Az árnyékod pontosan olyan ügyes, mint te, és minden mozdulatodat ismeri. Meg kell küzdened vele.
Ha legyőzöd, [[arnyek_gyoz]].''', fight([M('Az árnyékod', 9, 8)], T('arnyek_gyoz')))

sec('tukor_tor', '''A kardod markolatával belecsapsz a tükörbe. Csörömpölve törik szét, és az árnyékod felsikolt, és
üvegszilánkokká hullik szét. De a szilánkok megsebeznek. Elveszítesz 2 ÉLETERŐ és 1 SZERENCSE
pontot; a tükörtörés balszerencsét hoz. [[arnyek_gyoz]].''', st(E, -2), st(SZ, -1))

sec('arnyek_gyoz', '''A terem elcsendesedik. A tükrök most már csak a saját képedet mutatják, fáradtan és sebesülten.
A terem közepén, a padlón egy kis ezüstkulcs csillog, ahol az árnyékod eltűnt. Hasonlít a toronykapu
kulcsára. Elteszed. Kimész a folyosóra: [[lepcso_tovabb]].''', iff('!ezustkulcs', gain('ezustkulcs')))

sec('orszoba', '''A tölgyfa ajtó mögött egy őrszoba van. Két emberforma, de varjúfejű lény ül egy asztalnál, és
kockáznak. A falon lándzsák. Ahogy belépsz, felugranak, és a lándzsák után kapnak. Ha van
varjútollad, megpróbálhatod elhitetni velük, hogy Morvath küldött: [[orszoba_toll]]. Ha harcolsz
velük, [[varjuemberek]]. Ha kihátrálsz, [[lepcso_tovabb]].''', gate(T('orszoba_toll'), 'varjutoll'))

sec('orszoba_toll', '''- A Mester küldött - mondod, és a tollra mutatsz a sapkádon. A varjúemberek összenéznek, és károgva
tanakodnak. Tedd próbára a szerencsédet! Ha szerencséd van, hisznek neked: [[orszoba_hisz]]. Ha nincs,
rájönnek a cselre: [[varjuemberek]].''', luck(T('orszoba_hisz'), T('varjuemberek')))

sec('orszoba_hisz', '''- A Mester! - hajolnak meg a varjúemberek. - Parancsolj! - Azt parancsolod nekik, hogy menjenek le a
csarnokba, és őrizzék a kaput. Engedelmesen elkárognak. Az asztalukon hagyott kockák mellett négy
aranytallér hever. Elteszed. Kimész a folyosóra: [[lepcso_tovabb]].''', gold(4))

sec('varjuemberek', '''A varjúemberek lándzsát szegezve rád rontanak. Egyenként küzdesz meg velük. Ha mindkettőt legyőzöd,
[[varjuemberek_gyoz]].''', fight([M('Első varjúember', 7, 7), M('Második varjúember', 7, 6)], T('varjuemberek_gyoz')))

sec('varjuemberek_gyoz', '''A varjúemberek holtan fekszenek a padlón. Az asztalukon négy aranytallér, és egy korsó bor. Egy
kortyot iszol belőle, és erőre kapsz. Visszanyersz 2 ÉLETERŐ pontot. Kimész a folyosóra:
[[lepcso_tovabb]].''', gold(4), st(E, 2))

sec('tetoterasz', '''A torony lapos tetején állsz. A szél süvít, a völgy messze alattad. A terasz közepén egy kőoltár áll,
rajta egy csillagászati műszer, és a peremén varjak ülnek. Egy csapóajtó vezet le a torony legfelső
szintjére, a pecsétes ajtó folyosójára. A varjak károgni kezdenek. Ha van varjútollad, [[terasz_toll]].
Ha nincs, [[terasz_varjak]].''', gate(T('terasz_toll'), 'varjutoll'), gate(T('terasz_varjak'), '!varjutoll'))

sec('terasz_toll', '''A varjak meglátják a tollat, és elcsendesednek. Az oltáron lévő műszeren a Nap, a csillagok és a
Hold vannak bevésve, egymás után, egy körben. Mellettük egy felirat: "A nap rendje szerint". Lemászol a
csapóajtón át a folyosóra: [[lepcso_tovabb]].''')

sec('terasz_varjak', '''A varjak felrebbennek, és károgva köröznek a fejed körül. Nem támadnak, de a lármájuk messze
hallatszik. Morvath most már tudja, hogy itt vagy. Elveszítesz 1 SZERENCSE pontot. Sietve
lemászol a csapóajtón át a folyosóra: [[lepcso_tovabb]].''', st(SZ, -1))

sec('pecset', '''A fekete kőajtón három faragott jel van, egymás mellett: egy sugaras Nap, egy ötágú csillag és
egy holdsarló. Mindegyik jel egy-egy kőkorong, amit be lehet nyomni. A korongok fölött egy felirat:
"Aki a rendet nem ismeri, égjen el." Melyiket nyomod meg elsőként? Ha a Napot, [[pecset_nap]]. Ha a
csillagot, [[pecset_r1]]. Ha a Holdat, [[pecset_r2]]. Ha inkább visszamész a folyosóra,
[[lepcso_tovabb]].''')

sec('pecset_nap', '''A Nap korongja mély hangon kattanva benyomódik, és aranyszínű fény gyúl a sugaraiban. Melyiket
nyomod meg másodikként? Ha a csillagot, [[pecset_csillag]]. Ha a Holdat, [[pecset_r3]].''')

sec('pecset_r1', '''A csillag korongja kattanva benyomódik, de a csúcsai nem ezüstösen, hanem vörösen kezdenek izzani.
A kőajtó felhorkan, mint egy élőlény, és a résein forró füst tör elő. [[pecsetrossz]].''')

sec('pecset_r2', '''A holdsarló korongja benyomódik, és egy pillanatig hideg, fehér fény önti el a folyosót. Aztán a
fény vörösre vált, és a kőajtó mélyéről morajlás hallatszik, mintha egy kemence ajtaja nyílna
ki. [[pecsetrossz]].''')

sec('pecset_r3', '''A holdsarló korongja benyomódik, de a Nap sugaraiban az aranyszínű fény kialszik, mintha a
Hold eltakarta volna. Napfogyatkozás! A kőajtó haragosan megremeg. [[pecsetrossz]].''')

sec('pecset_csillag', '''A csillag korongja is benyomódik, és ezüstös fény gyúl a csúcsain. Már csak egy maradt: a Hold.
Megnyomod. [[pecsetjo]].''')

sec('pecsetrossz', '''A korong benyomódik, de a jel vörösen izzani kezd, és a kőajtóból tűz csap ki! Hátraugrasz, de a láng
megperzsel. Elveszítesz 3 ÉLETERŐ pontot. A korongok visszaugranak a helyükre. Ha újra
megpróbálod, [[pecset]]. Ha visszamész a folyosóra, [[lepcso_tovabb]].''', st(E, -3))

sec('pecsetjo', '''A Hold korongja is benyomódik, és a három jel egyszerre felragyog: arany, ezüst és fehér fénnyel. A
fekete kőajtó hangtalanul kitárul. Mögötte egy kör alakú terem, a mennyezete üvegkupola, amelyen át
a telihold előtti utolsó este csillagai látszanak. A terem közepén egy oltáron ott ragyog a Holdkő,
és mellette, háttal neked, egy fekete köpenyes alak áll. [[morvath_terem]].''')

sec('konyv_tiltott', '''A fekete könyv lapjai sötétek, és a betűk vörösen izzanak rajtuk, mint a parázs. Ahogy olvasni
kezded, a szavak maguktól formálódnak a szádon, és egy idegen, rekedt hang szól belőled. A
gyertyák lángja kékre vált, és a terem levegője megfagy. Valami közeledik a könyv lapjain át. Ha
abbahagyod az olvasást, és becsapod a könyvet, [[konyv_becsap]]. Ha tovább olvasol, hogy megtudd,
mit rejt, [[konyv_demon]].''')

sec('konyv_becsap', '''Minden erődet összeszedve becsapod a könyvet. A hang elhallgat a torkodban, a gyertyák lángja újra
sárga lesz. Tedd próbára a szerencsédet! Ha szerencséd van, az idézés megszakad, a vörös betűk kihunynak, és visszamehetsz a
könyvtár közepére: [[konyvtar]]. Ha nincs, a könyv fedele újra felpattan, és a lapjai közül fekete füst tör elő: [[konyv_fust]].''',
    luck(T('konyvtar'), T('konyv_fust')))

sec('konyv_fust', '''A fekete füst a torkodba tódul, és a tüdődet égeti. Köhögve, fuldokolva tántorogsz hátra, amíg a
füst lassan szétoszlik. Elveszítesz 4 ÉLETERŐ és 1 SZERENCSE pontot. A könyv a földre esett, és a
lapjai üresek: a démon visszatért oda, ahonnan jött. Ha az íróasztalhoz mész, [[konyv_naplo]]. Ha
visszamész a csarnokba, [[csarnok_kozep]].''', st(E, -4), st(SZ, -1))

sec('konyv_demon', '''Tovább olvasol, és a szavak egyre gyorsabban, egyre hangosabban törnek fel belőled. A könyv lapjai
közül egy fekete, szarvas fej emelkedik ki, a szeme két izzó parázs. - Ki hívott? - dörgi, és a
hangja a csontjaidig hatol. Mielőtt felelhetnél, a démon karmos keze kinyúlik a könyvből, és
magával ránt a lapok közé, a sötétségbe, ahonnan nincs visszaút. A kalandod itt véget ért.''')

sec('alkimia_lombik', '''A tűz fölött egy ember nagyságú lombik bugyborékol, benne sűrű, aranyszínű folyadék. A gőze édes és
kábító. A lombik mellett egy kis csap van, alatta egy üres kupa. Ha megtöltöd a kupát, és iszol
belőle (egyszer teheted meg), [[lombik_iszik]]. Ha
visszamész az asztalhoz, [[alkimia]].''', gate(T('lombik_iszik'), nvis('lombik_iszik')))

sec('lombik_iszik', '''Az aranyszínű folyadék édes, mint a méz, de utána égetni kezdi a torkodat. Tedd próbára a
szerencsédet! Ha szerencséd van, a varázsital ereje a javadra válik: az ÜGYESSÉGED, az ÉLETERŐD és a
SZERENCSÉD is visszanyeri a kezdeti értékét. Ha nincs, a méreg 3 ÉLETERŐ pontot vesz el. Visszamész
az asztalhoz: [[alkimia]].''', luck(), iff('res', [st(U, 12), st(E, 24), st(SZ, 12)], [st(E, -3)]))

sec('halo_lada', '''Az ágy alatt egy kis, vasalt ládika lapul, a zárja egy varjúfej, a csőrében egy apró tű. Ha
kinyitod a ládikát, [[halo_lada_nyit]]. Ha nem nyúlsz hozzá, [[halo]].''')

sec('halo_lada_nyit', '''Megfogod a varjúfejet, és elfordítod. A csőrből az apró tű a hüvelykujjadba szúr. Tedd próbára a
szerencsédet! Ha szerencséd van, a tű hegyén a méreg már régen kiszáradt: [[halo_kincs]]. Ha nincs,
[[halo_tu]].''', luck(T('halo_kincs'), T('halo_tu')))

sec('halo_tu', '''A hüvelykujjad elzsibbad, aztán a kezed, a karod, és a zsibbadás lassan a szíved felé kúszik. Le
akarsz ülni, de a lábad már nem engedelmeskedik. A ládika kinyílik a kezedben, és üres: Morvath
csak csapdának szánta. A bíbor kárpitok között egy varjú károg, és ez az utolsó, amit hallasz. A
kalandod itt véget ért.''')

sec('halo_kincs', '''A ládikában bíborbársonyon egy aranyozott hajtű, egy tincs ősz haj egy szalagon, és egy kis,
festett kép: egy fiatal asszony, a nyakában ugyanaz az ezüstgyűrű, amit Gáspár viselt. Kelemen
anyja. A hajtű tíz aranyat ér. Elteszed, a képet és a hajtincset pedig visszateszed a helyére. Ha
belenézel a kristálygömbbe, [[kristalygomb]]. Ha kimész a folyosóra, [[lepcso_tovabb]].''', gold(10))
