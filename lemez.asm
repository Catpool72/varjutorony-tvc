;=============================================================================
; LEMEZ: a teljes konyv VT-DOS lemezrol (HBF kartya). A VT-DOS a kazettas
; rendszerhivasokon at erheto el (RST 30h):  D3h megnyitas (DE = nev: hossz + betuk),
; D2h blokk-beolvasas (DE = cel, BC = hossz), D4h lezaras; A = 0 siker.
; Az 1705h-n az eszkoz/irany (D0h = lemez, bemenet), a 0B6Bh = 0 bufferelatlan eleres.
; A hivas alatt a ROM a 3. lapra SYS-t lapoz es engedelyezi a megszakitast,
; ezert a verem es a valtozok itt $C000 alatt vannak, a cel legfeljebb $BFFF,
; utana DI es ujra MAP_LOGIC. (Forras: teki/tvc-ports, Laser Squad lemezes betoltoje.)
; A lemezen minden fajl .CAS: a 128 bajtos kulso fejlec utan a 16 bajtos programfejlec,
; amit elobb atolvasunk, aztan az adat.
;=============================================================================
DOS_DEV     equ $1705
DOS_BUF     equ $0B6B
CHUNK_MAX   equ 4096

; disk_load: DE = nev, HL = cel, BC = hossz -> A = 0 / hibakod
disk_load:
        ld (dl_name),de
        ld (dl_dest),hl
        ld (dl_len),bc
        ld (dl_sp),sp
        ld sp,disk_stack_top
        ld a,$82                ; kek keret (a keret bitjei: I0G0R0B0): lemezolvasas folyik (ha igy marad: a VT-DOS hivas nem tert vissza)
        out ($00),a
        call music_silence      ; a betoltes alatt ne szoljon a hang
        ld a,MAP_LOGIC
        ld (P_SAVE),a
        out ($02),a
        ld a,$D0
        ld (DOS_DEV),a
        xor a
        ld (DOS_BUF),a
        ld de,(dl_name)
        rst $30
        db $D3
        or a
        jr nz,.done
        ld de,disk_hdr
        ld bc,16
        rst $30
        db $D2
        or a
        jr nz,.close
        ld de,(dl_dest)
        ld bc,(dl_len)
        rst $30
        db $D2
.close: push af
        rst $30
        db $D4
        pop af
.done:
disk_done:                      ; kozos befejezes: DI, lapozas, verem, video
        di
        ld b,a
        ld a,MAP_LOGIC
        ld (P_SAVE),a
        out ($02),a
        ld sp,(dl_sp)
        xor a                   ; a ROM a videomodot, a palettat es a keretet is allithatta
        out ($06),a
        ld a,BORDER_COL : out ($00),a
        push bc
        call apply_pal
        pop bc
        ld a,b
        ret

; disk_load_retry: mint a disk_load, de hiba eseten uzenet es ujraproba
disk_load_retry:
        push de
        push hl
        push bc
        call disk_load
        or a
        jr z,.ok
        ld hl,MSG_DISKERR
        ld de,MSG_RETRY
        call msg_num            ; "Lemezhiba: 128 Szokoz: ujra"
        pop bc
        pop hl
        pop de
        jr disk_load_retry
.ok:    pop bc
        pop hl
        pop de
        ret

; set_name: A = sorszam (0..99), C = betu -> disk_name = 3,"X12"
set_name:
        ld b,'0'-1
.t:     inc b
        sub 10
        jr nc,.t
        add a,'0'+10
        ld (disk_name+3),a
        ld a,b
        ld (disk_name+2),a
        ld a,c
        ld (disk_name+1),a
        ld a,3
        ld (disk_name),a
        ld de,disk_name
        ret

; sec_text_ptr: (cur_sec) -> HL = a tomoritett szoveg (a gyorsitotarban), MAP_LOGIC
sec_text_ptr:
        ld hl,(cur_sec)
        ld d,h
        ld e,l
        add hl,hl
        add hl,de
        ld de,SEC_CHUNK         ; fejezetenkent: blokk, eltolas (2)
        add hl,de
        ld a,(hl)
        inc hl
        ld e,(hl)
        inc hl
        ld d,(hl)
        push de
        call ensure_chunk
        pop de
        add hl,de
        ld a,MAP_LOGIC
        jp setmap

; ensure_chunk: A = blokk -> HL = a helye a gyorsitotarban
ensure_chunk:
        ld hl,cache_tag
        ld bc,NSLOT*256         ; B = helyek, C = sorszam
.f:     cp (hl)
        jr z,.hit
        inc hl
        inc c
        djnz .f
        ; nincs bent: a kovetkezo helyre toltjuk
        ld b,a
        ld a,(cache_next)
        ld c,a
        inc a
        cp NSLOT
        jr c,.n
        xor a
