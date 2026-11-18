"""Sprites v3: personajes dibujados a mano píxel a píxel (plantillas ASCII).

Cada plantilla es una ventana de 20 columnas (x = 6..25) y 32 filas.
Las letras son "roles" de color que cada personaje traduce a su paleta.
"""
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from paleta import CONTORNO, a_rgb, fuera_de_paleta

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OX = 6


def filas(segmentos):
    """Construye 32 filas de 20 columnas a partir de {fila: [(columna, texto), ...]}."""
    out = []
    for y in range(32):
        f = ["."] * 20
        for x0, txt in segmentos.get(y, []):
            for i, ch in enumerate(txt):
                assert 0 <= x0 + i < 20, (y, x0, txt)
                f[x0 + i] = ch
        out.append("".join(f))
    return out


# ------------------------------------------------------------------ Ryu
# Ryu: pelo corto en puntas con lados rapados, orejas visibles, mandíbula cuadrada,
# cejas gruesas, sonrisa de lado y hombros anchos.
RYU_ABAJO = filas({
    1: [(10, "h")],
    2: [(5, "h"), (9, "hh"), (14, "h")],
    3: [(5, "Hh"), (9, "HHh"), (13, "hH")],
    4: [(4, "HHH"), (8, "HHHHH"), (13, "HHH")],
    5: [(3, "HHHHHHHHHHHHHH")],
    6: [(2, "HHHHggHHHHggHHHH")],
    7: [(2, "HHHHHHggggHHHHHH")],
    8: [(3, "HHHHHHHHHHHHHH")],
    9: [(3, "jHHHjHHHHjHHHj")],
    10: [(3, "jSHHSSHHSSHHSj")],
    11: [(3, "KSEEESSSSEEESK")],
    12: [(2, "S"), (3, "KSSSSSSSSSSSSK"), (17, "S")],
    13: [(2, "K"), (3, "SSSIESSSSEISSS"), (17, "K")],
    14: [(3, "KSSSSSSKSSSSSK")],
    15: [(3, "KSSSSSSSSSSSSK")],
    16: [(4, "KSSSSMMMSSSK")],
    17: [(5, "KKSSSSSSKK")],
    18: [(6, "KKKKKKKK")],
    19: [(2, "cCCCDBBBBBBDCCCD")],
    20: [(1, "cCDCCTBBBBBBTCCDDD")],
    21: [(1, "cCDCCTBBbBBBTCCDDD")],
    22: [(1, "cCDCCTBBBBBBTCCDDD")],
    23: [(1, "TTDCCTBBBBBBTCCDTT")],
    24: [(1, "SSTTTTBBBBBBTTTTKK")],
    25: [(4, "PPPPPPPPPPPP")],
    26: [(4, "pPPPPQQPPPPQ")],
    27: [(5, "pPPP"), (11, "pPPQ")],
    28: [(5, "zZZZ"), (11, "zZZZ")],
    29: [(5, "ZZZZ"), (11, "ZZZZ")],
    30: [(5, "XXXX"), (11, "XXXX")],
})
RYU_COLORES = {
    "H": "#2B2230", "h": "#8E1B1B", "g": "#3B3846", "j": "#24222B",  # pelo negro, puntas rojas
    "S": "#F2C9A0", "s": "#F2C9A0", "K": "#D9A06B",            # piel
    "E": "#2B2230", "I": "#F28C28", "W": "#F4F1E8", "M": "#A86B3C",
    "C": "#D9481E", "c": "#F28C28", "D": "#8E1B1B",            # chaqueta roja
    "B": "#2B2230", "b": "#3B3846",                            # camiseta negra
    "T": "#C9A227",                                            # ribete dorado
    "P": "#3B3846", "p": "#5A5566", "Q": "#24222B",            # pantalón
    "Z": "#D9481E", "z": "#F28C28", "X": "#F4F1E8",            # zapatillas
}

