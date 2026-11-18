"""Sprites finales de los jugables (Ryu, Gao, Nerea) en estilo v3.

Cada personaje tiene 3 poses dibujadas a mano (abajo, arriba, derecha) en plantillas ASCII.
Las animaciones se derivan moviendo piezas (brazos, piernas, torso) de esas plantillas.
Uso: python3 herramientas/jugables_v3.py
"""
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from sprites_v3 import filas, render, GAO_ABAJO, GAO_COLORES, RAIZ, OX
from catalogo_ryu import PEINADOS, CARA, CUERPO, COLORES as RYU_COL

W = 20


# ================================================================== plantillas
def _a_dict(lista):
    """Convierte una plantilla de 32 filas de texto en segmentos {fila: [(0, texto)]}."""
    return {y: [(0, f)] for y, f in enumerate(lista)}


# ------------------------------------------------------------------ Ryu
RYU = {
    "abajo": filas({**PEINADOS["3 Flequillo"], **CARA, **CUERPO}),
    "arriba": filas({
        3: [(6, "HHHHHHHH")],
        4: [(4, "HHHHhHHHhHHH")],
        5: [(3, "HHHhHHHHHHhHHH")],
        6: [(3, "HHHHHHHHHHHHHH")],
        7: [(3, "HHHHHhhHHHHHHH")],
        8: [(3, "HHHHHHHHHHHHHH")],
        9: [(3, "HHHHHHHHHHHHHH")],
        10: [(3, "jHHHHHHHHHHHHj")],
        11: [(2, "S"), (3, "jHHHHHHHHHHHHj"), (17, "S")],
        12: [(2, "K"), (3, "jjHHHHHHHHHHjj"), (17, "K")],
        13: [(4, "jHHjHHHHjHHj")],
        14: [(4, "KjSjjSSjjSjK")],
        15: [(5, "KSSSSSSSSK")],
        16: [(5, "KSSSSSSSSK")],
        17: [(6, "KKSSSSKK")],
        18: [(5, "DDDDDDDDDD")],
        19: [(2, "cCCCDDDDDDDDCCCD")],
        20: [(1, "cCDCCCCDDDDCCCCDDD")],
        21: [(1, "cCDCCCCCDDCCCCCDDD")],
        22: [(1, "cCDCCCCCCCCCCCCDDD")],
        23: [(1, "TTDCCCCCCCCCCCCDTT")],
        24: [(1, "SSTTTTTTTTTTTTTTKK")],
        **{k: v for k, v in CUERPO.items() if k >= 25},
    }),
    "derecha": filas({
        3: [(6, "HHHHHHH")],
        4: [(4, "HHHHhHHHhHH")],
        5: [(3, "HHHhHHHHHHhHH")],
        6: [(3, "HHHHHHHHHHHHHH")],
        7: [(3, "HHHHHHHHHHHHHH")],
        8: [(3, "HHHHHHHHjHHHHH")],
        9: [(3, "jHHHHHHjSHHSHj")],
        10: [(3, "jHHHHHjSSSHSSS")],
        11: [(3, "jHHHHjSSSSEEES")],
        12: [(3, "jHHHSSSSSSSSSS")],
        13: [(3, "jHHHSKSSSSEESS")],
        14: [(3, "jHHHSKSSSSIESS")],
        15: [(3, "jHHKSSSSSSSSSSS")],
        16: [(4, "jKSSSSSSSMMS")],
        17: [(5, "KKSSSSSSSSK")],
        18: [(7, "KKKKKK")],
        19: [(5, "cCCCCCCCTB")],
        20: [(5, "cCCcCDCCTB")],
        21: [(5, "cCCcCDCCTB")],
        22: [(5, "cCCcCDCCTB")],
        23: [(5, "cCCTTTCCTB")],
        24: [(5, "TTTSSSTTTT")],
        25: [(6, "PPPPPPPP")],
        26: [(7, "pPPPPQ")],
        27: [(8, "pPPQ")],
        28: [(8, "zZZZZ")],
        29: [(8, "ZZZZZ")],
        30: [(8, "XXXXX")],
    }),
}

