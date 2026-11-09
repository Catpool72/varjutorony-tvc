"""1. Fenyvesvölgy, a falu."""
from kv import *

sec('kezdet', '''Fenyvesvölgy főterén állsz. A házak ablakait bedeszkázták, a kút mellett egy ősz szakállú öregember
vár rád: Bodor, a falu vénje. - Hát eljöttél - mondja fáradtan. - Morvath, a varjak ura ellopta a
Holdkövet a kápolnából. És ez még nem minden: az unokám, Bence a nyomába eredt, és két napja nem jött
haza. Ha visszahozod a követ, a falu minden aranya a tiéd. Ha a fiút is... - elcsuklik a hangja, és a
kezedbe nyom egy kis erszényt. - Ennyi telik tőlünk. Költsd okosan! A téren túl a Részeg Kecske fogadó
lámpása ég; ha ott tudakozódnál, [[fogado]]. A kovácsműhelyből kalapácsszó hallatszik; ha oda mennél,
[[kovacs]]. A tér sarkán Gyopár, a füvesasszony kunyhója áll; ha meglátogatod, [[fuvesno]]. Ha a falu
utcáit járnád be, [[utca]]. Ha azonnal útnak indulnál az északi kapu felé, [[kapu]].''')

sec('ter', '''Visszatérsz a főtérre. A szél zörgeti a bedeszkázott ablakokat, a kútkáván egy varjú ül, és fél
szemmel figyel. Amikor ránézel, károgva elrepül észak felé. Ha a fogadóba mész, [[fogado]]. Ha a
kovácshoz, [[kovacs]]. Ha a füvesasszonyhoz, [[fuvesno]]. Ha a falu utcáit járnád be, [[utca]]. Ha a
kúthoz lépsz, [[kut_f]]. Ha elindulsz az északi kapu felé, [[kapu]].''')

sec('kut_f', '''A kút kávájába régi írás van vésve: "Aki rézpénzt vet belém, annak a Hold vigyáz az útjára." A
víz mélyén apró érmék csillognak; a falubeliek sok kívánsága. Ha te is bedobsz egy aranytallért, és
kívánsz valamit, [[kut_kivan]]. Ha nem hiszel az ilyesmiben, és visszamész a tér közepére, [[ter]].''',
    gate(T('kut_kivan'), ('gold', 1)))

sec('kut_kivan', '''Az érme csobbanva tűnik el a mélyben. Behunyod a szemed, és azt kívánod, hogy épségben hozd haza
a Holdkövet. Amikor kinyitod, a víz tükrén mintha egy pillanatra halvány, fehér fény villanna. Furcsa
nyugalom száll meg. Visszamész a tér közepére: [[ter]].''', gold(-1), st(SZ, 2))

sec('utca', '''A főtérről három kanyargós utca indul. A Templom utca végén a kápolna fehér falai látszanak. A Kút
utcában áll Bodor háza, mellette a harangláb. A Malom utca a patak felé lejt, ahol a falu öreg molnára
lakik, a szélén pedig a temető kőfala húzódik. A piactéren még áll néhány sátor, és ott van az istálló
is. Ha a kápolnához mész, [[kapolna_f]]. Ha Bodor házához, [[bodor_haz]]. Ha a haranglábhoz,
[[harang]]. Ha a Malom utcán indulsz el, [[malom_utca]]. Ha a piactérre mész, [[piac]]. Ha visszamész
a főtérre, [[ter]].''')

sec('malom_utca', '''A Malom utca sáros és csendes. A patak partján egy öreg vízimalom kereke nyikorog lassan, a kéménye
füstöl. Az utca túlsó végén a temető kőfala látszik, a kapuja nyitva, és bentről lapátcsörgés
hallatszik. Ha bekopogsz a malomba, [[molnar]]. Ha a temetőbe mész, [[temeto]]. Ha visszamész az
utcák kereszteződéséhez, [[utca]].''')

