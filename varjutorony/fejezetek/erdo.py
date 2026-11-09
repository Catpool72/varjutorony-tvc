"""2. A Feketeerdő."""
from kv import *

sec('erdo', '''Az erdei út a fenyők közé kanyarodik, és pár száz lépés után a falu zaja elhal mögötted. Csend van,
csak a tűlevelek pattognak a talpad alatt. Egyszer csak morgás: az út közepén egy hatalmas, szürke
farkas áll, a szeme vörösen izzik, mint a parázs. Lassan közelebb lopakodik. Ha előrántod a kardod, és
szembeszállsz vele, [[farkas_harc]]. Ha megpróbálsz felkapaszkodni a legközelebbi fenyőre, [[farkas_fa]].
Ha van nálad elemózsia, és odadobod neki, [[farkas_etet]].''', gate(T('farkas_etet'), 'kenyer'))

sec('farkas_harc', '''A farkas rád veti magát, a fogai a karod felé kapnak. Meg kell küzdened vele. Ha legyőzöd,
[[farkas_utan]].''', fight([M('Vörös szemű farkas', 7, 6)], T('farkas_utan')))

sec('farkas_fa', '''Elrugaszkodsz, és elkapod a legalsó ágat. Ügyes vagy-e annyira, hogy feljuss, mielőtt a farkas
elkapja a lábad? Tedd próbára az ügyességedet! Ha sikerül, [[farkas_fan]]. Ha nem, a farkas a
bokádba mar, és lerángat a földre: [[farkas_lerant]].''', skill(T('farkas_fan'), T('farkas_lerant')))

sec('farkas_lerant', '''Hanyatt esel a tűlevelek közé, a bokád vérzik. A farkas fölötted áll. Nincs más hátra, meg kell
küzdened vele, de a sérült lábad miatt nehezebben mozogsz. Ha legyőzöd, [[farkas_utan]].''',
    st(E, -2), fight([M('Vörös szemű farkas', 7, 6)], T('farkas_utan'), skmod=-1))

sec('farkas_fan', '''Az ágak között ülve nézed, ahogy a farkas morogva köröz a fa alatt. Aztán, mintha valaki hívná,
felkapja a fejét, és eloson észak felé. A szeme vörös fénye sokáig látszik a fák között. Morvath
szolgája volt, biztosan. Óvatosan lemászol, és folytatod az utad: [[erdo_ut]].''')

sec('farkas_etet', '''Az elemózsiádból egy darab füstölt szalonnát dobsz a farkas elé. A fenevad megtorpan, megszagolja,
aztán mohón befalja. A vörös fény egy pillanatra kihuny a szemében, és egy közönséges, éhes, sovány
farkas néz rád. Aztán megrázza magát, és beoson a bozótba. Mintha egy varázslat szakadt volna meg.
Folytatod az utad: [[erdo_ut]].''', lose('kenyer'))

sec('farkas_utan', '''A farkas mozdulatlanul fekszik. Ahogy a szeme kihuny, a vörös fény füstként száll fel belőle, és
egy károgó hang hallatszik a magasból. Morvath tudja már, hogy jössz. A farkas nyakán egy
fekete bőrszíj, rajta egy varjútollal. Letéped, és elhajítod. Aztán lehajolsz, és megtörlöd a
kardod a fűben. Folytatod az utad: [[erdo_ut]].''')

sec('erdo_ut', '''Az út egy tisztáson vezet át. Jobbra kis füstcsík száll fel a fák közül: egy vadászkunyhó.
Balra fejszecsapások hallatszanak. Előtted az út tovább kanyarog észak felé, a kőkereszt felé, ahol
kettéválik. Az út szélén, a puha földben egy fiatal fiú csizmájának nyomát látod, frisset, legfeljebb
két naposat. Bence erre járt! Ha a vadászkunyhóhoz mész, [[vadasz]]. Ha a fejszecsapások irányába,
[[favago]]. Ha letérsz az útról, és a sűrűbe vágsz, [[surU]]. Ha tovább mész az úton a gázló felé,
[[erdo_ut2]]; ha a rablókkal már elszámoltál, [[gazlo]].''', gate(T('erdo_ut2'), '!rablo'), gate(T('gazlo'), 'rablo'))

