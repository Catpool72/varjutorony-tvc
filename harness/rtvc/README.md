# Teszt valódi VT-DOS alatt (rtvc)

A `ktest.rs` teki **rtvc** emulátorának (https://github.com/teki/rtvc, MIT) könyvtárára épül:
TVC 1.2 ROM + HBF kártya + VT-DOS 1.2, a valódi lemezvezérlővel. A szkript billentyűt nyom,
képet ment, és utasításonként figyeli a futást (rossz PC, érvénytelen utasítás, a lemezverem mélysége).

Fordítás (crates.io nélkül is): az rtvc forrásában a `Cargo.toml` függőségeit ki kell venni, a `fatfs`
helyére egy csonk kell (csak új lemez formázásához kell), a `machine_type.rs` négy segédfüggvényét
`pub`-ra kell tenni, és a `ktest.rs`-t `src/bin/`-be kell tenni. Futtatás:

```
ktest snapshots/boot12dos.rtvcsnap ../build_disk/sarkany.dsk pelda_indulas.txt
```
Parancsok: `type <szöveg>`, `enter`, `key <kód>`, `frames <n>`, `shot <név>` (PPM), `pc`,
`watch <n>`, `fuzz <képkocka> <mag> <verem alja> <verem teteje>`, `peek <cím> <n>`, `dumpu <fájl>`.

Eredmény (2026-11-08): négy véletlen billentyűzéses futás, egyenként 11–13 perc játék, hiba nélkül;
a VT-DOS a megszakítás-kezelővel együtt **194 bájt** vermet használt.
