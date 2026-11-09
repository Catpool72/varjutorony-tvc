"""6. A torony belseje: udvar, kaszárnya, konyha, pince, katakomba, börtön."""
from kv import *

sec('udvar', '''A torony udvara kövezett, a kövek között gaz és fekete tollak. Középen egy kút áll, a kávájára
koponyákat raktak. Balra egy alacsony épület: a kaszárnya, az ablakai sötétek. Jobbra egy
kéményes épület, ahonnan zsíros füst és émelyítő szag árad: a konyha. Előtted a torony nagy
ajtaja, ami a csarnokba vezet. A torony tövében egy lépcső vezet le a pincébe, és az udvar sarkán
egy keskeny, kerek torony áll, tele varjakkal. Ha a kúthoz mész, [[kut_t]]. Ha a kaszárnyába,
[[kaszarnya]]. Ha a konyhába, [[konyha]]. Ha a csarnokba, [[csarnok]]. Ha a pincébe, [[pince]]. Ha a
varjak tornyába, [[varjuhaz]].''')

sec('kut_t', '''A kút káváján koponyák vigyorognak. A mélyéből halvány, ezüstös fény dereng, és a vödör kötele még
ép. Ha felhúzod a vödröt (egyszer teheted meg), [[kut_vodor]]. Ha belenézel a kútba, [[kut_nez]]. Ha visszamész az udvar
közepére, [[udvar]].''', gate(T('kut_vodor'), nvis('kut_vodor')))

sec('kut_vodor', '''A csörlő nyikorogva fordul, és a vödör lassan felemelkedik. Tedd próbára a szerencsédet! Ha szerencséd
van, a vödörben a víz mellett három aranytallér csillog, amit valaki a kútba ejtett. Ha nincs, egy
kígyó tekeredik ki belőle, és megmarja a kezed. Visszamész az udvar közepére: [[udvar]].''',
    luck(), iff('res', [gold(3)], [st(E, -2)]))

sec('kut_nez', '''Belenézel a kútba. A víz tükrén nem a saját arcodat látod, hanem egy szobát: egy sötét cellát,
ahol egy fiú ül a szalmán, és egy fűzfasípot forgat a kezében. Bence! A kép elhomályosul, és egy
hang suttog a mélyből: "A pince alatt, a holtak útján túl." Visszamész az udvar közepére: [[udvar]].''',
    st(SZ, 1))

sec('kaszarnya', '''A kaszárnya ajtaja nyikorogva nyílik. Bent hosszú teremben priccsek sorakoznak, és mindegyiken egy
csontváz fekszik páncélban, mintha aludnának. A terem végén egy ládát látsz, a falon pedig
kardok és pajzsok lógnak. Ha óvatosan a ládához lopakodsz, [[kaszarnya_lada]]. Ha egy pajzsot veszel le
a falról, [[kaszarnya_pajzs]]. Ha kimész, [[udvar]].''')

sec('kaszarnya_lada', '''Lábujjhegyen haladsz a priccsek között. Az egyik csontváz koponyája megmozdul, mintha utánad
nézne. Tedd próbára a szerencsédet! Ha szerencséd van, [[lada_nyit]]. Ha nincs, a csontvázak
felébrednek: [[kaszarnya_harc]].''', luck(T('lada_nyit'), T('kaszarnya_harc')))

sec('kaszarnya_pajzs', '''Leakasztasz egy pajzsot a falról. A szöge csikorogva kiesik a falból, és csörömpölve a kőre esik. A
priccseken a csontvázak mind egyszerre ülnek fel. [[kaszarnya_harc]].''')

sec('kaszarnya_harc', '''A csontvázak felkelnek a priccsekről, és fegyvert ragadnak. Hárman jönnek feléd, a többiek csak
csörögnek, de nem kelnek fel. Egyenként küzdesz meg a hárommal. Ha van ezüsttőröd, az ezüst
kétszeresen sebzi őket. Ha legyőzöd őket, [[lada_nyit]].''',
    iff('ezusttor',
        fight([M('Csontváz katona', 6, 5), M('Csontváz katona', 6, 5), M('Csontváz őrmester', 7, 6)], pdmg=4, mdmg=2),
        fight([M('Csontváz katona', 6, 5), M('Csontváz katona', 6, 5), M('Csontváz őrmester', 7, 6)])),
    only(T('lada_nyit')))

