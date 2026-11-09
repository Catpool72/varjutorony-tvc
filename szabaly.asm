;=============================================================================
; A SARKANY SZEME - jatekszabalyok: kalandlap, bajtkod-ertelmezo, harc,
; szerencse- es ugyessegproba, targyak, arany, kulcsok, bolt, varazsital.
; A bajtkodot a rules.py irja le es a build.py forditja (a J<n> rekordok vegen).
;=============================================================================

; muveletkodok (rules.py OP)
OP_END      equ 0
C_KEY       equ 64
C_RES       equ 65
C_X         equ 66
C_GOLD      equ 67
C_VIS       equ 68          ; + dw fejezet: mar jartunk ott
C_REV       equ 69          ; ebben a fejezetben mar jartunk
CH_SHEET    equ $FFFF           ; menu: kalandlap
CH_DRINK    equ $FFFE           ; menu: varazsital
FIGHT_ROW0  equ 7               ; a harci sorok elso sora
LB_SKILL    equ 8

;-----------------------------------------------------------------------------
; veletlenszam (xorshift16, J. Metcalf), A = H
;-----------------------------------------------------------------------------
rnd:    push hl
        ld hl,(rng)
        ld a,h
        rra
        ld a,l
        rra
        xor h
        ld h,a
        ld a,l
        rra
        ld a,h
        rra
        xor l
        ld l,a
        xor h
        ld h,a
        ld (rng),hl
        pop hl
        ret

d6:     call rnd
        and 7
        cp 6
        jr nc,d6
        inc a
        ret

; roll_n: B kocka osszege -> A (B >= 1)
roll_n: ld c,0
.l:     call d6
        add a,c
        ld c,a
        djnz .l
        ret

roll2:  ld b,2
        jr roll_n

;-----------------------------------------------------------------------------
; uj jatek: pontok dobasa, varazsital valasztasa, indulas az 1. fejezetrol
;-----------------------------------------------------------------------------
new_game:
        ld sp,STACK_TOP
        ld hl,MUS_TITLE
        call music_play
        ld hl,GAME_VARS
        ld de,GAME_VARS+1
        ld bc,GAME_LEN-1
        ld (hl),0
        ldir
        ld hl,START_ITEMS
.si:    ld a,(hl)
        inc hl
        cp $FF
        jr z,.sd
        push hl
        call item_addr
        ld a,(hl)
        or c
        ld (hl),a
        pop hl
        jr .si
.sd:    ld a,START_GOLD
        ld (g_gold),a
        call d6
        add a,6
        ld (g_sk),a
        ld (g_sk0),a
        call roll2
        add a,12
        ld (g_st),a
        ld (g_st0),a
        call d6
        add a,6
        ld (g_lk),a
        ld (g_lk0),a
        call clear_text
        call clear_prompt
        call draw_status
        ld a,1 : ld hl,MSG_SHEET : call print_at
        ld a,3 : ld hl,MSG_SK : call print_at
        ld a,(g_sk) : call print_a
        ld a,4 : ld hl,MSG_ST : call print_at
        ld a,(g_st) : call print_a
        ld a,5 : ld hl,MSG_LK : call print_at
        ld a,(g_lk) : call print_a
        ld a,8 : ld hl,MSG_POTSEL : call print_at
        ld hl,POTNAMES
        ld de,lm_ptr
        ld bc,6
        ldir
        ld a,3
        ld (lm_n),a
        ld hl,lm_val
        ld (hl),$FF
        inc hl
        ld (hl),$FF
        inc hl
        ld (hl),$FF
        ld a,10
        call listmenu
        ld (g_pot),a
        ld a,2
        ld (g_dose),a
        ld hl,START_SEC         ; 0: elobb az elozmenyek (ha vannak), kulonben az 1.
        jp show_section

;-----------------------------------------------------------------------------
; allapotsor (22. sor): U 10/12 E 20/24 Sz 11 Arany 15
;-----------------------------------------------------------------------------
draw_status:
        ld hl,(cur_col)         ; a kurzor (cur_col, cur_row) megmarad
        push hl
        call .d
        pop hl
        ld (cur_col),hl
        ret
.d:     ld a,TXT_ROWS
        ld c,1
        call clear_rows
        ld a,TXT_ROWS
        ld (cur_row),a
        xor a
        ld (cur_col),a
        ld hl,MSG_S_SK : call print_str
        ld a,(g_sk) : call print_a
        ld a,SLASH_IDX : call putc_cur
        ld a,(g_sk0) : call print_a
        ld hl,MSG_S_ST : call print_str
        ld a,(g_st) : call print_a
        ld a,SLASH_IDX : call putc_cur
        ld a,(g_st0) : call print_a
        ld hl,MSG_S_LK : call print_str
        ld a,(g_lk) : call print_a
        ld hl,MSG_S_GOLD : call print_str
        ld a,(g_gold)
        ; fall through
print_a:                        ; A = 0..255 kiirasa
        ld l,a
        ld h,0
        jp print_num

putc_cur:                       ; A = font-index kiirasa es leptetes
        call putc_nw
        ld hl,cur_col
        inc (hl)
        ret