# ------------------------------------------------------------------ Gao
GAO = {
    "abajo": GAO_ABAJO,
    "arriba": filas({
        2: [(10, "hH")],
        3: [(7, "HHHhHH")],
        4: [(5, "HHHHHhhHHH")],
        5: [(4, "HHHHHHHhhHHH")],
        6: [(3, "HHHHHHHHHHhhHH")],
        7: [(3, "HHHHHHHHHHHHHH")],
        8: [(3, "HHHHHHHHHHHHHH")],
        9: [(3, "HHHHHHHHHHHHHH")],
        10: [(3, "jHHHHHHHHHHHHj")],
        11: [(2, "S"), (3, "jHHHHHHHHHHHHj"), (17, "S")],
        12: [(2, "K"), (3, "jHHHHHHHHHHHHj"), (17, "K")],
        13: [(3, "jjHHHHHHHHHHjj")],
        14: [(4, "jjjjjjjjjjjj")],
        15: [(5, "KSSSSSSSSK")],
        16: [(5, "KSSSSSSSSK")],
        17: [(5, "KKSSSSSSKK")],
        18: [(5, "KKKKKKKKKK")],
        19: [(1, "bBBCCCCCCCCCCCCBBV")],
        20: [(1, "bBVcCCCCCCCCCCDBBV")],
        21: [(1, "bBVcCCCCCCCCCCDBBV")],
        22: [(1, "LLLcCCCCCCCCCCDLLL")],
        23: [(1, "LLLRRRRRRRRRRRRLLL")],
        24: [(1, "SSSPPPPPPPPPPPPKKK")],
        **{y: [(0, GAO_ABAJO[y])] for y in range(25, 32)},
    }),
    "derecha": filas({
        2: [(11, "hH")],
        3: [(7, "HHHHhHH")],
        4: [(5, "HHHHHHhhHH")],
        5: [(4, "HHHHHHHHhhHH")],
        6: [(3, "HHHHHHHHHHHhHH")],
        7: [(3, "HHHHHHHHHHHHHH")],
        8: [(3, "jHHHHHHHHHHHHH")],
        9: [(3, "jHHHHHHjSHHSHj")],
        10: [(3, "jjHHHHjSSSHSSS")],
        11: [(3, "jjHHHjSSSSEEES")],
        12: [(3, "jjHHSSSSSSSSSS")],
        13: [(3, "jjHSKSSSSSEESS")],
        14: [(3, "jjHSKSSSSSIESS")],
        15: [(4, "KSSSSSSSSSSSSS")],
        16: [(4, "KSSSSSSSSMMMS")],
        17: [(5, "KKSSSSSSSSKK")],
        18: [(7, "KKKKKK")],
        19: [(4, "CCCCCCCCCCBB")],
        20: [(4, "cCCCbBVCCCBB")],
        21: [(4, "cCCCbBVCCCBB")],
        22: [(4, "cCCCLLLCCCBB")],
        23: [(4, "RRRRLLLRRRRR")],
        24: [(4, "PPPPSSSPPPPP")],
        25: [(5, "PPPPPPPPPP")],
        26: [(6, "pPPPPPQ")],
        27: [(7, "pPPPQ")],
        28: [(7, "ZZZZZZ")],
        29: [(7, "zZZZZZ")],
        30: [(7, "XXXXXX")],
    }),
}

# ------------------------------------------------------------------ Nerea
# U = rubor, Y = puños blancos (roles únicos para que las animaciones no dependan de la fila)
_NEREA_COLA = {4: (16, "HhH"), 5: (16, "HhHj"), 6: (16, "HhHj"), 7: (16, "HhHj"), 8: (16, "HhHj"),
               9: (16, "HhHj"), 10: (16, "HhHj"), 11: (16, "HhH"), 12: (16, "HhH"), 13: (16, "HhH"),
               14: (16, "HhH"), 15: (16, "HhH"), 16: (16, "Hhj"), 17: (17, "hj"), 18: (17, "Hj"),
               19: (17, "Hj"), 20: (17, "j")}