sec('lada_nyit', '''Kinyitod a ládát. Benne a katonák zsoldja: öt aranytallér, egy rozsdás, de használható sisak, ami
megvédi a fejedet, és egy tekercs. A tekercsen ez áll: "A Mester rendelete: a foglyot a konyhai
vaskulccsal zárt cellában kell tartani. Gorgó felel érte." Elteszed az aranyat, és felveszed a
sisakot. Kimész az udvarra: [[udvar]].''', gold(5), st(U, 1))

sec('konyha', '''A konyhában egy óriási üstben fortyog valami zöld lé, a gőze émelyítő. Az üst mellett egy
tagbaszakadt, szürke bőrű alak kavargatja a levest: egy ghoul, a torony szakácsa. Gorgó a neve, ez
áll a kötényén. Az övén egy kulcskarikán egy nagy vaskulcs lóg. Háttal áll neked. Ha rátámadsz,
[[ghoul_harc]]. Ha a zöld üvegcse tartalmát a levesbe öntöd, [[ghoul_meregy]]. Ha a füstölt húst a
sarokba dobod, hogy elcsald, [[ghoul_hus]]. Ha csendben kihátrálsz, [[udvar]].''',
    gate(T('ghoul_meregy'), 'meregital'), gate(T('ghoul_hus'), 'hus'))

sec('ghoul_harc', '''Gorgó megfordul, és a fogait vicsorgatva rád ront a merőkanalával. A karmai mérgesek: minden sebe
kétszeresen fáj. Meg kell küzdened vele. Ha legyőzöd, [[ghoul_gyoz]].''',
    fight([M('Gorgó, a ghoul szakács', 8, 8)], T('ghoul_gyoz'), mdmg=3))

sec('ghoul_meregy', '''Lábujjhegyen az üsthöz lopakodsz. Tedd próbára az ügyességedet! Ha sikerül, a zöld üvegcse tartalmát
észrevétlenül a levesbe csorgatod: [[ghoul_mergezett]]. Ha nem, Gorgó megfordul: [[ghoul_harc]].''',
    skill(T('ghoul_mergezett'), T('ghoul_harc')))

sec('ghoul_mergezett', '''A sárkányfű-méreg szó nélkül feloldódik a levesben. Gorgó megkóstolja, csettint, aztán merít még egy
nagy kanállal. Néhány pillanat múlva fuldokolni kezd, és összeesik. Leveszed az övéről a
vaskulcsot. A leves többi részét pedig gondosan kiöntöd a lefolyóba. [[ghoul_gyoz]].''', lose('meregital'))

sec('ghoul_hus', '''A füstölt húst a konyha sarkába hajítod. Gorgó felkapja a fejét, és szimatolva odacsoszog. Amíg
mohón falatozik, odalopakodsz, és leakasztod a vaskulcsot az övéről. Tedd próbára a szerencsédet!
Ha szerencséd van, nem veszi észre: [[ghoul_kijut]]. Ha nincs, megfordul: [[ghoul_harc]].''',
    lose('hus'), luck(T('ghoul_kijut'), T('ghoul_harc')))

sec('ghoul_kijut', '''A kulcs a kezedben, és Gorgó még mindig csámcsog. Csendben kiosonsz a konyhából. A vaskulcs nehéz és
hideg; a börtön cellájáé. [[udvar]].''', gain('vaskulcs'))

sec('ghoul_gyoz', '''Gorgó holtan fekszik a konyha kövén. A vaskulcs a tiéd. A konyha kamrájában találsz egy kenyeret,
egy szép darab sajtot és egy korsó tiszta vizet; megeszel egy keveset. A konyha hátsó ajtaja egy
folyosóra nyílik, ami a csarnok mellé vezet. Ha a hátsó ajtón mész ki, [[csarnok_oldal]]. Ha az
udvarra mész vissza, [[udvar]].''', gain('vaskulcs'), st(E, 3), iff('!kenyer', gain('kenyer')))

sec('pince', '''A pince boltíves, hideg és nyirkos. Hordók és ládák sorakoznak, a pókhálók a mennyezetig érnek.
A sarokban egy csapóajtó, a túlsó falon egy bronzzal kivert, vastag ajtó, rajta egy nagy zár és
egy felirat: "Katakomba". A lépcső felfelé az udvarra vezet. Ha van lámpásod, meggyújtod:
[[pince_feny]]. Ha nincs, a sötétben tapogatózol: [[pince_sotet]].''',
    gate(T('pince_feny'), 'lampas'), gate(T('pince_sotet'), '!lampas'))

