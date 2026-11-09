;=============================================================================
; A SARKANY SZEME - lapozgatos kalandkonyv-motor, Videoton TVC 64K
; GRAPHICS 2 (512x240, 2 szin), Z80 @ 3.125 MHz, sjasmplus
;
; Kepernyo:  bal oldalt rajz (30 bajt = 240 pont x 240 sor),
;            jobb oldalt szoveg: 33 oszlop x 22 sor (8x10-es font), a 24. sor a menu.
; Memoria:   $19EF-  BASIC betolto, kod, tablak, font, tomoritett szoveg, rajzok
;                    (a CAS legfeljebb $BFFF-ig tart; az U2-ben levo adatot $B0 lapozassal olvassuk)
;            $C000-  rajz-puffer (7200 B), $DC40- szovegpuffer, $F000- valtozok, verem $FF00
; Lapozas:   MAP_LOGIC ($B0 = U0,U1,U2,U3): kicsomagolas, rajz betoltese
;            MAP_DRAW  ($90 = U0,U1,VID,U3): minden kepernyorajzolas (font, szoveg- es rajzpuffer
;                       ilyenkor is lathato, mert az U0/U1/U3-ban vannak)
; A megszakitasok tiltva, a kepkocka-szinkron a $59-es port 4. bitjen (CRTC flip-flop).
;=============================================================================

        DEVICE NOSLOT64K

VRAM        equ $8000
IMG_BUF     equ $C000
IMG_SIZE    equ 30*240
TEXT_BUF    equ $DC40
VARS        equ $F000
STACK_TOP   equ $FF00

P_SAVE      equ $0003           ; ROM: aktualis lapozas masolata
PORT03      equ $0B11
PORT05      equ $0B12
PORT06      equ $0B13
INKV        equ $0B4D
PAPERV      equ $0B4E
BORDERV     equ $0B4F

MAP_LOGIC   equ $B0
MAP_DRAW    equ $90
MAP_BASIC   equ $70

PAPER_COL   equ $00             ; 0I0G0R0B: fekete hatter
INK_COL     equ $50             ; vilagos zold (I+G): betuk, a rajzok feher reszei
BORDER_COL  equ $00

IMG_BYTES   equ 30
TXT_COL0    equ 31              ; a szoveg elso bajtoszlopa
TXT_W       equ 33              ; oszlopszam
TXT_ROWS    equ 22              ; szovegsorok: 0..21
PROMPT_ROW  equ 23

; billentyubitek
K_LEFT      equ $01
K_RIGHT     equ $02
K_UP        equ $04
K_DOWN      equ $08
K_FIRE      equ $10             ; Szokoz vagy Tuz
K_ESC       equ $20

