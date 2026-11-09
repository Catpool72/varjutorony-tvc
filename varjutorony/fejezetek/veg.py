"""7. A befejezés: Morvath, a menekülés, a hazatérés."""
from kv import *

sec('morvath_terem', '''A köpenyes alak lassan megfordul. Fiatalabb, mint gondoltad: sápadt, beesett arcú férfi, a szeme
fekete, mint a varjúé, és a vállán egy ősz holló ül. - Hát eljöttél - mondja halkan. - Fenyvesvölgy
hőse. Ugyanazok küldtek, akik engem kicsúfoltak. - Felemeli a kezét, és a Holdkő fénye elsötétül. -
Holnap telihold. És a völgy, amely gyűlölt, az enyém lesz. Ha kimondod a valódi nevét,
[[morvath_nev]]. Ha átnyújtod neki az apja gyűrűjét, [[morvath_gyuru]]. Ha szentelt vízzel locsolod meg,
[[morvath_viz]]. Ha a napkövet emeled a magasba, [[morvath_napko]]. Ha kardot rántasz, [[morvath_harc]].''',
    gate(T('morvath_nev'), 'nev'), gate(T('morvath_gyuru'), 'gyuru'), gate(T('morvath_viz'), 'szenteltviz'),
    gate(T('morvath_napko'), 'napko'))

sec('morvath_nev', '''- Kelemen! - kiáltod. - Kelemen, Gáspár molnár fia! - A varázsló megtántorodik, mintha arcul ütötték
volna. A fekete fény, ami körülvette, megremeg és szétfoszlik. A holló riadtan felrebben a vállától.
- Honnan... honnan tudod? - Most csak egy sápadt, megrémült férfi áll előtted, egy tőrrel a
kezében. Mégis rád támad. Meg kell küzdened vele. Ha legyőzöd, [[morvath_legyozve]].''',
    fight([M('Kelemen', 6, 6)], T('morvath_legyozve')))

sec('morvath_viz', '''Kirántod a dugót, és a szentelt vizet Morvathra locsolod. A víz sisteregve gőzölög a köpenyén, és a
varázsló felüvölt. A fekete fény meggyengül körülötte, de még mindig ott van. Morvath egy fekete
pengét húz elő a semmiből, és rád ront. Meg kell küzdened vele. Ha legyőzöd, [[morvath_legyozve]].''',
    lose('szenteltviz'), fight([M('Morvath (meggyengült)', 8, 8)], T('morvath_legyozve')))

sec('morvath_napko', '''A napkövet a magasba emeled, és vakító, aranyszínű fény önti el a termet. Morvath felsikolt, és a
szeme elé kapja a kezét. A sötétség, amiből az ereje táplálkozik, elillan a fény elől. Vakon,
tántorogva támad rád. Meg kell küzdened vele. Ha legyőzöd, [[morvath_legyozve]].''',
    fight([M('Morvath (elvakítva)', 8, 8)], T('morvath_legyozve')))

sec('morvath_harc', '''Kardot rántasz, és rárontasz. Morvath felnevet, és a keze egy mozdulatával fekete pengét idéz a
semmiből. A holló is rád csap, a karmaival a szemedet keresve. Morvath ereje teljes, és minden
fordulóban kétszer támad: egyszer a pengével, egyszer a varázslatával. Meg kell küzdened vele. Ha
legyőzöd, [[morvath_legyozve]].''', fight([M('Morvath, a varjak ura', 10, 12)], T('morvath_legyozve'), mdbl=1))

sec('morvath_gyuru', '''Lassan előveszed az ezüstgyűrűt, és a tenyereden felé nyújtod. Morvath megdermed. - Az anyám gyűrűje.
- A hangja elcsuklik. - Honnan van? - Az apádtól - feleled. - Azt üzeni, hogy vár téged. - Aztán a nevén
szólítod: [[gyuru_nev]].''')

sec('gyuru_nev', '''- Kelemen - mondod csendesen. - Gáspár minden este a rajzodat nézi. Haza akar vinni. - A varázsló keze
remeg. A fekete fény körülötte lassan elhalványul, és a holló a vállán halkan, szomorúan károg. -
Apám... - suttogja Kelemen, és a térdre rogy. Sír, mint egy gyerek. A Holdkő fénye felragyog, mintha
megkönnyebbült volna. [[kelemen_megter]].''')

sec('morvath_legyozve', '''Morvath a földre rogy, a köpenye szétterül körülötte, mint egy fekete szárny. Az utolsó erejével
feléd emeli a kezét, és rekedten, gyűlölettel suttogni kezd: a halálátkot. A szavai a levegőben
fekete füstként kavarognak, és feléd úsznak. Ha Ábris amulettje a nyakadban van, [[atok_amulett]]. Ha
nincs, csak a szerencse menthet meg: [[atok_szerencse]].''',
    gate(T('atok_amulett'), 'amulett'), gate(T('atok_szerencse'), '!amulett'))

