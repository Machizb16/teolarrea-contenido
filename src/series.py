"""Serie de 20 vídeos verticales para TikTok de «Nadie se va del todo»."""
import os, sys, json, subprocess
os.environ['ORIENT'] = 'v'
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import trailer2 as T

W, H, AH, FPS = T.W, T.H, T.AH, T.FPS
BEBAS, PAGI, COUR, HAND = T.BEBAS, T.PAGI, T.COUR, T.HAND
OUT = os.path.join(os.environ.get('TRABAJO', '/tmp/teolarrea'), 'piezas'); os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- capturar fondos de trailer2
_cap = []
T.scene = lambda name, dur, fn, fi=0.4, fo=0.4: _cap.append(fn)


def grab(f, *a, **k):
    _cap.clear(); f('x', *a, **k); return _cap[-1]


A = T.assets()


def shot(src, z0, z1, c0, c1, k=1.0, flicker=False):
    return grab(T.s_shot, 1, src, z0, z1, c0, c1, k, flicker)


def sketch(n, rot, path, z0=1.0, z1=1.12, c0=(0.5, 0.5), c1=(0.5, 0.5)):
    return grab(T.s_sketch, 1, n, rot, path, z0, z1, c0, c1)


def notebook(lines, dur):
    return grab(T.s_notebook, dur, lines)


# ---------------------------------------------------------------- fondos nuevos
YY, XX = T.YY, T.XX
NX, NY = T.NX, T.NY