sec('pince_feny', '''A lámpás fényében egy hatalmas, kutyányi pókot pillantasz meg a mennyezeten. Ahogy a fény ráesik,
lezuhan a hálójáról, és rád támad. Legalább látod, hova üss. Meg kell küzdened vele. Ha legyőzöd,
[[pince_kincs]].''', fight([M('Óriáspók', 7, 8)], T('pince_kincs')))

sec('pince_sotet', '''A sötétben valami a nyakadra ereszkedik egy fonálon: egy hatalmas pók! Vakon kell harcolnod.
Meg kell küzdened vele. Ha legyőzöd, [[pince_kincs]].''',
    fight([M('Óriáspók', 7, 8)], T('pince_kincs'), skmod=-2))

sec('pince_kincs', '''A pók hálójában egy szerencsétlen tolvaj csontváza lóg. A kezében egy kis ládikát szorongat.
Kinyitod: benne négy aranytallér, és egy tojásnyi, sárgán izzó kő, ami meleg, mint a napsugár. Ha
már van napköved, ez a második; egy is elég. A pók marása még ég a nyakadon: ha van holdvirágod, megrágsz egy szirmot,
és visszanyersz 3 ÉLETERŐ pontot; ha nincs, a méreg elvesz 1 ÉLETERŐ pontot. A katakomba ajtajához mész: [[katakomba_ajto]]. Ha az udvarra mész
fel, [[udvar]].''', gold(4), gain('napko'), iff('holdvirag', [st(E, 3)], [st(E, -1)]))

sec('katakomba_ajto', '''A katakomba ajtaja vastag tölgyfa, bronzzal kiverve, a zárja egy bronzlakat. Ha van bronzkulcsod,
[[katakomba]]. Ha tolvajkulccsal próbálkozol, [[kata_tolvaj]]. Ha van kőfaragó vésőd, a zár körül
kivághatod a fát: [[kata_veso]]. Ha visszamész a pincébe, [[pince_vissza]].''',
    gate(T('katakomba'), 'bronzkulcs'), gate(T('kata_tolvaj'), 'tolvajkulcs'), gate(T('kata_veso'), 'fahej'))

sec('pince_vissza', '''A pince csendes, a pók holtan fekszik. A lépcső felfelé az udvarra vezet, a katakomba ajtaja zárva.
Ha az udvarra mész fel, [[udvar]]. Ha még egyszer a katakomba ajtajához mész, [[katakomba_ajto]].''')

sec('kata_tolvaj', '''A bronzlakat régi és bonyolult. Tedd próbára az ügyességedet! Ha sikerül, a zár kattan: [[katakomba]].
Ha nem, a drót beletörik a zárba, és a zárat már nem tudod kinyitni vele: [[pince_vissza]].''',
    skill(T('katakomba'), T('pince_vissza')))

sec('kata_veso', '''A törp vésője könnyedén belevág a vastag tölgyfába. Néhány ütés, és a zár egy darab fával együtt
kiesik az ajtóból. Az ajtó kitárul. [[katakomba]].''')

sec('katakomba', '''A katakombában száraz és hideg a levegő. Végtelen folyosók, a falakba vájt fülkékben koponyák és
csontok, egykori szerzetesek maradványai. A folyosó kettéágazik: balra a csontok között halvány zöld
fény dereng, jobbra egy lépcső vezet fel. Ha balra mész, [[kata_zold]]. Ha jobbra, a lépcső felé,
[[kata_lepcso]]. Ha a csontokkal teli oldalkamrába lépsz, [[kata_csontkamra]].''')

sec('kata_zold', '''A zöld fény egy kis kápolnából árad, ahol a szerzetesek ereklyéit őrzik. Egy kőoltáron egy kristály
kehely áll, benne tiszta víz, ami magától világít. Fölötte felirat: "A Holdanya könnye. Igyál, ha
tiszta a szándékod." Ha iszol a kehelyből, [[kata_kehely]]. Ha nem nyúlsz hozzá, és továbbmész a
folyosón, [[kata_mely]].''')

sec('kata_kehely', '''Iszol egy kortyot. A víz hideg és édes, és a fáradtságod elszáll. Visszanyersz 4 ÉLETERŐ és 2
SZERENCSE pontot. Ha van üres üvegcséd, vagy kulacsod, meg is töltheted: a szentelt víz soha nem
fogy el a kehelyből. Továbbmész a folyosón: [[kata_mely]].''',
    st(E, 4), st(SZ, 2), iff('!szenteltviz', gain('szenteltviz')))

