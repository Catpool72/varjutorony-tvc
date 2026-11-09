// Minimal TVC 64K test harness for the prototype (not a full emulator).
// (kiegeszitve: 2 szinu mod kepmentese)
// Emulates: memory paging (port 02), 4 RAM pages + 16K VRAM, palette (60-63),
// video mode (06), keyboard matrix (03/58), 50 Hz CRTC IT flip-flop (59/07),
// profiling markers on port FE.  Runs code from $1A03 like "PRINT USR(6659)".
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "z80.h"

#define FRAME_CYC 62500UL

static uint8_t ram[4][16384], vrampg[4][16384];
static int plus = 0; static uint8_t p0f = 0;
#define vram (vrampg[(plus ? (p0f >> 4) & 3 : 0)])
static uint8_t p2 = 0x70, pal[4], vmode, kbrow, kb[16], ff = 1;
static unsigned long next_frame = FRAME_CYC;
static z80 cpu;
static int bad_write = 0;

typedef struct { int frame, row, mask; } kev;
static kev evs[16384]; static int nev;
typedef struct { int frame, addr, val, len, dump; } pk;
static pk pks[16384]; static int npk;
static int shots[2048]; static char shotname[2048][64]; static int nshot;
static unsigned long prof_start[32]; static unsigned long prof_sum[32], prof_max[32], prof_n[32];

static uint8_t *map(uint16_t a, int write) {
    int pg = a >> 14; uint16_t o = a & 0x3fff;
    switch (pg) {
    case 0: { int s = (p2 >> 3) & 3; if (s == 2) return &ram[0][o]; if (s == 3 && plus) return &vrampg[p0f & 3][o]; return NULL; }
    case 1: return &ram[1][o];
    case 2: return (p2 & 0x20) ? &ram[2][o] : &vrampg[plus ? (p0f >> 2) & 3 : 0][o];
    default: { int s = (p2 >> 6) & 3; if (s == 2) return &ram[3][o]; return NULL; }
    }
}
static uint8_t rb(void *u, uint16_t a) { uint8_t *p = map(a, 0); return p ? *p : 0xFF; }
static void wb(void *u, uint16_t a, uint8_t v) {
    uint8_t *p = map(a, 1);
    if (p) *p = v; else bad_write++;
}
/* Lemez (HLE): a VT-DOS kazettás felületének utánzata - RST 30h + D3 (open), D2 (blokk be), D4 (close).
   DISKDIR=<mappa>: a fájlok <NÉV>.CAS néven, a 128 bájtos külső fejléc után a 16 bájtos programfejléc és az adat.
   Ellenőrzi: a verem $C000 alatt legyen, a cél $BFFF-ig érjen, és a 2. lapon U2 legyen. */
