"""Generador diario de piezas para TikTok y YouTube Shorts.

Uso:
  python3 src/diario.py --n 2            # elige al azar 2 libros distintos y genera una idea sin usar de cada uno
  python3 src/diario.py --ids n21 n22    # genera ideas concretas
  python3 src/diario.py --marcar n21 n22 # marca ideas como publicadas en borrador (actualiza estado.json)
Salida: $TRABAJO/salida/<fecha>/ con los .mp4, las portadas .jpg y manifest.json
"""
import os, sys, json, argparse, datetime, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
os.environ.setdefault('TRABAJO', '/tmp/teolarrea')
IDEAS = os.path.join(ROOT, 'ideas.json')
ESTADO = os.path.join(ROOT, 'estado.json')

CTA = '📖 «Nadie se va del todo», thriller y ciencia ficción de Teo Larrea. Tapa blanda y Kindle en Amazon. 🔗 Enlace en la bio.'
AVISO = 'Obra de ficción inspirada en los relatos y leyendas sobre el Área 51.'
LIBROS = ['nadie', 'abras', 'mires', 'creas']
CTA_COL = {
    'abras': '📖 «No abras este libro», de Teo Larrea. Novela interactiva de la colección Libros prohibidos.',
    'mires': '📖 «No mires este libro», de Teo Larrea. Novela interactiva de la colección Libros prohibidos.',
    'creas': '📖 «No creas este libro», de Teo Larrea. Novela interactiva de la colección Libros prohibidos.',
}
CTA_FIN = 'Disponible en Amazon, en Kindle y en tapa blanda. Gratis con Kindle Unlimited. 🔗 Enlace en la bio.'
TAGS_COL = ['libros', 'novela interactiva', 'booktok', 'teo larrea', 'libros prohibidos', 'thriller psicologico']


def libro_de(idea): return idea.get('libro', 'nadie')


def cargar_estado():
    if os.path.exists(ESTADO):
        return json.load(open(ESTADO))
    return {'usadas': [], 'historial': []}


def fondo(spec, dur):
    import series as S, coleccion as C
    if C.es_fondo(spec):
        return C.fondo(spec)
    if isinstance(spec, str):
        return getattr(S, spec)()
    if 'clock' in spec:
        h, m = spec['clock']; return S.clock_at(h, m, spec.get('segundos'))
    if 'notebook' in spec:
        return S.notebook(spec['notebook'], dur)
    if 'sketch' in spec:
        z = spec.get('zoom', [1.0, 1.12]); c = spec.get('centro', [[0.5, 0.5], [0.5, 0.5]])
        luz = spec.get('luz', [[0.4, 0.45], [0.6, 0.45]])
        return S.sketch(spec['sketch'], spec.get('rot', 0.0), luz, z[0], z[1], tuple(c[0]), tuple(c[1]))
    raise ValueError(spec)


def portada(idea, num, path):
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    import series as S, trailer2 as T
    W, H = T.W, T.H
    fn = fondo(idea['portada'], 3)
    a = np.clip(fn(0.7, 3.3) * T.VIG * 1.05, 0, 1)
    arr = (a * 255).astype(np.float32)
    yy = np.linspace(0, 1, H)[:, None, None]
    arr *= (1 - 0.55 * np.exp(-((yy - 0.3) / 0.16) ** 2))
    img = Image.fromarray(arr.clip(0, 255).astype(np.uint8)); d = ImageDraw.Draw(img)
    def ct(y, t, f, fill):
        w = d.textlength(t, font=f); x = (W - w) / 2
        for dx, dy in [(0, 6), (4, 6), (-4, 6), (0, 10)]: d.text((x + dx, y + dy), t, font=f, fill=(0, 0, 0))
        d.text((x, y), t, font=f, fill=fill)
    size = 132; lines = S.wrap(idea['gancho'], T.BEBAS, size, 900)
    while len(lines) > 4:
        size -= 10; lines = S.wrap(idea['gancho'], T.BEBAS, size, 900)
    f = ImageFont.truetype(T.BEBAS, size); y = 430 - len(lines) * size * 0.5
    red = set(idea.get('rojo', []))
    for l in lines:
        hot = any(w.strip('.,:;¿?¡!«»').upper() in red for w in l.split())
        ct(y, l, f, (236, 92, 92) if hot and len(l.split()) <= 2 else (246, 247, 249)); y += size * 1.02
    ct(150, 'NADIE SE VA DEL TODO', ImageFont.truetype(T.BEBAS, 46), (205, 212, 220))
    fb = ImageFont.truetype(T.BEBAS, 76); t = 'ENLACE EN LA BIO'
    w = d.textlength(t, font=fb); x0 = (W - w) / 2 - 50; yb = 1350
    d.rounded_rectangle((x0, yb, x0 + w + 100, yb + 110), radius=18, fill=(200, 38, 43))
    d.text((x0 + 50, yb + 15), t, font=fb, fill=(255, 255, 255))
    ct(yb + 135, 'Tapa blanda y Kindle en Amazon', ImageFont.truetype(T.PAGI, 42), (222, 226, 230))
    img.convert('RGB').save(path, quality=90)