.n:     ld (cache_next),a
        ld hl,cache_tag
        ld a,l
        add a,c
        ld l,a
        ld (hl),$FF             ; tolt-ig ervenytelen
        push hl
        push bc
        ld a,b
        add a,a
        ld l,a
        ld h,0
        ld de,CHUNK_LEN
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        push hl                 ; hossz
        call slot_addr          ; C -> HL
        ld a,b
        push hl
        ld c,'T'
        call set_name
        pop hl
        pop bc
        call disk_load_retry
        pop bc
        pop hl
        ld (hl),b
.hit:   ; C = hely
slot_addr:
        ld a,c
        rlca
        rlca
        rlca
        rlca                    ; *16 -> *4096
        add a,CACHE >> 8
        ld h,a
        ld l,CACHE & 255
        ret

; load_image: A = rajz (1..N) -> HL = IMG_STAGE (a rajz betoltve)
load_image:
        ld c,'I'
        call set_name
        ld hl,IMG_STAGE
        ld bc,IMG_SIZE
        call disk_load_retry
        ld hl,IMG_STAGE
        ret

;-----------------------------------------------------------------------------
; MENTES: egyetlen mentes a lemezen (MENTES.CAS). A VT-DOS kimenete: 1705h = 50h,
; 53h letrehozas (DE = nev), 51h karakter ki (C), 52h blokk ki (DE, BC), 54h lezaras.
; Tartalom: "SZ", a program valtozatszama (DATA_END), majd a VARS elso SAVE_LEN bajtja
; (fejezet, valasztasok, rajz, pontok, targyak, arany, bejart fejezetek, ...).
;-----------------------------------------------------------------------------
SAVE_LEN    equ 352             ; VARS..VARS+351 (a gyorsitotar-cimkek nelkul)
SAVE_MAGIC  equ 'S' + 256*'Z'

; disk_save -> A = 0 / hibakod
disk_save:
        ld a,MAP_LOGIC
        call setmap
        ld hl,VARS
        ld de,save_buf+4
        ld bc,SAVE_LEN
        ldir
        ld hl,SAVE_MAGIC
        ld (save_buf),hl
        ld hl,DATA_END
        ld (save_buf+2),hl
        ld (dl_sp),sp
        ld sp,disk_stack_top
        ld a,MAP_LOGIC
        ld (P_SAVE),a
        out ($02),a
        ld a,$82                ; kek keret
        out ($00),a
        ld a,$50                ; lemez, kimenet
        ld (DOS_DEV),a
        xor a
        ld (DOS_BUF),a
        ld de,save_name
        rst $30
        db $53
        or a
        jp nz,disk_done
        ld hl,save_hdr
        ld b,16
.h:     ld c,(hl)
        push bc
        push hl
        rst $30
        db $51
        pop hl
        pop bc
        or a
        jr nz,.close
        inc hl
        djnz .h
        ld de,save_buf
        ld bc,SAVE_LEN+4
        rst $30
        db $52
.close: push af
        rst $30
        db $54
        ld c,a
        pop af
        or c
        jp disk_done

; disk_restore -> A = 0: az allas visszatoltve a VARS-ba; kulonben nincs (jo) mentes
disk_restore:
        ld de,save_name
        ld hl,save_buf
        ld bc,SAVE_LEN+4
        call disk_load
        or a
        ret nz
        ld hl,(save_buf)
        ld de,SAVE_MAGIC
        or a
        sbc hl,de
        jr nz,.bad
        ld hl,(save_buf+2)
        ld de,DATA_END
        sbc hl,de
        jr nz,.bad
        ld hl,save_buf+4
        ld de,VARS
        ld bc,SAVE_LEN
        ldir
        xor a
        ret
.bad:   ld a,1
        ret

; resume_game: a visszatoltott allas folytatasa (rajz, szoveg, menu)
resume_game:
        ld sp,STACK_TOP
        ld a,(cur_img)
        or a
        call nz,draw_image
        call sec_text_ptr
        ld de,TEXT_BUF
        call DECODE_SECTION
        call print_section_text
        call draw_status
        jp choose_again

save_name:  db 6,"MENTES"
save_hdr:   db 0, 0             ; adatfajl
            dw SAVE_LEN+4
            db 0                ; nem indul el magatol
            ds 11

; ide, $C000 ala: a lemezhivasok verme es valtozoi. A VT-DOS a megszakitas-kezelovel
; egyutt valodi gepen (rtvc + VT-DOS 1.2) 150 bajtnal is melyebbre visz le: a 160 bajtos verem
; alatti valtozokat felulirta. Ezert bo verem, es a valtozok a verem FOLOTT vannak.
            ds 768
disk_stack_top:
dl_name:    dw 0
dl_dest:    dw 0
dl_len:     dw 0
dl_sp:      dw 0
disk_name:  ds 4
disk_hdr:   ds 16
save_buf:   ds SAVE_LEN+4