_NEREA_FRENTE = {
    1: [(12, "HHh")],
    2: [(11, "HHhHH")],
    3: [(6, "HHHHXx"), (12, "HhHHj")],
    4: [(5, "HHHHHHHHHHH")],
    5: [(4, "HHHHHHHHHHHH")],
    6: [(3, "HHhhhhHHHHHHH")],
    7: [(3, "HHHHHhhhhHHHH")],
    8: [(3, "HHHHHHjjHHHHH")],
    9: [(3, "HHHHHHSSHHHHH")],
    10: [(3, "HHHHHSSSSHHHH")],
    11: [(3, "HHHHSSSSSSHHH")],
    12: [(3, "HHEEESSSSEEEH")],
    13: [(3, "HHSIESSSSEISH")],
    14: [(3, "HHSUSSSKSSUSH")],
    15: [(3, "HHKSSSMMSSSKH")],
    16: [(3, "HH"), (6, "KSSSSSSK"), (15, "H")],
    17: [(3, "H"), (7, "KKKKKK")],
    18: [(3, "ccCCCBBBBCCCDD")],
    19: [(3, "cDCCCBBBBCCCDD")],
    20: [(3, "cDCCCBVBBCCCDD")],
    21: [(3, "cDTTTTTTTTTTDD")],
    22: [(3, "YYCCCCtTCCCCYY")],
    23: [(3, "SSCCCCTtCCCCKK")],
    24: [(4, "PPPPPTtPPPPP")],
    25: [(6, "pPP"), (11, "pPQ")],
    26: [(6, "pPP"), (11, "pPQ")],
    27: [(6, "zZZ"), (11, "ZZZ")],
    28: [(6, "zZZ"), (11, "ZZZ")],
    29: [(5, "VVVV"), (11, "VVVV")],
}
for _y, _seg in _NEREA_COLA.items():
    _NEREA_FRENTE.setdefault(_y, []).append(_seg)

NEREA = {
    "abajo": filas(_NEREA_FRENTE),
    "arriba": filas({
        3: [(6, "HHHHHHHH")],
        4: [(5, "HHHHhHHHHH")],
        5: [(4, "HHHhhHHHHHHH")],
        6: [(3, "HHHHHHXXHHHHHH")],
        7: [(3, "HHHHHhHHhHHHHH")],
        8: [(3, "HHHHHHHHHHHHHH")],
        9: [(3, "HHHHHHhHHHHHHH")],
        10: [(3, "HHHHHHHHHHHHHH")],
        11: [(3, "HHHHHHhHHHHHHH")],
        12: [(3, "HHHHHHHHHHHHHH")],
        13: [(3, "jHHHHHhHHHHHHj")],
        14: [(3, "jHHHHHHHHHHHHj")],
        15: [(4, "jHHHHhHHHHHj")],
        16: [(5, "KSSHhHHSSK")],
        17: [(6, "KKHhHHKK")],
        18: [(3, "ccCCCHhHHCCCDD")],
        19: [(3, "cDCCCHhHHCCCDD")],
        20: [(3, "cDCCCjHhHCCCDD")],
        21: [(3, "cDTTTTjhjTTTDD")],
        22: [(3, "YYCCCCCCCCCCYY")],
        23: [(3, "SSCCCCCCCCCCKK")],
        24: [(4, "PPPPPPPPPPPP")],
        **{y: _NEREA_FRENTE[y] for y in range(25, 30)},
    }),
    "derecha": filas({
        2: [(7, "HHHH")],
        3: [(5, "HHXXHHHHH")],
        4: [(3, "HHHHHhhHHHHH")],
        5: [(2, "HHHHHHHHhhHHHH")],
        6: [(2, "HhHHHHHHHHHHHHH")],
        7: [(2, "HhHHHHHHHHHHHHH")],
        8: [(2, "HhH"), (5, "HHHHHHHHHHHH")],
        9: [(2, "HhH"), (5, "HHHHHHHHHjSS")],
        10: [(2, "HhH"), (5, "HHHHHHHHjSSS")],
        11: [(2, "HhH"), (5, "HHHHHHSSSSSS")],
        12: [(2, "Hh"), (5, "HHHHSSSSSEES")],
        13: [(2, "Hh"), (5, "HHHSKSSSSIES")],
        14: [(3, "Hh"), (5, "HHHSKSSSSSUSS")],
        15: [(3, "Hj"), (5, "HHKSSSSSSSMS")],
        16: [(4, "H"), (5, "HHKSSSSSSK")],
        17: [(4, "j"), (7, "KKKK")],
        18: [(5, "cCCCCCCBB")],
        19: [(5, "cCCcDCCBB")],
        20: [(5, "cCCcDCCBV")],
        21: [(5, "TTTcDTTTT")],
        22: [(5, "CCCYYCCCt")],
        23: [(5, "CCCSSCCCT")],
        24: [(6, "PPPPPPP")],
        25: [(7, "pPPQ")],
        26: [(7, "pPPQ")],
        27: [(7, "zZZZ")],
        28: [(7, "zZZZZ")],
        29: [(7, "VVVVV")],
    }),
}
NEREA_COL = {
    "H": "#4A3B32", "h": "#7A5230", "j": "#2B2230",
    "x": "#8FD3F0", "X": "#3A86C8",
    "S": "#F2C9A0", "s": "#F2C9A0", "K": "#D9A06B", "U": "#D9A06B",
    "E": "#2B2230", "I": "#3A86C8", "W": "#F4F1E8", "M": "#A86B3C",
    "C": "#3A86C8", "c": "#8FD3F0", "D": "#1E4F8C",
    "B": "#F2F7FA", "V": "#8FD3F0", "Y": "#F2F7FA",
    "T": "#8FD3F0", "t": "#F2F7FA",
    "P": "#2B2230", "p": "#3B3846", "Q": "#24222B",
    "Z": "#F2F7FA", "z": "#F2F7FA",
}

