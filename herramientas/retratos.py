"""Retratos de diálogo 64x64 (busto a tres cuartos mirando a la derecha).

Formas rellenas con máscaras (numpy) y sombreado plano de 3 tonos con luz arriba-izquierda.
Uso: python3 herramientas/retratos.py [ryu gao nerea tsering norbu daichi]
"""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from paleta import CONTORNO, a_rgb, fuera_de_paleta
import personajes as P

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
N = 64
OSC = "#2B2230"
BLANCO = "#F4F1E8"


# ---------------------------------------------------------------- máscaras
def _m(fn):
    img = Image.new("L", (N, N), 0)
    fn(ImageDraw.Draw(img))
    return np.array(img) > 0


def elipse(cx, cy, rx, ry):
    return _m(lambda d: d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255))


def poli(pts):
    return _m(lambda d: d.polygon(pts, fill=255))


def rect(x0, y0, x1, y1):
    return _m(lambda d: d.rectangle([x0, y0, x1, y1], fill=255))


def linea(pts, ancho=1):
    return _m(lambda d: d.line(pts, fill=255, width=ancho))


def desplazar(m, dx, dy):
    out = np.zeros_like(m)
    ys, xs = np.nonzero(m)
    ys2, xs2 = ys + dy, xs + dx
    ok = (ys2 >= 0) & (ys2 < N) & (xs2 >= 0) & (xs2 < N)
    out[ys2[ok], xs2[ok]] = True
    return out


class Retrato:
    def __init__(self):
        self.c = np.full((N, N), None, dtype=object)

    def color(self, m, c):
        self.c[m] = c

    def pintar(self, m, tri, banda=2):
        """Relleno con luz (arriba-izq.) y sombra (abajo-der.)."""
        base, luz, sombra = tri
        self.c[m] = base
        sh = m & ~desplazar(m, -banda, -banda)
        li = m & ~desplazar(m, banda, banda)
        self.c[sh] = sombra
        self.c[li & ~sh] = luz

    def borde_interno(self, m, color, sobre):
        """Línea de 1 px por el borde de `m` donde cae sobre `sobre`."""
        borde = m & ~(desplazar(m, 1, 0) & desplazar(m, -1, 0) & desplazar(m, 0, 1) & desplazar(m, 0, -1))
        self.c[borde & sobre] = color

    def px(self, x, y, c):
        if 0 <= x < N and 0 <= y < N:
            self.c[y, x] = c

    def plantilla(self, filas, ox, oy, roles):
        for j, f in enumerate(filas):
            for i, ch in enumerate(f):
                if ch in roles:
                    self.px(ox + i, oy + j, roles[ch])

    def imagen(self):
        img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        px = img.load()
        lleno = np.zeros((N, N), bool)
        for y in range(N):
            for x in range(N):
                if self.c[y, x] is not None:
                    px[x, y] = a_rgb(self.c[y, x]) + (255,)
                    lleno[y, x] = True
        borde = ~lleno & (desplazar(lleno, 1, 0) | desplazar(lleno, -1, 0) | desplazar(lleno, 0, 1) | desplazar(lleno, 0, -1))
        for y, x in zip(*np.nonzero(borde)):
            px[x, y] = a_rgb(CONTORNO) + (255,)
        return img


# ---------------------------------------------------------------- rostro
OJO_CERCA = [
    ".KKKKK.",
    ".WIHIW.",
    ".WIPIW.",
    "..kkk..",
]
OJO_LEJOS = [
    ".KKKK.",
    ".WIHI.",
    ".WIPI.",
    "..kk..",
]
OJO_CERRADO = [
    ".......",
    ".KKKKK.",
    "..kkk..",
    ".......",
]


def cara_mask(forma=None):
    if forma == "cuadrada":
        return elipse(30, 24, 13, 13) | poli([(17, 26), (43, 26), (43, 37), (38, 44), (23, 44), (18, 37)])
    return elipse(30, 25, 13, 14) | poli([(17, 27), (43, 27), (40, 38), (34, 44), (27, 44), (21, 38)])


