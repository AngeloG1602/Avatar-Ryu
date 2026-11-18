"""Música y efectos de sonido chiptune sintetizados (sin samples externos).

Salida: juego/assets/audio/<nombre>.ogg
  musica_exploracion, musica_pelea, musica_jefe  (loops exactos)
  sfx_fuego, sfx_aire, sfx_agua, sfx_tierra, sfx_golpe, sfx_danio, sfx_derribo,
  sfx_puerta, sfx_pista, sfx_desbloqueo, sfx_dialogo, sfx_menu
Uso: python3 herramientas/audio.py
"""
import os
import subprocess
import tempfile
import wave
import numpy as np

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SALIDA = os.path.join(RAIZ, "juego", "assets", "audio")
SR = 44100
RNG = np.random.default_rng(7)

NOTAS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def frec(nombre):
    n = NOTAS[nombre[0]]
    i = 1
    if nombre[i] == "#":
        n += 1; i += 1
    elif nombre[i] == "b":
        n -= 1; i += 1
    octava = int(nombre[i:])
    midi = 12 * (octava + 1) + n
    return 440.0 * 2 ** ((midi - 69) / 12)


# ================================================================== osciladores
def fase(f, n):
    return np.cumsum(np.full(n, f) / SR) if np.isscalar(f) else np.cumsum(f / SR)


def pulso(f, n, duty=0.5):
    return np.where((fase(f, n) % 1.0) < duty, 1.0, -1.0)


def triangulo(f, n):
    return 4 * np.abs((fase(f, n) % 1.0) - 0.5) - 1


def ruido(n):
    return RNG.uniform(-1, 1, n)


def envolvente(n, ataque=0.005, decaida=0.08, sostenido=0.7, soltar=0.03):
    t = np.arange(n) / SR
    dur = n / SR
    e = np.ones(n) * sostenido
    a = t < ataque
    e[a] = t[a] / ataque
    d = (t >= ataque) & (t < ataque + decaida)
    e[d] = 1 - (1 - sostenido) * (t[d] - ataque) / decaida
    r = t > dur - soltar
    e[r] *= np.clip((dur - t[r]) / soltar, 0, 1)
    return e


def pasa_bajos(x, tau_ms):
    """Filtro pasa bajos aproximado (núcleo exponencial)."""
    k = max(1, int(SR * tau_ms / 1000))
    nucleo = np.exp(-np.arange(k * 5) / k)
    nucleo /= nucleo.sum()
    return np.convolve(x, nucleo)[: len(x)]


# ================================================================== percusión
def bombo(n):
    t = np.arange(n) / SR
    f = 40 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 12)


def caja(n):
    t = np.arange(n) / SR
    return (ruido(n) * 0.8 + np.sin(2 * np.pi * 185 * t) * 0.4) * np.exp(-t * 22)


def platillo(n):
    t = np.arange(n) / SR
    r = ruido(n)
    r = r - pasa_bajos(r, 0.15)
    return r * np.exp(-t * 60)


def taiko(n):
    t = np.arange(n) / SR
    f = 48 + 60 * np.exp(-t * 18)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) + ruido(n) * 0.15 * np.exp(-t * 60)) * np.exp(-t * 6)


# ================================================================== secuenciador
def parsear(patron):
    """'A4*4 F#4*2 -*2' -> [(nota|None, pasos)]"""
    out = []
    for tok in patron.split():
        nota, _, k = tok.partition("*")
        out.append((None if nota == "-" else nota, int(k or 1)))
    return out