; clear_rows: A = elso szovegsor, C = sorok szama (a szovegterulet szelessegeben)
clear_rows:
        push af
        ld a,MAP_DRAW
        call setmap
        pop af
        add a,a
        ld l,a
        ld h,0
        ld de,ROWTAB
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        dec hl                  ; a 30. bajtoszloptol
        ld a,c
        add a,a
        ld b,a
        add a,a
        add a,a
        add a,b                 ; *10 pontsor
        ld c,a
        ld de,64-34
.r:     ld b,34
        xor a
.b:     ld (hl),a
        inc hl
        djnz .b
        add hl,de
        dec c
        jr nz,.r
        ret

;-----------------------------------------------------------------------------
; uzenet a menusorban, varakozas Szokozre/Tuzre
; msg_wait: HL = szoveg;  msg_num: HL = szoveg, A = szam, DE = utana szoveg (0: nincs)
;-----------------------------------------------------------------------------
msg_wait:
        call clear_prompt
        call print_str
wait_fire:
.w:     call wait_key
        bit 5,a : jp nz,quit
        bit 4,a : jr z,.w
        ret

msg_num:
        push de
        push af
        call clear_prompt
        call print_str
        pop af
        call print_a
        pop hl
        ld a,h
        or l
        call nz,print_str
        jr wait_fire

; msg_item: HL = elotag, A = targy -> "Megszerezted: Kotel"
msg_item:
        push hl
        call item_name
        pop de
        ret z                   ; rejtett jelzo: nincs uzenet
        push hl
        ex de,hl
        call clear_prompt
        call print_str
        pop hl
        call print_str
        jr wait_fire

; item_name: A = targy -> HL = nev, Z = nincs neve
item_name:
        add a,a
        ld l,a
        ld h,0
        ld de,ITEMNAMES
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        or h
        ret

;-----------------------------------------------------------------------------
; targyak (bitkeszlet)
;-----------------------------------------------------------------------------
item_addr:                      ; A = targy -> HL = bajt, C = maszk
        push af
        rrca
        rrca
        rrca
        and $1F
        ld hl,items
        add a,l
        ld l,a
        adc a,h
        sub l
        ld h,a
        pop af
        and 7
        ld c,1
        ret z
.s:     sla c
        dec a
        jr nz,.s
        ret

has_item:                       ; A = targy -> NZ, ha megvan
        call item_addr
        ld a,(hl)
        and c
        ret

gain_item:                      ; A = targy
        push af
        call item_addr
        ld a,(hl)
        and c
        jr nz,.have
        ld a,(hl)
        or c
        ld (hl),a
        pop af
        ld hl,MSG_GAIN
        jp msg_item
.have:  pop af
        ret

lose_item:                      ; A = targy
        push af
        call item_addr
        ld a,(hl)
        and c
        jr z,.no
        ld a,c
        cpl
        and (hl)
        ld (hl),a
        pop af
        ld hl,MSG_LOSE
        jp msg_item
.no:    pop af
        ret

; lose_random: egy veletlen (nevvel biro, elveszithetu) targy elvesztese
lose_random:
        ld e,0                  ; E = jeloltek szama
        ld d,0
.c:     call .cand
        jr z,.cn
        inc e
.cn:    inc d
        ld a,d
        cp N_ITEMS
        jr c,.c
        ld a,e
        or a
        ret z
        call rnd
.m:     sub e
        jr nc,.m
        add a,e                 ; 0..E-1
        ld e,a
        ld d,0
.f:     call .cand
        jr z,.fn
        ld a,e
        or a
        jr z,.got
        dec e
.fn:    inc d
        jr .f
.got:   ld a,d
        jp lose_item
.cand:  push de                 ; D = targy -> NZ, ha jelolt
        ld a,d
        ld hl,ITEMLOSS
        add a,l
        ld l,a
        adc a,h
        sub l
        ld h,a
        ld a,(hl)
        or a
        jr z,.cx
        ld a,d
        call has_item
.cx:    pop de
        ret

;-----------------------------------------------------------------------------
; pontok
;-----------------------------------------------------------------------------
; add_stat: B = pont (0 U, 1 E, 2 Sz), C = elojeles valtozas; a Kezdeti ertek a felso korlat
add_stat:
        ld a,b
        add a,a
        ld hl,g_sk
        add a,l
        ld l,a
        jr nc,$+3
        inc h
        ld a,(hl)
        add a,c
        bit 7,c
        jr nz,.neg
        inc hl
        cp (hl)                 ; a Kezdeti ertek folott?
        dec hl
        jr c,.st
        ld a,(hl)
        inc hl
        ld a,(hl)
        dec hl
        jr .st
.neg:   or a
        jp p,.st
        xor a
.st:    ld (hl),a
        call draw_status
check_dead:
        ld a,(g_st)
        or a
        ret nz
        ; fall through
die:    ld sp,STACK_TOP
        ld hl,MUS_DEATH
        call music_play
        call draw_status
        ld hl,MSG_END
        call msg_wait
        jp new_game

damage:                         ; A = ELETERO-veszteseg
        neg
        ld c,a
        ld b,1
        jr add_stat

;-----------------------------------------------------------------------------
; valasztasok kezelese (choices[0..nch-1])
;-----------------------------------------------------------------------------
; find_choice: DE = cel -> HL = elem cime, Z = megvan
find_choice:
        ld hl,choices
        ld a,(nch)
        or a
        jr z,.nf
        ld b,a
