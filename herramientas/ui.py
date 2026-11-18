"""Interfaz: HUD, iconos, caja de diálogo, teclas/botones y pantallas (640x360).

Fuente: Press Start 2P (SIL Open Font License), en juego/assets/ui/fuente/.
Salida: juego/assets/ui/
Uso: python3 herramientas/ui.py
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from paleta import a_rgb, fuera_de_paleta, CONTORNO
from tiles_ciudad import Lienzo, RAIZ, OSCURECER

UI = os.path.join(RAIZ, "juego", "assets", "ui")
A = os.path.join(RAIZ, "juego", "assets")
FUENTE = ImageFont.truetype(os.path.join(UI, "fuente", "PressStart2P-Regular.ttf"), 8)

COLOR_JUGADOR = {
    "ryu": ("#D9481E", "#F28C28", "#8E1B1B"),
    "gao": ("#6B8E3D", "#C29A5B", "#3F5A2A"),
    "nerea": ("#3A86C8", "#8FD3F0", "#1E4F8C"),
}


# ================================================================== texto
def texto(s, color, escala=1, contorno=None, sombra=None):
    """Texto pixelado sin suavizado. Devuelve RGBA recortado al ancho del texto (alto fijo)."""
    w = max(8, len(s) * 8 + 4)
    m = Image.new("L", (w, 14), 0)
    d = ImageDraw.Draw(m)
    d.fontmode = "1"
    d.text((1, 3), s, font=FUENTE, fill=255)
    bb = m.getbbox() or (0, 0, 1, 1)
    m = m.crop((bb[0], 0, bb[2], 14))
    img = Image.new("RGBA", m.size, (0, 0, 0, 0))
    img.paste(Image.new("RGBA", m.size, a_rgb(color) + (255,)), (0, 0), m.point(lambda v: 255 if v > 127 else 0))
    if escala > 1:
        img = img.resize((img.width * escala, img.height * escala), Image.NEAREST)
    pad = 2 if (contorno or sombra) else 0
    out = Image.new("RGBA", (img.width + pad * 2 + (escala if sombra else 0), img.height + pad * 2 + (escala if sombra else 0)), (0, 0, 0, 0))
    if sombra:
        sh = Image.new("RGBA", img.size, a_rgb(sombra) + (255,))
        out.paste(sh, (pad + escala, pad + escala), img)
    out.alpha_composite(img, (pad, pad))
    if contorno:
        L = Lienzo.de(out)
        llenos = {(x, y) for y in range(L.h) for x in range(L.w) if L.p[x, y][3]}
        for y in range(L.h):
            for x in range(L.w):
                if (x, y) not in llenos and any((x + dx, y + dy) in llenos for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    L.px(x, y, contorno)
        out = L.img
    return out


def poner(base, img, x, y, centrado=False):
    if centrado:
        x -= img.width // 2
    base.alpha_composite(img, (int(x), int(y)))


def plantilla(filas, roles, w=16, h=16):
    L = Lienzo(w, h)
    for y, f in enumerate(filas):
        for x, ch in enumerate(f):
            if ch in roles:
                L.px(x, y, roles[ch])
    return L


# ================================================================== iconos 16x16
def icono_fuego():
    filas = [
        "......D.........",
        ".....DfD........",
        ".....DffD...D...",
        "....DffffD.DfD..",
        "....DfFFfDDffD..",
        "...DfFFFFfffD...",
        "..DfFFFyFFffD...",
        "..DFFFyyyFFfD...",
        ".DfFFyyyyyFFfD..",
        ".DFFyyyyyyyFFD..",
        ".DFFyyyWyyyFFD..",
        ".DFFFyyyyyFFFD..",
        "..DFFFyyyFFFD...",
        "...DDFFFFFDD....",
        ".....DDDDD......",
    ]
    return plantilla(filas, {"D": "#8E1B1B", "F": "#D9481E", "f": "#F28C28", "y": "#E8D27A", "W": "#F4F1E8"}).contorno().img


def icono_agua():
    filas = [
        ".......B........",
        "......BbB.......",
        "......BbB.......",
        ".....BbbbB......",
        ".....BbbbB......",
        "....BbbbbbB.....",
        "...BbcbbbbbB....",
        "...BcwbbbbbB....",
        "..BbcwbbbbbbB...",
        "..BbcbbbbbbbB...",
        "..BbbbbbbbbbB...",
        "..BbbbbbbbbDB...",
        "...BbbbbbbDB....",
        "....BBbbbBB.....",
        "......BBB.......",
    ]
    return plantilla(filas, {"B": "#1E4F8C", "b": "#3A86C8", "c": "#8FD3F0", "w": "#F2F7FA", "D": "#1E4F8C"}).contorno().img


def icono_tierra():
    filas = [
        "................",
        ".GGGGGGGGGGGGGG.",
        ".GYYYYYYYYYYYYG.",
        ".GYggggggggggYG.",
        ".GYgGGGGGGGGgYG.",
        ".GYgGYYYYYYGgYG.",
        ".GYgGYggggYGgYG.",
        ".GYgGYgGGgYGgYG.",
        ".GYgGYgGGgYGgYG.",
        ".GYgGYggggYGgYG.",
        ".GYgGYYYYYYGgYG.",
        ".GYgGGGGGGGGgYG.",
        ".GYggggggggggYG.",
        ".GYYYYYYYYYYYYG.",
        ".GGGGGGGGGGGGGG.",
    ]
    return plantilla(filas, {"G": "#3F5A2A", "g": "#6B8E3D", "Y": "#C9A227"}).contorno().img


def icono_aire():
    L = Lienzo(16, 16)
    pts = []
    for i in range(40):
        a = i * 0.28
        r = 0.6 + i * 0.16
        pts.append((8 + r * math.cos(a), 8 + r * math.sin(a)))
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L.linea(int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1)), "#F4F1E8")
    L.linea(1, 13, 6, 13, "#C8C8C0"); L.linea(3, 15, 9, 15, "#C8C8C0") if False else None
    for x, y in ((8, 8), (9, 8)):
        L.px(x, y, "#C8C8C0")
    L.contorno()
    return L.img


def icono_pista():
    filas = [
        "................",
        "..PPPPPPPPPPP...",
        ".PwwwwwwwwwwwP..",
        ".PwKKKKKKKwwwP..",
        ".PwwwwwwwwwwwP..",
        ".PwKKKKKKKKKwP..",
        ".PwwwwwwwwwwwP..",
        ".PwKKKKKKwwwwP..",
        ".PwwwwwwwwwwwP..",
        ".PwKKKKKKKKwwP..",
        ".PwwwwwwwwwRRP..",
        ".PwwwwwwwwRRRP..",
        "..PPPPPPPPPPP...",
    ]
    return plantilla(filas, {"P": "#C29A5B", "w": "#F4F1E8", "K": "#5A5566", "R": "#D9481E"}).contorno().img


ICONOS = {"fuego": icono_fuego, "agua": icono_agua, "tierra": icono_tierra, "aire": icono_aire, "pista": icono_pista}


# ================================================================== HUD
def mini_retrato(nombre):
    import retratos_v3 as R
    filas, col = R.RETRATOS[nombre]
    return R.render32(filas, col).crop((4, 1, 28, 25))


def hud(nombre):
    """Panel del jugador: retrato 24x24, nombre y huecos para las barras (vida y energía)."""
    c, cl, co = COLOR_JUGADOR[nombre]
    ancho = 132 if nombre == "ryu" else 112
    L = Lienzo(ancho, 32)
    L.rect(1, 1, ancho - 2, 30, "#24222B")
    L.rect(0, 2, ancho - 1, 29, "#24222B")
    L.rect(2, 1, ancho - 3, 1, c); L.rect(2, 30, ancho - 3, 30, co)
    L.rect(1, 2, 1, 29, c); L.rect(ancho - 2, 2, ancho - 2, 29, co)
    L.rect(2, 2, ancho - 3, 2, cl)
    # retrato
    L.rect(3, 4, 28, 29, co)
    L.img.alpha_composite(mini_retrato(nombre), (4, 5)); L.p = L.img.load()
    # nombre
    poner(L.img, texto(nombre.upper(), "#F4F1E8", sombra="#1A1420"), 31, 1)
    L.p = L.img.load()
    # huecos de barras: vida (31,15) 76x5 y energía (31,23) 76x4
    for (y, h) in ((15, 5), (23, 4)):
        L.rect(31, y, 108, y + h + 1, "#5A5566")
        L.rect(32, y + 1, 107, y + h, "#1A1420")
    if nombre == "ryu":
        L.rect(112, 6, 129, 25, "#5A5566")
        L.rect(113, 7, 128, 24, "#1A1420")
    L.contorno()
    return L.img


def barra(tipo):
    """Relleno de barra (76 px de ancho). En GDevelop: escalar en X según vida/vidaMax."""
    if tipo == "vida":
        L = Lienzo(76, 5)
        L.rect(0, 0, 75, 4, "#D9481E"); L.rect(0, 0, 75, 0, "#F28C28"); L.rect(0, 4, 75, 4, "#8E1B1B")
    elif tipo == "vida_baja":
        L = Lienzo(76, 5)
        L.rect(0, 0, 75, 4, "#8E1B1B"); L.rect(0, 0, 75, 0, "#D9481E"); L.rect(0, 4, 75, 4, "#2B2230")
    else:
        L = Lienzo(76, 4)
        L.rect(0, 0, 75, 3, "#C9A227"); L.rect(0, 0, 75, 0, "#E8D27A"); L.rect(0, 3, 75, 3, "#7A5230")
    return L.img


# ================================================================== diálogo
def caja_dialogo():
    """9-slice de 48x48 (márgenes de 12 px para Panel Sprite de GDevelop)."""
    L = Lienzo(48, 48)
    L.rect(1, 1, 46, 46, "#24222B")
    L.rect(0, 3, 47, 44, "#24222B"); L.rect(3, 0, 44, 47, "#24222B")
    L.rect(2, 2, 45, 3, "#C9A227"); L.rect(2, 44, 45, 45, "#C9A227")
    L.rect(2, 2, 3, 45, "#C9A227"); L.rect(44, 2, 45, 45, "#C9A227")
    L.rect(2, 2, 45, 2, "#E8D27A"); L.rect(2, 2, 2, 45, "#E8D27A")
    L.rect(4, 4, 43, 4, "#3B3846")
    for cx, cy in ((3, 3), (44, 3), (3, 44), (44, 44)):
        L.rect(cx - 2, cy - 2, cx + 2, cy + 2, "#C9A227")
        L.rect(cx - 1, cy - 1, cx + 1, cy + 1, "#8E1B1B")
        L.px(cx, cy, "#F28C28")
    L.contorno()
    return L.img


def marco_retrato():
    L = Lienzo(72, 72)
    L.rect(0, 0, 71, 71, "#C9A227")
    L.rect(0, 0, 71, 0, "#E8D27A"); L.rect(0, 0, 0, 71, "#E8D27A")
    L.rect(71, 0, 71, 71, "#7A5230"); L.rect(0, 71, 71, 71, "#7A5230")
    L.rect(2, 2, 69, 69, "#8E1B1B")
    L.rect(4, 4, 67, 67, "#3B3846")
    for x in range(4, 68, 4):
        for y in range(4, 68, 4):
            if (x + y) % 8 == 0:
                L.px(x, y, "#5A5566")
    return L.img


def placa_nombre():
    L = Lienzo(24, 16)
    L.rect(0, 0, 23, 15, "#C9A227")
    L.rect(0, 0, 23, 0, "#E8D27A")
    L.rect(2, 2, 21, 13, "#8E1B1B")
    L.rect(2, 2, 21, 2, "#D9481E")
    L.rect(0, 15, 23, 15, "#7A5230")
    return L.img


def continuar(f):
    L = Lienzo(8, 8)
    dy = f
    for i, w in enumerate((3, 2, 1, 0)):
        L.rect(3 - w, 2 + i + dy, 4 + w, 2 + i + dy, "#E8D27A" if i < 2 else "#C9A227")
    L.contorno()
    return L.img


# ================================================================== teclas y botones
def tecla(etiqueta, flecha=None):
    t = texto(etiqueta, "#2B2230") if etiqueta else None
    ancho = max(16, (t.width + 8) if t else 16)
    L = Lienzo(ancho, 16)
    L.rect(1, 1, ancho - 2, 14, "#9AA3A8")
    L.rect(1, 1, ancho - 2, 12, "#F4F1E8")
    L.rect(2, 2, ancho - 3, 11, "#C8C8C0")
    L.rect(1, 14, ancho - 2, 14, "#5A5566")
    if t:
        L.img.alpha_composite(t, ((ancho - t.width) // 2, -1)); L.p = L.img.load()
    if flecha:
        cx, cy = ancho // 2, 7
        for i in range(4):
            if flecha == "arriba":
                L.rect(cx - i, cy - 3 + i, cx + i - 1, cy - 3 + i, "#2B2230")
            elif flecha == "abajo":
                L.rect(cx - i, cy + 2 - i, cx + i - 1, cy + 2 - i, "#2B2230")
            elif flecha == "izquierda":
                L.rect(cx - 3 + i, cy - i, cx - 3 + i, cy + i - 1, "#2B2230")
            else:
                L.rect(cx + 2 - i, cy - i, cx + 2 - i, cy + i - 1, "#2B2230")
    L.contorno()
    return L.img


def boton_mando(etiqueta):
    colores = {"A": "#6B8E3D", "B": "#D9481E", "X": "#3A86C8", "Y": "#C9A227"}
    if etiqueta in colores:
        L = Lienzo(16, 16)
        c = colores[etiqueta]
        L.circulo(8, 8, 7.5, OSCURECER[c])
        L.circulo(8, 7.5, 7, c)
        L.circulo(6, 5, 2, "#F4F1E8", r_in=0.6)
        t = texto(etiqueta, "#F4F1E8")
        L.img.alpha_composite(t, ((16 - t.width) // 2 + 1, -1)); L.p = L.img.load()
        L.contorno()
        return L.img
    if etiqueta == "STICK":
        L = Lienzo(16, 16)
        L.circulo(8, 8, 7.5, "#3B3846")
        L.circulo(8, 8, 5, "#5A5566")
        L.circulo(7.5, 7.5, 4, "#9AA3A8")
        L.circulo(6.5, 6.5, 1.5, "#C8C8C0")
        L.contorno()
        return L.img
    t = texto(etiqueta, "#F4F1E8")
    ancho = t.width + 10
    L = Lienzo(ancho, 16)
    L.rect(2, 2, ancho - 3, 13, "#3B3846")
    L.rect(1, 4, ancho - 2, 11, "#3B3846")
    L.rect(2, 2, ancho - 3, 2, "#5A5566")
    L.img.alpha_composite(t, ((ancho - t.width) // 2, -1)); L.p = L.img.load()
    L.contorno()
    return L.img


TECLAS = {
    **{k.lower(): (k, None) for k in "WASDFRTGQEIJKLUOPHN"},
    "num0": ("0", None), "num1": ("1", None), "num4": ("4", None), "num5": ("5", None), "num6": ("6", None),
    "arriba": ("", "arriba"), "abajo": ("", "abajo"), "izquierda": ("", "izquierda"), "derecha": ("", "derecha"),
    "shift": ("SHIFT", None), "espacio": ("ESPACIO", None), "esc": ("ESC", None), "enter": ("ENTER", None),
}
BOTONES = ["A", "B", "X", "Y", "LB", "RB", "START", "STICK"]


# ================================================================== pantallas 640x360
def cielo_atardecer(img, y0=0, y1=360):
    bandas = ["#24222B", "#3B3846", "#8E1B1B", "#D9481E", "#F28C28", "#E8D27A"]
    L = Lienzo.de(img)
    alto = (y1 - y0) / len(bandas)
    for y in range(y0, y1):
        t = (y - y0) / alto
        i = min(int(t), len(bandas) - 1)
        frac = t - i
        c = bandas[i]
        for x in range(640):
            if i + 1 < len(bandas) and frac > 0.6 and ((x + y) % 2 == 0 or frac > 0.85):
                L.px(x, y, bandas[i + 1])
            else:
                L.px(x, y, c)
    return L.img


def silueta_ciudad(img, base=360):
    L = Lienzo.de(img)
    import random
    rnd = random.Random(3)
    x = 0
    while x < 640:
        w = rnd.randrange(40, 90)
        h = rnd.randrange(50, 130)
        top = base - h
        L.rect(x, top, x + w, base, "#24222B")
        # tejado curvo estilo Nación del Fuego
        for i in range(w + 12):
            yy = top - int(10 * math.sin(math.pi * i / (w + 12)) ** 0.5) + 6
            L.rect(x - 6 + i, yy, x - 6 + i, top, "#24222B")
        L.rect(x - 8, top + 5, x - 6, top + 7, "#24222B"); L.rect(x + w + 6, top + 5, x + w + 8, top + 7, "#24222B")
        for wy in range(top + 14, base - 8, 12):
            for wx in range(x + 6, x + w - 6, 10):
                if rnd.random() < 0.45:
                    L.rect(wx, wy, wx + 3, wy + 4, "#E8D27A" if rnd.random() < .7 else "#F28C28")
        x += w + rnd.randrange(8, 20)
    return L.img


def sprite(ruta, escala):
    im = Image.open(os.path.join(A, ruta + ".png")).convert("RGBA")
    return im.resize((im.width * escala, im.height * escala), Image.NEAREST)


def oscurecer(img, veces=1, tramado=False):
    L = Lienzo.de(img)
    for _ in range(veces):
        L.oscurecer(lambda x, y: (not tramado) or (x + y) % 2 == 0)
    return L.img


def marco_panel(img):
    L = Lienzo.de(img)
    for k, c in ((0, "#1A1420"), (1, "#1A1420"), (2, "#1A1420"), (3, "#F4F1E8")):
        L.rect(k, k, 639 - k, k, c); L.rect(k, 359 - k, 639 - k, 359 - k, c)
        L.rect(k, k, k, 359 - k, c); L.rect(639 - k, k, 639 - k, 359 - k, c)
    # franja inferior para el texto de la intro
    L.rect(4, 290, 635, 355, "#24222B")
    L.rect(4, 290, 635, 290, "#F4F1E8")
    return L.img


def pantalla_titulo():
    img = Image.new("RGBA", (640, 360), (0, 0, 0, 255))
    img = cielo_atardecer(img, 0, 300)
    L = Lienzo.de(img)
    L.circulo(320, 210, 70, "#F28C28"); L.circulo(320, 210, 60, "#E8D27A")
    img = silueta_ciudad(L.img, 300)
    L = Lienzo.de(img)
    L.rect(0, 300, 639, 359, "#24222B")
    img = L.img
    # símbolo de los cuatro elementos detrás del título
    for (ic, dx) in (("fuego", -150), ("agua", -50), ("tierra", 50), ("aire", 150)):
        poner(img, ICONOS[ic]().resize((32, 32), Image.NEAREST), 320 + dx - 16, 26)
    poner(img, texto("RYU", "#F28C28", escala=8, contorno="#1A1420", sombra="#8E1B1B"), 320, 66, centrado=True)
    poner(img, texto("El Último Ciclo", "#F4F1E8", escala=2, contorno="#1A1420", sombra="#3B3846"), 320, 150, centrado=True)
    poner(img, sprite("personajes/gao_reposo_abajo_0", 3), 40, 246)
    poner(img, sprite("personajes/ryu_reposo_abajo_0", 4), 110, 218)
    poner(img, sprite("personajes/nerea_reposo_abajo_0", 3), 220, 246)
    poner(img, sprite("personajes/norbu_reposo_abajo_0", 3), 520, 246)
    poner(img, texto("Proyecto académico - inspirado en Avatar", "#9AA3A8"), 320, 344, centrado=True)
    return img


def intro(n):
    if n == 1:
        img = Image.open(os.path.join(RAIZ, "arte_fuente", "previews", "mapa_ciudad_ejemplo.png")).convert("RGBA").crop((0, 0, 640, 360))
        img = oscurecer(img, 1, tramado=True)
        for i, ic in enumerate(("fuego", "agua", "tierra", "aire")):
            poner(img, ICONOS[ic]().resize((64, 64), Image.NEAREST), 96 + i * 128, 110)
    elif n == 2:
        img = Image.open(os.path.join(A, "tilesets", "fondo_pelea_canon.png")).convert("RGBA")
        img = oscurecer(img, 2)
        L = Lienzo.de(img)
        L.rect(220, 30, 419, 229, "#C9A227"); L.rect(224, 34, 415, 225, "#24222B")
        img = L.img
        poner(img, Image.open(os.path.join(UI, "retrato_daichi.png")).convert("RGBA").resize((192, 192), Image.NEAREST), 224, 34)
        poner(img, texto("DAICHI", "#E8D27A", escala=2, contorno="#1A1420"), 320, 240, centrado=True)
    elif n == 3:
        img = Image.new("RGBA", (640, 360), a_rgb("#24222B") + (255,))
        L = Lienzo.de(img)
        L.circulo(320, 120, 90, "#3B3846")
        L.circulo(320, 120, 80, "#E8D27A", r_in=0.85)
        for x, y in ((320, 30), (410, 120), (320, 210), (230, 120)):
            L.circulo(x, y, 8, "#E8D27A")
        for i in range(-70, 71):
            for k in range(-3, 4):
                L.px(320 + i + k, 120 - i, "#D9481E")
        img = L.img
        for i, el in enumerate(("fuego", "agua", "tierra", "aire", "fuego")):
            poner(img, sprite(f"enemigos/soldado_{el}_reposo_abajo_0", 3), 40 + i * 120, 180)
    else:
        img = Image.open(os.path.join(A, "tilesets", "fondo_pelea_plaza.png")).convert("RGBA")
        img = cielo_atardecer(img.copy(), 0, 0) if False else img
        img = oscurecer(img, 1, tramado=True)
        poner(img, sprite("personajes/ryu_reposo_abajo_0", 6), 224, 70)
    return marco_panel(img)


def panel_final():
    img = Image.new("RGBA", (640, 360), (0, 0, 0, 255))
    img = cielo_atardecer(img, 0, 290)
    L = Lienzo.de(img)
    L.circulo(320, 205, 70, "#F28C28"); L.circulo(320, 205, 58, "#E8D27A")
    L.rect(0, 250, 639, 359, "#C8C8C0")
    L.rect(0, 250, 639, 252, "#F4F1E8")
    img = L.img
    for i, (n, e) in enumerate((("tsering", 3), ("gao", 4), ("ryu", 4), ("nerea", 4))):
        poner(img, sprite(f"personajes/{n}_reposo_arriba_0", e), 150 + i * 90, 150 if e == 4 else 182)
    return marco_panel(img)


def pantalla_derrota():
    img = Image.open(os.path.join(A, "tilesets", "fondo_pelea_plaza.png")).convert("RGBA")
    img = oscurecer(img, 3)
    L = Lienzo.de(img)
    L.circulo(320, 140, 70, "#8E1B1B", r_in=0.85)
    for i in range(-55, 56):
        for k in range(-2, 3):
            L.px(320 + i + k, 140 - i, "#D9481E")
    img = L.img
    poner(img, sprite("personajes/ryu_derribado_abajo_0", 3), 272, 150)
    poner(img, texto("DERROTA", "#D9481E", escala=5, contorno="#1A1420", sombra="#2B2230"), 320, 30, centrado=True)
    poner(img, texto("Nadie tiene que cargar el ciclo solo. Inténtalo otra vez.", "#F4F1E8", contorno="#1A1420"), 320, 250, centrado=True)
    return img


def pantalla_controles():
    img = Image.new("RGBA", (640, 360), a_rgb("#24222B") + (255,))
    L = Lienzo.de(img)
    for y in range(0, 360, 4):
        for x in range(0, 640, 4):
            if (x // 4 + y // 4) % 9 == 0:
                L.px(x, y, "#2B2230")
    img = L.img
    poner(img, texto("CONTROLES", "#E8D27A", escala=3, contorno="#1A1420", sombra="#7A5230"), 320, 8, centrado=True)
    acciones = ["Moverse", "Golpe", "Poder 1", "Poder 2", "Poder 3", "Defensa", "Elemento", "Interactuar"]
    teclas = {
        "ryu": [["w", "a", "s", "d"], ["f"], ["r"], ["t"], ["g"], ["shift"], ["q"], ["e"]],
        "gao": [["arriba", "izquierda", "abajo", "derecha"], ["num1"], ["num4"], ["num5"], ["num6"], ["num0"], [], ["enter"]],
        "nerea": [["i", "j", "k", "l"], ["u"], ["o"], ["p"], ["h"], ["espacio"], [], ["n"]],
        "mando": [["STICK"], ["A"], ["X"], ["Y"], ["B"], ["RB"], ["LB"], ["A"]],
    }
    x0 = 8
    for i, a in enumerate(acciones):
        poner(img, texto(a, "#F4F1E8"), x0, 64 + i * 32)
    cols = [("ryu", 120), ("gao", 250), ("nerea", 380), ("mando", 520)]
    for n, cx in cols:
        if n in COLOR_JUGADOR:
            poner(img, mini_retrato(n), cx, 34)
            poner(img, texto(n.upper(), COLOR_JUGADOR[n][1], contorno="#1A1420"), cx + 28, 42)
        else:
            poner(img, texto("MANDO", "#C8C8C0", contorno="#1A1420"), cx, 42)
        for i, ks in enumerate(teclas[n]):
            x = cx
            if not ks:
                poner(img, texto("-", "#5A5566"), x + 4, 64 + i * 32)
                continue
            for k in ks:
                ic = boton_mando(k) if n == "mando" else tecla(*TECLAS[k])
                poner(img, ic, x, 60 + i * 32)
                x += ic.width + 2
    poner(img, texto("Esc / Start: pausa    Solo Ryu cambia de elemento (Q / LB)", "#9AA3A8"), 320, 344, centrado=True)
    return img


# ================================================================== guardar
def guardar(nombre, img):
    assert not fuera_de_paleta(img), (nombre, list(fuera_de_paleta(img))[:5])
    img.save(os.path.join(UI, nombre + ".png"))


if __name__ == "__main__":
    for n, fn in ICONOS.items():
        guardar(f"ui_icono_{n}", fn())
    for n in COLOR_JUGADOR:
        guardar(f"ui_hud_{n}", hud(n))
    for t in ("vida", "vida_baja", "energia"):
        guardar(f"ui_barra_{t}", barra(t))
    guardar("ui_caja_dialogo", caja_dialogo())
    guardar("ui_marco_retrato", marco_retrato())
    guardar("ui_placa_nombre", placa_nombre())
    for f in range(2):
        guardar(f"ui_continuar_{f}", continuar(f))
    for k, (et, fl) in TECLAS.items():
        guardar(f"ui_tecla_{k}", tecla(et, fl))
    for b in BOTONES:
        guardar(f"ui_boton_{b.lower()}", boton_mando(b))
    guardar("pantalla_titulo", pantalla_titulo())
    for n in range(1, 5):
        guardar(f"intro_panel_{n}", intro(n))
    guardar("panel_final", panel_final())
    guardar("pantalla_derrota", pantalla_derrota())
    guardar("pantalla_controles", pantalla_controles())
    print("ok")