sec('atok_amulett', '''A fekete füst eléri a mellkasodat, de Ábris amulettje fehér fénnyel felragyog, és az átok szétfoszlik,
mint a köd. Az amulett halkan megreped, és a szellemkezek, amelyek az átkot hozták, visszafordulnak.
Morvath szemében rémület. Az átok őt magát éri el. Egy utolsó sóhajjal elterül, és a teste fekete
tollak halmazává hullik szét. [[holdko]].''')

sec('atok_szerencse', '''A fekete füst eléri a mellkasodat, és jeges hideg szorítja össze a szívedet. Tedd próbára a
szerencsédet! Ha szerencséd van, az átok gyenge, mert Morvath már haldoklik: [[atok_tuleled]]. Ha nincs,
[[atok_halal]].''', luck(T('atok_tuleled'), T('atok_halal')))

sec('atok_tuleled', '''A szíved egy pillanatra megáll, a világ elsötétül, aztán... újra dobban. Térdre esel, zihálsz, de
élsz. Az átok elszállt. Elveszítesz 4 ÉLETERŐ pontot. Morvath egy utolsó sóhajjal elterül, és a teste
fekete tollak halmazává hullik szét. [[holdko]].''', st(E, -4))

sec('atok_halal', '''A jeges hideg a szívedig hatol. Még látod, ahogy Morvath fekete tollakká hullik szét, és hallod, ahogy a
holló felkárog. Aztán lehunyod a szemed. A völgy megmenekült, a Holdkő az oltáron ragyog, de te
már nem viszed haza. A kalandod itt véget ért.''')

sec('kelemen_megter', '''Kelemen feltápászkodik, és a Holdkőhöz lép. Leemeli az oltárról, és a kezedbe adja. - Vidd vissza a
kápolnába. És... - lehajtja a fejét - mondd meg apámnak, hogy hazamegyek. Ha nem kerget el. - A holló
a válláról a te válladra száll, és halkan károg. Ekkor a torony megremeg: Kelemen varázslata tartotta
egyben a régi falakat, és most, hogy elengedte, omlani kezdenek. - Fussatok! - kiáltja. [[omlas]].''',
    gain('kelemen'))

sec('holdko', '''A Holdkő az oltáron ragyog, fehér fénye betölti a termet. Leemeled, és a köpenyed alá rejted. Hűvös és
nehéz, mintha a Hold egy darabja volna. Ekkor a torony megremeg alattad. Morvath varázslata tartotta
egyben a régi falakat, és most, hogy halott, omlani kezdenek. Kövek hullanak a kupoláról. [[omlas]].''')

sec('omlas', '''A kupola üvege csörömpölve hullik, a padló megreped. Ha Bence veled van, [[omlas_bence]]. Ha nincs,
de tudod, hogy a börtönben raboskodik, [[bence_keres]]. Ha a sas a barátod, és a tetőn várja, hogy
hívd, [[sas_ment]]. Ha a csigalépcsőn rohansz lefelé, [[lepcson_le]].''',
    gate(T('omlas_bence'), 'bence'), gate(T('bence_keres'), '!bence'), gate(T('sas_ment'), 'sas'))

sec('omlas_bence', '''Bence a kezedbe kapaszkodik. - Erre! A cselédlépcső! - kiáltja, és egy rejtett ajtóhoz rángat a
terem falában. Ha követed, [[cseledlepcso]]. Ha a sas a barátod, és inkább a tetőre futtok, [[sas_ment]].''',
    gate(T('sas_ment'), 'sas'))

sec('cseledlepcso', '''A keskeny cselédlépcső a fal belsejében kanyarog lefelé, a por és a kőzápor elől védve. Bence fürgén
szalad előtted, ő itt többször is járt, amikor a börtönből a konyhára vitték. A lépcső a konyhába
torkollik, és onnan kirohantok az udvarra, éppen akkor, amikor a torony csúcsa összeomlik
mögöttetek. [[kijut]].''')

sec('bence_keres', '''A fiú! Nem hagyhatod itt! Lerohansz a csigalépcsőn, a kövek a fejed körül hullanak. A csarnokon át
a börtönbe futsz. Tedd próbára a szerencsédet! Ha szerencséd van, [[bence_talal]]. Ha nincs, [[bence_nem]].''',
    luck(T('bence_talal'), T('bence_nem')))

sec('bence_talal', '''A börtön folyosóján a mennyezet már beomlott, de a cella fala is megrepedt, és Bence kipréselte magát
a résen. Kormos, véres, de él! - Tudtam, hogy jössz! - kiáltja. Kézen fogod, és együtt rohantok ki a
börtön ajtaján, át a csarnokon, ki az udvarra, éppen akkor, amikor a torony csúcsa összeomlik.
[[kijut]].''', gain('bence'), st(E, -2))

sec('bence_nem', '''A börtön folyosóját már elzárta egy beomlott fal. Hiába kiabálsz, csak a kövek moraját hallod.
Egy újabb gerenda zuhan le melletted, és a por a torkodat fojtogatja. Nincs más választásod:
kirohansz a toronyból, éppen akkor, amikor a csúcsa összeomlik. Elveszítesz 4 ÉLETERŐ pontot. [[kijut]].''',
    st(E, -4))