.l:     ld a,(hl)
        cp e
        jr nz,.n
        inc hl
        ld a,(hl)
        dec hl
        cp d
        ret z
.n:     inc hl
        inc hl
        djnz .l
.nf:    or 1                    ; NZ
        ret

remove_choice:                  ; DE = cel
        call find_choice        ; B = az elemtol a vegeig hatralevo elemek
        ret nz
        dec b
        jr z,.d
        ld d,h
        ld e,l
        inc hl
        inc hl
        ld a,b
        add a,a
        ld c,a
        ld b,0
        ldir
.d:     ld hl,nch
        dec (hl)
        ret

add_choice:                     ; DE = cel
        call find_choice
        ret z
        ld a,(nch)
        cp MAX_CH
        ret nc
        inc a
        ld (nch),a
        dec a
        add a,a
        ld hl,choices
        add a,l
        ld l,a
        jr nc,$+3
        inc h
        ld (hl),e
        inc hl
        ld (hl),d
        ret

only_choice:                    ; DE = cel
        ld (choices),de
        ld a,1
        ld (nch),a
        ret

;-----------------------------------------------------------------------------
; bajtkod-ertelmezo. HL = a szkript; a muveletek HL-t a kovetkezo muveletre allitva ternek vissza
;-----------------------------------------------------------------------------
sget:   ld a,MAP_LOGIC          ; a szkript az U2-ben is lehet
        ld (P_SAVE),a
        out ($02),a
        ld a,(hl)
        inc hl
        ret

sget16: call sget
        ld e,a
        call sget
        ld d,a
        ret

run_script:
.l:     call sget
        or a
        ret z
        ld de,.l
        push de
        add a,a
        ld e,a
        ld d,0
        push hl
        ld hl,OPTAB-2
        add hl,de
        ld e,(hl)
        inc hl
        ld d,(hl)
        pop hl
        push de
        ret

OPTAB:  dw op_stat, op_gold, op_gold0, op_gain, op_lose, op_gate, op_if, op_skip
        dw op_luck, op_skill, op_pick, op_only, op_dmg, op_fight, op_loseitems, op_keys
        dw op_swarm, op_xset, op_xsub, op_dmgx, op_add, op_hide, op_shop, op_onchoose
        dw op_pickx, die

; ismetelt latogataskor a nyereseg kimarad
op_stat:
        call sget
        ld b,a
        call sget
        ld c,a
        bit 7,c
        jr nz,.do
        ld a,(revisit)
        or a
        ret nz
.do:    push hl
        call add_stat
        pop hl
        ret

op_gold:
        call sget
        ld c,a
        ld a,(g_gold)
        bit 7,c
        jr nz,.neg
        ld b,a
        ld a,(revisit)
        or a
        ret nz
        ld a,b
        add a,c
        jr nc,.st
        ld a,255
        jr .st
.neg:   add a,c
        jr c,.st
        xor a
.st:    ld (g_gold),a
        push hl
        call draw_status
        pop hl
        ret

op_gold0:
        xor a
        ld (g_gold),a
        push hl
        call draw_status
        pop hl
        ret

op_gain:
        call sget
        ld b,a
        ld a,(revisit)
        or a
        ret nz
        ld a,b
        push hl
        call gain_item
        pop hl
        ret

op_lose:
        call sget
        push hl
        call lose_item
        pop hl
        ret

; eval_cond: a feltetel beolvasasa -> A = 0/1
eval_cond:
        call sget
        ld b,a
        and $7F
        cp C_GOLD
        jr z,.gold
        cp C_X
        jr z,.x
        cp C_RES
        jr z,.res
        cp C_KEY
        jr z,.key
        cp C_VIS
        jr z,.vis
        cp C_REV
        jr z,.rev
        push hl
        push bc
        call has_item
        pop bc
        pop hl
        jr .bool
.gold:  call sget
        ld c,a
        ld a,(g_gold)
        cp c
        ccf
        sbc a,a
        jr .bool
.x:     ld a,(xv)
        jr .bool
.res:   ld a,(res)
        jr .bool
.rev:   ld a,(revisit)
        jr .bool
.vis:   call sget16
        push hl
        ld a,e
        and 7
        ld c,a
        srl d
        rr e
        srl d
        rr e
        srl d
        rr e
        ld hl,visited
        add hl,de
        ld a,(hl)
        inc c
.vs:    dec c
        jr z,.vd
        rrca
        jr .vs
.vd:    and 1
        pop hl
        jr .bool
.key:   ld a,(items+KEYBYTE)
        and KEYMASK
.bool:  or a
        jr z,.f
        ld a,1
.f:     bit 7,b
        ret z
        xor 1
        ret

op_gate:
        call sget16
        push de
        call eval_cond
        pop de
        or a
        ret nz
        push hl
        call remove_choice
        pop hl
        ret

op_if:  call eval_cond
        ld c,a
        call sget               ; az "akkor" ag hossza
        dec c
        ret z                   ; igaz: folytatas
        ld e,a
        ld d,0
        add hl,de
        ret

op_skip:
        call sget
        ld e,a
        ld d,0
        add hl,de
        ret

op_only:
        call sget16
        jp only_choice

op_add: call sget16
        push hl
        call add_choice
        pop hl
        ret

