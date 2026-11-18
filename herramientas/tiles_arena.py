"""Arena final: plataforma de piedra en las alturas, nubes, columnas, banderas y pilares del sello.

Genera:
  juego/assets/tilesets/tiles_arena.png (+ .json) y arena/<nombre>.png
  juego/assets/tilesets/obj_<nombre>.png  (columna, columna_rota, bandera_0..2, mosaico_aire, pilar_entero, pilar_roto)
  juego/assets/tilesets/fondo_arena_final.png (640x360)
Uso: python3 herramientas/tiles_arena.py
"""
import json
import math
import os
import random
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from paleta import a_rgb, fuera_de_paleta
from tiles_ciudad import Lienzo, RAIZ, T

TS = os.path.join(RAIZ, "juego", "assets", "tilesets")
CIELO = "#8FD3F0"
NUBE = ["#C8C8C0", "#F2F7FA", "#F4F1E8"]


# ================================================================== suelo de la plataforma
def plataforma(semilla=1, grieta=False):
    L = Lienzo(fondo="#9AA3A8")
    rnd = random.Random(semilla)
    for by in (0, 16):
        for bx in (0, 16):
            base = "#C8C8C0"
            L.rect(bx + 1, by + 1, bx + 14, by + 14, base)
            L.rect(bx + 1, by + 1, bx + 14, by + 1, "#F4F1E8")
            L.rect(bx + 1, by + 1, bx + 1, by + 14, "#F4F1E8")
            L.rect(bx + 2, by + 14, bx + 14, by + 14, "#9AA3A8")
            L.rect(bx + 14, by + 2, bx + 14, by + 14, "#9AA3A8")
            for _ in range(3):
                L.px(bx + rnd.randrange(3, 13), by + rnd.randrange(3, 13), "#9AA3A8")
            if rnd.random() < 0.3:
                L.px(bx + rnd.randrange(3, 13), by + rnd.randrange(3, 13), "#F4F1E8")
    if grieta:
        for x, y in ((5, 18), (6, 19), (7, 19), (8, 20), (9, 22), (10, 23), (11, 23), (12, 25), (9, 21)):
            L.px(x, y, "#5A5566")
        for x, y in ((22, 3), (23, 4), (23, 5), (24, 6)):
            L.px(x, y, "#5A5566")
    return L.img


def _cara(L, y0, y1):
    """Cara lateral de piedra de la plataforma (bloques) que cae hacia las nubes."""
    for y in range(y0, y1 + 1):
        fila = (y - y0) // 6
        off = 8 if fila % 2 else 0
        for x in range(32):
            c = "#9AA3A8"
            if (y - y0) % 6 == 5:
                c = "#5A5566"
            elif (x + off) % 16 == 0:
                c = "#5A5566"
            elif (y - y0) % 6 == 0:
                c = "#C8C8C0"
            L.px(x, y, c)


def borde_s():
    """Borde sur: losa, reborde dorado y cara de piedra."""
    L = Lienzo.de(plataforma(3))
    L.rect(0, 12, 31, 13, "#C9A227")
    L.rect(0, 12, 31, 12, "#E8D27A")
    _cara(L, 14, 31)
    return L.img


def cara_inferior():
    """Continuación de la cara de piedra que se pierde entre las nubes."""
    L = Lienzo(fondo=CIELO)
    _cara(L, 0, 17)
    for x in range(32):
        lim = 16 + round(2 * math.sin(x * 0.45) + math.sin(x * 1.3))
        for y in range(lim, 32):
            L.px(x, y, NUBE[2] if y > lim + 1 else NUBE[0])
    return L.img


def borde_n():
    """Borde norte: barandilla baja de piedra con nubes detrás."""
    L = Lienzo.de(plataforma(5))
    L.rect(0, 0, 31, 9, CIELO)
    for x in range(32):
        lim = 5 + round(1.5 * math.sin(x * 0.5))
        for y in range(lim, 10):
            L.px(x, y, NUBE[1] if y > lim else NUBE[0])
    L.rect(0, 10, 31, 15, "#C8C8C0")
    L.rect(0, 10, 31, 10, "#F4F1E8")
    L.rect(0, 15, 31, 15, "#5A5566")
    for x in range(0, 32, 8):
        L.rect(x, 11, x, 14, "#9AA3A8")
    L.rect(0, 16, 31, 17, "#9AA3A8")
    return L.img


