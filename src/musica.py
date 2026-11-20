"""Música de fondo sintetizada, con varios estilos para que los vídeos no suenen todos igual.

pista(estilo, seed, total, title_at, cortes) devuelve un array estéreo (N, 2) en -1..1 a 48 kHz.
- title_at: segundo en que aparece el título (golpe final).
- cortes: segundos de los cambios de plano (pequeños acentos).
Todo es síntesis propia: no se usa música de terceros.
"""
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
ESTILOS = ['cine', 'piano', 'pulso', 'lofi', 'pizzicato', 'ambiente']
POR_LIBRO = {
    'nadie': ['cine', 'pulso', 'ambiente', 'piano'],
    'abras': ['ambiente', 'piano', 'pulso', 'lofi'],
    'mires': ['piano', 'lofi', 'ambiente', 'pizzicato'],
    'creas': ['pizzicato', 'lofi', 'pulso', 'piano'],
}


def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, f1, f2): return sosfilt(butter(2, [f1, f2], 'band', fs=SR, output='sos'), x)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)


def env(n, a=0.005, d=0.3, s=0.0, r=None):
    """Ataque lineal y caída exponencial hacia s."""
    t = np.arange(n) / SR; e = np.exp(-t / max(d, 1e-4)) * (1 - s) + s
    ka = int(a * SR)
    if ka: e[:ka] *= np.linspace(0, 1, ka)
    if r:
        kr = min(n, int(r * SR)); e[-kr:] *= np.linspace(1, 0, kr)
    return e


class Mezcla:
    def __init__(self, total):
        self.N = int(total * SR); self.L = np.zeros(self.N); self.R = np.zeros(self.N)

    def add(self, sig, at, g=1.0, pan=0.0):
        i = int(at * SR)
        if i >= self.N or i + len(sig) <= 0: return
        if i < 0: sig = sig[-i:]; i = 0
        j = min(self.N, i + len(sig)); s = sig[:j - i] * g
        self.L[i:j] += s * np.sqrt(0.5 * (1 - pan)); self.R[i:j] += s * np.sqrt(0.5 * (1 + pan))


# ------------------------------------------------------------------ voces
def seno(f, dur, harm=(1.0,), det=0.0):
    t = np.arange(int(dur * SR)) / SR
    return sum(a * np.sin(2 * np.pi * f * (k + 1) * t * (1 + det)) for k, a in enumerate(harm))


def piano(f, dur=1.6):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * k * t * (1 + 0.0004 * k * k)) * np.exp(-t * (1.2 + k * 0.9))
            for k, a in zip(range(1, 7), (1, 0.5, 0.28, 0.15, 0.08, 0.05)))
    return s * env(n, 0.003, 10, 0, 0.05)


def caja_musica(f, dur=1.4):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 3.98 * t) * np.exp(-t * 6)) * np.exp(-t * 2.4) * env(n, 0.002, 10)


def pluck(f, dur=0.5, brillo=3000):
    n = int(dur * SR); t = np.arange(n) / SR
    saw = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 10))
    return lp(saw, brillo) * np.exp(-t * 9)


def rhodes(f, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t + 1.2 * np.sin(2 * np.pi * f * t) * np.exp(-t * 3))
    return s * env(n, 0.01, 1.8, 0.25, 0.2) * (1 + 0.15 * np.sin(2 * np.pi * 4.5 * t))


def pad(f, dur, corte=900):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * k * t * (1 + d)) / k for k in range(1, 7) for d in (-0.003, 0.0, 0.004))
    e = np.minimum(1, t / min(1.5, dur / 3)) * np.minimum(1, (dur - t) / min(1.2, dur / 3))
    return lp(s, corte) * e * 0.35


def campana(f, dur=3.0):
    n = int(dur * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t + 2.0 * np.sin(2 * np.pi * f * 1.41 * t) * np.exp(-t * 1.5)) * np.exp(-t * 1.1)


def bombo(dur=0.5):
    n = int(dur * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (45 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 7)


def caja(rng, dur=0.25):
    n = int(dur * SR); t = np.arange(n) / SR
    return bp(rng.normal(0, 1, n), 900, 5000) * np.exp(-t * 18) * 0.8 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25) * 0.4


def hat(rng, dur=0.06):
    n = int(dur * SR); return hp(rng.normal(0, 1, n), 7000) * np.exp(-np.arange(n) / SR * 60)


def tic(rng, dur=0.03):
    n = int(dur * SR); return hp(rng.normal(0, 1, n), 3000) * np.exp(-np.arange(n) / SR * 200)


def subida(dur):
    n = int(dur * SR); u = np.arange(n) / n; rng = np.random.default_rng(5)
    return hp(rng.normal(0, 1, n), 600) * u ** 3