# ------------------------------------------------------------------ Gao
GAO_ABAJO = [
    "....................",  # 0
    "....................",  # 1
    "..........hH........",  # 2
    ".......HHHhHH.......",  # 3
    ".....HHHHHhhHHH.....",  # 4
    "....HHHHHHHhhHHH....",  # 5
    "...HHHHHHHHHHhhHH...",  # 6
    "...jHHHHHHHHHHHHj...",  # 7
    "...jjHHHjHHHHHHjj...",  # 8
    "...jSHHSSHHHSSHSj...",  # 9
    "...jSSHSSSSHSSSSj...",  # 10
    "...jSEEESSSSEEESj...",  # 11
    "...KSSSSSSSSSSSSK...",  # 12
    "...KSSEESSSSEESSK...",  # 13
    "...KSSIESSSSEISSK...",  # 14
    "...KSSSSSSKSSSSSK...",  # 15
    "...KSSSSMMMMSSSSK...",  # 16
    "....KKSSSSSSSSKK....",  # 17
    ".....KKKKKKKKKK.....",  # 18
    ".bBBCCCBBBBBBCCCBBV.",  # 19
    ".bBVcCCBBbBBBCCDBBV.",  # 20
    ".bBVcCCBBBBBBCCDBBV.",  # 21
    ".LLLcCCBBBBBBCCDLLL.",  # 22
    ".LLLRRRRRTTRRRRRLLL.",  # 23
    ".SSSPPPPPPPPPPPPKKK.",  # 24
    "....pPPPPQQpPPPQ....",  # 25
    "....pPPPP..pPPPQ....",  # 26
    "....pPPPQ..pPPPQ....",  # 27
    "....ZZZZZ..ZZZZZ....",  # 28
    "....zZZZZ..ZZZZZ....",  # 29
    "....XXXXX..XXXXX....",  # 30
    "....................",  # 31
]
GAO_COLORES = {
    "H": "#7A5230", "h": "#C29A5B", "j": "#4A3B32",            # pelo castaño
    "S": "#D9A06B", "s": "#F2C9A0", "K": "#A86B3C",
    "E": "#2B2230", "I": "#7A5230", "W": "#F4F1E8", "M": "#A86B3C",
    "C": "#3F5A2A", "c": "#6B8E3D", "D": "#2B2230",            # chaleco verde
    "B": "#C29A5B", "b": "#E8D27A", "V": "#7A5230",            # camiseta arena
    "L": "#7A5230", "R": "#4A3B32", "T": "#C9A227",            # brazaletes y cinturón
    "P": "#7A5230", "p": "#C29A5B", "Q": "#4A3B32",            # pantalón cargo
    "Z": "#4A3B32", "z": "#7A5230", "X": "#2B2230",            # botas
}

# ------------------------------------------------------------------ Nerea (rediseño 2)
# Cola de caballo alta con lazo azul que cae por detrás a la derecha, flequillo abierto
# al centro que enmarca la cara, piel clara, chaqueta corta azul con top blanco y faja celeste.
NEREA_ABAJO = filas({
    1: [(12, "HHh")],
    2: [(11, "HHhHH")],
    3: [(6, "HHHHXx"), (12, "HhHHj")],
    4: [(5, "HHHHHHHHHHH"), (16, "HhH")],
    5: [(4, "HHHHHHHHHHHH"), (16, "HhHj")],
    6: [(3, "HHhhhhHHHHHHH"), (16, "HhHj")],
    7: [(3, "HHHHHhhhhHHHH"), (16, "HhHj")],
    8: [(3, "HHHHHHjjHHHHH"), (16, "HhHj")],
    9: [(3, "HHHHHHSSHHHHH"), (16, "HhHj")],
    10: [(3, "HHHHHSSSSHHHH"), (16, "HhHj")],
    11: [(3, "HHHHSSSSSSHHH"), (16, "HhH")],
    12: [(3, "HHEEESSSSEEEH"), (16, "HhH")],
    13: [(3, "HHSIESSSSEISH"), (16, "HhH")],
    14: [(3, "HHSCSSSKSSCSH"), (16, "HhH")],
    15: [(3, "HHKSSSMMSSSKH"), (16, "HhH")],
    16: [(3, "HH"), (6, "KSSSSSSK"), (15, "H"), (16, "Hhj")],
    17: [(3, "H"), (7, "KKKKKK"), (17, "hj")],
    18: [(3, "ccCCCBBBBCCCDD"), (17, "Hj")],
    19: [(3, "cDCCCBBBBCCCDD"), (17, "Hj")],
    20: [(3, "cDCCCBVBBCCCDD"), (17, "j")],
    21: [(3, "cDTTTTTTTTTTDD"), (17, "j")],
    22: [(3, "XXCCCCtTCCCCXX")],
    23: [(3, "SSCCCCTtCCCCKK")],
    24: [(4, "PPPPPTtPPPPP")],
    25: [(6, "pPP"), (11, "pPQ")],
    26: [(6, "pPP"), (11, "pPQ")],
    27: [(6, "zZZ"), (11, "ZZZ")],
    28: [(6, "zZZ"), (11, "ZZZ")],
    29: [(5, "VVVV"), (11, "VVVV")],
})
NEREA_COLORES = {
    "H": "#4A3B32", "h": "#7A5230", "j": "#2B2230",            # pelo castaño oscuro
    "x": "#8FD3F0", "X": "#3A86C8",                            # lazo de la coleta
    "S": "#F2C9A0", "s": "#F2C9A0", "K": "#D9A06B",            # piel clara
    "E": "#2B2230", "I": "#3A86C8", "W": "#F4F1E8", "M": "#A86B3C",
    "C": "#3A86C8", "c": "#8FD3F0", "D": "#1E4F8C",            # chaqueta azul
    "B": "#F2F7FA", "V": "#8FD3F0",                            # top blanco
    "T": "#8FD3F0", "t": "#F2F7FA",                            # faja celeste
    "P": "#2B2230", "p": "#3B3846", "Q": "#24222B",            # mallas
    "Z": "#F2F7FA", "z": "#F2F7FA",                            # botas
}
NEREA_COLORES["C"] = "#3A86C8"