def borde_lado(lado):
    """Borde este u oeste: losa con reborde y cielo al costado."""
    L = Lienzo.de(plataforma(7))
    xs = range(26, 32) if lado == "e" else range(0, 6)
    for x in xs:
        for y in range(32):
            L.px(x, y, CIELO)
    xr = 24 if lado == "e" else 6
    L.rect(xr, 0, xr + 1, 31, "#C9A227")
    L.rect(xr, 0, xr, 31, "#E8D27A") if lado == "o" else L.rect(xr + 1, 0, xr + 1, 31, "#7A5230")
    return L.img


def cielo(semilla=1):
    L = Lienzo(fondo=CIELO)
    rnd = random.Random(semilla)
    for _ in range(6):
        L.px(rnd.randrange(32), rnd.randrange(32), "#F2F7FA")
    return L.img


def nubes(semilla=2):
    L = Lienzo(fondo=NUBE[2])
    rnd = random.Random(semilla)
    for _ in range(7):
        cx, cy, r = rnd.randrange(32), rnd.randrange(32), rnd.randrange(4, 8)
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                d = (x - cx) ** 2 + (y - cy) ** 2
                if r * r * 0.7 < d <= r * r and y > cy:
                    L.px(x, y, NUBE[0], envolver=True)
                elif d <= r * r * 0.3 and y < cy:
                    L.px(x, y, NUBE[1], envolver=True)
    return L.img


def nubes_borde(arriba=True):
    """Nubes que se abren al cielo (arriba=True: cielo arriba, nubes abajo)."""
    L = Lienzo.de(nubes(4))
    for x in range(32):
        lim = 14 + round(3 * math.sin(x * 0.4) + 1.5 * math.sin(x * 1.1))
        for y in range(32):
            v = y if arriba else 31 - y
            if v < lim:
                L.px(x, y, CIELO)
            elif v < lim + 2:
                L.px(x, y, NUBE[1])
    return L.img


# ================================================================== objetos
def columna(rota=False):
    L = Lienzo(32, 64)
    L.sombra_suelo(16, 61, 12, 2)
    top = 22 if rota else 6
    L.rect(8, top, 23, 57, "#C8C8C0")
    L.rect(8, top, 10, 57, "#F4F1E8")
    L.rect(21, top, 23, 57, "#9AA3A8")
    for x in (13, 17):
        L.rect(x, top, x, 57, "#9AA3A8")
    L.rect(5, 56, 26, 61, "#9AA3A8")
    L.rect(5, 56, 26, 56, "#F4F1E8")
    L.rect(5, 61, 26, 61, "#5A5566")
    if rota:
        for x in range(8, 24):
            L.px(x, top + (x * 7) % 4, (0, 0, 0, 0)) if False else None
        pts = [(8, top), (12, top - 4), (15, top + 1), (19, top - 5), (23, top - 1)]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L.linea(x0, y0, x1, y1, "#9AA3A8")
        for x in range(8, 24):
            for y in range(top - 6, top):
                pass
        for cx, cy in ((4, 58), (27, 59), (29, 55)):
            L.circulo(cx, cy, 2.5, "#C8C8C0"); L.px(cx - 1, cy - 1, "#F4F1E8")
    else:
        L.rect(4, 1, 27, 6, "#C9A227")
        L.rect(4, 1, 27, 1, "#E8D27A")
        L.rect(6, 7, 25, 8, "#C9A227")
        L.rect(6, 8, 25, 8, "#7A5230")
        for x in (8, 15, 22):
            L.circulo(x, 4, 1.5, "#E8D27A")
    L.contorno()
    return L.img


def bandera(f):
    """Bandera de El Ciclo Roto ondeando (32x64), cuadro f de 0 a 2."""
    L = Lienzo(32, 64)
    L.sombra_suelo(8, 61, 6, 2)
    L.rect(6, 2, 7, 61, "#5A5566")
    L.rect(6, 2, 6, 61, "#9AA3A8")
    L.circulo(6.5, 2, 2, "#C9A227")
    for x in range(8, 30):
        k = x - 8
        dy = round(2 * math.sin(k * 0.35 + f * 2.1) * (k / 22))
        for y in range(6 + dy, 34 + dy):
            c = "#3B3846"
            if (k + f * 3) % 11 < 2:
                c = "#24222B"
            elif y == 6 + dy or y == 33 + dy:
                c = "#E8D27A"
            L.px(x, y, c)
        if x > 26:
            for y in range(28 + dy, 34 + dy):
                L.px(x, y, (0, 0, 0, 0)) if False else None
    cx = 18
    cy = 20 + round(2 * math.sin(10 * 0.35 + f * 2.1) * (10 / 22))
    L.circulo(cx, cy, 6, "#E8D27A", r_in=0.7)
    for x, y in ((cx, cy - 7), (cx + 7, cy), (cx, cy + 7), (cx - 7, cy)):
        L.px(x, y, "#E8D27A")
    L.linea(cx - 5, cy + 5, cx + 5, cy - 5, "#D9481E")
    L.contorno()
    return L.img


