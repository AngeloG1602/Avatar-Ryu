"""Zona de tierra: camino de montaña, cañón, mina y cámara sellada. Tiles de 32x32, paleta oficial.

Genera:
  juego/assets/tilesets/tiles_tierra.png (+ .json) y tierra/<nombre>.png
  juego/assets/tilesets/obj_<nombre>.png   (pino, entrada_mina, vagoneta, puerta elemental, pistas)
  juego/assets/tilesets/fondo_pelea_canon.png, fondo_pelea_mina.png (640x360)
  arte_fuente/previews/mapa_tierra_ejemplo.png
Uso: python3 herramientas/tiles_tierra.py
"""
import json
import math
import os
import random
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from paleta import a_rgb, fuera_de_paleta
from tiles_ciudad import Lienzo, RAIZ, T, OSCURECER

TS = os.path.join(RAIZ, "juego", "assets", "tilesets")

# rocas del cañón (rojizas) y de la mina (oscuras)
CANON = ["#6E4426", "#A86B3C", "#D9A06B", "#F2C9A0"]
MINA = ["#1A1420", "#2B2230", "#4A3B32", "#7A5230"]


def _salpicar(L, n, colores, semilla, x0=0, y0=0, x1=31, y1=31):
    rnd = random.Random(semilla)
    for _ in range(n):
        L.px(rnd.randint(x0, x1), rnd.randint(y0, y1), rnd.choice(colores))


def _piedra(L, cx, cy, rx, ry, pal, semilla=0):
    """Piedra redondeada con luz arriba-izquierda."""
    L.circulo(cx, cy + 1, rx, pal[0], ry=ry)
    L.circulo(cx, cy, rx, pal[1], ry=ry)
    L.circulo(cx - rx * 0.3, cy - ry * 0.3, rx * 0.5, pal[2], ry=ry * 0.45)


# ================================================================== exterior
def sendero(semilla=1):
    L = Lienzo(fondo="#C29A5B")
    _salpicar(L, 40, ["#D9A06B", "#E8D27A"], semilla)
    _salpicar(L, 30, ["#A86B3C", "#7A5230"], semilla + 1)
    rnd = random.Random(semilla + 2)
    for _ in range(4):
        _piedra(L, rnd.randrange(3, 29), rnd.randrange(3, 29), 1.8, 1.4, ["#7A5230", "#A86B3C", "#D9A06B"])
    return L.img


def pasto_monte(semilla=3):
    L = Lienzo(fondo="#6B8E3D")
    rnd = random.Random(semilla)
    for _ in range(6):
        cx, cy, r = rnd.randrange(32), rnd.randrange(32), rnd.randrange(3, 6)
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r and (x + y) % 2 == 0:
                    L.px(x, y, "#3F5A2A", envolver=True)
    for _ in range(14):
        x, y = rnd.randrange(32), rnd.randrange(32)
        L.px(x, y, "#C29A5B", True); L.px(x + 1, y - 1, "#C29A5B", True); L.px(x - 1, y - 1, "#7A5230", True)
    return L.img


def suelo_rocoso(semilla=5):
    L = Lienzo(fondo="#A86B3C")
    _salpicar(L, 40, ["#7A5230", "#6E4426"], semilla)
    _salpicar(L, 20, ["#D9A06B"], semilla + 1)
    rnd = random.Random(semilla + 2)
    for _ in range(5):
        _piedra(L, rnd.randrange(3, 29), rnd.randrange(3, 29), rnd.uniform(2, 3.5), rnd.uniform(1.5, 2.5), CANON)
    for x, y in ((4, 20), (5, 21), (6, 21), (7, 22), (8, 22)):
        L.px(x, y, "#6E4426")
    return L.img


def sendero_borde(lado):
    """Pasto de montaña que se funde con el sendero por un lado."""
    p, q = pasto_monte(11), sendero(12)
    L = Lienzo.de(q)
    pp = p.load()
    for y in range(32):
        for x in range(32):
            u, v = {"s": (x, y), "n": (x, 31 - y), "e": (y, x), "o": (y, 31 - x)}[lado]
            lim = 17 + round(2 * math.sin(u * 0.6) + math.sin(u * 1.7))
            if v < lim:
                L.p[x, y] = pp[x, y]
            elif v == lim:
                L.px(x, y, "#3F5A2A")
            elif v == lim + 1:
                L.px(x, y, "#7A5230")
    return L.img