def rostro(R, d):
    """Pinta cabeza base (cuello, cara, oreja, nariz, ojos, cejas, boca)."""
    piel = d["piel"]
    cuello = rect(25, 36, 36, 50)
    R.pintar(cuello, (piel[2], piel[2], piel[2]), 1)
    cara = cara_mask(d.get("cara"))
    R.pintar(cara, piel, 3)
    # oreja trasera
    R.pintar(elipse(17, 29, 3, 4), piel, 1)
    R.px(17, 29, piel[2]); R.px(17, 30, piel[2])
    # nariz: volumen que sobresale a la derecha
    R.pintar(elipse(37, 32, 3, 3), piel, 1)
    R.px(36, 35, piel[2]); R.px(37, 35, piel[2]); R.px(38, 34, piel[2])
    # ojos
    roles = {"K": OSC, "W": BLANCO, "I": d["iris"], "H": BLANCO, "P": OSC, "k": piel[2]}
    if d.get("ojos_cerrados"):
        R.plantilla(OJO_CERRADO, 23, 26, roles); R.plantilla(OJO_CERRADO, 34, 26, roles)
    else:
        R.plantilla(OJO_CERCA, 23, 26, roles)
        R.plantilla(OJO_LEJOS, 35, 26, roles)
        if d.get("pestanas"):
            for x, y in ((23, 26), (22, 25), (40, 26), (41, 25)):
                R.px(x, y, OSC)
    # cejas
    cj = d["ceja"]
    for (x0, y0, x1, y1) in d["cejas"]:
        R.color(linea([(x0, y0), (x1, y1)], d.get("ceja_grosor", 1)), cj)
    # ojeras / arrugas
    for (x, y) in d.get("sombras", []):
        R.px(x, y, piel[2])
    # boca
    boca = d.get("boca", "neutral")
    if boca == "sonrisa":
        R.color(linea([(29, 38), (31, 40), (36, 40), (38, 38)]), OSC)
        R.color(rect(31, 39, 36, 39), BLANCO)
        R.color(linea([(30, 38), (30, 38)]), OSC)
    elif boca == "leve":
        R.color(linea([(30, 39), (35, 39)]), d["piel"][2])
        R.px(36, 38, d["piel"][2])
    elif boca == "firme":
        R.color(linea([(30, 39), (37, 39)]), OSC)
        R.px(38, 38, piel[2])
    else:
        R.color(linea([(30, 39), (37, 39)]), piel[2])
        R.px(31, 40, piel[2])
    # mejilla
    R.px(24, 35, piel[1]); R.px(25, 35, piel[1])
    return cara


# ---------------------------------------------------------------- peinados
def _techo(extra=None):
    return elipse(30, 22, 16, 15) if extra is None else elipse(30, 22, 16, 15) | extra


def pelo_puntas(R, d, cara):
    t = d["pelo"]
    flequillo = poli([(12, 4), (48, 4), (48, 20), (44, 20), (42, 25), (40, 20), (36, 20), (32, 20),
                      (31, 27), (30, 20), (26, 20), (22, 25), (20, 20), (12, 20)])
    m = (flequillo & elipse(30, 22, 16, 17))
    m |= rect(14, 20, 19, 31) | rect(41, 20, 45, 28)
    pinchos = poli([(16, 14), (18, 3), (25, 11)]) | poli([(24, 10), (30, 0), (36, 10)]) | poli([(35, 11), (42, 3), (45, 15)]) | poli([(13, 17), (9, 11), (16, 11)])
    R.pintar(m | pinchos, t, 3)
    R.borde_interno(m, t[2], cara)


def pelo_corto(R, d, cara):
    t = d["pelo"]
    m = poli([(13, 6), (47, 6), (47, 27), (43, 27), (41, 22), (33, 21), (27, 22), (22, 25), (19, 29), (13, 29)]) & elipse(30, 22, 16, 17)
    m |= rect(14, 20, 19, 31) | rect(41, 20, 45, 27)
    R.pintar(m, t, 3)
    R.borde_interno(m, t[2], cara)
    R.px(24, 14, t[1]); R.px(26, 13, t[1]); R.px(28, 13, t[1])