def clock_at(hh, mm, sec0=0):
    def fn(u, t):
        s = 900; img = Image.new('RGB', (s, s), (10, 10, 12)); d = ImageDraw.Draw(img); c = s / 2
        d.ellipse((60, 60, s - 60, s - 60), fill=(205, 200, 185), outline=(40, 40, 40), width=18)
        for k in range(60):
            ang = k / 60 * 2 * np.pi; r0 = c - 95 if k % 5 == 0 else c - 80
            d.line((c + np.sin(ang) * r0, c - np.cos(ang) * r0, c + np.sin(ang) * (c - 70), c - np.cos(ang) * (c - 70)),
                   fill=(30, 30, 30), width=8 if k % 5 == 0 else 3)
        def hand(fr, L, w_, col):
            ang = fr * 2 * np.pi; d.line((c, c, c + np.sin(ang) * L, c - np.cos(ang) * L), fill=col, width=w_)
        hand((hh % 12 + mm / 60) / 12, 200, 22, (20, 20, 20)); hand(mm / 60, 300, 14, (20, 20, 20))
        if sec0 is not None: hand((sec0 + int(t)) / 60, 330, 4, (150, 20, 20))
        d.ellipse((c - 18, c - 18, c + 18, c + 18), fill=(20, 20, 20))
        canvas = Image.new('RGB', (1500, 2667), (10, 10, 12)); canvas.paste(img, ((1500 - s) // 2, 820))
        a = T.arr(T.kenburns(T.grade(canvas, 0.75), u, 1.0, 1.15, (0.5, 0.48), (0.5, 0.48)))
        lamp = np.exp(-(((NX - 0.5) / 0.55) ** 2 + ((NY - 0.47) / 0.4) ** 2))
        return a * (0.25 + 0.85 * lamp[..., None])
    return fn


def radar():
    cx, cy, R = W / 2, AH * 0.45, W * 0.42
    r = np.sqrt((XX - cx) ** 2 + (YY - cy) ** 2); ang = np.arctan2(YY - cy, XX - cx)
    inside = (r < R)
    rings = sum(np.exp(-((r - R * f) / 2.5) ** 2) for f in (0.25, 0.5, 0.75, 1.0))
    cross = np.exp(-((XX - cx) / 1.5) ** 2) + np.exp(-((YY - cy) / 1.5) ** 2)
    base = (rings * 0.35 + cross * inside * 0.15)
    def fn(u, t):
        sweep = (t * 1.6) % (2 * np.pi) - np.pi
        da = (ang - sweep) % (2 * np.pi)
        trail = np.exp(-da / 0.9) * inside
        g = base * 0.6 + trail * 0.55
        a = np.zeros((AH, W, 3), np.float32) + 0.01
        a += g[..., None] * np.array([0.25, 1.0, 0.45])
        a += (inside * 0.03)[..., None] * np.array([0.1, 0.4, 0.15])
        return a
    return fn


def heart(d, x, y, s, col):
    d.ellipse((x - s, y - s * 0.6, x, y + s * 0.3), fill=col); d.ellipse((x, y - s * 0.6, x + s, y + s * 0.3), fill=col)
    d.polygon([(x - s * 0.97, y - 0.05 * s), (x + s * 0.97, y - 0.05 * s), (x, y + s * 1.15)], fill=col)


def card_img():
    cw, ch = 700, 1000
    card = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    d.rounded_rectangle((0, 0, cw - 1, ch - 1), radius=50, fill=(238, 232, 218, 255), outline=(150, 140, 120, 255), width=4)
    red = (170, 25, 30, 255); f = ImageFont.truetype(T.COURB, 110)
    d.text((40, 30), '7', font=f, fill=red); heart(d, 85, 190, 34, red)
    for (x, y) in [(230, 230), (470, 230), (230, 430), (470, 430), (350, 330), (230, 630), (470, 630)]:
        heart(d, x, y, 62, red)
    d.text((cw - 40, ch - 30), '7', font=f, fill=red, anchor='rd')
    fh = ImageFont.truetype(HAND, 54)
    d.text((60, ch - 230), 'Terminaron.', font=fh, fill=(40, 45, 90, 255)); d.text((60, ch - 165), 'Cuida al niño.', font=fh, fill=(40, 45, 90, 255))
    card = card.rotate(-8, expand=True, resample=Image.BICUBIC)
    table = T.wall_texture(9, (0.35, 0.25, 0.18))
    bg = Image.fromarray((np.clip(table * 0.5, 0, 1) * 255).astype(np.uint8)).resize((round(W * 1.2), round(AH * 1.1)))
    bg = bg.convert('RGBA'); x, y = (bg.width - card.width) // 2, (bg.height - card.height) // 2
    sh = Image.new('RGBA', bg.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 220), (x + 20, y + 30), card.split()[-1])
    bg = Image.alpha_composite(bg, sh.filter(ImageFilter.GaussianBlur(25))); bg.alpha_composite(card, (x, y))
    return bg.convert('RGB')


def card():
    src = card_img()
    def fn(u, t):
        a = T.arr(T.kenburns(src, u, 1.0, 1.12, (0.5, 0.40), (0.5, 0.43)))
        lamp = np.exp(-(((NX - 0.5) / 0.6) ** 2 + ((NY - 0.45) / 0.55) ** 2))
        return a * np.array([1.0, 0.92, 0.8]) * (0.15 + 0.95 * lamp[..., None])
    return fn


def hangar_door():
    stripes = 0.55 + 0.45 * np.sin(XX / W * 2 * np.pi * 26) ** 2
    wall = T.wall_texture(14, (0.5, 0.52, 0.55)) * stripes[..., None] * 0.55
    img = Image.fromarray((np.clip(wall, 0, 1) * 255).astype(np.uint8)); d = ImageDraw.Draw(img)
    f = ImageFont.truetype(BEBAS, 900); d.text((W / 2, AH * 0.47), '7', font=f, fill=(225, 225, 220), anchor='mm')
    d.rectangle((0, AH * 0.83, W, AH), fill=(30, 30, 32))
    base = T.arr(img)
    lamp = np.exp(-(((XX - W * 0.82) / 26) ** 2 + ((YY - AH * 0.1) / 26) ** 2))
    glow = np.exp(-(((XX - W * 0.82) / 260) ** 2 + ((YY - AH * 0.1) / 260) ** 2))
    def fn(u, t):
        p = 0.5 + 0.5 * np.sin(t * 4.0)
        a = base * 0.55 + (lamp * 2 + glow * 0.35)[..., None] * np.array([1, 0.12, 0.1]) * p
        a = a * (0.7 + 0.3 * p * glow[..., None] * 3).clip(0, 1.4)
        return np.clip(a, 0, 1)
    return fn


def kenn(): return shot(A['kenn'], 1.0, 1.12, (0.5, 0.55), (0.5, 0.6))
def ghost(): return shot(A['ghost'], 1.0, 1.15, (0.5, 0.42), (0.5, 0.36))
def walter_front(z1=1.6): return shot(A['wl'], 1.0, z1, (0.36, 0.5), (0.36, 0.2))
def walter_face(): return shot(A['wl'], 2.4, 2.8, (0.36, 0.2), (0.36, 0.17))
def walter_prof(): return shot(A['wr'], 1.05, 1.7, (0.5, 0.45), (0.48, 0.22), 0.9)
def garage_shelf(): return shot(A['garage'], 2.0, 2.3, (0.17, 0.12), (0.2, 0.14), 1.0, True)
def garage_window(): return shot(A['garage'], 1.7, 1.9, (0.77, 0.25), (0.75, 0.3))
def garage_wide(): return shot(A['garage'], 1.0, 1.2, (0.55, 0.5), (0.7, 0.5), 1.0, True)
def desert(): return grab(T.s_desert, 3)
def lights(): return grab(T.s_lights, 4)
def headlights(): return grab(T.s_headlights, 3)
def dossier(): return grab(T.s_dossier, 3)


# ---------------------------------------------------------------- texto superpuesto
def wrap(text, font, size, maxw):
    f = ImageFont.truetype(font, size); d = ImageDraw.Draw(Image.new('L', (4, 4)))
    lines, cur = [], ''
    for wd in text.split():
        tst = (cur + ' ' + wd).strip()
        if d.textlength(tst, font=f) <= maxw: cur = tst
        else: lines.append(cur); cur = wd
    lines.append(cur); return lines


def overlay(text, font, size, ycenter, color=(244, 246, 248), maxw=820, gap=1.12, red_words=(), red_col=(232, 80, 80)):
    lines = wrap(text, font, size, maxw); f = ImageFont.truetype(font, size)
    img = Image.new('RGBA', (W, AH), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    lh = size * gap; y = ycenter - lh * len(lines) / 2
    for l in lines:
        x = (W - d.textlength(l, font=f)) / 2
        for wd in l.split(' '):
            col = red_col if wd.strip('.,:;¿?¡!«»').upper() in red_words else color
            d.text((x, y), wd, font=f, fill=col + (255,)); x += d.textlength(wd + ' ', font=f)
        y += lh
    a = np.asarray(img).astype(np.float32) / 255
    sh = np.asarray(Image.fromarray((a[..., 3] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))).astype(np.float32)[..., None] / 255
    box = Image.new('L', (W, AH), 0); bd = ImageDraw.Draw(box)
    top = ycenter - lh * len(lines) / 2 - size * 0.35; bot = ycenter + lh * len(lines) / 2 + size * 0.2
    wmax = max(d.textlength(l, font=f) for l in lines)
    bd.rounded_rectangle(((W - wmax) / 2 - 40, top, (W + wmax) / 2 + 40, bot), radius=28, fill=220)
    bx = np.asarray(box.filter(ImageFilter.GaussianBlur(18))).astype(np.float32)[..., None] / 255
    return a[..., :3], a[..., 3:4], np.clip(np.maximum(sh * 1.6, bx), 0, 1)


def compose(bg, layers, t_rel):
    for (rgb, al, sh, t0) in layers:
        k = T.ease((t_rel - t0) / 0.35)
        if k <= 0: continue
        bg = bg * (1 - 0.88 * sh * k) * (1 - al * k) + rgb * al * k
    return bg


# ---------------------------------------------------------------- render de un vídeo
# Variantes de formato (spec['estilo']):
#   gancho: banda (franja oscura) | cinta (franja roja) | palabras (aparece palabra a palabra)
#   texto:  pagi (cursiva) | anton (mayúsculas) | maquina (máquina de escribir)
#   trans:  fundido | corte (corte seco con destello) | zoom (empuje al entrar)
ESTILOS = dict(gancho=['banda', 'cinta', 'palabras'], texto=['pagi', 'anton', 'maquina'], trans=['fundido', 'corte', 'zoom'])
ROJO_T = np.array([200, 33, 28], np.float32) / 255


def _capa(ov, t0, tint=None, fade=True):
    return dict(frames=[(t0, ov)], t0=t0, tint=tint, fade=fade)


def compose2(bg, layers, t):
    for L in layers:
        if t < L['t0']: continue
        ov = L['frames'][0][1]
        for ts, o in L['frames']:
            if ts <= t: ov = o
        k = T.ease((t - L['t0']) / 0.35) if L['fade'] else 1.0
        rgb, al, sh = ov
        if L['tint'] is None:
            bg = bg * (1 - 0.88 * sh * k)
        else:
            bg = bg * (1 - 0.95 * sh * k) + L['tint'] * 0.95 * sh * k
        bg = bg * (1 - al * k) + rgb * al * k
    return bg


def capa_gancho(spec, est):
    hf, hs = spec.get('hook_font', (BEBAS, 118)); red = spec.get('red', ()); y = AH * 0.25
    g = est.get('gancho', 'banda')
    if g == 'cinta':
        return _capa(overlay(spec['hook'], hf, hs, y, color=(246, 242, 234), red_words=red, red_col=(18, 16, 16)), 0.15, ROJO_T)
    if g == 'palabras':
        pal = spec['hook'].split(); fr = []
        for k in range(1, len(pal) + 1):
            fr.append((0.1 + 0.16 * (k - 1), overlay(' '.join(pal[:k]), hf, hs, y, red_words=red)))
        return dict(frames=fr, t0=0.1, tint=None, fade=False)
    return _capa(overlay(spec['hook'], hf, hs, y, red_words=red), 0.15)


def capa_texto(line, pos, est):
    y = AH * pos; tx = est.get('texto', 'pagi')
    if tx == 'anton':
        import coleccion as C
        return _capa(overlay(line.upper(), C.ANTON, 64, y, maxw=860, gap=1.18), 0.45)
    if tx == 'maquina':
        fr = []; n = len(line); paso = 3
        for k in list(range(paso, n, paso)) + [n]:
            fr.append((0.4 + k / 32, overlay(line[:k], T.COURB, 56, y, maxw=860, gap=1.2)))
        return dict(frames=fr, t0=0.4, tint=None, fade=False)
    return _capa(overlay(line, PAGI, 62, y, maxw=840), 0.5)


def _zoom(a, z):
    if z <= 1.001: return a
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)); w, h = im.size
    cw, ch = w / z, h / z; x0, y0 = (w - cw) / 2, (h - ch) / 2
    return np.asarray(im.transform((w, h), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BILINEAR)).astype(np.float32) / 255