sec('gazlo', '''A gázlónál most csend van, a rablók nem mutatkoznak. A patak hideg vize a térdedig ér, ahogy
átgázolsz rajta. A túlparton az út a domb felé kapaszkodik, ahol a kőkereszt áll. [[kokereszt]].''')

sec('erdo_ut2', '''Az út egy patak mellett halad. A gázlónál, ahol át kell kelned, három rongyos alak ugrik elő a
bokrokból, rozsdás kardokkal. - Vámot kell fizetni, vándor! - vigyorog a legnagyobb, akinek a fél
füle hiányzik. - Öt aranytallér, vagy itt hagyod a csontjaidat! Ha kifizeted az öt aranyat, [[rablo_fizet]].
Ha megtagadod, és kardot rántasz, [[rablo_harc]]. Ha azt mondod, hogy Morvath ellen mész, [[rablo_beszel]].''',
    gate(T('rablo_fizet'), ('gold', 5)))

sec('rablo_fizet', '''A félfülű elveszi az aranyakat, és meghajol. - Szép napot, uraság! - röhögnek, és visszabújnak a
bokrok közé. Átkelsz a gázlón. A túlparton azonban észreveszed, hogy egyikük óvatosan a nyomodba
szegődött. Ha megvárod egy fa mögött, [[rablo_kovet]]. Ha nem törődsz vele, és sietsz tovább, [[kokereszt]].''',
    gold(-5), gain('rablo'))

sec('rablo_kovet', '''Előugrasz a fa mögül, és a rabló a földre huppan ijedtében. Egy vékony, ijedt kamasz az. -
Ne bánts! Csak... csak meg akartam mondani, hogy Lajos, a vezérünk, rabol, de nem gyilkos. És
láttuk a fiút, a Bodorét. A sasbércek felé ment, a hágón át. Azt mondta, a remete majd segít neki.
- Elszalad. Folytatod az utad a kőkereszt felé: [[kokereszt]].''')

sec('rablo_harc', '''A három rabló körbevesz. Egyenként kell megküzdened velük, de úgy, hogy a többiek közben ott
állnak körülötted. Ha mindhármat legyőzöd, [[rablo_gyoz]].''',
    fight([M('Félfülű Lajos', 7, 7), M('Kampós Jóska', 6, 5), M('Sovány Kristóf', 5, 4)], T('rablo_gyoz')))

sec('rablo_gyoz', '''Lajos a földre rogy, a másik kettő elinal. A rablóvezér zsákjában hat aranytallért, és egy köteg
furcsa, hajlított drótot találsz: tolvajkulcsot. - Bármit kinyit - nyögi Lajos. - A torony börtönében
is... ott tartják a fiút. Mi láttuk, amikor a varjak elvitték. - Eszméletlenül hanyatlik hátra. Ha
átkutatod a rablók búvóhelyét is a bokrok mögött, [[rablo_tanya]]. Ha továbbmész, [[kokereszt]].''',
    gold(6), gain('tolvajkulcs'), gain('rablo'))

sec('rablo_tanya', '''A bokrok mögött egy ágakból font kunyhó áll. Bent szalmazsák, egy üres boroshordó és egy ládika.
A ládikában egy elsárgult levél van, Morvath varjúpecsétjével: "Aki a toronyba hozza a fenyvesvölgyi
vén unokáját, húsz aranyat kap." Bence életére vadásztak! A ládika alján egy kis üvegcse is van,
zöld folyadékkal. Ha elteszed az üvegcsét, [[rablo_uveg]]. Ha nem nyúlsz hozzá, és továbbmész,
[[kokereszt]].''')

sec('rablo_uveg', '''Az üvegcsét elteszed. A dugója alatt mérgesen zöld folyadék lötyög, erős, keserű szaga van. Nem
tudod, mi lehet. Talán gyógyír, talán méreg. Talán megtudod egyszer. Továbbmész a kőkereszt felé:
[[kokereszt]].''', gain('meregital'))

sec('rablo_beszel', '''- Morvath? - A félfülű elsápad. - Az a varjúördög? - A társai összenéznek. - Ha ellene mész, nem
fosztunk ki. Úgyis meghalsz. - Lajos a fejét vakarja. - Hallod-e, egy tanács ingyen: a toronykapu
őrei csontból vannak. Az ezüst ellenük jó. És a remete a hágón többet tud, mint bárki. - Átengednek a
gázlón, de előbb próbára kell tenned a szerencsédet. Ha nincs szerencséd, Lajos azért elkér két
aranytallért "a szegény rablók javára". Ha továbbmész, [[kokereszt]].''', luck(), iff('!res', [gold(-2)]), gain('rablo'))

