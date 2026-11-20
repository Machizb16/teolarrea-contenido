"""Fondos, cierres y portadas de la colección LIBROS PROHIBIDOS (No abras / No mires / No creas este libro).

Cada fondo devuelve fn(u, t) -> array float (AH, W, 3) en 0..1, igual que los de series.py.
Todo está dibujado con PIL/numpy: no se usa ningún texto de los libros.
"""
import os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
os.environ['ORIENT'] = 'v'
import trailer2 as T

W, AH, FPS = T.W, T.AH, T.FPS
F = T.FNT
ANTON = os.path.join(F, 'Anton-Regular.ttf')
BEBAS, PAGI, COUR, COURB, HAND = T.BEBAS, T.PAGI, T.COUR, T.COURB, T.HAND
PAGR = os.path.join(F, 'texgyrepagella-regular.otf')
NX, NY, XX, YY = T.NX, T.NY, T.XX, T.YY
ROJO = (200, 33, 28)
CREMA = (236, 230, 218)
NEGRO = (12, 11, 11)
ESC = os.path.join(T.A_, 'escenas')

LIBROS = {
    'abras': dict(verbo='ABRAS', titulo='No abras este libro', sub='No eres un lector. Eres parte de la historia.'),
    'mires': dict(verbo='MIRES', titulo='No mires este libro', sub='Mira donde nadie mira.'),
    'creas': dict(verbo='CREAS', titulo='No creas este libro', sub='Te voy a mentir siete veces.'),
}


def fnt(path, size): return ImageFont.truetype(path, size)


def lamp(cx, cy, sx, sy):
    return np.exp(-(((NX - cx) / sx) ** 2 + ((NY - cy) / sy) ** 2))[..., None]


def still(img, z0=1.0, z1=1.08, c0=(0.5, 0.5), c1=(0.5, 0.5), luz=(0.5, 0.5, 0.7, 0.75), amb=0.18, tinte=(1, 1, 1)):
    """Plano fijo con empuje lento de cámara y luz cálida."""
    L = lamp(*luz) if luz else 1.0
    tint = np.array(tinte, np.float32)
    def fn(u, t):
        a = T.arr(T.kenburns(img, u, z0, z1, c0, c1))
        return a * tint * (amb + (1 - amb) * L)
    return fn


def ctext(d, cx, y, s, f, fill, **k):
    w = d.textlength(s, font=f); d.text((cx - w / 2, y), s, font=f, fill=fill, **k)