op_hide:
        call sget16
        push hl
        call remove_choice
        pop hl
        ret

op_pick:
        ld a,(res)
pick_a: push af
        call sget16
        push de
        call sget16
        pop bc                  ; BC = a, DE = b
        pop af
        or a
        jr z,.b
        ld d,b
        ld e,c
.b:     jp only_choice

op_pickx:
        ld a,(xv)
        jr pick_a

; proba: B = cel, (2d6 <= B) -> res; uzenet
test_msg:                       ; HL = felirat, B = ertek; -> A = res
        push hl
        push bc
        call roll2
        pop bc
        pop hl
        ld c,a
        cp b
        ld a,0
        jr z,.ok
        jr nc,.no
.ok:    inc a
.no:    ld (res),a
        ld de,MSG_OK
        or a
        jr nz,.m
        ld de,MSG_FAIL
.m:     ld a,c
        jp msg_num

op_luck:
        push hl
        call luck_test
        pop hl
        ret

luck_test:                      ; -> res, SZERENCSE - 1
        ld a,(g_lk)
        ld b,a
        ld hl,MSG_LUCK
        call test_msg
        ld hl,g_lk
        ld a,(hl)
        or a
        jr z,.z
        dec (hl)
.z:     jp draw_status

op_skill:
        push hl
        ld a,(g_sk)
        ld b,a
        ld hl,MSG_SKILL
        call test_msg
        pop hl
        ret

op_dmg: call sget
        ld b,a
        call sget
        push hl
        push af
        call roll_n
        pop bc
        add a,b
dmg_msg:                        ; A = veszteseg (uzenettel)
        push af
        ld hl,MSG_DICE
        ld de,MSG_DMG
        call msg_num
        pop af
        call damage
        pop hl
        ret

op_dmgx:
        push hl
        ld a,(xv)
        or a
        jr nz,dmg_msg
        pop hl
        ret

op_xset:
        call sget
        ld b,a
        call sget
        push hl
        push af
        call roll_n
        pop bc
        add a,b
        ld (xv),a
        ld hl,MSG_LARVA
        ld de,0
        call msg_num
        pop hl
        ret

op_xsub:
        call sget
        ld b,a
        push hl
        call roll_n
        ld b,a
        ld a,(xv)
        sub b
        jr nc,$+3
        xor a
        ld (xv),a
        ld a,b
        call kill_msg
        pop hl
        ret

; kill_msg: A = megolt, (xv) = maradt -> "Megoltel 9, maradt 4"
kill_msg:
        ld hl,MSG_KILL
        call clear_prompt_str
        call print_a
        ld hl,MSG_LEFT
        call print_str
        ld a,(xv)
        call print_a
        jp wait_fire

clear_prompt_str:
        push af
        push hl
        call clear_prompt
        pop hl
        call print_str
        pop af
        ret

op_loseitems:
        call sget
        push hl
        or a
        jr nz,.n
        call d6
.n:     ld b,a
.l:     push bc
        call lose_random
        pop bc
        djnz .l
        pop hl
        ret

op_keys:
        push hl
        ld hl,KEYTAB
.l:     ld a,(hl)
        cp $FF
        jr z,.e
        inc hl
        ld e,(hl)
        inc hl
        ld d,(hl)
        inc hl
        push hl
        push de
        call has_item
        pop de
        call nz,add_choice
        pop hl
        jr .l
.e:     pop hl
        ret

op_onchoose:
        call sget16
        ld (oc_t),de
        call sget               ; felirat: 0 Harc, 1 Proba
        ld (oc_lbl),a
        call sget
        ld (oc_ptr),hl
        ld e,a
        ld d,0
        add hl,de
        ret

; Pestispatkanyok: korokent 1 ELETERO, amig elnek; megolsz 1d6 + UGYESSEG-et
op_swarm:
        call sget
        ld (xv),a
        push hl
.r:     ld a,(xv)
        or a
        jr z,.e
        ld a,1
        call damage
        call d6
        ld b,a
        ld a,(g_sk)
        add a,b
        ld b,a
        ld a,(xv)
        sub b
        jr nc,$+3
        xor a
        ld (xv),a
        ld a,b
        call kill_msg
        jr .r
.e:     pop hl
        ret

;-----------------------------------------------------------------------------
; bolt: SHOP n, (targy, ar) * n
;-----------------------------------------------------------------------------
op_shop:
        call sget
        ld (lm_n),a
        ld b,a
        ld de,shop_items
.c:     call sget
        ld (de),a
        inc de
        call sget
        ld (de),a
        inc de
        djnz .c
        ld (sptr),hl
.redraw:
        ld a,(lm_n)
        ld b,a
        ld hl,shop_items
        ld de,lm_ptr
        ld ix,lm_val
.f:     ld a,(hl)
        inc hl
        push hl
        push de
        call item_name
        pop de
        ex de,hl
        ld (hl),e
        inc hl
        ld (hl),d
        inc hl
        ex de,hl
        pop hl
        ld a,(hl)
        inc hl
        ld (ix+0),a
        inc ix
        djnz .f
        ex de,hl
        ld de,MSG_DONE
        ld (hl),e
        inc hl
        ld (hl),d
        ld (ix+0),$FF
        call clear_text
        xor a
        ld hl,MSG_SHOP
        call print_at
        ld a,(g_gold)
        call print_a
        ld hl,lm_n
        inc (hl)
        ld a,2
        call listmenu
        ld hl,lm_n
        dec (hl)
        cp (hl)
        jr z,.done
        add a,a
        ld l,a
        ld h,0
        ld de,shop_items
        add hl,de
        ld a,(hl)               ; targy
        inc hl
        ld b,(hl)               ; ar
        push af
        call has_item
        jr z,.nh
        pop af
        ld hl,MSG_HAVE
        call msg_wait
        jp .redraw