sec('vadasz', '''A kunyhó előtt egy idős vadász, Gergely ül, a karja véres rongyokba bugyolálva. - A farkasok -
mondja rekedten. - Nem közönséges farkasok. Egy falka jár erre, a vezérük vörös szemű, akkora, mint
egy borjú. A barlangjuk a Kőfejnél van, nem messze innen. Ha bekötöd a sebét, [[vadasz_seb]]. Ha
megkérdezed, mit tud a farkasok barlangjáról, [[vadasz_barlang]]. Ha visszamész az útra, [[erdo_ut]].''')

sec('vadasz_seb', '''Kimosod a sebét a patak vizében, és tiszta vászonnal kötöd be. Gergely hálásan bólint. - Nem
vagy rossz ember. - A kunyhóból egy nagy darab füstölt húst hoz ki. - Vidd el. A hegyekben jól
jöhet, az ott fent nem talál ennivalót, aki nem ismeri a járást. - Elteszed. Ha megkérdezed, mit
tud a farkasok barlangjáról, [[vadasz_barlang]]. Ha visszamész az útra, [[erdo_ut]].''', gain('hus'))

sec('vadasz_barlang', '''- A Kőfejnél, a sziklafal tövében - mondja Gergely. - Ott tanyázik a vezér. A szemem sarkából
láttam, hogy egy varjú ül a vállán, és beszél hozzá. Ha a vezért megölöd, a falka szétszéled. A
barlangban sok csont van, emberé is. Egy lovag is odaveszett, tavaly ősszel; a kardja fényesebb
volt a holdnál. Ha elindulsz a farkasbarlang felé, [[farkasbarlang]]. Ha visszamész az útra,
[[erdo_ut]].''')

sec('farkasbarlang', '''A Kőfej egy emberarcra emlékeztető szikla az erdő mélyén. Tövében sötét barlangszáj tátong, csontok
hevernek előtte. Bentről morgás hallatszik. Ha belépsz a barlangba, [[farkasbarlang_be]]. Ha
megvárod, amíg a vezér előjön, és lesből támadsz, [[farkas_les]]. Ha mégis inkább visszafordulsz
az útra, [[erdo_ut]].''')

sec('farkas_les', '''Bebújsz egy bokor mögé, és vársz. Órák telnek el. Alkonyatkor a barlang szájában megjelenik egy
óriási, szürke farkas, vörösen izzó szemmel. Megszimatolja a levegőt. Tedd próbára a szerencsédet!
Ha szerencséd van, a szél feléd fúj, és nem érzi a szagodat: [[farkas_les_jo]]. Ha nincs,
észrevesz: [[farkasvezer]].''', luck(T('farkas_les_jo'), T('farkasvezer')))

sec('farkas_les_jo', '''A vezér elhalad a bokrod mellett. Hátulról ugrasz rá, és mielőtt megfordulhatna, a kardod mélyen
a vállába hatol. Felüvölt, és szembefordul veled, de már sebesült. Meg kell küzdened vele. Ha
legyőzöd, [[farkas_kincs]].''', fight([M('Vörösszem, a falka vezére', 8, 5)], T('farkas_kincs')))

sec('farkasbarlang_be', '''A barlang bűzös és sötét. Ahogy beljebb lépsz, két kisebb farkas ugrik rád a sötétből! Egyszerre
kell velük megküzdened. Ha legyőzöd őket, [[farkasvezer]].''',
    fight([M('Első farkas', 6, 5), M('Második farkas', 6, 4)], T('farkasvezer'), all=1))

sec('farkasvezer', '''A barlang mélyéből egy borjúnyi, szürke farkas lép elő. A szeme vörösen izzik, a vállán egy
fekete varjú ül, és károg: - Morvath üdvözöl, bolond! - A farkas rád veti magát. Meg kell küzdened
vele. Ha legyőzöd, [[farkas_kincs]].''', fight([M('Vörösszem, a falka vezére', 9, 9)], T('farkas_kincs')))