def golpe(f=40, dur=4.0):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t * (1 - 0.1 * t / dur)) * np.exp(-t * 0.9)
            + lp(np.random.default_rng(1).normal(0, 1, n), 300) * np.exp(-t * 4) * 0.6)


def braam(dur, f):
    n = int(dur * SR); t = np.arange(n) / SR
    saw = np.tanh(sum(np.sin(2 * np.pi * f * h * t) / h for h in range(1, 12)) * 2.2)
    return lp(saw, 900) * env(n, 0.02, 1.0) * 0.6 + np.sin(2 * np.pi * 38 * t * (1 - 0.15 * t)) * env(n, 0.005, 0.8) * 0.9


# ------------------------------------------------------------------ armonía
PROGS = [[0, 8, 3, 10], [0, 5, 8, 7], [0, 10, 8, 7], [0, 3, 8, 10], [0, 8, 5, 7]]


def acorde(raiz, grado):
    """Tríada de la escala menor natural sobre el grado (en semitonos desde la tónica)."""
    menor = {0: 'm', 3: 'M', 5: 'm', 7: 'm', 8: 'M', 10: 'M', 2: 'd'}
    q = menor.get(grado, 'm'); r = raiz + grado
    return [r, r + (3 if q in 'md' else 4), r + (6 if q == 'd' else 7)]


# ------------------------------------------------------------------ estilos
def _cine(M, rng, total, ta, cortes, raiz):
    n = int(ta * SR); t = np.arange(n) / SR; base = hz(raiz - 12)
    drone = (np.sin(2 * np.pi * base * t) * 0.5 + np.sin(2 * np.pi * base * 1.5 * t) * 0.3) * np.clip(t / 2, 0, 1)
    M.add(drone, 0, 0.2)
    x = 0.5
    while x < ta - 0.5: M.add(tic(rng), x, 0.25, rng.uniform(-0.5, 0.5)); x += 1.0
    B = braam(2.5, base); M.add(B, 0.1, 0.5)
    for c in cortes: M.add(B[:int(1.2 * SR)] * np.linspace(1, 0, int(1.2 * SR)), c + 0.05, 0.3)
    M.add(subida(1.6), ta - 1.7, 0.35); M.add(braam(5.5, base * 0.8), ta + 0.15, 0.85)