.nh:    ld a,(g_gold)
        cp b
        jr nc,.buy
        pop af
        ld hl,MSG_NOGOLD
        call msg_wait
        jp .redraw
.buy:   sub b
        ld (g_gold),a
        call draw_status
        pop af
        call gain_item
        jp .redraw
.done:  call print_section_text
        ld hl,(sptr)
        ret

;-----------------------------------------------------------------------------
; listmenu: lm_n tetel (lm_ptr szovegek, lm_val szam vagy $FF) az A. sortol;
; fel/le, Szokoz/Tuz valaszt -> A = sorszam
;-----------------------------------------------------------------------------
listmenu:
        ld (lm_row),a
        xor a
        ld (lm_sel),a
.draw:  ld a,(lm_n)
        ld b,a
        ld c,0
.e:     push bc
        ld a,(lm_row)
        add a,c
        ld (cur_row),a
        xor a
        ld (cur_col),a
        ld a,(lm_sel)
        cp c
        ld a,0
        jr nz,.ni
        dec a
.ni:    ld (inv),a
        ld a,SP_IDX : call putc_cur
        ld a,c
        add a,a
        ld l,a
        ld h,0
        ld de,lm_ptr
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        call print_str
        pop bc
        push bc
        ld hl,lm_val
        ld a,c
        add a,l
        ld l,a
        jr nc,$+3
        inc h
        ld a,(hl)
        cp $FF
        jr z,.nv
        push af
        ld a,SP_IDX : call putc_cur
        ld a,LPAR_IDX : call putc_cur
        pop af
        call print_a
        ld a,RPAR_IDX : call putc_cur
.nv:    ld a,SP_IDX : call putc_cur
        xor a
        ld (inv),a
        ld a,SP_IDX : call putc_cur      ; az inverz csik vegenek torlese
        ld a,SP_IDX : call putc_cur
        pop bc
        inc c
        djnz .e
        call clear_prompt
        ld hl,MSG_LMHELP
        call print_str
.w:     call wait_key
        bit 5,a : jp nz,quit
        bit 4,a : jr nz,.go
        ld b,a
        and K_LEFT              ; bal: az elso tetel
        jr z,.nl
        xor a
        jr .set
.nl:    ld a,b
        and K_RIGHT             ; jobb: az utolso (a boltban: Kesz)
        jr z,.nr
        ld a,(lm_n)
        dec a
.set:   ld (lm_sel),a
        jp .draw
.nr:    ld a,b
        and K_UP
        jr z,.dn
        ld a,(lm_sel)
        or a
        jr z,.w
        dec a
        ld (lm_sel),a
        jp .draw
.dn:    ld a,(knew)
        and K_DOWN
        jr z,.w
        ld a,(lm_n)
        ld b,a
        ld a,(lm_sel)
        inc a
        cp b
        jr nc,.w
        ld (lm_sel),a
        jp .draw
.go:    ld a,(lm_sel)
        ret

;-----------------------------------------------------------------------------
; kalandlap (menu: "Lap") es varazsital (menu: "Ital")
;-----------------------------------------------------------------------------
show_sheet:
        call clear_text
        xor a : ld hl,MSG_SHEET : call print_at
        ld a,2 : ld hl,MSG_SK : call print_at
        ld a,(g_sk) : ld b,a : ld a,(g_sk0) : call print_pair
        ld a,3 : ld hl,MSG_ST : call print_at
        ld a,(g_st) : ld b,a : ld a,(g_st0) : call print_pair
        ld a,4 : ld hl,MSG_LK : call print_at
        ld a,(g_lk) : ld b,a : ld a,(g_lk0) : call print_pair
        ld a,5 : ld hl,MSG_GOLD : call print_at
        ld a,(g_gold) : call print_a
        ld a,6 : ld hl,MSG_POT : call print_at
        ld a,(g_pot)
        add a,a
        ld l,a
        ld h,0
        ld de,POTNAMES
        add hl,de
        ld a,(hl)
        inc hl
        ld h,(hl)
        ld l,a
        call print_str
        ld a,SP_IDX : call putc_cur
        ld a,(g_dose) : call print_a
        ld hl,MSG_DOSE : call print_str
        ld a,8 : ld hl,MSG_ITEMS : call print_at
        ld a,9
        ld (cur_row),a
        ld d,0                  ; D = targy, E = oszlop (0 / 17)
        ld e,0
.l:     ld a,d
        push de
        call has_item
        pop de
        jr z,.n
        ld a,d
        push de
        call item_name
        pop de
        jr z,.n
        ld a,e
        ld (cur_col),a
        ld b,16
        call print_strn
        ld a,e
        xor 17
        ld e,a
        jr nz,.n
        ld hl,cur_row
        inc (hl)
        ld a,(hl)
        cp TXT_ROWS-1
        jr nc,.x
