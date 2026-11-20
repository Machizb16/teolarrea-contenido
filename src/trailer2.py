"""Tráiler v2 de «Nadie se va del todo»: más variedad de planos. ORIENT=h (16:9) o v (9:16)."""
import os, sys, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ORIENT = os.environ.get('ORIENT', 'h')
if ORIENT == 'h':
    W, H, BAR = 1920, 1080, 138
else:
    W, H, BAR = 1080, 1920, 0
AH = H - 2 * BAR
FPS = 30
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A_ = os.path.join(ROOT, 'assets')
FNT = os.path.join(A_, 'fuentes')
OUT = os.path.join(os.environ.get('TRABAJO', '/tmp/teolarrea'), f'out_{ORIENT}')
BEBAS = os.path.join(FNT, 'BebasNeue-Bold.otf')
COUR = os.path.join(FNT, 'Courier Prime.otf')
COURB = os.path.join(FNT, 'Courier Prime Bold.otf')
PAGI = os.path.join(FNT, 'texgyrepagella-italic.otf')
HAND = os.path.join(FNT, 'dkg.ttf')
GARAGE = os.path.join(A_, 'garaje.png')
WALTER = os.path.join(A_, 'walter.png')
CUB = A_ + '/'
BOC = os.path.join(A_, 'bocetos') + '/'
rng = np.random.default_rng(11)
GRAIN = [rng.normal(0, 9, (AH, W, 1)).astype(np.int16) for _ in range(6)]
YY, XX = np.mgrid[0:AH, 0:W].astype(np.float32)
NX, NY = XX / W, YY / AH          # coordenadas normalizadas


def ease(x):
    x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)


def grade(im, k=1.0):
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255
    lum = a.mean(axis=2, keepdims=True)
    a = a * 0.35 + lum * np.array([0.62, 0.78, 0.92]) * 0.65
    return Image.fromarray((np.clip(a * k, 0, 1) * 255).astype(np.uint8))


def kenburns(src, t, z0, z1, c0, c1):
    z = z0 + (z1 - z0) * ease(t)
    cx = c0[0] + (c1[0] - c0[0]) * ease(t); cy = c0[1] + (c1[1] - c0[1]) * ease(t)
    s = max(W / src.width, AH / src.height) * z
    cw, ch = W / s, AH / s
    x0 = np.clip(cx * src.width - cw / 2, 0, src.width - cw)
    y0 = np.clip(cy * src.height - ch / 2, 0, src.height - ch)
    return src.transform((W, AH), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)


def arr(im): return np.asarray(im.convert('RGB')).astype(np.float32) / 255


VIG = np.clip(1.12 - (np.sqrt(((XX - W / 2) / (W * 0.6)) ** 2 + ((YY - AH / 2) / (AH * 0.75)) ** 2)) ** 2 * 0.65, 0.15, 1)[..., None]


def out_frame(a, fi, fade=1.0):
    a = np.clip(a * VIG * fade, 0, 1)
    o = np.zeros((H, W, 3), np.int16)
    o[BAR:BAR + AH] = (a * 255).astype(np.int16) + GRAIN[fi % 6]
    return np.clip(o, 0, 255).astype(np.uint8)


class Enc:
    def __init__(self, name):
        os.makedirs(OUT, exist_ok=True)
        self.tmp = f'{OUT}/{name}.part.mp4'; self.name = f'{OUT}/{name}.mp4'
        self.p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                                   '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast',
                                   '-pix_fmt', 'yuv420p', self.tmp], stdin=subprocess.PIPE)

    def write(self, f): self.p.stdin.write(f.tobytes())

    def close(self):
        self.p.stdin.close()
        if self.p.wait() == 0: os.replace(self.tmp, self.name)
        else: raise SystemExit('ffmpeg falló ' + self.name)


def fades(t, dur, fi=0.4, fo=0.4):
    return min(1.0, t / fi if fi else 1, (dur - t) / fo if fo else 1)


def scene(name, dur, fn, fi=0.4, fo=0.4):
    n = round(dur * FPS); e = Enc(name)
    for i in range(n):
        t = i / FPS; u = i / max(1, n - 1)
        e.write(out_frame(fn(u, t), i, fades(t, dur, fi, fo)))
    e.close()


def small_to_full(m):
    return np.asarray(Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8)).resize((W, AH), Image.BILINEAR)).astype(np.float32)[..., None] / 255