def render_video(vid, spec):
    name = f'{OUT}/v{vid:02d}_body'
    if os.path.exists(name + '.mp4') and not os.environ.get('FORCE'): return
    est = spec.get('estilo', {}); trans = est.get('trans', 'fundido')
    hook = capa_gancho(spec, est)
    class E: pass
    e = E(); e.tmp = name + '.part.mp4'; e.name = name + '.mp4'
    e.write = lambda f: e.p.stdin.write(f.tobytes())
    def _close():
        e.p.stdin.close()
        if e.p.wait() == 0: os.replace(e.tmp, e.name)
        else: raise SystemExit('ffmpeg falló')
    e.close = _close
    e.p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast',
                            '-pix_fmt', 'yuv420p', e.tmp], stdin=subprocess.PIPE)
    fi = 0; ns = len(spec['shots'])
    for si, (bgf, dur, line) in enumerate(spec['shots']):
        fn = bgf()
        layers = []
        if si == 0: layers.append(hook)
        if line:
            pos = (spec.get('pos') or [None] * 99)[si] or 0.56
            layers.append(capa_texto(line, pos, est))
        n = round(dur * FPS); ultimo = si == ns - 1
        for i in range(n):
            t = i / FPS; u = i / max(1, n - 1)
            bg = fn(u, t)
            if trans == 'zoom' and si > 0: bg = _zoom(bg, 1 + 0.12 * (1 - T.ease(t / 0.45)))
            a = compose2(bg, layers, t)
            if trans == 'fundido' or si == 0:
                fade = min(1.0, (t + 0.001) / 0.25, (dur - t) / 0.25 if (trans == 'fundido' or ultimo) else 1.0)
            else:
                fade = min(1.0, (dur - t) / 0.25) if ultimo else 1.0
                if trans == 'corte' and i < 3: a = a + (0.35, 0.18, 0.06)[i]
            e.write(T.out_frame(a, fi, fade)); fi += 1
    e.close()