sec('farkas_kincs', '''A vezér holtan fekszik, a varjú károgva elrepül. A barlang mélyén megtalálod a szerencsétlen
lovag maradványait. A csontjai között egy ezüsttőr csillog, és egy erszény, benne négy aranytallér.
A falon egy véstet látsz: valaki karcolta, haldokolva: "Ábris őr kincse a lovagok sírjában. A halál
szava ellen." Elteszed, amit találtál, és kijössz a barlangból: [[farkas_vissza]].''',
    gain('ezusttor'), gold(4), st(SZ, 1))

sec('farkas_vissza', '''Mire visszaérsz Gergely kunyhójához, beesteledik. A vadász meghallgatja a történetedet, és a
szeme könnybe lábad. - A falka nem bánt többé senkit. Itt alhatsz éjszakára. - A tűz mellett
megvacsorázol, és nyugodtan alszol. Reggel Gergely elkísér az útig. - Ha a hágón mész, a sasbércen
egy nagy sas fészkel. Ha a fiókáját megeteted, az anyja a barátod lesz. Visszatérsz az útra:
[[erdo_ut]].''', st(E, 4), iff('!hus', gain('hus')))

sec('favago', '''Egy tisztáson egy kidőlt fenyő alatt egy favágó fekszik, a lába a törzs alá szorult. - Segíts! -
nyögi. - Fábián vagyok, a Részeg Kecskében iszogató favágó öccse. Egy órája fekszem itt. Ha
megpróbálod felemelni a törzset, [[favago_emel]]. Ha a kötelet egy ágon átvetve próbálsz emelőt
csinálni, [[favago_kotel]]. Ha nem törődsz vele, és visszamész az útra, [[erdo_ut]].''',
    gate(T('favago_kotel'), 'kotel'))

sec('favago_emel', '''Megmarkolod a fenyőtörzset, és minden erődet beleadod. Tedd próbára az ügyességedet! Ha sikerül,
[[favago_ment]]. Ha nem, a hátadba éles fájdalom nyilall, és a törzs visszazuhan: [[favago_emel2]].''',
    skill(T('favago_ment'), T('favago_emel2')))

sec('favago_emel2', '''Pihensz egy kicsit, aztán újra nekifeszülsz. A hátad sajog, de most sikerül annyira megemelned a
törzset, hogy Fábián kihúzza a lábát. Elveszítesz 2 ÉLETERŐ pontot. [[favago_ment]].''', st(E, -2))

sec('favago_kotel', '''A kötelet átveted egy erős ágon, és a végét a törzshöz kötöd. Teljes súlyoddal húzod, a fenyő
nyikorogva felemelkedik, és Fábián kihúzza a lábát a csapdából. Szerencsére nem tört el. [[favago_ment]].''')

sec('favago_ment', '''Fábián felül, és megdörzsöli a lábát. - Az életemet köszönhetem neked. Nincs pénzem, de mondok
valamit, ami többet ér. A lápban, ahol a révész lakik, ott a régi malom, ahova a láp fölötti falu
molnárai jártak. Gáspár öreg molnár mondta egyszer, hogy a torony régi gazdái ott rejtették el a
kapu ezüstkulcsát, a malomkerék alatti mélységben. - Ad egy cipót is. Visszamész az útra: [[erdo_ut]].''',
    gain('kenyer'))

sec('surU', '''A sűrűben alig haladsz, a tüskés bokrok tépik a ruhádat. Egy idő után egy tisztásra érsz, ahol
gombák nőnek tökéletes körben. A kör közepén a fű ezüstösen csillog. A tisztás túloldalán, egy
vén tölgy alatt furcsa, mohos kunyhót látsz, a kéménye zöld füstöt ereget. Ha belépsz a gombakörbe,
[[tunderkor]]. Ha a kunyhóhoz mész, [[borcsa]]. Ha visszamész az útra, [[erdo_ut]].''')

sec('tunderkor', '''Ahogy belépsz a körbe, halk zene csendül fel, és apró, áttetsző szárnyú lények kezdenek körülötted
táncolni. - Táncolj velünk, halandó! - csilingelik. Ha velük táncolsz, [[tunder_tanc]]. Ha udvariasan
megköszönöd, és kilépsz a körből, [[tunder_ki]].''')