sec('sas_ment', '''Felrohansz a tetőteraszra, és kiáltasz. A hatalmas sas a felhők közül csap le, és a karmai közé
kap, vagy a hátára enged fel. A torony csúcsa recsegve dől meg alattatok, és a sas fölé emelkedik a
porfelhőnek. A völgy fölött körözve látod, ahogy a Varjútorony összeomlik, és a varjak szétszélednek
minden irányba. A sas a domb lábánál tesz le. [[kijut]].''')

sec('lepcson_le', '''Rohansz lefelé a csigalépcsőn. A kövek a fejed körül hullanak, a lépcsőfokok megrepednek a lábad
alatt. Tedd próbára az ügyességedet! Ha sikerül, épségben leérsz: [[kijut]]. Ha nem, egy kő eltalál:
[[lepcson_seb]].''', skill(T('kijut'), T('lepcson_seb')))

sec('lepcson_seb', '''Egy kő a válladba csapódik, és legurulsz a lépcsőn. Elveszítesz 4 ÉLETERŐ pontot. Feltápászkodsz, és
vérző fejjel, sántikálva menekülsz ki az udvarra, éppen akkor, amikor a torony csúcsa összeomlik.
[[kijut]].''', st(E, -4))

sec('kijut', '''A Varjútorony morajlással összeomlik, és hatalmas porfelhő száll fel a romjaiból. Amikor elül, a
domb tetején már csak egy halom fekete kő áll. A varjak szétszéledtek, és a völgy fölött, hosszú idő
után először, kék az ég. A Holdkő a kezedben ragyog. Ha Bence veled van, [[hazateres_bence]]. Ha
egyedül vagy, [[hazateres]].''', gate(T('hazateres_bence'), 'bence'), gate(T('hazateres'), '!bence'))

sec('hazateres', '''Egyedül indulsz haza. Az út hosszú, de most nem fenyeget semmi: a farkasok elbújnak, a láp
suttogása elhallgatott. Két nap múlva, telihold estéjén érsz Fenyvesvölgybe. A falu kapujában a
fiatal őr meglát, és kiabálva rohan a főtér felé. Bodor sírva ölel meg, amikor a kezébe adod a
Holdkövet, de a szeme a hátad mögé néz, Bencét keresi. [[hazateres_vege]].''')

sec('hazateres_vege', '''- Bence? - kérdezi halkan. Lehajtod a fejed. Ekkor a falu kapujából kiáltás hallatszik: egy kormos,
rongyos fiú botorkál be rajta, egy ősz holló a vállán. Bence! A romok közül mászott elő, és a holló
vezette haza. A falu ujjong, Bodor és Rozália sírva ölelik az unokájukat. [[unnep]].''', gain('bence'))

sec('hazateres_bence', '''Bencével együtt indultok haza. A fiú egész úton beszél: a varjakról, a börtönről, a remetéről, és
arról, hogy ő is hős akar lenni, mint te. Két nap múlva, telihold estéjén értek Fenyvesvölgybe. A
falu kapujában a fiatal őr meglát, és kiabálva rohan a főtér felé. Bodor és Rozália sírva ölelik
meg az unokájukat, és Bodor remegő kézzel veszi át tőled a Holdkövet. [[unnep]].''', st(SZ, 2))

sec('unnep', '''Másnap a Holdkő újra a kápolna fülkéjébe kerül. Márk atya megáldja, Gyopár néni virágot tesz elé,
Bendegúz, a kovács pedig olyan hangosan kongatja a haranglábat, hogy a fogadóban leesnek a korsók a
polcról. Fenyvesvölgy népe háromnapos lakomát csap a tiszteletedre, és Bodor a falu minden aranyát
a kezedbe nyomja, ahogy megígérte. Ha Kelemen megígérte, hogy hazatér, [[kelemen_haza]]. Ha nem,
[[gyozelem]].''', gate(T('kelemen_haza'), 'kelemen'), gate(T('gyozelem'), '!kelemen'))

sec('kelemen_haza', '''A lakoma harmadik napján egy sápadt, kopott köpenyes férfi érkezik a faluba, egy ősz holló a vállán.
A falubeliek gyanakodva néznek utána, de te tudod, ki az. Elkíséred a Malom utcára, és bekopogtok
az öreg molnár ajtaján. Gáspár félvak szemmel néz a fiára, aztán szó nélkül átöleli. Aznap este a
malom ablakában sokáig ég a gyertya, és a konyhából nevetés hallatszik. [[gyozelem]].''')

sec('gyozelem', '''Telihold éjszakáján a Holdkő ezüstös fénye beragyogja az egész völgyet, a fenyőerdőt, a lápot és a
hágó havas csúcsait. Varjúvá nem változik senki. A Varjútorony romjain már csak a szél fütyül, és a
varjak, akik Morvath rabszolgái voltak, szabadon szállnak a mezők fölött. Fenyvesvölgyben még sokáig
mesélnek a vándorról, aki egyedül indult a torony ellen. Bence pedig minden este a fűzfasípján
fújja azt a dalt, amit a hősről szerzett. A Varjútorony ura legyőzetett. Kalandod véget ért: GYŐZTÉL!''')
