#!/usr/bin/env python3
"""
Könyvillusztráció -> TVC GRAPHICS 2 (512x240, 2 szín) átalakító + előnézet.

A TVC pixele GRAPHICS 2-ben keskeny és magas (4:3 képernyőn 512x240 pont,
egy pont ~0,625 : 1 arányú). Hogy a rajz ne torzuljon, a képet vízszintesen
1/0,625 = 1,6-szoros pontszámra kell nyújtani: egy H=240 sor magas kép
szélessége  384 * (szélesség/magasság)  pont lesz.

Kimenet képenként:
  <név>.g2      nyers TVC videóadat: 240 sor, soronként ceil(w/8) bájt,
                bájtonként 8 pont, bit7 = bal szélső, 1 = előtér (paletta 1)
  <név>.png     a TVC-pontok 1:1-ben (w x 240)
Előnézet: a TVC képernyő 4:3-as arányban (1024x768), ahogy a monitoron látszana.

Használat: python3 tvcgfx.py kep.png [--dither fs|bayer|threshold] [--height 240]
"""
import argparse, numpy as np
from PIL import Image, ImageOps

PIX_ASPECT = 0.625          # TVC GRAPHICS 2 pont szélesség/magasság
BAYER8 = np.array([[0,32,8,40,2,34,10,42],[48,16,56,24,50,18,58,26],[12,44,4,36,14,46,6,38],
                   [60,28,52,20,62,30,54,22],[3,35,11,43,1,33,9,41],[51,19,59,27,49,17,57,25],
                   [15,47,7,39,13,45,5,37],[63,31,55,23,61,29,53,21]]) / 64.0

def to_tvc(img, height=240, dither='fs', gamma=1.0):
    g = ImageOps.autocontrast(img.convert('L'), cutoff=1)
    w = round(height * g.width / g.height / PIX_ASPECT)
    g = g.resize((w, height), Image.LANCZOS)
    a = (np.asarray(g, dtype=np.float64) / 255.0) ** gamma
    if dither == 'threshold':
        bw = a < 0.5
    elif dither == 'bayer':
        t = np.tile(BAYER8, (height // 8 + 1, w // 8 + 1))[:height, :w]
        bw = a < (t + 1 / 128)
    else:                                       # Floyd–Steinberg
        a = a.copy(); bw = np.zeros(a.shape, bool)
        for y in range(height):
            for x in range(w):
                old = a[y, x]; new = 0.0 if old < 0.5 else 1.0
                bw[y, x] = new == 0.0; err = old - new
                if x + 1 < w: a[y, x + 1] += err * 7 / 16
                if y + 1 < height:
                    if x > 0: a[y + 1, x - 1] += err * 3 / 16
                    a[y + 1, x] += err * 5 / 16
                    if x + 1 < w: a[y + 1, x + 1] += err * 1 / 16
    return bw                                   # True = fekete (előtér)

def pack(bw):
    h, w = bw.shape
    wb = (w + 7) // 8
    pad = np.zeros((h, wb * 8), bool); pad[:, :w] = bw
    return np.packbits(pad, axis=1).tobytes(), wb

def screen_preview(frame512):
    """512x240 bool keret -> 1024x768 kép, ahogy a 4:3 képernyőn látszik"""
    im = Image.fromarray(np.where(frame512, 20, 235).astype(np.uint8))
    return im.resize((1024, 768), Image.NEAREST)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('--dither', default='fs')
    ap.add_argument('--height', type=int, default=240); ap.add_argument('--out', default='.')
    a = ap.parse_args()
    import os
    bw = to_tvc(Image.open(a.src), a.height, a.dither)
    data, wb = pack(bw)
    base = os.path.join(a.out, os.path.splitext(os.path.basename(a.src))[0])
    open(base + '.g2', 'wb').write(data)
    Image.fromarray(np.where(bw, 0, 255).astype(np.uint8)).save(base + '.png')
    print(f'{bw.shape[1]}x{bw.shape[0]} pont, {wb} bájt/sor, {len(data)} bájt')