def voz(patrones, bpm, instrumento, vol, vibrato=False, total_pasos=None):
    paso = 60 / bpm / 4
    notas = [x for p in patrones for x in parsear(p)]
    n_total = int(round(sum(k for _, k in notas) * paso * SR)) if total_pasos is None else int(round(total_pasos * paso * SR))
    buf = np.zeros(n_total)
    pos = 0.0
    for nota, k in notas:
        i0 = int(round(pos * SR)); dur = k * paso
        n = int(round(dur * SR))
        if nota:
            f = frec(nota)
            if vibrato and dur > 0.2:
                t = np.arange(n) / SR
                f = f * (1 + 0.006 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 0.15) / 0.2, 0, 1))
            s = instrumento(f, n) * envolvente(n, soltar=min(0.04, dur / 3)) * vol
            buf[i0:i0 + n] += s[: max(0, min(n, n_total - i0))]
        pos += dur
    return buf


def bateria(compases, bpm, vol=0.3):
    paso = 60 / bpm / 4
    n_total = int(round(sum(len(c[0]) for c in compases) * paso * SR))
    buf = np.zeros(n_total)
    i = 0
    for patron in compases:
        for k in range(len(patron[0])):
            i0 = int(round(i * paso * SR))
            for linea, fn, n, v in ((patron[0], bombo, 0.25, 1.0), (patron[1], caja, 0.18, 0.55), (patron[2], platillo, 0.06, 0.25),
                                    (patron[3] if len(patron) > 3 else "." * 16, taiko, 0.6, 1.0)):
                if linea[k] != ".":
                    m = int(n * SR)
                    s = fn(m) * v * vol
                    fin = min(i0 + m, n_total)
                    buf[i0:fin] += s[: fin - i0]
            i += 1
    return buf


ACORDES = {
    "D": ["D4", "F#4", "A4", "D5"], "Bm": ["B3", "D4", "F#4", "B4"], "G": ["G3", "B3", "D4", "G4"],
    "A": ["A3", "C#4", "E4", "A4"], "Am": ["A3", "C4", "E4", "A4"], "F": ["F3", "A3", "C4", "F4"],
    "E": ["E3", "G#3", "B3", "E4"], "C": ["C4", "E4", "G4", "C5"], "Em": ["E3", "G3", "B3", "E4"],
    "B": ["B3", "D#4", "F#4", "B4"], "Dm": ["D4", "F4", "A4", "D5"],
}
RAIZ_BAJO = {"D": "D2", "Bm": "B1", "G": "G1", "A": "A1", "Am": "A1", "F": "F1", "E": "E2", "C": "C2", "Em": "E2", "B": "B1"}


def quinta(nota):
    f = frec(nota) * 1.5
    midi = int(round(69 + 12 * np.log2(f / 440)))
    nombres = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    return f"{nombres[midi % 12]}{midi // 12 - 1}"


def octava(nota, k=1):
    i = 2 if nota[1] in "#b" else 1
    return nota[:i] + str(int(nota[i:]) + k)


def arpegio(acordes, figura, paso_k=2):
    out = []
    for a in acordes:
        c = ACORDES[a]
        out.append(" ".join(f"{c[i]}*{paso_k}" for i in figura))
    return out


def mezclar(*pistas):
    n = max(len(p) for p in pistas)
    m = np.zeros(n)
    for p in pistas:
        m[: len(p)] += p
    return m


def normalizar(x, pico=0.89):
    return x * (pico / (np.max(np.abs(x)) + 1e-9))


# los tonos puros suenan más fuertes que el ruido: se bajan para equilibrar
GANANCIA = {"sfx_menu": 0.4, "sfx_dialogo": 0.35, "sfx_danio": 0.55, "sfx_desbloqueo": 0.8, "sfx_pista": 0.8}


def exportar(nombre, x):
    os.makedirs(SALIDA, exist_ok=True)
    x = np.clip(normalizar(x, 0.89 * GANANCIA.get(nombre, 1.0)), -1, 1)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        ruta = tmp.name
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
    destino = os.path.join(SALIDA, nombre + ".ogg")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", ruta, "-c:a", "libvorbis", "-q:a", "5", destino], check=True)
    os.remove(ruta)
    return destino