sec('fogado', '''A Részeg Kecske ivója füstös és meleg. A pult mögött Lenke, a fogadósné törölgeti a korsókat, a
kandalló mellett két szekeres kockázik, egy szálfa termetű favágó hangosan követeli a következő
korsót, a sarokban pedig egy csuklyás alak ül egyedül, és téged figyel. Ha odaülsz a csuklyáshoz,
[[idegen]]. Ha beszállsz a kockajátékba (egyszer játszhatsz), [[kocka]]. Ha a pulthoz lépsz, és Lenkével beszélsz,
[[fogado_pult]]. Ha kivennél egy szobát éjszakára, [[fogado_szoba]]. Ha visszamész a főtérre,
[[ter]].''', gate(T('kocka'), nvis('kocka')))

sec('fogado_pult', '''Lenke egy korsó forralt bort tol eléd. - Bence, Bodor unokája itt ült két napja, ahol most te -
mondja halkan. - Arról kérdezte a vendégeket, merre van a Varjútorony, és hogyan lehet bejutni. Azt
mondtam neki, ne bolondozzon. Aztán reggelre eltűnt. - Közelebb hajol. - Vigyázz a zsebedre is! Fürge,
a kis tolvaj, megint itt sündörög. Ha visszamész az ivó közepére, [[fogado]]. Ha odamész a hangoskodó
favágóhoz, [[favago_reszeg]].''')

sec('favago_reszeg', '''A favágó vöröslő arccal fordul feléd. - Mit bámulsz, vándor? Talán a toronyba készülsz te is, mint
az a taknyos kölyök? - Mielőtt felelhetnél, felborítja az asztalt, és rád veti magát. Meg kell
küzdened vele, de csak puszta ököllel. Ha legyőzöd, [[favago_bocsanat]].''',
    fight([M('Részeg favágó', 6, 7)], T('favago_bocsanat'), pdmg=1, mdmg=1))

sec('favago_bocsanat', '''A favágó a padlón ülve dörzsöli az állát, aztán harsányan felnevet. - Jó öklöd van! Na, bocsáss
meg, rossz napom volt: a farkasok széttépték a két ökrömet. - Kezet ráz veled, és két aranytallért
nyom a markodba a borravalóként szánt pénzéből. - Ha az erdőn át mész, az elágazásnál ne a lápon
menj, ha nincs köteled. A hágón legalább meg lehet kapaszkodni. Visszamész az ivó közepére:
[[fogado]].''', gold(2))

sec('fogado_szoba', '''Lenke két aranytallért kér egy éjszakáért, vacsorával. A szobák az emeleten vannak, tiszták, a
dunyha puha. Egy éjszakai pihenés jót tenne a kalandod előtt. Ha kifizeted a két aranyat, és lefekszel,
[[fogado_alvas]]. Ha inkább nem töltöd itt az éjszakát, és visszamész az ivóba, [[fogado]].''',
    gate(T('fogado_alvas'), ('gold', 2)))

sec('fogado_alvas', '''Kiadósan megvacsorázol, aztán mély álomba zuhansz. Valamikor éjfél után nyikorgásra riadsz: az ajtód
lassan kinyílik, és egy vékony árnyék oson az erszényed felé. Tedd próbára a szerencsédet! Ha szerencséd van, még időben elkapod a betolakodót: [[furge_elkap]]. Ha nincs, mire
felocsúdsz, már csak a nyitott ablakot látod: [[furge_lop]].''', gold(-2), st(E, 4), luck(T('furge_elkap'), T('furge_lop')))

sec('furge_elkap', '''Elkapod a karját: egy sovány, kócos legényke az. - Fürge vagyok, kérlek, ne adj fel! - nyöszörgi.
- Inkább adok valamit, ami jól jöhet neked! - A zsebéből egy köteg furcsa, hajlított drótot húz elő.
- Tolvajkulcs. Nincs olyan zár, amit ki ne nyitna, ha van hozzá türelmed. És hallod-e: a toronyban,
a börtön ajtaján olyan zár van, amit én is ki tudnék nyitni. Elengeded. Reggel lemész az ivóba:
[[fogado]].''', gain('tolvajkulcs'))