def mosaico_aire():
    """Mosaico central de 64x64 con el remolino del aire en dorado."""
    L = Lienzo(64, 64)
    for ty in (0, 32):
        for tx in (0, 32):
            L.img.paste(plataforma(9 + tx + ty), (tx, ty))
    L.p = L.img.load()
    L.circulo(32, 32, 28, "#C9A227", r_in=0.9)
    L.circulo(32, 32, 26, "#F4F1E8")
    L.circulo(32, 32, 26, "#E8D27A", r_in=0.94)
    for k in range(3):
        pts = []
        for i in range(30):
            a = k * 2 * math.pi / 3 + i * 0.2
            r = 3 + i * 0.7
            pts.append((32 + r * math.cos(a), 32 + r * math.sin(a)))
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L.linea(int(x0), int(y0), int(x1), int(y1), "#C9A227")
    L.circulo(32, 32, 3, "#C9A227")
    L.px(31, 31, "#E8D27A")
    return L.img


def pilar(roto=False):
    """Pilar del sello (32x64): obelisco oscuro con runas que brillan; roto = escombros apagados."""
    L = Lienzo(32, 64)
    L.sombra_suelo(16, 61, 13, 2)
    if roto:
        L.rect(9, 46, 22, 59, "#3B3846")
        L.rect(9, 46, 11, 59, "#5A5566")
        for (x0, y0, x1, y1) in ((9, 46, 13, 42), (13, 42, 17, 47), (17, 47, 22, 43)):
            L.linea(x0, y0, x1, y1, "#5A5566")
        for cx, cy, r in ((5, 57, 3), (26, 58, 3.5), (24, 52, 2), (7, 51, 2)):
            L.circulo(cx, cy, r, "#3B3846"); L.px(int(cx - 1), int(cy - 1), "#5A5566")
        L.px(15, 52, "#7A5230"); L.px(18, 55, "#7A5230")
        L.rect(5, 59, 26, 61, "#24222B")
        L.contorno()
        return L.img
    d = ImageDraw.Draw(L.img)
    d.polygon([(10, 58), (12, 8), (16, 2), (20, 8), (22, 58)], fill=a_rgb("#3B3846") + (255,))
    d.polygon([(10, 58), (12, 8), (16, 2), (15, 58)], fill=a_rgb("#5A5566") + (255,))
    L.p = L.img.load()
    L.rect(6, 56, 25, 61, "#24222B"); L.rect(6, 56, 25, 56, "#3B3846")
    # runas brillantes
    for y in range(14, 52, 7):
        L.rect(14, y, 18, y, "#E8D27A")
        L.px(15, y + 1, "#C9A227"); L.px(17, y - 1, "#C9A227")
    L.circulo(16, 10, 2.5, "#E8D27A"); L.px(16, 10, "#F4F1E8")
    # destellos alrededor
    for x, y in ((6, 20), (26, 30), (5, 40), (27, 14)):
        L.px(x, y, "#E8D27A")
    L.contorno()
    return L.img


# ================================================================== hoja y fondo
def construir():
    return [
        ("plataforma", plataforma()), ("plataforma_b", plataforma(11)), ("plataforma_grieta", plataforma(12, True)),
        ("borde_s", borde_s()), ("cara_inferior", cara_inferior()), ("borde_n", borde_n()),
        ("borde_e", borde_lado("e")), ("borde_o", borde_lado("o")),
        ("cielo", cielo()), ("nubes", nubes()), ("nubes_borde_arriba", nubes_borde(True)),
        ("nubes_borde_abajo", nubes_borde(False)),
    ]


def objetos():
    o = {"columna": columna(), "columna_rota": columna(True), "mosaico_aire": mosaico_aire(),
         "pilar_entero": pilar(), "pilar_roto": pilar(True)}
    for f in range(3):
        o[f"bandera_{f}"] = bandera(f)
    return o


