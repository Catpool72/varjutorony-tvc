"""A lefordított J<n> rekordok (célok + szabály-bájtkód) ellenőrzése a binárisban."""
import sys
B = sys.argv[1] if len(sys.argv) > 1 else 'build'
syms = {}
for l in open(f'{B}/kaland.sym'):
    p = l.replace(':', ' ').split()
    if len(p) >= 3 and p[1] == 'EQU': syms[p[0]] = int(p[2], 16)
mem = bytearray(65536); bin_ = open(f'{B}/kaland.bin', 'rb').read(); mem[0x19EF:0x19EF + len(bin_)] = bin_
w = lambda a: mem[a] | mem[a + 1] << 8
L = {1: 2, 2: 1, 3: 0, 4: 1, 5: 1, 6: None, 7: None, 8: 1, 9: 0, 10: 0, 11: 4, 12: 2, 13: 2, 14: None, 15: 1,
     16: 0, 17: 1, 18: 2, 19: 1, 20: 0, 21: 2, 22: 2, 23: None, 24: None, 25: 4, 26: 0}
def cond(p):
    c = mem[p] & 0x7F
    return p + {67: 2, 68: 3}.get(c, 1)
bad = 0
for n in range(0, syms.get('INTRO2_SEC', 407) + 1):
    j = w(syms['JUMPTAB'] + 2 * n)
    if not j: continue
    p = j + 1 + 2 * mem[j]
    def walk(p, end=None):
        global bad
        while True:
            op = mem[p]; p += 1
            if op == 0: return p
            if op not in L: print('rossz művelet', n, hex(op), hex(p - 1)); bad += 1; return None
            if op == 6: p = cond(p + 2)
            elif op == 7: p = cond(p) + 1
            elif op == 14:
                cnt, fl = mem[p], mem[p + 1]; p += 2
                p += (fl >> 3 & 1) + 2 * (fl >> 4 & 1) + (fl >> 5 & 1) + 2 * (fl >> 6 & 1) + (fl >> 7 & 1)
                for _ in range(cnt):
                    p += 2
                    while mem[p]: p += 1
                    p += 1
            elif op == 23: p += 1 + 2 * mem[p]
            elif op == 24: p += 4 + mem[p + 3]
            else: p += L[op]
    walk(p)
print('hibás:', bad)