sec('furge_lop', '''Az erszényed könnyebb lett: három aranytallér hiányzik belőle. A tolvaj nyomát sem látod. Lenke
reggel együttérzően csóválja a fejét. - Fürge volt, biztosan. Ma már nem fogod megtalálni. Lemész az
ivóba: [[fogado]].''', gold(-3))

sec('idegen', '''A csuklyás hátratolja a kámzsáját: egy sebhelyes arcú, középkorú férfi az. - Ádor vagyok. Egykor
a Varjútorony őre voltam, mielőtt Morvath beköltözött. Két út vezet oda. Nyugatra a Suttogó-láp, ahol
Csobán, a révész visz át a Fekete-patakon. Keletre a Kőkapu-hágó, ott egy remete él. A torony kapuja
vasból van; ezüstkulcs nyitja. - A kupájába néz, ami üres. - Ha fizetsz egy kupa bort, elmondok még
valamit. Ha fizetsz neki egy kupa bort két aranytallérért, [[ador_ital]]. Ha megköszönöd, amit
mondott, és visszamész az ivó közepére, [[fogado]].''', gate(T('ador_ital'), ('gold', 2)))

sec('ador_ital', '''Ádor nagyot húz a borból, aztán egy gyűrött bőrdarabot terít az asztalra. - A torony térképe.
Emlékezetből rajzoltam. Látod ezt itt, a lovagok temetője mögött? Egy kiskapu. Kívülről nem látszik,
de ha tudod, hol keresd, a falba vájt lépcsőn át bejuthatsz az udvarra a kapu nélkül is. - A térképet
neked adja. - És még valami: Morvath nem mindig volt varázsló. Valaha egyszerű falusi legény volt.
Visszamész az ivó közepére: [[fogado]].''', gold(-2), gain('terkep'))

sec('kocka', '''A szekeresek szívesen beengednek a játékba. - Egy forduló, nagy tét! - röhög az egyik. Kétszer
dobtok, a magasabb nyer. Hogy kedvez-e a szerencse, azt mindjárt meglátod. Ha nyersz, négy
aranytallérral leszel gazdagabb, ha vesztesz, kettővel szegényebb. A forduló után a szekeresek
fizetnek egy kört, és elmerülnek a saját beszélgetésükben; többet nem játszanak veled. Ha
visszamész az ivó közepére, [[fogado]].''', luck(), iff('res', [gold(4)], [gold(-2)]))

sec('kovacs', '''Bendegúz, a kovács vállas, kormos ember. - Ha a toronyba mész, ne üres kézzel indulj - dörmögi, és
a pultra rakja, amije van: egy ezüstből vert tőrt, egy hosszú, erős kötelet és egy olajjal teli
lámpást. - Az ezüst a holtak ellen jó, a kötél a hegyekben, a lámpás a sötétben. Válogass, de ne
alkudj, nincs nekem se sok. Ha végeztél, és visszamész a főtérre, [[ter]]. Ha felajánlod, hogy
segítesz neki a fújtatónál, [[kovacs_munka]].''',
    shop(('ezusttor', 4), ('kotel', 2), ('lampas', 3)))

sec('kovacs_munka', '''Egy órán át húzod a fújtatót, amíg Bendegúz egy ekevasat kalapál. Izzadsz, a karod sajog, de a kovács
elégedett. - Rendes ember vagy - mondja, és két aranytallért nyom a kezedbe. - Ha a hágón mész, és
találsz ezüstércet a régi törpbányában, hozd el nekem; pénzt adok érte, ha egyszer hazajössz.
Visszamész a főtérre: [[ter]].''', gold(2), st(E, -1))

