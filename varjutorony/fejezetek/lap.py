"""3. A Suttogó-láp."""
from kv import *

sec('lap1', '''A nyugati út lejt, a fenyők megritkulnak, és hamarosan nyirkos, sásos rétre érsz. Sűrű, fehér köd
gomolyog a víz fölött, és mindenfelől halk suttogás hallatszik, mintha láthatatlanok beszélgetnének
körülötted. Ez a Suttogó-láp. Egy korhadt cölöpön tábla: "Révész - pallón át". Mellette rozoga
pallósor vezet be a ködbe. A távolban, balra, halvány kék fény imbolyog. Ha a pallón indulsz el,
[[lap_pallo]]. Ha a kék fény felé indulsz, [[liderc]]. Ha megvárod, amíg a köd felszáll, [[lap_kod]].''')

sec('lap_kod', '''Leülsz egy kőre, és vársz. A köd nem száll fel, inkább sűrűsödik, és a suttogás egyre
hangosabb. Most már szavakat is kivehetsz: "Gyere... gyere közénk... itt jó a víz..." Hideg borzongás
fut végig rajtad. Valami a nyakadat érinti, mint egy nedves ujj. Elveszítesz 1 SZERENCSE pontot.
Felugrasz. Ha a pallón indulsz el, [[lap_pallo]]. Ha a kék fény felé, [[liderc]].''', st(SZ, -1))

sec('liderc', '''A kék fény egy ember magasságában lebeg, és lassan távolodik, ahogy közeledsz. Olyan, mintha egy
lámpást vinne valaki. Talán a révész? - Hahó! - kiáltasz, de nem jön válasz. A talaj egyre
süppedősebb a lábad alatt. Ha továbbra is követed a fényt, [[liderc_kovet]]. Ha eszedbe jutnak Gyopár
néni szavai, és visszafordulsz, [[liderc_vissza]].''')

sec('liderc_vissza', '''Megtorpansz, és visszanézel. A lábnyomaidban már víz áll. A kék fény megáll, mintha várna rád,
aztán egy gúnyos, kísérteties kacagással kihuny. Visszagázolsz a szilárd talajra, és a
pallósorhoz mész: [[lap_pallo]].''')

sec('liderc_kovet', '''A fény egyre gyorsabban siklik előtted, és te utána sietsz. Hirtelen eltűnik, és ugyanabban a
pillanatban a lábad alól kicsúszik a talaj. Derékig süllyedsz a fekete, hideg iszapba, ami lassan
lefelé húz. Tedd próbára a szerencsédet! Ha szerencséd van, [[mocsar]]. Ha nincs, a mocsár mélyebbre
ránt, és már a mellkasodig ér: [[mocsar_mely]].''', luck(T('mocsar'), T('mocsar_mely')))

sec('mocsar', '''Egy kidőlt fa ága nyúlik fölötted, épp elérhető távolságban. Ha van köteled, rádobhatod az
ágra, és kihúzhatod magad: [[mocsar_kotel]]. Ha nincs, megpróbálhatod elkapni az ágat puszta kézzel:
[[mocsar_kuzd]].''', gate(T('mocsar_kotel'), 'kotel'))

sec('mocsar_mely', '''Az iszap a melledig ér, a hideg elszorítja a lélegzetedet. Kétségbeesetten kapálózol. Ha van
köteled, egy közeli ágra hajíthatod: [[mocsar_kotel]]. Ha nincs, meg kell próbálnod kievickélni:
[[mocsar_kuzd2]].''', gate(T('mocsar_kotel'), 'kotel'), gate(T('mocsar_kuzd2'), '!kotel'))

sec('mocsar_kotel', '''A kötél a második dobásra átcsúszik az ágon. Kapaszkodva, centiméterről centiméterre húzod ki
magad a cuppogó sárból. Amikor végre szilárd talajon fekszel, alig kapsz levegőt. Csupa sár vagy,
de élsz. Elveszítesz 2 ÉLETERŐ pontot. A kötelet leoldod, és visszabotorkálsz a pallósorhoz:
[[lap_pallo]].''', st(E, -2))

sec('mocsar_kuzd', '''Kinyújtod a kezed az ág felé. Tedd próbára az ügyességedet! Ha sikerül elkapnod, [[mocsar_ki]].
Ha nem, mélyebbre süllyedsz: [[mocsar_kuzd2]].''', skill(T('mocsar_ki'), T('mocsar_kuzd2')))

sec('mocsar_kuzd2', '''Most már csak az utolsó erődre számíthatsz. Előredobod magad, és hason fekve próbálod
kiszabadítani a lábadat az iszapból. Tedd próbára az ügyességedet! Ha sikerül, [[mocsar_ki]]. Ha nem,
[[mocsar_halal]].''', skill(T('mocsar_ki'), T('mocsar_halal')))