static uint16_t ring[64]; static int rp; static uint8_t port03;
static FILE *dfile; static long disk_reads, disk_bytes;
static int disk_call(void) {
    const char *dir = getenv("DISKDIR");
    uint16_t ret = rb(0, cpu.sp) | (rb(0, cpu.sp + 1) << 8);
    uint8_t fn = rb(0, ret);
    if (getenv("DISKDBG")) fprintf(stderr, "rst30 fn=%02X ret=%04X dir=%s\n", fn, ret, dir ? dir : "-");
    if (!dir || (fn != 0xD3 && fn != 0xD2 && fn != 0xD4 && fn != 0x53 && fn != 0x51 && fn != 0x52 && fn != 0x54)) return 0;
    if (cpu.sp >= 0xC000) { fprintf(stderr, "DISK: verem az U3-ban (SP=%04X)\n", cpu.sp); exit(3); }
    if ((port03 & 0xF0) != (rb(0, 0x0B11) & 0xF0)) { fprintf(stderr, "DISK: a $03 port felso fele (%02X) nem egyezik a ROM-masolattal (%02X) - a bovitohely-valasztas elveszett\n", port03, rb(0, 0x0B11)); exit(3); }
    if ((fn & 0x80) ? rb(0, 0x1705) != 0xD0 : rb(0, 0x1705) != 0x50) { fprintf(stderr, "DISK: 1705H != D0\n"); exit(3); }
    /* a valódi VT-DOS a megszakítás-kezelővel együtt ~150-200 bájt vermet használ: itt 400 bájtot
       szemetelünk a verem alatt, hogy a verem alá tett változók hibája kiderüljön */
    for (int i = 1; i <= 400; i++) wb(0, cpu.sp - i, 0xA5);
    uint16_t de = (cpu.d << 8) | cpu.e, bc = (cpu.b << 8) | cpu.c;
    uint8_t st = 0;
    if (fn == 0xD3) {
        char name[64]; int n = rb(0, de); if (n > 16) n = 16;
        snprintf(name, sizeof name, "%s/", dir); int k = strlen(name);
        for (int i = 0; i < n; i++) name[k++] = rb(0, de + 1 + i);
        strcpy(name + k, ".CAS");
        if (dfile) { fprintf(stderr, "DISK: open, de mar nyitva\n"); exit(3); }
        dfile = fopen(name, "rb");
        if (!dfile) { st = 0x80; fprintf(stderr, "DISK: nincs %s\n", name); }
        else fseek(dfile, 128, SEEK_SET);
        cpu.cyc += 150000;                 /* keresés ~50 ms */
    } else if (fn == 0xD2) {
        if (!dfile) st = 0xE9;
        else if ((unsigned)de + bc > 0xC000 || !(p2 & 0x20)) { fprintf(stderr, "DISK: rossz cél %04X+%04X map %02X\n", de, bc, p2); exit(3); }
        else {
            for (unsigned i = 0; i < bc; i++) { int c = fgetc(dfile); if (c == EOF) { st = 0xEC; break; } wb(0, de + i, c); }
            cpu.cyc += 100UL * bc;             /* ~31 KB/s */
            disk_reads++; disk_bytes += bc;
        }
    } else if (fn == 0x53) {           /* létrehozás írásra: 128 bájtos CAS-fejléc, a többit a program írja */
        char name[64]; int n = rb(0, de); if (n > 16) n = 16;
        snprintf(name, sizeof name, "%s/", dir); int k = strlen(name);
        for (int i = 0; i < n; i++) name[k++] = rb(0, de + 1 + i);
        strcpy(name + k, ".CAS");
        if (dfile) { fprintf(stderr, "DISK: create, de mar nyitva\n"); exit(3); }
        dfile = fopen(name, "wb");
        if (!dfile) st = 0x80; else { static const uint8_t h[128] = {0x11}; fwrite(h, 1, 128, dfile); }
        cpu.cyc += 150000;
    } else if (fn == 0x51) {
        if (!dfile) st = 0xE9; else fputc(cpu.c, dfile);
    } else if (fn == 0x52) {
        if (!dfile) st = 0xE9;
        else { for (unsigned i = 0; i < bc; i++) fputc(rb(0, de + i), dfile); cpu.cyc += 100UL * bc; }
    } else { if (dfile) fclose(dfile); dfile = NULL; }
    cpu.a = st; if (getenv("DISKDBG")) fprintf(stderr, "  -> st=%02X de=%04X bc=%04X sp=%04X\n", st, de, bc, cpu.sp);
    cpu.sp += 2; cpu.pc = ret + 1;
    cpu.iff1 = cpu.iff2 = 1;                   /* a VT-DOS engedélyezett megszakítással tér vissza */
    return 1;
}

