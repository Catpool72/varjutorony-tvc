; ===========================================================================
;  A Sárkány szeme – fejezet-kicsomagoló (BPE + kanonikus Huffman), Z80
; ===========================================================================
;  Bemenet:  HL = a tömörített fejezet első bájtja (a book_text.bin-ben)
;            DE = kimeneti puffer (min. 2407 bájt: leghosszabb fejezet + 0)
;  Kimenet:  a puffer a fejezet szövege, 0-val lezárva
;            HL = a lezáró 0 címe
;  Rontja:   AF, BC, DE, HL   (IX, IY és a kiegészítő regiszterek érintetlenek,
;            a megszakításokat nem tiltja)
;  Verem:    max. 2 * (BPE-mélység + 3) bájt (a táblákhoz < 30 bájt)
;
;  Szükséges táblák (book_tables.asm, az encode.py generálja):
;    NBASE (< 256), CHARTAB, RULES, LIMOFF, SYMS
;
;  A bemenet bájtonkénti olvasása egyetlen helyen történik (DEC_FETCH).
;  Ha a szöveg több memórialapon van (pl. a 64+ videó-RAM lapjain), ott kell
;  a lapváltást elvégezni, amikor HL átlépi a lap határát.
; ===========================================================================

DECODE_SECTION:
        ld (dec_inptr),hl
        ld (dec_outptr),de
        ld a,080h               ; üres bitpuffer (csak az őrbit)
        ld (dec_bitbuf),a
ds_loop:
        call DEC_GETTOK         ; HL = következő token
        call DEC_EXPAND         ; Z = fejezet vége
        jr nz,ds_loop
        ld hl,(dec_outptr)
        ld (hl),0
        ret

; ---------------------------------------------------------------------------
; DEC_GETTOK – egy token kanonikus Huffman-dekódolása
;   code = 0; hosszanként: code = code*2 + bit
;   ha code < LIM[len]: token = SYMS[code + OFF[len]]
; Regiszterek a ciklusban: BC = code, HL = LIMOFF mutató, E = bitpuffer
; (alján 1-es őrbit; ha az kicsúszik, új bájt jön). Kimenet: HL = token
; ---------------------------------------------------------------------------
DEC_GETTOK:
        ld a,(dec_bitbuf)
        ld e,a
        ld bc,0
        ld hl,LIMOFF
gt_loop:
        sla e                   ; Carry = következő bit
        jr nz,gt_bit
        push hl                 ; elfogyott a bájt: új bájt olvasása
        ld hl,(dec_inptr)
DEC_FETCH:                      ; <- itt olvas a memóriából (lapváltás ide)
        ld a,(hl)
        inc hl
        ld (dec_inptr),hl
        pop hl
        scf
        adc a,a                 ; Carry = bit7, A = bájt*2 + 1 (őrbit)
        ld e,a
gt_bit:
        rl c
        rl b                    ; code = code*2 + bit
        ld a,c
        sub (hl)
        inc hl
        ld a,b
        sbc a,(hl)              ; Carry, ha code < LIM[len]
        inc hl                  ; (az inc hl nem rontja a flageket)
        jr c,gt_found
        inc hl
        inc hl
        jr gt_loop
gt_found:
        ld a,e
        ld (dec_bitbuf),a
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a                  ; HL = OFF[len]
        add hl,bc               ; HL = code + OFF = index a SYMS-ben
        add hl,hl
        ld bc,SYMS
        add hl,bc
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a                  ; HL = token
        ret

; ---------------------------------------------------------------------------
; DEC_EXPAND – token kibontása a kimenetre (BPE, a jobb oldalak a veremben)
; Bemenet: HL = token. Kimenet: Z = END token (fejezet vége), NZ = folytatás
; A ciklusban BC = kimeneti mutató.
; ---------------------------------------------------------------------------
DEC_EXPAND:
        ld bc,(dec_outptr)
        ld de,0FFFFh            ; őrérték a veremben
        push de
ex_loop:
        ld a,h
        or a
        jr nz,ex_rule
        ld a,l
        cp NBASE
        jr nc,ex_rule           ; token >= NBASE -> szabály
        ld de,CHARTAB           ; alapkarakter
        add hl,de
        ld a,(hl)
        or a
        jr z,ex_end             ; 0 = END
        ld (bc),a
        inc bc
ex_next:
        pop hl
        ld a,h
        and l
        inc a                   ; A = 0, ha HL = FFFFh (őrérték)
        jr nz,ex_loop
        ld (dec_outptr),bc
        or 1                    ; NZ: a fejezet folytatódik
        ret
ex_rule:
        ld de,-NBASE
        add hl,de               ; HL = token - NBASE
        add hl,hl
        add hl,hl               ; * 4
        ld de,RULES
        add hl,de
        ld e,(hl)
        inc hl
        ld d,(hl)               ; DE = bal
        inc hl
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a                  ; HL = jobb
        push hl                 ; a jobb oldal később jön
        ex de,hl                ; először a bal oldal
        jr ex_loop
ex_end:
        pop hl                  ; őrérték le a veremről
        ld (dec_outptr),bc
        xor a                   ; Z
        ret

; ---------------------------------------------------------------------------
; Munkaváltozók (5 bájt)
; ---------------------------------------------------------------------------
dec_inptr:   dw 0
dec_outptr:  dw 0
dec_bitbuf:  db 0