sec('mocsar_ki', '''Az ujjaid egy gyökérbe kapaszkodnak, és nagy cuppanással kiszabadulsz. Négykézláb mászol ki a
szilárd talajra, és sokáig fekszel ott zihálva. A csizmád tele van iszappal, és az egyik
aranytallérod is elnyelte a láp. Elveszítesz 3 ÉLETERŐ pontot. Visszabotorkálsz a pallósorhoz:
[[lap_pallo]].''', st(E, -3), gold(-1))

sec('mocsar_halal', '''A fekete iszap a válladig, aztán az álladig ér. Még egyszer felnézel a ködre, ahol a kék fény
újra felragyog, és mintha nevetne. Aztán a láp bezárul fölötted. A Suttogó-láp újabb hangot nyert
magának. A kalandod itt véget ért.''')

sec('lap_pallo', '''A pallók nyikorognak a súlyod alatt, némelyik már félig elkorhadt. A köd olyan sűrű, hogy alig
látsz két lépésnyire. Egy helyen a pallósor kettéválik: az egyik ág jobbra, egy nádas felé tart,
ahonnan brekegés hallatszik, a másik egyenesen előre visz tovább. Ha jobbra mész, a nádas felé,
[[bekak]]. Ha egyenesen tovább mész, [[pallo_tores]].''')

sec('pallo_tores', '''Egy hosszú, egyenes pallószakaszon haladsz, amikor a deszka hangos reccsenéssel kettétörik a
lábad alatt. Tedd próbára az ügyességedet! Ha sikerül, egy ugrással átjutsz a következő deszkára:
[[lap_sziget]]. Ha nem, belezuhansz a hideg vízbe: [[piocak]].''', skill(T('lap_sziget'), T('piocak')))

sec('piocak', '''Mellig érő, fekete vízbe zuhansz. Ahogy kikapaszkodsz, látod, hogy a karodon és a nyakadon
ujjnyi vastag piócák lógnak. Undorral tépdesed le őket, de egy hatalmas, alkarnyi pióca a lábadra
tapadt, és nem ereszt. Meg kell küzdened vele. Ha legyőzöd, [[lap_sziget]].''',
    st(E, -1), fight([M('Óriáspióca', 5, 6)], T('lap_sziget')))

sec('lap_sziget', '''A pallósor egy kis, füves szigeten ér véget. Egy fűzfa áll a közepén, a törzsébe valaki nyilakat
vésett. Az egyik nyugat felé mutat: "Révész". Egy másik dél felé: "Holt Fák - ne!". A harmadik
észak felé, de mellette csak egy kereszt. Arrafelé, a köd fölött, egy templomtorony csúcsa
emelkedik ki a vízből. Ha nyugatra mész, a révészhez, [[revesz]]. Ha délre, a Holt Fák felé, [[banya_ut]].
Ha északra, a templomtorony felé, [[sullyedt]]. Ha megpihensz a fűzfa alatt, [[lap_piheno]].''')

sec('lap_piheno', '''Leülsz a fűzfa tövébe. A suttogás itt halkabb, a fa ágai mintha védelmeznének. Eszel egy keveset,
és lehunyod a szemed. Ha van elemózsiád, megeheted most, és visszanyersz 4 ÉLETERŐ pontot. Ha
felálltál, a révészhez mehetsz, [[revesz]], a Holt Fák felé, [[banya_ut]], vagy a templomtorony
felé, [[sullyedt]]. Ha éjszakára a fűzfa alatt maradsz, [[lap_ejszaka]].''', iff('kenyer', [st(E, 4), lose('kenyer')]))

sec('bekak', '''A nádas mögött egy kerek tó csillog, és a tó partján száz meg száz béka brekeg kórusban. Egy
hatalmas, borjúnyi zöld béka ül a tó közepén egy tavirózsalevélen, a fején aranykorona. A békák
királynője! Mellette a sásban egy kis béka nyöszörög: egy szürke gém áll fölötte, és lecsapni
készül. Ha a kis béka segítségére sietsz, [[gem_harc]]. Ha a királynőhöz fordulsz, [[kiralyno]]. Ha
visszamész a pallóra, [[pallo_tores]].''')

sec('gem_harc', '''Odaugrasz, és a gém felé suhintasz a karddal. A hatalmas madár felrikolt, és a hosszú, éles
csőrével feléd vág. Meg kell küzdened vele. Ha legyőzöd, [[gem_utan]].''',
    fight([M('Óriásgém', 6, 5)], T('gem_utan')))

sec('gem_utan', '''A gém szárnyát vonszolva elmenekül. A kis béka hálás brekegéssel a királynőhöz ugrál. A koronás
béka feléd fordul, és emberi hangon szól: - Megmentetted a lányomat, vándor. Kérj, amit akarsz!
Ha azt kéred, hogy segítsen átjutni a lápon, [[kiralyno_segit]]. Ha a Varjútoronyról kérdezed,
[[kiralyno_torony]].''', gain('kiralyno'))