# ================================================================== música
def musica_exploracion():
    bpm = 100
    acordes = ["D", "Bm", "G", "A", "D", "Bm", "G", "D"] + ["Bm", "G", "D", "A", "Bm", "G", "A", "A"]
    melodia = [
        "A4*4 F#4*2 E4*2 D4*4 E4*4", "F#4*6 A4*2 B4*4 A4*4", "D5*4 B4*2 A4*2 B4*8", "A4*12 -*4",
        "A4*4 F#4*2 E4*2 D4*4 E4*2 F#4*2", "A4*6 B4*2 D5*4 E5*4", "F#5*4 E5*2 D5*2 B4*4 A4*4", "D5*12 -*4",
        "B4*4 D5*4 E5*4 F#5*4", "E5*6 D5*2 B4*8", "A4*4 B4*4 D5*4 A4*4", "E5*12 -*4",
        "B4*4 D5*4 E5*4 A5*4", "F#5*6 E5*2 D5*8", "E5*4 D5*2 B4*2 A4*4 F#4*4", "A4*8 -*8",
    ]
    lead = voz(melodia, bpm, triangulo, 0.5, vibrato=True)
    arp = voz(arpegio(acordes, [0, 1, 2, 3, 2, 1, 2, 1]), bpm, lambda f, n: pulso(f, n, 0.125), 0.1)
    bajo = voz([f"{RAIZ_BAJO[a]}*8 {quinta(RAIZ_BAJO[a])}*8" for a in acordes], bpm, triangulo, 0.45)
    bat = bateria([("k.......k.......", "................", "..h...h...h...h.")] * 16, bpm, 0.25)
    return mezclar(lead, arp, bajo, bat)


def musica_pelea():
    bpm = 144
    acordes = ["Am", "G", "F", "E", "Am", "G", "F", "E"] + ["Am", "C", "G", "E", "Am", "C", "D" if False else "G", "E"]
    melodia = [
        "E5*2 E5*2 D5*2 E5*2 G5*4 E5*4", "D5*2 D5*2 C5*2 D5*2 E5*4 D5*4", "C5*2 C5*2 A4*2 C5*2 D5*4 C5*2 A4*2", "B4*8 G#4*4 E4*4",
        "A5*4 G5*2 E5*2 G5*4 A5*4", "G5*2 E5*2 D5*4 E5*8", "C5*4 D5*4 E5*4 G5*4", "E5*12 -*4",
        "A4*2 C5*2 E5*2 A5*2 G5*4 E5*4", "C5*2 E5*2 G5*2 C6*2 A5*8", "G5*4 D5*4 G5*4 B5*4", "G#5*8 E5*8",
        "A5*2 G5*2 E5*2 D5*2 E5*4 A4*4", "C5*2 D5*2 E5*2 G5*2 E5*8", "D5*4 G5*4 B5*4 D6*4", "E5*4 G#5*4 B5*8",
    ]
    lead = voz(melodia, bpm, lambda f, n: pulso(f, n, 0.25), 0.3, vibrato=True)
    arp = voz(arpegio(acordes, [0, 1, 2, 1] * 4, 1), bpm, lambda f, n: pulso(f, n, 0.125), 0.07)
    bajo = voz([" ".join(f"{n}*2" for n in (r, r, octava(r), r, r, octava(r), r, quinta(r))) for r in (RAIZ_BAJO[a] for a in acordes)],
               bpm, triangulo, 0.5)
    patron = ("k.....k.k.......", "....s.......s...", "h.h.h.h.h.h.h.h.")
    final = ("k.....k.k...k.k.", "....s.......s.ss", "h.h.h.h.h.h.h.h.")
    bat = bateria([patron] * 7 + [final] + [patron] * 7 + [final], bpm, 0.32)
    return mezclar(lead, arp, bajo, bat)