# ------------------------------------------------------------------ metadatos para animar
# brazos: columnas (x0, x1) y filas (y0, y1) dentro de la ventana; piernas: primera fila.
JUGABLES = {
    "ryu": dict(poses=RYU, colores=RYU_COL, manga="C", mano="S",
                brazos={"abajo": ((1, 2), (17, 18), (20, 24)), "arriba": ((1, 2), (17, 18), (20, 24)),
                        "derecha": ((8, 10), None, (20, 24))},
                piernas={"abajo": 26, "arriba": 26, "derecha": 26}),
    "gao": dict(poses=GAO, colores=GAO_COLORES, manga="B", mano="S",
                brazos={"abajo": ((1, 3), (16, 18), (20, 24)), "arriba": ((1, 3), (16, 18), (20, 24)),
                        "derecha": ((8, 10), None, (20, 24))},
                piernas={"abajo": 26, "arriba": 26, "derecha": 26}),
    "nerea": dict(poses=NEREA, colores=NEREA_COL, manga="C", mano="S",
                  brazos={"abajo": ((3, 4), (15, 16), (19, 23)), "arriba": ((3, 4), (15, 16), (19, 23)),
                          "derecha": ((8, 9), None, (19, 23))},
                  piernas={"abajo": 25, "arriba": 25, "derecha": 25}),
}


# ================================================================== operaciones sobre la rejilla
def rejilla(pose):
    return [list(f) for f in pose]


def texto(g):
    return ["".join(f) for f in g]


def bloque(g, x0, x1, y0, y1):
    """Extrae un bloque y lo borra de la rejilla. Devuelve [(x, y, ch)]."""
    out = []
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if g[y][x] != ".":
                out.append((x, y, g[y][x]))
                g[y][x] = "."
    return out


def pegar(g, pix, dx=0, dy=0, mapa=None, solo_vacio=False):
    for x, y, ch in pix:
        nx, ny = x + dx, y + dy
        if 0 <= nx < W and 0 <= ny < 32:
            if solo_vacio and g[ny][nx] != ".":
                continue
            g[ny][nx] = mapa.get(ch, ch) if mapa else ch


def rect(g, x0, y0, x1, y1, ch):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if 0 <= x < W and 0 <= y < 32:
                g[y][x] = ch


def subir_torso(g, desde):
    """Baja 1 px todo lo que está por encima de la fila `desde` (respiración / paso)."""
    for y in range(desde - 1, 0, -1):
        g[y] = list(g[y - 1]) if y - 1 >= 0 else ["."] * W
    g[0] = ["."] * W


def piernas(g, desde, centro=10):
    izq = [(x, y, g[y][x]) for y in range(desde, 32) for x in range(0, centro) if g[y][x] != "."]
    der = [(x, y, g[y][x]) for y in range(desde, 32) for x in range(centro, W) if g[y][x] != "."]
    return izq, der