sec('kata_mely', '''A folyosó egyre mélyebbre vezet, a csontok egyre sűrűbben. Egyszer csak megtorpansz: a folyosó
közepén egy szobor áll, egy szerzetes kőszobra, az arca rémült. Mögötte még egy, és még egy:
kővé dermedt emberek. És a folyosó végén mozgást látsz: valami közeledik, és csoszogó léptei
visszhangzanak. A kőszemű őr! Ha van ezüsttükröd, [[koszem_tukor]]. Ha behunyod a szemed, és vakon
harcolsz, [[koszem_vak]]. Ha elmenekülsz a lépcső felé, [[koszem_menekul]].''',
    gate(T('koszem_tukor'), 'tukor'))

sec('koszem_tukor', '''Elfordítod a fejed, és a tükröt a lény felé tartod. Egy dühös, sziszegő hang, aztán csend. Amikor
óvatosan visszanézel a tükörben, egy újabb kőszobrot látsz a folyosó végén: egy pikkelyes, kígyófejű
lényt, a saját pillantása dermesztette kővé. A szobor lábánál egy szerzetes kincsesládája: hat
aranytallér. Továbbmész: [[kata_lepcso2]].''', gold(6), st(SZ, 1))

sec('koszem_vak', '''Behunyod a szemed, és a hallásodra hagyatkozol. A lény sziszeg, és a karmai a levegőt hasítják.
Vakon kell harcolnod. Meg kell küzdened vele. Ha legyőzöd, [[koszem_gyoz]].''',
    fight([M('Kőszemű őr', 8, 7)], T('koszem_gyoz'), skmod=-3))

sec('koszem_gyoz', '''A lény holtan esik össze. Nem nézel rá, amíg el nem haladtál mellette. A folyosó végén egy kis
fülkében egy szerzetes kincsesládáját találod: hat aranytallér. Továbbmész: [[kata_lepcso2]].''', gold(6))

sec('koszem_menekul', '''Megfordulsz, és rohansz vissza a folyosón. A lény sziszegése követ. Tedd próbára a szerencsédet! Ha
szerencséd van, [[kata_lepcso]]. Ha nincs, akaratlanul visszanézel: [[koszem_ko]].''',
    luck(T('kata_lepcso'), T('koszem_ko')))

sec('koszem_ko', '''Egy pillanatra hátrafordulsz, és a pillantásod találkozik a lény sárga, kígyószerű szemével. A tagjaid
megmerevednek, a bőröd szürkévé válik, és a szíved megáll. Újabb szobor áll a katakomba folyosóján. A
kalandod itt véget ért.''')

sec('kata_lepcso', '''A lépcső egy rövid folyosóra vezet fel, amelynek a végén vasrácsos ajtó áll. Mögötte cellák: a
torony börtöne. A folyosón egy fáklya ég. Ha belépsz a börtönbe, [[borton]].''')

sec('kata_lepcso2', '''A katakomba folyosója egy lépcsőben végződik, ami felfelé visz. A tetején egy vasrácsos ajtó,
mögötte cellák: a torony börtöne. [[borton]].''')

sec('borton', '''A börtön folyosóján nyirkos cellák sorakoznak. A legtöbb üres, csak csontok és rozsdás láncok
hevernek bennük. A folyosó végén, egy vasajtós cellában valaki mozog. Ha van fűzfasípod, és
megfújod, [[borton_sip]]. Ha a cellához mész, [[bence_cella]]. Ha a börtön ajtaján a csarnok felé
mész, [[csarnok]].''', gate(T('borton_sip'), 'sip'))

sec('borton_sip', '''Belefújsz a fűzfasípba, és a hangja végigcseng a börtön folyosóján. A folyosó végén lévő cellából
azonnal felel egy másik síp hangja, és egy rekedt, fiatal hang kiált: - Nagyapa? Ki az? Itt vagyok!
Odasietsz: [[bence_cella]].''', st(SZ, 1))

sec('bence_cella', '''A vasajtó kis rácsos ablakán át egy sápadt, piszkos arcú fiú néz rád: Bence! - Ki vagy? Morvath
küldött? - kérdezi gyanakodva. A cella ajtaján nagy vaszár. Ha van vaskulcsod, kinyithatod: [[bence_nyit]].
Ha tolvajkulccsal próbálkozol, [[bence_tolvaj]]. Ha nincs mivel kinyitnod, [[bence_nincs]].''',
    gate(T('bence_nyit'), 'vaskulcs'), gate(T('bence_tolvaj'), 'tolvajkulcs'))