def musica_jefe():
    bpm = 150
    acordes = ["Em", "F", "Em", "D" if False else "C", "Em", "F", "C", "B"] + ["Em", "C", "Am", "B", "Em", "C", "Am", "B"]
    melodia = [
        "E5*6 F5*2 G5*4 B5*4", "A5*6 G5*2 F5*8", "E5*4 G5*4 B5*4 E6*4", "C6*8 B5*4 G5*4",
        "B5*6 A5*2 G5*4 F5*4", "E5*4 F5*4 A5*4 C6*4", "B5*4 A5*4 G5*4 E5*4", "F#5*8 D#5*8",
        "E6*2 B5*2 G5*2 E5*2 G5*2 B5*2 E6*4", "C6*4 G5*4 E5*4 G5*4", "A5*6 C6*2 E6*8", "D#6*8 B5*8",
        "E6*4 D6*2 B5*2 G5*4 E5*4", "G5*4 C6*4 E6*4 D6*4", "C6*4 B5*2 A5*2 E5*8", "F#5*4 A5*4 B5*8",
    ]
    lead = voz(melodia, bpm, lambda f, n: pulso(f, n, 0.5), 0.26, vibrato=True)
    pad = voz([" ".join(f"{n}*16" for n in [ACORDES[a][1]]) for a in acordes], bpm, lambda f, n: pulso(f, n, 0.25), 0.08)
    pad2 = voz([" ".join(f"{n}*16" for n in [ACORDES[a][2]]) for a in acordes], bpm, lambda f, n: pulso(f, n, 0.25), 0.07)
    bajo = voz([" ".join(f"{n}*1" for n in (r, r, octava(r), r, quinta(r), r, octava(r), r) * 2) for r in (RAIZ_BAJO[a] for a in acordes)],
               bpm, lambda f, n: pulso(f, n, 0.5), 0.2)
    patron = ("k..k..k.k..k..k.", "....s.......s...", "h.hhh.hhh.hhh.hh", "t.......t.......")
    final = ("k..k..k.k..k.kkk", "....s.......ssss", "h.hhh.hhh.hhh.hh", "t...t...t.t.tttt")
    bat = bateria([patron] * 7 + [final] + [patron] * 7 + [final], bpm, 0.32)
    return mezclar(lead, pad, pad2, bajo, bat)


# ================================================================== efectos de sonido
def _ajustar(x, n):
    return x[:n] if len(x) >= n else np.concatenate([x, np.zeros(n - len(x))])


def t_(seg):
    return np.arange(int(seg * SR)) / SR


def barrido(f0, f1, seg, fn=lambda f, n: pulso(f, n, 0.5), curva=1.0):
    t = t_(seg)
    f = f0 + (f1 - f0) * (t / seg) ** curva
    return fn(f, len(t))


def sfx_fuego():
    t = t_(0.45)
    r = pasa_bajos(ruido(len(t)), 0.25)
    rugido = r * np.exp(-t * 6) * np.clip(t / 0.02, 0, 1)
    chispas = (ruido(len(t)) > 0.97) * ruido(len(t)) * np.exp(-t * 5) * 0.6
    tono = barrido(110, 60, 0.45, triangulo) * np.exp(-t * 8) * 0.5
    return rugido * 1.4 + chispas + tono


def sfx_aire():
    t = t_(0.5)
    r = ruido(len(t))
    lento, rapido = pasa_bajos(r, 1.2), pasa_bajos(r, 0.12)
    mezcla = np.sin(np.pi * t / 0.5)
    return (lento * (1 - t / 0.5) + rapido * (t / 0.5)) * mezcla * 2


def sfx_agua():
    out = []
    for i, f in enumerate((520, 680, 900, 760, 1100)):
        t = t_(0.06)
        s = np.sin(2 * np.pi * np.cumsum(f * (1 + 2.5 * t / 0.06)) / SR) * np.exp(-t * 40)
        out.append(s * (0.8 if i % 2 else 1))
    burbujas = np.concatenate(out)
    t = t_(len(burbujas) / SR)
    chapoteo = pasa_bajos(ruido(len(t)), 0.08) * np.exp(-t * 14) * 0.8
    return burbujas + chapoteo