.n:     inc d
        ld a,d
        cp N_ITEMS
        jr c,.l
.x:     ld a,TXT_ROWS-1
        ld hl,MSG_COLHINT       ; Bal/Jobb: hatter- es tintaszin
        call print_at
    IFDEF DISK
        ld hl,MSG_SHEETKEYS     ; Szokoz: vissza, Fel: mentes, Le: visszatoltes
        call clear_prompt_str
.k:     call wait_key
        bit 5,a : jp nz,quit
        bit 4,a : jr nz,.back
        call color_keys
        ld b,a
        and K_UP
        jr nz,.save
        ld a,b
        and K_DOWN
        jr z,.k
        call disk_restore
        or a
        jp z,resume_game
        ld hl,MSG_NOSAVE
        call msg_wait
        jr .back
.save:  call disk_save
        or a
        ld hl,MSG_SAVED
        jr z,.sm
        ld hl,MSG_SAVEERR
        ld de,0
        call msg_num
        jr .back
.sm:    call msg_wait
.back:
    ELSE
        ld hl,MSG_BACK
        call clear_prompt_str
.k:     call wait_key
        bit 5,a : jp nz,quit
        bit 4,a : jr nz,.back
        call color_keys
        jr .k
.back:
    ENDIF
        call print_section_text
        jp choose_again

;-----------------------------------------------------------------------------
; SZINEK: a hatter ($60) es a tinta ($61) a TVC 16 szinebol (Bal: hatter, Jobb: tinta).
; A szinindex bitjei: 0 kek, 1 voros, 2 zold, 3 fenyes -> a port 0I0G0R0B formatuma.
; Ugyanaz a szin nem lehet hatter es tinta is (atugorja).
;-----------------------------------------------------------------------------
pal_paper:  db 0                ; fekete
pal_ink:    db 12               ; vilagoszold

; color_keys: A = lenyomott billentyuk; A-t es B-t megtartja
color_keys:
        push af
        push bc
        ld b,a
        ld hl,pal_paper
        and K_LEFT
        jr nz,.st
        ld a,b
        ld hl,pal_ink
        and K_RIGHT
        jr z,.x
.st:    ld a,(hl)
        inc a
        and 15
        ld (hl),a
        ld a,(pal_paper)
        ld c,a
        ld a,(pal_ink)
        cp c
        jr z,.st
        call apply_pal
.x:     pop bc
        pop af
        ret

apply_pal:
        ld a,(pal_paper)
        call pal_val
        out ($60),a
        ld a,(pal_ink)
        call pal_val
        out ($61),a
        ret

pal_val:                        ; A = 0..15 -> 0I0G0R0B
        ld c,0
        rrca
        rl c                    ; C: ...B  (fordítva gyűjtjük, majd szétrakjuk)
        rrca
        rl c
        rrca
        rl c
        rrca
        rl c                    ; C = B R G I (3..0)
        xor a
        rr c : rla              ; I
        add a,a
        rr c : rla              ; G
        add a,a
        rr c : rla              ; R
        add a,a
        rr c : rla              ; B
        ret

print_pair:                     ; B / A
        push af
        ld a,b
        call print_a
        ld a,SLASH_IDX : call putc_cur
        pop af
        jp print_a

print_strn:                     ; HL = szoveg, legfeljebb B karakter
        ld a,(hl)
        or a
        ret z
        push hl
        call putc_cur
        pop hl
        inc hl
        djnz print_strn
        ret

drink:
        ld hl,g_dose
        dec (hl)
        ld a,(g_pot)
        or a
        jr nz,.n1
        ld a,(g_sk0)
        ld (g_sk),a
        jr .d
.n1:    dec a
        jr nz,.n2
        ld a,(g_st0)
        ld (g_st),a
        jr .d
.n2:    ld hl,g_lk0
        inc (hl)
        ld a,(hl)
        ld (g_lk),a
.d:     call draw_status
        ld hl,MSG_DRANK
        call msg_wait
        jp choose_again

;-----------------------------------------------------------------------------
; HARC
; FIGHT n, flags, [hitlim], [pdmg, mdmg], [skmod], [ev, evp], [ext], n * (UGY, ELE, nev 0)
; flags: 1 egyszerre mind, 2 Littlebig is ut, 4 a szorny ketszer tamad, 8 talalathatar,
;        16 sebzesek, 32 UGY-modosito, 64 esemeny, 128 kiegeszito
; esemeny: 1 elvesztett kor, 2 elso kor, 3 n megnyert kor, 4 n kor tulelese, 5 megnyert kor,
;          6 menekules n kor utan (szerencsevel); kiegeszito: 1 gazfelho, 2 vérszivas, 3 kris kes
; res = 1, ha a kulonleges kimenetel kovetkezett be
;-----------------------------------------------------------------------------
op_fight:
        call sget
        ld (f_n),a
        call sget
        ld (f_flags),a
        ld c,a
        ld a,2
        ld (f_pdmg),a
        ld (f_mdmg),a
        xor a
        ld (f_hitlim),a
        ld (f_skmod),a
        ld (f_ev),a
        ld (f_evp),a
        ld (f_ext),a
        ld (f_round),a
        ld (f_hits),a
        ld (f_wins),a
        ld (res),a
        bit 3,c : jr z,.a1
        call sget : ld (f_hitlim),a