sec('fuvesno', '''Gyopár néni kunyhója tele van szárított füvekkel. - Tudom, hová mész - mondja, mielőtt egy szót
szólnál. - Ez itt szentelt víz a kápolna kútjából; Morvath ereje ettől megtörik, ha meglocsolod. Négy
aranyért a tiéd. - Aztán halkabban folytatja: - Ha a lápon kék fényt látsz, ne kövesd! A lidércfény a
mélybe csal. És ha a toronyban három jelet találsz egy ajtón, emlékezz: előbb kel a Nap, aztán
gyúlnak a csillagok, és csak a végén jön fel a Hold. Ha visszamész a főtérre, [[ter]]. Ha még
megkérdezed tőle, mit tud a lápi banyáról, [[fuvesno_banya]].''', shop(('szenteltviz', 4)))

sec('fuvesno_banya', '''Gyopár néni összerezzen. - A Holt Fák szigetén él, a láp közepén. Vén, mint a láp maga, és csak azt
segíti, aki hoz neki valamit. Holdvirág nő a szigetén, ami minden sebet begyógyít; de a banya nem
adja ingyen. Az ilyesmiért mindig valami mást kér. - Megpaskolja a kezed. - Légy vele udvarias, és
ne egyél semmit, amit kínál! Visszamész a főtérre: [[ter]].''')

sec('kapolna_f', '''A kápolna ajtaja tárva-nyitva. Bent hideg van, a padokon megolvadt gyertyák, az oltár mögötti
fülke, ahol a Holdkő állt, üres. Az egyik ablak betörve, a padlón fekete tollak. Egy fiatal, sápadt
pap térdel az oltár előtt: Márk atya. Ha megvizsgálod a nyomokat, [[kapolna_nyom]]. Ha a paphoz
fordulsz, [[kapolna_pap]]. Ha visszamész az utcára, [[utca]].''')

sec('kapolna_nyom', '''A betört ablak alatt a fekete tollak között fehér port találsz: lisztet. A fülke peremén fekete
viaszcsepp, rajta egy pecsétnyomat: egy varjú, a csőrében egy kis K betűvel. Furcsa egy tolvaj, aki
lisztes kézzel jár, és pecsétet hord. Elgondolkodva teszed vissza a viaszt. Ha a paphoz fordulsz,
[[kapolna_pap]]. Ha visszamész az utcára, [[utca]].''')

sec('kapolna_pap', '''Márk atya felnéz. - Imádkoztam, hogy jöjjön valaki - suttogja. - Az őrünket holtan találtam, és
azóta éjjelente a temetőben is megmozdul a föld. Morvath halottakat ébreszt. - Egy kis üvegcsét ad át
neked. - Szentelt víz. A holtak és a sötét varázslat ellen. És áldásom rád. Ha visszamész az utcára,
[[utca]]. Ha megkérdezed, mi történt a temetőben, [[pap_temeto]].''', gain('szenteltviz'), st(SZ, 1))

sec('pap_temeto', '''- Mátyás, a sírásó virraszt ott minden éjjel - mondja a pap. - Tegnapelőtt két sírt talált feltúrva,
és hajnalban valami járkált a sírkövek között. Egyedül van, öreg ember. Ha segítenél neki, Isten
megfizeti. És talán Mátyás is tud valamit, amit mi nem. Visszamész az utcára: [[utca]].''')

sec('bodor_haz', '''Bodor háza a Kút utca legszebb háza, de most csend van benne. A konyhában Rozália, Bodor felesége
ül, és a kötényébe sír. - Bence... - zokogja. - Tizenhat éves, és azt hiszi, ő lesz a hős. Ha
megtalálod, add oda neki ezt a levelet; a nagyapja írta. Akkor tudni fogja, hogy megbízhat benned.
- Egy lepecsételt levelet ad át. Ha megnézed Bence szobáját, [[bence_szoba]]. Ha visszamész az
utcára, [[utca]].''', gain('level'))