def cerrar_ojos(g, mapa=None):
    mapa = mapa or {"I": "S", "W": "S", "M": "E"}
    for y in range(6, 18):
        for x in range(W):
            if g[y][x] in mapa:
                g[y][x] = mapa[g[y][x]]


# ================================================================== animaciones
LEJOS = {c: "Q" for c in "PpQZzXVY"}


def cuadro(nombre, d, anim, f):
    cfg = JUGABLES[nombre]
    g = rejilla(cfg["poses"][d])
    bi, bd, (by0, by1) = cfg["brazos"][d]
    pierna_y = cfg["piernas"][d]
    manga, mano = cfg["manga"], cfg["mano"]

    if anim == "reposo":
        if f == 1:
            subir_torso(g, pierna_y - 1)

    elif anim == "caminar":
        if d in ("abajo", "arriba"):
            izq, der = piernas(g, pierna_y)
            for x, y, _ in izq + der:
                g[y][x] = "."
            li = (-1, 0, 0, 0)[f]
            ld = (0, 0, -1, 0)[f]
            pegar(g, izq, dy=li)
            pegar(g, der, dy=ld)
            # balanceo de brazos opuesto a las piernas
            a = bloque(g, bi[0], bi[1], by0, by1)
            b = bloque(g, bd[0], bd[1], by0, by1)
            pegar(g, a, dy=(1, 0, -1, 0)[f])
            pegar(g, b, dy=(-1, 0, 1, 0)[f])
            if f in (1, 3):
                subir_torso(g, pierna_y - 1)
        else:
            pier = [(x, y, g[y][x]) for y in range(pierna_y, 32) for x in range(W) if g[y][x] != "."]
            if f in (0, 2):
                for x, y, _ in pier:
                    g[y][x] = "."
                s = 2 if f == 0 else -2
                pegar(g, pier, dx=-s, mapa=LEJOS)      # pierna de atrás (oscura)
                pegar(g, pier, dx=s)                   # pierna de adelante
            a = bloque(g, bi[0], bi[1], by0, by1)
            pegar(g, a, dx=(-1, 0, 1, 0)[f])
            if f in (1, 3):
                subir_torso(g, pierna_y - 1)

    elif anim == "golpe":
        if d == "abajo":
            b = bloque(g, bd[0], bd[1], by0, by1)
            dy = (-4, 2, 0)[f]
            pegar(g, b, dy=dy)
            if f == 1:
                rect(g, bd[0], by1 + 2, bd[1] + 1, by1 + 3, mano)
        elif d == "arriba":
            b = bloque(g, bd[0], bd[1], by0, by1)
            pegar(g, b, dy=(1, -7, -3)[f])
            if f == 1:
                rect(g, bd[0], by0 - 9, bd[1] + 1, by0 - 8, mano)
        else:
            bloque(g, bi[0], bi[1], by0, by1)
            x0 = bi[0]
            largo = (2, 7, 4)[f]
            if f == 0:
                rect(g, x0 - 2, by0 + 1, x0 + 1, by0 + 2, manga)
                rect(g, x0 - 3, by0 + 1, x0 - 3, by0 + 2, mano)
            else:
                rect(g, x0 + 1, by0 + 1, x0 + largo, by0 + 2, manga)
                rect(g, x0 + largo + 1, by0, x0 + largo + 2, by0 + 2, mano)

    elif anim == "poder":
        if d == "abajo":
            a = bloque(g, bi[0], bi[1], by0, by1)
            b = bloque(g, bd[0], bd[1], by0, by1)
            if f == 0:
                pegar(g, a, dy=-2)
                pegar(g, b, dy=-2)
            else:
                pegar(g, a, dx=2, dy=1)
                pegar(g, b, dx=-2, dy=1)
                rect(g, 8, by1 + 2, 11, by1 + 3, mano)
        elif d == "arriba":
            a = bloque(g, bi[0], bi[1], by0, by1)
            b = bloque(g, bd[0], bd[1], by0, by1)
            pegar(g, a, dy=(-5, -7)[f])
            pegar(g, b, dy=(-5, -7)[f])
        else:
            bloque(g, bi[0], bi[1], by0, by1)
            x0 = bi[0]
            largo = (5, 7)[f]
            rect(g, x0 + 1, by0, x0 + largo, by0 + 2, manga)
            rect(g, x0 + largo + 1, by0 - 1, x0 + largo + 3, by0 + 2, mano)

    elif anim == "defensa":
        if d in ("abajo", "arriba"):
            a = bloque(g, bi[0], bi[1], by0, by1)
            b = bloque(g, bd[0], bd[1], by0, by1)
            pegar(g, a, dy=-1)
            pegar(g, b, dy=-1)
            if d == "abajo":
                rect(g, bi[1] + 1, by0, bd[0] - 1, by0 + 2, manga)
                rect(g, bi[1] + 1, by0, bi[1] + 2, by0 + 1, mano)
                rect(g, bd[0] - 2, by0, bd[0] - 1, by0 + 1, mano)
        else:
            bloque(g, bi[0], bi[1], by0, by1)
            x0 = bi[0] + 4
            rect(g, x0, by0 - 3, x0 + 2, by0 + 3, manga)
            rect(g, x0, by0 - 5, x0 + 2, by0 - 4, mano)

    elif anim == "danio":
        a = bloque(g, bi[0], bi[1], by0, by1)
        b = bloque(g, bd[0], bd[1], by0, by1)
        pegar(g, a, dx=-1, dy=-2)
        pegar(g, b, dx=1, dy=-2)
        cerrar_ojos(g, cfg.get("ojos_cerrados"))

    return render(texto(g), cfg["colores"])