; valtozok (U3)
cur_col     equ VARS+0
cur_row     equ VARS+1
inv         equ VARS+2          ; 0 vagy $FF (inverz kiiras)
cur_img     equ VARS+3
nch         equ VARS+4          ; valasztasok szama
sel         equ VARS+5
keys        equ VARS+6
kprev       equ VARS+7
knew        equ VARS+8
cur_sec     equ VARS+10         ; 2 bajt
sec_scr     equ VARS+12         ; 2: a fejezet szabaly-szkriptje
nch_tot     equ VARS+14         ; valasztasok + Lap (+ Ital)
rng         equ VARS+16         ; 2
VARS_LEN    equ 18
; jatekallapot (uj jateknal torlodik)
GAME_VARS   equ VARS+18
g_sk        equ VARS+18         ; UGYESSEG, Kezdeti
g_sk0       equ VARS+19
g_st        equ VARS+20         ; ELETERO
g_st0       equ VARS+21
g_lk        equ VARS+22         ; SZERENCSE
g_lk0       equ VARS+23
g_gold      equ VARS+24
g_pot       equ VARS+25         ; varazsital: 0 UGY, 1 ERO, 2 SZER
g_dose      equ VARS+26
res         equ VARS+27         ; az utolso proba / harc eredmenye
xv          equ VARS+28         ; segedszamlalo (huslarvak, patkanyok)
revisit     equ VARS+29         ; a fejezetben mar jartunk
oc_t        equ VARS+30         ; 2: ha ezt valasztja, elotte oc_ptr szkriptje fut (harc)
oc_ptr      equ VARS+32         ; 2
f_n         equ VARS+34
f_flags     equ VARS+35
f_ev        equ VARS+36
f_evp       equ VARS+37
f_ext       equ VARS+38
f_pdmg      equ VARS+39
f_mdmg      equ VARS+40
f_skmod     equ VARS+41
f_hitlim    equ VARS+42
f_round     equ VARS+43
f_hits      equ VARS+44
f_wins      equ VARS+45
f_tgt       equ VARS+46
f_rwon      equ VARS+47
f_msk       equ VARS+48         ; 4
f_mst       equ VARS+52         ; 4
f_pas       equ VARS+56
f_mas       equ VARS+57
f_rlost     equ VARS+58
f_line      equ VARS+59
lm_n        equ VARS+60
lm_sel      equ VARS+61
lm_row      equ VARS+62
oc_lbl      equ VARS+63         ; az oc_t menupont felirata: 0 Harc, 1 Proba
items       equ VARS+64         ; 8 bajt = 64 targy
MAX_CH      equ 16
choices     equ VARS+72         ; MAX_CH x 2 bajt
visited     equ VARS+104        ; 52 bajt: bejart fejezetek
sptr        equ VARS+156        ; 2
GAME_LEN    equ 160-18
shop_items  equ VARS+160        ; 12 x 2
lm_ptr      equ VARS+184        ; 12 x 2
lm_val      equ VARS+208        ; 12
NAME_LEN    equ 32
f_names     equ VARS+224        ; 4 x 32 (32-re igazitva)
cache_tag   equ VARS+352        ; 8: a gyorsitotar-helyek blokkszama ($FF = ures)
cache_next  equ VARS+360        ; a kovetkezo felulirando hely

;-----------------------------------------------------------------------------
; BASIC betolto: 10 PRINT USR(6659)
;-----------------------------------------------------------------------------
        ORG $19EF
        db $0F,$0A,$00,$DD
        db " USR"
        db $96
        db "6659"
        db $95,$FF
        db 0,0,0,0,0
        ASSERT $ == 6659

;=============================================================================
start:
        di
        ld (quit_sp+1),sp
        ld a,($1705)            ; a rendszer eszkoz/fuggveny bajtja es a pufferelesi jelzo:
        ld (sav_1705),a         ; a lemezkezeles atallitja, kilepeskor vissza kell adni
        ld a,($0B6B)            ; (kulonben a BASIC "System error 233"-mal all meg)
        ld (sav_0b6b),a
        ld a,MAP_LOGIC
        call setmap
        ld sp,STACK_TOP
        xor a
        out ($05),a             ; hang ki
        out ($06),a             ; 2 szinu mod (GRAPHICS 2)
        ld a,(PORT03)           ; a $03 felso fele a bovitohely-valasztas (HBF lemezkartya!):
        and $F0                 ; azt meg kell tartani, csak a billentyusor valtozhat
        out ($03),a
        ld a,BORDER_COL : out ($00),a
        call apply_pal
        ld hl,VARS
        ld de,VARS+1
        ld bc,VARS_LEN-1
        ld (hl),0
        ldir
    IFDEF DISK
        ld hl,cache_tag
        ld b,8
.ct:    ld (hl),$FF
        inc hl
        djnz .ct
        xor a
        ld (cache_next),a
    ENDIF
        ld a,r
        or 1
        ld (rng),a
        ld (rng+1),a
        call cls
        ; fall through