sec('kiralyno', '''- Mit akarsz, halandó? - brekegi a királynő megvetően. - Nem látod, hogy a lányom bajban van? Ha
nem segítesz neki, menj utadra! - A gém lecsap, a kis béka visít. Ha a kis béka segítségére sietsz,
[[gem_harc]]. Ha visszamész a pallóra, [[pallo_tores]].''')

sec('kiralyno_segit', '''- A lápon át? - brekegi a királynő. - Az én népem minden zugát ismeri. - Egy apró, smaragdzöld békát
küld melléd. - Kövesd őt! Elvezet a pallók szigetéig, ahol a régi fűzfa áll, és nem kell a törött
pallón átkelned. És ha az elsüllyedt faluba mennél, keresd a templom pincéjét: a népem tudja, hol a
titkos ajtó, amit az emberek elfelejtettek. A kis béka ugrálva vezet: [[lap_sziget]].''')

sec('kiralyno_torony', '''A királynő szeme elsötétül. - A varjak ura elűzte a vizekből a halakat, és a lápi trollal
szövetkezett, hogy ne engedjen át senkit a Fekete-patakon. De az elsüllyedt falu templomából régi
alagút vezet a torony pincéjébe. Az emberek elfelejtették, de az én népem nem. Ha odamész, a
lányaim megmutatják az utat. - Brekeg egyet, és egy kis béka melléd ugrik. Követed: [[lap_sziget]].''')

sec('revesz', '''A sziget nyugati csücskén egy cölöpökre épült kunyhó áll, előtte egy lapos fenekű csónak ringatózik.
Egy szakállas, horgas orrú öregember ül a stégen, és pipázik: Csobán, a révész. - Át akarsz kelni a
Fekete-patakon? - kérdezi, meg sem fordulva. - Három aranytallér. Előre. Ha kifizeted, [[atkeles]]. Ha
megkérdezed, járt-e erre egy fiú, [[revesz_bence]]. Ha alkudni próbálsz, [[revesz_alku]].''',
    gate(T('atkeles'), ('gold', 3)))

sec('revesz_bence', '''Csobán kiveszi a pipát a szájából. - Járt. Két napja. Át akart kelni, de nem volt pénze, hát
elküldtem a hágó felé. Bolond kölyök. - Hallgat egy darabig. - Aztán éjjel láttam, hogy varjak
szállnak a hegyek felől a torony felé, és egy zsákot visznek. A zsák vergődött. Elkapták, azt hiszem.
Ha kifizeted a három aranyat, [[atkeles]]. Ha alkudni próbálsz, [[revesz_alku]].''', gate(T('atkeles'), ('gold', 3)))

sec('revesz_alku', '''- Alku? - Csobán megvetően köp a vízbe. - Itt a troll a patakban, kölyök. Az enyém is kockázat.
Három arany, vagy átúszol. - Aztán vállat von. - Vagy ha van nálad valami a faluból... Bodor nekem
egyszer jót tett. Ha nála jártál, és hozol tőle írást, ingyen viszlek. Ha megmutatod Bodor levelét,
[[revesz_level]]. Ha kifizeted a három aranyat, [[atkeles]]. Ha inkább a patak mentén keresel
másik átkelőt, [[troll_hid]].''', gate(T('revesz_level'), 'level'), gate(T('atkeles'), ('gold', 3)),
    gate(T('troll_hid'), '!troll'))

sec('revesz_level', '''Csobán megnézi a pecsétet a levélen, és bólint. - Bodor pecsétje. Nem bontom fel, az a fiúnak szól.
- Visszaadja. - Gyere, átviszlek. És ha a trollal találkozunk, ne félj, én tudom, mit szeret. - A
csónakba szállsz, és Csobán ellöki a stégtől: [[atkeles_ingyen]].''')

sec('atkeles', '''Kifizeted a három aranyat. Csobán a csónakba int, és ellök a stégtől. Lassan siklotok a fekete
vízen, a köd bezárul körülöttetek. A patak közepén a víz hirtelen fodrozódni kezd, és egy hatalmas,
mohos fej bukkan fel: a lápi troll! - Vám! - bömböli, és a csónak peremébe kapaszkodik. Ha kardot
rántasz, [[troll_harc]]. Ha Csobánra bízod a dolgot, [[troll_revesz]].''', gold(-3))

sec('atkeles_ingyen', '''Csobán egyenletesen evez, és dúdol valamit. A patak közepén a víz fodrozódni kezd, és egy
hatalmas, mohos fej bukkan fel: a lápi troll. Csobán nyugodtan előhúz egy füstölt halat a láda
mélyéről, és a troll felé hajítja. A troll elkapja, megszagolja, és elégedetten elmerül. - Ez a
vám - vigyorog az öreg. A túlparton kiszállsz: [[tulpart]].''')

