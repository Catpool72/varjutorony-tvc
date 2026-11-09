# A Varjútorony ura – saját kalandkönyv a TVC kalandkönyv-motorhoz

**413 fejezet, kb. 175 000 karakter** (A Sárkány szeme 407 fejezet / 184 000 karakter), **72 kép**, lemezes
(VT-DOS) változat Videoton TV-Computerre. Klasszikus fantasy, közepes nehézség: több út a győzelemig, öt módja a végső
összecsapásnak, tíz halálos csapda a harcokon felül, és egy jobb befejezés (Bence kiszabadítása, Kelemen hazatérése).
Saját írás: szöveg, szabályok, a programmal rajzolt ideiglenes képek és a zene.

## Fordítás (a fő mappából)
```
python3 build.py --book varjutorony --disk    # -> build_varjutorony_disk/varjutorony.dsk
```
A lemez szinte tele van: 93 fájl, kb. 20 KB szabad marad (a MENTES fájlnak elég).

## Felépítés
- `fejezetek/*.py` – a fejezetek régiónként (falu, erdő, láp, hágó, a torony külseje, belseje, felső része,
  befejezés): `sec(név, szöveg, *szabályok)`. A szövegben `[[név]]` hivatkozás áll, ebből lesz a
  "lapozz a(z) N-re/-ra" (a névelő és a rag a szám kiejtéséből); a szabályokban `T('név')`.
- `fejezetek/bovit_*.py` – kiegészítő leírások: a fejezet első választási mondata elé kerülnek.
- `fejezetek/kv.py` – a közös segédek (`sec`, `fight`, `vis`/`nvis`: járt-e már ott, `bovit`, `load_all`).
- `konyv.py` – számozás (rögzített véletlen sorrend, 1 = kezdet), `book.json`, `varjutorony.txt`.
- `rules_book.py` – a tárgyak listája és a szabályok fordítása (a `build.py --book` használja).
- `ellenoriz.py` – ellenőrzés: üres menü, legfeljebb 6 cél, 20 000 véletlen játék (minden fejezet elérhető,
  mind az öt győzelmi út működik). `hianyzo.py` – hiányzó hivatkozások, hossz régiónként.
- `kepek.py` + `rajzkeszlet.py` – a 72 kép: melyik fejezethez tartozik, leírás és angol prompt, és egy
  programmal rajzolt ideiglenes változat. Kimenet: `ill/p1..p72.png`, `img_sections.json`, `KEPEK.md`, `kepek.json`.
- `kepcsere.py` – egy új (pl. másik MI által rajzolt) kép beillesztése, előnézettel.

## A képek cseréje
A `KEPEK.md` táblázatában minden képnek van magyar leírása és angol promptja (a közös stílusleírással a
`kepek.json`-ban egyben). A legjobb eredményt **fekete tusrajz fehér papíron** stílus adja, álló 5:8 arányban
(pl. 640×1024): a TVC a kép sötét részeit festi zölddel, a világosakat feketén hagyja.

```
python3 kepcsere.py 12 letoltott_kep.png          # -> ill/p12.png és elonezet/p12.png
python3 kepcsere.py 12 letoltott_kep.png --neg    # világos rajz sötét alapon / éjszakai jelenet: megfordítva
python3 kepcsere.py 12 letoltott_kep.png --gamma 1.4   # sötétebb eredmény (kisebb szám: világosabb)
python3 kepcsere.py 1 zold_fekete_kep.png --neg --lagyit 2   # már zöld-fekete, pontozott kép (így készült az 1. kép)
python3 kepcsere.py 1 kep.png --teljes                # vágás nélkül, fekete sávokkal
cd .. && python3 build.py --book varjutorony --disk
```
Az `elonezet/pN.png` mutatja, hogyan fog kinézni a TVC-n (zöld-fekete, raszterezve). A `kepek.py` újrafuttatása
felülírja az `ill/` mappát a programmal rajzolt képekkel – cserék után ne futtasd.

## Tárgyak és utak (röviden – vigyázat, árulkodó!)
A torony kapuja: ezüstkulcs (malomgödör, a remete találós kérdése, a tükörterem), vagy a fal (kötél, véső,
ügyesség), vagy a rejtett kiskapu (térkép: Ádor vagy Vince szelleme). Morvath ellen: a valódi neve (a molnár,
Ábris szelleme a gyűrűvel, a holló, a napló, a levél), szentelt víz, napkő (törpök sírja, pince), puszta kard,
vagy a legjobb: az apja gyűrűje. A halálátok ellen Ábris amulettje véd. Bence a börtönben: vaskulcs (a ghoul
szakács) vagy tolvajkulcs (Fürge, a rablók).
