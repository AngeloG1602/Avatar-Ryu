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

# ------------------------------------------------------------------ Ryu
RYU_ABAJO = [
    "....................",  # 0
    "..........h.........",  # 1
    ".....h...hh...h.....",  # 2
    ".....HH..HHh.HH.....",  # 3
    "....HHH.HHhH.HHH....",  # 4
    "...HHHHHHHHHHHHHH...",  # 5
    "..HHHggHHHHHggHHHH..",  # 6
    ".HHHHHggggggHHHHHHH.",  # 7
    "..HHHHHHHHHHHHHHHH..",  # 8
    "..HHjHHHjHHHjHHHHH..",  # 9
    "..HHSHHSSHHSSHHSHH..",  # 10
    "..HHsSSHSSSSHSSSHH..",  # 11
    "..HHSSEESSSSEESSHH..",  # 12
    "..HHSSIESSSSEISSHH..",  # 13
    "..jHSSSSSSKSSSSSHj..",  # 14
    "....KSSMMMMMSSSK....",  # 15
    ".....KSSSSSSSSK.....",  # 16
    "......KKKKKKKK......",  # 17
    "...cCCDBBBBBBDCCD...",  # 18
    "..ccCCTBBBBBBTCCDD..",  # 19
    "..cDCCTBBbBBBTCCDD..",  # 20
    "..cDCCTBBBBBBTCCDD..",  # 21
    "..TTCCTBBBBBBTCCTT..",  # 22
    "..SSTTTBBBBBBTTTKK..",  # 23
    "....PPPPPPPPPPPP....",  # 24
    "....pPPPPQQPPPPQ....",  # 25
    ".....pPPP..pPPQ.....",  # 26
    ".....pPPP..pPPQ.....",  # 27
    ".....zZZZ..zZZZ.....",  # 28
    ".....ZZZZ..ZZZZ.....",  # 29
    ".....XXXX..XXXX.....",  # 30
    "....................",  # 31
]
RYU_COLORES = {
    "H": "#2B2230", "h": "#8E1B1B", "g": "#3B3846", "j": "#24222B",  # pelo negro, puntas rojas
    "S": "#F2C9A0", "s": "#F2C9A0", "K": "#D9A06B",            # piel
    "E": "#2B2230", "I": "#F28C28", "W": "#F4F1E8", "M": "#2B2230",
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

# ------------------------------------------------------------------ Nerea (rediseño)
# Pelo largo y ondulado con medio moño atado con una cinta azul, flequillo de lado,
# chaqueta corta azul con top blanco, faja celeste anudada, mallas oscuras y botas blancas.
NEREA_ABAJO = [
    "....................",  # 0
    "........jHHj........",  # 1
    "........HhHH........",  # 2
    ".......xXXXXX.......",  # 3
    ".....HHHHHHHHHH.....",  # 4
    "....HHHHHHHHHHHH....",  # 5
    "...HHhhhhHHHHHHH....",  # 6
    "..HHHHHhhhhHHHHHH...",  # 7
    "..HHHHHHHHHHHHHjHH..",  # 8
    "..HHHHHHHHHHjjSSHH..",  # 9
    "..HHHHHHHHjjSSSSHH..",  # 10
    "..HHHHHHjjSSSSSSHH..",  # 11
    "..HHHEEESSSSEEESHH..",  # 12
    "..HHSSIESSSSEISSHH..",  # 13
    "..HHSCSSSSKSSSCSHH..",  # 14
    "..HHKSSSSMMSSSSKHH..",  # 15
    "..HHHKSSSSSSSSKHHH..",  # 16
    ".HhHHHKKKKKKKKHHjHH.",  # 17
    ".HhccCCCBBBBCCCDDHH.",  # 18
    ".HhcDCCCBBBBCCCDDjH.",  # 19
    ".HHcDCCCBVBBCCCDDHH.",  # 20
    ".jHcDTTTTTTTTTTDDHj.",  # 21
    ".HHXXCCCCtTCCCCXXHH.",  # 22
    "..jSSCCCCTtCCCCKKj..",  # 23
    "..HHPPPPPTtPPPPPHH..",  # 24
    "......pPP..pPQ......",  # 25
    "......pPP..pPQ......",  # 26
    "......zZZ..ZZZ......",  # 27
    "......zZZ..ZZZ......",  # 28
    ".....VVVV..VVVV.....",  # 29
    "....................",  # 30
    "....................",  # 31
]
NEREA_COLORES = {
    "H": "#2B2230", "h": "#1E4F8C", "j": "#24222B",            # pelo negro con brillo azul
    "x": "#8FD3F0", "X": "#3A86C8",                            # cinta del moño / puños
    "S": "#A86B3C", "s": "#D9A06B", "K": "#6E4426", "C_": "",
    "E": "#2B2230", "I": "#3A86C8", "W": "#F4F1E8", "M": "#6E4426",
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