def _rol_mejilla(colores):
    # 'C' en la cara de Nerea es rubor; en el cuerpo es la chaqueta. Se resuelve por fila.
    return colores


def render(filas, colores, roles_por_fila=None):
    assert len(filas) == 32, len(filas)
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    px = img.load()
    lleno = set()
    for y, fila in enumerate(filas):
        assert len(fila) == 20, (y, fila, len(fila))
        for i, ch in enumerate(fila):
            if ch == ".":
                continue
            c = colores
            if roles_por_fila and y in roles_por_fila and ch in roles_por_fila[y]:
                col = roles_por_fila[y][ch]
            else:
                col = c[ch]
            px[OX + i, y] = a_rgb(col) + (255,)
            lleno.add((OX + i, y))
    for y in range(32):
        for x in range(32):
            if (x, y) in lleno:
                continue
            if any((x + dx, y + dy) in lleno for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = a_rgb(CONTORNO) + (255,)
    malos = fuera_de_paleta(img)
    assert not malos, malos
    return img


PRUEBA = {
    "ryu": (RYU_ABAJO, RYU_COLORES, None),
    "gao": (GAO_ABAJO, GAO_COLORES, None),
    # en la cara de Nerea, 'C' es rubor
    "nerea": (NEREA_ABAJO, NEREA_COLORES, {14: {"C": "#D9A06B"}, 22: {"X": "#F2F7FA"}}),
}

if __name__ == "__main__":
    E = 10
    imgs = [render(*PRUEBA[n]) for n in ("ryu", "gao", "nerea")]
    hoja = Image.new("RGBA", (len(imgs) * 32 * E + 40, 32 * E + 20), (58, 54, 70, 255))
    for i, im in enumerate(imgs):
        hoja.alpha_composite(im.resize((32 * E, 32 * E), Image.NEAREST), (10 + i * (32 * E + 10), 10))
    # también a tamaño real x3 para ver cómo se lee en juego
    real = Image.new("RGBA", (len(imgs) * 40 * 3, 40 * 3), (58, 54, 70, 255))
    for i, im in enumerate(imgs):
        real.alpha_composite(im.resize((96, 96), Image.NEAREST), (12 + i * 120, 12))
    hoja.save(os.path.join(RAIZ, "arte_fuente", "previews", "v3_frente.png"))
    real.save(os.path.join(RAIZ, "arte_fuente", "previews", "v3_frente_x3.png"))
    print("ok")


# ------------------------------------------------------------------ Ryu: dos alternativas más masculinas
_RYU_CARA_CUERPO = {
    10: [(4, "KEESSSSSSEEK")],
    11: [(3, "S"), (4, "KSSESSSSESSK"), (16, "S")],
    12: [(3, "K"), (4, "KSIESSSSEISK"), (16, "K")],
    13: [(4, "KSSSSSKSSSSK")],
    14: [(4, "KKSSSSSSSSKK")],
    15: [(4, "KSSSSMMMSSSK")],
    16: [(5, "KSSSSSSSSK")],
    17: [(6, "KKSSSSKK")],
    18: [(6, "KKKKKKKK")],
    19: [(2, "cCCCDBBBBBBDCCCD")],
    20: [(1, "cCDCCTBBBBBBTCCDDD")],
    21: [(1, "cCDCCTBBbBBBTCCDDD")],
    22: [(1, "cCDCCTBBBBBBTCCDDD")],
    23: [(1, "TTDCCTBBBBBBTCCDTT")],
    24: [(1, "SSTTTTBBBBBBTTTTKK")],
    25: [(4, "PPPPPPPPPPPP")],
    26: [(4, "pPPPPQQPPPPQ")],
    27: [(5, "pPPP"), (11, "pPPQ")],
    28: [(5, "zZZZ"), (11, "zZZZ")],
    29: [(5, "ZZZZ"), (11, "ZZZZ")],
    30: [(5, "XXXX"), (11, "XXXX")],
}

# A: peinado hacia atrás en puntas, lados rapados, un mechón suelto en la frente
RYU_A = filas({
    1: [(7, "h"), (11, "h")],
    2: [(6, "hH"), (10, "hHh"), (14, "h")],
    3: [(5, "HHHhHHHHhHH")],
    4: [(4, "HHHHHHHHHHHH")],
    5: [(4, "HHHggggHHHHH")],
    6: [(4, "jHHHHHHHHHHj")],
    7: [(4, "jjHHHHHHHHjj")],
    8: [(4, "jSSHSSSSSSSj")],
    9: [(4, "KSSHSSSSSSSK")],
    **_RYU_CARA_CUERPO,
})

# B: pelo corto revuelto con bandana roja anudada a un lado
RYU_B = filas({
    3: [(6, "H"), (9, "Hh"), (13, "H")],
    4: [(5, "HHhHHHHhHH")],
    5: [(4, "HHHHHgHHHHHH")],
    6: [(4, "rrrrrrrrrrrr")],
    7: [(4, "RRRRRRRRRRRR"), (16, "RD")],
    8: [(4, "HSHHSSSHHSSH"), (16, "DR")],
    9: [(4, "KSSHSSSSSSSK"), (17, "D")],
    **_RYU_CARA_CUERPO,
})

RYU_COLORES_V2 = dict(RYU_COLORES)
RYU_COLORES_V2.update({"R": "#D9481E", "r": "#F28C28", "D": "#8E1B1B"})


if __name__ == "__main__":
    E = 10
    imgs = [render(RYU_A, RYU_COLORES), render(RYU_B, RYU_COLORES_V2),
            render(*PRUEBA["gao"]), render(*PRUEBA["nerea"])]
    hoja = Image.new("RGBA", (len(imgs) * (32 * E + 10) + 10, 32 * E + 20), (58, 54, 70, 255))
    for i, im in enumerate(imgs):
        hoja.alpha_composite(im.resize((32 * E, 32 * E), Image.NEAREST), (10 + i * (32 * E + 10), 10))
    hoja.save(os.path.join(RAIZ, "arte_fuente", "previews", "v3_ryu_opciones.png"))


# ------------------------------------------------------------------ Ryu shonen: pelo medio despeinado
_CUERPO_RYU = {k: v for k, v in _RYU_CARA_CUERPO.items() if k >= 19}
RYU_SHONEN = filas({
    1: [(6, "H"), (10, "H"), (13, "H")],
    2: [(5, "HH"), (9, "HHH"), (13, "HH")],
    3: [(4, "HHHHHHHHHHHH")],
    4: [(3, "HHHHhhHHHHHHHH")],
    5: [(2, "HHHHHhhhHHHHHHHH")],
    6: [(1, "H"), (2, "HHHHHHHHgggHHHHH"), (18, "H")],
    7: [(2, "HHHHHHHHHHHHHHHH")],
    8: [(2, "HHHjHHHHjHHHHjHH")],
    9: [(2, "H"), (3, "HHHSSSHHSSSHHH"), (17, "H")],
    10: [(2, "j"), (3, "HHEEESHHSEEEHH"), (17, "j")],
    11: [(3, "HHSSSSSHSSSSHH")],
    12: [(4, "HSEEESSEEESH")],
    13: [(5, "SWIESSEIWS")],
    14: [(5, "SSSSSKSSSS")],
    15: [(5, "KSSSMMMSSK")],
    16: [(6, "KSSSSSSK")],
    17: [(7, "KSSSSK")],
    18: [(7, "KKKKKK")],
    **_CUERPO_RYU,
})
RYU_SHONEN_NEGRO = dict(RYU_COLORES)
RYU_SHONEN_NEGRO.update({"H": "#2B2230", "h": "#8E1B1B", "g": "#3B3846", "j": "#1A1420", "E": "#1A1420"})
RYU_SHONEN_ROJO = dict(RYU_COLORES)
RYU_SHONEN_ROJO.update({"H": "#8E1B1B", "h": "#D9481E", "g": "#F28C28", "j": "#2B2230", "E": "#1A1420"})

if __name__ == "__main__":
    E = 10
    imgs = [render(RYU_SHONEN, RYU_SHONEN_NEGRO), render(RYU_SHONEN, RYU_SHONEN_ROJO),
            render(*PRUEBA["gao"]), render(*PRUEBA["nerea"])]
    hoja = Image.new("RGBA", (len(imgs) * (32 * E + 10) + 10, 32 * E + 20), (58, 54, 70, 255))
    for i, im in enumerate(imgs):
        hoja.alpha_composite(im.resize((32 * E, 32 * E), Image.NEAREST), (10 + i * (32 * E + 10), 10))
    hoja.save(os.path.join(RAIZ, "arte_fuente", "previews", "v3_ryu_shonen.png"))
