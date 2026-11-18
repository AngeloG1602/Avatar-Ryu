"""Tileset de la ciudad (Nación del Fuego) v2, tiles de 32x32, paleta oficial.

Genera:
  juego/assets/tilesets/tiles_ciudad.png        hoja de tiles (8 columnas)
  juego/assets/tilesets/tiles_ciudad.json       índice -> nombre
  juego/assets/tilesets/ciudad/<nombre>.png     cada tile suelto
  juego/assets/tilesets/obj_<nombre>.png        objetos grandes (árbol, puesto, fuente_0..2)
  juego/assets/tilesets/obj_sombra.png          sombra para poner bajo objetos (usar con opacidad ~40%)
  juego/assets/tilesets/fondo_pelea_plaza.png   640x360
  arte_fuente/previews/mapa_ciudad_ejemplo.png  mapa de muestra
Uso: python3 herramientas/tiles_ciudad.py
"""
import json
import math
import os
import random
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from paleta import CONTORNO, a_rgb, fuera_de_paleta

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
T = 32

# tono más oscuro de cada color de la paleta (para sombras proyectadas)
OSCURECER = {
    "#C8C8C0": "#9AA3A8", "#F4F1E8": "#C8C8C0", "#9AA3A8": "#5A5566", "#5A5566": "#3B3846",
    "#3B3846": "#24222B", "#24222B": "#1A1420", "#1A1420": "#1A1420", "#D9A06B": "#A86B3C",
    "#C29A5B": "#7A5230", "#E8D27A": "#C29A5B", "#A86B3C": "#6E4426", "#7A5230": "#4A3B32",
    "#6B8E3D": "#3F5A2A", "#3F5A2A": "#2B2230", "#F2C9A0": "#D9A06B", "#4A3B32": "#2B2230",
    "#2B2230": "#1A1420", "#D9481E": "#8E1B1B", "#8E1B1B": "#2B2230", "#F28C28": "#D9481E",
    "#C9A227": "#7A5230", "#3A86C8": "#1E4F8C", "#1E4F8C": "#24222B", "#8FD3F0": "#3A86C8",
    "#F2F7FA": "#8FD3F0", "#6E4426": "#4A3B32",
}
_RGB2HEX = {a_rgb(k): k for k in OSCURECER}