static uint8_t pin(z80 *z, uint8_t port) {
    switch (port) {
    case 0x58: return (uint8_t)~kb[kbrow & 15];
    case 0x59: return 0x40 | (ff << 4) | 0x0f;
    default: return 0xFF;
    }
}
static void pout(z80 *z, uint8_t port, uint8_t v) {
    switch (port) {
    case 0x02: p2 = v; break;
    case 0x0F: if (plus) p0f = v; else bad_write += 1000; break;
    case 0x03: kbrow = v & 15; port03 = v; break;
    case 0x04: case 0x05: case 0x06: {
        static uint8_t sp[3]; static int last_on = -1, last_f = -1, last_v = -1;
        sp[port - 4] = v; if (port == 6) vmode = v & 3;
        int on = (sp[1] >> 4) & 1, pitch = (sp[0] | (sp[1] << 8)) & 0xfff, vol = (sp[2] >> 2) & 15;
        int f = (pitch == 0xfff) ? 0 : (int)(195312.5 / (4096 - pitch));
        if (getenv("SNDLOG") && (on != last_on || (on && (f != last_f || vol != last_v))))
            fprintf(stderr, "snd f%lu %s %dHz vol%d\n", z->cyc / FRAME_CYC, on ? "ON " : "off", f, vol);
        last_on = on; last_f = f; last_v = vol;
        break; }
    case 0x07: ff = 1; break;
    case 0x60: case 0x61: case 0x62: case 0x63: pal[port - 0x60] = v; break;
    case 0xFE: {
        int id = v;
        if (id & 1) prof_start[id] = z->cyc;
        else if (id > 0) {
            unsigned long d = z->cyc - prof_start[id - 1];
            prof_sum[id - 1] += d; prof_n[id - 1]++;
            if (d > prof_max[id - 1]) prof_max[id - 1] = d;
        }
        break; }
    }
}
static void rgb(uint8_t c, uint8_t *o) {
    int i = (c >> 6) & 1, g = (c >> 4) & 1, r = (c >> 2) & 1, b = c & 1;
    int hi = i ? 255 : 170;
    o[0] = r ? hi : (i && !r && !g && !b ? 85 : 0);
    o[1] = g ? hi : (i && !r && !g && !b ? 85 : 0);
    o[2] = b ? hi : (i && !r && !g && !b ? 85 : 0);
}
static void shot(const char *name) {
    FILE *f = fopen(name, "wb");
    fprintf(f, "P6 512 480 255\n");
    for (int y = 0; y < 240; y++) {
        uint8_t line[512 * 3];
        for (int xb = 0; xb < 64; xb++) {
            uint8_t d = vram[y * 64 + xb];
            if (vmode == 0) {           /* 2 szinu mod: 8 pont/bajt, bit7 = bal, a bit a paletta-index */
                for (int i = 0; i < 8; i++) {
                    uint8_t o[3]; rgb(pal[(d >> (7 - i)) & 1], o);
                    memcpy(&line[(xb * 8 + i) * 3], o, 3);
                }
            } else
            for (int i = 0; i < 4; i++) {
                int c = vmode == 1 ? (((d >> (3 - i)) & 1) * 2 + ((d >> (7 - i)) & 1)) : 0;
                uint8_t o[3]; rgb(pal[c], o);
                for (int k = 0; k < 2; k++) memcpy(&line[((xb * 4 + i) * 2 + k) * 3], o, 3);
            }
        }
        fwrite(line, 1, sizeof line, f); fwrite(line, 1, sizeof line, f);
    }
    fclose(f);
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: tvcsim file.cas script.txt frames\n"); return 1; }
    FILE *f = fopen(argv[1], "rb");
    static uint8_t buf[65536]; size_t n = fread(buf, 1, sizeof buf, f); fclose(f);
    int size = buf[0x82] | (buf[0x83] << 8);
    if (buf[0] != 0x11 || buf[0x81] != 1 || 0x90 + size != (int)n) { fprintf(stderr, "bad cas\n"); return 1; }
    p2 = 0x70;
    wb(0, 0x0B13, 0x02); wb(0, 0x0B12, 0x00); wb(0, 0x0B11, 0x00); wb(0, 0x0B4F, 0x00);
    wb(0, 0x0B4D, 0x01); wb(0, 0x0B4E, 0x00);   // ROM copies: mode 16, INK 1, PAPER 0
    for (int i = 0; i < size; i++) wb(0, 0x19EF + i, buf[0x90 + i]);
    if (getenv("DISKDIR")) { wb(0, 0x0B11, 0x50); port03 = 0x50; }   /* HBF: bővítőhely-választás a ROM-másolatban és a porton */
    // a few BASIC-area bytes must form the loader line
    if (rb(0, 0x19EF) != 0x0F || rb(0, 0x19F2) != 0xDD) { fprintf(stderr, "loader line missing\n"); return 1; }

    FILE *s = fopen(argv[2], "r"); char w[64];
    while (fscanf(s, "%63s", w) == 1) {
        if (!strcmp(w, "key")) { fscanf(s, "%d %d %i", &evs[nev].frame, &evs[nev].row, &evs[nev].mask); nev++; }
        else if (!strcmp(w, "poke")) { fscanf(s, "%d %i %i", &pks[npk].frame, &pks[npk].addr, &pks[npk].val); pks[npk].dump = 0; npk++; }
        else if (!strcmp(w, "dump")) { fscanf(s, "%d %i %i", &pks[npk].frame, &pks[npk].addr, &pks[npk].len); pks[npk].dump = 1; npk++; }
        else if (!strcmp(w, "shot")) { fscanf(s, "%d %63s", &shots[nshot], shotname[nshot]); nshot++; }
    }
    fclose(s);
    int frames = atoi(argv[3]);
    plus = argc > 4 && !strcmp(argv[4], "plus");

    z80_init(&cpu);
    cpu.read_byte = rb; cpu.write_byte = wb; cpu.port_in = pin; cpu.port_out = pout;
    cpu.pc = 0x1A03; cpu.sp = 0x7F00; cpu.iff1 = cpu.iff2 = 0;
    int frame = 0;
    while (frame < frames) {
        ring[rp++ & 63] = cpu.pc;
        z80_step(&cpu);
        if (cpu.pc == 0x0030 && disk_call()) continue;
        if (cpu.pc == 0x0030) {
            printf("EXIT to BASIC at frame %d: p0f=%02X map=%02X mode=%d sp=%04X iff1=%d pal=%02X %02X %02X %02X\n",
                   frame, p0f, p2, vmode, cpu.sp, cpu.iff1, pal[0], pal[1], pal[2], pal[3]);
            return 0;
        }
        if (cpu.pc >= 0x8000 || cpu.pc < 0x1A03) { fprintf(stderr, "PC out of range: %04X at frame %d SP=%04X\ntrace:", cpu.pc, frame, cpu.sp); for (int i = 0; i < 64; i++) fprintf(stderr, " %04X", ring[(rp + i) & 63]); fprintf(stderr, "\n"); return 2; }
        if (cpu.halted) { fprintf(stderr, "HALT at frame %d\n", frame); return 2; }
        if (bad_write) { fprintf(stderr, "write to ROM/unmapped (map %02X) at PC %04X\n", p2, cpu.pc); return 2; }
        if (cpu.cyc >= next_frame) {
            next_frame += FRAME_CYC; frame++; ff = 0;
            for (int i = 0; i < nev; i++) if (evs[i].frame == frame) kb[evs[i].row] = evs[i].mask;
            for (int i = 0; i < npk; i++) if (pks[i].frame == frame) {
                if (!pks[i].dump) wb(0, pks[i].addr, pks[i].val);
                else { printf("dump f%d %04X:", frame, pks[i].addr); for (int k = 0; k < pks[i].len; k++) printf("%s%02X", k % 8 ? "" : " ", rb(0, pks[i].addr + k)); printf("\n"); }
            }
            for (int i = 0; i < nshot; i++) if (shots[i] == frame) shot(shotname[i]);
        }
    }
    if (disk_reads) printf("disk: %ld olvasas, %ld bajt\n", disk_reads, disk_bytes);
    printf("map=%02X mode=%d pal=%02X %02X %02X %02X  sp=%04X\n", p2, vmode, pal[0], pal[1], pal[2], pal[3], cpu.sp);
    const char *names[] = {"", "show_piece (erase+draw)", "", "full_redraw", "", "  cls", "", "  draw_grid", "", "  draw_settled", "", "  save_bg", "", "  erase_piece", "", "redraw_new (lerakas)"};
    for (int id = 1; id < 16; id += 2)
        if (prof_n[id]) printf("%-26s n=%-4lu avg=%6lu  max=%6lu ciklus  (max %.2f kepkocka)\n", names[id], prof_n[id],
                               prof_sum[id] / prof_n[id], prof_max[id], prof_max[id] / (double)FRAME_CYC);
    return 0;
}