sec('tunder_tanc', '''Táncolsz a tündérekkel, és az idő megszűnik. Amikor a zene elhallgat, nem tudod, mennyi idő
telt el: egy óra vagy egy nap. Tedd próbára a szerencsédet! Ha szerencséd van, a tündérek
megajándékoznak: [[tunder_ajandek]]. Ha nincs, kifosztottan és kimerülten ébredsz a fűben:
[[tunder_kifoszt]].''', luck(T('tunder_ajandek'), T('tunder_kifoszt')))

sec('tunder_ajandek', '''A tündérkirálynő, egy fénylő, ujjnyi asszonyka megérinti a homlokodat. - Jól táncoltál. Az erőd
legyen teljes! - Egész testedben frissességet érzel. - És vidd magaddal a tudást is: a lápi banya a
holdvirágért egy szép tükörképet kér, mert a magáét régen elvesztette. - A tündérek eltűnnek. Kilépsz a
körből: [[tunder_ki]].''', st(E, 6), st(SZ, 1))

sec('tunder_kifoszt', '''Fázva ébredsz a hideg fűben, a nap már magasan jár. Az erszényed könnyebb: a tündérek elvitték a
fényes aranyaid egy részét. És fáradtabb vagy, mint valaha. Elveszítesz 3 aranytallért és 2 ÉLETERŐ
pontot. Tápászkodva kilépsz a körből: [[tunder_ki]].''', gold(-3), st(E, -2))

sec('tunder_ki', '''Kilépsz a gombakörből, és a zene elhalkul. A tisztás túloldalán a mohos kunyhó kéménye zöld
füstöt ereget. Ha a kunyhóhoz mész, [[borcsa]]. Ha visszavágsz az útra, [[erdo_ut]].''')

sec('borcsa', '''Kopogtatsz. Az ajtót egy görbe hátú, hosszú orrú öregasszony nyitja ki, a vállán egy fekete macska.
- Varga Borcsa vagyok - károgja. - Mit akarsz, vándor? Varázslatot, jóslatot vagy egy jó tanácsot?
A kunyhó tele van üvegekkel, szárított békákkal és tükrökkel. Ha udvariasan köszönsz, és bemutatkozol,
[[borcsa_udv]]. Ha azt mondod, hogy Morvath ellen mész, [[borcsa_morvath]]. Ha szó nélkül hátat
fordítasz, és visszamész az útra, [[erdo_ut]].''')

sec('borcsa_udv', '''Borcsa elégedetten csettint. - Végre egy jól nevelt vándor! Gyere be. - Teával kínál, ami furcsa
szagú, de jólesik. - Egy jóslatot ingyen kapsz: kétszer fogsz a halállal szembenézni, és csak egyszer
mentheted meg magad a saját erődből. - Aztán ravaszul hunyorít. - A többiért fizetni kell. Ha
megkérdezed, mit kér a segítségéért, [[borcsa_ar]]. Ha megkéred, hogy bővebben is jósoljon neked,
[[borcsa_jos]]. Ha megköszönöd, és távozol, [[erdo_ut]].''',
    st(E, 2), gain('borcsa'))

sec('borcsa_morvath', '''Az öregasszony arca elsötétül. - Morvath! Az a varjas taknyos! Valaha hozzám járt tanulni, aztán
ellopta a legjobb varázskönyvemet. - A macska fújni kezd. - Ha ellene mész, segítek. De ingyen semmi
sincs. Ha megkérdezed, mit kér a segítségéért, [[borcsa_ar]]. Ha inkább távozol, [[erdo_ut]].''',
    gain('borcsa'))

sec('borcsa_ar', '''- Két dolgom van, ami neked kell - mondja Borcsa. - Egy varjútoll, amitől Morvath varjai a
sajátjuknak hisznek, és egy ezüsttükör, ami visszaveri a gonosz pillantást. A katakombákban egy
kőpillantású őr jár: aki a szemébe néz, kővé válik. Mindkettőért négy aranyat kérek. Vagy hozz
nekem valamit, ami érdekel. Ha fizetsz, és vásárolsz, megteheted most. Ha felajánlasz neki egy
furcsa zöld üvegcsét, [[borcsa_uveg]]. Ha végeztél, és távozol, [[erdo_ut]].''',
    shop(('varjutoll', 4), ('tukor', 4)), gate(T('borcsa_uveg'), 'meregital'))