;-----------------------------------------------------------------------------
; cimlap: az 1. fejezet rajza + cim, Szokoz/Tuz indit, Esc kilep
;-----------------------------------------------------------------------------
title:
        ld hl,MUS_TITLE
        call music_play
        ld a,(SEC_IMG+1)
        or a
        call nz,draw_image
        call clear_text
        ld a,3 : ld hl,TITLE1 : call print_at
        ld a,5 : ld hl,TITLE2 : call print_at
        ld a,7 : ld hl,TITLE3 : call print_at
        ld a,12 : ld hl,TITLE4 : call print_at
        ld a,18 : ld hl,TITLE5 : call print_at
        ld a,19 : ld hl,TITLE6 : call print_at
    IFDEF DISK
        ld a,20 : ld hl,TITLE7 : call print_at
    ENDIF
        ld a,21 : ld hl,MSG_COLHINT : call print_at
.w:     call wait_key
        bit 5,a : jp nz,quit
        bit 4,a : jp nz,new_game
        call color_keys
    IFDEF DISK
        and K_DOWN              ; Le: a mentett jatek
        jr z,.w
        call disk_restore
        or a
        jp z,resume_game
        ld hl,MSG_NOSAVE
        call msg_wait
        call clear_prompt
    ENDIF
        jr .w

; print_at: A = sor, HL = szoveg (a sor elejetol, tordeles nelkul)
print_at:
        ld (cur_row),a
        xor a
        ld (cur_col),a
        jp print_str

;-----------------------------------------------------------------------------
; show_section: HL = fejezet szama (1..407)
;-----------------------------------------------------------------------------
show_section:
        ld sp,STACK_TOP
        push hl
        call music_stop
        pop hl
    IFDEF PROFILE
        ld a,1 : out ($FE),a    ; meres kezdete (fejezet megjelenitese)
    ENDIF
        ld (cur_sec),hl
        ld a,MAP_LOGIC
        call setmap
        ; valasztasok atmasolasa
        add hl,hl
        ld de,JUMPTAB
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        or h
        jp z,sec_missing
        ld a,(hl)
        ld (nch),a
        inc hl
        add a,a
        jr z,.nojmp
        ld c,a
        ld b,0
        ld de,choices
        ldir
.nojmp: ld (sec_scr),hl
        ld hl,0
        ld (oc_t),hl
        ; bejart fejezet?
        ld hl,(cur_sec)
        ld a,l
        and 7
        ld b,a
        srl h
        rr l
        srl h
        rr l
        srl h
        rr l
        ld de,visited
        add hl,de
        ld a,1
        inc b
.vb:    dec b
        jr z,.vm
        add a,a
        jr .vb
.vm:    ld c,a
        and (hl)
        ld (revisit),a
        ld a,(hl)
        or c
        ld (hl),a
        ; szoveg kicsomagolasa
    IFDEF DISK
        call sec_text_ptr       ; a fejezet blokkja a gyorsitotarban (szukseg eseten lemezrol)
    ELSE
        ld hl,(cur_sec)
        add hl,hl
        ld de,SEC_INDEX
        add hl,de
        ld e,(hl)
        inc hl
        ld d,(hl)
        ld hl,SEC_DATA
        add hl,de
    ENDIF
        ld de,TEXT_BUF
        call DECODE_SECTION
        ; rajz, ha van es nem az latszik
        ld hl,(cur_sec)
        ld de,SEC_IMG
        add hl,de
        ld a,(hl)
        or a
        jr z,.noimg
        ld b,a
        ld a,(cur_img)
        cp b
        ld a,b
        call nz,draw_image
.noimg:
        call print_section_text
        call draw_status
    IFDEF PROFILE
        ld a,2 : out ($FE),a    ; meres vege
    ENDIF
        ld hl,(sec_scr)
        call run_script
        jr choose

print_section_text:
        call clear_text
        ld hl,(cur_sec)
        ld a,h
        or l
        jr z,.intro
        ld de,INTRO2_SEC
        or a
        sbc hl,de
        add hl,de
        jr nz,.num