sec('troll_revesz', '''Csobán felsóhajt. - Már megint te, Bütyök? - A ládából egy füstölt halat vesz elő, és a troll
felé tartja. A troll kiveszi a kezéből, és elmerül. - Mindig éhes - mondja Csobán. - Egyszer nem lesz
halam, és akkor vége a révésznek. - A túlparton kiszállsz: [[tulpart]].''')

sec('troll_harc', '''A troll a csónakba kapaszkodva csapkod a hatalmas, karmos kezével. A csónak veszélyesen billeg,
nehéz így harcolni. Meg kell küzdened vele. Ha legyőzöd, [[troll_gyoz]].''',
    fight([M('Lápi troll', 8, 9)], T('troll_gyoz'), skmod=-1))

sec('troll_gyoz', '''A troll fájdalmas bömböléssel elengedi a csónakot, és elmerül a fekete vízben. Csobán elismerően
füttyent. - Ilyet még nem láttam. Bütyök évek óta itt tanyázik. - A túlparton kiszállsz. - Vigyázz
magadra, kölyök. A torony nincs messze, de a varjak mindent látnak. [[tulpart]].''', gain('troll'))

sec('troll_hid', '''Elindulsz a patak partján. A sás között egy ősi, mohos kőhíd ível át a vízen, a pillérei között
sötét üreg tátong. Ahogy a híd közepére érsz, az üregből egy mohos, kétszer akkora alak mászik elő, mint
te: a lápi troll. - Az én hidam! Vámot! Vagy megeszlek! Ha harcolsz vele, [[troll_hid_harc]]. Ha
felajánlod neki a füstölt húst, [[troll_hus]]. Ha megkérdezed, mit kér vámként, [[troll_talany]].''',
    gate(T('troll_hus'), 'hus'))

sec('troll_hid_harc', '''A troll bunkót ragad, és lassú, de rettenetes erejű csapásokkal támad rád. Meg kell küzdened vele.
Ha legyőzöd, [[troll_hid_gyoz]].''', fight([M('Lápi troll', 8, 9)], T('troll_hid_gyoz')))

sec('troll_hid_gyoz', '''A troll a hídra rogy, aztán belegurul a vízbe, és elsodorja a sodrás. Az üregében, a híd alatt
csontok és rozsdás vértek között két aranytallért és egy olajosüveget találsz. A lámpásba való olaj
még jól jöhet. Átkelsz a hídon: [[tulpart]].''', gold(2), gain('olaj'), gain('troll'))

sec('troll_hus', '''A troll kikapja a kezedből a füstölt húst, és nagy csámcsogással bekebelezi. - Jó hús! Jó vándor!
- Félreáll az útból. - Menj át, menj! - Átkelsz a hídon, a troll pedig elégedetten böfög utánad.
Csak sajnálod a húst; a hegyekben talán jól jött volna. [[tulpart]].''', lose('hus'))

sec('troll_talany', '''A troll vakarja a fejét. - Vám... talány! Ha kitalálod, átmész. Ha nem, megeszlek! - Hosszan
gondolkodik, aztán diadalmasan felbömböl: - Mi az: minél többet veszel el belőle, annál nagyobb? Ha
azt feleled, hogy "a gödör", [[talany_jo]]. Ha azt, hogy "az éhség", [[talany_rossz]].''')

sec('talany_jo', '''- Gödör! - A troll a földhöz vágja a bunkóját. - Honnan tudtad? Senki se tudta még! - Megsértődve
visszamászik az üregébe. Átkelsz a hídon. A túloldalon hallod még, ahogy magában dörmögi: "Gödör...
gödör...". [[tulpart]].''', st(SZ, 1))

sec('talany_rossz', '''- Rossz! Rossz! - örvendezik a troll, és rád veti magát. Meg kell küzdened vele. Ha legyőzöd,
[[troll_hid_gyoz]].''', fight([M('Lápi troll', 8, 9)], T('troll_hid_gyoz')))

sec('tulpart', '''A Fekete-patak túlpartján a talaj szilárdabb, a köd ritkul. Egy fűzfák közötti ösvény vezet
észak felé, és a távolban, egy sziklás dombon már tisztán látod a Varjútorony fekete, csorba
tornyát, körülötte varjak keringenek. Jobbra, a patak partján egy öreg vízimalom áll romokban, a
kereke még mindig forog. Ha a malomhoz mész, [[malom]]. Ha a torony felé vezető ösvényen indulsz el,
[[toronyut]].''')

sec('malom', '''A malom ajtaja félig leszakadt, bent pókhálós sötétség. A hatalmas, mohos kerék lassan forog a
patak sodrásában, a lapátjai közül vízfüggöny zuhog le a mély malomgödörbe. Ádor és Fábián szavaira
gondolsz: a kapu ezüstkulcsa itt van elrejtve, valahol a kerék alatt. Ha bemész a malomba, [[malom_bent]].
Ha a malomgödörhöz mész, [[malomgodor]].''')