def ruido_papel(w, h, base, seed=1, k=10):
    rng = np.random.default_rng(seed)
    n = rng.normal(0, k, (h // 4, w // 4)).astype(np.float32)
    n = np.asarray(Image.fromarray(np.clip(n + 128, 0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) - 128
    a = np.array(base, np.float32)[None, None, :] + n[..., None]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    v = 1 - 0.25 * (((xx / w - 0.5) * 2) ** 2 + ((yy / h - 0.5) * 2) ** 2)
    return Image.fromarray(np.clip(a * v[..., None], 0, 255).astype(np.uint8))


def simbolo(d, x, y, s, cual, col):
    if cual in ('▲', 'triangulo'):
        d.polygon([(x, y - s), (x - s * 0.9, y + s * 0.6), (x + s * 0.9, y + s * 0.6)], outline=col, width=4)
    elif cual in ('◆', 'rombo'):
        d.polygon([(x, y - s), (x + s * 0.7, y), (x, y + s), (x - s * 0.7, y)], outline=col, width=4)
    else:
        d.ellipse((x - s * 0.75, y - s * 0.75, x + s * 0.75, y + s * 0.75), fill=col)


# ====================================================================== NO ABRAS ESTE LIBRO
def faro():
    """Faro de noche: tres destellos y una pausa."""
    rng = np.random.default_rng(3)
    sky = np.zeros((AH, W, 3), np.float32)
    g = NY[..., None]
    sky += np.array([0.03, 0.045, 0.08]) * (1.4 - g) + np.array([0.02, 0.02, 0.03])
    for _ in range(260):
        x, y = rng.integers(0, W), rng.integers(0, int(AH * 0.55)); b = rng.uniform(0.25, 0.8)
        sky[y:y + 2, x:x + 2] += b
    img = Image.fromarray((np.clip(sky, 0, 1) * 255).astype(np.uint8)); d = ImageDraw.Draw(img)
    # mar
    d.rectangle((0, int(AH * 0.66), W, AH), fill=(8, 12, 20))
    # acantilado
    d.polygon([(int(W * 0.18), int(AH * 0.70)), (int(W * 0.30), int(AH * 0.665)), (int(W * 0.45), int(AH * 0.615)), (int(W * 0.55), int(AH * 0.592)),
               (int(W * 0.80), int(AH * 0.596)), (int(W * 0.92), int(AH * 0.62)), (W, int(AH * 0.64)), (W, int(AH * 0.76)), (int(W * 0.25), int(AH * 0.76))], fill=(6, 7, 10))
    d.rectangle((0, int(AH * 0.76), W, AH), fill=(8, 12, 20))
    # torre
    lx, ly = int(W * 0.66), int(AH * 0.41)
    d.polygon([(lx - 52, int(AH * 0.59)), (lx - 34, ly + 40), (lx + 34, ly + 40), (lx + 52, int(AH * 0.59))], fill=(30, 30, 34))
    for k in range(4):
        y0 = ly + 70 + k * 55; d.rectangle((lx - 40 + k * 3, y0, lx + 40 - k * 3, y0 + 22), fill=(70, 20, 18))
    d.rectangle((lx - 40, ly + 30, lx + 40, ly + 44), fill=(20, 20, 22))
    d.rectangle((lx - 28, ly - 18, lx + 28, ly + 30), fill=(60, 58, 50))
    d.polygon([(lx - 36, ly - 18), (lx, ly - 60), (lx + 36, ly - 18)], fill=(20, 20, 22))
    base = T.arr(img)
    dx, dy = XX - lx, YY - ly; dist = np.sqrt(dx ** 2 + dy ** 2) + 1; ang = np.arctan2(dy, dx)
    halo = np.exp(-(dist / 38) ** 2)[..., None]; glow = np.exp(-dist / 260)[..., None]
    sea = (NY > 0.665)[..., None] * np.exp(-((XX - lx) / 90) ** 2)[..., None]
    col = np.array([1.0, 0.93, 0.75])
    ripple = rng.random((AH, 1, 1)).astype(np.float32)

    def flash(t):
        p = t % 3.6
        return sum(np.exp(-((p - c) / 0.11) ** 2) for c in (0.3, 0.85, 1.4))

    def fn(u, t):
        f = flash(t); th = np.pi * (0.92 + 0.08 * math.sin(t * 0.7))
        beam = np.exp((np.cos(ang - th) - 1) / 0.0035)[..., None] * np.exp(-dist / 1400)[..., None]
        beam2 = np.exp((np.cos(ang) - 1) / 0.0035)[..., None] * np.exp(-dist / 900)[..., None] * 0.5
        light = (halo * 2.2 + glow * 0.35 + (beam + beam2) * 0.55 + sea * 0.35 * (0.6 + 0.4 * np.sin(ripple * 40 + t * 3))) * f
        return np.clip(base * (0.75 + 0.25 * f) + light * col + halo * 0.15 * col, 0, 1)
    return fn


TEXTO_RELLENO = ('Las páginas tienen una manera rara de esperar. Se quedan quietas en la estantería, '
                 'se dejan mover, se dejan prestar, y un día alguien las abre por donde no debía. '
                 'Entonces ya no hay forma de volver a dejarlas como estaban. Pasa con las puertas, '
                 'con las cartas y con algunas preguntas. Uno cree que solo está mirando y en realidad '
                 'ya ha empezado a jugar. Las reglas estaban escritas desde el principio, aunque nadie '
                 'las leyera en voz alta. Y lo que se lee no se puede desleer. ') * 4


def pagina(notas=(), simbolos=('▲', '◆', '●'), numero=None):
    """Página vieja con notas a lápiz en el margen (texto de relleno propio, no del libro)."""
    pw, ph = 1350, 2400
    img = ruido_papel(pw, ph, (226, 214, 188), seed=5, k=9); d = ImageDraw.Draw(img)
    f = fnt(PAGR, 44); y = 180; words = TEXTO_RELLENO.split(); i = 0
    while y < ph - 200:
        line = ''
        while i < len(words) and d.textlength(line + ' ' + words[i], font=f) < pw - 380:
            line = (line + ' ' + words[i]).strip(); i += 1
        d.text((190, y), line, font=f, fill=(92, 84, 72)); y += 66
        if i >= len(words): i = 0
    if numero is not None:
        ctext(d, pw / 2, 90, f'— {numero} —', fnt(PAGI, 52), (90, 80, 68))
    paper = img.filter(ImageFilter.GaussianBlur(0.8))
    hf = fnt(HAND, 84)
    total = sum(len(n) for n in notas)

    def fn(u, t):
        im = paper.copy(); dd = ImageDraw.Draw(im, 'RGBA')
        k = int(total * min(1, max(0, (t - 0.3) / 2.2))); left = k
        y = ph * 0.6
        for j, n in enumerate(notas):
            s = n[:max(0, min(len(n), left))]; left -= len(n)
            dd.rectangle((150, y - 10, pw - 150, y + 110), fill=(226, 214, 188, 200))
            simbolo(dd, 215, y + 50, 26, simbolos[j % len(simbolos)], (70, 70, 78))
            dd.text((270, y), s, font=hf, fill=(62, 62, 70)); y += 150
        a = T.arr(T.kenburns(im, u, 1.0, 1.08, (0.5, 0.55), (0.5, 0.6)))
        return a * (0.22 + 0.85 * lamp(0.45, 0.55, 0.7, 0.8))
    return fn


def tipos(texto='NO ABRAS'):
    """Imprenta de composición a mano: tipos de metal con letras invertidas."""
    pw, ph = 1350, 2400
    img = Image.new('RGB', (pw, ph), (40, 28, 18)); d = ImageDraw.Draw(img)
    rng = np.random.default_rng(9); fl = fnt(COURB, 54)
    cw, chh = 150, 150
    for gy in range(0, ph, chh):
        for gx in range(0, pw, cw):
            d.rectangle((gx + 6, gy + 6, gx + cw - 6, gy + chh - 6), fill=(24, 17, 11), outline=(88, 62, 38), width=8)
            for _ in range(5):
                x = gx + rng.integers(22, cw - 70); y = gy + rng.integers(22, chh - 70)
                d.rectangle((x, y, x + 44, y + 50), fill=(110, 110, 112))
    # componedor con el texto
    s = 150; n = len(texto); x0 = (pw - n * s) / 2; y0 = ph * 0.47
    d.rectangle((x0 - 40, y0 - 40, x0 + n * s + 40, y0 + s + 40), fill=(150, 150, 155), outline=(60, 60, 62), width=10)
    fb = fnt(ANTON, 120)
    for k, ch in enumerate(texto[::-1]):
        x = x0 + k * s
        blk = Image.new('RGB', (s - 8, s - 8), (120, 120, 124)); bd = ImageDraw.Draw(blk)
        for r in range(0, s - 8, 3): bd.line((0, r, s, r), fill=(112 + r % 9, 112 + r % 9, 118))
        if ch != ' ':
            g = Image.new('L', (s - 8, s - 8), 0); gd = ImageDraw.Draw(g)
            ctext(gd, (s - 8) / 2, -4, ch, fb, 255)
            g = g.transpose(Image.FLIP_LEFT_RIGHT)
            blk.paste((30, 30, 32), (0, 0), g)
            ink = Image.new('RGB', blk.size, (16, 16, 18)); blk.paste(ink, (2, 2), g.filter(ImageFilter.GaussianBlur(1)))
        img.paste(blk, (int(x + 4), int(y0 + 4)))
    return still(img, 1.0, 1.12, (0.5, 0.52), (0.5, 0.5), luz=(0.5, 0.5, 0.55, 0.45), amb=0.22, tinte=(1.0, 0.92, 0.8))


def numeros(resaltar=None, desde=1.4):
    """Del 0 al 9. Si resaltar=N, ese número se enciende en rojo a partir de 'desde' segundos."""
    f = fnt(ANTON, 230)
    def capa(red):
        img = Image.new('RGB', (W, AH), NEGRO); d = ImageDraw.Draw(img)
        for k in range(10):
            r, c = divmod(k, 5)
            cx = W * (0.14 + 0.18 * c); y = AH * (0.50 + 0.18 * r)
            col = ROJO if (red and k == resaltar) else ((92, 88, 84) if red else CREMA)
            ctext(d, cx, y, str(k), f, col)
        return T.arr(img)
    A0 = capa(False); A1 = capa(True) if resaltar is not None else A0
    glow = None
    if resaltar is not None:
        r, c = divmod(resaltar, 5)
        glow = lamp(0.14 + 0.18 * c, 0.57 + 0.18 * r, 0.12, 0.08) * np.array([0.5, 0.08, 0.06])
    def fn(u, t):
        k = T.ease((t - desde) / 0.5) if resaltar is not None else 0
        a = A0 * (1 - k) + A1 * k
        if glow is not None: a = a + glow * k
        return a
    return fn


def palabras(lista, y0=0.36, ritmo=0.42):
    """Lista de palabras que aparecen una a una, como en los experimentos de memoria."""
    pw, ph = W, AH
    paper = ruido_papel(pw, ph, (232, 226, 212), seed=2, k=6); f = fnt(COURB, 62); fn_ = fnt(COUR, 44)
    def fn(u, t):
        im = paper.copy(); d = ImageDraw.Draw(im)
        n = int(t / ritmo) + 1
        sp = (0.96 - y0) * ph / max(12, len(lista))
        for k, w in enumerate(lista[:n]):
            y = ph * y0 + k * sp
            d.text((pw * 0.26, y + 12), f'{k + 1:>2}.', font=fn_, fill=(140, 40, 34))
            d.text((pw * 0.38, y), w.upper(), font=f, fill=(34, 32, 30))
        return T.arr(im) * (0.3 + 0.75 * lamp(0.5, 0.6, 0.8, 0.8))
    return fn


def llave_carta():
    """Una llave antigua y una carta boca abajo: hay que elegir."""
    img = ruido_papel(1350, 2400, (40, 12, 14), seed=7, k=8); d = ImageDraw.Draw(img)
    # llave
    kx, ky = 380, 1350
    d.ellipse((kx - 120, ky - 300, kx + 120, ky - 60), outline=(196, 150, 70), width=34)
    d.rectangle((kx - 22, ky - 70, kx + 22, ky + 380), fill=(186, 142, 62))
    d.rectangle((kx + 22, ky + 250, kx + 100, ky + 300), fill=(176, 134, 58))
    d.rectangle((kx + 22, ky + 330, kx + 80, ky + 372), fill=(176, 134, 58))
    d.line((kx - 10, ky - 60, kx - 10, ky + 370), fill=(232, 196, 120), width=6)
    # carta
    cx0, cy0, cw, ch = 760, 1000, 400, 600
    d.rounded_rectangle((cx0, cy0, cx0 + cw, cy0 + ch), radius=26, fill=(238, 234, 226))
    back = Image.new('RGB', (cw - 52, ch - 52), ROJO); bd = ImageDraw.Draw(back)
    for k in range(-ch, cw + ch, 34):
        bd.line((k, 0, k - ch, ch), fill=(236, 200, 190), width=4); bd.line((k - ch, 0, k, ch), fill=(236, 200, 190), width=4)
    img.paste(back, (cx0 + 26, cy0 + 26))
    d.rounded_rectangle((cx0 + 18, cy0 + 18, cx0 + cw - 18, cy0 + ch - 18), radius=18, outline=(238, 234, 226), width=14)
    im = img.rotate(0)
    base = still(im, 1.0, 1.06, (0.5, 0.56), (0.5, 0.56), luz=None)
    def fn(u, t):
        a = base(u, t); s = 0.5 + 0.5 * math.sin(t * 1.6)
        L = 0.15 + 0.95 * (lamp(0.28, 0.6, 0.22, 0.28) * s + lamp(0.72, 0.56, 0.22, 0.28) * (1 - s))
        return a * L
    return fn


# ====================================================================== NO MIRES ESTE LIBRO
def _bokeh(img, seed=1, n=26, y0=0.0, y1=0.5):
    rng = np.random.default_rng(seed)
    lay = Image.new('RGB', img.size, (0, 0, 0)); d = ImageDraw.Draw(lay)
    cols = [(255, 190, 90), (240, 70, 50), (120, 220, 120), (255, 230, 170)]
    for _ in range(n):
        x = rng.uniform(0, img.width); y = rng.uniform(y0, y1) * img.height; r = rng.uniform(14, 40)
        d.ellipse((x - r, y - r, x + r, y + r), fill=cols[rng.integers(0, 4)])
    lay = lay.filter(ImageFilter.GaussianBlur(14))
    return Image.fromarray(np.clip(np.asarray(img).astype(np.int16) + np.asarray(lay).astype(np.int16) * 0.55, 0, 255).astype(np.uint8))


def camara(cuenta=None):
    """Cámara de 35 mm en trípode con la luz roja del disparador. cuenta=10 añade la cuenta atrás."""
    pw, ph = 1350, 2400
    img = Image.new('RGB', (pw, ph), (30, 22, 18)); img = _bokeh(img, 3, 30, 0.05, 0.4); d = ImageDraw.Draw(img)
    cx, cy = pw / 2, ph * 0.5
    # trípode
    for dx in (-330, 0, 330):
        d.line((cx, cy + 180, cx + dx, ph), fill=(18, 18, 20), width=26)
    d.rectangle((cx - 40, cy + 140, cx + 40, cy + 230), fill=(25, 25, 27))
    # cuerpo
    d.rounded_rectangle((cx - 330, cy - 150, cx + 330, cy + 170), radius=30, fill=(22, 22, 24))
    d.rectangle((cx - 330, cy - 150, cx + 330, cy - 60), fill=(150, 150, 156))
    d.polygon([(cx - 90, cy - 150), (cx - 60, cy - 240), (cx + 60, cy - 240), (cx + 90, cy - 150)], fill=(140, 140, 146))
    for k in range(0, 660, 12): d.line((cx - 330 + k, cy - 50, cx - 330 + k, cy + 160), fill=(30, 30, 32), width=2)
    d.ellipse((cx - 175, cy - 140, cx + 175, cy + 210), fill=(10, 10, 12), outline=(110, 110, 116), width=14)
    d.ellipse((cx - 120, cy - 85, cx + 120, cy + 155), fill=(20, 24, 34))
    d.ellipse((cx - 60, cy - 50, cx + 10, cy + 20), fill=(90, 100, 130))
    d.rectangle((cx + 230, cy - 130, cx + 300, cy - 90), fill=(60, 60, 64))
    lx, ly = cx - 250, cy - 105
    base = img
    def fn(u, t):
        a = T.arr(T.kenburns(base, u, 1.0, 1.1, (0.5, 0.5), (0.5, 0.48)))
        a = a * (0.25 + 0.85 * lamp(0.5, 0.48, 0.6, 0.5))
        rate = 1.0 if cuenta is None else (1.0 if t < cuenta - 3 else 3.0)
        on = (t * rate * 2) % 2 < 1
        # posición del led en pantalla (aprox. con el zoom)
        z = 1.0 + 0.1 * T.ease(u); s = max(W / pw, AH / ph) * z
        cxs = 0.5 * pw; cys = (0.5 - 0.02 * T.ease(u)) * ph
        px = W / 2 + (lx - cxs) * s; py = AH / 2 + (ly - cys) * s
        led = np.exp(-(((XX - px) / 16) ** 2 + ((YY - py) / 16) ** 2))[..., None]
        halo = np.exp(-(((XX - px) / 120) ** 2 + ((YY - py) / 120) ** 2))[..., None]
        if on: a = a + led * np.array([1.4, 0.15, 0.1]) + halo * np.array([0.35, 0.03, 0.02])
        else: a = a + led * np.array([0.25, 0.03, 0.02])
        if cuenta is not None:
            n = max(0, cuenta - int(t))
            a = a + _txt(str(n), 0.86)
        return a
    return fn


_cache = {}


def _txt(s, yc, size=170, col=ROJO):
    k = (s, yc, size, col)
    if k not in _cache:
        img = Image.new('RGB', (W, AH), (0, 0, 0)); d = ImageDraw.Draw(img)
        ctext(d, W / 2, AH * yc - size * 0.65, s, fnt(ANTON, size), col)
        _cache[k] = T.arr(img)
    return _cache[k]


def _txtmask(s, yc): return _txt(s, yc).max(axis=2)


def _salon(cambio=None, seed=0):
    """Foto familiar en el salón dibujada en blanco y negro (genérica, sin detalles del libro)."""
    w, h = 1200, 860
    img = Image.new('L', (w, h), 70); d = ImageDraw.Draw(img)
    d.rectangle((0, 0, w, h * 0.62), fill=92)                       # pared
    for x in range(0, w, 60): d.line((x, 0, x, h * 0.62), fill=86, width=3)
    d.rectangle((0, h * 0.62, w, h), fill=58)                          # suelo
    # ventana con cortinas
    d.rectangle((760, 70, 1010, 330), fill=30); d.line((885, 70, 885, 330), fill=110, width=8); d.line((760, 200, 1010, 200), fill=110, width=8)
    cort = cambio == 'cortina'
    d.polygon([(735, 50), (800, 50), (780 if not cort else 900, 350), (735, 350)], fill=140)
    d.polygon([(970, 50), (1035, 50), (1035, 350), (990, 350)], fill=140)
    # cuadro
    if cambio == 'cuadro':
        q = Image.new('L', (190, 140), 150); qd = ImageDraw.Draw(q); qd.rectangle((14, 14, 176, 126), fill=110); qd.polygon([(20, 120), (90, 50), (170, 120)], fill=80)
        q = q.rotate(9, expand=True, fillcolor=0); m = q.point(lambda v: 255 if v else 0); img.paste(q, (430, 70), m); d = ImageDraw.Draw(img)
    else:
        d.rectangle((430, 80, 620, 220), fill=150); d.rectangle((444, 94, 606, 206), fill=110); d.polygon([(450, 200), (520, 130), (600, 200)], fill=80)
    # lámpara de pie
    lampon = cambio != 'lampara'
    d.line((690, 220, 690, 600), fill=40, width=10); d.polygon([(640, 220), (740, 220), (715, 150), (665, 150)], fill=225 if lampon else 120)
    # árbol
    d.polygon([(150, 120), (40, 520), (260, 520)], fill=40); d.rectangle((135, 520, 165, 580), fill=35)
    rng = np.random.default_rng(4)
    for _ in range(16):
        x = rng.uniform(80, 220); y = rng.uniform(200, 500)
        if abs(x - 150) < (y - 120) * 0.27: d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=200)
    if cambio != 'estrella':
        cx, cy = 150, 105; pts = []
        for k in range(10):
            r = 34 if k % 2 == 0 else 14; an = -math.pi / 2 + k * math.pi / 5
            pts.append((cx + r * math.cos(an), cy + r * math.sin(an)))
        d.polygon(pts, fill=235)
    # familia: siete figuras genéricas
    pos = [(300, 300, 1.0), (395, 330, 0.85), (490, 300, 1.0), (585, 315, 0.95), (680, 360, 0.7), (775, 345, 0.75), (870, 300, 1.0)]
    for x, y, s in pos:
        d.rounded_rectangle((x - 66 * s, y + 30 * s, x + 66 * s, y + 280), radius=int(34 * s), fill=34 + int(30 * s))
        d.rectangle((x - 12 * s, y + 20 * s, x + 12 * s, y + 44 * s), fill=150)
        d.ellipse((x - 32 * s, y - 40 * s, x + 32 * s, y + 36 * s), fill=176)
        d.chord((x - 33 * s, y - 44 * s, x + 33 * s, y + 10 * s), 180, 360, fill=50 + int(60 * ((x // 95) % 3)))
    # mesa con mantel
    d.rectangle((210, 560, 990, 600), fill=230); d.polygon([(210, 600), (990, 600), (1010, 760), (190, 760)], fill=215)
    for k in range(0, 800, 40): d.line((200 + k, 600, 195 + k * 1.02, 760), fill=200, width=2)
    velas = [420, 600, 780] if cambio != 'vela' else [420, 780]
    for x in velas:
        d.rectangle((x - 9, 500, x + 9, 560), fill=240); d.ellipse((x - 8, 478, x + 8, 502), fill=255)
    d.ellipse((540, 540, 660, 575), fill=180)
    img = img.filter(ImageFilter.GaussianBlur(1.6))
    a = np.asarray(img).astype(np.float32)
    a += np.random.default_rng(seed).normal(0, 7, a.shape)
    rgb = np.stack([a * 1.04, a * 0.98, a * 0.88], -1)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def foto(anio=1993, cambio=None, cuenta=None, rot=-2.0):
    """Foto de Nochebuena impresa sobre la mesa. cambio: estrella|lampara|cuadro|vela|cortina."""
    pw, ph = 1350, 2400
    mesa = ruido_papel(pw, ph, (48, 32, 22), seed=8, k=10)
    pic = _salon(cambio, seed=anio)
    card = Image.new('RGB', (pic.width + 60, pic.height + 60), (236, 232, 222)); card.paste(pic, (30, 30))
    dd = ImageDraw.Draw(card)
    stamp = f"24 12 '{anio % 100:02d}"
    dd.text((card.width - 300, card.height - 120), stamp, font=fnt(COURB, 44), fill=(255, 140, 40))
    card = card.rotate(rot, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0))
    m = Image.new('L', (pic.width + 60, pic.height + 60), 255).rotate(rot, expand=True, fillcolor=0)
    sh = Image.new('L', mesa.size, 0); x0 = (pw - card.width) // 2; y0 = int(ph * 0.56 - card.height / 2)
    sh.paste(m, (x0 + 18, y0 + 26)); sh = sh.filter(ImageFilter.GaussianBlur(22))
    mesa = Image.composite(Image.new('RGB', mesa.size, (5, 4, 3)), mesa, sh.point(lambda v: v * 0.7))
    mesa.paste(card, (x0, y0), m)
    base = still(mesa, 1.0, 1.04, (0.5, 0.5), (0.5, 0.5), luz=(0.5, 0.56, 0.75, 0.55), amb=0.25)
    if cuenta is None: return base
    def fn(u, t):
        a = base(u, t); n = max(0, cuenta - int(t))
        return a + _txt(str(n), 0.9, 120)
    return fn


def telefono():
    """Teléfono de disco de los noventa sobre un mueble del recibidor."""
    pw, ph = 1350, 2400
    img = ruido_papel(pw, ph, (54, 40, 30), seed=11, k=9); d = ImageDraw.Draw(img)
    d.rectangle((0, ph * 0.6, pw, ph), fill=(70, 46, 30))
    cx, cy = pw / 2, ph * 0.53
    d.polygon([(cx - 330, cy + 220), (cx - 250, cy - 120), (cx + 250, cy - 120), (cx + 330, cy + 220)], fill=(214, 204, 180))
    d.rounded_rectangle((cx - 380, cy - 250, cx + 380, cy - 130), radius=60, fill=(200, 190, 166))
    d.ellipse((cx - 420, cy - 290, cx - 260, cy - 110), fill=(200, 190, 166)); d.ellipse((cx + 260, cy - 290, cx + 420, cy - 110), fill=(200, 190, 166))
    d.ellipse((cx - 190, cy - 100, cx + 190, cy + 280), fill=(180, 170, 148), outline=(150, 140, 120), width=8)
    for k in range(10):
        an = math.radians(-60 + k * 27); r = 135
        x, y = cx + r * math.cos(an), cy + 90 + r * math.sin(an)
        d.ellipse((x - 30, y - 30, x + 30, y + 30), fill=(60, 56, 50))
        ctext(d, x, y - 20, str((k + 1) % 10), fnt(COURB, 34), (230, 226, 214))
    d.ellipse((cx - 55, cy + 35, cx + 55, cy + 145), fill=(230, 222, 200))
    # cable
    pts = [(cx + 330, cy + 150 + 30 * math.sin(k / 3)) for k in range(0)]
    for k in range(40):
        x = cx + 330 + k * 8; y = cy + 160 + k * 14 + 18 * math.sin(k * 1.3)
        d.ellipse((x - 10, y - 10, x + 10, y + 10), outline=(170, 160, 140), width=5)
    base = still(img, 1.0, 1.1, (0.5, 0.5), (0.5, 0.48), luz=(0.5, 0.45, 0.6, 0.5), amb=0.2, tinte=(1.0, 0.95, 0.85))
    return base


def cuenta_atras(desde=10):
    """Cuenta atrás grande con la luz roja."""
    def fn(u, t):
        n = max(0, desde - int(t)); fr = t % 1
        a = np.zeros((AH, W, 3), np.float32) + 0.04
        a = a + _txt(str(n), 0.6, 520, CREMA) * (1 - 0.6 * fr)
        led = lamp(0.5, 0.26, 0.03, 0.017) * np.array([1.3, 0.12, 0.08]) * (fr < 0.5)
        return a + led + lamp(0.5, 0.26, 0.12, 0.07) * np.array([0.3, 0.02, 0.02]) * (fr < 0.5)
    return fn


# ====================================================================== NO CREAS ESTE LIBRO
def sobre():
    """Sobre con sello y siete rayas rojas sobre un escritorio."""
    pw, ph = 1350, 2400
    img = ruido_papel(pw, ph, (46, 30, 20), seed=13, k=12); d = ImageDraw.Draw(img)
    for y in range(0, ph, 90): d.line((0, y, pw, y + 30), fill=(40, 26, 17), width=3)
    sx, sy, sw, sh = 175, 900, 1000, 640
    env = ruido_papel(sw, sh, (214, 190, 150), seed=14, k=7); ed = ImageDraw.Draw(env)
    ed.polygon([(0, 0), (sw / 2, sh * 0.55), (sw, 0)], outline=(170, 146, 108), width=4)
    for k in range(7):
        x = 60 + k * 46; ed.polygon([(x, sh - 40), (x + 26, sh - 40), (x + 96, sh - 200), (x + 70, sh - 200)], fill=ROJO)
    ed.rectangle((sw - 210, 40, sw - 50, 230), fill=(236, 230, 214)); ed.rectangle((sw - 196, 54, sw - 64, 216), fill=(120, 40, 36))
    ed.text((sw - 178, 110), '1978', font=fnt(COURB, 40), fill=(236, 220, 200))
    for k in range(4): ed.arc((sw - 330 + k * 14, 60 + k * 14, sw - 170 - k * 14, 220 - k * 14), 0, 360, fill=(70, 60, 60), width=3)
    ed.ellipse((sw / 2 - 70, sh * 0.55 - 70, sw / 2 + 70, sh * 0.55 + 70), fill=(150, 22, 20))
    ed.ellipse((sw / 2 - 48, sh * 0.55 - 48, sw / 2 + 48, sh * 0.55 + 48), outline=(110, 14, 12), width=6)
    env = env.rotate(-4, expand=True, fillcolor=(0, 0, 0)); m = Image.new('L', (sw, sh), 255).rotate(-4, expand=True, fillcolor=0)
    img.paste(env, (sx, sy), m)
    return still(img, 1.0, 1.1, (0.5, 0.5), (0.5, 0.52), luz=(0.5, 0.52, 0.6, 0.45), amb=0.2, tinte=(1.0, 0.93, 0.82))


def telegrama(lineas=('LLEGO EL MARTES STOP', 'TODO EN ORDEN STOP')):
    """Telegrama de 1978 que se escribe solo."""
    pw, ph = 1350, 2400
    mesa = ruido_papel(pw, ph, (40, 28, 20), seed=15, k=10)
    tw, th = 1150, 900
    paper = ruido_papel(tw, th, (226, 214, 160), seed=16, k=6); d = ImageDraw.Draw(paper)
    ctext(d, tw / 2, 50, 'TELEGRAMA', fnt(ANTON, 96), (60, 50, 40))
    d.line((60, 190, tw - 60, 190), fill=(90, 80, 60), width=4)
    d.text((70, 215), 'FUENSANTA DEL RÍO    1978', font=fnt(COUR, 38), fill=(90, 80, 60))
    d.line((60, 280, tw - 60, 280), fill=(90, 80, 60), width=2)
    f = fnt(COURB, 54); total = sum(len(l) for l in lineas)
    def fn(u, t):
        p = paper.copy(); dd = ImageDraw.Draw(p); k = int(total * min(1, max(0, (t - 0.3) / 2.4))); left = k; y = 340
        for l in lineas:
            s = l[:max(0, min(len(l), left))]; left -= len(l)
            dd.text((80, y), s, font=f, fill=(30, 28, 26)); y += 90
        im = mesa.copy(); im.paste(p.rotate(2, expand=True, fillcolor=(0, 0, 0)), (100, 640), Image.new('L', (tw, th), 255).rotate(2, expand=True, fillcolor=0))
        a = T.arr(T.kenburns(im, u, 1.0, 1.06, (0.5, 0.5), (0.5, 0.5)))
        return a * (0.22 + 0.85 * lamp(0.5, 0.48, 0.65, 0.5))
    return fn


def mentirometro(frases, mentira=None, desde=None):
    """El Mentirómetro: tres frases; si mentira=i, al final se marca cuál era falsa."""
    pw, ph = W, AH
    bg = ruido_papel(pw, ph, (22, 20, 20), seed=17, k=5); d = ImageDraw.Draw(bg)
    ctext(d, pw / 2, ph * 0.075, 'MENTIRÓMETRO', fnt(ANTON, 110), CREMA)
    cx, cy, r = pw / 2, ph * 0.33, 250
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=(40, 38, 36))
    for k in range(11):
        an = math.pi + k * math.pi / 10; col = ROJO if k >= 7 else CREMA
        d.line((cx + (r - 50) * math.cos(an), cy + (r - 50) * math.sin(an), cx + (r - 8) * math.cos(an), cy + (r - 8) * math.sin(an)), fill=col, width=8)
    d.text((cx - r, cy + 16), 'VERDAD', font=fnt(BEBAS, 46), fill=CREMA)
    tw = d.textlength('MENTIRA', font=fnt(BEBAS, 46)); d.text((cx + r - tw, cy + 16), 'MENTIRA', font=fnt(BEBAS, 46), fill=ROJO)
    fcard = fnt(COURB, 46); fl = fnt(ANTON, 80); boxes = []
    import series as S
    for i, fr in enumerate(frases):
        y = ph * (0.47 + i * 0.165); lines = S.wrap(fr, COURB, 46, 540)
        boxes.append((y, lines))
    def card(red, i):
        im = bg.copy(); dd = ImageDraw.Draw(im)
        for j, (y, lines) in enumerate(boxes):
            hot = red and j == mentira; ok = red and j != mentira
            dd.rounded_rectangle((70, y, pw - 70, y + 260), radius=22, fill=(150, 26, 22) if hot else (236, 230, 218),
                                 outline=ROJO, width=6)
            dd.text((110, y + 70), 'ABC'[j], font=fl, fill=(236, 230, 218) if hot else ROJO)
            ty = y + 130 - len(lines) * 27
            for l in lines:
                dd.text((230, ty), l, font=fcard, fill=(250, 246, 240) if hot else (30, 28, 26)); ty += 54
            if hot:
                dd.text((pw - 270, y + 95), 'MENTIRA', font=fnt(ANTON, 50), fill=CREMA)
            if ok:
                dd.text((pw - 250, y + 100), 'VERDAD', font=fnt(BEBAS, 50), fill=(70, 120, 70))
        return T.arr(im)
    A0 = card(False, 0); A1 = card(True, 0) if mentira is not None else A0
    def fn(u, t):
        dur_rev = desde if desde is not None else 1e9
        k = T.ease((t - dur_rev) / 0.4) if mentira is not None else 0
        a = A0 * (1 - k) + A1 * k
        # aguja
        wob = 0.5 + 0.38 * math.sin(t * 2.3) * math.cos(t * 0.9)
        if k > 0: wob = wob * (1 - k) + 0.93 * k
        an = math.pi + wob * math.pi
        x1, y1 = cx + (r - 60) * math.cos(an), cy + (r - 60) * math.sin(an)
        n = 40; xs = np.linspace(cx, x1, n); ys = np.linspace(cy, y1, n)
        for x, y in zip(xs[::2], ys[::2]):
            x, y = int(x), int(y); a[max(0, y - 6):y + 6, max(0, x - 6):x + 6] = np.array([0.85, 0.12, 0.1])
        a[int(cy) - 16:int(cy) + 16, int(cx) - 16:int(cx) + 16] = 0.85
        return a * (0.45 + 0.6 * lamp(0.5, 0.5, 0.9, 0.9))
    return fn


def rayas(n=7, desde=0.4, ritmo=0.35):
    """Cuenta de rayas a lápiz, de cinco en cinco."""
    paper = ruido_papel(W, AH, (230, 224, 210), seed=18, k=7)
    rng = np.random.default_rng(1)
    jit = rng.normal(0, 6, (40, 4))
    def fn(u, t):
        im = paper.copy(); d = ImageDraw.Draw(im); k = min(n, int(max(0, t - desde) / ritmo) + (1 if t > desde else 0))
        x0, y0 = W * 0.2, AH * 0.6
        for i in range(k):
            g, j = divmod(i, 5); gx = x0 + (g % 3) * 260; gy = y0 + (g // 3) * 300
            if j < 4:
                x = gx + j * 46; d.line((x + jit[i, 0], gy + jit[i, 1], x + jit[i, 2], gy + 220 + jit[i, 3]), fill=(50, 48, 52), width=12)
            else:
                d.line((gx - 30, gy + 170, gx + 190, gy + 40), fill=ROJO, width=12)
        return T.arr(im) * (0.3 + 0.75 * lamp(0.5, 0.65, 0.8, 0.6))
    return fn


def pueblo():
    """Fuensanta del Río de noche: torre de la iglesia con el reloj y la fuente de la plaza."""
    rng = np.random.default_rng(21)
    sky = (np.array([0.05, 0.06, 0.1]) * (1.3 - NY[..., None]) + 0.01).astype(np.float32)
    for _ in range(220):
        x, y = rng.integers(0, W), rng.integers(0, int(AH * 0.45)); sky[y:y + 2, x:x + 2] += rng.uniform(0.3, 0.8)
    img = Image.fromarray((np.clip(sky, 0, 1) * 255).astype(np.uint8)); d = ImageDraw.Draw(img)
    d.polygon([(0, AH * 0.5), (300, AH * 0.42), (620, AH * 0.47), (W, AH * 0.40), (W, AH), (0, AH)], fill=(14, 16, 22))
    # casas
    for k in range(9):
        x = k * 130 - 20 + rng.integers(-15, 15); hh = rng.integers(160, 300); y = AH * 0.66 - hh
        d.rectangle((x, y, x + 140, AH * 0.7), fill=(26, 24, 26)); d.polygon([(x - 10, y), (x + 70, y - 60), (x + 150, y)], fill=(34, 24, 22))
        for _ in range(2):
            if rng.random() < 0.55:
                wx = x + rng.integers(20, 90); wy = y + rng.integers(30, hh - 60); d.rectangle((wx, wy, wx + 30, wy + 40), fill=(230, 170, 80))
    # iglesia y reloj
    tx = int(W * 0.56); d.rectangle((tx - 90, AH * 0.28, tx + 90, AH * 0.7), fill=(38, 34, 34))
    d.polygon([(tx - 105, AH * 0.28), (tx, AH * 0.2), (tx + 105, AH * 0.28)], fill=(30, 26, 26))
    ccx, ccy = tx, AH * 0.34; R = 60
    d.ellipse((ccx - R, ccy - R, ccx + R, ccy + R), fill=(214, 204, 176))
    for k in range(12):
        an = k / 12 * 2 * math.pi; d.line((ccx + math.sin(an) * (R - 14), ccy - math.cos(an) * (R - 14), ccx + math.sin(an) * (R - 4), ccy - math.cos(an) * (R - 4)), fill=(40, 40, 40), width=4)
    for fr, L, wdt in (((4 + 10 / 60) / 12, 32, 9), (10 / 60, 48, 6)):
        an = fr * 2 * math.pi; d.line((ccx, ccy, ccx + math.sin(an) * L, ccy - math.cos(an) * L), fill=(20, 20, 20), width=wdt)
    # plaza y fuente
    d.rectangle((0, AH * 0.7, W, AH), fill=(30, 27, 26))
    fx, fy = W / 2, AH * 0.83
    d.ellipse((fx - 300, fy - 40, fx + 300, fy + 80), fill=(70, 66, 62)); d.ellipse((fx - 270, fy - 30, fx + 270, fy + 50), fill=(20, 30, 44))
    d.rectangle((fx - 22, fy - 230, fx + 22, fy), fill=(80, 76, 70)); d.ellipse((fx - 80, fy - 250, fx + 80, fy - 205), fill=(86, 82, 76))
    base = T.arr(img)
    glow = lamp(0.56, 0.34, 0.08, 0.05) * np.array([0.35, 0.28, 0.16])
    lampp = lamp(0.5, 0.78, 0.5, 0.25) * np.array([0.35, 0.24, 0.1])
    water = ((NY > 0.81) & (NY < 0.86) & (np.abs(NX - 0.5) < 0.24))[..., None].astype(np.float32)
    ph = rng.random((AH, W, 1)).astype(np.float32) * 6.28
    def fn(u, t):
        sp = water * (0.5 + 0.5 * np.sin(ph + t * 5)) ** 8 * 0.6
        return np.clip(base * (1 + lampp * 2) + glow + sp, 0, 1)
    return fn


def anuncio(lineas=('AGUA DE', 'FUENSANTA')):
    """Anuncio de periódico de 1978 con una botella dibujada."""
    pw, ph = 1350, 2400
    mesa = ruido_papel(pw, ph, (34, 26, 20), seed=23, k=9)
    aw, ah = 1050, 1500
    p = ruido_papel(aw, ah, (222, 212, 186), seed=24, k=8); d = ImageDraw.Draw(p)
    d.rectangle((24, 24, aw - 24, ah - 24), outline=(40, 36, 32), width=8)
    y = 70
    for l in lineas:
        ctext(d, aw / 2, y, l, fnt(ANTON, 150), (30, 28, 26)); y += 190
    bx, by = aw / 2, y + 140
    d.rounded_rectangle((bx - 90, by + 120, bx + 90, by + 560), radius=40, outline=(40, 36, 32), width=10)
    d.rectangle((bx - 36, by, bx + 36, by + 130), outline=(40, 36, 32), width=10)
    d.rectangle((bx - 90, by + 300, bx + 90, by + 420), fill=ROJO)
    ctext(d, bx, by + 318, 'S. A.', fnt(ANTON, 70), (236, 230, 218))
    for k in range(6):
        d.arc((bx - 260 - k * 30, by + 200 - k * 30, bx + 260 + k * 30, by + 660 + k * 30), 200, 340, fill=(140, 130, 112), width=3)
    d.text((80, ah - 200), 'Análisis de laboratorio a disposición', font=fnt(COUR, 40), fill=(50, 46, 40))
    d.text((80, ah - 140), 'del público. Plazas limitadas.', font=fnt(COUR, 40), fill=(50, 46, 40))
    im = mesa.copy(); im.paste(p.rotate(-3, expand=True, fillcolor=(0, 0, 0)), (130, 480), Image.new('L', (aw, ah), 255).rotate(-3, expand=True, fillcolor=0))
    return still(im, 1.0, 1.08, (0.5, 0.5), (0.5, 0.45), luz=(0.5, 0.5, 0.65, 0.6), amb=0.2, tinte=(1.0, 0.94, 0.84))


# ====================================================================== registro
FONDOS = dict(faro=faro, pagina=pagina, tipos=tipos, numeros=numeros, palabras=palabras, llave_carta=llave_carta,
              cubierta=lambda *a, **k: cubierta(*a, **k), camara=camara, foto=foto, telefono=telefono, cuenta_atras=cuenta_atras,
              sobre=sobre, telegrama=telegrama, mentirometro=mentirometro, rayas=rayas, pueblo=pueblo, anuncio=anuncio)


def fondo(spec):
    """'faro' | {"foto": {"anio":1993, "cambio":"estrella"}} | {"numeros": 7} | {"palabras": [...]}"""
    if isinstance(spec, str): return FONDOS[spec]()
    (k, v), = spec.items()
    if isinstance(v, dict): return FONDOS[k](**v)
    return FONDOS[k](v)


def es_fondo(spec):
    if isinstance(spec, str): return spec in FONDOS
    return isinstance(spec, dict) and len(spec) == 1 and next(iter(spec)) in FONDOS


# ====================================================================== cierres
def _enc(path, dur, fn):
    n = round(dur * FPS); tmp = path + '.part.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{T.H}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast',
                          '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS; u = i / max(1, n - 1)
        p.stdin.write(T.out_frame(fn(u, t), i, T.fades(t, dur, 0.35, 0.35)).tobytes())
    p.stdin.close()
    if p.wait() != 0: raise SystemExit('ffmpeg falló ' + path)
    os.replace(tmp, path)


def _capa(draw):
    img = Image.new('RGBA', (W, AH), (0, 0, 0, 0)); draw(ImageDraw.Draw(img))
    a = np.asarray(img).astype(np.float32) / 255
    return a[..., :3], a[..., 3:4]


def _libro_en_mesa(libro, alto=1400, yc=0.45, pie=True):
    """La cubierta real del libro sobre fondo oscuro, con sombra."""
    L = LIBROS[libro]; pw, ph = 1350, 2400; k = pw / W
    img = ruido_papel(pw, ph, (16, 15, 15), seed=4, k=5)
    cov = Image.open(os.path.join(T.A_, 'cubiertas', f'{libro}.jpg')).convert('RGB')
    h = int(alto * k); w = int(h * cov.width / cov.height); cov = cov.resize((w, h), Image.LANCZOS)
    x0 = (pw - w) // 2; y0 = int(ph * yc - h / 2)
    sh = Image.new('L', (pw, ph), 0); ImageDraw.Draw(sh).rectangle((x0 + 20, y0 + 30, x0 + w + 20, y0 + h + 30), fill=200)
    img = Image.composite(Image.new('RGB', img.size, (0, 0, 0)), img, sh.filter(ImageFilter.GaussianBlur(40)))
    img.paste(cov, (x0, y0))
    if pie:
        d = ImageDraw.Draw(img)
        ctext(d, pw / 2, y0 + h + 70, 'Colección Libros prohibidos · Teo Larrea', fnt(PAGI, 50), (190, 184, 176))
    return img


def cubierta(libro='abras', sub=True):
    """La cubierta real del libro, con un empuje lento de cámara."""
    return still(_libro_en_mesa(libro, 1380, 0.5, pie=False), 1.0, 1.06, (0.5, 0.5), (0.5, 0.5), luz=(0.5, 0.5, 0.9, 0.8), amb=0.55)


def escena_titulo(libro):
    img = _libro_en_mesa(libro)
    def fn(u, t):
        a = T.arr(T.kenburns(img, u, 1.0, 1.07, (0.5, 0.47), (0.5, 0.46)))
        return a * (0.6 + 0.45 * lamp(0.5, 0.45, 0.8, 0.7))
    return fn


def escena_cta(libro):
    L = LIBROS[libro]; B = T.arr(ruido_papel(W, AH, (14, 13, 13), seed=6, k=4))
    def draw(d):
        ctext(d, W / 2, AH * 0.31, 'ENLACE EN LA BIO', fnt(ANTON, 128), CREMA)
        d.rectangle((W / 2 - 160, AH * 0.41, W / 2 + 160, AH * 0.41 + 8), fill=ROJO)
        ctext(d, W / 2, AH * 0.445, 'KINDLE Y TAPA BLANDA', fnt(BEBAS, 78), (226, 222, 214))
        ctext(d, W / 2, AH * 0.49, 'EN AMAZON', fnt(BEBAS, 78), (226, 222, 214))
        ctext(d, W / 2, AH * 0.56, 'Gratis con Kindle Unlimited', fnt(PAGI, 54), (236, 120, 110))
        ctext(d, W / 2, AH * 0.64, 'o búscalo en Amazon:', fnt(PAGI, 46), (190, 186, 180))
        ctext(d, W / 2, AH * 0.67, f'«{L["titulo"]}»', fnt(PAGI, 46), (190, 186, 180))
    c = _capa(draw)
    def fn(u, t):
        k = T.ease((t - 0.1) / 0.4); return B * (1 - c[1] * k) + c[0] * c[1] * k
    return fn


def asegurar_cierres(libro):
    os.makedirs(ESC, exist_ok=True)
    a, b = os.path.join(ESC, f'{libro}_titulo.mp4'), os.path.join(ESC, f'{libro}_cta.mp4')
    if not os.path.exists(a): _enc(a, 5.0, escena_titulo(libro))
    if not os.path.exists(b): _enc(b, 4.0, escena_cta(libro))
    return [os.path.join(ESC, 'a20.mp4'), a, b]


# ====================================================================== portada
def portada(idea, path):
    import series as S
    libro = idea['libro']; L = LIBROS[libro]
    fn = fondo(idea['portada']) if es_fondo(idea['portada']) else None
    a = np.clip(fn(0.7, 2.6) * T.VIG * 1.05, 0, 1)
    arr = (a * 255).astype(np.float32)
    yy = np.linspace(0, 1, AH)[:, None, None]
    arr *= (1 - 0.6 * np.exp(-((yy - 0.3) / 0.17) ** 2))
    img = Image.fromarray(arr.clip(0, 255).astype(np.uint8)); d = ImageDraw.Draw(img)
    def ct(y, t, f, fill):
        w = d.textlength(t, font=f); x = (W - w) / 2
        for dx, dy in [(0, 6), (4, 6), (-4, 6), (0, 10)]: d.text((x + dx, y + dy), t, font=f, fill=(0, 0, 0))
        d.text((x, y), t, font=f, fill=fill)
    # etiqueta del libro
    lab = f'NO {L["verbo"]} ESTE LIBRO'; fl = fnt(ANTON, 52); wl = d.textlength(lab, font=fl)
    d.rectangle(((W - wl) / 2 - 30, 128, (W + wl) / 2 + 30, 212), fill=ROJO); d.text(((W - wl) / 2, 132), lab, font=fl, fill=CREMA)
    size = 120; lines = S.wrap(idea['gancho'], ANTON, size, 920)
    while len(lines) > 4:
        size -= 10; lines = S.wrap(idea['gancho'], ANTON, size, 920)
    f = fnt(ANTON, size); y = 560 - len(lines) * size * 0.62
    red = {r.strip('.,:;¿?¡!«»').upper() for r in idea.get('rojo', [])}
    for l in lines:
        hot = any(w.strip('.,:;¿?¡!«»').upper() in red for w in l.split())
        ct(y, l, f, (236, 80, 72) if hot and len(l.split()) <= 2 else (246, 244, 240)); y += size * 1.2
    fb = fnt(ANTON, 72); t = 'ENLACE EN LA BIO'
    w = d.textlength(t, font=fb); x0 = (W - w) / 2 - 50; yb = 1600
    d.rounded_rectangle((x0, yb, x0 + w + 100, yb + 120), radius=18, fill=ROJO)
    d.text((x0 + 50, yb + 12), t, font=fb, fill=(255, 255, 255))
    ct(yb + 150, 'Kindle y tapa blanda · Gratis con Kindle Unlimited', fnt(PAGI, 38), (226, 222, 214))
    img.convert('RGB').save(path, quality=90)
