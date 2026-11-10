#!/usr/bin/env python3
"""
Kép cseréje: egy tetszőleges (pl. másik MI által rajzolt) képből elkészíti a könyv N. képét.

  python3 kepcsere.py N uj_kep.png [--neg] [--teljes] [--lagyit 2] [--gamma 1.0]

- A képet álló 5:8 arányra vágja (középről), és az ill/pN.png-be menti.
- Elkészíti az előnézetet is (elonezet/pN.png): így fog kinézni a TVC 2 színű képernyőjén
  (fehér lapon fekete tintával; a kép világos részei maradnak fehérek).
- --neg: a kép megfordítása. Akkor kell, ha a kép világos rajz sötét alapon, vagy éjszakai
  jelenet, aminek a világos részeit (hold, tűz, fények) szeretnéd zölden látni.
- --teljes: nem vág, a teljes kép látszik (ha nem 5:8 arányú, fölül-alul fekete sáv marad).
- --lagyit R: elmosás R képpont sugárral a kicsinyítés előtt. Pontozott/raszteres (pl. már zöld-fekete)
  képnél kell, hogy a pontokból tónus legyen, és ne keletkezzen moaré.
- --gamma: a tónusok (1-nél nagyobb: sötétebb, kisebb: világosabb eredmény).
Utána: python3 ../build.py --book varjutorony --disk
"""
import argparse, os, sys
import numpy as np
from PIL import Image, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tvc_gfx')); sys.path.insert(0, os.path.join(HERE, '..'))
from tvcgfx import to_tvc, PIX_ASPECT

ap = argparse.ArgumentParser()
ap.add_argument('n', type=int); ap.add_argument('kep')
ap.add_argument('--neg', action='store_true'); ap.add_argument('--teljes', action='store_true')
ap.add_argument('--lagyit', type=float, default=0); ap.add_argument('--gamma', type=float, default=1.0)
a = ap.parse_args()
from PIL import ImageFilter
src = Image.open(a.kep).convert('RGB')
# szürkeárnyalat: a zöld-fekete (TVC-stílusú) képeknél a legerősebb csatorna adja a fényességet
arr = np.asarray(src).astype(np.float64)
im = Image.fromarray((0.5 * arr.max(axis=2) + 0.5 * (arr @ [0.299, 0.587, 0.114])).clip(0, 255).astype('uint8'), 'L')
w, h = im.size
if a.lagyit: im = im.filter(ImageFilter.GaussianBlur(a.lagyit))
if a.teljes:
    pass
elif w / h > 5 / 8:
    nw = int(h * 5 / 8); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
else:
    nh = int(w * 8 / 5); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
im = im.resize((600, round(600 * im.height / im.width)), Image.LANCZOS)
if a.neg: im = ImageOps.invert(im)
if a.gamma != 1.0: im = im.point(lambda v: int(255 * (v / 255) ** a.gamma))
os.makedirs(os.path.join(HERE, 'ill'), exist_ok=True)
im.save(os.path.join(HERE, 'ill', f'p{a.n}.png'))
# ugyanúgy, mint a build.py make_img-je
r = im.width / im.height; hh = 240
if round(hh * r / PIX_ASPECT) > 240: hh = int(240 * PIX_ASPECT / r)
bw = to_tvc(im, hh, 'fs')
fr = np.zeros((240, 240), bool); y0 = (240 - bw.shape[0]) // 2; x0 = (240 - bw.shape[1]) // 2
fr[y0:y0 + bw.shape[0], x0:x0 + bw.shape[1]] = bw
pv = Image.fromarray(np.stack([np.where(fr, 0, 255)] * 3, -1).astype('uint8'))   # fekete tinta fehér lapon
os.makedirs(os.path.join(HERE, 'elonezet'), exist_ok=True)
pv.resize((300, 480), Image.NEAREST).save(os.path.join(HERE, 'elonezet', f'p{a.n}.png'))
print(f'ill/p{a.n}.png kész; előnézet: elonezet/p{a.n}.png')