sec('malom_bent', '''A malomban a liszt helyett vastag porréteg fedi a padlót. Az őrlőkövek mozdulatlanok. A sarokban
egy rozsdás láda, a tetején egy elmosódott név: "Kelemen". Kinyitod: egy fiúnak való ruha van benne,
egy fakard, és egy gyerekrajz egy varjúról. Morvath nevére gondolsz, és a falu molnárára. Lehet, hogy
a fiú, akit kicsúfoltak, itt rejtőzködött, mielőtt elment? Ha a malomgödörhöz mész, [[malomgodor]].
Ha a torony felé vezető ösvényen indulsz el, [[toronyut]].''')

sec('malomgodor', '''A kerék alatt a víz mély, sötét gödörbe zuhog. Az alján, a buborékok között, halvány csillogás
látszik: valami fényes fekszik a fenéken. Ha van köteled, a kerék tengelyéhez kötheted, és leereszkedhetsz
rajta: [[buvar]]. Ha nincs, fejest ugorhatsz: [[buvar2]]. Ha nem kockáztatsz, [[toronyut]].''',
    gate(T('buvar'), 'kotel'), gate(T('buvar2'), '!kotel'))

sec('buvar', '''A kötél végét a kerék tengelyéhez kötöd, és lassan leereszkedsz a jéghideg vízbe. A kötélbe
kapaszkodva a sodrás nem tud elragadni. A fenéken, egy kő alatt egy kis ezüstkulcsot és egy bőrerszényt
találsz, benne öt aranytallért. Kihúzod magad a kötélen, és vacogva kimászol a gödörből. Ha a torony
felé indulsz, [[toronyut]].''', gold(5), gain('ezustkulcs'))

sec('buvar2', '''Belevetsz magad a vízbe. A sodrás azonnal megragad, és a kerék lapátjai felé ránt. Tedd próbára az
ügyességedet! Ha sikerül, a fenékig úszol: [[buvar]]. Ha nem, a víz a kerék alá sodor, és egy lapát
a válladba csapódik: [[buvar_seb]].''', st(E, -2), skill(T('buvar'), T('buvar_seb')))

sec('buvar_seb', '''Fuldokolva bukkansz a felszínre, a vállad zsibbad, és vér festi a vizet. Valahogy kikapaszkodsz a
gödör partjára. Elveszítesz még 3 ÉLETERŐ pontot. A csillogó valami még mindig ott van lent, de még
egyszer nem mersz lemenni utána. Csalódottan indulsz a torony felé: [[toronyut]].''', st(E, -3))

sec('sullyedt', '''Térdig, aztán derékig gázolsz a hideg vízben, amíg a köd szétnyílik előtted, és meglátod az elsüllyedt
falu romjait. A házak tetejei kiállnak a vízből, a kéményeken varjak ülnek. Középen a templom
tornya magasodik, a kapuja félig víz alatt van. Egy nagy, tölgyfa kapu. Halk harangszó hallatszik a
mélyből. Ha a templomba mész, [[sullyedt_templom]]. Ha a házak közt kutatsz, [[sullyedt_haz]]. Ha
visszamész a fűzfás szigetre, [[lap_sziget]].''')

sec('sullyedt_haz', '''Egy félig összedőlt házba mászol be a tetején át. A padlás száraz, bent egy régi szekrény áll. A
fiókjában egy rongyba csavart lámpást találsz, és egy kevés olajat. A gerendán egy faragás: "Kelemen
és Gáspár, molnárok, Anno Domini..." A dátumot lekoptatta az idő. Elteszed, amit találtál. Ha a
templomba mész, [[sullyedt_templom]]. Ha visszamész a fűzfás szigetre, [[lap_sziget]].''',
    iff('lampas', gain('olaj'), gain('lampas')))

sec('sullyedt_templom', '''A templom belsejében derékig ér a víz. A padok között sápadt, kékes alakok lebegnek: a vízbe fúlt
falu lakói, akik nem nyugszanak. Ahogy belépsz, mind feléd fordulnak, és üres szemükkel rád merednek.
- Élő... - suttogják. - Élő... gyere le közénk... - Lassan feléd siklanak. Ha van rézcsengőd, és
megrázod, [[holtak_csengo]]. Ha kardot rántasz, [[holtak_harc]]. Ha menekülsz, [[holtak_menekul]].''',
    gate(T('holtak_csengo'), 'csengo'))

sec('holtak_csengo', '''Megrázod a temetői csengőt. A tiszta, éles hang betölti a templomot, és a lebegő alakok megtorpannak.
Egymásra néznek, és a szemük üressége helyén mintha könnyek csillannának. - Harang... - suttogják. -
Elfelejtettük... - Egyenként elhalványulnak, mint a köd napfelkeltekor. A templom elcsendesedik. Ha
lemész a pincébe, [[templom_pince]].''', st(SZ, 2))