def _piano(M, rng, total, ta, cortes, raiz):
    bpm = rng.uniform(72, 88); beat = 60 / bpm; prog = PROGS[rng.integers(len(PROGS))]
    voz = caja_musica if rng.random() < 0.5 else piano
    patron = [0, 1, 2, 1, 0, 2, 1, 2] if rng.random() < 0.5 else [0, 2, 1, 2, 0, 1, 2, 1]
    t = 0.2; k = 0
    while t < total - 1.5:
        ch = acorde(raiz, prog[(k // 8) % 4]); nota = ch[patron[k % 8]] + 12
        g = 0.32 if t < ta else 0.22
        M.add(voz(hz(nota), 1.6), t, g, 0.3 * np.sin(k));
        if k % 8 == 0:
            M.add(pad(hz(ch[0] - 12), beat * 8 + 0.5, 600), t, 0.5)
            M.add(piano(hz(ch[0] - 24), 2.5), t, 0.3)
        t += beat / 2; k += 1
    M.add(golpe(hz(raiz - 24), 4.0), ta + 0.1, 0.55)
    for q, m in enumerate(acorde(raiz, 0)): M.add(piano(hz(m), 4.0), ta + 0.12 + q * 0.06, 0.25, (q - 1) * 0.4)


def _pulso(M, rng, total, ta, cortes, raiz):
    bpm = rng.uniform(108, 124); s16 = 60 / bpm / 4; prog = PROGS[rng.integers(len(PROGS))]
    patron = [0, 2, 1, 2, 0, 2, 1, 0]
    t = 0.0; k = 0
    while t < ta - 0.1:
        compas = (k // 16) % 4; ch = acorde(raiz, prog[compas])
        apertura = 800 + 2600 * min(1, t / max(ta, 1))
        M.add(pluck(hz(ch[patron[k % 8]] + 12), 0.25, apertura), t, 0.22, 0.35 * (1 if k % 2 else -1))
        if k % 4 == 0:
            M.add(seno(hz(ch[0] - 12), s16 * 3.5) * env(int(s16 * 3.5 * SR), 0.005, 0.2), t, 0.45)
        if k % 8 == 0 and t > 1.5: M.add(bombo(), t, 0.5)
        t += s16; k += 1
    for c in cortes: M.add(subida(0.4), c - 0.4, 0.15)
    M.add(subida(1.5), ta - 1.5, 0.3)
    M.add(golpe(hz(raiz - 24), 5.0), ta + 0.1, 0.8)
    M.add(pad(hz(raiz), total - ta, 1200), ta + 0.1, 0.6)


def _lofi(M, rng, total, ta, cortes, raiz):
    bpm = rng.uniform(78, 90); beat = 60 / bpm; prog = PROGS[rng.integers(len(PROGS))]
    t = 0.0; k = 0
    while t < total - 1.0:
        swing = beat / 2 * (0.12 if k % 2 else 0)
        if k % 8 == 0:
            ch = acorde(raiz + 12, prog[(k // 8) % 4])
            for q, m in enumerate(ch + [ch[0] + 10]): M.add(rhodes(hz(m), beat * 4), t + q * 0.012, 0.11, (q - 1.5) * 0.3)
            M.add(seno(hz(ch[0] - 24), beat * 3) * env(int(beat * 3 * SR), 0.01, 0.9), t, 0.4)
        if t < ta:
            if k % 4 == 0: M.add(bombo(0.4), t, 0.45)
            if k % 4 == 2: M.add(caja(rng), t + swing, 0.25)
            M.add(hat(rng), t + swing, 0.07 if k % 2 else 0.11, 0.3)
        t += beat / 2; k += 1
    crack = np.zeros(M.N)
    idx = rng.integers(0, M.N, int(total * 18)); crack[idx] = rng.uniform(-1, 1, len(idx))
    M.add(lp(crack, 4000) * 0.5 + hp(rng.normal(0, 0.02, M.N), 2000), 0, 0.5)
    M.add(campana(hz(raiz + 24), 3.0), ta + 0.1, 0.12)


def _pizzicato(M, rng, total, ta, cortes, raiz):
    bpm = rng.uniform(96, 112); beat = 60 / bpm; prog = PROGS[rng.integers(len(PROGS))]
    escala = [0, 2, 3, 5, 7, 8, 11, 12]
    t = 0.0; k = 0
    while t < total - 1.0:
        swing = beat / 2 * (0.16 if k % 2 else 0)
        ch = acorde(raiz, prog[(k // 8) % 4])
        if t < ta:
            if k % 2 == 0: M.add(pluck(hz(ch[(k // 2) % 3] - 12), 0.4, 1200), t + swing, 0.4, -0.2)
            if k % 2 == 1 or rng.random() < 0.3:
                M.add(pluck(hz(raiz + 12 + escala[rng.integers(len(escala))]), 0.3, 4500), t + swing, 0.2, 0.3)
            M.add(tic(rng), t, 0.18 if k % 2 == 0 else 0.1, 0.5)
        t += beat / 2; k += 1
    for c in cortes: M.add(pluck(hz(raiz + 24), 0.6, 6000), c, 0.25)
    M.add(golpe(hz(raiz - 24), 3.0), ta + 0.1, 0.5)
    for q, m in enumerate([0, 3, 7, 12]): M.add(pluck(hz(raiz + m), 0.8, 3000), ta + 0.15 + q * 0.11, 0.3, (q - 1.5) * 0.3)
    M.add(pad(hz(raiz), total - ta - 0.3, 800), ta + 0.3, 0.4)


def _ambiente(M, rng, total, ta, cortes, raiz):
    prog = PROGS[rng.integers(len(PROGS))]; dur = 3.6
    t = 0.0; k = 0
    while t < total - 0.5:
        for m in acorde(raiz, prog[k % 4]): M.add(pad(hz(m), dur + 1.5, 700), t, 0.35, rng.uniform(-0.4, 0.4))
        t += dur; k += 1
    viento = lp(rng.normal(0, 1, M.N), 500) * (0.6 + 0.4 * np.sin(np.arange(M.N) / SR * 0.5))
    M.add(viento, 0, 0.08)
    # tres destellos y una pausa
    x = 0.3
    while x < ta:
        for q in range(3): M.add(campana(hz(raiz + 24 + (7 if q == 1 else 0)), 2.5), x + q * 0.55, 0.12, (q - 1) * 0.5)
        x += 3.6
    M.add(golpe(hz(raiz - 24), 5.0), ta + 0.1, 0.6)


FUNC = dict(cine=_cine, piano=_piano, pulso=_pulso, lofi=_lofi, pizzicato=_pizzicato, ambiente=_ambiente)


def pista(estilo, seed, total, title_at, cortes=()):
    rng = np.random.default_rng(seed)
    raiz = int(rng.integers(45, 53))      # tónica entre La2 y Do#3
    M = Mezcla(total)
    FUNC[estilo](M, rng, total, title_at, list(cortes), raiz)
    S = np.stack([M.L, M.R], 1)
    S = S * (0.16 / (np.sqrt((S ** 2).mean()) + 1e-9))      # mismo volumen percibido en todos los estilos
    S = np.tanh(S * 1.4) / np.tanh(1.4)
    S = S / max(1.0, np.abs(S).max() / 0.89)
    nf = int(1.2 * SR); S[-nf:] *= np.linspace(1, 0, nf)[:, None]
    return S