.intro:
        ld hl,MSG_INTRO         ; 0.: elozmenyek (lemezes valtozat)
        call print_str
        jr .nl
.num:   call print_num
        ld a,DOT_IDX
        call putc_nw
.nl:    call newline
        ld hl,TEXT_BUF
        jp print_wrapped

sec_missing:                     ; a fejezet nincs a demoban: vissza az elejere
        ld hl,0
        ld (oc_t),hl
        ld a,1
        ld (nch),a
        ld hl,1
        ld (choices),hl
        call clear_text
        ld hl,(cur_sec)
        call print_num
        ld a,DOT_IDX
        call putc_nw
        call newline
        ld hl,MSG_MISSING
        call print_wrapped
        ; fall through

;-----------------------------------------------------------------------------
; choose: valasztas a "Lapozz:" sorban (bal/jobb/fel/le, Szokoz/Tuz, Esc)
;-----------------------------------------------------------------------------
choose:
choose_again:
        ld a,(nch)
        or a
        jp z,.end
        inc a                   ; + Lap
        ld b,a
        ld a,(g_dose)
        or a
        jr z,.nd
        inc b                   ; + Ital
.nd:    ld a,b
        ld (nch_tot),a
        xor a
        ld (sel),a
.redraw:
        call draw_choices
.w:     call wait_key
        bit 5,a : jp nz,quit
        bit 4,a : jr nz,.go
        and K_LEFT|K_UP
        jr z,.next
        ld a,(sel)
        or a
        jr z,.w
        dec a
        ld (sel),a
        jr .redraw
.next:  ld a,(knew)
        and K_RIGHT|K_DOWN
        jr z,.w
        ld a,(nch_tot)
        ld b,a
        ld a,(sel)
        inc a
        cp b
        jr nc,.w
        ld (sel),a
        jr .redraw
.go:    ld a,(sel)
        call get_choice
        ld a,h
        inc a
        jr nz,.sec
        ld a,l
        inc a
        jp z,show_sheet         ; $FFFF
        jp drink                ; $FFFE
.sec:   ld de,(oc_t)            ; elotte harc?
        or a
        sbc hl,de
        add hl,de
        jp nz,show_section
        xor a                   ; a torzs PICK/ONLY-val masik celt adhat meg
        ld (nch),a
        push hl
        ld hl,(oc_ptr)
        call run_script
        pop hl
        ld a,(nch)
        or a
        jp z,show_section
        ld hl,(choices)
        jp show_section
.end:   ld hl,MUS_DEATH
        ld de,(cur_sec)
        ld a,e
        cp WIN_SEC & 255
        jr nz,.em
        ld a,d
        cp WIN_SEC >> 8
        jr nz,.em
        ld hl,MUS_WIN
.em:    call music_play
        ld hl,MSG_END
        ld de,(cur_sec)
        ld a,e
        cp WIN_SEC & 255
        jr nz,.ew
        ld a,d
        cp WIN_SEC >> 8
        jr nz,.ew
        ld hl,MSG_WIN
.ew:    call msg_wait
        jp new_game

; get_choice: A = sorszam -> HL = cel (a valasztasok utan: $FFFF Lap, $FFFE Ital)
get_choice:
        ld hl,nch
        cp (hl)
        jr c,.c
        sub (hl)
        ld hl,CH_SHEET
        ret z
        dec hl
        ret
.c:     add a,a
        ld l,a
        ld h,0
        ld de,choices
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ret

draw_choices:
        call clear_prompt
        ld a,(nch)
        cp 5
        jr nc,.nl
        ld hl,MSG_LAPOZZ
        call print_str
.nl:    ld b,0                  ; B = sorszam
.l:     ld a,(nch_tot)
        cp b
        ret z
        ld a,(sel)
        cp b
        ld a,0
        jr nz,.n
        dec a