def pelo_trenza(R, d, cara):
    t = d["pelo"]
    atras = poli([(11, 22), (18, 12), (22, 12), (22, 44), (16, 52), (9, 42)])
    R.pintar(atras, t, 2)
    m = poli([(13, 7), (47, 7), (47, 26), (43, 26), (40, 21), (31, 20), (25, 21), (21, 24), (18, 29), (13, 29)]) & elipse(30, 22, 16, 17)
    m |= rect(14, 20, 18, 34) | poli([(41, 20), (47, 22), (48, 36), (43, 36)])
    R.pintar(m, t, 3)
    R.borde_interno(m, t[2], cara)
    R.px(25, 12, t[1]); R.px(28, 11, t[1]); R.px(32, 12, t[1])
    # trenza sobre el hombro derecho
    for i, (x, y) in enumerate([(44, 38), (45, 42), (44, 46), (45, 50), (44, 54), (45, 58)]):
        R.pintar(elipse(x, y, 3, 3), t, 1)
    R.color(rect(43, 59, 46, 60), d["lazo"])


def pelo_calvo(R, d, cara):
    # brillo en el cráneo
    R.px(24, 12, d["piel"][1]); R.px(25, 11, d["piel"][1]); R.px(26, 11, d["piel"][1])


def pelo_daichi(R, d, cara):
    t = d["pelo"]
    R.pintar(elipse(31, 6, 5, 4), t, 1)  # moño
    R.color(rect(27, 9, 36, 10), d["lazo"])
    m = poli([(13, 8), (47, 8), (47, 26), (42, 26), (40, 20), (33, 18), (26, 20), (20, 24), (16, 28), (13, 28)]) & elipse(30, 22, 16, 16)
    m |= rect(14, 20, 18, 30) | rect(42, 20, 45, 26)
    R.pintar(m, t, 3)
    R.borde_interno(m, t[2], cara)


# ---------------------------------------------------------------- ropa
def torso(R, tri, d=None):
    m = poli([(6, 64), (9, 53), (17, 47), (25, 44), (37, 44), (45, 47), (53, 53), (57, 64)])
    R.pintar(m, tri, 3)
    return m


def ropa_ryu(R, d):
    torso(R, P.ROJO)
    R.pintar(poli([(18, 47), (25, 43), (37, 43), (44, 47), (41, 54), (23, 54)]), P.ROJO_OSC, 2)   # capucha enrollada
    R.pintar(poli([(25, 44), (36, 44), (34, 64), (27, 64)]), P.NEGRO, 1)    # camiseta
    R.color(rect(30, 47, 31, 63), "#C9A227")                                 # cierre
    R.color(rect(9, 60, 20, 63), "#C9A227"); R.color(rect(45, 60, 56, 63), "#C9A227")  # ribete
    R.px(30, 47, "#E8D27A")


def ropa_gao(R, d):
    torso(R, ("#6B8E3D", "#C29A5B", "#3F5A2A"))
    R.pintar(poli([(10, 64), (12, 53), (20, 47), (25, 44), (27, 64)]), P.VERDE_OSC, 2)   # chaleco izq.
    R.pintar(poli([(36, 44), (45, 47), (51, 53), (54, 64), (35, 64)]), P.VERDE_OSC, 2)   # chaleco der.
    R.color(linea([(20, 47), (40, 64)], 2), "#7A5230")                                  # correa
    R.color(rect(38, 58, 40, 60), "#C29A5B")
    R.pintar(poli([(25, 44), (36, 44), (33, 52), (28, 52)]), ("#C29A5B", "#C29A5B", "#7A5230"), 1)  # cuello camiseta


def ropa_nerea(R, d):
    torso(R, P.AZUL)
    R.pintar(poli([(24, 40), (37, 40), (39, 52), (22, 52)]), P.CELESTE, 2)               # bufanda
    R.color(rect(23, 46, 38, 47), P.CELESTE[2])
    R.pintar(poli([(34, 48), (40, 48), (41, 60), (35, 58)]), P.CELESTE, 1)               # cola de la bufanda
    R.color(rect(29, 52, 32, 63), "#F2F7FA")                                             # cierre/camisa
    R.color(rect(9, 60, 20, 63), "#F2F7FA")