def _estratos(L, y0, y1, semilla, pal=CANON):
    """Cara de acantilado: estratos de grosor variable con bordes ondulados y grietas."""
    rnd = random.Random(semilla)
    # límites de banda que se repiten cada 32 px para que el tile encaje
    limites = [0, 5, 9, 16, 19, 26, 32]
    colores = [pal[1], pal[2], pal[1], pal[0], pal[2], pal[1]]
    for x in range(32):
        ond = [round(1.4 * math.sin(x * 2 * math.pi / 32 * (k + 1) + k)) for k in range(len(limites))]
        for y in range(y0, y1 + 1):
            yy = y - y0
            banda = 0
            for k in range(1, len(limites) - 1):
                if yy >= limites[k] + ond[k]:
                    banda = k
            c = colores[banda]
            L.px(x, y, c)
            if any(yy == limites[k] + ond[k] for k in range(1, len(limites) - 1)):
                L.px(x, y, pal[0])
            elif any(yy == limites[k] + ond[k] + 1 for k in range(1, len(limites) - 1)) and c != pal[2]:
                L.px(x, y, pal[2])
    for _ in range(18):
        L.px(rnd.randrange(32), rnd.randrange(y0, y1 + 1), rnd.choice([pal[0], pal[3]]))
    for _ in range(3):
        x = rnd.randrange(32)
        yy = rnd.randrange(y0, max(y0 + 1, y1 - 6))
        for k in range(rnd.randrange(5, 10)):
            xx = x + (k // 3) * (1 if semilla % 2 else -1)
            L.px(xx, yy + k, pal[0], envolver=True)
            L.px(xx + 1, yy + k, pal[2], envolver=True)


def acantilado(semilla=21):
    L = Lienzo()
    _estratos(L, 0, 31, semilla)
    return L.img


def acantilado_borde(semilla=22):
    """Borde superior: pasto arriba, labio de roca y cara del acantilado."""
    L = Lienzo.de(pasto_monte(semilla))
    for x in range(32):
        lim = 10 + round(1.5 * math.sin(x * 0.5) + math.sin(x * 1.3))
        for y in range(lim, 32):
            L.px(x, y, "#D9A06B" if y < lim + 2 else "#A86B3C")
        L.px(x, lim - 1, "#3F5A2A")
        L.px(x, lim, "#F2C9A0")
    tmp = Lienzo()
    _estratos(tmp, 0, 31, semilla)
    for y in range(16, 32):
        for x in range(32):
            L.p[x, y] = tmp.p[x, y]
    L.rect(0, 15, 31, 15, "#6E4426")
    return L.img


def acantilado_base(semilla=23):
    """Base del acantilado: cara arriba, escombros y sombra sobre el suelo."""
    L = Lienzo.de(suelo_rocoso(semilla))
    tmp = Lienzo()
    _estratos(tmp, 0, 31, semilla)
    for y in range(0, 14):
        for x in range(32):
            L.p[x, y] = tmp.p[x, y]
    L.rect(0, 14, 31, 14, "#6E4426")
    L.oscurecer(lambda x, y: 15 <= y <= 20 or (21 <= y <= 22 and (x + y) % 2 == 0))
    rnd = random.Random(semilla)
    for _ in range(4):
        _piedra(L, rnd.randrange(3, 29), rnd.randrange(14, 22), rnd.uniform(2, 3.5), 2, CANON)
    return L.img


def roca_grande():
    L = Lienzo()
    L.sombra_suelo(16, 28, 13, 3)
    pts = [(4, 24), (6, 12), (12, 5), (22, 6), (28, 13), (29, 24), (20, 27), (9, 27)]
    from tiles_ciudad import ImageDraw
    d = ImageDraw.Draw(L.img)
    d.polygon(pts, fill=a_rgb("#A86B3C") + (255,))
    d.polygon([(6, 13), (12, 6), (21, 7), (17, 13), (8, 17)], fill=a_rgb("#D9A06B") + (255,))
    d.polygon([(28, 14), (29, 24), (20, 27), (22, 18)], fill=a_rgb("#6E4426") + (255,))
    L.p = L.img.load()
    L.linea(12, 7, 16, 12, "#F2C9A0")
    L.linea(17, 15, 21, 24, "#6E4426")
    L.contorno()
    return L.img


def piedras():
    L = Lienzo()
    L.sombra_suelo(16, 27, 12, 2)
    for cx, cy, r in ((10, 22, 5), (21, 23, 4), (16, 16, 3.5), (25, 18, 2.5)):
        _piedra(L, cx, cy, r, r * 0.8, CANON)
    L.contorno()
    return L.img


def arbusto_seco():
    L = Lienzo()
    L.sombra_suelo(16, 28, 10, 2)
    rnd = random.Random(4)
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.33
        L.linea(16, 27, int(16 + math.cos(a) * rnd.uniform(9, 13)), int(27 + math.sin(a) * rnd.uniform(9, 14)), "#7A5230")
    for _ in range(18):
        x, y = rnd.randrange(6, 26), rnd.randrange(12, 26)
        if L.p[x, y][3] or rnd.random() < .4:
            L.px(x, y, rnd.choice(["#6B8E3D", "#C29A5B", "#3F5A2A"]))
    L.contorno()
    return L.img


def pino():
    """Pino de 2x2 tiles (64x64)."""
    L = Lienzo(64, 64)
    L.sombra_suelo(32, 59, 16, 3)
    L.rect(29, 46, 34, 59, "#7A5230"); L.rect(29, 46, 30, 59, "#C29A5B"); L.rect(34, 46, 34, 59, "#4A3B32")
    from tiles_ciudad import ImageDraw
    d = ImageDraw.Draw(L.img)
    for (top, base, ancho) in ((2, 22, 12), (12, 36, 18), (24, 50, 24)):
        d.polygon([(32, top), (32 - ancho, base), (32 + ancho, base)], fill=a_rgb("#3F5A2A") + (255,))
        d.polygon([(32, top + 2), (32 - ancho + 4, base - 2), (31, base - 4)], fill=a_rgb("#6B8E3D") + (255,))
        for x in range(32 - ancho + 2, 32 + ancho - 1, 4):
            L.px(x, base - 1, "#2B2230") if False else None
    L.p = L.img.load()
    rnd = random.Random(1)
    for _ in range(30):
        x, y = rnd.randrange(10, 54), rnd.randrange(4, 48)
        if L.p[x, y][3]:
            L.px(x, y, rnd.choice(["#2B2230", "#C29A5B", "#3F5A2A"]))
    L.contorno()
    return L.img


def entrada_mina():
    """Boca de la mina en la cara del acantilado, 96x64 (3x2 tiles)."""
    L = Lienzo(96, 64)
    for tx in range(3):
        for ty in range(2):
            tile = Lienzo()
            _estratos(tile, 0, 31, 30 + tx + ty)
            L.img.paste(tile.img, (tx * 32, ty * 32))
    L.p = L.img.load()
    # túnel oscuro con degradado tramado
    L.rect(26, 18, 69, 63, "#1A1420")
    for y in range(18, 40):
        for x in range(26, 70):
            if (x + y) % 2 == 0 and y < 30:
                L.px(x, y, "#24222B")
    # vigas
    for x0 in (20, 70):
        L.rect(x0, 14, x0 + 5, 63, "#7A5230")
        L.rect(x0, 14, x0 + 1, 63, "#C29A5B")
        L.rect(x0 + 5, 14, x0 + 5, 63, "#4A3B32")
    L.rect(16, 8, 79, 15, "#7A5230")
    L.rect(16, 8, 79, 9, "#C29A5B")
    L.rect(16, 15, 79, 15, "#4A3B32")
    for x in (22, 73):
        L.rect(x, 11, x + 1, 12, "#5A5566")
    # letrero
    L.rect(38, 1, 57, 7, "#7A5230"); L.rect(38, 1, 57, 1, "#C29A5B")
    for x in range(41, 55, 3):
        L.rect(x, 3, x + 1, 5, "#2B2230")
    # lámpara colgando
    L.rect(47, 16, 48, 21, "#2B2230")
    L.rect(45, 22, 50, 27, "#C9A227"); L.rect(46, 23, 49, 26, "#E8D27A"); L.px(47, 24, "#F4F1E8")
    # rieles saliendo
    for y in range(40, 64, 4):
        L.rect(32, y, 63, y + 1, "#4A3B32")
    L.rect(36, 40, 37, 63, "#9AA3A8"); L.rect(58, 40, 59, 63, "#9AA3A8")
    return L.img


# ================================================================== mina
def mina_suelo(semilla=40):
    L = Lienzo(fondo="#4A3B32")
    _salpicar(L, 50, ["#2B2230", "#7A5230"], semilla)
    rnd = random.Random(semilla)
    for _ in range(3):
        _piedra(L, rnd.randrange(3, 29), rnd.randrange(3, 29), rnd.uniform(1.5, 2.5), 1.5, MINA)
    if semilla % 2:
        L.px(rnd.randrange(32), rnd.randrange(32), "#C9A227")
    return L.img


def mina_pared(semilla=41, beta=True):
    """Cara de la pared de la mina con vetas de mineral."""
    L = Lienzo(fondo="#4A3B32")
    rnd = random.Random(semilla)
    for _ in range(9):
        cx, cy = rnd.randrange(32), rnd.randrange(32)
        rx, ry = rnd.uniform(3, 7), rnd.uniform(2, 4)
        for y in range(int(cy - ry), int(cy + ry) + 1):
            for x in range(int(cx - rx), int(cx + rx) + 1):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    L.px(x, y, "#7A5230" if y < cy else "#4A3B32", envolver=True)
        L.px(int(cx - rx / 2), int(cy - ry / 2), "#C29A5B", envolver=True)
        for x in range(int(cx - rx), int(cx + rx)):
            L.px(x, int(cy + ry), "#2B2230", envolver=True)
    if beta:
        x, y = rnd.randrange(6, 26), rnd.randrange(6, 26)
        for k in range(6):
            L.px(x + k, y + (k % 2), "#C9A227")
            if k % 2:
                L.px(x + k, y - 1, "#E8D27A")
    return L.img


def mina_pared_borde():
    """Parte superior de la pared (techo de roca visto desde arriba) + inicio de la cara."""
    L = Lienzo.de(mina_pared(42))
    for y in range(0, 12):
        for x in range(32):
            L.px(x, y, "#24222B" if (x * 3 + y * 5) % 11 else "#2B2230")
    L.rect(0, 12, 31, 12, "#7A5230")
    L.rect(0, 13, 31, 13, "#C29A5B")
    return L.img


def mina_viga():
    L = Lienzo.de(mina_pared(43, beta=False))
    L.rect(2, 0, 7, 31, "#7A5230"); L.rect(2, 0, 3, 31, "#C29A5B"); L.rect(7, 0, 7, 31, "#4A3B32")
    L.rect(24, 0, 29, 31, "#7A5230"); L.rect(24, 0, 25, 31, "#C29A5B"); L.rect(29, 0, 29, 31, "#4A3B32")
    L.rect(0, 2, 31, 7, "#7A5230"); L.rect(0, 2, 31, 3, "#C29A5B"); L.rect(0, 7, 31, 7, "#4A3B32")
    for x in (4, 26):
        L.rect(x, 4, x + 1, 5, "#5A5566")
    return L.img


def mina_base():
    """Base de la pared con sombra sobre el suelo."""
    L = Lienzo.de(mina_suelo(44))
    tmp = mina_pared(45)
    L.img.paste(tmp.crop((0, 0, 32, 12)), (0, 0)); L.p = L.img.load()
    L.rect(0, 12, 31, 12, "#2B2230")
    L.oscurecer(lambda x, y: 13 <= y <= 19 or (y <= 21 and (x + y) % 2 == 0 and y > 12))
    return L.img


def rieles(vertical=False):
    L = Lienzo.de(mina_suelo(46))
    for y in range(1, 32, 6):
        L.rect(4, y, 27, y + 2, "#7A5230")
        L.rect(4, y, 27, y, "#C29A5B")
        L.rect(4, y + 2, 27, y + 2, "#4A3B32")
    for x in (8, 22):
        L.rect(x, 0, x + 1, 31, "#9AA3A8")
        L.rect(x, 0, x, 31, "#C8C8C0")
    return L.img.rotate(90) if vertical else L.img


def lampara_mina():
    L = Lienzo()
    L.rect(14, 0, 17, 3, "#5A5566")
    L.rect(15, 4, 16, 8, "#2B2230")
    L.rect(11, 9, 20, 10, "#C9A227")
    L.rect(11, 11, 20, 20, "#C9A227")
    L.rect(12, 12, 19, 19, "#F28C28")
    L.rect(13, 13, 18, 18, "#E8D27A")
    L.rect(15, 14, 16, 16, "#F4F1E8")
    L.rect(11, 21, 20, 22, "#C9A227")
    L.rect(14, 11, 14, 20, "#C9A227"); L.rect(17, 11, 17, 20, "#C9A227")
    L.contorno()
    return L.img


def vagoneta():
    L = Lienzo(32, 32)
    L.sombra_suelo(16, 28, 13, 2)
    L.rect(4, 12, 27, 24, "#5A5566")
    L.rect(4, 12, 27, 13, "#9AA3A8")
    L.rect(4, 24, 27, 24, "#3B3846")
    L.rect(3, 11, 28, 11, "#C8C8C0")
    for x in (9, 16, 23):
        L.rect(x, 14, x, 23, "#3B3846")
    for cx, cy, c in ((10, 9, "#C29A5B"), (16, 8, "#7A5230"), (21, 9, "#C29A5B"), (14, 10, "#C9A227"), (19, 7, "#7A5230")):
        L.circulo(cx, cy, 3, c, ry=2.5)
    L.px(14, 9, "#E8D27A"); L.px(17, 6, "#E8D27A")
    for x in (7, 22):
        L.circulo(x + 1.5, 26, 3, "#2B2230"); L.circulo(x + 1.5, 26, 1.5, "#5A5566")
    L.contorno()
    return L.img


# ================================================================== cámara sellada
def camara_suelo():
    L = Lienzo(fondo="#5A5566")
    for by in (0, 16):
        for bx in (0, 16):
            L.rect(bx + 1, by + 1, bx + 14, by + 14, "#9AA3A8")
            L.rect(bx + 1, by + 1, bx + 14, by + 1, "#C8C8C0")
            L.rect(bx + 1, by + 1, bx + 1, by + 14, "#C8C8C0")
            L.rect(bx + 2, by + 14, bx + 14, by + 14, "#5A5566")
            L.rect(bx + 14, by + 2, bx + 14, by + 14, "#5A5566")
    # incrustación verde en las juntas
    L.rect(14, 14, 17, 17, "#6B8E3D"); L.rect(15, 15, 16, 16, "#C29A5B")
    for x, y in ((0, 0), (31, 0), (0, 31), (31, 31)):
        L.px(x, y, "#6B8E3D")
    return L.img


def camara_pared():
    L = Lienzo(fondo="#9AA3A8")
    for y in range(0, 32, 8):
        off = 8 if (y // 8) % 2 else 0
        L.rect(0, y, 31, y, "#5A5566")
        L.rect(0, y + 1, 31, y + 1, "#C8C8C0")
        for x in range(off, 32, 16):
            L.rect(x, y, x, y + 7, "#5A5566")
    L.rect(0, 26, 31, 31, "#6B8E3D"); L.rect(0, 26, 31, 26, "#C29A5B"); L.rect(0, 31, 31, 31, "#3F5A2A")
    return L.img


def camara_emblema():
    """Pared con el emblema de la tierra en bajorrelieve dorado y verde."""
    L = Lienzo.de(camara_pared())
    L.circulo(16, 13, 11, "#5A5566")
    L.circulo(16, 13, 10, "#C9A227")
    L.circulo(16, 13, 8, "#3F5A2A")
    L.rect(10, 7, 22, 19, "#C9A227")
    L.rect(11, 8, 21, 18, "#6B8E3D")
    L.rect(13, 10, 19, 16, "#C9A227")
    L.rect(14, 11, 18, 15, "#3F5A2A")
    L.px(10, 7, "#E8D27A"); L.px(11, 8, "#C29A5B")
    return L.img


# ================================================================== puerta elemental (64x64)
def _icono_elemento(L, cx, cy, el):
    if el == "tierra":
        L.rect(cx - 7, cy - 7, cx + 7, cy + 7, "#2B2230")
        L.rect(cx - 6, cy - 6, cx + 6, cy + 6, "#C9A227")
        L.rect(cx - 5, cy - 5, cx + 5, cy + 5, "#6B8E3D")
        L.rect(cx - 2, cy - 2, cx + 2, cy + 2, "#C9A227")
        L.rect(cx - 1, cy - 1, cx + 1, cy + 1, "#3F5A2A")
        L.px(cx - 6, cy - 6, "#E8D27A")
    else:
        L.circulo(cx, cy, 8, "#1E4F8C"); L.circulo(cx, cy, 7, "#8FD3F0"); L.circulo(cx, cy, 6, "#3A86C8")
        for x in range(cx - 5, cx + 6):
            L.px(x, cy - 1 + (1 if (x % 3) else 0), "#F2F7FA")
            L.px(x, cy + 2 + (1 if ((x + 1) % 3) else 0), "#8FD3F0")


def puerta(estado, f=0):
    L = Lienzo(64, 64)
    # marco de piedra
    L.rect(0, 0, 63, 63, "#5A5566")
    L.rect(2, 2, 61, 61, "#9AA3A8")
    L.rect(2, 2, 61, 3, "#C8C8C0")
    L.rect(8, 10, 55, 63, "#24222B")
    L.rect(4, 4, 59, 9, "#7A5230"); L.rect(4, 4, 59, 4, "#C29A5B")
    for x in (2, 58):
        for y in range(12, 62, 8):
            L.rect(x, y, x + 3, y, "#5A5566")
    if estado == "abierta":
        for y in range(10, 64):
            for x in range(8, 56):
                if (x + y) % 2 == 0 and y < 30:
                    L.px(x, y, "#1A1420")
        L.rect(8, 58, 55, 63, "#4A3B32")
        return L.contorno().img
    hundido = {"abriendo": (14, 30, 46)[f]}.get(estado, 0)
    top = 10 + hundido
    if top < 64:
        # losa de roca maciza con grietas
        L.rect(9, top, 54, 63, "#A86B3C")
        L.rect(9, top, 54, top + 1, "#D9A06B")
        L.rect(9, top, 10, 63, "#D9A06B")
        L.rect(53, top, 54, 63, "#6E4426")
        rnd = random.Random(3)
        for _ in range(40):
            y = rnd.randrange(top + 2, 64)
            L.px(rnd.randrange(11, 53), y, rnd.choice(["#7A5230", "#D9A06B"]))
        for (x0, y0, dx) in ((14, 4, 1), (46, 8, -1), (20, 34, 1), (44, 30, -1)):
            for k in range(7):
                yy = top + y0 + k
                if yy < 64:
                    L.px(x0 + (k // 2) * dx, yy, "#6E4426")
        cy = top + 22
        if cy < 58:
            if estado == "cerrada_tierra":
                _icono_elemento(L, 32, cy, "tierra")
            elif estado == "cerrada_tierra_agua":
                _icono_elemento(L, 22, cy, "tierra")
                _icono_elemento(L, 42, cy, "agua")
    if estado == "abriendo":
        rnd = random.Random(f)
        for _ in range(10 + f * 4):
            L.circulo(rnd.randrange(8, 56), rnd.randrange(top - 6, min(top + 4, 63)), rnd.uniform(1, 2.5), "#C29A5B")
    return L.contorno().img


# ================================================================== pistas
def pista_simbolo():
    L = Lienzo()
    L.rect(6, 4, 26, 27, "#F4F1E8"); L.rect(6, 4, 26, 4, "#C8C8C0")
    L.px(26, 27, "#C8C8C0"); L.px(25, 27, "#C8C8C0"); L.px(26, 26, "#C8C8C0")
    L.circulo(16, 15, 7, "#24222B", r_in=0.7)
    L.linea(10, 21, 22, 9, "#8E1B1B"); L.linea(11, 21, 23, 9, "#8E1B1B")
    for x, y in ((16, 7), (24, 15), (16, 23), (8, 15)):
        L.px(x, y, "#24222B")
    L.contorno()
    return L.img


def pista_documento():
    L = Lienzo()
    L.sombra_suelo(16, 28, 11, 2)
    L.rect(7, 3, 25, 27, "#F4F1E8")
    L.rect(7, 3, 25, 3, "#C8C8C0"); L.rect(25, 3, 25, 27, "#C8C8C0")
    L.rect(22, 3, 25, 6, "#C8C8C0"); L.px(22, 6, "#9AA3A8")
    for y in (10, 13, 16, 19, 22):
        L.rect(10, y, 22 - (y % 4), y, "#5A5566")
    L.circulo(13, 6, 2.5, "#24222B", r_in=0.5)
    L.px(15, 4, "#8E1B1B"); L.px(11, 8, "#8E1B1B")
    L.contorno()
    return L.img


def pista_diario():
    L = Lienzo()
    L.sombra_suelo(16, 28, 12, 2)
    L.rect(6, 6, 26, 25, "#3F5A2A")
    L.rect(6, 6, 26, 7, "#6B8E3D")
    L.rect(6, 6, 8, 25, "#2B2230")
    L.rect(9, 24, 26, 25, "#F4F1E8")
    L.rect(9, 26, 26, 26, "#C8C8C0")
    L.rect(13, 11, 21, 19, "#C9A227"); L.rect(14, 12, 20, 18, "#6B8E3D"); L.rect(16, 14, 18, 16, "#C9A227")
    L.rect(24, 13, 27, 17, "#7A5230"); L.px(26, 15, "#C9A227")
    L.contorno()
    return L.img


# ================================================================== hoja y fondos
def construir():
    return [
        ("sendero", sendero()), ("sendero_b", sendero(7)), ("pasto_monte", pasto_monte()),
        ("suelo_rocoso", suelo_rocoso()), ("suelo_rocoso_b", suelo_rocoso(9)),
        ("sendero_borde_s", sendero_borde("s")), ("sendero_borde_n", sendero_borde("n")),
        ("sendero_borde_e", sendero_borde("e")), ("sendero_borde_o", sendero_borde("o")),
        ("acantilado", acantilado()), ("acantilado_b", acantilado(27)),
        ("acantilado_borde", acantilado_borde()), ("acantilado_base", acantilado_base()),
        ("roca_grande", roca_grande()), ("piedras", piedras()), ("arbusto_seco", arbusto_seco()),
        ("mina_suelo", mina_suelo()), ("mina_suelo_b", mina_suelo(47)), ("mina_pared", mina_pared()),
        ("mina_pared_borde", mina_pared_borde()), ("mina_viga", mina_viga()), ("mina_base", mina_base()),
        ("rieles_v", rieles()), ("rieles_h", rieles(True)), ("lampara_mina", lampara_mina()), ("vagoneta", vagoneta()),
        ("camara_suelo", camara_suelo()), ("camara_pared", camara_pared()), ("camara_emblema", camara_emblema()),
    ]


def objetos():
    o = {"pino": pino(), "entrada_mina": entrada_mina(),
         "puerta_elemental_cerrada_tierra": puerta("cerrada_tierra"),
         "puerta_elemental_cerrada_tierra_agua": puerta("cerrada_tierra_agua"),
         "puerta_elemental_abierta": puerta("abierta"),
         "pista_simbolo": pista_simbolo(), "pista_documento": pista_documento(), "pista_diario": pista_diario()}
    for f in range(3):
        o[f"puerta_elemental_abriendo_{f}"] = puerta("abriendo", f)
    return o


def guardar(tiles):
    suelto = os.path.join(TS, "tierra")
    os.makedirs(suelto, exist_ok=True)
    cols = 8
    hoja = Image.new("RGBA", (cols * T, ((len(tiles) + cols - 1) // cols) * T), (0, 0, 0, 0))
    indice = {}
    for i, (n, img) in enumerate(tiles):
        assert not fuera_de_paleta(img), (n, fuera_de_paleta(img))
        hoja.alpha_composite(img, ((i % cols) * T, (i // cols) * T))
        img.save(os.path.join(suelto, n + ".png"))
        indice[i] = n
    hoja.save(os.path.join(TS, "tiles_tierra.png"))
    with open(os.path.join(TS, "tiles_tierra.json"), "w") as fh:
        json.dump({"tamano_tile": T, "columnas": cols, "tiles": indice}, fh, indent=2, ensure_ascii=False)
    for n, img in objetos().items():
        assert not fuera_de_paleta(img), n
        img.save(os.path.join(TS, f"obj_{n}.png"))
    return hoja


def _pintar(img, t, plano, y0=0):
    for y, fila in enumerate(plano):
        for x, n in enumerate(fila):
            img.alpha_composite(t[n], (x * T, y0 + y * T))


def fondo_canon(tiles):
    t = dict(tiles); o = objetos()
    img = Image.new("RGBA", (640, 360), a_rgb("#24222B") + (255,))
    for x in range(20):
        img.alpha_composite(t["acantilado" if x % 3 else "acantilado_b"], (x * T, -16))
        img.alpha_composite(t["acantilado"], (x * T, 16))
        img.alpha_composite(t["acantilado_base"], (x * T, 48))
    for y in range(80, 360, T):
        for x in range(20):
            if x == 0 or x == 19:
                n = "pasto_monte"
            elif x == 1:
                n = "sendero_borde_e"
            elif x == 18:
                n = "sendero_borde_o"
            else:
                h = (x * 73 + (y // T) * 151) % 10
                n = "sendero_b" if h < 4 else "sendero"
            img.alpha_composite(t[n], (x * T, y))
    for n, x, y in (("roca_grande", 40, 100), ("piedras", 560, 96), ("arbusto_seco", 120, 300), ("piedras", 300, 320),
                    ("roca_grande", 590, 300), ("arbusto_seco", 480, 110)):
        img.alpha_composite(t[n], (x, y))
    img.alpha_composite(o["pino"], (-20, 120)); img.alpha_composite(o["pino"], (596, 150))
    img.alpha_composite(o["pino"], (-10, 280))
    return img


def fondo_mina(tiles):
    t = dict(tiles)
    img = Image.new("RGBA", (640, 360), a_rgb("#1A1420") + (255,))
    for x in range(20):
        img.alpha_composite(t["mina_pared_borde"], (x * T, 0))
        img.alpha_composite(t["mina_viga" if x % 5 == 2 else "mina_pared"], (x * T, 32))
        img.alpha_composite(t["mina_base"], (x * T, 64))
    for y in range(96, 360, T):
        for x in range(20):
            n = "rieles_h" if y == 256 else ("mina_suelo", "mina_suelo_b")[(x * 3 + y // T) % 2]
            img.alpha_composite(t[n], (x * T, y))
    for x in (84, 244, 404, 564):
        img.alpha_composite(t["lampara_mina"], (x, 34))
    img.alpha_composite(t["vagoneta"], (520, 246))
    img.alpha_composite(t["piedras"], (40, 110)); img.alpha_composite(t["piedras"], (590, 320))
    # borde oscuro tramado en los lados para encerrar la arena
    L = Lienzo.de(img)
    L.oscurecer(lambda x, y: (x < 12 or x > 627) and (x + y) % 2 == 0)
    return L.img


def mapa_ejemplo(tiles):
    t = dict(tiles); o = objetos()
    img = Image.new("RGBA", (640, 480), a_rgb("#24222B") + (255,))
    plano = []
    plano.append(["pasto_monte"] * 20)
    plano.append(["acantilado_borde"] * 20)
    plano.append(["acantilado"] * 20)
    plano.append(["acantilado_b"] * 20)
    plano.append(["acantilado_base"] * 20)
    for y in range(5, 10):
        plano.append([("pasto_monte" if x < 7 or x > 12 else ("sendero_borde_o" if x == 7 else "sendero_borde_e" if x == 12 else "sendero"))
                      for x in range(20)])
    plano.append(["mina_pared_borde"] * 20)
    plano.append(["mina_viga" if x % 5 == 2 else "mina_pared" for x in range(20)])
    plano.append(["mina_base"] * 20)
    plano.append(["mina_suelo", "mina_suelo_b"] * 4 + ["rieles_h"] * 4 + ["mina_suelo_b", "mina_suelo"] * 2 + ["camara_suelo"] * 4)
    plano.append(["mina_suelo_b", "mina_suelo"] * 8 + ["camara_suelo"] * 4)
    _pintar(img, t, plano)
    img.alpha_composite(t["camara_emblema"], (17 * T, 11 * T)); img.alpha_composite(t["camara_pared"], (16 * T, 11 * T))
    img.alpha_composite(t["camara_pared"], (18 * T, 11 * T)); img.alpha_composite(t["camara_pared"], (19 * T, 11 * T))
    img.alpha_composite(o["entrada_mina"], (8 * T, 2 * T + 32))
    img.alpha_composite(o["pino"], (T, 5 * T)); img.alpha_composite(o["pino"], (16 * T, 5 * T + 10))
    img.alpha_composite(t["roca_grande"], (4 * T, 7 * T)); img.alpha_composite(t["arbusto_seco"], (14 * T, 8 * T))
    img.alpha_composite(o["puerta_elemental_cerrada_tierra"], (5 * T, 10 * T + 16))
    img.alpha_composite(o["puerta_elemental_cerrada_tierra_agua"], (12 * T - 16, 10 * T + 16))
    img.alpha_composite(t["lampara_mina"], (3 * T, 11 * T)); img.alpha_composite(t["vagoneta"], (9 * T, 12 * T + 10))
    img.alpha_composite(o["pista_documento"], (2 * T, 14 * T)); img.alpha_composite(o["pista_diario"], (18 * T, 14 * T))
    return img


if __name__ == "__main__":
    tiles = construir()
    hoja = guardar(tiles)
    prev = os.path.join(RAIZ, "arte_fuente", "previews")
    hoja.resize((hoja.width * 3, hoja.height * 3), Image.NEAREST).save(os.path.join(prev, "tiles_tierra_x3.png"))
    for n, fn in (("fondo_pelea_canon", fondo_canon), ("fondo_pelea_mina", fondo_mina)):
        im = fn(tiles)
        assert not fuera_de_paleta(im), (n, fuera_de_paleta(im))
        im.save(os.path.join(TS, n + ".png"))
    m = mapa_ejemplo(tiles)
    assert not fuera_de_paleta(m)
    m.save(os.path.join(prev, "mapa_tierra_ejemplo.png"))
    # objetos en una hoja
    o = objetos()
    ho = Image.new("RGBA", (sum(i.width + 8 for i in o.values()) + 8, 72), a_rgb("#3B3846") + (255,))
    x = 8
    for i in o.values():
        ho.alpha_composite(i, (x, 4)); x += i.width + 8
    ho.resize((ho.width * 2, ho.height * 2), Image.NEAREST).save(os.path.join(prev, "objetos_tierra.png"))
    print(len(tiles), "tiles,", len(o), "objetos")