.n:     ld (inv),a
        ld a,SP_IDX
        call putc_cur
        push bc
        ld a,b
        call get_choice
        ld de,MSG_LAP
        ld a,h
        inc a
        jr nz,.num
        ld a,l
        inc a
        jr z,.str
        ld de,MSG_ITAL
        jr .str
.num:   ld de,(oc_t)
        or a
        sbc hl,de
        add hl,de
        ld de,MSG_FIGHT
        jr nz,.nolbl
        ld a,(oc_lbl)
        or a
        jr z,.str
        ld de,MSG_TRY
        jr .str
.nolbl:
        call print_num
        jr .nx
.str:   ex de,hl
        call print_str
.nx:    pop bc
        xor a
        ld (inv),a
        inc b
        jr .l

; clear_prompt: a menusor torlese, kurzor az elejere
clear_prompt:
        push hl
        ld a,MAP_DRAW
        call setmap
        ld hl,(ROWTAB+2*PROMPT_ROW)
        ld c,10
.r:     push hl
        ld b,TXT_W
        xor a
.b:     ld (hl),a
        inc hl
        djnz .b
        pop hl
        ld de,64
        add hl,de
        dec c
        jr nz,.r
        ld a,PROMPT_ROW
        ld (cur_row),a
        xor a
        ld (cur_col),a
        ld (inv),a
        pop hl
        ret

;=============================================================================
; SZOVEG
;=============================================================================

; print_wrapped: HL = 0-val lezart font-index szoveg, szotordelessel, lapozassal
print_wrapped:
.word:  ld a,(hl)
        or a
        ret z
        cp SP_IDX
        jr nz,.notsp
        inc hl
        ld a,(cur_col)
        or a
        jr z,.word              ; sor elejen nincs szokoz
        cp TXT_W
        jr nc,.word
        ld a,SP_IDX
        call putc_adv
        jr .word
.notsp: push hl                 ; szo hossza -> B
        ld b,0
.m:     ld a,(hl)
        or a
        jr z,.me
        cp SP_IDX
        jr z,.me
        inc hl
        inc b
        jr .m
.me:    pop hl
        ld a,(cur_col)
        or a
        jr z,.p                 ; sor elejen mindenkepp ide kerul (tul hosszu szot tordeli a putc_adv)
        add a,b
        cp TXT_W+1
        call nc,newline
.p:     ld a,(hl)
        inc hl
        call putc_adv
        djnz .p
        jr .word

; putc_adv: kiir es lep; a sor vegen uj sor (HL, B, C megmarad)
putc_adv:
        call putc_nw
        push hl
        ld hl,cur_col
        inc (hl)
        ld a,(hl)
        pop hl
        cp TXT_W
        ret c
        ; fall through
; newline: uj sor; ha a szovegterulet betelt: "tovabb" es uj oldal (HL, B, C megmarad)
newline:
        xor a
        ld (cur_col),a
        ld a,(cur_row)
        inc a
        ld (cur_row),a
        cp TXT_ROWS
        ret c
        push hl
        push bc
        call clear_prompt
        ld hl,MSG_MORE
        call print_str
    IFDEF PROFILE
        ld a,3 : out ($FE),a    ; varakozas a "tovabb"-nal (a merésbol levonando)
    ENDIF
.w:     call wait_key
        bit 5,a : jp nz,quit
        bit 4,a : jr z,.w
    IFDEF PROFILE
        ld a,4 : out ($FE),a
    ENDIF
        call clear_text
        pop bc
        pop hl
        ret

; print_str: HL = szoveg, tordeles nelkul (menu, cim)
print_str:
        ld a,(hl)
        or a
        ret z
        call putc_nw
        push hl
        ld hl,cur_col
        inc (hl)
        pop hl
        inc hl
        jr print_str