def ropa_tsering(R, d):
    torso(R, P.BLANCO)
    R.pintar(poli([(24, 44), (37, 44), (40, 56), (21, 56)]), P.AMARILLO, 2)              # cuello amarillo
    R.pintar(poli([(15, 49), (22, 46), (30, 64), (17, 64)]), P.GRIS_AZUL, 2)             # bufanda gris
    R.color(rect(9, 60, 20, 63), "#E8D27A")


def ropa_norbu(R, d):
    torso(R, P.CICLO_OSC)
    R.pintar(poli([(18, 44), (26, 36), (37, 36), (44, 44), (40, 52), (23, 52)]), P.CICLO, 2)  # cuello alto
    R.pintar(poli([(26, 44), (36, 44), (33, 64), (28, 64)]), P.BLANCO, 1)                     # camisa clara
    R.color(linea([(18, 50), (45, 64)], 3), "#E8D27A")                                        # faja
    # símbolo: círculo roto con cuatro marcas
    for (x, y) in [(41, 54), (42, 53), (43, 53), (44, 54), (44, 55), (44, 56), (43, 57), (42, 57), (41, 56)]:
        R.px(x, y, "#E8D27A")
    R.color(linea([(40, 58), (45, 52)]), P.CICLO_OSC[2])


def ropa_daichi(R, d):
    torso(R, P.VERDE_OSC)
    R.pintar(poli([(24, 44), (37, 44), (40, 56), (21, 56)]), ("#7A5230", "#C29A5B", "#4A3B32"), 2)
    R.color(rect(9, 60, 20, 63), "#C29A5B")
    # emblema de tierra
    R.pintar(elipse(30, 58, 4, 4), ("#C29A5B", "#E8D27A", "#7A5230"), 1)
    R.color(rect(29, 56, 31, 60), "#3F5A2A"); R.color(rect(28, 58, 32, 58), "#3F5A2A")


# ---------------------------------------------------------------- personajes
RETRATOS = {
    "ryu": dict(
        piel=P.PIEL_CLARA, iris="#F28C28", ceja="#2B2230", ceja_grosor=2,
        cejas=[(22, 23, 28, 22), (36, 22, 41, 23)], boca="sonrisa",
        pelo=P.PELO_NEGRO, peinado=pelo_puntas, ropa=ropa_ryu,
    ),
    "gao": dict(
        piel=P.PIEL_MEDIA, iris="#7A5230", ceja="#2B2230", ceja_grosor=2,
        cejas=[(22, 23, 29, 23), (36, 23, 41, 23)], boca="firme",
        pelo=P.PELO_CAFE, peinado=pelo_corto, ropa=ropa_gao,
    ),
    "nerea": dict(
        piel=P.PIEL_OSCURA, iris="#3A86C8", ceja="#2B2230",
        cejas=[(22, 23, 28, 22), (36, 22, 41, 22)], boca="neutral",
        pelo=P.PELO_NEGRO, lazo="#8FD3F0", peinado=pelo_trenza, ropa=ropa_nerea,
    ),
    "tsering": dict(
        piel=P.PIEL_MEDIA, iris="#9AA3A8", ceja="#F4F1E8", ceja_grosor=2,
        cejas=[(22, 22, 28, 22), (36, 22, 41, 22)], boca="neutral",
        sombras=[(22, 20), (24, 20), (26, 19), (34, 19), (36, 20), (38, 20)],
        pelo=P.PELO_NEGRO, peinado=pelo_calvo, ropa=ropa_tsering, barba=True,
    ),
    "norbu": dict(
        piel=P.PIEL_MEDIA, iris="#E8D27A", ceja="#2B2230",
        cejas=[(21, 21, 28, 24), (36, 24, 42, 21)], boca="firme",
        sombras=[(25, 31), (26, 31), (36, 31)],
        pelo=P.PELO_NEGRO, peinado=pelo_calvo, ropa=ropa_norbu,
    ),
    "daichi": dict(
        piel=P.PIEL_CLARA, iris="#6B8E3D", ceja="#4A3B32", ceja_grosor=2,
        cejas=[(22, 23, 28, 23), (36, 23, 41, 23)], boca="firme",
        sombras=[(24, 31), (25, 31), (36, 31), (37, 31)],
        pelo=P.PELO_CAFE, lazo="#C29A5B", peinado=pelo_daichi, ropa=ropa_daichi,
    ),
}


