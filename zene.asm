;=============================================================================
; ZENE: egyszolamu lejatszo a TVC hanggeneratorara. Kepkockankent egy lepes
; (a wait_key varakozo ciklusabol), a hangok rovid lecsengessel.
; Dalformatum (zene.py): db hang, hossz ... ; 0 = szunet, $FF = ismetles, $FE = vege
;=============================================================================
mus_ptr     equ VARS+368        ; 2: a kovetkezo hang (0 = nem szol)
mus_loop    equ VARS+370        ; 2: a dal eleje
mus_cnt     equ VARS+372        ; hatralevo kepkockak
mus_amp     equ VARS+373        ; hangero (0..15)
mus_env     equ VARS+374        ; lecsenges-szamlalo
MUS_AMP0    equ 11
MUS_FLOOR   equ 3

; music_play: HL = dal
music_play:
        ld (mus_ptr),hl
        ld (mus_loop),hl
        ld a,1
        ld (mus_cnt),a
        ret

music_stop:
        ld hl,0
        ld (mus_ptr),hl
music_silence:
        xor a
        ld (mus_amp),a
        out ($06),a             ; 2 szinu mod, hangero 0
        ld a,$FF
        out ($04),a
        ld a,$0F                ; osztó $FFF: all az oszcillator
        out ($05),a
        ret

music_tick:
        ld hl,(mus_ptr)
        ld a,h
        or l
        ret z
        ld a,(mus_cnt)
        dec a
        ld (mus_cnt),a
        jr z,.next
        ld a,(mus_env)          ; lecsenges: 2 kepkockankent -1
        inc a
        ld (mus_env),a
        and 1
        ret nz
        ld a,(mus_amp)
        cp MUS_FLOOR+1
        ret c
        dec a
        ld (mus_amp),a
        jr .out
.next:  ld a,(hl)
        cp $FE
        jr z,music_stop
        cp $FF
        jr nz,.n
        ld hl,(mus_loop)
        ld a,(hl)
.n:     inc hl
        ld b,(hl)
        inc hl
        ld (mus_ptr),hl
        ld c,a
        ld a,b
        ld (mus_cnt),a
        xor a
        ld (mus_env),a
        ld a,c
        or a
        jr z,.rest
        add a,a
        ld l,a
        ld h,0
        ld de,NOTETAB-2
        add hl,de
        ld a,(hl)
        out ($04),a
        inc hl
        ld a,(hl)
        or $10                  ; a negyszogjel kapuzza a hangerot
        out ($05),a
        ld a,MUS_AMP0
        jr .set
.rest:  xor a
.set:   ld (mus_amp),a
.out:   ld a,(mus_amp)
        add a,a
        add a,a                 ; 2-5. bit; a 0-1. bit a videomod (0)
        out ($06),a
        ret

        include "zene.inc"
