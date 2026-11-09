"""Egyszerű rajzkészlet a Varjútorony képeihez (saját, programmal rajzolt jelenetek).

A vászon 300x480 (5:8, a TVC 2 színű módjának álló képkockája), 'L' mód, világos = megvilágított.
Mentéskor a kép megfordul (ImageOps.invert): a motor a sötét pontokat festi tintával (zöld),
így a megvilágított részek lesznek zöldek a fekete képernyőn.
"""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageOps

W, H = 300, 480

class _Draw:
    """ImageDraw, ami a fordított sarkú dobozokat is elfogadja"""
    def __init__(self, im): self._d = ImageDraw.Draw(im)
    def __getattr__(self, k): return getattr(self._d, k)
    @staticmethod
    def _box(b):
        x0, y0, x1, y1 = b
        return [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]
    def ellipse(self, b, *a, **k): return self._d.ellipse(self._box(b), *a, **k)
    def rectangle(self, b, *a, **k): return self._d.rectangle(self._box(b), *a, **k)
    def chord(self, b, *a, **k): return self._d.chord(self._box(b), *a, **k)
    def pieslice(self, b, *a, **k): return self._d.pieslice(self._box(b), *a, **k)
    def arc(self, b, *a, **k): return self._d.arc(self._box(b), *a, **k)