def guardar(tiles):
    suelto = os.path.join(TS, "arena")
    os.makedirs(suelto, exist_ok=True)
    cols = 8
    hoja = Image.new("RGBA", (cols * T, ((len(tiles) + cols - 1) // cols) * T), (0, 0, 0, 0))
    indice = {}
    for i, (n, img) in enumerate(tiles):
        assert not fuera_de_paleta(img), (n, fuera_de_paleta(img))
        hoja.alpha_composite(img, ((i % cols) * T, (i // cols) * T))
        img.save(os.path.join(suelto, n + ".png"))
        indice[i] = n
    hoja.save(os.path.join(TS, "tiles_arena.png"))
    with open(os.path.join(TS, "tiles_arena.json"), "w") as fh:
        json.dump({"tamano_tile": T, "columnas": cols, "tiles": indice}, fh, indent=2, ensure_ascii=False)
    for n, img in objetos().items():
        assert not fuera_de_paleta(img), (n, fuera_de_paleta(img))
        img.save(os.path.join(TS, f"obj_{n}.png"))
    return hoja


def fondo_arena(tiles):
    """Arena final 640x360: plataforma de 16x8 tiles rodeada de cielo y nubes."""
    t = dict(tiles); o = objetos()
    img = Image.new("RGBA", (640, 360), a_rgb(CIELO) + (255,))
    for y in range(12):
        for x in range(20):
            if x < 2 or x > 17 or y < 1 or y > 9:
                n = "nubes" if y >= 10 else ("nubes_borde_abajo" if y == 0 else "cielo")
                if (x < 2 or x > 17) and y >= 8:
                    n = "nubes_borde_arriba" if y == 8 else "nubes"
                img.alpha_composite(t[n], (x * T, y * T))
    for x in range(2, 18):
        img.alpha_composite(t["borde_n"], (x * T, 1 * T))
        for y in range(2, 9):
            n = ("plataforma", "plataforma_b", "plataforma", "plataforma_grieta")[(x * 5 + y * 3) % 4]
            img.alpha_composite(t[n], (x * T, y * T))
        img.alpha_composite(t["borde_s"], (x * T, 9 * T))
        img.alpha_composite(t["cara_inferior"], (x * T, 10 * T))
    for y in range(2, 10):
        img.alpha_composite(t["borde_o"], (1 * T, y * T))
        img.alpha_composite(t["borde_e"], (18 * T, y * T))
    img.alpha_composite(o["mosaico_aire"], (9 * T, 5 * T))
    for x, n in ((2 * T + 4, "columna"), (17 * T - 4, "columna_rota")):
        img.alpha_composite(o[n], (x, 1 * T - 20))
    for x, n in ((2 * T + 4, "columna_rota"), (17 * T - 4, "columna")):
        img.alpha_composite(o[n], (x, 8 * T - 8))
    for x in (5 * T, 8 * T, 11 * T, 14 * T):
        img.alpha_composite(o["bandera_0"], (x, 0))
    return img


if __name__ == "__main__":
    tiles = construir()
    hoja = guardar(tiles)
    prev = os.path.join(RAIZ, "arte_fuente", "previews")
    hoja.resize((hoja.width * 3, hoja.height * 3), Image.NEAREST).save(os.path.join(prev, "tiles_arena_x3.png"))
    f = fondo_arena(tiles)
    assert not fuera_de_paleta(f), fuera_de_paleta(f)
    f.save(os.path.join(TS, "fondo_arena_final.png"))
    # prueba con personajes, pilares y sello
    b = os.path.join(RAIZ, "juego", "assets")
    p = f.copy()
    o = objetos()
    sello = Image.open(os.path.join(b, "efectos", "efecto_sello_1.png")).convert("RGBA")
    p.alpha_composite(sello, (300 - 32, 200 - 48))
    for x, y in ((150, 110), (470, 110), (310, 250)):
        p.alpha_composite(o["pilar_entero"], (x, y))
    p.alpha_composite(o["pilar_roto"], (230, 240))
    for s, x, y in (("personajes/ryu_poder_abajo_1", 300, 170), ("personajes/gao_golpe_derecha_1", 120, 140),
                    ("personajes/nerea_reposo_abajo_0", 420, 190), ("personajes/norbu_reposo_abajo_0", 304, 80)):
        p.alpha_composite(Image.open(os.path.join(b, s + ".png")).convert("RGBA"), (x, y))
    p.resize((1280, 720), Image.NEAREST).save(os.path.join(prev, "prueba_arena_final.png"))
    ho = Image.new("RGBA", (sum(i.width + 8 for i in o.values()) + 8, 72), a_rgb("#3B3846") + (255,))
    x = 8
    for i in o.values():
        ho.alpha_composite(i, (x, 4)); x += i.width + 8
    ho.resize((ho.width * 3, ho.height * 3), Image.NEAREST).save(os.path.join(prev, "objetos_arena.png"))
    print(len(tiles), "tiles,", len(o), "objetos")