# ---------------------------------------------------------------- audio
def make_audio(vid, spec, total, title_at):
    from scipy.signal import butter, sosfilt
    from scipy.io import wavfile
    SR = 48000; N = int(total * SR); L = np.zeros(N); rng = np.random.default_rng(vid)
    lp = lambda x, f: sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
    hp = lambda x, f: sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
    def add(sig, at, g):
        i = int(at * SR); j = min(N, i + len(sig)); L[i:j] += sig[:j - i] * g
    def env(n, a, d):
        e = np.ones(n); ka = int(a * SR)
        if ka: e[:ka] = np.linspace(0, 1, ka)
        return e * np.exp(-np.arange(n) / (d * SR))
    def braam(dur, f):
        n = int(dur * SR); t_ = np.arange(n) / SR
        saw = np.tanh(sum(np.sin(2 * np.pi * f * h * t_) / h for h in range(1, 12)) * 2.2)
        return lp(saw, 900) * env(n, 0.02, 1.0) * 0.6 + np.sin(2 * np.pi * 38 * t_ * (1 - 0.15 * t_)) * env(n, 0.005, 0.8) * 0.9
    n = int(title_at * SR); tt = np.arange(n) / SR
    base = [55, 49, 61.7, 58.3][vid % 4]
    drone = (np.sin(2 * np.pi * base * tt) * 0.5 + np.sin(2 * np.pi * base * 1.5 * tt) * 0.3) * np.clip(tt / 2, 0, 1) * (0.6 + 0.4 * tt / tt[-1])
    add(drone, 0, 0.18)
    x = 0.5
    while x < title_at - 0.5:
        add(hp(rng.normal(0, 1, 1400), 2000) * env(1400, 0, 0.006), x, 0.07); x += 1.0
    B = braam(2.5, 43 + vid % 5)
    add(B, 0.1, 0.5)
    t = 0
    for (_, dur, line) in spec['shots']:
        if t > 0: add(B[: int(1.2 * SR)] * np.linspace(1, 0, int(1.2 * SR)), t + 0.05, 0.3)
        t += dur
    n = int(1.6 * SR); u = np.arange(n) / n
    add(hp(rng.normal(0, 1, n), 800) * u ** 3 * 0.4, title_at - 1.7, 0.6)
    add(braam(5.5, 36), title_at + 0.15, 0.85)
    m = np.abs(L).max(); L = L / m * 0.89
    wavfile.write(f'{OUT}/v{vid:02d}.wav', SR, (np.stack([L, L], 1) * 32767).astype(np.int16))