sec('bence_szoba', '''Bence szobája a padláson van. A falon szénnel rajzolt kép: a Varjútorony, és a tövében, a
temetőnél, egy kis ajtó bekarikázva. Az ágy alatt faragóeszközök és egy félkész fűzfasíp. Rozália a
lépcső aljáról szól fel: - Mindig sípolt, ha a mezőn járt. Úgy találtuk meg, ha elkóborolt. Ha
sípolsz, felel. - Elteszed a sípot. Visszamész az utcára: [[utca]].''', gain('sip'))

sec('harang', '''A harangláb egy magas, fából ácsolt torony a Kút utca végén. A létra korhadt, de a tetejéről messzire
lehet látni. Ha felmászol, [[harang_fent]]. Ha visszamész az utcára, [[utca]].''')

sec('harang_fent', '''A harang mellett állva látod az egész völgyet: a fenyőerdőt, a láp ködét nyugaton, a hágó havas
csúcsait keleten, és a messzeségben a Varjútorony fekete tüskéjét. Ekkor szárnysuhogás: egy nagy,
fekete varjú csap le rád, a szeme vörösen izzik. Morvath kémje! Meg kell küzdened vele. Ha legyőzöd,
[[harang_toll]].''', fight([M('Kémvarjú', 5, 4)], T('harang_toll')))

sec('harang_toll', '''A varjú lehull a deszkákra. A tollai között egy különös, kékes fényű evezőtollat találsz. Ahogy
megérinted, halk károgást hallasz a fejedben. Valahogy tudod: aki ezt a tollat viseli, azt Morvath
varjai a sajátjuknak hiszik. A tollat a sapkádba tűzöd, és lemászol a létrán: [[utca]].''', gain('varjutoll'))

sec('molnar', '''Egy hajlott hátú, félvak öregember nyit ajtót, lisztes kötényben: Gáspár, a molnár. - Vendég?
Régen járt erre vendég - mondja, és behív a meleg konyhába. A tűzhely felett egy fiatal legény
rajza lóg; a legény vállán varjú ül. Ha megkérdezed, ki a legény a képen, [[molnar_kerdez]]. Ha
megköszönöd a vendéglátást, és visszamész a Malom utcára, [[malom_utca]].''')

sec('molnar_kerdez', '''Gáspár keze megremeg. - Kelemen, a fiam. Tíz éve ment el. A falu kicsúfolta, mert varjakkal
beszélt, és egyszer a legények a malomgödörbe lökték. Azon az éjjelen elment, és nem jött vissza. -
Egy kopott ezüstgyűrűt húz le az ujjáról. - Az anyjáé volt. Ha valaha találkozol vele... mondd meg
neki, hogy az apja vár. - A gyűrű pecsétjén varjú, a csőrében K betű. A kápolnában látott viaszra
gondolsz, és megborzongsz. Visszamész a Malom utcára: [[malom_utca]].''', gain('gyuru'), gain('nev'))

sec('temeto', '''A temetőben két sír fel van túrva, a kereszteket kidöntötték. Egy öregember, Mátyás, a sírásó
lapátol, és visszahányja a földet. - Ma éjjel megint jönnek - mondja komoran. - Ha éjfélig itt
maradsz, és velem virrasztasz, megláthatod magad. Ha vele maradsz éjfélig, [[temeto_virraszt]]. Ha
inkább visszamész a Malom utcára, [[malom_utca]].''')

sec('temeto_virraszt', '''Éjfélkor a hold kibújik a felhők mögül, és a feltúrt sírokból két alak tápászkodik fel: rongyos,
szürke bőrű halottak, a szemük helyén üresség. Mátyás felkapja a lapátját. Ha van ezüsttőröd, azzal
harcolsz, és az ezüst minden csapással kétszeresen sebzi őket: [[zombi_tor]]. Ha nincs, a kardoddal
kell megküzdened velük: [[zombi_kard]].''', gate(T('zombi_tor'), 'ezusttor'), gate(T('zombi_kard'), '!ezusttor'))