class Lienzo:
    def __init__(self, w=T, h=T, fondo=None):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w, h), (0, 0, 0, 0) if fondo is None else a_rgb(fondo) + (255,))
        self.p = self.img.load()

    @classmethod
    def de(cls, img):
        L = cls(img.width, img.height)
        L.img = img.copy(); L.p = L.img.load()
        return L

    def px(self, x, y, c, envolver=False):
        if envolver:
            x, y = x % self.w, y % self.h
        if 0 <= x < self.w and 0 <= y < self.h:
            self.p[x, y] = a_rgb(c) + (255,)

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def circulo(self, cx, cy, rx, c, ry=None, r_in=-1.0):
        ry = rx if ry is None else ry
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                d = math.hypot((x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry)
                if r_in < d <= 1.0:
                    self.px(x, y, c)

    def linea(self, x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0)) or 1
        for i in range(n + 1):
            self.px(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)

    def oscurecer(self, cond):
        for y in range(self.h):
            for x in range(self.w):
                r, g, b, a = self.p[x, y]
                if a and cond(x, y):
                    h = _RGB2HEX.get((r, g, b))
                    if h:
                        self.px(x, y, OSCURECER[h])

    def contorno(self):
        lleno = {(x, y) for y in range(self.h) for x in range(self.w) if self.p[x, y][3]}
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) not in lleno and any((x + dx, y + dy) in lleno for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    self.px(x, y, CONTORNO)
        return self

    def sombra_suelo(self, cx, cy, rx, ry):
        """Sombra tramada (patrón de ajedrez) bajo un objeto."""
        for y in range(int(cy - ry), int(cy + ry) + 1):
            for x in range(int(cx - rx), int(cx + rx) + 1):
                if (0 <= x < self.w and 0 <= y < self.h and ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1
                        and (x + y) % 2 == 0 and not self.p[x, y][3]):
                    self.px(x, y, "#1A1420")


# ================================================================== suelos
def asfalto(semilla=1):
    L = Lienzo(fondo="#3B3846")
    rnd = random.Random(semilla)
    for _ in range(70):
        L.px(rnd.randrange(32), rnd.randrange(32), "#24222B")
    for _ in range(25):
        L.px(rnd.randrange(32), rnd.randrange(32), "#5A5566")
    return L.img


def asfalto_linea():
    L = Lienzo.de(asfalto(2))
    for x in range(4, 24):
        L.px(x, 15, "#E8D27A"); L.px(x, 16, "#C9A227")
    return L.img


def paso_peatonal():
    L = Lienzo.de(asfalto(3))
    for x0 in (2, 12, 22):
        L.rect(x0, 0, x0 + 6, 31, "#C8C8C0")
        L.rect(x0, 0, x0, 31, "#F4F1E8")
        rnd = random.Random(x0)
        for _ in range(8):
            L.px(x0 + rnd.randrange(7), rnd.randrange(32), "#9AA3A8")
    return L.img


def alcantarilla():
    L = Lienzo.de(asfalto(4))
    L.circulo(16, 16, 11, "#24222B")
    L.circulo(16, 16, 10, "#5A5566")
    L.circulo(16, 16, 10, "#9AA3A8", r_in=0.85)
    for y in range(9, 24, 3):
        L.rect(9, y, 23, y, "#24222B")
    L.circulo(16, 16, 10, "#5A5566", r_in=0.95)
    return L.img


def acera(semilla=7):
    L = Lienzo(fondo="#C8C8C0")
    rnd = random.Random(semilla)
    for by in (0, 16):
        for bx in (0, 16):
            L.rect(bx, by, bx + 15, by, "#F4F1E8")
            L.rect(bx, by, bx, by + 15, "#F4F1E8")
            L.rect(bx + 15, by + 1, bx + 15, by + 15, "#9AA3A8")
            L.rect(bx + 1, by + 15, bx + 15, by + 15, "#9AA3A8")
    for _ in range(12):
        L.px(rnd.randrange(1, 31), rnd.randrange(1, 31), "#9AA3A8")
    if semilla % 2:
        for x, y in ((20, 4), (21, 5), (21, 6), (22, 7), (23, 7), (24, 8)):
            L.px(x, y, "#9AA3A8")
    return L.img


def acera_sombra():
    """Acera con la sombra del edificio en la mitad superior."""
    L = Lienzo.de(acera(8))
    L.oscurecer(lambda x, y: y < 12 or (y < 15 and (x + y) % 2 == 0))
    return L.img


def bordillo():
    """Acera arriba, bordillo de piedra y asfalto abajo (lado sur). Rotar para otros lados."""
    L = Lienzo.de(acera(9))
    L.rect(0, 20, 31, 24, "#9AA3A8")
    L.rect(0, 20, 31, 20, "#F4F1E8")
    L.rect(0, 21, 31, 21, "#C8C8C0")
    L.rect(0, 24, 31, 24, "#5A5566")
    for x in range(0, 32, 8):
        L.rect(x, 21, x, 23, "#5A5566")
    a = asfalto(5)
    L.img.paste(a.crop((0, 25, 32, 32)), (0, 25))
    L.p = L.img.load()
    L.rect(0, 25, 31, 26, "#24222B")
    return L.img


def plaza(semilla=3, grieta=False, musgo=False):
    """Losas grandes de piedra dorada en damero suave."""
    L = Lienzo(fondo="#7A5230")
    rnd = random.Random(semilla)
    for by in (0, 16):
        for bx in (0, 16):
            base = "#C29A5B" if (bx + by) % 32 == 0 else "#D9A06B"
            L.rect(bx + 1, by + 1, bx + 14, by + 14, base)
            L.rect(bx + 1, by + 1, bx + 14, by + 1, "#E8D27A")
            L.rect(bx + 1, by + 1, bx + 1, by + 14, "#E8D27A")
            L.rect(bx + 2, by + 14, bx + 14, by + 14, "#A86B3C")
            L.rect(bx + 14, by + 2, bx + 14, by + 14, "#A86B3C")
            for _ in range(3):
                L.px(bx + rnd.randrange(3, 13), by + rnd.randrange(3, 13), "#A86B3C" if base == "#D9A06B" else "#7A5230")
    if grieta:
        for x, y in ((18, 19), (19, 20), (20, 20), (21, 21), (22, 22), (23, 22), (24, 23), (25, 25)):
            L.px(x, y, "#4A3B32")
    if musgo:
        for x, y in ((15, 3), (15, 4), (16, 9), (15, 10), (0, 15), (1, 16), (3, 16), (15, 22), (16, 23), (30, 15)):
            L.px(x, y, "#6B8E3D")
        L.px(15, 5, "#3F5A2A"); L.px(2, 16, "#3F5A2A")
    return L.img


def cenefa():
    """Banda decorativa de ladrillo rojo que bordea la plaza (horizontal)."""
    L = Lienzo(fondo="#4A3B32")
    for fila, y0 in enumerate((4, 10, 16, 22)):
        off = 4 if fila % 2 else 0
        for x0 in range(-off, 32, 8):
            c = "#D9481E" if fila in (1, 2) else "#8E1B1B"
            for x in range(x0, x0 + 7):
                for y in range(y0, y0 + 5):
                    L.px(x % 32, y, c)
                L.px(x % 32, y0, "#F28C28" if c == "#D9481E" else "#D9481E")
    L.rect(0, 0, 31, 3, "#C9A227")
    L.rect(0, 0, 31, 0, "#E8D27A")
    L.rect(0, 28, 31, 31, "#C9A227")
    L.rect(0, 31, 31, 31, "#7A5230")
    return L.img


def pasto(flores=False, semilla=5):
    L = Lienzo(fondo="#6B8E3D")
    rnd = random.Random(semilla)
    # manchas oscuras suaves
    for _ in range(6):
        cx, cy, r = rnd.randrange(32), rnd.randrange(32), rnd.randrange(3, 6)
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r and (x + y) % 2 == 0:
                    L.px(x, y, "#3F5A2A", envolver=True)
    # briznas
    for _ in range(16):
        x, y = rnd.randrange(32), rnd.randrange(32)
        L.px(x, y, "#3F5A2A", True); L.px(x - 1, y - 1, "#3F5A2A", True); L.px(x + 1, y - 2, "#3F5A2A", True)
        L.px(x, y - 1, "#6B8E3D", True)
    for _ in range(6):
        L.px(rnd.randrange(32), rnd.randrange(32), "#C29A5B")
    if flores:
        for (x, y), c in zip(((6, 8), (22, 5), (14, 20), (26, 24), (5, 26), (18, 13)),
                             ("#F28C28", "#E8D27A", "#F4F1E8", "#D9481E", "#E8D27A", "#F4F1E8")):
            for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                L.px(x + dx, y + dy, c)
            L.px(x, y, "#C9A227")
            L.px(x, y + 2, "#3F5A2A")
    return L.img


def pasto_borde(lado):
    """Pasto que se funde con la plaza por un lado con borde irregular (lado = 's','n','e','o')."""
    p = pasto(semilla=21)
    q = plaza(22)
    L = Lienzo.de(q)
    pp = p.load()
    for y in range(32):
        for x in range(32):
            if lado == "s":
                lim, v = 18 + round(2 * math.sin(x * 0.7) + math.sin(x * 1.9)), y
            elif lado == "n":
                lim, v = 18 + round(2 * math.sin(x * 0.7) + math.sin(x * 1.9)), 31 - y
            elif lado == "e":
                lim, v = 18 + round(2 * math.sin(y * 0.7) + math.sin(y * 1.9)), x
            else:
                lim, v = 18 + round(2 * math.sin(y * 0.7) + math.sin(y * 1.9)), 31 - x
            if v < lim:
                L.p[x, y] = pp[x, y]
            elif v == lim:
                L.px(x, y, "#3F5A2A")
            elif v == lim + 1:
                L.px(x, y, "#4A3B32")
    return L.img


# ================================================================== edificios
def _estuco(semilla):
    L = Lienzo(fondo="#F2C9A0")
    rnd = random.Random(semilla)
    for _ in range(14):
        L.px(rnd.randrange(32), rnd.randrange(32), "#D9A06B")
    for _ in range(8):
        L.px(rnd.randrange(32), rnd.randrange(32), "#F4F1E8")
    # ladrillo asomando bajo el estuco
    if semilla % 3 == 0:
        for (x, y) in ((22, 20), (26, 20), (24, 23)):
            L.rect(x, y, x + 3, y + 1, "#A86B3C")
            L.px(x, y, "#D9A06B")
    return L


def _base_piedra(L):
    """Zócalo de piedra en los 7 px inferiores (planta baja)."""
    L.rect(0, 25, 31, 31, "#9AA3A8")
    L.rect(0, 25, 31, 25, "#C8C8C0")
    for x0, y0 in ((0, 26), (10, 26), (20, 26), (5, 29), (15, 29), (25, 29)):
        L.rect(x0, y0, x0, y0 + 2, "#5A5566")
    L.rect(0, 28, 31, 28, "#5A5566")
    L.rect(0, 31, 31, 31, "#5A5566")


def pared(alto=True, semilla=11):
    L = _estuco(semilla)
    L.rect(0, 0, 31, 1, "#D9A06B") if alto else None
    if not alto:
        _base_piedra(L)
    return L.img


def pared_viga(alto=True):
    """Columna de madera roja (esquina o separación entre edificios)."""
    L = Lienzo.de(pared(alto, 12))
    L.rect(12, 0, 19, 31 if alto else 24, "#8E1B1B")
    L.rect(12, 0, 13, 31 if alto else 24, "#D9481E")
    L.rect(19, 0, 19, 31 if alto else 24, "#2B2230")
    L.rect(11, 4, 20, 5, "#C9A227")
    L.rect(11, 4, 20, 4, "#E8D27A")
    if not alto:
        L.rect(10, 22, 21, 24, "#5A5566")
        L.rect(10, 22, 21, 22, "#9AA3A8")
    return L.img


def pared_ventana(semilla=13):
    L = Lienzo.de(pared(True, semilla))
    L.rect(6, 4, 25, 25, "#2B2230")
    L.rect(7, 5, 24, 24, "#8E1B1B")
    L.rect(7, 5, 24, 5, "#D9481E")
    L.rect(9, 7, 22, 22, "#1E4F8C")
    L.rect(9, 7, 22, 9, "#3A86C8")
    for i in range(6):
        L.px(11 + i, 15 - i, "#8FD3F0")
    # celosía de madera
    for x in (12, 15, 18):
        L.rect(x, 7, x, 22, "#7A5230")
    for y in (11, 15, 19):
        L.rect(9, y, 22, y, "#7A5230")
    # jardinera con flores
    L.rect(5, 25, 26, 28, "#7A5230")
    L.rect(5, 25, 26, 25, "#C29A5B")
    for x in range(6, 26, 3):
        L.px(x, 24, "#6B8E3D"); L.px(x + 1, 23, "#3F5A2A")
        L.px(x + 1, 22, "#D9481E" if x % 2 else "#E8D27A")
    L.rect(6, 29, 25, 29, "#D9A06B")
    return L.img


def pared_puerta():
    L = Lienzo.de(pared(False, 14))
    L.rect(6, 1, 25, 4, "#2B2230")
    L.rect(6, 1, 25, 2, "#C9A227")
    L.rect(7, 5, 24, 26, "#2B2230")
    L.rect(8, 5, 15, 26, "#8E1B1B"); L.rect(16, 5, 23, 26, "#8E1B1B")
    L.rect(8, 5, 8, 26, "#D9481E"); L.rect(16, 5, 16, 26, "#D9481E")
    for y in (9, 15, 21):
        for x in (10, 13, 18, 21):
            L.px(x, y, "#C9A227")
    L.rect(14, 14, 14, 17, "#E8D27A"); L.rect(17, 14, 17, 17, "#E8D27A")
    L.rect(5, 27, 26, 29, "#C8C8C0")
    L.rect(5, 27, 26, 27, "#F4F1E8")
    return L.img


def pared_tienda():
    """Escaparate de tienda con toldo a rayas (planta baja)."""
    L = Lienzo.de(pared(False, 15))
    for x in range(1, 31):
        c = "#D9481E" if (x // 3) % 2 == 0 else "#F4F1E8"
        L.rect(x, 1, x, 6, c)
        L.px(x, 7, "#8E1B1B" if c == "#D9481E" else "#C8C8C0")
    for x in range(1, 31, 3):
        L.px(x, 8, "#8E1B1B")
    L.rect(3, 10, 28, 24, "#2B2230")
    L.rect(4, 11, 27, 23, "#3A86C8")
    L.rect(4, 11, 27, 13, "#8FD3F0")
    L.rect(4, 19, 27, 23, "#7A5230")
    for x, c in ((7, "#F28C28"), (12, "#E8D27A"), (17, "#D9481E"), (22, "#F4F1E8")):
        L.rect(x, 17, x + 2, 19, c)
    L.rect(15, 11, 16, 23, "#2B2230")
    return L.img


def pared_simbolo():
    """Pista 1: el símbolo de El Ciclo Roto pintado con aerosol."""
    L = Lienzo.de(pared(True, 16))
    tinta = "#24222B"
    L.circulo(16, 15, 12, tinta, r_in=0.78)
    for x, y in ((16, 1), (15, 2), (16, 2), (17, 2), (14, 3), (18, 3)):          # fuego
        L.px(x, y, tinta)
    for x in range(26, 31):                                                     # agua
        L.px(x, 14 + (x % 2), tinta); L.px(x, 16 + (x % 2), tinta)
    L.rect(14, 27, 18, 30, tinta)                                               # tierra
    for x, y in ((1, 14), (2, 13), (3, 13), (4, 14), (3, 16), (2, 16)):         # aire
        L.px(x, y, tinta)
    for i in range(-13, 14):
        for k in (0, 1, 2):
            L.px(16 + i + k - 1, 15 - i, "#8E1B1B")
    for x, y0, n in ((7, 22, 5), (24, 21, 4), (11, 26, 4), (20, 26, 3)):
        L.rect(x, y0, x, y0 + n, tinta)
    rnd = random.Random(4)
    for _ in range(12):
        L.px(rnd.randrange(32), rnd.randrange(32), tinta if rnd.random() < .5 else "#8E1B1B")
    return L.img


def _tejas(base, luz, sombra, hueco):
    """Tejas cilíndricas en columnas de 4 px, filas de 8 px."""
    L = Lienzo(fondo=base)
    for x in range(32):
        k = x % 4
        for y in range(32):
            if k == 0:
                L.px(x, y, hueco)
            elif k == 1:
                L.px(x, y, luz)
            elif k == 3:
                L.px(x, y, sombra)
    for fila in range(4):
        y = fila * 8 + 7
        for x in range(32):
            L.px(x, y, "#2B2230" if hueco == "#8E1B1B" else "#4A3B32")
            if x % 4 in (1, 2):
                L.px(x, y - 1, sombra)
        for x in range(1, 32, 4):
            L.px(x, fila * 8, "#F4F1E8" if luz == "#F28C28" else "#F2C9A0")
    return L


def techo_rojo():
    return _tejas("#D9481E", "#F28C28", "#8E1B1B", "#8E1B1B").img


def techo_terracota():
    return _tejas("#A86B3C", "#D9A06B", "#6E4426", "#6E4426").img


def cumbrera(rojo=True):
    L = Lienzo.de(techo_rojo() if rojo else techo_terracota())
    L.rect(0, 14, 31, 21, "#2B2230")
    L.rect(0, 15, 31, 19, "#3B3846")
    L.rect(0, 15, 31, 15, "#5A5566")
    L.rect(0, 20, 31, 21, "#C9A227")
    for x in (6, 22):
        L.circulo(x, 14, 3, "#C9A227"); L.px(x - 1, 12, "#E8D27A")
    L.img = L.img.crop((0, 0, 32, 32))
    for y in range(14):
        for x in range(32):
            L.p[x, y] = (0, 0, 0, 0)
    for x in (6, 22):
        L.circulo(x, 13, 3, "#C9A227"); L.px(x - 1, 11, "#E8D27A"); L.px(x, 9, "#C9A227")
    return L.img


def alero(rojo=True):
    """Borde inferior del tejado: remates redondos, moldura dorada y sombra con vigas."""
    L = Lienzo.de(techo_rojo() if rojo else techo_terracota())
    luz = "#F28C28" if rojo else "#D9A06B"
    base = "#D9481E" if rojo else "#A86B3C"
    L.rect(0, 16, 31, 31, (0, 0, 0, 0)) if False else None
    for y in range(16, 32):
        for x in range(32):
            L.p[x, y] = (0, 0, 0, 0)
    for x0 in range(0, 32, 4):
        L.circulo(x0 + 2, 16, 2, base)
        L.px(x0 + 1, 15, luz)
    L.rect(0, 18, 31, 20, "#C9A227")
    L.rect(0, 18, 31, 18, "#E8D27A")
    L.rect(0, 21, 31, 27, "#24222B")
    for x in range(1, 32, 5):
        L.rect(x, 21, x + 2, 24, "#7A5230")
        L.rect(x, 24, x + 2, 24, "#4A3B32")
    L.rect(0, 28, 31, 31, "#D9A06B")
    L.rect(0, 28, 31, 28, "#A86B3C")
    return L.img


# ================================================================== objetos
def farol():
    """Farol dorado de 1x2 tiles: devuelve (arriba, abajo)."""
    L = Lienzo(T, 2 * T)
    L.sombra_suelo(16, 61, 9, 2)
    L.rect(15, 20, 16, 59, "#2B2230")
    L.rect(15, 20, 15, 59, "#3B3846")
    for y in (28, 44):
        L.rect(14, y, 17, y + 1, "#C9A227")
    L.rect(12, 56, 19, 60, "#2B2230")
    L.rect(12, 56, 19, 56, "#5A5566")
    L.rect(13, 1, 18, 2, "#2B2230")
    L.rect(9, 3, 22, 5, "#8E1B1B"); L.rect(9, 3, 22, 3, "#D9481E")
    L.rect(10, 6, 21, 17, "#C9A227")
    L.rect(12, 7, 19, 16, "#F28C28")
    L.rect(13, 8, 18, 15, "#E8D27A")
    L.rect(14, 9, 16, 13, "#F4F1E8")
    L.rect(15, 6, 16, 17, "#C9A227")
    L.rect(9, 18, 22, 19, "#8E1B1B")
    L.contorno()
    return L.img.crop((0, 0, T, T)), L.img.crop((0, T, T, 2 * T))


def farolillo():
    """Farolillo de papel rojo colgante."""
    L = Lienzo()
    L.rect(15, 0, 16, 5, "#2B2230")
    L.rect(12, 6, 19, 7, "#C9A227")
    L.circulo(16, 15, 8, "#D9481E", ry=7)
    L.circulo(14, 13, 4, "#F28C28", ry=4)
    L.px(12, 11, "#E8D27A")
    for y in (11, 15, 19):
        L.rect(9, y, 23, y, "#8E1B1B")
    L.rect(12, 22, 19, 23, "#C9A227")
    L.rect(15, 24, 16, 28, "#D9481E")
    L.px(15, 29, "#8E1B1B"); L.px(16, 29, "#8E1B1B")
    L.contorno()
    return L.img


def banca():
    L = Lienzo()
    L.sombra_suelo(16, 27, 14, 3)
    L.rect(4, 6, 27, 7, "#7A5230"); L.rect(4, 6, 27, 6, "#C29A5B")
    L.rect(4, 9, 27, 10, "#7A5230"); L.rect(4, 9, 27, 9, "#C29A5B")
    L.rect(2, 13, 29, 19, "#C29A5B")
    for y in (13, 16):
        L.rect(2, y, 29, y, "#E8D27A")
    for y in (15, 18):
        L.rect(2, y, 29, y, "#7A5230")
    L.rect(2, 19, 29, 19, "#4A3B32")
    for x in (3, 27):
        L.rect(x, 5, x + 1, 24, "#2B2230")
        L.rect(x, 5, x, 24, "#3B3846")
        L.rect(x - 1, 23, x + 2, 24, "#2B2230")
    L.contorno()
    return L.img


def letrero():
    L = Lienzo()
    L.rect(2, 2, 24, 3, "#2B2230")
    L.rect(2, 2, 3, 8, "#2B2230")
    L.circulo(24, 2, 2, "#C9A227")
    L.px(9, 4, "#5A5566"); L.px(9, 5, "#5A5566"); L.px(20, 4, "#5A5566"); L.px(20, 5, "#5A5566")
    L.rect(5, 6, 25, 23, "#C9A227")
    L.rect(5, 6, 25, 6, "#E8D27A")
    L.rect(6, 7, 24, 22, "#8E1B1B")
    L.rect(6, 7, 24, 7, "#D9481E")
    L.rect(11, 12, 18, 17, "#F4F1E8")
    L.rect(12, 17, 17, 18, "#C8C8C0")
    L.rect(19, 13, 20, 15, "#F4F1E8")
    L.rect(12, 12, 17, 12, "#C29A5B")
    L.px(13, 10, "#C8C8C0"); L.px(15, 9, "#C8C8C0"); L.px(14, 11, "#C8C8C0"); L.px(16, 10, "#C8C8C0")
    L.contorno()
    return L.img


def maceta():
    L = Lienzo()
    L.sombra_suelo(16, 30, 10, 2)
    L.circulo(16, 12, 11, "#3F5A2A", ry=9)
    L.circulo(15, 11, 9, "#6B8E3D", ry=7)
    for x, y in ((10, 8), (14, 5), (19, 7), (21, 12), (12, 14)):
        L.px(x, y, "#C29A5B"); L.px(x + 1, y + 1, "#3F5A2A")
    for x, y, c in ((9, 11, "#D9481E"), (18, 4, "#F28C28"), (20, 15, "#E8D27A"), (13, 7, "#F4F1E8")):
        L.rect(x, y, x + 1, y + 1, c); L.px(x, y, "#E8D27A" if c != "#E8D27A" else "#F4F1E8")
    for y in range(21, 30):
        w = 9 - (y - 21) // 3
        L.rect(16 - w, y, 15 + w, y, "#A86B3C")
        L.px(16 - w, y, "#D9A06B"); L.px(16 - w + 1, y, "#D9A06B"); L.px(15 + w, y, "#6E4426")
    L.rect(6, 20, 25, 22, "#D9A06B")
    L.rect(6, 20, 25, 20, "#F2C9A0")
    L.rect(8, 25, 23, 25, "#C9A227")
    L.contorno()
    return L.img


def arbusto():
    L = Lienzo()
    L.sombra_suelo(16, 29, 12, 2)
    L.circulo(16, 17, 13, "#3F5A2A", ry=11)
    L.circulo(14, 15, 10, "#6B8E3D", ry=8)
    L.circulo(11, 12, 4, "#6B8E3D")
    rnd = random.Random(2)
    for _ in range(10):
        x, y = rnd.randrange(6, 24), rnd.randrange(8, 22)
        L.px(x, y, "#3F5A2A"); L.px(x + 1, y - 1, "#C29A5B")
    for x, y in ((8, 16), (20, 11), (15, 21)):
        L.px(x, y, "#E8D27A"); L.px(x + 1, y, "#F4F1E8")
    L.contorno()
    return L.img


def barril():
    L = Lienzo()
    L.sombra_suelo(16, 29, 10, 2)
    L.rect(9, 6, 22, 27, "#7A5230")
    L.rect(8, 9, 23, 24, "#7A5230")
    L.rect(9, 6, 11, 27, "#C29A5B")
    L.rect(20, 6, 22, 27, "#4A3B32")
    for y in (9, 23):
        L.rect(8, y, 23, y + 1, "#3B3846")
        L.rect(8, y, 23, y, "#5A5566")
    L.circulo(15.5, 6, 6.5, "#C29A5B", ry=2.5)
    L.circulo(15.5, 6, 5, "#7A5230", ry=1.5)
    L.contorno()
    return L.img


def cajas():
    L = Lienzo()
    L.sombra_suelo(16, 29, 13, 2)
    for x0, y0, w, h in ((3, 13, 15, 14), (15, 16, 14, 11), (8, 2, 13, 12)):
        L.rect(x0, y0, x0 + w, y0 + h, "#C29A5B")
        L.rect(x0, y0, x0 + w, y0 + 1, "#E8D27A")
        L.rect(x0, y0 + h, x0 + w, y0 + h, "#7A5230")
        L.rect(x0 + w, y0, x0 + w, y0 + h, "#7A5230")
        L.linea(x0 + 1, y0 + 2, x0 + w - 1, y0 + h - 1, "#7A5230")
        L.rect(x0, y0, x0 + w, y0 + h, None) if False else None
    L.contorno()
    return L.img


def arbol():
    """Árbol de 2x2 tiles (64x64)."""
    L = Lienzo(64, 64)
    L.sombra_suelo(32, 58, 20, 4)
    L.rect(28, 36, 35, 58, "#7A5230")
    L.rect(28, 36, 29, 58, "#C29A5B")
    L.rect(34, 36, 35, 58, "#4A3B32")
    L.rect(25, 55, 38, 58, "#7A5230")
    for cx, cy, r in ((32, 24, 22), (18, 30, 12), (46, 30, 12), (32, 12, 13)):
        L.circulo(cx, cy, r, "#3F5A2A")
    for cx, cy, r in ((29, 21, 17), (16, 27, 8), (43, 26, 9), (30, 10, 10)):
        L.circulo(cx, cy, r, "#6B8E3D")
    for cx, cy, r in ((24, 15, 6), (14, 25, 3), (38, 20, 4)):
        L.circulo(cx, cy, r, "#C29A5B", r_in=0.7)
    rnd = random.Random(8)
    for _ in range(40):
        x, y = rnd.randrange(12, 52), rnd.randrange(4, 42)
        if L.p[x, y][3]:
            L.px(x, y, "#3F5A2A" if rnd.random() < .6 else "#C29A5B")
    for x, y in ((20, 30), (40, 18), (30, 34), (46, 32), (24, 8)):
        L.rect(x, y, x + 1, y + 1, "#D9481E"); L.px(x, y, "#F28C28")
    L.contorno()
    return L.img


def puesto():
    """Puesto de comida de 2x2 tiles (64x64) con toldo a rayas."""
    L = Lienzo(64, 64)
    L.sombra_suelo(32, 60, 28, 3)
    for x in (6, 56):
        L.rect(x, 14, x + 2, 58, "#7A5230"); L.px(x, 14, "#C29A5B")
    for x in range(2, 62):
        c = "#D9481E" if (x // 6) % 2 == 0 else "#F4F1E8"
        L.rect(x, 4, x, 14, c)
        L.px(x, 15, "#8E1B1B" if c == "#D9481E" else "#C8C8C0")
        if x % 6 == 3:
            L.px(x, 16, "#8E1B1B" if c == "#D9481E" else "#C8C8C0")
    L.rect(2, 3, 61, 3, "#8E1B1B")
    L.rect(4, 36, 59, 58, "#8E1B1B")
    L.rect(4, 36, 59, 39, "#C9A227")
    L.rect(4, 36, 59, 36, "#E8D27A")
    for x in range(8, 58, 8):
        L.rect(x, 42, x + 4, 54, "#D9481E"); L.rect(x, 42, x, 54, "#F28C28")
    # comida sobre el mostrador
    for x, c in ((12, "#F28C28"), (22, "#E8D27A"), (32, "#D9481E"), (42, "#6B8E3D"), (50, "#F4F1E8")):
        L.circulo(x, 32, 4, "#C8C8C0", ry=2)
        L.circulo(x, 31, 3, c, ry=2)
    L.rect(26, 18, 37, 26, "#2B2230")
    L.rect(27, 19, 36, 25, "#C9A227")
    L.rect(29, 21, 34, 23, "#8E1B1B")
    L.contorno()
    return L.img


def fuente(f):
    """Fuente octogonal de 64x64, cuadro f de 0 a 2."""
    L = Lienzo(64, 64)
    L.sombra_suelo(32, 58, 28, 4)
    oct_ = lambda r, dy=0: [(32 + r * math.cos(math.pi / 8 + k * math.pi / 4), 32 + dy + r * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    img = L.img
    d = ImageDraw.Draw(img)
    d.polygon(oct_(30, 3), fill=a_rgb("#5A5566") + (255,))
    d.polygon(oct_(30), fill=a_rgb("#C8C8C0") + (255,))
    d.polygon(oct_(30), outline=a_rgb("#F4F1E8") + (255,))
    d.polygon(oct_(25), fill=a_rgb("#9AA3A8") + (255,))
    d.polygon(oct_(24, 1), fill=a_rgb("#1E4F8C") + (255,))
    d.polygon(oct_(22, 2), fill=a_rgb("#3A86C8") + (255,))
    L.p = img.load()
    for k in range(3):
        r = 7 + ((k * 5 + f * 2) % 15)
        L.circulo(32, 34, r, "#8FD3F0", ry=r * 0.9, r_in=1 - 1.2 / r)
    for x, y in ((18, 26), (44, 38), (22, 42)):
        L.px(x + f, y, "#F2F7FA")
    L.circulo(32, 35, 7, "#5A5566", ry=5)
    L.circulo(32, 33, 6, "#C8C8C0", ry=5)
    L.circulo(32, 32, 4, "#F4F1E8", ry=3)
    L.rect(31, 22, 33, 31, "#9AA3A8")
    L.rect(31, 22, 31, 31, "#C8C8C0")
    L.circulo(32, 21, 3, "#C9A227", ry=2)
    alto = (14, 12, 13)[f]
    L.rect(31, alto, 32, 20, "#F2F7FA")
    for i, (dx, dy) in enumerate(((-5, 2), (5, 2), (-8, 6), (8, 6), (-10, 11), (10, 11))):
        if (i + f) % 3 != 0:
            L.px(32 + dx, alto + dy + f, "#F2F7FA")
            L.px(32 + dx, alto + dy + f + 1, "#8FD3F0")
    L.contorno()
    return L.img


def sombra_objeto():
    L = Lienzo(32, 12)
    L.circulo(16, 6, 15, "#1A1420", ry=5)
    return L.img


# ================================================================== hoja
def construir():
    farol_a, farol_b = farol()
    b = bordillo()
    return [
        ("asfalto", asfalto()), ("asfalto_linea", asfalto_linea()), ("paso_peatonal", paso_peatonal()),
        ("alcantarilla", alcantarilla()), ("acera", acera()), ("acera_b", acera(10)), ("acera_sombra", acera_sombra()),
        ("bordillo_s", b), ("bordillo_n", b.rotate(180)), ("bordillo_e", b.rotate(90)), ("bordillo_o", b.rotate(-90)),
        ("plaza", plaza()), ("plaza_b", plaza(9)), ("plaza_grieta", plaza(4, grieta=True)),
        ("plaza_musgo", plaza(6, musgo=True)), ("cenefa_h", cenefa()), ("cenefa_v", cenefa().rotate(90)),
        ("pasto", pasto()), ("pasto_flores", pasto(flores=True)),
        ("pasto_borde_s", pasto_borde("s")), ("pasto_borde_n", pasto_borde("n")),
        ("pasto_borde_e", pasto_borde("e")), ("pasto_borde_o", pasto_borde("o")),
        ("pared", pared()), ("pared_ventana", pared_ventana()), ("pared_viga", pared_viga()),
        ("pared_simbolo", pared_simbolo()), ("pared_baja", pared(False)), ("pared_puerta", pared_puerta()),
        ("pared_tienda", pared_tienda()), ("pared_viga_baja", pared_viga(False)),
        ("techo_rojo", techo_rojo()), ("techo_terracota", techo_terracota()),
        ("cumbrera_roja", cumbrera()), ("cumbrera_terracota", cumbrera(False)),
        ("alero_rojo", alero()), ("alero_terracota", alero(False)),
        ("farol_arriba", farol_a), ("farol_abajo", farol_b), ("farolillo", farolillo()),
        ("banca", banca()), ("letrero", letrero()), ("maceta", maceta()), ("arbusto", arbusto()),
        ("barril", barril()), ("cajas", cajas()),
    ]


GRANDES = lambda: {"arbol": arbol(), "puesto": puesto(), "fuente_0": fuente(0), "fuente_1": fuente(1),
                   "fuente_2": fuente(2), "sombra": sombra_objeto()}


def guardar(tiles):
    out_dir = os.path.join(RAIZ, "juego", "assets", "tilesets")
    suelto = os.path.join(out_dir, "ciudad")
    os.makedirs(suelto, exist_ok=True)
    for f in os.listdir(suelto):
        os.remove(os.path.join(suelto, f))
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
    for n, img in GRANDES().items():
        assert not fuera_de_paleta(img), n
        img.save(os.path.join(out_dir, f"obj_{n}.png"))
    return hoja


# ================================================================== composición de mapas
def componer(tiles, plano, objetos=(), w=None, h=None):
    t = dict(tiles); t.update(GRANDES())
    w = w or len(plano[0]) * T
    h = h or len(plano) * T
    img = Image.new("RGBA", (w, h), a_rgb("#24222B") + (255,))
    for y, fila in enumerate(plano):
        for x, n in enumerate(fila):
            if n:
                img.alpha_composite(t[n], (x * T, y * T))
    for n, x, y in objetos:
        img.alpha_composite(t[n], (x, y))
    return img


def _farol(objs, x, y):
    objs += [("farol_arriba", x, y), ("farol_abajo", x, y + T)]


def mapa_ejemplo(tiles):
    cr, ct = "cumbrera_roja", "cumbrera_terracota"
    tr, tt, ar, at = "techo_rojo", "techo_terracota", "alero_rojo", "alero_terracota"
    pl = lambda x, y: ("plaza", "plaza_b", "plaza", "plaza_musgo", "plaza", "plaza_grieta")[(x * 7 + y * 3) % 6]
    plano = [
        [cr] * 7 + [ct] * 6 + [cr] * 7,
        [tr] * 7 + [tt] * 6 + [tr] * 7,
        [ar] * 7 + [at] * 6 + [ar] * 7,
        ["pared_ventana", "pared", "pared_ventana", "pared_viga", "pared_ventana", "pared_simbolo", "pared_ventana",
         "pared_viga", "pared_ventana", "pared", "pared_ventana", "pared", "pared_ventana", "pared_viga",
         "pared_ventana", "pared", "pared_ventana", "pared", "pared_ventana", "pared"],
        ["pared_baja", "pared_puerta", "pared_tienda", "pared_viga_baja", "pared_baja", "pared_tienda", "pared_baja",
         "pared_viga_baja", "pared_puerta", "pared_baja", "pared_tienda", "pared_tienda", "pared_puerta", "pared_viga_baja",
         "pared_baja", "pared_tienda", "pared_puerta", "pared_baja", "pared_tienda", "pared_baja"],
        ["acera_sombra"] * 20,
        [("acera", "acera_b")[x % 2] for x in range(20)],
        ["bordillo_s"] * 20,
        ["asfalto"] * 5 + ["paso_peatonal"] * 2 + ["asfalto"] * 4 + ["alcantarilla"] + ["asfalto"] * 8,
        ["asfalto_linea"] * 5 + ["paso_peatonal"] * 2 + ["asfalto_linea"] * 13,
        ["asfalto"] * 5 + ["paso_peatonal"] * 2 + ["asfalto"] * 13,
        ["bordillo_n"] * 20,
        ["pasto", "pasto_borde_e"] + ["cenefa_h"] * 16 + ["pasto_borde_o", "pasto_flores"],
        ["pasto_flores", "pasto_borde_e"] + [pl(x, 13) for x in range(16)] + ["pasto_borde_o", "pasto"],
        ["pasto", "pasto_borde_e"] + [pl(x, 14) for x in range(16)] + ["pasto_borde_o", "pasto"],
    ]
    objs = [("farolillo", 2 * T, 4 * T - 6), ("farolillo", 9 * T, 4 * T - 6), ("farolillo", 15 * T, 4 * T - 6),
            ("letrero", 6 * T + 2, 3 * T + 6), ("maceta", 4 * T, 5 * T + 2), ("maceta", 12 * T, 5 * T + 2),
            ("barril", 17 * T, 5 * T + 4), ("cajas", 18 * T, 5 * T + 4), ("arbol", 0, 11 * T - 4),
            ("arbol", 18 * T, 11 * T - 4), ("banca", 5 * T, 14 * T), ("banca", 14 * T, 14 * T),
            ("fuente_0", 9 * T, 13 * T - 8)]
    _farol(objs, 3 * T, 11 * T - 8)
    _farol(objs, 16 * T, 11 * T - 8)
    objs.append(("puesto", 20 * T - 96, 5 * T - 24))
    return componer(tiles, plano, objs)


def fondo_pelea(tiles):
    t = dict(tiles)
    img = Image.new("RGBA", (640, 360), a_rgb("#24222B") + (255,))
    alto = ["pared_ventana", "pared_viga", "pared_ventana", "pared", "pared_ventana", "pared_viga", "pared_ventana",
            "pared", "pared_ventana", "pared_simbolo", "pared_ventana", "pared", "pared_ventana", "pared_viga",
            "pared_ventana", "pared", "pared_ventana", "pared_viga", "pared_ventana", "pared"]
    bajo = ["pared_tienda", "pared_viga_baja", "pared_puerta", "pared_baja", "pared_tienda", "pared_viga_baja",
            "pared_baja", "pared_tienda", "pared_puerta", "pared_baja", "pared_tienda", "pared_baja", "pared_puerta",
            "pared_viga_baja", "pared_tienda", "pared_baja", "pared_puerta", "pared_viga_baja", "pared_tienda", "pared_baja"]
    for x in range(20):
        terr = 7 <= x < 13
        img.alpha_composite(t["techo_terracota" if terr else "techo_rojo"].crop((0, 16, 32, 32)), (x * T, 0))
        img.alpha_composite(t["alero_terracota" if terr else "alero_rojo"], (x * T, 16))
        img.alpha_composite(t[alto[x]], (x * T, 48))
        img.alpha_composite(t[bajo[x]], (x * T, 80))
        img.alpha_composite(t["acera_sombra"], (x * T, 112))
        img.alpha_composite(t["cenefa_h"], (x * T, 144))
    for y in range(176, 360, T):
        for x in range(20):
            n = ("plaza", "plaza_b", "plaza", "plaza_musgo", "plaza", "plaza_grieta")[(x * 7 + y // T * 3) % 6]
            img.alpha_composite(t[n], (x * T, y))
    d = ImageDraw.Draw(img)
    cx, cy = 320, 272
    for (rx, ry, c, w) in ((190, 78, "#C9A227", 2), (184, 74, "#8E1B1B", 5), (176, 69, "#C9A227", 1),
                           (34, 14, "#8E1B1B", 3)):
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=a_rgb(c) + (255,), width=w)
    d.ellipse([cx - 27, cy - 11, cx + 27, cy + 11], fill=a_rgb("#D9481E") + (255,))
    d.ellipse([cx - 18, cy - 7, cx + 18, cy + 7], fill=a_rgb("#F28C28") + (255,))
    d.ellipse([cx - 8, cy - 3, cx + 8, cy + 3], fill=a_rgb("#E8D27A") + (255,))
    g = GRANDES()
    for n, x, y in (("farolillo", 72, 86), ("farolillo", 232, 86), ("farolillo", 376, 86), ("farolillo", 536, 86),
                    ("maceta", 150, 114), ("maceta", 458, 114), ("barril", 600, 112), ("cajas", 4, 112)):
        img.alpha_composite(t[n], (x, y))
    for x in (24, 584):
        img.alpha_composite(t["farol_arriba"], (x, 150)); img.alpha_composite(t["farol_abajo"], (x, 182))
    img.alpha_composite(g["arbol"], (-14, 300))
    img.alpha_composite(g["arbol"], (590, 300))
    img.alpha_composite(t["banca"], (110, 336)); img.alpha_composite(t["banca"], (498, 336))
    return img


if __name__ == "__main__":
    tiles = construir()
    hoja = guardar(tiles)
    prev = os.path.join(RAIZ, "arte_fuente", "previews")
    hoja.resize((hoja.width * 3, hoja.height * 3), Image.NEAREST).save(os.path.join(prev, "tiles_ciudad_x3.png"))
    m = mapa_ejemplo(tiles)
    assert not fuera_de_paleta(m)
    m.save(os.path.join(prev, "mapa_ciudad_ejemplo.png"))
    fp = fondo_pelea(tiles)
    assert not fuera_de_paleta(fp), fuera_de_paleta(fp)
    fp.save(os.path.join(RAIZ, "juego", "assets", "tilesets", "fondo_pelea_plaza.png"))
    print(len(tiles), "tiles")