def pelo_flequillo(R, d, cara):
    """Ryu: pelo corto texturizado con mechones en punta sobre la frente, lados cortos."""
    t = d["pelo"]
    m = poli([(13, 8), (47, 8), (47, 24), (44, 24), (43, 28), (40, 22), (38, 22), (36, 28), (33, 21),
              (31, 21), (29, 28), (26, 21), (24, 21), (22, 28), (19, 22), (16, 24), (13, 24)]) & elipse(30, 21, 17, 17)
    m |= poli([(17, 11), (19, 6), (23, 9)]) | poli([(24, 8), (27, 4), (31, 7)]) | poli([(31, 7), (35, 4), (38, 8)]) | poli([(38, 9), (42, 7), (43, 12)])
    m |= rect(14, 18, 18, 25) | rect(42, 18, 45, 25)
    R.pintar(m, t, 3)
    R.borde_interno(m, t[2], cara)
    for a, b in (((21, 11), (24, 16)), ((28, 8), (30, 14)), ((35, 9), (37, 14))):
        R.color(linea([a, b]), t[1])


def pelo_gao(R, d, cara):
    """Gao: pelo castaño corto con remolino arriba y flequillo desordenado."""
    t = d["pelo"]
    m = poli([(13, 6), (47, 6), (47, 25), (44, 25), (42, 21), (39, 24), (36, 20), (32, 23), (28, 20),
              (24, 24), (21, 21), (18, 27), (13, 27)]) & elipse(30, 22, 16, 17)
    m |= rect(14, 20, 17, 28) | rect(42, 20, 45, 26)
    remolino = poli([(27, 9), (30, 0), (35, 3), (33, 9)])
    R.pintar(m | remolino, t, 3)
    R.borde_interno(m, t[2], cara)
    R.color(linea([(30, 2), (31, 8)]), t[1])
    R.color(linea([(22, 12), (26, 9)]), t[1]); R.color(linea([(36, 10), (40, 13)]), t[1])


def cola_nerea(R, d):
    """Coleta alta: sale de la coronilla y cae por detrás a la derecha."""
    t = d["pelo"]
    cola = poli([(38, 8), (45, 1), (52, 5), (53, 18), (51, 32), (48, 46), (44, 42), (46, 28), (45, 16)])
    R.pintar(cola, t, 2)
    R.color(linea([(48, 6), (49, 30)]), t[1])


def pelo_coleta(R, d, cara):
    """Nerea: flequillo abierto al centro que enmarca la cara + lazo de la coleta."""
    t = d["pelo"]
    m = poli([(10, 4), (50, 4), (50, 26), (44, 26), (42, 22), (36, 19), (31, 22), (30, 22), (25, 19),
              (19, 22), (17, 27), (10, 27)]) & elipse(30, 21, 16, 16)
    m |= poli([(13, 21), (20, 22), (20, 40), (17, 45), (12, 37)])
    m |= poli([(40, 22), (47, 21), (48, 37), (44, 45), (41, 37)])
    R.pintar(m, t, 3)
    R.borde_interno(m, t[2], cara)
    R.color(linea([(30, 7), (30, 20)]), t[2])
    R.color(linea([(20, 12), (26, 9)]), t[1]); R.color(linea([(34, 9), (40, 12)]), t[1])
    R.pintar(poli([(39, 6), (44, 3), (46, 7), (41, 10)]), (d["lazo"], "#8FD3F0", "#1E4F8C"), 1)


def ropa_gao_v3(R, d):
    torso(R, ("#C29A5B", "#E8D27A", "#7A5230"))
    R.pintar(poli([(8, 64), (11, 53), (19, 47), (25, 44), (26, 64)]), P.VERDE_OSC, 2)
    R.pintar(poli([(36, 44), (45, 47), (52, 53), (55, 64), (36, 64)]), P.VERDE_OSC, 2)
    R.pintar(poli([(25, 44), (36, 44), (34, 50), (27, 50)]), ("#7A5230", "#C29A5B", "#4A3B32"), 1)
    R.color(rect(38, 56, 39, 57), "#C29A5B")