.a1:    bit 4,c : jr z,.a2
        call sget : ld (f_pdmg),a
        call sget : ld (f_mdmg),a
.a2:    bit 5,c : jr z,.a3
        call sget : ld (f_skmod),a
.a3:    bit 6,c : jr z,.a4
        call sget : ld (f_ev),a
        call sget : ld (f_evp),a
.a4:    bit 7,c : jr z,.a5
        call sget : ld (f_ext),a
.a5:    ld a,(f_n)
        ld b,a
        ld ix,f_msk
        ld de,f_names
.m:     call sget
        ld (ix+0),a
        call sget
        ld (ix+4),a
        inc ix
        push bc
        ld b,NAME_LEN-1
.nm:    call sget
        ld (de),a
        or a
        jr z,.nz
        inc de
        djnz .nm
        xor a
        ld (de),a
.sk:    call sget               ; a tul hosszu nev maradeka
        or a
        jr nz,.sk
.nz:    ld a,e                  ; DE a kovetkezo nev elejere
        and $E0
        add a,NAME_LEN
        ld e,a
        jr nc,$+3
        inc d
        pop bc
        djnz .m
        ld (sptr),hl
        ld hl,MUS_FIGHT
        call music_play
        ld hl,MSG_TOFIGHT       ; elobb a fejezet szoveget el kell tudni olvasni
        call msg_wait
        ; kepernyo
        call clear_text
        xor a : ld hl,MSG_HARC : call print_at
        call fight_mons
        ld a,(f_flags)
        and 2
        jr z,.nlb
        ld a,(f_n)
        inc a
        ld hl,MSG_LB
        call print_at
.nlb:   ld a,FIGHT_ROW0
        ld (f_line),a

.round: ; elso elo ellenfel
        ld hl,f_mst
        ld a,(f_n)
        ld b,a
        ld c,0
.ft:    ld a,(hl)
        or a
        jr nz,.tg
        inc hl
        inc c
        djnz .ft
        jp .won
.tg:    ld a,c
        ld (f_tgt),a
        ld hl,f_round
        inc (hl)
        xor a
        ld (f_rwon),a
        ld (f_rlost),a
        ; menekules (Vampir: hat kor utan, szerencsevel)
        ld a,(f_ev)
        cp 6
        jr nz,.nofl
        ld a,(f_evp)
        ld b,a
        ld a,(f_round)
        dec a
        cp b
        jr c,.nofl
        ld hl,MSG_FLEEQ
        call clear_prompt_str
.fw:    call wait_key
        bit 5,a : jp nz,quit
        bit 4,a : jr nz,.att
        and K_UP
        jr z,.fw
        call luck_test
        ld a,(res)
        or a
        jp nz,.special
        xor a
        ld (f_ev),a             ; nem sikerult: halalig
        ld hl,MSG_NOFLEE
        call msg_wait
        jr .att
.nofl:  ld hl,MSG_ATTACK
        call msg_wait
.att:   call fight_newline
        ld a,(f_round)
        call print_a
        ld hl,MSG_ROUND
        call print_str
        call exch               ; sajat tamadas
        jr c,.mw
        jr z,.dr
        ; te nyerted: sebzes
        ld a,1
        ld (f_rwon),a
        ld hl,f_wins
        inc (hl)
        call hit_mon
        ld a,(f_ext)
        cp 3                    ; kris kes: -2 UGYESSEG is
        jr nz,.nk
        call tgt_msk
        ld a,(hl)
        sub 2
        jr nc,$+3
        xor a
        ld (hl),a
.nk:    ld hl,MSG_HIT
        jr .pr
.mw:    call hit_me
        ld hl,MSG_HURT
        jr .pr
.dr:    ld hl,MSG_DRAW
.pr:    call print_str
        ; Littlebig
        ld a,(f_flags)
        and 2
        jr z,.nlb2
        call tgt_mst
        ld a,(hl)
        or a
        jr z,.nlb2
        call fight_newline
        ld hl,MSG_LBN
        call print_str
        ld a,LB_SKILL
        call exch_sk
        ld hl,MSG_MISS
        jr c,.lp
        jr z,.lp
        call hit_mon
        ld hl,MSG_LBHIT
.lp:    call print_str
.nlb2:  ; a szorny ketszer tamad
        ld a,(f_flags)
        and 4
        jr z,.nmd
        call fight_newline
        ld hl,MSG_SECOND
        call print_str
        call exch
        ld hl,MSG_PARRY
        jr nc,.mp
        call hit_me
        ld hl,MSG_HURT
.mp:    call print_str
.nmd:   ; egyszerre mind: a tobbiek is tamadnak
        ld a,(f_flags)
        and 1
        jr z,.nall
        ld a,(f_tgt)
        push af
        ld a,(f_n)
        ld b,a
        ld c,0
.ol:    push bc
        ld a,(f_tgt)
        cp c
        jr z,.on
        ld a,c
        ld (f_tgt),a
        call tgt_mst
        ld a,(hl)
        or a
        jr z,.on
        call fight_newline
        ld hl,MSG_OTHER
        call print_str
        call exch
        ld hl,MSG_PARRY
        jr nc,.op
        call hit_me
        ld hl,MSG_HURT