sec('borcsa_uveg', '''Borcsa szeme felcsillan, amikor meglátja a zöld üvegcsét. - Sárkányfű-kivonat! Halálos méreg, ha
megiszod, de én tudok vele bánni. - Kiveszi a kezedből. - Fejében válassz: a tükör vagy a toll.
Ha a tükröt választod, [[borcsa_tukor]]. Ha a varjútollat, [[borcsa_toll]].''', lose('meregital'))

sec('borcsa_tukor', '''Borcsa egy kis, ezüstkeretes tükröt ad át. A lapja olyan tiszta, mint a hegyi patak. - Ha a
kőpillantású őrrel találkozol, fordítsd felé, és ne nézz rá. A saját pillantása öli meg. - Elteszed a
tükröt, és elbúcsúzol a boszorkánytól: [[erdo_ut]].''', gain('tukor'))

sec('borcsa_toll', '''Borcsa egy hosszú, kékesen fénylő varjútollat húz ki egy agyagkorsóból. - Tűzd a sapkádba, és
Morvath varjai nem riasztják az urukat, ha meglátnak. Azt hiszik, közéjük tartozol. - Elteszed a
tollat, és elbúcsúzol a boszorkánytól: [[erdo_ut]].''', gain('varjutoll'))

sec('kokereszt', '''Az út egy dombtetőn ér véget, ahol egy mohos kőkereszt áll. Mellette egy apró, fehérre meszelt
kápolnácska, az ajtaja nyitva. Innen két út indul tovább: nyugatra lefelé, a láp ködös síksága felé,
keletre fölfelé, a hágó sziklái felé. Ha bemész a kápolnácskába, [[kapolnacska]]. Ha körülnézel a
kereszt körül, [[elagazas]].''')

sec('kapolnacska', '''A kápolnácska belsejében egy kis, festett Mária-szobor áll, előtte elhervadt mezei virágok. A falon
egy régi felirat: "Vándor, ki itt megpihensz, a Hold anyja vigyáz rád." Letérdelsz, és imádkozol egy
rövid ideig. Békesség száll rád, és az elfáradt tagjaid megnyugszanak. Ha kijössz a kápolnából,
[[elagazas]].''', st(SZ, 2), st(E, 2))

sec('elagazas', '''A kőkeresztnél állsz, ahol az út kettéválik. A kereszt tövébe valaki friss vadvirágot tett, és
egy szénnel írt cédulát: "Nagyapa, a hágón át megyek. Bence." A nyugati út a Suttogó-lápon át, Csobán
révész csónakjával vezet a toronyig; a keleti a Kőkapu-hágón, a hegyeken át. Ha nyugatra mész, a láp
felé, [[lap1]]. Ha keletre, a hágó felé, [[hago1]]. Ha visszamész az erdőbe, [[erdo_vissza]].''')

sec('erdo_vissza', '''Visszafordulsz az erdei úton. A fák között az út ismerősnek tűnik. Ha a vadászkunyhóhoz mész,
[[vadasz]]. Ha a favágók tisztására, [[favago]]. Ha letérsz a sűrűbe, a boszorkány kunyhója felé,
[[surU]]. Ha mégis visszafordulsz a kőkereszthez, [[elagazas]]. Ha egészen hazamész Fenyvesvölgybe,
[[haza_falu]].''')

sec('haza_falu', '''Délutánra visszaérsz Fenyvesvölgybe. A kapuőr meglepve néz rád, de beenged. A falu csendes, a
lakók az ablakokból figyelnek. Talán elfelejtettél valamit? A főtérre mész: [[ter]].''')

sec('borcsa_jos', '''Borcsa egy marék csontot vesz elő egy bőrzacskóból, és az asztalra szórja. Hosszan nézi őket, és a
macskája is lekuporodik mellé. - Egy torony, ami leomlik - mormolja. - Egy fiú egy sötét lyukban. Egy
öreg ember, aki egy rajzot néz. És egy név, amit egy apa kiált. - Felnéz rád. - A varjak urát nem a kard
győzi le, vándor. Az csak a legrosszabb út. - Összesöpri a csontokat. - Ennyi. Többet nem mondhatok, mert
a csontok elhallgattak. Ha megkérdezed, mit kér a segítségéért, [[borcsa_ar]]. Ha megköszönöd, és
távozol, [[erdo_ut]].''', st(SZ, 1))