def ropa_nerea_v3(R, d):
    torso(R, P.AZUL)
    R.pintar(poli([(25, 44), (36, 44), (34, 64), (27, 64)]), ("#F2F7FA", "#F2F7FA", "#8FD3F0"), 1)
    R.color(linea([(25, 44), (22, 64)]), "#8FD3F0"); R.color(linea([(36, 44), (39, 64)]), "#8FD3F0")
    R.color(rect(9, 60, 20, 63), "#F2F7FA"); R.color(rect(45, 60, 56, 63), "#1E4F8C")


RETRATOS["ryu"] = dict(
    piel=P.PIEL_CLARA, iris="#7A5230", ceja="#2B2230", ceja_grosor=2, cara="cuadrada",
    cejas=[(22, 22, 28, 23), (35, 23, 41, 22)], boca="leve",
    pelo=P.PELO_NEGRO, peinado=pelo_flequillo, ropa=ropa_ryu,
)
RETRATOS["gao"] = dict(
    piel=P.PIEL_MEDIA, iris="#7A5230", ceja="#2B2230", ceja_grosor=2, cara="cuadrada",
    cejas=[(22, 23, 29, 23), (35, 23, 41, 23)], boca="firme",
    pelo=("#7A5230", "#C29A5B", "#4A3B32"), peinado=pelo_gao, ropa=ropa_gao_v3,
)
RETRATOS["nerea"] = dict(
    piel=P.PIEL_CLARA, iris="#3A86C8", ceja="#4A3B32", pestanas=True,
    cejas=[(22, 23, 28, 22), (35, 22, 41, 23)], boca="neutral",
    pelo=("#4A3B32", "#7A5230", "#2B2230"), lazo="#3A86C8",
    atras=cola_nerea, peinado=pelo_coleta, ropa=ropa_nerea_v3,
)


def barba_tsering(R, d, cara):
    b = ("#F4F1E8", "#F4F1E8", "#C8C8C0")
    m = poli([(19, 32), (24, 36), (30, 38), (36, 36), (41, 32), (40, 44), (34, 52), (27, 52), (21, 44)])
    m &= ~elipse(33, 38, 4, 2)   # hueco de la boca
    m &= ~rect(24, 28, 40, 33)
    R.pintar(m, b, 2)
    R.color(linea([(29, 38), (38, 38)]), P.PIEL_MEDIA[2])
    R.pintar(poli([(26, 35), (35, 35), (38, 37), (30, 38), (26, 37)]), b, 1)   # bigote
    R.color(linea([(29, 41), (31, 44)]), b[2]); R.color(linea([(35, 42), (33, 46)]), b[2])


def dibujar(nombre):
    d = RETRATOS[nombre]
    R = Retrato()
    # el pelo largo de Nerea va detrás de todo
    if d.get("atras"):
        d["atras"](R, d)
    d["ropa"](R, d)
    cara = rostro(R, d)
    d["peinado"](R, d, cara)
    if d.get("barba"):
        barba_tsering(R, d, cara)
    img = R.imagen()
    malos = fuera_de_paleta(img)
    assert not malos, f"{nombre}: colores fuera de paleta {malos}"
    return img


def generar(nombres, guardar=True):
    salida = os.path.join(RAIZ, "juego", "assets", "ui")
    os.makedirs(salida, exist_ok=True)
    res = {}
    for n in nombres:
        img = dibujar(n)
        res[n] = img
        if guardar:
            img.save(os.path.join(salida, f"retrato_{n}.png"))
    return res


if __name__ == "__main__":
    nombres = sys.argv[1:] or list(RETRATOS)
    res = generar(nombres)
    E = 6
    hoja = Image.new("RGBA", (len(res) * (N * E + 12) + 12, N * E + 24), (58, 54, 70, 255))
    for i, (n, img) in enumerate(res.items()):
        hoja.alpha_composite(img.resize((N * E, N * E), Image.NEAREST), (12 + i * (N * E + 12), 12))
    ruta = os.path.join(RAIZ, "arte_fuente", "previews", "retratos.png")
    hoja.save(ruta)
    print(ruta)