sec('zombi_tor', '''Az ezüsttőr sisteregve hatol a holt húsba. Egyenként küzdesz meg a két élőhalottal. Ha mindkettőt
legyőzöd, [[temeto_hajnal]].''', fight([M('Első élőhalott', 6, 6), M('Második élőhalott', 6, 5)], T('temeto_hajnal'), pdmg=4, mdmg=2))

sec('zombi_kard', '''A kardod nehezen birkózik a szívós, holt testekkel. Egyenként küzdesz meg a két élőhalottal. Ha
mindkettőt legyőzöd, [[temeto_hajnal]].''', fight([M('Első élőhalott', 6, 6), M('Második élőhalott', 6, 5)], T('temeto_hajnal')))

sec('temeto_hajnal', '''Hajnalban Mátyás visszatemeti a halottakat, és szentelt földet szór a sírokra. - Köszönöm, vándor.
Ezt neked adom. - Egy zöldre patinásodott rézcsengőt ad át. - A temetői csengő. Ha megrázod, a holtak
megtorpannak: régen azért kötötték a sírokra, hogy ha valaki élve kerül a föld alá, csengethessen.
A holtak nem szeretik a hangját. És még valami: a torony alatt régi kripta van. Nem minden halott
nyugszik ott. Visszamész a Malom utcára: [[malom_utca]].''', gain('csengo'), gold(3), gain('temeto'))

sec('piac', '''A piactéren csak egy vándorárus sátra áll: Ilkó, a félszemű kereskedő pipázik a ládái között. -
Kötél, elemózsia, és egy kis kincs a hozzáértőnek! - kiabálja. Egy ezüstkeretes kézitükröt mutat:
- Varázstükör, mondják. Mindenesetre tiszta ezüst. Ha vásárolsz valamit, megteheted most. Ha átmész
az istállóba, [[istallo]]. Ha visszamész az utcára, [[utca]].''',
    shop(('kotel', 3), ('kenyer', 1), ('tukor', 5)))

sec('istallo', '''Az istállóban egy öreg, szürke kanca rágja a szénát. Az istállófiú, Peti, vigyorogva lép elő. - Ez
Csillag. Öreg, de az erdei úton akár az elágazásig is elvisz, és onnan magától hazatalál. Három
aranytallér. Ha kibéreled Csillagot három aranyért, [[lovaglas]]. Ha nem, és visszamész a piactérre,
[[piac]].''', gate(T('lovaglas'), ('gold', 3)))

sec('lovaglas', '''Csillag egykedvűen ügetve visz ki az északi kapun, be a fenyőerdőbe. Egyszer egy farkas szürke
árnyát látod a fák között, de a ló nem ijed meg, és a farkas nem mer közelebb jönni. Délre a
kőkereszthez értek, ahol az út kettéválik. Leszállsz, megpaskolod Csillag nyakát, és a kanca
megfordul, és hazaindul. Ha körülnézel az elágazásnál, [[elagazas]].''', gold(-3))

sec('kapu', '''Az északi kapunál egy fiatal őr áll, lándzsáját szorongatva. - Az erdőn át vezet az út - mondja. -
Tegnap éjjel farkasokat láttam a fák között, de nem olyanokat, mint máskor. A szemük vörösen izzott.
És Bence is erre ment, Bodor unokája. Rászóltam, de nem hallgatott rám. - Kinyitja a kaput, és a
nyikorgó szárnyak bezárulnak mögötted. Ha elindulsz az erdei úton, [[erdo]]; ha már jártál az
erdőben, [[erdo_ut]].''', gate(T('erdo'), nvis('erdo')), gate(T('erdo_ut'), vis('erdo')))