; print_num: HL = 0..999, vezeto nullak nelkul (a kurzort lepteti)
print_num:
        ld c,0                  ; volt mar nem nulla jegy?
        ld de,100
        call .dig
        ld de,10
        call .dig
        ld c,1
        ld de,1
.dig:   ld b,0
.s:     or a
        sbc hl,de
        jr c,.d
        inc b
        jr .s
.d:     add hl,de
        ld a,b
        or c
        ret z
        ld c,1
        ld a,b
        add a,DIG0_IDX
        call putc_nw
        push hl
        ld hl,cur_col
        inc (hl)
        pop hl
        ret

; putc_nw: A = font-index kiirasa a (cur_col, cur_row) cellaba, leptetes nelkul
; minden regisztert megtart (AF kivetelevel); MAP_DRAW lapozas kell
putc_nw:
        push hl
        push de
        push bc
        ld c,a                  ; a sor vegen tul ne rajzoljon (a kovetkezo pontsor elejere, a rajzba lognek)
        ld a,(cur_col)
        cp TXT_W
        ld a,c
        jr c,.ok
        pop bc
        pop de
        pop hl
        ret
.ok:
        ld l,a
        ld h,0
        add hl,hl
        ld e,l
        ld d,h
        add hl,hl
        add hl,hl
        add hl,de               ; *10
        ld de,FONT
        add hl,de
        ex de,hl                ; DE = karakterkep
        ld a,(cur_row)
        add a,a
        ld l,a
        ld h,0
        ld bc,ROWTAB
        add hl,bc
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        ld a,(cur_col)
        add a,l
        ld l,a
        jr nc,.nc
        inc h
.nc:    ld a,(inv)
        ld c,a
        ld b,10
.l:     ld a,(de)
        xor c
        ld (hl),a
        inc de
        ld a,l
        add a,64
        ld l,a
        jr nc,.n2
        inc h
.n2:    djnz .l
        pop bc
        pop de
        pop hl
        ret

;=============================================================================
; KEPERNYO
;=============================================================================
setmap:
        ld (P_SAVE),a
        out ($02),a
        ret

cls:
        ld a,MAP_DRAW
        call setmap
        ld hl,VRAM
        ld de,VRAM+1
        ld bc,240*64-1
        ld (hl),0
        ldir
        ret

; clear_text: a szovegterulet (30..63. bajtoszlop) torlese, kurzor a bal felso sarokba
clear_text:
        ld a,MAP_DRAW
        call setmap
        ld hl,VRAM+30
        ld de,64-34
        ld c,TXT_ROWS*10
        xor a
.r:     ld b,34
.b:     ld (hl),a
        inc hl
        djnz .b
        add hl,de
        dec c
        jr nz,.r
        ld (cur_col),a
        ld (cur_row),a
        ld (inv),a
        ret

; draw_image: A = rajz sorszama (1..N_IMG); a bal oldali 30 bajtos savba
draw_image:
        ld (cur_img),a
        push af
        ld a,MAP_LOGIC
        call setmap
        pop af
    IFDEF DISK
        call load_image         ; -> HL = IMG_STAGE
    ELSE
        add a,a
        ld l,a
        ld h,0
        ld de,IMGTAB
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
    ENDIF
        ld de,IMG_BUF           ; U1/U2 -> U3
        ld bc,IMG_SIZE
        ldir
        ld a,MAP_DRAW
        call setmap
        ld hl,IMG_BUF
        ld de,VRAM
        ld a,240
.r:     ld bc,IMG_BYTES
        ldir
        ex de,hl
        ld bc,64-IMG_BYTES
        add hl,bc
        ex de,hl
        dec a
        jr nz,.r
        ret

ROWTAB:                         ; szovegsor -> VRAM cim (a szovegterulet elso oszlopa)
rr = 0
        DUP 24
        dw VRAM + rr*640 + TXT_COL0
rr = rr + 1
        EDUP