sec('holtak_harc', '''A kardod átsuhan a kísérteteken, de a jéghideg érintésük mélyen a csontjaidig hatol. Meg kell
küzdened velük, egyszerre kettővel, és minden sebük kétszeresen fáj. Ha legyőzöd őket, [[holtak_utan]].''',
    fight([M('Vízbefúlt lélek', 6, 5), M('Vízbefúlt lélek', 6, 5)], T('holtak_utan'), all=1, mdmg=3))

sec('holtak_utan', '''A kísértetek sikoltva szétfoszlanak, de a templom hideg csendjében érzed, hogy a többiek még ott
vannak a víz alatt, és figyelnek. Sietned kell. Az oltár mögött lépcső vezet lefelé. Ha lemész a
pincébe, [[templom_pince]]. Ha kimenekülsz a templomból, [[holtak_menekul]].''')

sec('holtak_menekul', '''Kirohansz a templomból, a vízben botladozva. A hideg kezek a bokádat markolják, és lefelé húznak.
Tedd próbára a szerencsédet! Ha szerencséd van, [[holtak_kijut]]. Ha nincs, [[holtak_halal]].''',
    luck(T('holtak_kijut'), T('holtak_halal')))

sec('holtak_kijut', '''Kitépsz a jeges szorításból, és kigázolsz a falu romjai közül. A templomból panaszos sóhaj kísér.
Elveszítesz 2 ÉLETERŐ pontot. Vacogva érsz vissza a fűzfás szigetre: [[lap_sziget]].''', st(E, -2))

sec('holtak_halal', '''A hideg ujjak egyre többen vannak, és egyre erősebben húznak. A víz összecsap a fejed fölött, és
a templom harangja megkondul a mélyben. Most már te is az elsüllyedt falu lakója vagy. A kalandod itt
véget ért.''')

sec('templom_pince', '''A pincelépcső alja szárazabb, mint a templom; a víz itt csak a bokádig ér. A falak mentén régi
borosládák és szentképek. Az egyik falon, egy vasajtón, egy dombormű: egy torony, és alatta egy
kanyargó vonal. Az ajtó rozsdás, de a zára ép. Ha a békák királynője segített neked, a kis béka
egy repedéshez ugrál a fal tövében: [[pince_beka]]. Ha megpróbálod betörni az ajtót, [[pince_ajto]]. Ha
tolvajkulccsal próbálkozol, [[pince_tolvaj]]. Ha visszamész, [[sullyedt]].''',
    gate(T('pince_beka'), 'kiralyno'), gate(T('pince_tolvaj'), 'tolvajkulcs'))

sec('pince_beka', '''A kis béka egy laza kőhöz ugrál, és brekeg. Kihúzod a követ: mögötte egy rozsdás kar van. Meghúzod,
és a vasajtó nyikorogva kitárul. Mögötte szűk, sötét alagút vezet északnak, a torony felé. A kis béka
búcsúzóul brekeg egyet, és elugrál. Ha belépsz az alagútba, [[alagut]].''')

sec('pince_ajto', '''Nekifeszülsz a vasajtónak a válladdal. Egyszer, kétszer, háromszor. Tedd próbára az ügyességedet!
Ha sikerül, a rozsdás zár enged: [[pince_nyit]]. Ha nem, a vállad sajog, és az ajtó meg sem mozdul:
[[pince_nem]].''', skill(T('pince_nyit'), T('pince_nem')))

sec('pince_nem', '''Elveszítesz 2 ÉLETERŐ pontot. A vasajtó szilárdan áll. Hiába próbálkozol, nem tudod kinyitni. Ha
van tolvajkulcsod, megpróbálhatod azzal: [[pince_tolvaj]]. Ha nincs, nincs más hátra, mint
visszamenni a felszínre: [[sullyedt]].''', st(E, -2), gate(T('pince_tolvaj'), 'tolvajkulcs'))

sec('pince_tolvaj', '''Kiválasztasz egy hajlított drótot, és piszkálni kezded a zárat. Egy idő után kattanás hallatszik.
Fürge, vagy Lajos, a rablóvezér igazat mondott: ez bármit kinyit. [[pince_nyit]].''')

sec('pince_nyit', '''A vasajtó nyikorogva kitárul. Mögötte szűk, sötét alagút vezet északnak, a torony felé. Penész és
dohos víz szaga árad belőle. Ha belépsz az alagútba, [[alagut]].''')

sec('alagut', '''Az alagút sötét, a falai nyirkosak. Ha van lámpásod, meggyújtod: [[alagut_lampas]]. Ha nincs,
tapogatózva haladsz előre: [[alagut_sotet]].''', gate(T('alagut_lampas'), 'lampas'), gate(T('alagut_sotet'), '!lampas'))