def derribado(nombre):
    base = cuadro(nombre, "abajo", "danio", 0)
    rot = base.rotate(90, expand=False)
    out = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    bbox = rot.getbbox()
    pieza = rot.crop(bbox)
    out.alpha_composite(pieza, ((32 - pieza.width) // 2, 31 - pieza.height))
    return out


ANIMS = [
    ("reposo", 2, ("abajo", "arriba", "derecha")),
    ("caminar", 4, ("abajo", "arriba", "derecha")),
    ("golpe", 3, ("abajo", "arriba", "derecha")),
    ("poder", 2, ("abajo", "arriba", "derecha")),
    ("defensa", 1, ("abajo", "arriba", "derecha")),
    ("danio", 1, ("abajo",)),
    ("derribado", 1, ("abajo",)),
]


def generar(nombre, guardar=True):
    salida = os.path.join(RAIZ, "juego", "assets", "personajes")
    res = {}
    for anim, n, dirs in ANIMS:
        for d in dirs:
            for f in range(n):
                img = derribado(nombre) if anim == "derribado" else cuadro(nombre, d, anim, f)
                res[(anim, d, f)] = img
                if guardar:
                    img.save(os.path.join(salida, f"{nombre}_{anim}_{d}_{f}.png"))
    return res


def hoja(nombres, escala=4):
    celda = 32 * escala
    filas_ = [(a, d) for a, n, ds in ANIMS for d in ds]
    out = Image.new("RGBA", (len(nombres) * (4 * celda + 16) + 16, len(filas_) * celda + 16), (58, 54, 70, 255))
    for ci, n in enumerate(nombres):
        res = generar(n, guardar=False)
        ox = 16 + ci * (4 * celda + 16)
        for ri, (a, d) in enumerate(filas_):
            k = 0
            while (a, d, k) in res:
                out.alpha_composite(res[(a, d, k)].resize((celda, celda), Image.NEAREST), (ox + k * celda, 8 + ri * celda))
                k += 1
    return out


if __name__ == "__main__":
    nombres = ["ryu", "gao", "nerea"]
    for n in nombres:
        print(n, len(generar(n)), "cuadros")
    hoja(nombres).save(os.path.join(RAIZ, "arte_fuente", "previews", "v3_jugables_hoja.png"))
    # vistas base en grande
    E = 8
    out = Image.new("RGBA", (9 * (32 * E + 8) + 8, 32 * E + 16), (58, 54, 70, 255))
    i = 0
    for n in nombres:
        for d in ("abajo", "derecha", "arriba"):
            out.alpha_composite(cuadro(n, d, "reposo", 0).resize((32 * E, 32 * E), Image.NEAREST), (8 + i * (32 * E + 8), 8))
            i += 1
    out.save(os.path.join(RAIZ, "arte_fuente", "previews", "v3_jugables_vistas.png"))