def generar(ideas_sel, todas):
    import series as S, coleccion as C
    hoy = datetime.date.today().isoformat()
    out = os.path.join(os.environ['TRABAJO'], 'salida', hoy); os.makedirs(out, exist_ok=True)
    man = []
    for idea in ideas_sel:
        libro = libro_de(idea)
        num = [i['id'] for i in todas].index(idea['id']) + 1
        spec = dict(slug=idea['slug'], hook=idea['gancho'], red=tuple(r.strip('.,:;¿?¡!«»').upper() for r in idea.get('rojo', [])),
                    pos=[p.get('pos') for p in idea['planos']],
                    shots=[((lambda s=p['fondo'], d=p.get('dur', 3.7): fondo(s, d)), p.get('dur', 3.7), p.get('texto'))
                           for p in idea['planos']])
        if libro != 'nadie':
            spec['hook_font'] = (C.ANTON, 104); spec['cierre'] = C.asegurar_cierres(libro)
        S.render_video(num, spec); S.assemble(num, spec)
        src = os.path.join(S.OUT, f'TikTok_{num:02d}_{idea["slug"]}.mp4')
        video = os.path.join(out, f'{idea["id"]}_{idea["slug"]}.mp4'); shutil.copy(src, video)
        cov = os.path.join(out, f'{idea["id"]}_{idea["slug"]}.jpg')
        if libro == 'nadie':
            portada(idea, num, cov)
            texto = f'{idea["descripcion"]}\n\n{CTA}\n{AVISO}\n\n{idea["hashtags"]}'
            tags = idea.get('tags_youtube', ['thriller', 'novela', 'area 51', 'booktok', 'libros'])
        else:
            C.portada(idea, cov)
            texto = f'{idea["descripcion"]}\n\n{CTA_COL[libro]}\n{CTA_FIN}\n\n{idea["hashtags"]}'
            tags = idea.get('tags_youtube', TAGS_COL)
        man.append(dict(id=idea['id'], libro=libro, slug=idea['slug'], video=video, portada=cov,
                        titulo_tiktok=idea['titulo'][:90], titulo_youtube=(idea['titulo'][:88] + ' #shorts'),
                        texto=texto, tags_youtube=tags))
        print('generada', idea['id'], flush=True)
    json.dump(man, open(os.path.join(out, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
    print('MANIFEST', os.path.join(out, 'manifest.json'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=0); ap.add_argument('--ids', nargs='*'); ap.add_argument('--marcar', nargs='*')
    a = ap.parse_args()
    ideas = json.load(open(IDEAS)); est = cargar_estado()
    if a.marcar:
        for i in a.marcar:
            if i not in est['usadas']: est['usadas'].append(i)
        est['historial'].append({'fecha': datetime.date.today().isoformat(), 'ids': a.marcar})
        json.dump(est, open(ESTADO, 'w'), ensure_ascii=False, indent=1)
        resumen(ideas, est); return
    if a.ids:
        sel = [i for i in ideas if i['id'] in a.ids]
    else:
        sel = elegir(ideas, est, a.n)
    if not sel:
        print('NO QUEDAN IDEAS: amplía ideas.json'); sys.exit(2)
    generar(sel, ideas)
    resumen(ideas, est)


def libres_por_libro(ideas, est):
    return {l: [i for i in ideas if libro_de(i) == l and i['id'] not in est['usadas']] for l in LIBROS}


def elegir(ideas, est, n):
    """n piezas de libros distintos elegidos al azar (si no hay bastantes libros con ideas, repite)."""
    import random
    lib = libres_por_libro(ideas, est)
    con = [l for l in LIBROS if lib[l]]
    random.shuffle(con)
    sel = []
    while len(sel) < n and any(lib[l] for l in con):
        for l in con:
            if lib[l] and len(sel) < n:
                sel.append(lib[l].pop(random.randrange(len(lib[l]))))
    return sel


def resumen(ideas, est):
    lib = libres_por_libro(ideas, est)
    for l in LIBROS:
        aviso = '  <- AMPLIAR (paso 7)' if len(lib[l]) < 4 else ''
        print(f'ideas sin usar [{l}]: {len(lib[l])}{aviso}')


if __name__ == '__main__':
    main()