sec('bence_tolvaj', '''Előveszed a tolvajkulcsot, és a zárban kezdesz kotorászni. Tedd próbára az ügyességedet! Ha
sikerül, a zár kattan: [[bence_nyit]]. Ha nem, a zár makacs: [[bence_nincs]].''',
    skill(T('bence_nyit'), T('bence_nincs')))

sec('bence_nincs', '''- Nem tudod kinyitni? - Bence a rácsba kapaszkodik. - A szakács, Gorgó tartja a kulcsot, a konyhában!
Kérlek, hozd el! - Megígéred neki, hogy visszajössz érte. A börtön ajtaja a csarnokba vezet:
[[csarnok]].''')

sec('bence_nyit', '''A cella ajtaja kinyílik. Bence a nyakadba borul, aztán szégyenlősen elhúzódik. - Bocsáss meg.
Nagyon féltem. - Ha van Bodor levele, odaadhatod neki: [[bence_level]]. Ha azonnal tovább akarsz
indulni, [[bence_vele]].''', gate(T('bence_level'), 'level'))

sec('bence_level', '''Bence remegő kézzel bontja fel a levelet. Ahogy olvassa, a szeme megtelik könnyel. - Nagyapa azt írja,
bízzak benned, és fogadjak szót. - Összehajtja, és a keblébe dugja. - Akkor szót fogadok. Megyek
veled. - A tekintete elszánt. [[bence_vele]].''', lose('level'), st(SZ, 2))

sec('bence_vele', '''- Tudok egy-két dolgot - mondja Bence. - Hallottam, ahogy Gorgó beszél. A Holdkő a torony
tetején van, Morvath termében, egy pecsétes ajtó mögött. Az ajtón három jel van: a Nap, a csillag
és a Hold. Rossz sorrendben megnyomva tűz csap ki belőle. És még valami: Morvath fél a naptól. A
csarnokban a démon alszik, ha a nap süt az ablakon. Indulunk? Ha a börtön ajtaján át a csarnokba
mész vele, [[csarnok]]. Ha a sebesült Bencét előbb holdvirággal gyógyítod meg, [[bence_gyogyit]].''',
    gain('bence'), gate(T('bence_gyogyit'), 'holdvirag'))

sec('bence_gyogyit', '''Bence karján mély, gennyedő seb van, ahol a varjak megtépték. A holdvirág egy szirmát a sebre
teszed, és a seb szemed láttára beforr. Bence ámulva nézi a karját. - Mintha soha nem lett volna
ott. - Felkap egy rozsdás kardot az egyik cellából. - Most már harcolni is tudok! [[csarnok]].''',
    st(SZ, 1))

sec('kata_csontkamra', '''Az oldalkamra mennyezetig tele van csontokkal: koponyákból rakott oszlopok, combcsontokból font
boltívek. A közepén egy csontból faragott oltár áll, rajta egy ezüst gyertyatartó. Ahogy belépsz,
a koponyák szemüregében zöld fény gyúl, és a csontok zörögve megmozdulnak: három szerzetes
csontváza bontakozik ki a falból, csuhába burkolózva. Ha van rézcsengőd, és megrázod, [[csontkamra_csengo]].
Ha harcolsz velük, [[csontkamra_harc]]. Ha visszahátrálsz a folyosóra, [[katakomba]].''',
    gate(T('csontkamra_csengo'), 'csengo'))

sec('csontkamra_csengo', '''A csengő tiszta hangja végigzeng a kamrán, és a szerzetesek csontvázai megtorpannak. Egyikük, a
legöregebb, lassan meghajol előtted, aztán a társaival együtt visszahúzódik a falba, és a zöld fény
kihuny a koponyákban. Az oltáron az ezüst gyertyatartó mellett egy kis erszény fekszik, benne öt
aranytallér: a zarándokok adománya. Elteszed; a szerzetesek talán nem bánják, hiszen az adományuk
most a Holdkő visszaszerzését szolgálja. Visszamész a folyosóra: [[katakomba]].''', gold(5))

sec('csontkamra_harc', '''A szerzetesek csontvázai lassan, de összehangoltan támadnak, mint akik egész életükben egy ütemre
imádkoztak. Egyenként küzdesz meg velük. Ha legyőzöd őket, [[katakomba]].''',
    fight([M('Csontváz szerzetes', 6, 5), M('Csontváz szerzetes', 6, 5), M('Csontváz apát', 7, 6)], T('katakomba')))