def sfx_tierra():
    t = t_(0.5)
    golpe = barrido(90, 35, 0.5, lambda f, n: np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 7)
    crujido = pasa_bajos(ruido(len(t)), 0.6) * np.exp(-t * 10) * 1.6
    return golpe + crujido


def sfx_golpe():
    t = t_(0.15)
    return (ruido(len(t)) * np.exp(-t * 60) + np.sin(2 * np.pi * np.cumsum(140 - 80 * t / 0.15) / SR) * np.exp(-t * 25))


def sfx_danio():
    t = t_(0.25)
    return barrido(520, 180, 0.25, lambda f, n: pulso(f, n, 0.25)) * np.exp(-t * 6) * 0.7


def sfx_derribo():
    t = t_(0.9)
    caida = barrido(440, 70, 0.9, lambda f, n: pulso(f, n, 0.5), curva=0.6) * np.exp(-t * 2.5) * 0.5
    golpe = _ajustar(np.concatenate([np.zeros(int(0.55 * SR)), bombo(int(0.35 * SR))]), len(caida))
    return caida + golpe


def sfx_puerta():
    t = t_(1.3)
    retumbe = pasa_bajos(ruido(len(t)), 2.0) * 3.0
    raspado = pasa_bajos(ruido(len(t)), 0.3) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t)) * 0.8
    env = np.clip(t / 0.1, 0, 1) * np.clip((1.3 - t) / 0.3, 0, 1)
    golpe_final = _ajustar(np.concatenate([np.zeros(int(1.0 * SR)), taiko(int(0.3 * SR))]), len(t))
    return (retumbe + raspado) * env + golpe_final * 0.8


def sfx_pista():
    out = []
    for f in ("E5", "G#5", "B5", "E6"):
        n = int(0.08 * SR)
        out.append(triangulo(frec(f), n) * envolvente(n, decaida=0.05, sostenido=0.4))
    n = int(0.3 * SR)
    out.append(triangulo(frec("E6"), n) * envolvente(n, decaida=0.2, sostenido=0.3, soltar=0.15) * 0.8)
    return np.concatenate(out)


def sfx_desbloqueo():
    pasos = [("C5", .1), ("E5", .1), ("G5", .1), ("C6", .1), ("E6", .1), ("G6", .5)]
    out = []
    for nota, d in pasos:
        n = int(d * SR)
        s = pulso(frec(nota), n, 0.25) * 0.5 + triangulo(frec(nota) / 2, n) * 0.5
        out.append(s * envolvente(n, decaida=0.05, sostenido=0.6, soltar=min(0.08, d / 2)))
    x = np.concatenate(out)
    t = np.arange(len(x)) / SR
    brillo = (ruido(len(x)) > 0.985) * 0.4 * np.clip((t - 0.4) / 0.2, 0, 1)
    return x + brillo


def sfx_dialogo():
    n = int(0.045 * SR)
    return pulso(frec("A5"), n, 0.5) * envolvente(n, decaida=0.02, sostenido=0.4, soltar=0.015) * 0.5


def sfx_menu():
    a = int(0.05 * SR); b = int(0.08 * SR)
    return np.concatenate([pulso(frec("E6"), a, 0.25) * envolvente(a, soltar=0.01),
                           pulso(frec("B6"), b, 0.25) * envolvente(b, soltar=0.04)]) * 0.5


SFX = {n: f for n, f in globals().items() if n.startswith("sfx_")}
MUSICA = {"musica_exploracion": musica_exploracion, "musica_pelea": musica_pelea, "musica_jefe": musica_jefe}

if __name__ == "__main__":
    for n, fn in {**MUSICA, **SFX}.items():
        x = fn()
        exportar(n, x)
        print(f"{n}: {len(x) / SR:.1f} s")