E = os.path.join(T.A_, 'escenas')


def assemble(vid, spec):
    total_body = sum(d for _, d, _ in spec['shots'])
    total = total_body + 0.8 + 5.0 + 4.0
    if spec.get('musica'):
        import musica as Mu
        from scipy.io import wavfile
        cortes = list(np.cumsum([d for _, d, _ in spec['shots']])[:-1])
        S = Mu.pista(spec['musica'], vid * 7919 + len(spec['slug']), total, total_body + 0.8, cortes)
        wavfile.write(f'{OUT}/v{vid:02d}.wav', Mu.SR, (S * 32767).astype(np.int16))
    else:
        make_audio(vid, spec, total, total_body + 0.8)
    lst = f'{OUT}/v{vid:02d}.txt'
    cierre = spec.get('cierre') or [f'{E}/a20.mp4', f'{E}/a21.mp4', f'{E}/b22.mp4']
    open(lst, 'w').write(f"file 'v{vid:02d}_body.mp4'\n" + ''.join(f"file '{c}'\n" for c in cierre))
    final = f'{OUT}/TikTok_{vid:02d}_{spec["slug"]}.mp4'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-i', f'{OUT}/v{vid:02d}.wav',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '24', '-maxrate', '10M', '-bufsize', '20M', '-preset', 'veryfast',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', final + '.part.mp4'], check=True)
    os.replace(final + '.part.mp4', final)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    from guiones import VIDEOS
    ids = [int(x) for x in sys.argv[1:]] or list(VIDEOS)
    for v in ids:
        render_video(v, VIDEOS[v]); assemble(v, VIDEOS[v]); print('video', v, flush=True)