sec('alagut_lampas', '''A lámpás sárga fényében az alagút falain régi vésetek látszanak: szerzetesek menekülő útja volt
ez, amikor a torony még kolostor volt. Egy helyen a járat kettéágazik; a bal ágban a víz csobog, a
jobb ág felfelé kapaszkodik. A jobb ágat választod. Egyszer csak cincogás: patkányok hada rohan
feléd a sötétből. Meg kell küzdened velük. Ha legyőzöd őket, [[alagut_vege]].''',
    fight([M('Patkánycsapat', 5, 6)], T('alagut_vege')))

sec('alagut_sotet', '''Tapogatózva haladsz a sötétben. A víz a térdedig ér, aztán apad. Egyszer egy elágazáshoz érsz, és
fogalmad sincs, merre tovább. Tedd próbára a szerencsédet! Ha szerencséd van, a jó irányba indulsz:
[[alagut_patkany]]. Ha nincs, a bal ágba tévedsz: [[alagut_viz]].''',
    luck(T('alagut_patkany'), T('alagut_viz')))

sec('alagut_viz', '''A bal ág egyre lejjebb visz, és a víz egyre mélyebb. Egy idő után már a mellkasodig ér, és a
sodrás magával akar ragadni. Megfordulsz, és küszködve visszavergődsz az elágazásig. Elveszítesz 3
ÉLETERŐ pontot. Most már a másik ágat választod: [[alagut_patkany]].''', st(E, -3))

sec('alagut_patkany', '''A jobb ág felfelé kapaszkodik. Egyszer csak cincogás és apró karmok kopogása: patkányok hada rohan
feléd a sötétből, és a lábadba marnak. Vakon kell harcolnod. Meg kell küzdened velük. Ha legyőzöd
őket, [[alagut_vege]].''', fight([M('Patkánycsapat', 5, 6)], T('alagut_vege'), skmod=-2))

sec('alagut_vege', '''Az alagút egy keskeny kőlépcsőben végződik. A tetején egy csapóajtó, amit nem zár semmi. Óvatosan
felemeled. Hideg, száraz levegő csapja meg az arcodat, és penészes hordók és ládák szaga. Egy
pincében vagy, a Varjútorony alatt. Felhúzódzkodsz: [[pince]].''')

sec('banya_ut', '''A déli nyíl irányába pallók nem vezetnek; zsombékról zsombékra ugrálva haladsz. A köd egyre
sűrűbb, és a fák, amelyek kibukkannak belőle, mind halottak: csupasz, fehér ágaik csontként
meredeznek az ég felé. Egy kis szigeten egy görbe kunyhó áll, cölöpökön. A kunyhó ajtaja előtt
egy ezüstös, holdfényszerű virág nyílik. Ha a kunyhóhoz mész, [[banya]]. Ha visszafordulsz, [[lap_sziget]].''')

sec('banya', '''Az ajtóban egy ránctól barázdált, vén asszony áll, a haja hínárként lóg. - Látogató - sziszegi -,
régen volt látogatóm. Gyere be, gyere, egyél velem! - Az asztalán egy bogrács gőzölög, illata édes és
csábító. Ha leülsz, és eszel vele, [[banya_etel]]. Ha udvariasan megköszönöd, de nem eszel,
[[banya_udv]]. Ha a kardodat rántod, [[banya_harag]].''')

sec('banya_etel', '''Leülsz, és belemerítesz a kanaladba. Az étel édes, mint a méz, és meleg. Egy kanál, kettő,
három... Egyre álmosabb leszel. A banya kacag, és az arca megváltozik: a szemei sárgák, mint egy
békának. - Jó lesz belőled egy fűzfa - suttogja. A lábaid gyökeret eresztenek. Ha van holdvirágod,
megrághatod: [[banya_holdvirag_ment]]. Ha nincs, [[banya_fa]].''', gate(T('banya_holdvirag_ment'), 'holdvirag'))

sec('banya_holdvirag_ment', '''Az utolsó erőddel a zsebedbe nyúlsz, és megrágod a holdvirág egyik szirmát. A virág hűvös íze
kitisztítja a fejed, és a lábaid kiszabadulnak. Kirohansz a kunyhóból, a banya átkai kísérnek.
Elveszítesz 2 ÉLETERŐ pontot. Visszamenekülsz a fűzfás szigetre: [[lap_sziget]].''', st(E, -2))

sec('banya_fa', '''A gyökereid mélyen a láp sarába hatolnak, a karjaid ágakká merevednek, az ujjaidból levelek
sarjadnak. Mire felkel a nap, egy újabb fehér, holt fa áll a banya szigetén. A kalandod itt véget ért.''')

