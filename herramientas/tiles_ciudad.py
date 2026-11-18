"""Tileset de la ciudad (Nación del Fuego), tiles de 32x32, paleta oficial.

Genera:
  juego/assets/tilesets/tiles_ciudad.png        hoja de tiles (8 columnas)
  juego/assets/tilesets/tiles_ciudad.json       índice -> nombre
  juego/assets/tilesets/ciudad/<nombre>.png     cada tile suelto (para Tiled Sprite en GDevelop)
  juego/assets/tilesets/obj_fuente_<n>.png      fuente 64x64, 3 cuadros
  juego/assets/tilesets/fondo_pelea_plaza.png   640x360
  arte_fuente/previews/mapa_ciudad_ejemplo.png  mapa de muestra
Uso: python3 herramientas/tiles_ciudad.py
"""
import json
import math
import os
import random
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from paleta import CONTORNO, a_rgb, fuera_de_paleta

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
T = 32


class Lienzo:
    def __init__(self, w=T, h=T, fondo=None):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w, h), (0, 0, 0, 0) if fondo is None else a_rgb(fondo) + (255,))
        self.p = self.img.load()

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[x, y] = a_rgb(c) + (255,)

    def get(self, x, y):
        return self.p[x % self.w, y % self.h]

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def circulo(self, cx, cy, r, c, r_in=-1):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
                if r_in < d <= r:
                    self.px(x, y, c)

    def linea(self, x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0)) or 1
        for i in range(n + 1):
            self.px(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)

    def contorno(self):
        lleno = {(x, y) for y in range(self.h) for x in range(self.w) if self.p[x, y][3]}
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) not in lleno and any((x + dx, y + dy) in lleno for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    self.px(x, y, CONTORNO)
        return self


# ================================================================== suelos
def calle(semilla=1, grieta=False):
    """Ladrillo rojizo en aparejo de soga, sin costuras."""
    L = Lienzo(fondo="#6E4426")
    rnd = random.Random(semilla)
    for fila in range(8):
        off = 4 if fila % 2 else 0
        for col in range(5):
            x0 = col * 8 - off
            c = rnd.choices(["#A86B3C", "#7A5230", "#D9A06B"], [7, 2, 1])[0]
            for y in range(fila * 4, fila * 4 + 3):
                for x in range(x0, x0 + 7):
                    L.px(x % T, y, c)
            L.px((x0) % T, fila * 4, "#D9A06B" if c != "#D9A06B" else "#F2C9A0")
            L.px((x0 + 6) % T, fila * 4 + 2, "#6E4426")
    if grieta:
        for x, y in ((6, 9), (7, 10), (8, 10), (9, 11), (10, 12), (11, 12), (12, 13), (13, 14)):
            L.px(x, y, "#4A3B32")
    return L.img


def acera():
    L = Lienzo(fondo="#C8C8C0")
    rnd = random.Random(7)
    for by in (0, 16):
        for bx in (0, 16):
            L.rect(bx, by, bx + 15, by, "#F4F1E8")
            L.rect(bx, by, bx, by + 15, "#F4F1E8")
            L.rect(bx + 15, by, bx + 15, by + 15, "#9AA3A8")
            L.rect(bx, by + 15, bx + 15, by + 15, "#9AA3A8")
    for _ in range(14):
        L.px(rnd.randrange(1, 31), rnd.randrange(1, 31), "#9AA3A8")
    return L.img


def acera_borde():
    """Acera con bordillo en el lado sur; debajo empieza la calle."""
    img = acera()
    L = Lienzo()
    L.img = img; L.p = img.load()
    L.rect(0, 24, 31, 27, "#9AA3A8")
    L.rect(0, 24, 31, 24, "#F4F1E8")
    L.rect(0, 27, 31, 27, "#5A5566")
    L.rect(0, 28, 31, 31, "#4A3B32")
    for x in range(0, 32, 8):
        L.px(x, 25, "#5A5566"); L.px(x, 26, "#5A5566")
    return img


def plaza(semilla=3):
    """Adoquines dorados de la plaza."""
    L = Lienzo(fondo="#4A3B32")
    rnd = random.Random(semilla)
    for fila in range(4):
        off = 4 if fila % 2 else 0
        for col in range(5):
            x0, y0 = col * 8 - off, fila * 8
            base = rnd.choices(["#C29A5B", "#D9A06B", "#A86B3C"], [6, 3, 1])[0]
            for y in range(y0, y0 + 7):
                for x in range(x0, x0 + 7):
                    esquina = (x - x0 in (0, 6)) and (y - y0 in (0, 6))
                    if esquina:
                        continue
                    c = base
                    if y == y0 or x == x0:
                        c = "#E8D27A"
                    elif y == y0 + 6 or x == x0 + 6:
                        c = "#7A5230"
                    L.px(x % T, y, c)
    return L.img


def pasto(flores=False, semilla=5):
    L = Lienzo(fondo="#6B8E3D")
    rnd = random.Random(semilla)
    for _ in range(18):
        x, y = rnd.randrange(32), rnd.randrange(32)
        L.px(x, y, "#3F5A2A"); L.px(x - 1, y - 1, "#3F5A2A"); L.px(x + 1, y - 1, "#3F5A2A")
    for _ in range(10):
        L.px(rnd.randrange(32), rnd.randrange(32), "#C29A5B")
    if flores:
        for (x, y), c in zip(((6, 8), (22, 5), (14, 20), (26, 24), (5, 26)),
                             ("#F28C28", "#E8D27A", "#F4F1E8", "#D9481E", "#E8D27A")):
            for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                L.px(x + dx, y + dy, c)
            L.px(x, y, "#C9A227")
    return L.img


# ================================================================== edificios
def pared(semilla=11):
    L = Lienzo(fondo="#F2C9A0")
    rnd = random.Random(semilla)
    for _ in range(16):
        L.px(rnd.randrange(32), rnd.randrange(32), "#D9A06B")
    for _ in range(8):
        L.px(rnd.randrange(32), rnd.randrange(32), "#F4F1E8")
    return L.img


def _sobre(img):
    L = Lienzo()
    L.img = img.copy(); L.p = L.img.load()
    return L


def pared_ventana():
    L = _sobre(pared())
    # toldo rojo a rayas
    for x in range(6, 26):
        c = "#D9481E" if (x // 2) % 2 == 0 else "#F28C28"
        L.rect(x, 3, x, 6, c)
    L.rect(5, 7, 26, 7, "#8E1B1B")
    # marco y vidrio
    L.rect(8, 9, 23, 23, "#4A3B32")
    L.rect(9, 10, 22, 22, "#7A5230")
    L.rect(10, 11, 21, 21, "#1E4F8C")
    L.rect(10, 11, 21, 12, "#3A86C8")
    for i in range(5):
        L.px(12 + i, 15 - i, "#8FD3F0")
    L.px(19, 18, "#8FD3F0")
    L.rect(15, 11, 16, 21, "#7A5230")
    L.rect(10, 16, 21, 16, "#7A5230")
    L.rect(7, 24, 24, 25, "#C29A5B")
    L.rect(7, 26, 24, 26, "#7A5230")
    return L.img


def pared_puerta():
    L = _sobre(pared())
    L.rect(7, 4, 24, 6, "#8E1B1B")
    L.rect(7, 4, 24, 4, "#C9A227")
    L.rect(9, 7, 22, 31, "#4A3B32")
    L.rect(10, 8, 21, 31, "#7A5230")
    for x in (13, 16, 19):
        L.rect(x, 8, x, 31, "#4A3B32")
    L.rect(10, 8, 21, 8, "#C29A5B")
    L.rect(18, 19, 19, 20, "#C9A227")
    L.px(18, 19, "#E8D27A")
    return L.img


def pared_simbolo():
    """Pista 1: el símbolo de El Ciclo Roto pintado en la pared."""
    L = _sobre(pared())
    tinta = "#24222B"
    L.circulo(16, 15, 10, tinta, r_in=8)
    # cuatro marcas de los elementos
    for x, y in ((16, 4), (15, 5), (17, 5)):           # fuego (arriba)
        L.px(x, y, tinta)
    for x in range(25, 29):                             # agua (derecha)
        L.px(x, 14 + (x % 2), tinta)
    L.rect(15, 25, 17, 27, tinta)                       # tierra (abajo)
    for x, y in ((4, 14), (5, 13), (6, 14), (5, 16), (4, 16)):  # aire (izquierda)
        L.px(x, y, tinta)
    # línea diagonal que lo parte
    for i in range(-11, 12):
        L.px(16 + i, 15 - i, "#8E1B1B")
        L.px(17 + i, 15 - i, "#8E1B1B")
    # chorreones de pintura
    for x, y0, n in ((8, 21, 4), (21, 21, 3), (12, 25, 3)):
        L.rect(x, y0, x, y0 + n, tinta)
    return L.img


def zocalo():
    L = _sobre(pared())
    L.rect(0, 22, 31, 31, "#8E1B1B")
    L.rect(0, 22, 31, 23, "#C9A227")
    L.rect(0, 24, 31, 24, "#7A5230")
    L.rect(0, 31, 31, 31, "#4A3B32")
    return L.img


def techo(base, luz, sombra, linea):
    L = Lienzo(fondo=base)
    for fila in range(4):
        y0 = fila * 8
        off = 4 if fila % 2 else 0
        for col in range(5):
            x0 = col * 8 - off
            for x in range(x0, x0 + 8):
                xx = x % T
                L.px(xx, y0, luz)
                L.px(xx, y0 + 6, sombra)
                L.px(xx, y0 + 7, linea)
            L.rect(x0 % T, y0, x0 % T, y0 + 7, linea)
            L.px((x0 + 1) % T, y0 + 1, luz)
            L.px((x0 + 7) % T, y0 + 5, sombra)
    return L.img


def techo_rojo():
    return techo("#D9481E", "#F28C28", "#8E1B1B", "#2B2230")


def techo_terracota():
    return techo("#A86B3C", "#D9A06B", "#6E4426", "#4A3B32")


def alero(base_fn=techo_rojo):
    L = _sobre(base_fn())
    L.rect(0, 20, 31, 22, "#C9A227")
    L.rect(0, 20, 31, 20, "#E8D27A")
    L.rect(0, 23, 31, 31, "#4A3B32")
    for x in range(2, 32, 6):
        L.rect(x, 23, x + 1, 27, "#2B2230")
    return L.img


# ================================================================== objetos (fondo transparente)
def farol():
    """Farol dorado de 1x2 tiles: devuelve (arriba, abajo)."""
    L = Lienzo(T, 2 * T)
    L.rect(15, 18, 16, 61, "#2B2230")
    L.rect(15, 18, 15, 61, "#3B3846")
    L.rect(12, 58, 19, 63, "#2B2230")
    L.rect(12, 58, 19, 58, "#3B3846")
    # cabeza del farol
    L.rect(10, 4, 21, 6, "#8E1B1B")
    L.rect(13, 2, 18, 3, "#8E1B1B")
    L.rect(11, 7, 20, 16, "#C9A227")
    L.rect(13, 8, 18, 15, "#E8D27A")
    L.rect(14, 9, 16, 13, "#F4F1E8")
    L.rect(11, 17, 20, 18, "#8E1B1B")
    L.contorno()
    return L.img.crop((0, 0, T, T)), L.img.crop((0, T, T, 2 * T))


def banca():
    L = Lienzo()
    L.rect(3, 8, 28, 9, "#7A5230"); L.rect(3, 11, 28, 12, "#7A5230")
    L.rect(3, 8, 28, 8, "#C29A5B"); L.rect(3, 11, 28, 11, "#C29A5B")
    L.rect(4, 13, 5, 14, "#2B2230"); L.rect(26, 13, 27, 14, "#2B2230")
    L.rect(2, 15, 29, 20, "#C29A5B")
    for y in (17, 19):
        L.rect(2, y, 29, y, "#7A5230")
    L.rect(2, 15, 29, 15, "#E8D27A")
    L.rect(4, 21, 5, 25, "#2B2230"); L.rect(26, 21, 27, 25, "#2B2230")
    L.contorno()
    return L.img


def letrero():
    L = Lienzo()
    L.rect(3, 3, 22, 4, "#2B2230")
    L.rect(3, 3, 4, 8, "#2B2230")
    L.px(9, 5, "#5A5566"); L.px(9, 6, "#5A5566"); L.px(19, 5, "#5A5566"); L.px(19, 6, "#5A5566")
    L.rect(6, 7, 24, 22, "#C9A227")
    L.rect(7, 8, 23, 21, "#7A5230")
    L.rect(7, 8, 23, 8, "#C29A5B")
    # taza de té
    L.rect(12, 13, 18, 18, "#F4F1E8")
    L.rect(13, 18, 17, 19, "#C8C8C0")
    L.rect(19, 14, 20, 16, "#F4F1E8")
    L.px(14, 11, "#C8C8C0"); L.px(16, 10, "#C8C8C0"); L.px(15, 12, "#C8C8C0")
    L.contorno()
    return L.img


def maceta():
    L = Lienzo()
    L.circulo(16, 13, 9, "#3F5A2A")
    L.circulo(15, 12, 7, "#6B8E3D")
    for x, y in ((11, 9), (18, 8), (20, 14), (13, 16)):
        L.px(x, y, "#C29A5B")
    for x, y in ((10, 12), (19, 10), (16, 7)):
        L.rect(x, y, x + 1, y + 1, "#F28C28"); L.px(x, y, "#E8D27A")
    for y in range(21, 31):
        w = 8 - (y - 21) // 3
        L.rect(16 - w, y, 15 + w, y, "#A86B3C")
        L.px(16 - w, y, "#D9A06B"); L.px(15 + w, y, "#6E4426")
    L.rect(7, 21, 24, 22, "#D9A06B")
    L.contorno()
    return L.img


def arbusto():
    L = Lienzo()
    L.circulo(16, 18, 12, "#3F5A2A")
    L.circulo(14, 16, 10, "#6B8E3D")
    for x, y in ((9, 12), (12, 9), (17, 11), (20, 16), (11, 19)):
        L.px(x, y, "#C29A5B")
    for x, y in ((22, 22), (8, 22), (16, 26)):
        L.px(x, y, "#2B2230")
    L.contorno()
    return L.img


# ================================================================== fuente animada (64x64)
def fuente(f):
    L = Lienzo(64, 64)
    L.circulo(32, 33, 30, "#9AA3A8")
    L.circulo(32, 32, 30, "#C8C8C0")
    L.circulo(32, 32, 30, "#F4F1E8", r_in=28.5)
    L.circulo(32, 33, 25, "#1E4F8C")
    L.circulo(32, 33, 24, "#3A86C8")
    for k in range(3):
        r = 9 + ((k * 6 + f * 2) % 18)
        L.circulo(32, 33, r, "#8FD3F0", r_in=r - 1)
    L.circulo(32, 33, 7, "#5A5566")
    L.circulo(32, 32, 6, "#9AA3A8")
    L.circulo(32, 31, 4, "#C8C8C0")
    # chorro y gotas
    L.rect(31, 22 - f, 32, 30, "#F2F7FA")
    for i, (dx, dy) in enumerate(((-6, 4), (6, 4), (-9, 9), (9, 9), (-4, -1), (4, -1))):
        if (i + f) % 3 != 2:
            L.px(32 + dx + (f if dx > 0 else -f), 24 + dy, "#F2F7FA")
    L.contorno()
    return L.img


# ================================================================== hoja y mapas
def construir():
    farol_a, farol_b = farol()
    tiles = [
        ("calle", calle()), ("calle_grieta", calle(grieta=True)), ("acera", acera()),
        ("acera_borde_s", acera_borde()), ("acera_borde_n", acera_borde().rotate(180)),
        ("acera_borde_e", acera_borde().rotate(90)), ("acera_borde_o", acera_borde().rotate(-90)),
        ("plaza", plaza()),
        ("plaza_b", plaza(9)), ("pasto", pasto()), ("pasto_flores", pasto(flores=True)),
        ("pared", pared()), ("pared_ventana", pared_ventana()), ("pared_puerta", pared_puerta()),
        ("pared_simbolo", pared_simbolo()), ("zocalo", zocalo()),
        ("techo_rojo", techo_rojo()), ("techo_terracota", techo_terracota()),
        ("alero_rojo", alero()), ("alero_terracota", alero(techo_terracota)),
        ("farol_arriba", farol_a), ("farol_abajo", farol_b), ("banca", banca()), ("letrero", letrero()),
        ("maceta", maceta()), ("arbusto", arbusto()),
    ]
    return tiles


def guardar(tiles):
    out_dir = os.path.join(RAIZ, "juego", "assets", "tilesets")
    suelto = os.path.join(out_dir, "ciudad")
    os.makedirs(suelto, exist_ok=True)
    cols = 8
    filas = (len(tiles) + cols - 1) // cols
    hoja = Image.new("RGBA", (cols * T, filas * T), (0, 0, 0, 0))
    indice = {}
    for i, (n, img) in enumerate(tiles):
        assert not fuera_de_paleta(img), (n, fuera_de_paleta(img))
        hoja.alpha_composite(img, ((i % cols) * T, (i // cols) * T))
        img.save(os.path.join(suelto, n + ".png"))
        indice[i] = n
    hoja.save(os.path.join(out_dir, "tiles_ciudad.png"))
    with open(os.path.join(out_dir, "tiles_ciudad.json"), "w") as fh:
        json.dump({"tamano_tile": T, "columnas": cols, "tiles": indice}, fh, indent=2, ensure_ascii=False)
    for f in range(3):
        fi = fuente(f)
        assert not fuera_de_paleta(fi)
        fi.save(os.path.join(out_dir, f"obj_fuente_{f}.png"))
    return hoja


def mapa(nombre_tiles, plano, objetos=(), w=20, h=12):
    t = dict(nombre_tiles)
    img = Image.new("RGBA", (w * T, h * T), (0, 0, 0, 255))
    for y, fila in enumerate(plano):
        for x, n in enumerate(fila):
            img.alpha_composite(t[n], (x * T, y * T))
    for n, x, y in objetos:
        pieza = t[n] if n in t else n
        img.alpha_composite(pieza, (x, y))
    return img


def mapa_ejemplo(tiles):
    R, A, W, V, P, S, Z = "techo_rojo", "alero_rojo", "pared", "pared_ventana", "pared_puerta", "pared_simbolo", "zocalo"
    RT, AT = "techo_terracota", "alero_terracota"
    plano = [
        [R] * 8 + [RT] * 6 + [R] * 6,
        [A] * 8 + [AT] * 6 + [A] * 6,
        [W, V, W, V, W, V, W, V, V, W, S, W, V, W, V, W, V, W, V, W],
        [Z, P, Z, Z, Z, P, Z, Z, Z, P, Z, Z, Z, Z, Z, P, Z, Z, P, Z],
        ["acera"] * 20,
        ["acera_borde_s"] * 20,
        ["calle"] * 7 + ["calle_grieta"] + ["calle"] * 12,
        ["calle"] * 20,
        ["acera_borde_n"] * 20,
        ["pasto", "pasto_flores"] + ["plaza", "plaza_b"] * 8 + ["pasto_flores", "pasto"],
        ["pasto"] + ["plaza_b", "plaza"] * 9 + ["pasto"],
        ["pasto_flores", "pasto"] + ["plaza", "plaza_b"] * 8 + ["pasto", "pasto_flores"],
    ]
    fa, fb = dict(tiles)["farol_arriba"], dict(tiles)["farol_abajo"]
    objs = [("letrero", 3 * T, 2 * T - 10), ("maceta", 6 * T, 3 * T + 4), ("maceta", 13 * T, 3 * T + 4),
            ("banca", 5 * T, 10 * T), ("banca", 13 * T, 10 * T), ("arbusto", 0, 9 * T + 8), ("arbusto", 19 * T, 10 * T)]
    img = mapa(tiles, plano, objs)
    for x in (2 * T, 17 * T):
        img.alpha_composite(fa, (x, 8 * T)); img.alpha_composite(fb, (x, 9 * T))
    img.alpha_composite(fuente(0), (9 * T, 9 * T + 16))
    return img


def fondo_pelea(tiles):
    t = dict(tiles)
    img = Image.new("RGBA", (640, 360), (0, 0, 0, 255))
    fila_techo = ["techo_rojo"] * 7 + ["techo_terracota"] * 6 + ["techo_rojo"] * 7
    fila_pared = ["pared", "pared_ventana", "pared", "pared_ventana", "pared", "pared_puerta", "pared",
                  "pared_ventana", "pared", "pared_simbolo", "pared", "pared_ventana", "pared", "pared_puerta",
                  "pared", "pared_ventana", "pared", "pared_ventana", "pared", "pared"]
    for x in range(20):
        img.alpha_composite(t[fila_techo[x]].crop((0, 16, 32, 32)), (x * T, 0))
        img.alpha_composite(t["alero_terracota" if 7 <= x < 13 else "alero_rojo"], (x * T, 16))
        img.alpha_composite(t[fila_pared[x]], (x * T, 48))
        img.alpha_composite(t["zocalo"], (x * T, 80))
    for y in range(112, 360, T):
        for x in range(20):
            n = "plaza" if (x + y // T) % 2 else "plaza_b"
            if (x in (0, 19)) and y >= 300:
                n = "pasto_flores"
            img.alpha_composite(t[n], (x * T, y))
    # anillo de mosaico en el centro de la plaza (área de combate)
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    cx, cy = 320, 236
    d.ellipse([cx - 200, cy - 100, cx + 200, cy + 100], outline=a_rgb("#8E1B1B") + (255,), width=4)
    d.ellipse([cx - 196, cy - 96, cx + 196, cy + 96], outline=a_rgb("#C9A227") + (255,), width=1)
    d.ellipse([cx - 205, cy - 105, cx + 205, cy + 105], outline=a_rgb("#C9A227") + (255,), width=1)
    d.ellipse([cx - 30, cy - 15, cx + 30, cy + 15], outline=a_rgb("#8E1B1B") + (255,), width=3)
    d.ellipse([cx - 22, cy - 10, cx + 22, cy + 10], fill=a_rgb("#D9481E") + (255,))
    d.ellipse([cx - 14, cy - 6, cx + 14, cy + 6], fill=a_rgb("#F28C28") + (255,))
    fa, fb = t["farol_arriba"], t["farol_abajo"]
    for x in (40, 568):
        img.alpha_composite(fa, (x, 96)); img.alpha_composite(fb, (x, 128))
    for n, x, y in (("maceta", 200, 92), ("maceta", 408, 92), ("banca", 96, 320), ("banca", 512, 320)):
        img.alpha_composite(t[n], (x, y))
    return img


if __name__ == "__main__":
    tiles = construir()
    hoja = guardar(tiles)
    prev = os.path.join(RAIZ, "arte_fuente", "previews")
    hoja.resize((hoja.width * 3, hoja.height * 3), Image.NEAREST).save(os.path.join(prev, "tiles_ciudad_x3.png"))
    m = mapa_ejemplo(tiles)
    m.save(os.path.join(prev, "mapa_ciudad_ejemplo.png"))
    fp = fondo_pelea(tiles)
    assert not fuera_de_paleta(fp)
    fp.save(os.path.join(RAIZ, "juego", "assets", "tilesets", "fondo_pelea_plaza.png"))
    print(len(tiles), "tiles")