# ------------------------------------------------------------------ texto
def text_layer(lines, font, size, color=(232, 236, 239), spacing=0, gap=1.05, dy=0):
    f = ImageFont.truetype(font, size)
    img = Image.new('RGBA', (W, AH), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    lh = size * gap; y = (AH - lh * len(lines)) / 2 + size * 0.08 + dy
    for l in lines:
        wd = sum(d.textlength(c, font=f) for c in l) + spacing * max(0, len(l) - 1); x = (W - wd) / 2
        for c in l:
            d.text((x, y), c, font=f, fill=color + (255,)); x += d.textlength(c, font=f) + spacing
        y += lh
    a = np.asarray(img).astype(np.float32) / 255
    return a[..., :3] * a[..., 3:4]


def s_card(name, dur, lines_h, lines_v, size_h=104, size_v=112):
    lines, size = (lines_h, size_h) if ORIENT == 'h' else (lines_v, size_v)
    base = Image.fromarray((text_layer(lines, BEBAS, size, spacing=6) * 255).astype(np.uint8))
    scene(name, dur, lambda u, t: arr(kenburns(base, u, 1.0, 1.035, (0.5, 0.5), (0.5, 0.5))), 0.45, 0.45)


def s_type(name, dur, text):
    f = ImageFont.truetype(COUR, 60 if ORIENT == 'h' else 64)
    def fn(u, t):
        k = int(min(len(text), max(0, (t - 0.5) / 0.09)))
        img = Image.new('RGB', (W, AH)); d = ImageDraw.Draw(img)
        x = (W - d.textlength(text, font=f)) / 2
        d.text((x, AH / 2 - 34), text[:k], font=f, fill=(215, 220, 224))
        if int(t * 2.2) % 2 == 0:
            cx = x + d.textlength(text[:k], font=f); d.rectangle((cx + 5, AH / 2 - 28, cx + 34, AH / 2 + 30), fill=(215, 220, 224))
        return arr(img)
    scene(name, dur, fn, 0.01, 0.5)


# ------------------------------------------------------------------ planos fotográficos
def s_shot(name, dur, src, z0, z1, c0, c1, k=1.0, flicker=False):
    def fn(u, t):
        a = arr(kenburns(src, u, z0, z1, c0, c1)) * k
        if flicker: a *= 1.0 - 0.5 * max(0, np.sin(t * 23.0) * np.sin(t * 7.3) - 0.55)
        return a
    scene(name, dur, fn)


# ------------------------------------------------------------------ planos generados
def wall_texture(seed=1, tint=(0.55, 0.5, 0.45)):
    r = np.random.default_rng(seed)
    n = Image.fromarray((r.random((AH // 8, W // 8)) * 255).astype(np.uint8)).resize((W, AH), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    return (0.6 + 0.4 * np.asarray(n).astype(np.float32)[..., None] / 255) * np.array(tint)


def s_headlights(name, dur):
    wall = wall_texture(3)
    def fn(u, t):
        pos = -0.4 + 1.8 * ease(u * 1.1)                # el foco cruza de izquierda a derecha
        sk = NY * 0.35
        slats = 0.5 + 0.5 * np.sign(np.sin((NY * (14 if ORIENT == 'h' else 22) + (NX - pos) * 0.8) * np.pi))
        spot = np.exp(-(((NX - pos - sk * 0.2) / 0.2) ** 2)) * np.exp(-(((NY - 0.45) / 0.55) ** 2))
        light = slats * spot * (0.85 + 0.15 * np.sin(t * 40))
        a = wall * (0.035 + light[..., None] * 0.75) * np.array([0.9, 0.95, 1.05])
        return a
    scene(name, dur, fn, 0.3, 0.4)


def make_dossier():
    pw, ph = 1700, 2200
    img = Image.new('RGB', (pw, ph), (226, 219, 200)); d = ImageDraw.Draw(img)
    r = np.random.default_rng(4)
    stain = (r.random((ph // 40, pw // 40)) * 255).astype(np.uint8)
    st = np.asarray(Image.fromarray(stain).resize((pw, ph), Image.BICUBIC).filter(ImageFilter.GaussianBlur(30))).astype(np.float32)[..., None] / 255
    img = Image.fromarray(np.clip(np.asarray(img) * (0.9 + 0.1 * st), 0, 255).astype(np.uint8)); d = ImageDraw.Draw(img)
    fC, fCB, fH = ImageFont.truetype(COUR, 44), ImageFont.truetype(COURB, 52), ImageFont.truetype(HAND, 92)
    d.text((pw / 2, 170), 'SECRECY AGREEMENT', font=fCB, fill=(30, 30, 32), anchor='mm')
    d.text((pw / 2, 240), 'PROJECT: ', font=fC, fill=(30, 30, 32), anchor='rm')
    d.rectangle((pw / 2 + 5, 215, pw / 2 + 420, 265), fill=(18, 18, 20))
    y = 380
    lines = ['I, the undersigned, hereby acknowledge that', 'I will never divulge, publish or reveal', 'by any means any information concerning',
             'the activities described in Section 2,', 'for the rest of my life.', '', 'Unauthorized disclosure may result in',
             'serious "consequences".']
    for l in lines:
        d.text((180, y), l, font=fC, fill=(35, 35, 38)); y += 70
    for (x0, x1, yy) in [(180, 980, y + 40), (1040, 1520, y + 40), (180, 760, y + 110), (180, 1400, y + 180)]:
        d.rectangle((x0, yy, x1, yy + 48), fill=(16, 16, 18))
    d.text((180, ph - 520), 'Signature:', font=fC, fill=(35, 35, 38))
    d.line((470, ph - 470, 1250, ph - 470), fill=(60, 60, 64), width=3)
    d.text((500, ph - 600), 'Walter J. Hayes', font=fH, fill=(25, 40, 95))
    d.text((180, ph - 380), 'Date:  April, 1963', font=fC, fill=(35, 35, 38))
    stamp = Image.new('RGBA', (900, 220), (0, 0, 0, 0)); sd = ImageDraw.Draw(stamp)
    sd.rectangle((8, 8, 892, 212), outline=(170, 30, 34, 230), width=12)
    sd.text((450, 112), 'CLASSIFIED', font=ImageFont.truetype(COURB, 130), fill=(170, 30, 34, 230), anchor='mm')
    stamp = stamp.rotate(-14, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (pw - stamp.width - 60, 380 + 70 * 4), stamp)
    img = img.rotate(2.5, expand=True, fillcolor=(8, 8, 10), resample=Image.BICUBIC)
    a = np.asarray(img).astype(np.float32) / 255 * np.array([1.0, 0.92, 0.78])
    canvas = np.zeros((round(img.height * 1.1), round(img.width * 1.35), 3), np.float32) + 0.025
    oy, ox = (canvas.shape[0] - img.height) // 2, (canvas.shape[1] - img.width) // 2
    canvas[oy:oy + img.height, ox:ox + img.width] = a
    return Image.fromarray((canvas * 255).astype(np.uint8))


def s_dossier(name, dur):
    src = make_dossier()
    if ORIENT == 'h': c0, c1, z0, z1 = (0.5, 0.25), (0.5, 0.68), 1.0, 1.15
    else: c0, c1, z0, z1 = (0.5, 0.3), (0.5, 0.62), 1.0, 1.12
    def fn(u, t):
        a = arr(kenburns(src, u, z0, z1, c0, c1))
        lamp = np.exp(-(((NX - 0.45) / 0.55) ** 2 + ((NY - 0.45) / 0.7) ** 2))
        return a * (0.15 + 0.95 * lamp[..., None])
    scene(name, dur, fn)


def mountains(seed, base, amp, n=W):
    r = np.random.default_rng(seed); x = np.linspace(0, 1, n)
    y = np.zeros(n)
    for k, a in [(2, 1), (5, 0.45), (11, 0.22), (29, 0.08), (67, 0.03)]:
        y += a * np.sin(2 * np.pi * (k * x + r.random()))
    y = (y - y.min()) / (y.max() - y.min())
    return base - amp * y


def night_desert(seed, pan_px=0):
    r = np.random.default_rng(seed)
    sky = np.zeros((AH, W, 3), np.float32)
    g = np.clip(NY / 0.62, 0, 1)[..., None]
    sky += (1 - g) * np.array([0.01, 0.015, 0.035]) + g * np.array([0.04, 0.06, 0.11])
    stars = np.zeros((AH, W), np.float32)
    ns = int(W * AH / 1500)
    sx, sy = r.integers(0, W, ns), r.integers(0, int(AH * 0.6), ns)
    stars[sy, sx] = r.random(ns) ** 3
    stars = np.asarray(Image.fromarray((stars * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 255 * 2.5
    sky += stars[..., None] * np.array([0.8, 0.85, 1.0])
    horizon = 0.62
    m_far = mountains(seed + 1, horizon * AH, AH * 0.12)
    m_near = mountains(seed + 2, horizon * AH + AH * 0.01, AH * 0.07)
    mf = (YY > m_far[None, :]); mn = (YY > m_near[None, :])
    sky[mf] = np.array([0.018, 0.024, 0.04]); sky[mn] = np.array([0.008, 0.01, 0.016])
    lake = YY > horizon * AH + AH * 0.03
    lake_col = np.array([0.05, 0.06, 0.08]) * (0.6 + 0.4 * (1 - (NY - horizon) / (1 - horizon)))[..., None]
    sky[lake] = lake_col[lake]
    glow = np.exp(-((NY - horizon) / 0.12) ** 2)[..., None] * np.array([0.05, 0.06, 0.09])
    sky = sky * 1.7 + glow
    return sky, horizon


def s_desert(name, dur):
    base, hz = night_desert(21)
    lights_x = np.linspace(0.18, 0.58, 14)
    def fn(u, t):
        a = base.copy()
        for k, lx in enumerate(lights_x):
            on = 0.6 + 0.4 * np.sin(t * 3 + k)
            gx, gy = lx * W, (hz + 0.07 + k * 0.004) * AH
            a += np.exp(-(((XX - gx) / 2.5) ** 2 + ((YY - gy) / 2.5) ** 2))[..., None] * np.array([1.0, 0.75, 0.4]) * 0.9 * on
        beacon = 0.5 + 0.5 * np.sign(np.sin(t * 2.4))
        a += np.exp(-(((XX - 0.72 * W) / 4) ** 2 + ((YY - (hz + 0.055) * AH) / 4) ** 2))[..., None] * np.array([1, 0.2, 0.2]) * beacon
        img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
        return arr(kenburns(img, u, 1.02, 1.12, (0.45, 0.55), (0.55, 0.55)))
    scene(name, dur, fn, 0.6, 0.5)


def s_lights(name, dur):
    base, hz = night_desert(33)
    P = np.array([(0.15, 0.30), (0.40, 0.30), (0.40, 0.14), (0.62, 0.14), (0.62, 0.40), (0.80, 0.40), (0.80, 0.05)])
    T = np.array([0.0, 0.9, 1.4, 2.3, 2.8, 3.5, 3.9])
    def pos(t, delay):
        tt = np.clip(t - delay, 0, T[-1])
        j = min(len(T) - 2, np.searchsorted(T, tt, side='right') - 1)
        f = (tt - T[j]) / (T[j + 1] - T[j]); f = 0 if f < 0.35 else ease((f - 0.35) / 0.3)   # parada en seco y salto
        return P[j] * (1 - f) + P[j + 1] * f
    def fn(u, t):
        a = base.copy()
        for k, delay in enumerate([0.0, 0.5, 0.95]):
            if t < delay: continue
            x, y = pos(t, delay); x = x * (1 if ORIENT == 'h' else 0.9) + (0 if ORIENT == 'h' else 0.05)
            gx, gy = x * W, (y * hz + 0.06 * k * hz) * AH
            d2 = ((XX - gx) ** 2 + (YY - gy) ** 2)
            a += (np.exp(-d2 / 30) * 1.4 + np.exp(-d2 / 900) * 0.25)[..., None] * np.array([0.8, 0.92, 1.0])
        return a
    scene(name, dur, fn, 0.5, 0.5)


def s_notebook(name, dur, lines):
    pw, ph = (2400, 1350) if ORIENT == 'h' else (1350, 2400)
    paper = Image.new('RGB', (pw, ph), (240, 236, 224)); d = ImageDraw.Draw(paper)
    for x in range(0, pw, 46): d.line((x, 0, x, ph), fill=(205, 212, 222), width=2)
    for y in range(0, ph, 46): d.line((0, y, pw, y), fill=(205, 212, 222), width=2)
    f = ImageFont.truetype(HAND, 120 if ORIENT == 'h' else 104)
    total = sum(len(l) for l in lines)
    y0 = ph * (0.36 if ORIENT == 'h' else 0.4)
    def fn(u, t):
        k = int(total * min(1, max(0, (t - 0.4) / (dur * 0.62))))
        im = paper.copy(); dd = ImageDraw.Draw(im); y = y0; left = k
        for l in lines:
            s = l[:max(0, min(len(l), left))]; left -= len(l)
            dd.text((pw * 0.16, y), s, font=f, fill=(55, 55, 60)); y += 170
        a = arr(kenburns(im, u, 1.03, 1.13, (0.5, 0.5), (0.52, 0.5)))
        lamp = np.exp(-(((NX - 0.5) / 0.6) ** 2 + ((NY - 0.5) / 0.75) ** 2))
        return a * np.array([1.0, 0.92, 0.78]) * (0.12 + 0.9 * lamp[..., None])
    scene(name, dur, fn)


def clock_img(t):
    s = 900; img = Image.new('RGB', (s, s), (10, 10, 12)); d = ImageDraw.Draw(img)
    c = s / 2
    d.ellipse((60, 60, s - 60, s - 60), fill=(205, 200, 185), outline=(40, 40, 40), width=18)
    for k in range(60):
        ang = k / 60 * 2 * np.pi; r0 = c - 95 if k % 5 == 0 else c - 80
        d.line((c + np.sin(ang) * r0, c - np.cos(ang) * r0, c + np.sin(ang) * (c - 70), c - np.cos(ang) * (c - 70)), fill=(30, 30, 30), width=8 if k % 5 == 0 else 3)
    def hand(frac, L, wdt, col):
        ang = frac * 2 * np.pi; d.line((c, c, c + np.sin(ang) * L, c - np.cos(ang) * L), fill=col, width=wdt)
    sec = 40 + int(t)               # 2:40 y unos segundos
    hand((2 + 40 / 60) / 12, 200, 22, (20, 20, 20)); hand(40 / 60, 300, 14, (20, 20, 20)); hand(sec / 60, 330, 4, (150, 20, 20))
    d.ellipse((c - 18, c - 18, c + 18, c + 18), fill=(20, 20, 20))
    return grade(img, 0.75)


# ------------------------------------------------------------------ bocetos con linterna
def make_paper(n, rot):
    b = Image.open(f'{BOC}boceto{n}.png').convert('RGB')
    target_w = W * 0.98 if ORIENT == 'h' else W * 1.25
    s = min(target_w / b.width, AH * 1.05 / b.height) if ORIENT == 'h' else target_w / b.width
    b = b.resize((round(b.width * s), round(b.height * s)), Image.LANCZOS).convert('RGBA').rotate(rot, expand=True, resample=Image.BICUBIC)
    cw, ch = max(round(W * 1.15), b.width + 60), max(round(AH * 1.15), b.height + 60)
    canvas = Image.new('RGBA', (cw, ch), (6, 7, 9, 255))
    x, y = (cw - b.width) // 2, (ch - b.height) // 2
    sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 240), (x + 18, y + 26), b.split()[-1])
    canvas = Image.alpha_composite(canvas, sh.filter(ImageFilter.GaussianBlur(22))); canvas.alpha_composite(b, (x, y))
    a = np.asarray(canvas.convert('RGB')).astype(np.float32) / 255 * np.array([1.0, 0.93, 0.80])
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def s_sketch(name, dur, n, rot, path, z0=1.0, z1=1.12, c0=(0.5, 0.5), c1=(0.5, 0.5)):
    src = make_paper(n, rot)
    def fn(u, t):
        a = arr(kenburns(src, u, z0, z1, c0, c1))
        p = np.array(path); k = u * (len(p) - 1); j = min(int(k), len(p) - 2); f = k - j
        px, py = p[j] * (1 - f) + p[j + 1] * f
        jit = np.sin(t * 9) * 0.004 + np.sin(t * 13.7) * 0.003
        rx, ry = (0.2, 0.42) if ORIENT == 'h' else (0.38, 0.24)
        m = np.exp(-(((NX - px - jit) / rx) ** 2 + ((NY - py) / ry) ** 2))
        return a * (0.07 + 1.05 * m[..., None])
    scene(name, dur, fn)


# ------------------------------------------------------------------ montaje y títulos
def s_montage(name, clips):
    total = sum(c[0] for c in clips); n = round(total * FPS); e = Enc(name)
    bounds = np.cumsum([0] + [c[0] for c in clips])
    for i in range(n):
        t = i / FPS; j = min(len(clips) - 1, int(np.searchsorted(bounds, t, side='right') - 1))
        u = (t - bounds[j]) / clips[j][0]
        a = clips[j][1](u, t - bounds[j]) + max(0, 1 - u * 6) * 0.3
        e.write(out_frame(a, i))
    e.close()


def s_title(name, dur):
    big = 190 if ORIENT == 'h' else 205
    f1 = ImageFont.truetype(BEBAS, big)
    img = Image.new('RGBA', (W, AH), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    todo = Image.new('RGBA', (W, AH), (0, 0, 0, 0)); dt = ImageDraw.Draw(todo)
    yc = AH / 2 - big * 0.95
    if ORIENT == 'h':
        d.text(((W - d.textlength('NADIE SE VA', font=f1)) / 2, yc), 'NADIE SE VA', font=f1, fill=(244, 246, 248, 255))
        x2 = (W - d.textlength('DEL TODO', font=f1)) / 2; y2 = yc + big * 0.9
        d.text((x2, y2), 'DEL ', font=f1, fill=(244, 246, 248, 255)); xt = x2 + d.textlength('DEL ', font=f1)
    else:
        for k, l in enumerate(['NADIE', 'SE VA', 'DEL']):
            d.text(((W - d.textlength(l, font=f1)) / 2, yc - big * 0.9 + k * big * 0.9), l, font=f1, fill=(244, 246, 248, 255))
        xt = (W - d.textlength('TODO', font=f1)) / 2; y2 = yc - big * 0.9 + 3 * big * 0.9
    dt.text((xt, y2), 'TODO', font=f1, fill=(205, 222, 238, 255))
    wt = d.textlength('TODO', font=f1)
    A = np.asarray(img).astype(np.float32) / 255; Tt = np.asarray(todo).astype(np.float32) / 255
    grad = np.clip(1 - (XX[..., None] - (xt + wt * 0.15)) / (wt * 1.05), 0.12, 1)
    sub = text_layer(['TEO LARREA'], BEBAS, 48, color=(200, 208, 216), spacing=16, dy=(AH * 0.30 if ORIENT == 'h' else AH * 0.27))
    def fn(u, t):
        ta = ease((t - 0.2) / 1.6); tf = ease((t - 1.4) / 2.5)
        a = A[..., :3] * A[..., 3:4] * ta + Tt[..., :3] * Tt[..., 3:4] * (1 - tf * (1 - grad)) * ta
        return a + sub * ease((t - 2.4) / 1.0)
    scene(name, dur, fn, 0.01, 0.8)


def s_end(name, dur):
    l1 = text_layer(['TAPA BLANDA Y KINDLE · EN AMAZON'] if ORIENT == 'h' else ['TAPA BLANDA Y KINDLE', 'EN AMAZON'],
                    BEBAS, 64 if ORIENT == 'h' else 84, spacing=5, dy=-40)
    l2 = text_layer(['Obra de ficción inspirada en los relatos y leyendas sobre el Área 51.'] if ORIENT == 'h'
                    else ['Obra de ficción inspirada en los relatos', 'y leyendas sobre el Área 51.'],
                    PAGI, 30 if ORIENT == 'h' else 36, color=(150, 158, 166), dy=(110 if ORIENT == 'h' else 190))
    scene(name, dur, lambda u, t: l1 + l2, 0.5, 1.0)


def s_bio(name, dur):
    l1 = text_layer(['ENLACE EN LA BIO'], BEBAS, 150, color=(244, 246, 248), spacing=4, dy=-260)
    l2 = text_layer(['Tapa blanda y Kindle', 'en Amazon'], BEBAS, 72, color=(205, 212, 220), spacing=4, dy=-40)
    l3 = text_layer(['o búscalo en Amazon:', '«Nadie se va del todo»'], PAGI, 44, color=(170, 178, 186), dy=170)
    l4 = text_layer(['Obra de ficción inspirada en los relatos', 'y leyendas sobre el Área 51.'], PAGI, 30, color=(120, 128, 136), dy=330)
    bar = np.zeros((AH, W, 3), np.float32)
    y0 = int(AH / 2 - 260 + 95); bar[y0:y0 + 6, W // 2 - 160:W // 2 + 160] = np.array([0.78, 0.15, 0.17])
    def fn(u, t):
        pulse = 0.85 + 0.15 * np.sin(t * 5)
        return l1 * pulse + l2 + l3 + l4 + bar
    scene(name, dur, fn, 0.3, 0.6)


# ------------------------------------------------------------------ material y guion
def assets():
    g = Image.open(GARAGE).convert('RGB')
    w = Image.open(WALTER).convert('RGB')
    kb = Image.open(CUB + 'fondo_kindle3.png').convert('RGB')
    geo = json.load(open(CUB + 'geo3.json'))['kindle']; sy = round(geo['seam_y'] * 300)
    return dict(
        garage=grade(g, 0.62),
        wl=grade(w.crop((0, 0, 840, 944)), 0.85), wr=grade(w.crop((840, 0, 1680, 944)), 0.7),
        kenn=kb.crop((0, sy - 470, 1800, sy + 283)) if ORIENT == 'h' else kb.crop((200, sy - 900, 1600, sy + 500)),
        ghost=kb.crop((0, 120, 1800, 1500)) if ORIENT == 'h' else kb.crop((150, 80, 1650, 2000)))


V = ORIENT == 'v'
VARIANT = os.environ.get('VARIANT', 'full')


def timeline():
    if not V:
        return [('a01', 3.2), ('a02', 3.6), ('a03', 3.4), ('a04', 3.0), ('a05', 4.6), ('a06', 4.4), ('a07', 3.0), ('a08', 4.6),
                ('a09', 3.8), ('a10', 3.8), ('a11', 3.2), ('a12', 4.8), ('a13', 3.8), ('a14', 3.0), ('a15', 4.4), ('a16', 4.2),
                ('a17', 3.2), ('a18', 4.0), ('a19', 4.6), ('a20', 1.0), ('a21', 6.0), ('a22', 4.5)]
    if VARIANT == 't1':
        return [('c01', 2.2), ('a05', 3.4), ('a06', 3.2), ('c02', 2.6), ('a15', 3.4), ('a17', 2.6), ('a20', 0.8), ('a21', 5.0), ('b22', 4.0)]
    if VARIANT == 't2':
        return [('c03', 2.4), ('a08', 3.4), ('a12', 3.8), ('c04', 2.4), ('a09', 3.4), ('a18', 3.0), ('c05', 2.6), ('a20', 0.8), ('a21', 5.0), ('b22', 4.0)]
    if VARIANT == 'tiktok':
        return [('a01', 2.4), ('a02', 2.8), ('a04', 2.4), ('a05', 3.4), ('a06', 3.2), ('a07', 2.4), ('a08', 3.4), ('a12', 3.8),
                ('a14', 2.4), ('a15', 3.4), ('a16', 3.2), ('a17', 2.6), ('a18', 3.0), ('a19', 4.6), ('a20', 0.8), ('a21', 5.0), ('b22', 4.0)]
    return [('a01', 2.4), ('a02', 2.8), ('a04', 2.4), ('a05', 3.4), ('a06', 3.2), ('a07', 2.4), ('a08', 3.4), ('a12', 3.8),
            ('a14', 2.4), ('a15', 3.4), ('a16', 3.2), ('a17', 2.6), ('a18', 3.0), ('a19', 4.6), ('a20', 0.8), ('a21', 5.0), ('a22', 3.8)]


def build(only=None):
    A = assets(); T = dict(timeline())
    gw = (0.62, 0.45) if not V else (0.78, 0.5)
    J = {
        'a01': lambda: s_type('a01', T['a01'], 'DAYTON, OHIO. 2025.'),
        'a02': lambda: s_headlights('a02', T['a02']),
        'a03': lambda: s_shot('a03', T['a03'], A['garage'], 2.1, 2.35, (0.17, 0.12), (0.2, 0.13), flicker=True),
        'a04': lambda: s_card('a04', T['a04'], ['EN 1963 FIRMÓ UN ACUERDO'], ['EN 1963', 'FIRMÓ UN', 'ACUERDO']),
        'a05': lambda: s_dossier('a05', T['a05']),
        'a06': lambda: s_shot('a06', T['a06'], A['wl'], 1.0 if not V else 1.0, 1.25 if not V else 1.6, (0.5, 0.21) if not V else (0.36, 0.5), (0.5, 0.18) if not V else (0.36, 0.2)),
        'a07': lambda: s_card('a07', T['a07'], ['NO PODRÍA CONTÁRSELO A NADIE'], ['NO PODRÍA', 'CONTÁRSELO', 'A NADIE']),
        'a08': lambda: s_desert('a08', T['a08']),
        'a09': lambda: s_sketch('a09', T['a09'], 3, -1.5, [(0.25, 0.35), (0.5, 0.5), (0.68, 0.45)], 1.0, 1.1),
        'a10': lambda: s_sketch('a10', T['a10'], 4, 1.2, [(0.3, 0.3), (0.55, 0.45), (0.6, 0.7)], 1.05, 1.15),
        'a11': lambda: s_card('a11', T['a11'], ['DURANTE SESENTA AÑOS', 'GUARDÓ SILENCIO'], ['DURANTE', 'SESENTA AÑOS', 'GUARDÓ', 'SILENCIO'], 96, 112),
        'a12': lambda: s_lights('a12', T['a12']),
        'a13': lambda: s_shot('a13', T['a13'], A['garage'], 1.6, 1.8, (0.8, 0.45), (0.78, 0.5), k=0.9),
        'a14': lambda: s_card('a14', T['a14'], ['AHORA HA DECIDIDO HABLAR'], ['AHORA', 'HA DECIDIDO', 'HABLAR']),
        'a15': lambda: s_notebook('a15', T['a15'], ['Me queda poco tiempo.', 'Tengo mucho que contar.']),
        'a16': lambda: s_sketch('a16', T['a16'], 0, 0.6, [(0.4, 0.5), (0.6, 0.42), (0.68, 0.36)], 1.0, 1.45, (0.5, 0.5), (0.63, 0.38)),
        'a17': lambda: s_card('a17', T['a17'], ['PERO ALGUIEN', 'ESTÁ ESCUCHANDO'], ['PERO', 'ALGUIEN', 'ESTÁ', 'ESCUCHANDO'], 96, 112),
        'a18': lambda: s_shot('a18', T['a18'], A['wr'], 1.05, 1.3 if not V else 1.7, (0.55, 0.22) if not V else (0.5, 0.45), (0.5, 0.2) if not V else (0.48, 0.22), k=0.9),
        'a19': lambda: s_montage('a19', [
            (0.7, lambda u, t: arr(kenburns(clock_img(t), u, 1.0, 1.25, (0.5, 0.5), (0.5, 0.5)))),
            (0.6, lambda u, t: arr(kenburns(A['kenn'], u, 1.0, 1.1, (0.5, 0.6), (0.5, 0.62)))),
            (0.5, lambda u, t: arr(kenburns(A['wl'], u, 2.2 if not V else 3.4, 2.4 if not V else 3.6, (0.36, 0.17), (0.36, 0.17)))),
            (0.6, lambda u, t: arr(kenburns(make_paper(5, 0), u, 1.6, 1.8, (0.5, 0.75), (0.5, 0.73))) * 0.8),
            (0.5, lambda u, t: arr(kenburns(A['garage'], u, 2.4, 2.6, (0.77, 0.2), (0.77, 0.2)))),
            (1.7, lambda u, t: arr(kenburns(A['ghost'], u, 1.0, 1.15, (0.5, 0.4), (0.5, 0.36))) * float(min(1, u * 3)) * float(min(1, (1 - u) * 4))),
        ]),
        'a20': lambda: scene('a20', T['a20'], lambda u, t: np.zeros((AH, W, 3), np.float32), 0, 0),
        'a21': lambda: s_title('a21', T['a21']),
        'a22': lambda: s_end('a22', T['a22']),
        'b22': lambda: s_bio('b22', T['b22']),
        'c01': lambda: s_card('c01', T['c01'], ['FIRMÓ QUE NUNCA LO CONTARÍA'], ['FIRMÓ QUE', 'NUNCA LO', 'CONTARÍA']),
        'c02': lambda: s_card('c02', T['c02'], ['SESENTA AÑOS DESPUÉS', 'HA DECIDIDO HABLAR'], ['SESENTA AÑOS', 'DESPUÉS,', 'HA DECIDIDO', 'HABLAR']),
        'c03': lambda: s_card('c03', T['c03'], ['TRES LUCES. SIN SONIDO.'], ['TRES LUCES.', 'SIN SONIDO.']),
        'c04': lambda: s_card('c04', T['c04'], ['NEVADA, 1968'], ['NEVADA,', '1968']),
        'c05': lambda: s_card('c05', T['c05'], ['NUNCA SE LO CONTÓ A NADIE'], ['NUNCA SE LO', 'CONTÓ', 'A NADIE']),
    }
    for k, _ in timeline():
        if only and k not in only: continue
        J[k](); print('escena', k, flush=True)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build(sys.argv[1:] or None)