sec('banya_udv', '''- Nem éhes? - A banya szeme összeszűkül. - Okos vándor. Vagy valaki figyelmeztetett. - Leül, és
végigmér. - Holdvirágot akarsz, igaz? Mind azt akarják. A holdvirág minden sebet begyógyít, és
megtöri a mérget. De nem adom ingyen. - Megérinti a saját arcát. - Valaha szép voltam. Hozz nekem
valamit, amiben újra láthatom magam szépnek! Ha egy ezüsttükröt adsz neki, [[banya_tukor]]. Ha
azt mondod, hogy nincs ilyened, [[banya_nincs]].''', gate(T('banya_tukor'), 'tukor'))

sec('banya_tukor', '''Odanyújtod neki az ezüsttükröt. A banya remegő kézzel veszi el, és belenéz. Egy pillanatra egy
fiatal, szép asszony arca villan fel a tükörben; a banya elsírja magát. - Köszönöm - suttogja. - Ezért
kétszer fizetek. - Ad egy ezüstös holdvirágot. - És tudd meg: Morvath halálos átkot mond, ha már
nincs más fegyvere. A lovagok temetőjében, Ábris őr sírjában van egy amulett, ami megvéd tőle. Ha
nem viseled, csak a szerencse menthet meg. Elbúcsúzol: [[lap_sziget]].''', lose('tukor'), gain('holdvirag'), gain('banya'), st(SZ, 1))

sec('banya_nincs', '''- Akkor nincs holdvirág - mondja a banya egykedvűen. - De egy tanácsot ingyen kapsz, mert nem ettél
a levesemből, és ez tetszett nekem. Morvath halálos átkot mond, ha már nincs más fegyvere. Ábris őr
amulettje megvéd tőle; a lovagok temetőjében van, a torony tövében. Most menj! Visszamész a fűzfás
szigetre: [[lap_sziget]].''')

sec('banya_harag', '''A banya felsikolt, és a keze egy pillanat alatt karmokká görbül. A kunyhó megtelik fekete füsttel,
és a láp békái, piócái mind feléd másznak. Meg kell küzdened a banyával. Ha legyőzöd, [[banya_halott]].''',
    fight([M('Lápi banya', 9, 8)], T('banya_halott')))

sec('banya_halott', '''A banya hamuvá omlik össze, és a kunyhó megrendül. A holdvirág a küszöb előtt elhervad, mintha a
banya életéhez lett volna kötve. A polcon csak egy fekete fiolát találsz, és egy cetlit: "Ábris
amulettje a lovagok temetőjében. A varjak ura félje." Elteszed a cetlit, és kimenekülsz, mielőtt a
kunyhó összedől. Visszamész a fűzfás szigetre: [[lap_sziget]].''', st(SZ, -1))

sec('lap_ejszaka', '''Leterítesz egy köpenyt a fűzfa gyökerei közé, és lefekszel. A köd lassan sötétkékre vált, aztán
feketére, és a láp hangjai megváltoznak: a békák elhallgatnak, és a suttogás közelebb jön. Éjfél
körül kék fények gyúlnak a víz fölött, egy, kettő, tíz, és lassan körbefogják a szigetet. A fűzfa
ágai megremegnek, mintha védeni próbálnának. Tedd próbára a szerencsédet! Ha szerencséd van, a fa
ereje megvéd: [[lap_alom]]. Ha nincs, a lidércek a szigetre lépnek: [[lap_lidercek]].''',
    luck(T('lap_alom'), T('lap_lidercek')))

sec('lap_alom', '''A kék fények a sziget partján megtorpannak, mintha egy láthatatlan falba ütköznének, és dühösen
sziszegve visszahúzódnak a ködbe. Te pedig elalszol, és azt álmodod, hogy egy ezüstös hajú asszony
áll a fűzfa alatt, és a homlokodra teszi a kezét. - A lápon a Hold vigyáz rád - mondja. Reggel
kipihenten ébredsz, a sebeid begyógyultak. Visszanyersz 4 ÉLETERŐ és 1 SZERENCSE pontot. Ha a
révészhez mész, [[revesz]]. Ha a Holt Fák felé, [[banya_ut]]. Ha a templomtorony felé, [[sullyedt]].''',
    st(E, 4), st(SZ, 1))

sec('lap_lidercek', '''A lidércek hideg, kék lángjai körülötted táncolnak, és mindegyik egy-egy elveszett vándor arcát
viseli. Nem bántanak, de a jelenlétük kiszívja belőled a meleget és az erőt. Egész éjjel vacogva
ülsz a fa törzsének dőlve, a kardodat markolva, és várod a hajnalt. Amikor végre feldereng, a
lidércek egy sóhajjal elhalványulnak. Elveszítesz 3 ÉLETERŐ pontot. Ha a révészhez mész, [[revesz]].
Ha a Holt Fák felé, [[banya_ut]]. Ha a templomtorony felé, [[sullyedt]].''', st(E, -3))