class Scene:
    def __init__(self, seed=1, base=0):
        self.r = random.Random(seed)
        self.im = Image.new('L', (W, H), base)
        self.d = _Draw(self.im)

    # ------------------------------------------------------------ háttér
    def sky(self, top=10, bottom=60, y1=H):
        for y in range(y1):
            t = y / max(1, y1 - 1)
            self.d.line([(0, y), (W, y)], fill=int(top + (bottom - top) * t))

    def stars(self, n=50, ymax=220):
        for _ in range(n):
            x, y = self.r.randrange(W), self.r.randrange(ymax)
            self.d.point((x, y), fill=self.r.choice([140, 190, 255]))
            if self.r.random() < 0.15:
                self.d.line([(x - 2, y), (x + 2, y)], fill=180); self.d.line([(x, y - 2), (x, y + 2)], fill=180)

    def glow(self, x, y, r, level=200, blur=None):
        m = Image.new('L', (W, H), 0)
        ImageDraw.Draw(m).ellipse([x - r, y - r, x + r, y + r], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(blur or r / 2))
        self.im = Image.composite(Image.new('L', (W, H), level), self.im, m)
        self.d = _Draw(self.im)

    def lightpoly(self, pts, level=120, blur=8, amount=200):
        m = Image.new('L', (W, H), 0)
        ImageDraw.Draw(m).polygon(pts, fill=amount)
        m = m.filter(ImageFilter.GaussianBlur(blur))
        self.im = Image.composite(Image.new('L', (W, H), level), self.im, m)
        self.d = _Draw(self.im)

    def moon(self, x, y, r, halo=True):
        if halo: self.glow(x, y, r + 30, 90, 20)
        self.d.ellipse([x - r, y - r, x + r, y + r], fill=235)
        for cx, cy, cr in [(-0.3, -0.3, 0.22), (0.3, 0.25, 0.15), (0.05, 0.4, 0.1), (0.25, -0.35, 0.08)]:
            self.d.ellipse([x + cx * r - cr * r, y + cy * r - cr * r, x + cx * r + cr * r, y + cy * r + cr * r], fill=205)

    def fog(self, y, h=14, level=110, amount=70):
        m = Image.new('L', (W, H), 0)
        ImageDraw.Draw(m).rectangle([0, y, W, y + h], fill=amount)
        m = m.filter(ImageFilter.GaussianBlur(h * 0.7))
        self.im = Image.composite(Image.new('L', (W, H), level), self.im, m)
        self.d = _Draw(self.im)

    def ground(self, y, fill=12, rough=6, y2=H):
        pts = [(0, y2), (0, y)]
        for x in range(0, W + 20, 20):
            pts.append((x, y + self.r.randint(-rough, rough)))
        pts.append((W, y2))
        self.d.polygon(pts, fill=fill)

    def hills(self, y, amp=40, fill=20, n=3):
        pts = [(0, H)]
        ph = self.r.random() * 6
        for x in range(0, W + 10, 10):
            pts.append((x, y - amp * (0.5 + 0.5 * math.sin(x / W * n * math.pi + ph))))
        pts.append((W, H))
        self.d.polygon(pts, fill=fill)

    def water(self, y, fill=16, y2=H, glints=40, glint=70):
        self.d.rectangle([0, y, W, y2], fill=fill)
        for _ in range(glints):
            x = self.r.randrange(W); yy = self.r.randrange(y, y2)
            self.d.line([(x, yy), (x + self.r.randrange(4, 22), yy)], fill=glint)

    def bricks(self, x0=0, y0=0, x1=W, y1=H, fill=None, outline=34, bw=40, bh=18):
        for row, y in enumerate(range(y0, y1, bh)):
            off = (row % 2) * bw // 2
            for x in range(x0 - off, x1, bw):
                self.d.rectangle([x, y, x + bw - 2, y + bh - 2], fill=fill, outline=outline)

    def floor(self, y, fill=20, lines=34, vx=W // 2):
        self.d.rectangle([0, y, W, H], fill=fill)
        for i in range(-2, 10):
            self.d.line([(vx, y), (i * 45 - 60, H)], fill=lines)
        for k in range(1, 6):
            yy = y + (H - y) * (k / 6) ** 1.6
            self.d.line([(0, yy), (W, yy)], fill=lines)

    def arch(self, x0, x1, y0, y1, fill=40):
        w = x1 - x0
        self.d.rectangle([x0, y0 + w / 2, x1, y1], fill=fill)
        self.d.pieslice([x0, y0, x1, y0 + w], 180, 360, fill=fill)

    # ------------------------------------------------------------ táj
    def pine(self, x, y, h, fill=6):
        w = h * 0.38
        for i in range(5):
            t = i / 5
            yy = y - h * (0.18 + t * 0.8)
            ww = w * (1 - t * 0.75)
            self.d.polygon([(x - ww, yy + h * 0.22), (x + ww, yy + h * 0.22), (x, yy - h * 0.05)], fill=fill)
        self.d.rectangle([x - 2, y - h * 0.2, x + 2, y], fill=fill)

    def forest(self, y, n=14, hmin=60, hmax=140, fill=6, x0=0, x1=W):
        for _ in range(n):
            self.pine(self.r.randrange(x0, x1), y + self.r.randrange(0, 20), self.r.randrange(hmin, hmax), fill)

    def deadtree(self, x, y, h, fill=8, width=7):
        self.d.line([(x, y), (x - 4, y - h)], fill=fill, width=width)
        def branch(px, py, a, l, wd, depth):
            if depth == 0 or l < 6: return
            ex, ey = px + l * math.cos(a), py + l * math.sin(a)
            self.d.line([(px, py), (ex, ey)], fill=fill, width=max(1, wd))
            branch(ex, ey, a - 0.5 + self.r.random() * 0.2, l * 0.7, wd - 1, depth - 1)
            branch(ex, ey, a + 0.4 + self.r.random() * 0.2, l * 0.6, wd - 1, depth - 1)
        for f, a in [(0.65, -2.3), (0.75, -0.8), (0.9, -1.8), (0.55, -0.5)]:
            branch(x - 4 * f, y - h * f, a, h * 0.35, width - 3, 4)

    def reeds(self, x0, x1, y, n=40, fill=8, hmax=140):
        for _ in range(n):
            x = self.r.randrange(x0, x1); h = self.r.randrange(40, hmax); yy = y + self.r.randrange(0, 40)
            tx = x + self.r.randrange(-10, 10)
            self.d.line([(x, yy), (tx, yy - h)], fill=fill, width=2)
            if self.r.random() < 0.5: self.d.ellipse([tx - 2, yy - h - 10, tx + 3, yy - h + 2], fill=fill)

    def rocks(self, y, n=8, fill=14, smax=50):
        for _ in range(n):
            x = self.r.randrange(-20, W); s = self.r.randrange(15, smax)
            pts = [(x + s * math.cos(a) * (0.7 + 0.5 * self.r.random()), y - abs(s * math.sin(a)) * (0.6 + 0.6 * self.r.random()))
                   for a in [i * math.pi / 6 for i in range(7)]]
            self.d.polygon(pts, fill=fill)

    def snow(self, n=300, level=200):
        for _ in range(n):
            x, y = self.r.randrange(W), self.r.randrange(H)
            self.d.line([(x, y), (x + 3, y + 1)], fill=level)

    # ------------------------------------------------------------ épületek
    def tower(self, x, y, w, h, fill=8, win=230, cone=True, broken=False):
        self.d.rectangle([x - w / 2, y - h, x + w / 2, y], fill=fill)
        top = y - h
        for i in range(-2, 3):
            self.d.rectangle([x + i * w / 5 - w / 14, top - w / 6, x + i * w / 5 + w / 14, top], fill=fill)
        if cone and not broken:
            self.d.polygon([(x - w / 2 - 4, top - w / 8), (x + w / 2 + 4, top - w / 8), (x, top - w * 1.1)], fill=fill)
        if broken:
            self.d.polygon([(x - w / 2, top), (x - w / 4, top - w * 0.5), (x, top - w * 0.2), (x + w / 4, top - w * 0.7),
                            (x + w / 2, top)], fill=fill)
        if win:
            for k in range(3):
                yy = top + h * (0.2 + 0.25 * k)
                self.d.rectangle([x - w / 10, yy, x + w / 10, yy + h * 0.06], fill=win if k == 0 else win // 2)

    def house(self, x, y, w, h, fill=10, win=180, roof=True):
        self.d.rectangle([x - w / 2, y - h, x + w / 2, y], fill=fill)
        if roof: self.d.polygon([(x - w / 2 - 6, y - h), (x + w / 2 + 6, y - h), (x, y - h - w * 0.55)], fill=fill)
        if win:
            self.d.rectangle([x - w / 4 - 5, y - h * 0.65, x - w / 4 + 5, y - h * 0.45], fill=win)
            self.d.rectangle([x + w / 4 - 5, y - h * 0.65, x + w / 4 + 5, y - h * 0.45], fill=win // 2)

    def chapel(self, x, y, w, h, fill=10, win=160):
        self.house(x, y, w, h, fill, win=0)
        self.d.rectangle([x - 7, y - h - w * 0.55 - 30, x + 7, y - h - w * 0.4], fill=fill)
        self.d.line([(x, y - h - w * 0.55 - 48), (x, y - h - w * 0.55 - 30)], fill=fill, width=3)
        self.d.line([(x - 7, y - h - w * 0.55 - 42), (x + 7, y - h - w * 0.55 - 42)], fill=fill, width=3)
        if win: self.arch(x - 8, x + 8, y - h * 0.8, y - h * 0.35, win)

    def well(self, x, y, s=1, fill=60, skulls=False):
        self.d.rectangle([x - 30 * s, y - 30 * s, x + 30 * s, y], fill=fill)
        self.d.rectangle([x - 34 * s, y - 36 * s, x + 34 * s, y - 28 * s], fill=fill + 20)
        self.d.line([(x - 28 * s, y - 36 * s), (x - 28 * s, y - 90 * s)], fill=fill, width=4)
        self.d.line([(x + 28 * s, y - 36 * s), (x + 28 * s, y - 90 * s)], fill=fill, width=4)
        self.d.line([(x - 34 * s, y - 90 * s), (x + 34 * s, y - 90 * s)], fill=fill, width=5)
        self.d.line([(x, y - 90 * s), (x, y - 60 * s)], fill=fill + 40, width=1)
        self.d.rectangle([x - 6 * s, y - 62 * s, x + 6 * s, y - 52 * s], fill=fill + 30)
        if skulls:
            for i in range(-2, 3):
                cx = x + i * 13 * s
                self.d.ellipse([cx - 5, y - 46 * s, cx + 5, y - 36 * s], fill=200)
                self.d.ellipse([cx - 3, y - 43 * s, cx - 1, y - 41 * s], fill=20)
                self.d.ellipse([cx + 1, y - 43 * s, cx + 3, y - 41 * s], fill=20)

    def bars(self, x0, x1, y0, y1, fill=6, step=18, width=5):
        for x in range(int(x0), int(x1) + 1, step):
            self.d.line([(x, y0), (x, y1)], fill=fill, width=width)
        self.d.line([(x0, y0 + 10), (x1, y0 + 10)], fill=fill, width=width)
        self.d.line([(x0, y1 - 20), (x1, y1 - 20)], fill=fill, width=width)

    def shelves(self, x0, x1, y0, y1, fill=40, book=90):
        for y in range(int(y0), int(y1), 34):
            self.d.rectangle([x0, y + 28, x1, y + 32], fill=fill)
            x = x0 + 2
            while x < x1 - 6:
                bw = self.r.randrange(4, 10); bh = self.r.randrange(16, 27)
                self.d.rectangle([x, y + 28 - bh, x + bw - 1, y + 27], fill=self.r.choice([book, book - 30, book + 30]))
                x += bw + 1

    def flask(self, x, y, s=1, level=200):
        self.d.ellipse([x - 12 * s, y - 24 * s, x + 12 * s, y], fill=level)
        self.d.rectangle([x - 3 * s, y - 40 * s, x + 3 * s, y - 20 * s], fill=level)
        self.d.ellipse([x - 8 * s, y - 18 * s, x + 2 * s, y - 10 * s], fill=255)

    def torch(self, x, y):
        self.d.line([(x, y), (x + 6, y - 24)], fill=40, width=4)
        self.glow(x + 6, y - 34, 26, 170, 14)
        self.d.polygon([(x, y - 30), (x + 6, y - 50), (x + 12, y - 30)], fill=250)

    def fire(self, x, y, s=1):
        self.glow(x, y - 20 * s, 70 * s, 150, 30 * s)
        for i in range(5):
            dx = (i - 2) * 7 * s
            self.d.polygon([(x + dx - 8 * s, y), (x + dx + self.r.randint(-4, 4), y - (25 + self.r.randrange(20)) * s),
                            (x + dx + 8 * s, y)], fill=240)
        self.d.line([(x - 20 * s, y + 2), (x + 20 * s, y - 2)], fill=30, width=int(5 * s))
        self.d.line([(x - 20 * s, y - 2), (x + 20 * s, y + 2)], fill=30, width=int(5 * s))

    # ------------------------------------------------------------ alakok
    def person(self, x, y, h, fill=4, sword=False, cloak=True, staff=False, beard=False, hood=False,
               hat=False, arms_up=False, child=False, eyes=None, lantern=False, bent=False):
        hd = h * (0.15 if child else 0.13)
        sh = y - h + hd * 2
        lean = h * 0.12 if bent else 0
        if cloak:
            self.d.polygon([(x - h * 0.12 + lean, sh), (x + h * 0.12 + lean, sh), (x + h * 0.2, y), (x - h * 0.2, y)], fill=fill)
        else:
            self.d.polygon([(x - h * 0.1 + lean, sh), (x + h * 0.1 + lean, sh), (x + h * 0.08, y - h * 0.45), (x - h * 0.08, y - h * 0.45)], fill=fill)
            self.d.line([(x - h * 0.05, y - h * 0.46), (x - h * 0.1, y)], fill=fill, width=max(2, int(h * 0.06)))
            self.d.line([(x + h * 0.05, y - h * 0.46), (x + h * 0.1, y)], fill=fill, width=max(2, int(h * 0.06)))
        hx, hy = x + lean, y - h + hd
        self.d.ellipse([hx - hd, hy - hd, hx + hd, hy + hd], fill=fill)
        if hood: self.d.polygon([(hx - hd * 1.1, hy + hd * 0.3), (hx, hy - hd * 1.9), (hx + hd * 1.1, hy + hd * 0.3)], fill=fill)
        if hat: self.d.polygon([(hx - hd * 1.8, hy - hd * 0.5), (hx + hd * 1.8, hy - hd * 0.5), (hx + hd * 0.4, hy - hd * 2.8)], fill=fill)
        if beard: self.d.polygon([(hx - hd * 0.8, hy + hd * 0.2), (hx + hd * 0.8, hy + hd * 0.2), (hx, hy + hd * 2.6)], fill=fill)
        aw = max(2, int(h * 0.05))
        if arms_up:
            self.d.line([(x - h * 0.1 + lean, sh + 4), (x - h * 0.3, sh - h * 0.25)], fill=fill, width=aw)
            self.d.line([(x + h * 0.1 + lean, sh + 4), (x + h * 0.3, sh - h * 0.25)], fill=fill, width=aw)
        else:
            self.d.line([(x + h * 0.1 + lean, sh + 4), (x + h * 0.25, sh + h * 0.3)], fill=fill, width=aw)
        if sword:
            self.d.line([(x + h * 0.25, sh + h * 0.3), (x + h * 0.45, sh - h * 0.25)], fill=fill if fill > 100 else 230, width=max(2, aw - 1))
        if staff:
            self.d.line([(x - h * 0.22, y), (x - h * 0.26, y - h * 1.05)], fill=fill, width=max(2, aw - 1))
        if lantern:
            lx, ly = x + h * 0.27, sh + h * 0.36
            self.glow(lx, ly, h * 0.25, 160, h * 0.12)
            self.d.rectangle([lx - 4, ly - 6, lx + 4, ly + 6], fill=250)
        if eyes is not None:
            self.d.ellipse([hx - hd * 0.5 - 1, hy - 1, hx - hd * 0.5 + 2, hy + 2], fill=eyes)
            self.d.ellipse([hx + hd * 0.5 - 2, hy - 1, hx + hd * 0.5 + 1, hy + 2], fill=eyes)

    def crow(self, x, y, s, fill=5, perched=False):
        if perched:
            self.d.ellipse([x - s, y - s * 0.7, x + s, y + s * 0.5], fill=fill)
            self.d.ellipse([x + s * 0.5, y - s * 1.2, x + s * 1.2, y - s * 0.4], fill=fill)
            self.d.polygon([(x + s * 1.1, y - s * 0.9), (x + s * 1.7, y - s * 0.75), (x + s * 1.1, y - s * 0.6)], fill=fill)
            self.d.polygon([(x - s, y), (x - s * 1.8, y + s * 0.4), (x - s * 0.8, y + s * 0.3)], fill=fill)
        else:
            self.d.line([(x - s, y - s / 2), (x - s / 3, y), (x, y - s / 4), (x + s / 3, y), (x + s, y - s / 2)], fill=fill,
                        width=max(2, int(s / 4)))

    def crows(self, n, x0=0, x1=W, y0=10, y1=200, smin=5, smax=12, fill=5):
        for _ in range(n):
            self.crow(self.r.randrange(x0, x1), self.r.randrange(y0, y1), self.r.randrange(smin, smax), fill)

    def wolf(self, x, y, s, fill=4, eyes=255, facing=1):
        f = facing
        self.d.ellipse([x - s * 1.2, y - s * 0.9, x + s * 0.8, y - s * 0.1], fill=fill)          # törzs
        self.d.polygon([(x + f * s * 0.5, y - s * 0.8), (x + f * s * 1.4, y - s * 1.2), (x + f * s * 1.9, y - s * 0.75),
                        (x + f * s * 1.3, y - s * 0.45)], fill=fill)                                # fej
        self.d.polygon([(x + f * s * 1.0, y - s * 1.1), (x + f * s * 1.15, y - s * 1.5), (x + f * s * 1.3, y - s * 1.1)], fill=fill)
        for dx in (-0.9, -0.6, 0.3, 0.55):
            self.d.line([(x + dx * s, y - s * 0.3), (x + dx * s + 2, y)], fill=fill, width=max(2, int(s / 6)))
        self.d.polygon([(x - f * s * 1.1, y - s * 0.7), (x - f * s * 2.0, y - s * 0.3), (x - f * s * 1.0, y - s * 0.45)], fill=fill)
        if eyes:
            ex, ey = x + f * s * 1.45, y - s * 0.95
            self.glow(ex, ey, s * 0.25, eyes, s * 0.12)
            self.d.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=255)

    def troll(self, x, y, s, fill=6, eyes=230):
        self.d.ellipse([x - s, y - s * 2.0, x + s, y - s * 0.4], fill=fill)
        self.d.ellipse([x - s * 0.5, y - s * 2.6, x + s * 0.5, y - s * 1.8], fill=fill)
        self.d.line([(x - s * 0.9, y - s * 1.6), (x - s * 1.5, y - s * 0.3)], fill=fill, width=int(s * 0.35))
        self.d.line([(x + s * 0.9, y - s * 1.6), (x + s * 1.5, y - s * 0.3)], fill=fill, width=int(s * 0.35))
        self.d.line([(x - s * 0.4, y - s * 0.6), (x - s * 0.5, y)], fill=fill, width=int(s * 0.4))
        self.d.line([(x + s * 0.4, y - s * 0.6), (x + s * 0.5, y)], fill=fill, width=int(s * 0.4))
        if eyes:
            for dx in (-0.2, 0.2):
                self.d.ellipse([x + dx * s - 3, y - s * 2.3 - 3, x + dx * s + 3, y - s * 2.3 + 3], fill=eyes)

    def skeleton(self, x, y, h, lit=210, weapon=True):
        hd = h * 0.11
        self.d.ellipse([x - hd, y - h, x + hd, y - h + hd * 2], fill=lit)
        self.d.ellipse([x - hd * 0.55, y - h + hd * 0.6, x - hd * 0.15, y - h + hd], fill=10)
        self.d.ellipse([x + hd * 0.15, y - h + hd * 0.6, x + hd * 0.55, y - h + hd], fill=10)
        top = y - h + hd * 2
        self.d.line([(x, top), (x, y - h * 0.45)], fill=lit, width=2)
        for k in range(4):
            yy = top + h * 0.06 + k * h * 0.06
            self.d.line([(x - h * 0.1, yy), (x + h * 0.1, yy)], fill=lit, width=2)
        self.d.line([(x, y - h * 0.45), (x - h * 0.12, y)], fill=lit, width=2)
        self.d.line([(x, y - h * 0.45), (x + h * 0.12, y)], fill=lit, width=2)
        self.d.line([(x - h * 0.1, top + 3), (x - h * 0.22, y - h * 0.4)], fill=lit, width=2)
        self.d.line([(x + h * 0.1, top + 3), (x + h * 0.24, top + h * 0.2)], fill=lit, width=2)
        if weapon:
            self.d.line([(x + h * 0.24, top + h * 0.2), (x + h * 0.3, y - h * 1.1)], fill=lit - 40, width=2)
            self.d.polygon([(x + h * 0.3, y - h * 1.1), (x + h * 0.42, y - h * 1.0), (x + h * 0.31, y - h * 0.93)], fill=lit - 40)

    def ghost(self, x, y, h, level=170):
        m = Image.new('L', (W, H), 0); g = ImageDraw.Draw(m)
        g.ellipse([x - h * 0.13, y - h, x + h * 0.13, y - h * 0.74], fill=255)
        g.polygon([(x - h * 0.17, y - h * 0.75), (x + h * 0.17, y - h * 0.75), (x + h * 0.25, y), (x + h * 0.1, y - h * 0.08),
                   (x, y), (x - h * 0.1, y - h * 0.08), (x - h * 0.25, y)], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(h * 0.04))
        self.im = Image.composite(Image.new('L', (W, H), level), self.im, m)
        self.d = _Draw(self.im)
        self.d.ellipse([x - h * 0.07, y - h * 0.9, x - h * 0.03, y - h * 0.86], fill=20)
        self.d.ellipse([x + h * 0.03, y - h * 0.9, x + h * 0.07, y - h * 0.86], fill=20)

    def spider(self, x, y, s, fill=4, eyes=230):
        self.d.ellipse([x - s, y - s * 0.8, x + s, y + s * 0.8], fill=fill)
        self.d.ellipse([x - s * 0.5, y + s * 0.5, x + s * 0.5, y + s * 1.2], fill=fill)
        for side in (-1, 1):
            for k in range(4):
                a = -0.9 + k * 0.6
                kx, ky = x + side * s * 1.6, y + (k - 1.5) * s * 0.6 - s * 0.6
                self.d.line([(x + side * s * 0.6, y + (k - 1.5) * s * 0.3), (kx, ky)], fill=fill, width=max(2, int(s / 6)))
                self.d.line([(kx, ky), (kx + side * s * 0.6, ky + s * 1.1)], fill=fill, width=max(2, int(s / 7)))
        for dx in (-0.25, -0.08, 0.08, 0.25):
            self.d.ellipse([x + dx * s - 2, y + s * 0.85 - 2, x + dx * s + 2, y + s * 0.85 + 2], fill=eyes)

    def frog(self, x, y, s, fill=6, crown=False):
        self.d.ellipse([x - s, y - s * 0.8, x + s, y], fill=fill)
        self.d.ellipse([x - s * 0.8, y - s * 1.15, x - s * 0.3, y - s * 0.65], fill=fill)
        self.d.ellipse([x + s * 0.3, y - s * 1.15, x + s * 0.8, y - s * 0.65], fill=fill)
        self.d.ellipse([x - s * 0.62, y - s * 1.0, x - s * 0.45, y - s * 0.83], fill=220)
        self.d.ellipse([x + s * 0.45, y - s * 1.0, x + s * 0.62, y - s * 0.83], fill=220)
        self.d.polygon([(x - s, y - s * 0.1), (x - s * 1.6, y), (x - s * 0.7, y)], fill=fill)
        self.d.polygon([(x + s, y - s * 0.1), (x + s * 1.6, y), (x + s * 0.7, y)], fill=fill)
        if crown:
            cx, cy = x, y - s * 1.15
            self.d.polygon([(cx - s * 0.4, cy), (cx - s * 0.4, cy - s * 0.4), (cx - s * 0.2, cy - s * 0.2), (cx, cy - s * 0.5),
                            (cx + s * 0.2, cy - s * 0.2), (cx + s * 0.4, cy - s * 0.4), (cx + s * 0.4, cy)], fill=230)

    def eagle(self, x, y, s, fill=6, up=True):
        k = -1 if up else 1
        self.d.polygon([(x, y), (x - s * 2.4, y + k * s * 0.9), (x - s * 1.6, y + k * s * 0.2), (x - s * 0.5, y + s * 0.2)], fill=fill)
        self.d.polygon([(x, y), (x + s * 2.4, y + k * s * 0.9), (x + s * 1.6, y + k * s * 0.2), (x + s * 0.5, y + s * 0.2)], fill=fill)
        self.d.ellipse([x - s * 0.4, y - s * 0.3, x + s * 0.4, y + s * 0.9], fill=fill)
        self.d.ellipse([x - s * 0.25, y - s * 0.6, x + s * 0.25, y - s * 0.1], fill=fill)
        self.d.polygon([(x - s * 0.4, y + s * 0.8), (x, y + s * 1.4), (x + s * 0.4, y + s * 0.8)], fill=fill)

    def demon(self, x, y, s, fill=4, eyes=255):
        self.d.polygon([(x, y - s * 1.2), (x - s * 2.6, y - s * 2.4), (x - s * 2.2, y - s * 1.2), (x - s * 2.6, y - s * 0.4),
                        (x - s * 0.6, y - s * 0.4)], fill=fill)
        self.d.polygon([(x, y - s * 1.2), (x + s * 2.6, y - s * 2.4), (x + s * 2.2, y - s * 1.2), (x + s * 2.6, y - s * 0.4),
                        (x + s * 0.6, y - s * 0.4)], fill=fill)
        self.d.ellipse([x - s * 0.6, y - s * 1.6, x + s * 0.6, y], fill=fill)
        self.d.ellipse([x - s * 0.4, y - s * 2.2, x + s * 0.4, y - s * 1.4], fill=fill)
        self.d.polygon([(x + s * 0.3, y - s * 1.9), (x + s * 0.9, y - s * 1.75), (x + s * 0.3, y - s * 1.6)], fill=fill)
        for dx in (-0.15, 0.15):
            self.glow(x + dx * s, y - s * 1.85, s * 0.12, eyes, s * 0.06)

    def save(self, path):
        # a sötét tónusok feketére tolva: a 2 színű raszterben ne legyen mindenütt zaj
        im = self.im.point(lambda v: 0 if v < 26 else min(255, int(30 + (v - 26) * 225 / 190)))
        ImageOps.invert(im).save(path)