;=============================================================================
; BILLENTYUZET, SZINKRON, KILEPES
;=============================================================================
vsync:
        ld hl,3000
.w:     in a,($59)
        and $10
        jr z,.got
        dec hl
        ld a,h
        or l
        jr nz,.w
.got:   out ($07),a
        ret

; read_keys: keys = allapot, knew = uj lenyomasok
; kbd_row: A = billentyusor -> A = lenyomott bitek (1 = lenyomva).
; A $03 port felso felet (bovitohely-valasztas) a ROM masolatabol ($0B11) megtartja.
kbd_row:
        ld c,a
        ld a,(PORT03)
        and $F0
        or c
        out ($03),a
        in a,($58)
        cpl
        ret

read_keys:
        ld a,(keys)
        ld (kprev),a
        ld e,0
        ; 8. sor: fel=02 le=04 tuz=08 jobb=20 bal=40
        ld a,8 : call kbd_row
        ld c,a
        bit 6,c : jr z,$+4 : set 0,e
        bit 5,c : jr z,$+4 : set 1,e
        bit 1,c : jr z,$+4 : set 2,e
        bit 2,c : jr z,$+4 : set 3,e
        bit 3,c : jr z,$+4 : set 4,e
        ; 7. sor: Esc=08 Szokoz=20
        ld a,7 : call kbd_row
        ld c,a
        bit 3,c : jr z,$+4 : set 5,e
        bit 5,c : jr z,$+4 : set 4,e
        ld a,e
        ld (keys),a
        ld a,(kprev)
        cpl
        and e
        ld (knew),a
        ret

; wait_key: var egy uj lenyomasig; A = knew
wait_key:
        push hl
        push bc
        push de
.w:     call vsync
        call music_tick
        call rnd                ; a varakozas hossza keveri a veletlenszamot
        call read_keys
        ld a,(knew)
        or a
        jr z,.w
        pop de
        pop bc
        pop hl
        ret

quit:
.rel:   call vsync
        call read_keys
        ld a,(keys)
        or a
        jr nz,.rel
        ld a,(sav_1705)
        ld ($1705),a
        ld a,(sav_0b6b)
        ld ($0B6B),a
        ld a,MAP_BASIC          ; kozvetlenul: a verem (U3) ezutan eltunik, nem lehet CALL
        ld (P_SAVE),a
        out ($02),a
        ld a,(PORT06) : out ($06),a
        ld a,(PORT05) : out ($05),a
        ld a,(PORT03) : out ($03),a
        ld a,(BORDERV) : out ($00),a
        ld a,(PAPERV) : and 3 : add a,$60 : ld c,a
        xor a
        out (c),a
        ld a,(INKV) : and 3 : add a,$60 : ld c,a
        ld a,$55
        out (c),a
        out ($07),a
quit_sp:
        ld sp,0                 ; onmodosito: BASIC verem
        ei
        rst $30
        db $05                  ; CLS
        ret
sav_1705:   db 0
sav_0b6b:   db 0

;=============================================================================
        include "szabaly.asm"
        include "zene.asm"
    IFDEF DISK
        include "lemez.asm"
    ENDIF
        include "decoder.asm"
CODE_END:
        include "data.inc"

        ASSERT DATA_END <= $C000
    IFDEF DISK
        ASSERT JUMPTAB <= $8000        ; a font es a feliratok MAP_DRAW mellett is lathatok
        ASSERT NSLOT >= 2
        ASSERT disk_stack_top <= $8000
    ELSE
        ASSERT SEC_INDEX <= $8000      ; a font es a feliratok MAP_DRAW mellett is lathatok
    ENDIF
        ASSERT TEXT_BUF + 2500 <= VARS
        ASSERT f_names + 4*NAME_LEN <= STACK_TOP - 256
        ASSERT (f_names & 31) == 0
        SAVEBIN "kaland.bin", $19EF, DATA_END-$19EF