.op:    call print_str
.on:    pop bc
        pop af
        push af
        ld (f_tgt),a
        inc c
        djnz .ol
        pop af
.nall:  ; kiegeszitok
        ld a,(f_ext)
        cp 1
        jr nz,.ng
        ld a,(f_round)
        dec a
        jr nz,.ng
        call fight_status
        call luck_test          ; gazfelho az elso korben
        ld a,(res)
        or a
        jr nz,.ng
        call fight_newline
        ld hl,MSG_GAS
        call print_str
        ld a,4
        call damage
.ng:    ld a,(f_ext)
        cp 2
        jr nz,.nd
        ld a,(f_mst)
        or a
        jr z,.nd
        call fight_newline
        ld hl,MSG_DRAIN
        call print_str
        ld a,1
        call damage
.nd:    call fight_status
        ; esemenyek
        ld a,(f_hitlim)
        or a
        jr z,.e0
        ld b,a
        ld a,(f_hits)
        cp b
        jr nc,.special
.e0:    ld a,(f_ev)
        dec a
        jr nz,.e2
        ld a,(f_rlost)          ; 1: elvesztett kor
        or a
        jr nz,.special
        jp .round
.e2:    dec a
        jr nz,.e3
        ld a,(f_rwon)           ; 2: az elso kor dont
        ld (res),a
        jr .fend
.e3:    dec a
        jr nz,.e4
        ld a,(f_evp)            ; 3: n megnyert kor
        ld b,a
        ld a,(f_wins)
        cp b
        jr nc,.special
        jp .round
.e4:    dec a
        jr nz,.e5
        ld a,(f_evp)            ; 4: n kor tulelese
        ld b,a
        ld a,(f_round)
        cp b
        jr nc,.special
        jp .round
.e5:    dec a
        jp nz,.round
        ld a,(f_rwon)           ; 5: megnyert kor
        or a
        jr nz,.special
        jp .round
.special:
        ld a,1
        ld (res),a
.fend:  ld hl,MSG_FEND
        jr .fx
.won:   ld hl,MUS_WON
        call music_play
        ld hl,MSG_WON
.fx:    call msg_wait
        call music_stop
        ld hl,(sptr)
        ret

; fight_newline: kovetkezo harci sor (ha betelt: torles)
fight_newline:
        ld a,(f_line)
        cp TXT_ROWS
        jr c,.ok
        ld a,FIGHT_ROW0
        ld c,TXT_ROWS-FIGHT_ROW0
        call clear_rows
        ld a,FIGHT_ROW0
.ok:    ld (cur_row),a
        inc a
        ld (f_line),a
        xor a
        ld (cur_col),a
        ret

; fight_mons: az ellenfelek sorai (1..n): nev, U, E
fight_mons:
        ld a,(f_n)
        ld b,a
        ld c,0
.l:     push bc
        ld a,c
        inc a
        ld c,1
        push af
        call clear_rows
        pop af
        ld (cur_row),a
        xor a
        ld (cur_col),a
        pop bc
        push bc
        ld a,c
        rrca
        rrca
        rrca                    ; *32 = NAME_LEN
        ld l,a
        ld h,0
        ld de,f_names
        add hl,de
        call print_str
        ld a,23
        ld (cur_col),a
        ld hl,MSG_S_SK
        call print_str
        pop bc
        push bc
        ld hl,f_msk
        ld a,c
        add a,l
        ld l,a
        jr nc,$+3
        inc h
        ld a,(hl)
        call print_a
        ld hl,MSG_S_ST
        call print_str
        pop bc
        push bc
        ld hl,f_mst
        ld a,c
        add a,l
        ld l,a
        jr nc,$+3
        inc h
        ld a,(hl)
        call print_a
        pop bc
        inc c
        djnz .l
        ret

fight_status:
        call fight_mons
        jp draw_status

; exch: sajat tamadoero (2d6+UGY+mod) a cel ellen (2d6+UGY) -> print "17:14 ";
; C: a szorny nyert, Z: dontetlen, NC NZ: te nyertel
exch:   ld a,(g_sk)
        ld b,a
        ld a,(f_skmod)
        add a,b
exch_sk:                        ; A = a tamado UGYESSEGE
        push af
        call roll2
        pop bc
        add a,b
        ld (f_pas),a
        call tgt_msk
        ld a,(hl)
        push af
        call roll2
        pop bc
        add a,b
        ld (f_mas),a
        ld a,(f_pas)
        call print_a
        ld a,COLON_IDX : call putc_cur
        ld a,(f_mas)
        call print_a
        ld a,SP_IDX : call putc_cur
        ld a,(f_mas)
        ld b,a
        ld a,(f_pas)
        cp b
        ret                     ; C: pas < mas, Z: egyenlo

tgt_msk:
        ld hl,f_msk
        jr tgt_x
tgt_mst:
        ld hl,f_mst
tgt_x:  ld a,(f_tgt)
        add a,l
        ld l,a
        ret nc
        inc h
        ret

hit_mon:
        call tgt_mst
        ld a,(f_pdmg)
        ld b,a
        ld a,(hl)
        sub b
        jr nc,$+3
        xor a
        ld (hl),a
        ret

hit_me: ld a,1
        ld (f_rlost),a
        ld hl,f_hits
        inc (hl)
        ld a,(f_mdmg)
        jp damage
